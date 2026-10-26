"""Mix: energetic narrator VO + ducked/carved swing score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1 dBTP)."""
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
exec(open(f"{_D}/sfx_lib.py").read())

for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-23), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-26), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-25), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-21, 700 + 120 * i), st + 0.02); add(thud(-20), st + 0.02)
# S0 hook: cinema + popcorn burst + ticket
add(pop(-23, 900), 0.05); add(thud(-17), 0.25)
for j in range(8): add(pop(-30, 900 + 90 * j), 0.2 + 0.09 * j)
tp = T("i1", "popcorn…") - 0.15; add(pop(-20, 1300), tp); add(ding(-25, 1568), tp + 0.05)
tt = T("i1", "ticket") - 0.15; add(thud(-14), tt); add(whoosh(0.3, level=-26), tt - 0.2)
# S0b crazy / math
add(pop(-22, 1000), T("i2", "crazy.") - 0.2)
for j in range(4): add(pop(-24, 1100 + 150 * j), T("i2", "math!") - 0.2 + 0.06 * j)
add(boom(-19, 0.3), T("i2", "math!") - 0.2)
# S1 ticket + price
add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=3000, level=-26), SHOT["S1"]["start"]); add(thud(-14), T("a1", "twelve") - 0.15); add(chaching(-20), T("a1", "twelve") - 0.05)
# S1b pie: slice grows, flies to studio, kept
swish(T("a2", "half") - 0.2, -23); add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=3500, level=-24), T("a2", "studio!") - 0.35); add(thud(-15), T("a2", "studio!") - 0.2)
add(pop(-20, 1200), T("a3", "keeps") - 0.15); add(ding(-24, 1568), T("a3", "fifty-two") - 0.1)
# S2 snack bar
for j in range(6): add(pop(-29, 700 + 80 * j), SHOT["S2"]["start"] + 0.3 + 0.1 * j)
clink(SHOT["S2"]["start"] + 0.25, -24); add(thud(-14), T("b1", "sixty") - 0.25); add(chaching(-19), T("b1", "sixty") - 0.15)
# S2b x-ray, cost, kept
add(scratch(-26), T("b2", "itself?") - 0.25); add(pop(-21, 900), T("b2", "twenty") - 0.2); add(buzzer(-29), T("b2", "twenty") - 0.1)
add(thud(-14), T("b3", "eighty") - 0.15); add(ding(-22, 2093), T("b3", "eighty") - 0.05); add(chaching(-21), T("b3", "stays") - 0.1)
# S3 bars rise
for j in range(3): add(whoosh(0.35, peak=0.8, f_lo=200, f_hi=2000 + 500 * j, level=-28), SHOT["S3"]["start"] + 0.15 + 0.15 * j)
add(thud(-15), T("c1", "third") - 0.15); add(pop(-21, 1200), T("c1", "third") - 0.1)
# S3b balance scale
add(creak(-24), T("c2", "billion") - 0.4); clink(T("c2", "billion") - 0.2, -22); clink(T("c3", "billion") - 0.25, -23)
add(creak(-25), T("c3", "tie!") - 0.4); add(boom(-17, 0.35), T("c3", "tie!") - 0.3); add(ding(-23, 1568), T("c3", "tie!") - 0.2)
# S4 door -> bills paid
add(creak(-24), SHOT["S4"]["start"] + 0.2); add(pop(-22, 900), SHOT["S4"]["start"] + 0.25)
for j in range(3):
    tq = T("d1", "popcorn") - 0.2 + 0.25 + 0.18 * j; add(pop(-22, 1000 + 150 * j), tq); add(thud(-18), tq + 0.3)
# S5 twist / loss
for j in range(6): add(pop(-29, 800 + 60 * j), SHOT["S5"]["start"] + 0.25 + 0.1 * j)
add(boom(-15, 0.5), T("f1", "lost") - 0.2); add(thud(-13), T("f1", "lost") - 0.15); add(buzzer(-25), T("f1", "lost") + 0.1)
# S5b bills drop
for w_ in ("Rent,", "staff", "debt"): add(thud(-17), T("f2", w_) - 0.15); add(pop(-23, 900), T("f2", w_) - 0.05)
# S6 blockbuster
add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=3500, level=-24), T("e1", "blockbuster!") - 0.5); add(boom(-18, 0.3), T("e1", "blockbuster!") - 0.3)
add(ding(-23, 1568), T("e1", "blockbuster!") - 0.2); add(ding(-25, 2093), T("e1", "blockbuster!") - 0.1)
# S7 send + sting
add(pop(-21, 900), SHOT["S7"]["start"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
vend = LINES["e2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
for j, f0 in enumerate((1046.5, 1318.5, 1568, 2093)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

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
