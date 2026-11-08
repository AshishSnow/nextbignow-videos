"""Mix: narrator VO + ducked/carved 80s aerobics synth-pop score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP). New foley (ep 28): spray (spit-take), glug, clank, pour, belt."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(28)
db = lambda x: 10 ** (x / 20)
S = {k: st for k, st, _ in SHOTLIST}; TD = T("i1", "detox") - 0.05
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
M[: int(LINES["i1"]["end"] * SR)] *= db(-4)
exec(open(f"{_D}/sfx_lib.py").read())
SHOT_END = lambda sid: next((SHOTLIST[i + 1][1] for i, s in enumerate(SHOTLIST) if s[0] == sid and i + 1 < len(SHOTLIST)), END)
def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)


BOARD = {"S0b", "S1b", "S3", "S3b", "S4", "S4b", "S6", "S6b", "S8", "S9", "S9b", "S12b", "S13", "S14", "S14b", "S17", "S18", "S20", "S23", "S24"}
FACT = {"S8b", "S10", "S10b"}
for i, s in enumerate(SHOTLIST[1:], 1):
    k = s[2]; st = s[1]
    if k == "erase": add(eraser(-27), st)
    elif k == "morph": add(whoosh(0.45, peak=0.5, f_lo=500, f_hi=2600, level=-27), st - 0.05); add(shimmer(-30, 0.5), st + 0.05)
    elif k == "whip": add(whoosh(0.4, level=-25), st - 0.22)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-27), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-25, 700 + 60 * i), st + 0.02)
    if s[0] in BOARD: add(pen_draw(-31, 0.9, i), st + 0.15)
    if s[0] in FACT: add(belt(-33, min(3.5, SHOT_END(s[0]) - st)), st)
# hook: the chug, then the spit-take
add(glug(-21, max(1, int((TD - 0.1) / 0.2)), 0.2), 0.05)
add(spray(-15, 0.6), TD); add(boing(-24, 160, 0.4), TD + 0.05)
add(pop(-24, 1300), T("i1", "right") + 0.1)
# no juice / no tea / no plan: an X each
for w_ in ("juice", "tea", "plan"): add(thud(-19), T("i2", w_) - 0.25); add(scratch(-26, 0.2), T("i2", w_) - 0.2)
add(ding(-22, 2093), T("i2", "free") - 0.1); add(chaching(-24), T("i2", "free"))
# the feed + the unimpressed liver
for j in range(5): add(click(-30), S["S2"] + 0.2 + j * 0.3)
add(rec_scratch(-20), T("i3", "impressed") - 0.2)
# the investigation
add(rustle(-26, 0.5), S["S3"] + 0.3)
for j in range(15): add(pop(-31, 900 + 40 * j), S["S4"] + 0.05 + j * 0.07)
tp = T("a2", "proof") - 0.3
for j in range(15): add(thud(-26), tp + j * 0.05)
add(buzzer(-25, 0.4), tp + 0.8)
add(boing(-24, 300, 0.4), T("a3", "tell") - 0.1)
add(squelch(-26, 0.4), T("a4", "oil") - 0.1); add(bubble_pop(-20), T("a4", "soap") - 0.1)
# part 1
add(rustle(-24, 0.6), S["S7"] + 0.2); add(ding(-23, 1568), T("b0", "cleaning") - 0.2)
add(ding(-24, 1760), T("b1", "liver") - 0.15)
for j in range(4): add(clank(-28, 420), S["S8b"] + 0.25 + j * 0.51)
add(dunk(-22, 0.6), T("b2", "fat") + 0.05); add(boing(-22, 220, 0.4), T("b2", "water") + 0.15); add(boing(-24, 260, 0.35), S["S9b"] + 0.6)
add(machine_whir(-24, 0.6, 140), T("b3", "one") - 0.1); add(machine_whir(-23, 0.6, 180), T("b3", "time") - 0.1); add(ding(-22, 2093), T("b3", "time") + 0.1)
add(creak(-24, 0.5), T("b4", "leave") - 0.6)
for j in range(3): add(footstep(-26, 0.5), T("b4", "leave") + j * 0.2)
# part 2: kidneys
add(pop(-20, 900), T("c0", "kidneys") - 0.2); add(pop(-20, 1200), T("c0", "kidneys") - 0.08)
add(clip_snap(-20), T("c1", "fist") - 0.2)
add(shimmer(-26, 0.9), T("c1", "million") - 0.3)
add(pour(-25, 1.8), S["S13"] + 0.2)
for j in range(7): add(thud(-22), S["S13b"] + 0.05 + j * 0.09)
for j in range(6): add(plip(-29, 800 + 70 * j), S["S14"] + 0.3 + j * 0.2)
add(drink(-26, 2, 0.2), T("c3", "two") - 0.1)
for j in range(8): add(tick(-27), S["S15"] + 0.1 + j * 0.25)
add(thud(-17), T("c4", "subscription") - 0.3); add(pop(-23, 600), T("c4", "subscription") - 0.25)
# part 3: cleanse
add(fridge_hum(-30, 1.5), S["S16"]); add(suction(-22), S["S16"] + 0.05)
for j in range(3): add(pop(-24, 1400 + 200 * j), S["S16"] + 0.2 + j * 0.12)
add(rustle(-26, 0.6), S["S17"] + 0.2); add(thud(-15), T("d1", "proof") - 0.2); add(pop(-21, 500), T("d1", "proof") - 0.18)
add(pen_draw(-28, 0.8, 55), T("d2", "back") - 0.3)
add(rattle(-26, 0.4, 20), T("d3", "Laxatives") - 0.1); add(stretch(-26, 0.8, False), T("d3", "dehydrated") - 0.3)
add(giggle(-28, 0.5), T("d4", "germs") - 0.1)
# part 4: what helps
add(ding(-23, 1568), T("e0", "helps") - 0.2); add(ding(-25, 2093), T("e0", "helps") - 0.1)
add(thud(-16), T("e1", "boring") - 0.1); add(snore(-27, 1.4), T("e1", "sleep") - 0.1)
add(munch_sfx(-28, 1.4), S["S22c"] + 0.2)
for j in range(6): add(plip(-28, 700 + 50 * j), S["S23"] + 0.2 + j * 0.18)
# recap + send
for j in range(3): add(pop(-22, 1000 + 200 * j), S["S24"] + 0.1 + j * 0.25)
add(scratch(-24, 0.2), T("f1", "needed") - 0.1)
add(ding(-24, 1760), T("f1", "day", 0) - 0.2)
add(pop(-18, 1300), T("f2", "Send") + 0.25); add(ding(-22, 2093), T("f2", "Send") + 0.27)
vend = LINES["f2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2); audio_logo(vend + 0.25, -15)

sfx *= db(-5.0)
bed = bed_carve.carve(M * db(-11.5) + sfx, vo)
mix = VO + bed
sf.write(f"{B}/work/mix_pre.wav", mix, SR, subtype="FLOAT")
TGT = -11.0
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{B}/work/mix_pre.wav", "-af", f"loudnorm=I={TGT}:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
ln = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/mix_pre.wav", "-af",
                f"loudnorm=I={TGT}:TP=-1.5:LRA=9:measured_I={ln['input_i']}:measured_TP={ln['input_tp']}:measured_LRA={ln['input_lra']}:"
                f"measured_thresh={ln['input_thresh']}:offset={ln['target_offset']}:linear=true,aresample=48000", "-c:a", "pcm_s16le", f"{B}/work/mix.wav"], check=True)
hp = signal.butter(2, 150, "high", fs=SR, output="sos"); vv = signal.sosfilt(hp, vo); bb = signal.sosfilt(hp, bed.mean(1))
print("VO/bed dB:", " ".join(f"{lid}:{20*np.log10(np.sqrt(np.mean(vv[int(L['start']*SR):int(L['end']*SR)]**2))/np.sqrt(np.mean(bb[int(L['start']*SR):int(L['end']*SR)]**2)+1e-12)):.1f}" for lid, L in LINES.items()))
