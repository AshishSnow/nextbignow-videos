"""Mix: narrator VO (per-line level automation + room tone) + ducked/carved ragtime score + per-moment SFX -> work/mix.wav (-11 LUFS, -1 dBTP)."""
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
m, _ = sf.read(f"{B}/work/music.wav", dtype="float32"); m = m[:NS]
if len(m) < NS: m = np.pad(m, ((0, NS - len(m)), (0, 0)))
win = int(0.03 * SR); env = np.sqrt(np.convolve(vo ** 2, np.ones(win) / win, "same"))
env = np.clip(env / (np.percentile(env[env > 1e-4], 95) + 1e-9) * 1.6, 0, 1)
g = np.zeros_like(env); prev = 0.0; aa, ar = np.exp(-1 / (0.03 * SR)), np.exp(-1 / (0.4 * SR))
for i in range(0, NS, 48):
    x = env[i]; a_ = aa if x > prev else ar; prev = a_ * prev + (1 - a_) * x; g[i:i + 48] = prev
M = m * (1 - 0.7 * g)[:, None]

# ---- VO level automation: Lizzie's sad beat intimate, reveals lifted ----
LINE_DB = {"i1": +1.0, "b5": +1.0, "c7": +1.0, "d2": -0.3, "d3": -0.5, "f1": -1.0, "t1": +1.0, "e1": +0.5, "c1": +0.5}
gl = np.zeros(NS, np.float32)
for lid, L in LINES.items():
    a0, a1 = int(L["start"] * SR), int(L["end"] * SR); gl[a0:a1] = LINE_DB.get(lid, 0.0)
ramp = int(0.08 * SR); gl = np.convolve(gl, np.ones(ramp) / ramp, "same").astype(np.float32)
vo = vo * 10 ** (gl / 20)
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


def tok(t0, lv=-27):   # wooden pawn tapping on the board
    add(click(lv), t0); add(pop(lv - 4, 520), t0 + 0.005)


def coinsfx(t0, n_=3, lv=-28):
    for j in range(n_): clink(t0 + 0.07 * j, lv - j, 3000 + 260 * j)


# hook: pawn hops (every 1/1.5 s) + WARNING stamp already on screen + reveal
for j in range(int(SHOT["S0"]["end"] * 1.5) + 1): tok(j / 1.5 + 0.4)
add(thud(-17), T("i1", "monopolies") - 0.1)
tf = T("i2", "five") - 0.2; add(chaching(-24), tf + 0.05); add(thud(-17), tf)
add(whoosh(0.5, peak=0.6, f_lo=300, f_hi=2500, level=-24), T("i3", "flipped") - 0.3); add(thud(-15), T("i3", "flipped") + 0.2)
for j in range(4): add(click(-27), SHOT["S3"]["start"] + 0.1 + 0.07 * j)
tp = T("a1", "patent") - 0.3; add(whoosh(0.4, peak=0.5, f_lo=900, f_hi=4000, level=-27), tp); add(thud(-18), tp + 0.4)
coinsfx(T("a3", "rent") - 0.15, 4); add(buzzer(-27, 0.25), T("a3", "jail") - 0.45)
add(thud(-16), T("a4", "message") - 0.3); add(creak(-29, 0.6), T("a5", "grab") - 0.2)
for j in range(2): add(thud(-21), SHOT["S9"]["start"] + 0.25 + 0.2 * j)
tc = T("b2", "crushing") - 0.25
for j in range(4): tok(tc + 0.08 * j + 0.15, -24)
add(boom(-17, 0.4), tc + 0.2)
te = T("b3", "everyone") - 0.25
for j in range(5): clink(te + 0.45 + 0.07 * j, -27, 2800 + 200 * j)
add(pop(-24, 1200), SHOT["S12"]["start"] + 0.3)
add(boom(-15, 0.5), SHOT["S13"]["start"] + 0.05)
tes = T("c1", "escaped") - 0.3
for j in range(8): tok(tes + 0.09 * j, -27)
add(whoosh(0.6, peak=0.5, f_lo=300, f_hi=3000, level=-25), tes + 0.3)
for j in range(9): add(pop(-28, 900 + 60 * j), SHOT["S15"]["start"] + 0.15 + 0.2 * j)
for j in range(10): add(scratch(-34, 0.12), SHOT["S16"]["start"] + 0.2 + 0.2 * j)
for j in range(8): add(scratch(-34, 0.1), SHOT["S18"]["start"] + 0.2 + 0.15 * j)
ts = T("c4", "sold") - 0.25; add(whoosh(0.6, peak=0.5, f_lo=500, f_hi=3500, level=-25), ts); add(chaching(-25), ts + 0.6)
add(thud(-15), T("c5", "invention") - 0.3)
for j in range(12): add(click(-29), SHOT["S21"]["start"] + 0.1 + 0.1 * j)
add(ding(-24, 1568), SHOT["S21b"]["start"] + 0.9)
add(chaching(-22), SHOT["S22"]["start"] + 0.1); coinsfx(SHOT["S22"]["start"] + 0.4, 5, -27)
add(chaching(-28), T("d1", "five") - 0.25)
tj = T("d2", "maker") - 0.3
for j in range(14): add(click(-25), tj + j * 0.9 / 14)
add(ding(-24, 2093), tj + 0.95)
add(thud(-13), T("d3", "Zero") - 0.25); add(boom(-18, 0.5), T("d3", "Zero") - 0.25)
for j in range(5): add(click(-27), SHOT["S27"]["start"] + 0.15 + 0.07 * j)
tct = T("f2", "court") - 0.1; add(thud(-11), tct); add(thud(-15), tct + 0.35)
add(ding(-24, 1760), T("f3", "found") - 0.25); add(ding(-26, 2349), T("f3", "found") - 0.15)
for j in range(6): add(whoosh(0.2, peak=0.5, f_lo=1500, f_hi=5000, level=-32), SHOT["S29b"]["start"] + 0.1 + 0.35 * j)
tw = T("t1", "became") - 0.25; add(boom(-16, 0.45), tw); add(ding(-24, 2093), tw + 0.3)
add(thud(-15), T("t2", "first") - 0.35)
q_ = SHOT["S31b"]["start"] + 0.2
for j in range(12): add(click(-31), q_ + j * 0.1)
add(thud(-17), T("t2", "free") - 0.3)
for j in range(int((SHOT["S33"]["start"] - SHOT["S32"]["start"]) * 1.5)): tok(SHOT["S32"]["start"] + j / 1.5 + 0.3)
add(thud(-16), T("e1", "don't") - 0.15)
add(pop(-21, 900), SHOT["S33"]["start"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
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
