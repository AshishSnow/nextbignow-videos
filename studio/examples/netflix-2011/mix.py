"""Mix: narrator VO + ducked/carved whistle-pop score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1.0 dBTP)."""
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
LINE_DB = {"i1": +2.0, "b5": +1.0, "c2": +0.8, "c3": +0.8, "c4": -1.5, "d1": +0.6, "t1": +1.0, "z1": +0.5}
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


def env_slide(level=-30, dur=0.45, seed=3):
    """paper envelope sliding: soft low band noise swell"""
    n_ = int(dur * SR); x = np.random.default_rng(seed).standard_normal(n_)
    x = signal.sosfilt(signal.butter(2, [500, 3200], "band", fs=SR, output="sos"), x) * np.sin(np.linspace(0, np.pi, n_)) ** 1.5
    y = x / (np.std(x) + 1e-9) * db(level); return np.stack([y, y], 1).astype(np.float32)


# ---- SFX: marker squeaks while things are drawn on, one hit per moment ----
for i, s_ in enumerate(SHOTS[1:], 1): add(marker(0.55, -35, i), s_["start"] + 0.2)
add(marker(0.5, -34, 40), 0.05)
for i in range(14): add(click(-33), 0.15 + i * 0.11)                                  # frame 0: the counter runs down
add(env_slide(-30), TT("i1", "July", 0.6) - 0.3)
add(pop(-28, 900), TT("i2", "price", 0.4) - 0.3); add(pop(-28, 1100), TT("i2", "name.", 0.4) - 0.4)
for i in range(5): add(env_slide(-34, 0.25, 10 + i), TT("i3", "DVDs", 0.3) - 0.5 + i * 0.1)
add(chaching(-28), TT("i3", "DVDs", 0.3) + 0.35)
add(whoosh(0.5, level=-31), TT("i4", "two", 0.3) - 0.2); add(pop(-28, 800), TT("i4", "Neither", 0.3) - 0.1)
add(scratch(-27, 0.25), TT("a1", "split", 0.4) - 0.05)
add(pop(-28, 1000), TT("a2", "nine", 0.3) - 0.3)
add(pop(-29, 900), SHOT["S_a3"]["start"] + 0.1); add(pop(-29, 1000), SHOT["S_a3"]["start"] + 0.6)
add(chaching(-25), TT("a3", "fifteen", 0.3) - 0.1); add(stamp_hit(-25), TT("a3", "sixty", 0.3))
for i in range(6): add(pop(-31, 700 + 60 * i), SHOT["S_a4"]["start"] + 0.2 + i * 0.1)
add(whoosh(0.7, level=-30), TT("a4", "cancelling.", 0.3) + 0.2)
add(marker(0.9, -33, 47), TT("b1", "messed", 0.3) - 0.6)
add(stamp_hit(-26), TT("b2", "own", 0.3) - 0.1); add(env_slide(-30), SHOT["S_b2"]["start"] + 0.2)
add(marker(0.6, -32, 48), L0("b3") - 0.1)
add(pop(-27, 1100), TT("b4", "Somebody", 0.3) - 0.3); add(stamp_hit(-22), TT("b4", "Twitter.", 0.3) - 0.2)
add(scratch(-20, 0.4), TT("b5", "Oops.", 0.2) - 0.25); add(stamp_hit(-21), TT("b5", "Oops.", 0.2))
add(pop(-28, 900), TT("b6", "Twenty-two", 0.3) - 0.3); add(eraser(-28), TT("b6", "website", 0.4) - 0.4); add(stamp_hit(-23), TT("b6", "no", 0.4) - 0.3)
add(marker(0.6, -33, 49), TT("c1", "stays.", 0.3) - 0.2); add(pop(-28, 800), TT("c1", "count", 0.3) - 0.4)
for i in range(7): add(env_slide(-35, 0.3, 30 + i), SHOT["S_c2"]["start"] + 0.2 + (i + 3) * 0.12)
for i in range(10): add(click(-33), TT("c3", "thirty-five", 0.3) - 0.9 + i * 0.07)
add(boom(-22), TT("c3", "thirty-five", 0.3) - 0.1)
add(eraser(-31), TT("c4", "scrapped", 0.3) - 0.2)
add(stamp_hit(-23), TT("d1", "kept", 0.3) - 0.2); add(marker(0.8, -33, 50), TT("d1", "quickly", 0.3))
add(ding(-28, 1568), TT("d2", "where.", 0.3)); add(pop(-27, 600), TT("d2", "fast.", 0.3))
add(chaching(-25), TT("d3", "More", 0.3) - 0.2)
add(env_slide(-28, 0.6), TT("d4", "last", 0.3)); add(thud(-26), TT("d4", "last", 0.3) + 0.55)
add(pop(-27, 1000), TT("t1", "explaining", 0.3) - 0.2); add(ding(-29, 1760), TT("t1", "why", 0.3))
add(pop(-25, 1000), TT("z1", "Keep", 0.4) - 0.2); add(pop(-24, 1180), TT("z1", "split,", 0.4, 1) - 0.2)
for j, f0 in enumerate((1568, 1318.5, 1174.7, 1568)): add(ding(-27, f0), END - 1.2 + j * 0.09)

sfx *= db(-4.0)
bed = bed_carve.carve(M * db(-14.0) + sfx, vo)
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

