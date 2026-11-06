"""Mix: narrator VO + ducked/carved courtroom-qawwali score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP). New foley (ep 25): gavel, sniff, torch_click, press."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(42)
db = lambda x: 10 ** (x / 20)
S = {k: st for k, st, _ in SHOTLIST}; TI = T("i1", "oil") - 0.08
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
M[: int(LINES["i1"]["end"] * SR)] *= db(-5)
sfx = np.zeros((NS, 2), np.float32)
exec(open(f"{_D}/sfx_lib.py").read())
def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)
def verdict_hit(t, lv=-15): add(gavel(lv), t); stamp(t + 0.02, lv - 2)

# hook: wet slide, then the tree
add(squelch(-27, 0.5), 0.05); add(creep(-26), 0.5); add(boing(-15, 150, 0.5), TI); add(rustle(-22, 0.5), TI + 0.05); add(boom(-22, 0.3), TI)
add(tick(-28), S["S1"] + 0.1)
for j in range(3): add(pop(-29, 1200 + 200 * j), S["S1"] + 0.25 + j * 0.2)
add(squelch(-24, 0.4), T("i2", "melts") - 0.05); add(plip(-24), T("i2", "slides") - 0.05)
for j in range(4): add(pop(-29, 700), T("i2", "everybody") + j * 0.2)
stamp(T("i2", "Pure") - 0.1, -16); add(ding(-24, 1568), T("i2", "Pure") - 0.08)
add(gavel(-11), T("i3", "trial") - 0.1); add(boom(-20, 0.35), T("i3", "trial") - 0.1)
for j in range(7): add(pop(-29, 900 + j * 60), S["S2b"] + j * 0.05)
add(ding(-22, 1760), T("i3", "ones") - 0.1)
# real + fake
add(sizzle(-28, S["S3c"] - S["S3"]), S["S3"]); add(pop(-23, 700), T("a1", "butter") - 0.35)
for j in range(6): add(plip(-27), S["S3b"] + 0.1 + j * 0.18)
add(shimmer(-22), S["S3c"]); add(ding(-22, 1319), S["S3c"] + 0.05)
add(clack(-25, 1000), T("a2", "cheaper") - 0.1); add(boing(-25, 240, 0.25), T("a2", "palm") - 0.1); add(thud(-22), T("a2", "vanuspatee") - 0.1)
add(torch_click(-20), S["S5"] + 0.05); add(rattle(-27), T("a3", "soybean") - 0.1); add(rustle(-27, 0.3), T("a3", "essence") - 0.2); add(thud(-20), T("a3", "pure") - 0.1)
# water
add(gavel(-16), S["S6"] + 0.06); add(plip(-21), T("b1", "water") - 0.05); add(plip(-22), T("b1", "floats"))
for j in range(4): add(plip(-22), T("b2", "every") - 0.1 + j * 0.12)
verdict_hit(T("b2", "kitchen") - 0.15, -14); add(buzzer(-29, 0.25), T("b2", "kitchen") - 0.1)
# palm
add(gavel(-16), S["S8"] + 0.06); add(squelch(-26, 0.4), T("c1", "melts") - 0.1); add(rattle(-29), S["S9"] + 0.1); add(boing(-26, 240, 0.22), T("c2", "runny") - 0.1)
add(tick(-26), T("c2", "twenty") - 0.15); add(ding(-23, 1175), T("c2", "six") - 0.05); add(squelch(-25, 0.4), S["S9c"]); stamp(T("c2", "too") - 0.12, -17)
add(pop(-23, 900), S["S10"] + 0.2); add(pop(-23, 700), T("c3", "another") - 0.1); add(rec_scratch(-27), T("c3", "Which") - 0.05); verdict_hit(T("c3", "it") - 0.02, -15)
# smell
add(gavel(-16), S["S11"] + 0.06); add(sniff(-18, 0.5), T("d1", "smell") + 0.02); add(sniff(-20, 0.35), T("d1", "nutty") - 0.1); add(ding(-27, 2093), T("d1", "real") - 0.1)
add(squirt(-23), T("d2", "Remember") + 0.2); add(squirt(-24), T("d2", "bottles")); verdict_hit(T("d2", "essence") + 0.05, -14); add(buzzer(-29, 0.25), T("d2", "essence") + 0.1)
# colour
add(gavel(-16), S["S13"] + 0.06); add(ding(-24, 1319), T("e1", "Yellows") - 0.1); add(pop(-23, 500), T("e1", "whites") - 0.1)
add(thud(-22), S["S14"] + 0.1); add(ding(-24, 1568), T("e2", "white") - 0.1)
for j in range(3): add(plip(-24), T("e2", "yellow") + j * 0.2)
add(creep(-24), T("e2", "yellow")); verdict_hit(T("e2", "bottle") - 0.1, -14)
# no winners + chemistry
for j in range(4): add(thud(-23), S["S15"] + 0.02 + j * 0.1)
add(buzzer(-27, 0.4), T("f1", "no") - 0.1); add(gavel(-11), T("f1", "chemistry") - 0.1); add(boom(-22, 0.3), T("f1", "chemistry") - 0.1); add(fizz(-30), T("f1", "chemistry"))
add(lock_click(-23), S["S16"] + 0.2)
for j in range(5): add(footstep(-27), S["S16b"] + 0.1 + j * 0.3)
stamp(T("f2", "starch") - 0.15, -17); add(rustle(-24, 0.4), T("f3", "official") - 0.1); add(shimmer(-24), T("f3", "crimson") - 0.15); add(hiss(-30), T("f3", "crimson"))
add(ding(-24, 1760), T("f4", "sesame") - 0.1); add(clip_snap(-22), T("f4", "tag") - 0.12)
for j in range(4): add(footstep(-27), S["S18b"] + 0.2 + j * 0.25)
stamp(T("f4", "through") - 0.15, -17); add(buzz(-30), S["S19"]); verdict_hit(T("f5", "kitchen") - 0.15, -15)
# fridge
add(fridge_hum(-30, S["S22"] - S["S20"]), S["S20"]); add(suction(-22), T("g1", "fridge") - 0.25); add(shimmer(-21), T("g1", "one") - 0.15); add(ding(-20, 1760), T("g1", "one") - 0.12)
add(clack(-25, 1400), T("g2", "teaspoon") - 0.1)
for j in range(6): add(tick(-28), T("g2", "couple") + j * 0.13)
add(creep(-25), T("g2", "evenly") - 0.1); add(pop(-24, 1200), T("g2", "little") - 0.1); add(rattle(-29), T("g3", "palm") - 0.1); add(ice_crack(-22), T("g3", "split") - 0.1); stamp(T("g3", "split") - 0.08, -17)
add(gavel(-17), T("g4", "clue") - 0.1); add(ding(-23, 1319), T("g4", "clue") - 0.08); add(whoosh(1.2, peak=0.5, f_lo=800, f_hi=4000, level=-30), S["S23b"]); add(ding(-24, 1760), T("g4", "smooth") - 0.2)
add(pop(-24, 500), T("g5", "suspicious") - 0.25); verdict_hit(T("g5", "proof") - 0.15, -15)
# lab
for j in range(5): add(plip(-27), S["S25"] + 0.2 + j * 0.25)
add(whoosh(0.5, peak=0.5, level=-28), T("h1", "blend") - 0.2)
for j in range(3): add(tick(-26), T("h1", "lab") - 0.1 + j * 0.1)
stamp(T("h1", "miss") - 0.15, -18); add(pop(-23, 1400), T("h2", "tiny") - 0.1); add(giggle(-28), T("h2", "butyric")); add(ding(-24, 1175), T("h2", "two") - 0.05); stamp(T("h2", "zero") - 0.1, -17)
add(machine_whir(-29), S["S27"] + 0.1); add(ding(-24, 1568), T("h3", "five") - 0.1); add(rec_scratch(-28), T("h3", "cant") - 0.08); add(boing(-26, 220, 0.3), T("h3", "cant"))
# tips
add(whoosh(0.4, peak=0.5, level=-27), T("k1", "tin") - 0.3); add(thud(-18), T("k1", "tin") - 0.12); add(clang(-27), T("k1", "tin") - 0.1)
for w_ in ("licence", "maker", "batch", "expiry"): add(ding(-24, 1319), T("k2", w_) - 0.1)
add(buzzer(-28, 0.15), T("k2", "batch", 1) - 0.1); add(buzzer(-28, 0.15), T("k2", "expiry", 1) - 0.1)
add(clip_snap(-22), S["S30"] + 0.1); verdict_hit(T("k3", "proof") - 0.15, -15)
pp = S["S30b"]; j = 0
while pp + (j + 0.5) / 1.6 < S["S31"]: add(press(-19), pp + (j + 0.5) / 1.6); j += 1
add(doorbell(-29), S["S31"] + 0.05); add(ding(-24, 1760), T("k4", "trust") - 0.15); add(pop(-23, 900), T("k4", "price") - 0.1); stamp(T("k4", "why") - 0.15, -18)
# card
for j in range(7): add(pop(-27, 800 + j * 80), S["S32"] + 0.02 + j * 0.05)
for w_ in ("clue", "truth", "pay"): add(gavel(-19), T("l1", w_) - 0.3)
add(pop(-18, 1300), T("l2", "Send") + 0.25); add(ding(-22, 2093), T("l2", "Send") + 0.27)
vend = LINES["l2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2); audio_logo(vend + 0.25, -15)

sfx *= db(-5.0)
bed = bed_carve.carve(M * db(-13.5) + sfx, vo)
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
