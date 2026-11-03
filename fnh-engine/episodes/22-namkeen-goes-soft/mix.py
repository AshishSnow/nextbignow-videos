"""Mix: narrator VO + ducked/carved Indo-disco score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP). New foley (ep 22, in sfx_lib): soft_flop, footstep, clip_snap, oven_ding, soggy, drink. The backbeat of the score is REAL CRUNCHES while crisp, SOGGY thuds when soft."""
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
BEAT = 0.54
def backbeat(t0, t1, kind="crunch", lv=-25, phase=0.0):
    t = t0 + BEAT + phase
    while t < t1 - 0.05:
        add(crunch(lv) if kind == "crunch" else soggy(lv + 2), t); t += 2 * BEAT
# hook: footsteps + crunchy backbeat, then the FLOP
ts = T("i1", "soft") - 0.25
for tq in [k * 0.54 for k in range(int((ts + 0.2) / 0.54) + 1)]: add(footstep(-23), tq)
backbeat(0.0, ts, "crunch", -22)
add(rustle(-23, 0.3), T("i1", "open") - 0.05); add(soft_flop(-13), ts + 0.02); stamp(ts + 0.05, -17); add(boing(-22, 150, 0.5), ts + 0.1)
add(tick(-26), S["S1"] + 0.05); add(rec_scratch(-27), T("i2", "getting") + 0.1)
add(drink(-18, 4, 0.2), T("i2", "drinking") - 0.1); add(boing(-24, 400, 0.25), T("i2", "drinking") - 0.1); add(plip(-24), T("i2", "air") - 0.1)
add(soggy(-20), S["S2"] + 0.15); add(bread_knock(-19), T("i3", "bread") - 0.15); stamp(T("i3", "opposite") - 0.1, -18)
add(sizzle(-24, 1.8) , S["S3"] + 0.1); add(bubble_pop(-27), T("a1", "fried")); add(hiss(-29, 1.2), T("a1", "almost") - 0.2)
add(crunch(-11), T("a2", "crunch") - 0.2); add(crust_crack(-20, 0.3), T("a2", "crunch") - 0.15); add(crunch(-18), T("a2", "crunch") + 0.1)
add(wind(-30, 1.8), S["S4b"]); add(sip(-24) , T("a2", "thirsty") - 0.1)
add(suction(-27), S["S5"] + 0.3); add(shimmer(-23), T("a3", "full") - 0.12); add(whoosh(0.5, peak=0.5, f_lo=800, f_hi=4000, level=-32), T("a3", "cant") - 0.1)
add(fizz(-30, 1.8), T("a4", "moves")); add(pop(-23, 900), T("a4", "more") - 0.1); add(pop(-23, 1200), T("a4", "less") - 0.1); add(ding(-24, 1318.5), T("a4", "even") - 0.1)
t7 = S["S7"]; 
for tq in [t7 + k * 0.54 for k in range(5)]: add(footstep(-21), tq)
stamp(T("b1", "meter") - 0.1, -19); add(pop(-25, 900), T("b1", "zero") - 0.1); add(whoosh(0.3, peak=0.6, level=-27), T("b1", "lower") - 0.1); add(drink(-24, 2, 0.15), T("b1", "thirstier") - 0.12)
add(pop(-21, 1000), T("b2", "three") - 0.25); add(pop(-21, 1400), T("b2", "air") - 0.3); add(ding(-25, 1568), T("b2", "seven") - 0.2)
add(rustle(-21, 0.4), T("b3", "lid") - 0.1); add(suction(-23), T("b3", "lid") - 0.08); add(whoosh(0.8, peak=0.5, f_lo=300, f_hi=3200, level=-25), T("b3", "lid") + 0.1); stamp(T("b3", "one") - 0.1, -17)
add(pop(-25, 700), T("b4", "isnt")); add(drink(-20, 3, 0.2), T("b4", "Your") - 0.1)
add(plip(-16), T("c1", "kill") - 0.2); add(boom(-20, 0.4), T("c1", "kill") - 0.1); add(crt_off(-29, 0.3), S["S11"])
add(snap(-11), T("c2", "snaps") - 0.12); add(crust_crack(-21, 0.3), T("c2", "snaps") - 0.1)
add(squelch(-20, 0.5), T("c2", "bends") - 0.15); add(boing(-24, 180, 0.5), T("c2", "bends") - 0.1); add(plip(-21), T("c2", "water") - 0.12); sparkle_sfx(T("c2", "water") - 0.05, -28)
add(ice_crack(-22, 0.4), T("c3", "brittle") - 0.1); add(ice_crack(-17, 0.6), T("c3", "like")); clink(T("c3", "glassy") - 0.12, -26); stamp(T("c3", "glassy") - 0.12, -20)
for j in range(5): add(plip(-25), T("c4", "slips") - 0.1 + j * 0.24)
add(stretch(-23, 0.9, True), T("c4", "loosens") - 0.1); add(boing(-19, 200, 0.6), T("c4", "rubbery") - 0.15); add(stretch(-26, 0.5, False), T("c4", "rubbery") + 0.2)
add(creak(-25, 0.5), T("c5", "bends") - 0.1); add(soft_flop(-20), T("c5", "snap")); stamp(T("c5", "No") - 0.1, -19); stamp(T("c5", "crunch") - 0.12, -16); add(soggy(-17), T("c5", "crunch") - 0.05)
backbeat(S["S13b"] + 0.5, S["S15"], "soggy", -29)
add(plip(-24), T("d1", "barely") - 0.1); add(buzzer(-27, 0.3), T("d1", "rejected") - 0.05); stamp(T("d1", "rejected") - 0.1, -16)
ts17 = T("d2", "only") - 0.05; add(footstep(-16), ts17); add(footstep(-16), ts17 + 0.54); add(pop(-22, 800), ts17 + 0.5); add(pop(-20, 1100), ts17 + 1.05); add(soft_flop(-14), ts17 + 1.1); add(boing(-22, 160, 0.4), ts17 + 1.12)
add(crt_off(-27, 0.4), S["S18"]); add(boom(-17, 0.5), T("e1", "trap") - 0.1); stamp(T("e1", "trap") - 0.1, -16); add(rip(-28, 0.2), T("e1", "Diwali")); sparkle_sfx(T("e1", "Diwali"), -28)
add(pop(-24, 800), S["S19"] + 0.2); add(pop(-24, 1000), T("e2", "barfi") - 0.12); add(ding(-25, 1760), T("e2", "zero") - 0.1)
add(clack(-26, 900), S["S20"] + 0.1); add(pop(-25, 900), T("e3", "crisp") - 0.12); add(pop(-25, 1100), T("e3", "soft") - 0.1)
add(soft_flop(-21), T("e3", "soft", 1) - 0.1); add(crust_crack(-25, 0.5), T("e3", "dry") - 0.1); add(fizz(-30, 1.2), S["S21"] + 0.1)
add(whoosh(0.35, peak=0.8, level=-22), T("e4", "closed") - 0.1); add(thud(-14), T("e4", "closed") + 0.25); stamp(T("e4", "closed") + 0.5, -19)
for j in range(3): add(pop(-21, 900 + 200 * j), T("f1", "three") - 0.1 + j * 0.1)
add(clack(-23, 1400), T("f1", "Lid") + 0.05); add(clip_snap(-11), T("f1", "on") + 0.05); add(lock_click(-20), T("f1", "airtight") - 0.1)
for j in range(4): add(plip(-29), T("f1", "airtight") - 0.5 + j * 0.3)
backbeat(S["S22b"], S["S24"], "crunch", -28)
add(whoosh(0.4, peak=0.6, level=-26), T("f2", "separate") - 0.15); add(thud(-20), T("f2", "separate") + 0.15)
pedal_bin(S["S24"] + 0.1, -22); stamp(T("f3", "dont") - 0.1, -17); add(knob(-22), S["S24b"] + 0.05); add(micro_hum(-30, 1.4), S["S24c"] + 0.1); micro_beep(S["S24c"] + 0.1, -26)
add(simmer(-29, 1.6), S["S25"]); add(hiss(-27, 1.5), S["S25"] + 0.1); add(crunch(-15), S["S25b"] - 0.35); backbeat(S["S25"] + 0.4, S["S26"], "crunch", -26)
add(oven_ding(-20), S["S25b"] + 0.02); add(tick(-27), S["S25b"] + 0.3); add(tick(-27), S["S25b"] + 0.7)
add(soggy(-24), S["S26"] + 0.2); add(pop(-25, 800), T("g1", "texture") - 0.1)
add(suction(-30), T("g1", "smells") - 0.1); add(creak(-27, 0.4), T("g1", "sharp") - 0.1); add(clack(-22, 700), T("g1", "paint") - 0.1); add(pop(-23, 1200), T("g1", "crayons") - 0.1)
add(squelch(-27, 0.4), T("g1", "oil") - 0.1); add(buzzer(-28, 0.3), T("g1", "No") - 0.05); pedal_bin(T("g1", "bin") - 0.12, -17); add(thud(-17), T("g1", "bin") + 0.25); stamp(T("g1", "bin") - 0.12, -19)
backbeat(S["S27"], S["S28"], "crunch", -25)
for w, f0 in (("lid", 1318.5), ("sweets", 1568), ("heat", 2093)):
    add(pop(-21, 900), T("h1", w) - 0.2); add(ding(-25, f0), T("h1", w) - 0.18)
for tq in [S["S28"] + k * 0.54 for k in range(int((LINES["h2"]["end"] + 0.3 - S["S28"]) / 0.54))]: add(footstep(-25), tq)
add(pop(-18, 1300), T("h2", "Send") + 0.3); add(ding(-22, 2093), T("h2", "Send") + 0.32)
vend = LINES["h2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(crunch(-16), vend + 0.2); add(boom(-18, 0.35), vend + 0.2)
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
