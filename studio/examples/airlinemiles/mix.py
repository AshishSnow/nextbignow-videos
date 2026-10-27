"""Mix: narrator VO (per-line level automation + room tone) + ducked/carved bossa-nova score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1 dBTP)."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
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

# ---- VO level automation (this run's audio upgrade): intimate "secret" lines a bit quieter, reveal lines a bit louder ----
LINE_DB = {"c3": -1.5, "t1": -2.0, "a2": +1.0, "b3": +1.0, "d3": +1.0, "e1": +0.5, "i1": +1.0}   # catch line intimate; reveals lifted
gl = np.zeros(NS, np.float32)
for lid, L in LINES.items():
    a0, a1 = int(L["start"] * SR), int(L["end"] * SR); gl[a0:a1] = LINE_DB.get(lid, 0.0)
ramp = int(0.08 * SR); gl = np.convolve(gl, np.ones(ramp) / ramp, "same").astype(np.float32)
vo = vo * 10 ** (gl / 20)
# room tone: very low filtered noise so the gaps between lines aren't digital silence (A/B: UTMOS 4.30 -> 4.29, within noise)
_rt = rng.standard_normal(NS); _rt = signal.sosfilt(signal.butter(2, [120, 3500], "band", fs=SR, output="sos"), _rt)
_rt = (_rt / np.sqrt(np.mean(_rt ** 2)) * 10 ** (-60 / 20)).astype(np.float32)
_fade = np.clip(np.arange(NS) / (0.3 * SR), 0, 1) * np.clip((NS - np.arange(NS)) / (0.8 * SR), 0, 1)
vo = vo + _rt * _fade.astype(np.float32)
VO = np.stack([vo, vo], 1)
exec(open(f"{_D}/sfx_lib.py").read())


for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-23), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-26), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-25), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-21, 700 + 120 * i), st + 0.02); add(thud(-20), st + 0.02)
# S0 hook: jet hum flyby, cash flutter, $8B stamp
add(whoosh(2.5, peak=0.5, f_lo=80, f_hi=900, level=-31), 0.0)
for j in range(10): add(pop(-39, 500 + 30 * j), 0.15 + 0.32 * j)
te = T("i1", "eight") - 0.2; add(thud(-16), te); add(boom(-20, 0.4), te); add(chaching(-24), te + 0.05)
# S1 cheque slides + PAID stamp
add(whoosh(0.5, peak=0.6, f_lo=300, f_hi=3000, level=-24), SHOT["S1"]["start"]); add(thud(-14), T("i2", "Delta") - 0.1)
# S2 bars, ? , $5.8B
add(whoosh(0.6, peak=0.6, f_lo=200, f_hi=2400, level=-25), SHOT["S2"]["start"] + 0.05); add(pop(-23, 900), SHOT["S2"]["start"] + 0.45)
add(whoosh(0.6, peak=0.6, f_lo=200, f_hi=2400, level=-25), SHOT["S2b"]["start"]); add(thud(-17), T("a1", "Five") + 0.5)
# S3 balance tips
tb = T("a2", "bigger") - 0.2; add(creak(-24, 0.6), tb); add(thud(-14), tb + 0.4); add(boom(-17, 0.4), tb + 0.4)
# S4 jets fly in
for j in range(3): add(whoosh(1.0, peak=0.45, f_lo=120, f_hi=1600, level=-25), SHOT["S4"]["start"] + 0.15 * j)
# S5 odometer
tf = T("b1", "fifty") - 0.25
for j in range(16): add(click(-31), tf + 0.06 * j)
add(ding(-23, 1568), tf + 1.0)
# S6 profit sliver
tm = T("b2", "million") - 0.3; add(pop(-20, 1400), tm); add(boom(-18, 0.3), tm)
# S7 bar rises, 56x stamp
t62 = T("b3", "six") - 0.25; add(whoosh(0.7, peak=0.6, f_lo=200, f_hi=2400, level=-24), t62 - 0.1); add(chaching(-19), t62 + 0.5); add(thud(-13), t62 + 0.9); add(boom(-17, 0.4), t62 + 0.9)
# S8 / S8b miles burst
tym = T("c1", "Your") - 0.15; add(boom(-17, 0.35), tym)
for j in range(10): add(pop(-29, 700 + 60 * j), tym + 0.05 + 0.04 * j)
# S9 swipe -> approved, bank pays, miles back
tsw = T("c2", "swipe") - 0.1; card_in(tsw, -24); add(beep(-25, 2200, 0.1), tsw + 0.3); add(ding(-25, 1760), tsw + 0.4)
tpy = T("c2", "pays") - 0.1; add(chaching(-21), tpy + 0.3)
for j in range(4): add(pop(-29, 1000 + 120 * j), SHOT["S9b"]["start"] + 0.6 + 0.18 * j)
# S10 confetti / bank / odometer
add(pop(-22, 1200), SHOT["S10"]["start"] + 0.05); add(pop(-24, 1400), SHOT["S10"]["start"] + 0.2)
for j in range(5): add(click(-33), SHOT["S10b"]["start"] + 0.2 * j)
ta = T("c3", "adds") - 0.15
for j in range(10): add(click(-32), ta + 0.07 * j)
add(ding(-24, 2093), ta + 0.8)
# S11 re-hook: airport PA chime + split-flap clatter
add(ding(-21, 1046.5), SHOT["S11"]["start"] + 0.05); add(ding(-22, 830.6), SHOT["S11"]["start"] + 0.42)
for j in range(18): add(click(-34), SHOT["S11"]["start"] + 0.1 + 0.04 * j)
t20 = T("d1", "twenty") - 0.3
for j in range(14): add(click(-33), t20 + 0.045 * j)
add(boom(-16, 0.4), t20 + 0.65)
# S12 parked, stamp
add(whoosh(1.5, peak=0.3, f_lo=80, f_hi=700, level=-27), SHOT["S12"]["start"]); add(thud(-13), T("d2", "parked") - 0.2)
# S12b cash, S12c chains + padlock
t68 = T("d2", "six") - 0.25; add(chaching(-20), t68 + 0.2)
for j in range(7): add(pop(-31, 600 + 40 * j), t68 + 0.12 * j)
for j in range(6): clink(SHOT["S12c"]["start"] + 0.25 + 0.2 * j, -27, 2600 + 200 * j)
tsec = T("d2", "security") - 0.2; add(thud(-13), tsec); add(click(-20), tsec + 0.05); add(boom(-17, 0.4), tsec)
# S13 price tag
t22 = T("d3", "twenty") - 0.25; add(boom(-15, 0.45), t22); add(chaching(-20), t22 + 0.05)
# S14 catch sign, dial drops, rulebook pages, stamp
add(pop(-21, 900), SHOT["S14"]["start"] + 0.12)
tw = T("t1", "worth") - 0.2; add(whoosh(0.7, peak=0.6, f_lo=600, f_hi=200, level=-26), tw)
for j in range(4): add(whoosh(0.25, peak=0.5, f_lo=1500, f_hi=5000, level=-31), SHOT["S14c"]["start"] + 0.1 + 0.62 * j)
tay = T("t1", "any") - 0.2; add(thud(-13), tay); add(boom(-18, 0.35), tay)
# S15 coin pile
for j in range(22): clink(SHOT["S15"]["start"] + 0.07 * j, -32, 2800 + 90 * (j % 7))
add(boom(-17, 0.4), T("t2", "ten") - 0.25)
# S16 shrink + checklist
add(whoosh(1.0, peak=0.6, f_lo=1200, f_hi=200, level=-26), T("t3", "shrink") - 0.2)
for nm in ("Earn", "use"): add(ding(-24, 1760), T("t3", nm) - 0.1)
add(buzzer(-24, 0.35), T("t3", "hoard") - 0.15)
# S17 suitcase X, loop back to the card
ti = T("e1", "isn't") - 0.1; add(scratch(-25, 0.25), ti); add(scratch(-25, 0.25), ti + 0.3)
add(whoosh(2.0, peak=0.4, f_lo=80, f_hi=900, level=-26), SHOT["S17b"]["start"]); add(chaching(-21), SHOT["S17b"]["start"] + 0.15)
# S18 send + sting
add(pop(-21, 900), SHOT["S18"]["start"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
vend = LINES["e2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
for j, f0 in enumerate((1318.5, 1568, 1975.5, 2637)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-12.0) + sfx, vo)
mix = VO + bed
sf.write(f"{B}/work/mix_pre.wav", mix, SR, subtype="FLOAT")
TGT = -11.0
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{B}/work/mix_pre.wav", "-af", f"loudnorm=I={TGT}:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
ln = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/mix_pre.wav", "-af",
                f"loudnorm=I={TGT}:TP=-1.5:LRA=9:measured_I={ln['input_i']}:measured_TP={ln['input_tp']}:measured_LRA={ln['input_lra']}:"
                f"measured_thresh={ln['input_thresh']}:offset={ln['target_offset']}:linear=true,aresample=48000", "-c:a", "pcm_s16le", f"{B}/work/mix.wav"], check=True)
hp = signal.butter(2, 150, "high", fs=SR, output="sos"); vv = signal.sosfilt(hp, vo); bb = signal.sosfilt(hp, bed.mean(1))
print("VO/bed dB:", " ".join(f"{lid}:{20*np.log10(np.sqrt(np.mean(vv[int(L['start']*SR):int(L['end']*SR)]**2))/np.sqrt(np.mean(bb[int(L['start']*SR):int(L['end']*SR)]**2)+1e-12)):.0f}" for lid, L in LINES.items()))
