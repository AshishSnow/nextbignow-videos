"""Mix: narrator VO (per-line level automation + room tone) + ducked/carved noir-jazz score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1 dBTP)."""
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
LINE_DB = {"a3": -1.5, "c3": -2.0, "b4": -1.0, "a2": +1.0, "a4": +1.0, "b5": +1.0, "d3": +1.0, "d5": +1.0, "e1": +0.5, "i1": +1.0}   # secret lines intimate; reveals lifted
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


def shimmer(t0, lv=-29, n_=5):   # diamond glint: a quick rising run of high dings
    for j in range(n_): add(ding(lv - 2 * j, 2637 + 330 * j), t0 + 0.05 * j)


# S0 hook: sparkle glints + tag swing + reveal thud
shimmer(0.05, -27); add(creak(-33, 0.6), 0.3)
tt = T("i1", "two") - 0.2; add(thud(-17), tt); add(chaching(-25), tt + 0.05)
# S1 RARE* stamp
tr = T("i2", "rare") - 0.15; add(thud(-14), tr); add(boom(-19, 0.35), tr)
# S2 three folders flip
for j in range(3): add(whoosh(0.25, peak=0.5, f_lo=900, f_hi=4000, level=-29), SHOT["S2"]["start"] + 0.25 + 0.18 * j); add(pop(-27, 900 + 150 * j), SHOT["S2"]["start"] + 0.4 + 0.18 * j)
# S3/S5b hourglass: gem drops tick
for sid in ("S3", "S5b"):
    a_, b_ = SHOT[sid]["start"], SHOT[sid]["end"]; tq = a_ + 0.3
    while tq < b_ - 0.2: clink(tq, -31, 3600); tq += 1.43
# S4 pie fills
tn = T("a2", "ninety") - 0.25; add(whoosh(0.9, peak=0.7, f_lo=300, f_hi=2600, level=-25), tn); add(ding(-23, 1568), tn + 0.9)
# S5 vault: lock clunk, drawers open slowly
tl = T("a3", "locked") - 0.1; add(thud(-14), tl); add(click(-19), tl + 0.04)
tsl = T("a3", "slowly") - 0.25
for j in range(3): add(creak(-28, 0.4), tsl + 0.3 * j)
# S6 mine cart rolls in, odometer, NOT RARE stamp
add(whoosh(1.0, peak=0.5, f_lo=80, f_hi=600, level=-25), SHOT["S6"]["start"])
for j in range(10): add(click(-29), SHOT["S6"]["start"] + 0.07 * j)
t22 = T("a4", "twenty") - 0.25
for j in range(16): add(click(-31), t22 + 0.06 * j)
for j in range(8): clink(SHOT["S6b"]["start"] + 0.08 * j, -30, 3000 + 140 * j)
trr = T("a4", "rare") - 0.15; add(thud(-13), trr); add(boom(-17, 0.4), trr)
# S7 hearts float up
for j in range(5): add(pop(-30, 1100 + 90 * j), SHOT["S7"]["start"] + 0.2 + 0.3 * j)
# S8 / S11b brides light up
t10 = T("b2", "ten") - 0.2; shimmer(t10, -27, 4)
t8 = T("b5", "eight") - 0.25
for j in range(8): add(ding(-31, 1760 + 110 * j), t8 + 0.12 * j)
# S9 posters slap on the wall
for j in range(3): add(thud(-22), SHOT["S9"]["start"] + 0.2 + 0.25 * j); add(whoosh(0.2, peak=0.6, f_lo=600, f_hi=3000, level=-30), SHOT["S9"]["start"] + 0.12 + 0.25 * j)
# S9b / S10 typewriter: keys while typing, bell at the end of the line
for j in range(5): add(click(-28), SHOT["S9b"]["start"] + 0.3 + 0.13 * j)
t0 = T("b4", "A") - 0.05; t1 = T("b4", "forever") + 0.45
tq = t0
while tq < t1: add(click(-24), tq); tq += max(0.08, (t1 - t0) / len("A DIAMOND IS FOREVER"))
add(ding(-22, 2093), t1 + 0.02); add(scratch(-30, 0.2), t1 + 0.1)
# S11 medal
add(thud(-16), T("b5", "century") - 0.7); shimmer(T("b5", "century") - 0.6, -28)
# S12 re-hook folder; S12b tag swing
add(boom(-17, 0.4), T("c1", "sneakiest") - 0.2); add(creak(-32, 0.5), SHOT["S12b"]["start"] + 0.1)
# S13 poster slides in; S13b calendar pages + cash fly into the ring
add(whoosh(0.4, peak=0.6, f_lo=400, f_hi=3000, level=-25), SHOT["S13"]["start"])
for j in range(2): add(pop(-25, 900 + 200 * j), SHOT["S13b"]["start"] + 0.1 + 0.25 * j)
for j in range(6): add(whoosh(0.2, peak=0.5, f_lo=1500, f_hi=5000, level=-33), SHOT["S13b"]["start"] + 0.4 + 0.12 * j)
add(chaching(-23), T("c2", "forever") - 0.2)
# S14 rulebook pages + stamp
for j in range(3): add(whoosh(0.25, peak=0.5, f_lo=1500, f_hi=5000, level=-31), SHOT["S14"]["start"] + 0.1 + 0.7 * j)
tsel = T("c3", "seller") - 0.2; add(thud(-13), tsel); add(boom(-18, 0.35), tsel)
# S15 the crack
tb = T("d1", "breaking") - 0.2; add(scratch(-20, 0.18), tb); add(boom(-15, 0.5), tb)
for j in range(5): clink(tb + 0.03 * j, -24, 4200 - 300 * j)
# S16 lab: bubbles + growth shimmer
bubbles(SHOT["S16"]["start"] + 0.1, 7, -28); shimmer(SHOT["S16"]["start"] + 1.2, -28)
shimmer(SHOT["S16b"]["start"] + 0.2, -30, 4)
# S17 chart falls
t96 = T("d3", "ninety") - 0.25; add(whoosh(1.2, peak=0.6, f_lo=2500, f_hi=200, level=-25), SHOT["S17"]["start"] + 0.2); add(thud(-16), t96 + 0.6)
# S18 tag, closed sign slam
add(creak(-31, 0.4), T("d4", "eight") - 0.25); tsh = T("d4", "shut") - 0.2; add(thud(-12), tsh + 0.2); add(boom(-16, 0.4), tsh + 0.2)
# S19 bar drops, FOR SALE
th = T("d5", "half") - 0.25; add(whoosh(0.8, peak=0.6, f_lo=1200, f_hi=150, level=-24), th); add(buzzer(-27, 0.3), th + 0.6)
tsell = T("d5", "selling") - 0.45; add(thud(-14), tsell); add(chaching(-24), tsell + 0.1)
# S20 takeaway, ≠ slam
add(creak(-33, 0.5), SHOT["S20"]["start"] + 0.2); add(thud(-15), SHOT["S20b"]["start"] + 0.15)
# S21 question tag
add(pop(-23, 1200), T("t2", "What") - 0.2)
# S22 loop back to the hook
shimmer(SHOT["S22"]["start"] + 0.1, -27); add(thud(-16), T("e1", "story") - 0.2)
# S23 send + sting
add(pop(-21, 900), SHOT["S23"]["start"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
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
