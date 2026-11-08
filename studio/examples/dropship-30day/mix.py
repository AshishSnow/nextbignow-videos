"""Mix: narrator VO + ducked/carved skiffle score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1.0 dBTP)."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
def st0(sid): return S[sid]
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(31)
db = lambda x: 10 ** (x / 20)
S = {k: st for k, st, _ in SHOTLIST}
v, _ = sf.read(f"{B}/work/vo.wav", dtype="float32")
vo = np.zeros(NS, np.float32); vo[: min(NS, len(v))] = v[:NS]
VO = np.stack([vo, vo], 1)
m, _ = sf.read(f"{B}/work/music.wav", dtype="float32"); m = m[:NS]
if len(m) < NS: m = np.pad(m, ((0, NS - len(m)), (0, 0)))
win = int(0.03 * SR); env = np.sqrt(np.convolve(vo ** 2, np.ones(win) / win, "same"))
env = np.clip(env / (np.percentile(env[env > 1e-4], 95) + 1e-9) * 1.6, 0, 1)
g = np.zeros_like(env); prev = 0.0; aa, ar = np.exp(-1 / (0.03 * SR)), np.exp(-1 / (0.4 * SR))
for i in range(0, NS, 48):
    x = env[i]; a_ = aa if x > prev else ar; prev = a_ * prev + (1 - a_) * x; g[i:i + 48] = prev
M = m * (1 - 0.7 * g)[:, None]
# ---- VO level automation: per-line dB offsets (quiet "secret" lines ~-2.5, reveal lines ~+1) + -60 dB room tone in the gaps ----
LINE_DB = {"i1": +2.0, "i2": +0.8, "a3": +0.4, "d2": +0.8, "d3": +0.4, "t1": +1.0, "z1": +0.5}
gl = np.zeros(NS, np.float32)
for lid, L in LINES.items():
    a0, a1 = int(L["start"] * SR), int(L["end"] * SR); gl[a0:a1] = LINE_DB.get(lid, 0.0)
ramp = int(0.08 * SR); gl = np.convolve(gl, np.ones(ramp) / ramp, "same").astype(np.float32)
vo = vo * 10 ** (gl / 20)
_rt = np.random.default_rng(77).standard_normal(NS); _rt = signal.sosfilt(signal.butter(2, [120, 3500], "band", fs=SR, output="sos"), _rt)
_rt = (_rt / np.sqrt(np.mean(_rt ** 2)) * 10 ** (-60 / 20)).astype(np.float32)
vo = vo + _rt * (np.clip(np.arange(NS) / (0.3 * SR), 0, 1) * np.clip((NS - np.arange(NS)) / (0.8 * SR), 0, 1)).astype(np.float32)
VO = np.stack([vo, vo], 1)
exec(open(f"{_D}/sfx_lib.py").read())

def marker(dur=0.5, level=-34, seed=0):
    """felt marker on a whiteboard: band-passed noise with short squeaky strokes"""
    r = np.random.default_rng(seed); n_ = int(dur * SR); x = r.standard_normal(n_)
    x = signal.sosfilt(signal.butter(2, [1800, 6500], "band", fs=SR, output="sos"), x)
    env_ = np.zeros(n_); p_ = 0
    while p_ < n_:
        L_ = int(r.uniform(0.05, 0.16) * SR); env_[p_:p_ + L_] = np.hanning(min(L_, n_ - p_) * 2)[:min(L_, n_ - p_)][::-1] if False else np.sin(np.linspace(0, np.pi, min(L_, n_ - p_)))
        p_ += L_ + int(r.uniform(0.01, 0.05) * SR)
    sq = np.sin(2 * np.pi * r.uniform(2400, 3200) * np.arange(n_) / SR) * 0.15
    y = (x / (np.std(x) + 1e-9) + sq) * env_ * db(level)
    return np.stack([y, y], 1).astype(np.float32)


def eraser(level=-30):
    n_ = int(0.36 * SR); x = np.random.default_rng(5).standard_normal(n_)
    x = signal.sosfilt(signal.butter(2, [300, 2400], "band", fs=SR, output="sos"), x) * np.sin(np.linspace(0, np.pi, n_)) ** 0.7
    y = x / (np.std(x) + 1e-9) * db(level); return np.stack([y, y], 1).astype(np.float32)


for i, s_ in enumerate(SHOTS[1:], 1):
    if s_["trans"] == "wipe": add(eraser(-29), s_["start"] - 0.02)


def quill(dur=1.6, level=-35, seed=7):
    """dip-pen scratch on parchment: lower, drier strokes than the marker"""
    r = np.random.default_rng(seed); n_ = int(dur * SR); x = r.standard_normal(n_)
    x = signal.sosfilt(signal.butter(2, [900, 4200], "band", fs=SR, output="sos"), x)
    env_ = np.zeros(n_); p_ = 0
    while p_ < n_:
        L_ = int(r.uniform(0.03, 0.09) * SR); m_ = min(L_, n_ - p_); env_[p_:p_ + m_] = np.sin(np.linspace(0, np.pi, m_)) ** 2; p_ += L_ + int(r.uniform(0.01, 0.04) * SR)
    y = x / (np.std(x) + 1e-9) * env_ * db(level); return np.stack([y, y], 1).astype(np.float32)


# ---- SFX: marker squeaks while things are drawn on, one hit per moment ----
def tape_rip(dur=0.45, level=-30, seed=3):
    """packing tape pulled off a roll: a rising crackle"""
    r = np.random.default_rng(seed); n_ = int(dur * SR); x = r.standard_normal(n_) * (r.random(n_) > 0.55)
    x = signal.sosfilt(signal.butter(2, [1200, 7000], "band", fs=SR, output="sos"), x)
    e = np.linspace(0.3, 1, n_) * np.sin(np.linspace(0, np.pi, n_)) ** 0.5
    y = x / (np.std(x) + 1e-9) * e * db(level); return np.stack([y, y], 1).astype(np.float32)


for i, s_ in enumerate(SHOTS[1:], 1): add(marker(0.55, -35, i), s_["start"] + 0.2)
add(marker(0.6, -34, 40), L0("i2") - 0.05); add(stamp_hit(-23), TT("i2", "fifty-three", 0.6) - 0.15)
add(tape_rip(0.45, -30), TT("i3", "supplier", 0.4) - 0.3); add(whoosh(0.5, level=-31), TT("i3", "straight", 0.6) - 0.2)
add(whoosh(0.6, level=-32), S["S_i4"] + 0.3)
for i in range(4): add(pop(-28, 800 + 110 * i), TT("i4", "Four", 0.3) - 0.2 + i * 0.18)
add(pop(-27, 1000), TT("a2", "real", 0.5) - 0.2); add(marker(0.7, -34, 41), L0("a2b") + 0.1)
for i in range(5): add(click(-33), L0("a2b") + 0.6 + i * 0.25)
add(ding(-29, 1568), TT("a2b", "prove", 0.6) + 0.3)
add(marker(0.4, -33, 42), TT("a3", "nothing", 0.4) - 0.1); add(stamp_hit(-26), TT("a3", "thirty", 0.5))
add(pop(-30, 600), TT("b1", "late.", 0.5) - 0.4); add(buzzer(-34, 0.18), TT("b1", "late.", 0.5))
add(whoosh(0.5, level=-31), SHOT["S_b2"]["start"] + 0.2); add(pop(-27, 1000), TT("b2", "new", 0.4) - 0.2); add(pop(-27, 1200), TT("b2", "cancel", 0.5) - 0.2)
add(ding(-29, 1318.5), TT("b3", "yes.", 0.3) - 0.2); add(buzzer(-33, 0.16), TT("b3", "real", 0.5) - 0.3)
for i in range(3): add(clink(0, -30) if False else pop(-30, 1400 + 120 * i), SHOT["S_c1"]["start"] + 0.4 + i * 0.12)
add(chaching(-27), TT("c2", "seven", 0.4) + 0.3); add(stamp_hit(-25), TT("c2", "doesn't", 0.5) - 0.1)
add(stamp_hit(-22), TT("c3", "twenty", 0.3) - 0.2); add(chaching(-26), TT("c3", "nine", 0.4) - 0.2)
add(pop(-26, 900), TT("d1", "supplier's", 0.4) - 0.2)
add(eraser(-31), TT("d2", "seller.", 0.4) - 0.35); add(thud(-22), TT("d2", "seller.", 0.4))
for i in range(12): add(click(-33), TT("d3", "most", 0.3) - 0.3 + i * 0.06)
for i in range(6): add(click(-32), TT("d3", "Honestly?", 0.3) + 0.3 + i * 0.25)
add(whoosh(0.6, level=-31), TT("e1", "deliver", 0.4) - 0.6); add(doorbell(-30), TT("e1", "deliver", 0.4))
add(stamp_hit(-26), TT("e2", "arrives.", 0.5))
add(tape_rip(0.4, -31, 5), SHOT["S_t1"]["start"] + 0.3)
for i in range(6): add(click(-33), SHOT["S_t1"]["start"] + 0.5 + i * 0.25)
add(ding(-29, 1760), TT("t1", "Check", 0.4) + 0.2)
add(pop(-25, 1000), TT("z1", "fast,", 0.4) - 0.2); add(pop(-24, 1180), TT("z1", "cheap?", 0.4) - 0.2)
for j, f0 in enumerate((1046.5, 1318.5, 1568, 2093)): add(ding(-27, f0), END - 1.2 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-9.5) + sfx, vo)
# word guard: no SFX hit / loud note within 12 dB of a word on a phone speaker (GUARD=0 disables; studio/tools/mix_check.py measures it)
if float(os.environ.get("GUARD", 12)) > 0: bed = bed_carve.guard(bed, vo, ld=float(os.environ.get("GUARD", 12)))
mix = VO + bed
# pre-limiter (3 Nov): take the peaks off so loudnorm can stay linear and really reach -11 LUFS (was -11.7..-11.9 on the dynamic path). LIM=0 disables.
if float(os.environ.get("LIM", -8)) < 0:
    from pedalboard import Limiter
    _p = float(np.abs(mix).max()) + 1e-9; _r = 10 ** (-1.0 / 20) / _p   # peak-normalise to -1 dBFS first, so the threshold means the same each video
    mix = Limiter(threshold_db=float(os.environ.get("LIM", -8)), release_ms=120.0)((mix * _r).astype(np.float32).T, SR).T / _r
sf.write(f"{B}/work/mix_pre.wav", mix, SR, subtype="FLOAT")
sf.write(f"{B}/work/stem_vo.wav", vo, SR, subtype="FLOAT"); sf.write(f"{B}/work/stem_bed.wav", bed, SR, subtype="FLOAT")
TGT = -11.0
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{B}/work/mix_pre.wav", "-af", f"loudnorm=I={TGT}:TP=-1.0:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
ln = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
print("loudnorm mode:", ln["normalization_type"], "| pre-master I", ln["input_i"], "TP", ln["input_tp"])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/mix_pre.wav", "-af",
                f"loudnorm=I={TGT}:TP=-1.0:LRA=9:measured_I={ln['input_i']}:measured_TP={ln['input_tp']}:measured_LRA={ln['input_lra']}:"
                f"measured_thresh={ln['input_thresh']}:offset={ln['target_offset']}:linear=true,aresample=48000", "-c:a", "pcm_s16le", f"{B}/work/mix.wav"], check=True)
hp = signal.butter(2, 150, "high", fs=SR, output="sos"); vv = signal.sosfilt(hp, vo); bb = signal.sosfilt(hp, bed.mean(1))
print("VO/bed dB:", " ".join(f"{lid}:{20*np.log10(np.sqrt(np.mean(vv[int(L['start']*SR):int(L['end']*SR)]**2))/np.sqrt(np.mean(bb[int(L['start']*SR):int(L['end']*SR)]**2)+1e-12)):.0f}" for lid, L in LINES.items()))

