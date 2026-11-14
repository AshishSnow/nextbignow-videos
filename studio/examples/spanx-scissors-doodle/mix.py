"""Mix: narrator VO + ducked/carved pop-funk score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1.0 dBTP)."""
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
LINE_DB = {"i1": +1.5, "i2": +0.6, "t1": +0.5, "g1": +0.6, "z1": +0.5}
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

# ---- SFX: one hit per anime moment (CUES in anim_shots.py) ----
def sparkle(level=-27):
    out = np.zeros((int(0.6 * SR), 2), np.float32)
    for j, f0 in enumerate((2093, 2637, 3136, 4186)):
        tt_ = np.arange(int(0.3 * SR)) / SR; y = np.sin(2 * np.pi * f0 * tt_) * np.exp(-tt_ / 0.08) * db(level)
        a0 = int(j * 0.05 * SR); out[a0:a0 + len(y)] += np.stack([y, y], 1)
    return out


def car_putt(dur=1.4, level=-30):
    tt_ = np.arange(int(dur * SR)) / SR; f = 14 + 4 * np.sin(tt_ * 3)
    x = (np.sin(2 * np.pi * np.cumsum(f) / SR) > 0.6).astype(np.float32) * np.random.default_rng(3).standard_normal(len(tt_))
    x = signal.sosfilt(signal.butter(2, [80, 900], "band", fs=SR, output="sos"), x) * np.sin(np.linspace(0, np.pi, len(tt_))) ** 0.5
    y = x / (np.std(x) + 1e-9) * db(level); return np.stack([y, y], 1).astype(np.float32)


def ring(level=-26):
    tt_ = np.arange(int(0.7 * SR)) / SR; y = (np.sin(2 * np.pi * 1400 * tt_) + np.sin(2 * np.pi * 1750 * tt_)) * (np.sin(2 * np.pi * 18 * tt_) > 0) * db(level) * np.exp(-tt_ / 0.5)
    return np.stack([y, y], 1).astype(np.float32)


def buzz(level=-26):
    tt_ = np.arange(int(0.35 * SR)) / SR; y = signal.sawtooth(2 * np.pi * 110 * tt_) * db(level) * np.exp(-tt_ / 0.25)
    y = signal.sosfilt(signal.butter(2, 1800, "low", fs=SR, output="sos"), y); return np.stack([y, y], 1).astype(np.float32)


def boing(level=-25):
    tt_ = np.arange(int(0.45 * SR)) / SR; f = 220 + 160 * np.sin(2 * np.pi * 9 * tt_) * np.exp(-tt_ / 0.25)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt_ / 0.18) * db(level); return np.stack([y, y], 1).astype(np.float32)


KIND = {"whoosh": lambda: whoosh(0.4, level=-24), "pop": lambda: pop(-25, 1100), "impact": lambda: boom(-18, 0.5), "slam": lambda: thud(-20),
        "truck": lambda: car_putt(1.2, -31), "ding": lambda: ding(-25, 1760), "ring": lambda: ring(-27), "buzz": lambda: buzz(-25),
        "spray": lambda: whoosh(0.5, f_lo=3000, f_hi=9000, level=-29), "chaching": lambda: chaching(-22),
        "stamp": lambda: thud(-19), "inflate": lambda: whoosh(1.0, f_lo=200, f_hi=1200, level=-29), "boing": lambda: boing(-25),
        "slide": lambda: whoosh(0.6, f_lo=150, f_hi=900, level=-27), "tick": lambda: scratch(-27, 0.18)}
for ti, kind in CUES: add(KIND[kind](), ti - 0.02)
for s_ in SHOTS[1:]:
    if s_["trans"] == "whip": add(whoosh(0.3, level=-25), s_["start"] - 0.04)
    if s_["trans"] == "pop": add(pop(-28, 1400), s_["start"])
for j, f0 in enumerate((1174.7, 1480, 1760, 2349.3)): add(ding(-27, f0), END - 1.3 + j * 0.09)


sfx = np.nan_to_num(sfx); sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-16.5) + sfx, vo)   # owner 13 Nov: keep music low   # owner 8 Nov: "not music loud" (-5.3 dB vs v2)
# word guard: no SFX hit / loud note within 12 dB of a word on a phone speaker (GUARD=0 disables; studio/tools/mix_check.py measures it)
if float(os.environ.get("GUARD", 16)) > 0: bed = bed_carve.guard(bed, vo, ld=float(os.environ.get("GUARD", 16)))
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
