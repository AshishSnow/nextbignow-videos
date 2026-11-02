"""Mix: narrator VO + ducked/carved ragtime score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP). New foley (ep 21, in sfx_lib): bread_knock, nail_tink, toaster_lever, toaster_pop, crust_crack, freeze_creak."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(42)
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
M[: int(LINES["i1"]["end"] * SR)] *= db(-5)
sfx = np.zeros((NS, 2), np.float32)
exec(open(f"{_D}/sfx_lib.py").read())
def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)
def sparkle_sfx(t, lv=-24): add(ding(lv, 2637), t); add(ding(lv - 3, 3520), t + 0.05); add(ding(lv - 6, 4186), t + 0.1)
# hook: every hammer swing lands a knock + a tink
tstop = T("i1", "than"); tq = 0.28; j = 0
while tq < tstop:
    add(bread_knock(-14), tq); add(nail_tink(-23), tq + 0.005); add(crust_crack(-30, 0.15), tq + 0.01); add(whoosh(0.18, peak=0.8, f_lo=500, f_hi=2500, level=-32), tq - 0.15); tq += 0.62; j += 1
stamp(T("i1", "faster") - 0.12, -15); add(boom(-20, 0.3), T("i1", "faster") - 0.12)
add(fridge_hum(-31, S["S1b"] - S["S1"]), S["S1"]); add(pop(-25, 700), S["S1"] + 0.3)
add(creak(-27, 0.6), T("i2", "aging") - 0.1); add(crust_crack(-24, 0.6), T("i2", "aging")); add(tick(-27), S["S1b"] + 0.2); add(tick(-27), S["S1b"] + 0.5)
add(crt_off(-29, 0.4), S["S2"]); add(ding(-27, 1046), T("i3", "isn't") - 0.1)
add(fizz(-30, 1.0), S["S3"] + 0.1); add(buzzer(-27, 0.3), T("a1", "dried") + 0.15); card_in(T("a1", "dried") - 0.1, -26)
add(suction(-24), S["S3b"] + 0.05); add(lock_click(-20), T("a1", "seal") - 0.05)
for k in range(4): add(bread_knock(-19), S["S3c"] + 0.05 + k * 0.28)
stamp(T("a1", "hard") - 0.15, -15); add(crust_crack(-24, 0.4), T("a1", "hard") - 0.1)
add(pop(-26, 800), S["S4"] + 0.15); add(pop(-26, 1000), S["S4"] + 0.65); add(boing(-22, 170, 0.45), T("a2", "Nowhere.") - 0.1)
add(lock_click(-20), T("a2", "locked") - 0.1); add(lock_click(-22), T("a2", "locked") + 0.1); add(lock_click(-22), T("a2", "locked") + 0.25)
add(rattle(-27, 0.5, 26), T("a3", "rice") - 0.1); add(pop(-25, 900), S["S5"] + 0.5)
add(rip(-24, 0.3), S["S5b"]); stamp(S["S5b"] + 0.03, -16); stamp(T("a3", "starch") - 0.1, -14); add(boom(-19, 0.35), T("a3", "starch") - 0.1)
add(bubble_pop(-25), T("b1", "water") - 0.1); add(stretch(-25, 0.7, True), T("b1", "swells,") - 0.12)
add(squelch(-27, 0.5), S["S6b"] + 0.1); add(boing(-24, 300, 0.3), T("b1", "soft.") - 0.15); sparkle_sfx(T("b1", "soft.") - 0.1, -27)
add(hiss(-29, 1.0), S["S7"] + 0.1); add(wind(-30, 1.0), T("b2", "cooling") - 0.1)
add(stretch(-25, 1.0, False), T("b2", "squeezing") - 0.1); add(ice_crack(-24, 0.5), T("b2", "crystals.") - 0.1)
add(lock_click(-19), T("b3", "trap") - 0.1); add(lock_click(-21), T("b3", "trap") + 0.1); add(lock_click(-22), T("b3", "trap") + 0.28)
add(bread_knock(-12), T("b3", "feels") - 0.1); add(tooth_crack(-20), T("b3", "feels") - 0.08); add(boing(-24, 180, 0.4), T("b3", "feels") + 0.05)
add(rec_scratch(-26), T("b4", "drying") + 0.4); stamp(T("b4", "setting.") - 0.12, -15)
add(crt_off(-28, 0.3), S["S10"]); add(pop(-23, 900), T("c1", "counter,") - 0.1); add(pop(-23, 1100), T("c1", "freezer,") - 0.1); add(pop(-23, 1300), T("c1", "fridge?") - 0.1)
add(boom(-18, 0.35), S["S10b"] + 0.05); add(whoosh(0.8, peak=0.3, f_lo=200, f_hi=4000, level=-22), S["S10b"]); add(rattle(-28, 0.9, 20), S["S10b"] + 0.1)
add(ice_crack(-26, 0.4), T("c2", "cold") - 0.1); add(clack(-25, 1800), T("c2", "exactly") - 0.1); add(fridge_hum(-30, 1.8), T("c2", "exactly"))
add(whoosh(0.7, peak=0.5, f_lo=300, f_hi=3200, level=-26), S["S12"] + 0.2); stamp(T("c3", "day") - 0.15, -18); add(chaching(-25), T("c3", "twice") - 0.12); add(boom(-20, 0.3), T("c3", "twice") - 0.12)
for w, f0 in (("Germs,", 900), ("mould,", 1050), ("milk", 1200)): add(pop(-24, f0), T("c4", w) - 0.1)
add(boing(-22, 300, 0.5), S["S13b"] + 0.05); add(ice_crack(-26, 0.5), T("c4", "weird") - 0.05); add(wind(-28, 1.2), S["S13b"])
add(wind(-26, 1.6), S["S14"]); add(freeze_creak(-24, 0.9), T("d1", "flips.") - 0.5); stamp(T("d1", "flips.") - 0.12, -19)
add(ice_crack(-20, 0.7), S["S14b"] + 0.05); add(freeze_creak(-27, 1.0), S["S14b"] + 0.4)
for k in range(4): add(tick(-26), T("d1", "stops.") - 2.0 + k * (0.4 + k * 0.2))
for w, f0 in (("slow,", 900), ("fast,", 1200), ("paused.", 700)): add(pop(-23, f0), T("d2", w) - 0.1)
add(wind(-30, 1.8), S["S16"]); add(rustle(-26, 0.4), T("e1", "back") - 0.2); add(boom(-18, 0.4), T("e1", "back") - 0.12); add(boing(-22, 220, 0.5), T("e1", "back") - 0.1)
add(toaster_lever(-18), T("e2", "Toast") + 0.05); add(micro_hum(-32, 1.5) if "micro_hum" in globals() else tick(-30), T("e2", "Toast") + 0.3)
add(rattle(-26, 0.8, 26), T("e2", "shakes") - 0.05); add(simmer(-29, 1.2), S["S17b"] + 0.1)
add(toaster_pop(-14), S["S17c"] + 0.03); add(crunch(-16), T("e2", "soft") + 0.05); sparkle_sfx(T("e2", "soft") - 0.1, -25)
stamp(T("e3", "one-time") + 0.1, -18)
for k in range(3): add(tick(-26), S["S18b"] + 0.15 + k * 0.3)
add(crust_crack(-24, 0.5), T("e3", "cools") + 0.1); add(boing(-25, 150, 0.4), T("e3", "faster") - 0.1)
add(nibble(-25, 1.2, 10), S["S18c"] + 0.2); add(crunch(-20), S["S18c"] + 0.05)
add(creak(-28, 0.5), S["S19"] + 0.3); add(squelch(-27, 0.8), S["S19"] + 0.8); add(buzz(-31, 1.2, 150), T("f1", "hot") - 0.1); stamp(T("f1", "crime") - 0.12, -19)
add(suction(-24), S["S20"] + 0.05); add(wind(-29, 1.2), S["S20"] + 0.1); add(chop(-22), T("f2", "Slice") - 0.05); add(rustle(-26, 0.4), T("f2", "wrap") - 0.05); add(lock_click(-24), T("f2", "freeze") + 0.1); add(freeze_creak(-29, 0.6), T("f2", "freeze") + 0.05)
add(clack(-24, 1400), T("f3", "straight") + 0.1); add(toaster_lever(-19), T("f3", "toaster.") - 0.1)
add(toaster_pop(-14), S["S21b"] + 0.05); add(ding(-25, 1568), S["S21b"] + 0.2)
for w, f0 in (("now,", 1318.5), ("later,", 1568), ("else.", 2093)): add(pop(-21, 900), T("g1", w) - 0.2); add(ding(-25, f0), T("g1", w) - 0.18)
add(pop(-18, 1300), T("g2", "Send") + 0.3); add(ding(-22, 2093), T("g2", "Send") + 0.32)
vend = LINES["g2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
for j, f0 in enumerate((1318.5, 1568, 1976, 2637)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

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
