"""Mix: narrator VO + ducked/carved sleepy Hawaiian-lounge score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP). New foley (ep 27): pen_draw (board strokes), eraser (the erase cut), snore, dial_ticks."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(27)
db = lambda x: 10 ** (x / 20)
S = {k: st for k, st, _ in SHOTLIST}; TN = T("i1", "meal") - 0.05
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
def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)

BOARD = {"S0b", "S1b", "S1c", "S2b", "S4", "S6", "S6b", "S7", "S8", "S10", "S10b", "S13", "S14b", "S16", "S16b", "S22", "S22b", "S23"}
for i, s in enumerate(SHOTLIST[1:], 1):
    k = s[2]; st = s[1]
    if k == "erase": add(eraser(-27), st)
    elif k == "whip": add(whoosh(0.4, level=-25), st - 0.22)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-27), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-25, 700 + 60 * i), st + 0.02)
    if s[0] in BOARD: add(pen_draw(-31, 0.9, i), st + 0.15)                     # the marker drawing the new picture
# hook: munching, then the head drop + snore
for j in range(int(TN / 0.5)): add(munch_sfx(-30, 0.3), 0.1 + j * 0.5)
add(thud(-15), TN); add(boom(-24, 0.3), TN); add(snore(-25, 1.6), TN + 0.35)
add(pop(-24, 1300), T("i1", "brain") - 0.05)
add(pen_draw(-30, 0.6, 3), T("i1", "blood") - 0.1)
for j in range(4): add(plip(-29, 700 + 80 * j), T("i1", "leaving") + 0.25 * j)
# the myth
add(stretch(-26, 0.5), T("i2", "steals") - 0.1)
for j in range(5): add(plip(-28, 600 + 60 * j), T("i2", "steals") + 0.2 + j * 0.18)
add(buzz(-30, 0.5, 120), T("i2", "dry") - 0.1); add(crt_off(-18, 0.5), T("i2", "out") - 0.05); add(snore(-28, 1.2), T("i2", "out") + 0.3)
add(ding(-25, 1568), S["S2"] + 0.2); add(rec_scratch(-20), T("i3", "myth") - 0.08); stamp(T("i3", "myth") - 0.05, -14)
# the nap excuse
add(soft_flop(-20), S["S3"] + 0.05); add(boing(-24, 180, 0.4), T("i4", "new") - 0.1)
# two things
for j in range(2): add(pop(-24, 1000 + 300 * j), T("a0", "two") + 0.4 + j * 0.3)
clink(T("a0", "skip") - 0.1, -26, 2400)
# body clock
for j in range(8): add(tick(-28), S["S5"] + 0.2 + j * 0.27)
add(boing(-26, 260, 0.4), T("a2", "dip") - 0.1)
for j in range(3): add(ding(-30 - 3 * j, 1760), S["S7"] + 0.2 + j * 0.35)
add(snore(-28, 1.3), T("a3", "still") - 0.1); clink(T("a4", "top") - 0.15, -22, 1900); add(thud(-16), T("a4", "top") - 0.12)
# the meal
clink(T("b1", "meal") - 0.35, -22, 3000); add(ding(-22, 2093), T("b1", "meal") - 0.15)
for j in range(3): add(click(-27), T("b2", "messages") - 0.2 + j * 0.3)
add(shimmer(-26, 0.8), T("b3", "orexin") - 0.25); add(crt_off(-26, 0.8), T("b3", "turned") - 0.2)
dial_ticks(T("b4", "nudges") - 0.1, T("b4", "down") + 0.3, -25, 7)
for j in range(3): dial_ticks(T("b5", "further") - 0.15 + j * 0.12, T("b5", "further") + 0.35 + j * 0.12, -30, 3)
add(boom(-22, 0.3), T("b5", "further") + 0.35)
# pizza study
add(munch_sfx(-26, 1.6), S["S14"] + 0.3); add(gulp(-24), T("c1", "another") - 0.1)
add(pop(-23, 900), T("c1", "twice") - 0.15); add(pop(-22, 1100), T("c1", "twice") + 0.05)
for j in range(8): add(tick(-26), S["S15"] + j * 0.2)
add(snore(-22, 1.6), T("c2", "Still") - 0.05)
# puzzle
add(thud(-18), S["S16b"] + 0.4); stamp(T("c3", "settled") - 0.1, -15)
# part 3
add(ding(-23, 1568), T("d0", "awake") - 0.15); add(ding(-25, 2093), T("d0", "awake") - 0.05)
add(rustle(-24, 0.5), T("d1", "smaller") + 0.05); add(ding(-24, 1760), T("d1", "smaller") - 0.1)
for t_ in np.arange(S["S19"] + 0.05, S["S20"] - 0.1, 0.54): add(footstep(-24), t_)
add(sniff(-26, 0.6), T("d3", "sleep") - 0.3)
add(jingle(-24), S["S21"] + 0.2); stamp(T("d4", "dont") - 0.05, -14); add(buzzer(-26, 0.3), T("d4", "dont"))
add(jingle(-22), T("d4", "keys") - 0.4); add(jingle(-24), T("d4", "keys") + 0.2)
# doctor: calm, no hits
add(ding(-30, 1318.5), T("e1", "doctor") - 0.25)
# recap
for w_ in ("body", "dimmer", "Not"): add(pop(-22, 1000), T("f1", w_) - 0.15)
add(pen_draw(-27, 0.3, 99), T("f1", "away") - 0.1)
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
