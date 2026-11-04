"""Mix: narrator VO + ducked/carved bedroom-pop score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1.0 dBTP)."""
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
LINE_DB = {"i1": +2.0, "i3": +0.5, "c4": +1.0, "b6": +0.5, "t1": +0.5, "z1": +0.5, "c5": -1.0}
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
add(ding(-27, 1400), 0.05)
# hook: counter ticks up to 999, coin clanks off the barrier
for i in range(9): add(click(-31), 0.04 + i * 0.06)
for tt in (T("i1", "pay"), T("i1", "pay") + 3.3): add(ding(-27, 3100), tt); add(thud(-27), tt)
add(thud(-21), T("i1", "zero?") - 0.05); add(buzzer(-33, 0.2), T("i1", "zero?"))
add(pop(-24, 800), T("i2", "tiny") - 0.15); add(thud(-22), T("i3", "It")); add(scratch(-30), T("i3", "It") + 0.02)
for i in range(4): add(pop(-24, 650 + i * 150), st0("S_four") + 0.2 + i * 0.3)
add(buzzer(-31, 0.25), T("i4", "three") - 0.02)
for sid in ("S_pot", "S_slice", "S_line", "S_booth"): add(pop(-23, 500), st0(sid) + 0.07); add(ding(-29, 1318.5), st0(sid) + 0.07)
_tp = st0("S_pour") + 0.2
for i in range(26): add(ding(-37, 2800 + 900 * rng.random()), _tp + i * 0.16 + 0.05 * rng.random())
add(chaching(-24), T("a3", "eleven") - 0.1)
for i in range(10): add(click(-33), st0("S_dots") + 0.2 + i * 0.17)
add(pop(-25, 900), st0("S_100") + 0.12)
add(chaching(-25), T("b4", "So") - 0.05)
add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=3000, level=-27), st0("S_200") + 0.02)
for i in range(12): add(click(-33), T("b5", "But") + i * 0.09)
add(thud(-22), L0("b6")); add(buzzer(-35, 0.2), L0("b6") + 0.02)
# gate 3: counter rolls, barrier opens; then slam on 999
for i in range(36): add(click(-35 + i * 0.1), L0("c2") + 0.6 + i * (T("c2", "thousand") - L0("c2") - 0.5) / 36)
add(ding(-26, 1568), T("c2", "thousand") + 0.08); add(creak(-29, 0.5), T("c2", "thousand") + 0.1)
add(boom(-19, 0.3), st0("S_out") + 0.05); add(thud(-18), st0("S_out") + 0.05); add(buzzer(-30, 0.35), st0("S_out") + 0.08)
add(ding(-29, 3200), st0("S_penny") + 0.5)
add(pop(-25, 800), T("c5", "pennies") - 0.05)
for i in range(5): add(ding(-35, 2600 + 200 * i), st0("S_share") + 0.2 + i * 0.25)
for i in range(8): add(ding(-36, 3000 + 500 * rng.random()), T("d2", "It") + i * 0.3)
add(scratch(-29), st0("S_deal") + 0.05); add(ding(-29, 3000), st0("S_deal") + 0.75)
add(pop(-25, 900), T("e1", "one") - 0.2)
for i in range(3): add(ding(-34, 2800 + 300 * i), st0("S_flow") + 0.3 + i * 0.5)
add(whoosh(0.5, peak=0.6, f_lo=400, f_hi=2600, level=-30), L0("e3") + 0.1)
add(scratch(-30), st0("S_study") + 0.05); add(pop(-25, 1000), st0("S_swing") + 0.5); add(pop(-25, 700), st0("S_swing") + 0.9)
add(thud(-24), T("t1", "paycheck.") - 0.05); add(scratch(-30), T("t1", "Making") - 0.02)
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-25), L0("z1") - 0.2)
add(pop(-24, 900), T("z1", "YES")); add(pop(-23, 1100), T("z1", "NO."))
for j, f0 in enumerate((1318.5, 1568, 1975.5, 2637)): add(ding(-27, f0), END - 1.2 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-10.2) + sfx, vo)
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
