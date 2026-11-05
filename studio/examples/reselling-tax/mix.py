"""Mix: narrator VO + ducked/carved lo-fi hip-hop score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1.0 dBTP)."""
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
LINE_DB = {"i1": +2.0, "i3": +0.5, "i5": +0.5, "d3": +0.5, "t1": +1.0, "z1": +0.5}
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

for i, s_ in enumerate(SHOTS[1:], 1):
    k = s_["trans"]; st = s_["start"]
    if k == "whip": add(whoosh(0.4, level=-23), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-26), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-25), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-21, 700 + 120 * i), st + 0.02); add(thud(-20), st + 0.02)
# ---- SFX: one per moment, nothing under a word that needs to be heard (the guard handles the rest) ----
H = st0
add(hanger(-28), 0.02); add(hanger(-31, 2650), 0.14)
add(stamp_hit(-22), TT("i1", "no", 0.34)); add(stamp_hit(-21), TT("i1", "can.", 0.72))
add(rattle(0.5, -31), H("S_closet") + 0.3); add(hanger(-30), TT("i2", "closet", 0.8) - 0.2)
add(pop(-26, 800), TT("i3", "eighty", 0.35)); add(scratch(-30, 0.16), TT("i3", "twenty.", 0.62)); add(pop(-25, 620), TT("i3", "twenty.", 0.62)); add(stamp_hit(-21), TT("i3", "no", 0.92))
add(pop(-25, 900), TT("i4", "five", 0.4)); add(chaching(-27), TT("i4", "thirty.", 0.88)); add(whoosh(0.4, peak=0.6, f_lo=400, f_hi=3000, level=-29), TT("i4", "thirty.", 0.88))
add(stamp_hit(-19), TT("i5", "income.", 0.32))
_tf = TT("i5", "four", 0.75)
for i in range(4): add(hanger(-30, 2100 + i * 220), _tf - 0.1 + i * 0.17)
add(thud(-26), TT("i5", "Step", 0.82))
for k in ("S_s1", "S_s2", "S_s3", "S_s4"): add(rewind(0.42, -30), H(k) - 0.3); add(hanger(-30), H(k) + 0.05)
add(pop(-26, 860), TT("a1", "Find", 0.45)); add(pop(-26, 980), TT("a2", "actually", 0.62)); add(ding(-29, 1760), TT("a2", "actually", 0.62) + 0.04)
add(tape_zip(0.9, -31), H("S_s2") + 0.15)
add(ding(-29, 2200), TT("b2", "fourteen", 0.62)); add(pop(-27, 1200), TT("b2", "order", 0.9))
for tt_ in (TT("b3", "five", 0.3), TT("b3", "Then", 0.5) + 0.5): add(click(-30), tt_); add(click(-32), tt_ + 0.05)
add(chaching(-26), TT("b4", "twenty,", 0.42)); add(thud(-27), TT("b4", "postage", 0.68))
for i in range(5): add(scratch(-36, 0.12), H("S_s3") + 0.7 + i * 0.42)
for i in range(2): add(scratch(-33, 0.3), H("S_list") + 0.2 + i * 0.7)
add(stamp_hit(-23), TT("c2", "profit,", 0.66) - 0.1)
add(boom(-24, 0.3), H("S_s4") + 0.02)
_t2 = TT("d2", "two", 0.86)
for i in range(10): add(click(-36 + i * 0.3), H("S_us") + 0.3 + i * (TT("d2", "twenty", 0.62) - H("S_us")) / 10)
for i in range(8): add(click(-36 + i * 0.3), _t2 - 0.9 + i * 0.12)
add(ding(-27, 1568), _t2 + 0.15); add(stamp_hit(-19), TT("d3", "all", 0.55))
add(thud(-24), H("S_400") + 0.05); add(pop(-26, 720), TT("d4", "Less", 0.68)); add(stamp_hit(-25), TT("d4", "Less", 0.68) + 0.5)
_tt = TT("d5", "thirty", 0.42); _d = max(0.02, (_tt - H("S_uk") + 0.2) / 30)
for i in range(0, 30, 2): add(click(-35), H("S_uk") + 0.05 + i * _d)
add(ding(-28, 2093), H("S_uk") + 0.05 + 29 * _d); add(whoosh(0.5, peak=0.6, f_lo=500, f_hi=3200, level=-29), TT("d5", "tells", 0.8) - 0.15)
add(stamp_hit(-22), TT("d6", "reported", 0.62)); add(stamp_hit(-22), TT("d6", "nothing.", 0.95) - 0.25); add(ding(-29, 2637), TT("d6", "nothing.", 0.95))
for i in range(8): add(click(-36), H("S_buy") + 0.4 + i * (TT("d7", "thousand", 0.68) - H("S_buy")) / 8)
add(buzzer(-33, 0.18), TT("d7", "thousand", 0.68) + 0.05); add(pop(-25, 1000), TT("d7", "tell", 0.9) - 0.15)
add(stamp_hit(-22), H("S_both") + 0.5); add(stamp_hit(-21), TT("t1", "No", 0.5) + 0.5)
add(pop(-25, 900), TT("t2", "Unsure?", 0.45))
add(hanger(-29), H("S_end") + 0.05); add(pop(-24, 900), TT("z1", "Fair", 0.5) - 0.03); add(pop(-23, 1120), TT("z1", "Fair", 0.5) + 0.12)
add(thud(-27), L0("z2") + 0.42)
for j, f0 in enumerate((1318.5, 1568, 1975.5, 2637)): add(ding(-27, f0), END - 1.2 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-8.2) + sfx, vo)
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
