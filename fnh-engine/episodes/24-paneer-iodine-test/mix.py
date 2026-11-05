"""Mix: narrator VO + ducked/carved 70s crime-funk score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP). New foley (ep 24): slowmo_swell (the sound of a speed ramp: a rising pitched-down swell), drip_big (a heavy slow-motion drop), audio_logo (the FreshNestHub 1-s sting)."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(42)
db = lambda x: 10 ** (x / 20)
S = {k: st for k, st, _ in SHOTLIST}; TP = T("i1", "pass") - 0.04
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
def slowmo_swell(level=-26, dur=2.0):
    """the sound of a speed ramp: a low sine + filtered noise that slowly rise toward the impact."""
    N_ = int(dur * SR); tt = np.arange(N_) / SR; k = tt / dur
    ph = 2 * np.pi * np.cumsum(50 + 90 * k ** 2) / SR; x = 0.6 * np.sin(ph) * k
    nz = signal.sosfilt(signal.butter(2, [200, 2400], "band", fs=SR, output="sos"), np.random.default_rng(3).normal(0, 1, N_)) * k ** 2.5
    x = x + 0.5 * nz / (np.abs(nz).max() + 1e-9); x = x / (np.abs(x).max() + 1e-9) * db(level)
    return np.stack([x, x], 1).astype(np.float32)
def drip_big(level=-13):
    """a heavy, pitched-down drop landing (a slowed plip with a body)."""
    N_ = int(0.5 * SR); tt = np.arange(N_) / SR
    x = np.sin(2 * np.pi * (240 * tt + 340 * tt ** 2)) * np.exp(-tt * 9) + 0.5 * np.sin(2 * np.pi * 90 * tt) * np.exp(-tt * 14)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1).astype(np.float32)
def audio_logo(t, lv=-16):
    """the FreshNestHub sting (1 s): three warm rising mallet notes (Fresh-Nest-Hub) + a crunch on the last one."""
    for j, f0 in enumerate((587.3, 880.0, 1174.7)):
        N_ = int(0.6 * SR); tt = np.arange(N_) / SR; x = (np.sin(2 * np.pi * f0 * tt) + 0.3 * np.sin(2 * np.pi * f0 * 4 * tt) * np.exp(-tt * 24)) * np.exp(-tt * 7)
        x = x / (np.abs(x).max() + 1e-9) * db(lv + (j == 2) * 2); add(np.stack([x, x], 1).astype(np.float32), t + j * 0.16)
    add(crunch(lv - 4), t + 0.32)

# hook: swell under the slow motion, then the landing
add(slowmo_swell(-23, TP), 0.0); add(plip(-30), 0.06); add(drip_big(-11), TP); stamp(TP + 0.05, -15); add(boom(-20, 0.35), TP); add(boing(-24, 150, 0.4), TP + 0.12)
add(tick(-28), S["S1"] + 0.1); add(pop(-23, 900), S["S1"] + 0.18)
for j in range(3): add(pop(-29, 1200 + 200 * j), S["S1"] + 0.3 + j * 0.25)
add(plip(-17), T("i2", "blue") - 0.32); add(creep(-22), T("i2", "blue") - 0.3); sparkle = lambda t, lv=-26: (add(ding(lv, 2093), t), add(ding(lv - 3, 2637), t + 0.06))
add(thud(-18), T("i2", "fake") - 0.15); add(boing(-25, 180, 0.3), T("i2", "fake") - 0.1); add(rec_scratch(-27), T("i2", "fake") - 0.05)
add(ding(-24, 1568), T("i3", "real") - 0.15); add(pop(-24, 700), T("i3", "think") - 0.15)
add(simmer(-29, S["S4"] - S["S3"]) if "simmer" in globals() else sizzle(-30, S["S4"] - S["S3"]), S["S3"])
add(squeeze(-22), T("a1", "sour") - 0.25); add(plip(-24), T("a1", "sour") + 0.05); add(plip(-26), T("a1", "sour") + 0.3)
add(pop(-25, 700), T("a2", "clump") - 0.15); add(squelch(-27, 0.4), T("a2", "clump")); add(pop(-25, 1000), T("a2", "catch") - 0.1)
add(giggle(-28), S["S4b"] + 0.1)
for j in range(4): add(plip(-25), S["S5"] + 0.15 + j * 0.3)
add(thud(-11), T("a3", "press") + 0.04); add(clang(-24), T("a3", "press") + 0.05); add(ding(-24, 1760), T("a3", "block") - 0.2)
add(rustle(-23, 0.6), S["S6"] + 0.05); stamp(T("a4", "No") + 0.05, -16)
for j in range(3): add(clack(-25, 1400), S["S7"] + 0.2 + j * 0.1)
add(pop(-23, 800), T("b1", "vegetable") - 0.1); add(whoosh(0.3, peak=0.5, level=-27), S["S8"] + 0.1); add(pop(-22, 700), T("b2", "analogue") - 0.15); add(rustle(-25, 0.3), T("b2", "analogue") - 0.1)
add(whoosh(0.3, peak=0.5, level=-26), S["S8b"] + 0.05); add(plip(-21), T("b2", "in") - 0.05); add(pop(-23, 600), T("b2", "maybe") - 0.1); add(clack(-23, 1200), T("b2", "half") - 0.2); add(ding(-25, 1319), T("b2", "half") - 0.18)
stamp(T("b3", "legal") - 0.15, -17); add(rustle(-25, 0.3), T("b3", "label") - 0.15)
add(thud(-17), T("b4", "plate") + 0.1); add(sizzle(-28, 1.4), T("b4", "plate") + 0.1); stamp(T("b4", "label") - 0.15, -17); add(buzzer(-29, 0.2), T("b4", "label") - 0.1)
add(squelch(-22, 0.5), S["S11"] + 0.05)
add(stretch(-25) if "stretch" in globals() else rustle(-25, 0.5), T("c2", "coils") - 0.1); add(boing(-26, 260, 0.3), T("c2", "spring") - 0.1)
for j in range(5): add(pop(-26, 1100 + 80 * j), T("c2", "Iodine") + 0.05 + j * 0.2)
add(shimmer(-25) if "shimmer" in globals() else ding(-25, 2000), S["S13"] + 0.1); add(ding(-22, 1047), T("c3", "blue") - 0.15); add(thud(-20), T("c3", "blue") - 0.13)
add(plip(-21), S["S14"] + 0.5); add(buzzer(-30, 0.25), T("c4", "brown") - 0.15)
add(lock_click(-23), S["S15"] + 0.2); stamp(T("c5", "Starch") - 0.1, -18); add(doorbell(-30), S["S15b"] - 0.1)
for j in range(5): add(footstep(-25), S["S15b"] + 0.1 + j * 0.3)
for j in range(5): add(footstep(-28), S["S16"] + 0.1 + j * 0.5)
add(rec_scratch(-28), S["S16b"] + 0.02); add(plip(-13), T("d2", "Brown") - 0.2); stamp(T("d2", "Brown") - 0.05, -17); stamp(T("d2", "passes") - 0.1, -15); add(clack(-24, 500), T("d2", "passes"))
add(whoosh(0.4, peak=0.5, level=-29), S["S18"] + 0.1); add(giggle(-28), S["S18b"] + 0.1)
add(rec_scratch(-27), S["S19"]); add(squelch(-23, 0.5), T("d4", "gravy") - 0.1); add(plip(-24), T("d4", "starch")); add(creep(-23), S["S19c"]); stamp(T("d4", "blue") - 0.15, -16)
add(snip(-24) if "snip" in globals() else clack(-23, 900), T("d5", "fake") + 0.15); stamp(T("d5", "starch") - 0.1, -13); add(ding(-22, 1568), T("d5", "starch")); add(ding(-24, 2093), T("d5", "starch") + 0.07)
for j in range(3): add(boing(-23, 220 + 30 * j, 0.22), T("e1", "rubbery") - 0.15 + j * 0.28)
for j in range(4): add(boing(-26, 180, 0.2), S["S22"] + 0.2 + j * 0.52)
stamp(T("e4", "no") - 0.1, -17); add(machine_whir(-29, 0.8) if False else tick(-27), T("e4", "lab") - 0.3); add(ding(-24, 1760), T("e4", "lab") - 0.1)
for j, f0 in enumerate((988, 1175, 1319)): add(pop(-22, f0), T("f1", "Three") - 0.12 + j * 0.12)
add(rustle(-24, 0.4), S["S26"] + 0.1); stamp(T("f2", "analogue") - 0.15, -17); add(doorbell(-29), S["S27"] + 0.05); add(pop(-22, 900), T("f3", "Dairy") - 0.15); add(rustle(-25, 0.4), S["S27b"]); add(pop(-23, 1100), T("f3", "menu") - 0.3)
add(clack(-23, 1200), S["S28"] + 0.12); stamp(T("f4", "why") - 0.15, -17)
add(plip(-24), S["S29"] + 0.5)
add(sizzle(-28, 0.5), T("f5", "Boil") - 0.05); add(pop(-23, 800), T("f5", "cool") - 0.1); add(plip(-21), T("f5", "add") - 0.05); add(plip(-23), T("f5", "add") + 0.15)
stamp(T("f5", "dont") - 0.1, -17); pedal_bin(T("f5", "food") - 0.5, -21)
add(rustle(-24, 0.5), S["S30"] + 0.1); add(whoosh(0.5, peak=0.5, f_lo=500, f_hi=3000, level=-25), T("f6", "word") - 0.1); stamp(T("f6", "draft") - 0.2, -18)
add(lock_click(-20), S["S31"] + 0.05); add(pop(-23, 900), T("g1", "Blue") - 0.12); add(ding(-25, 1047), T("g1", "starch") - 0.1); add(pop(-23, 700), T("g1", "no") - 0.12)
add(pop(-18, 1300), T("g2", "send") + 0.25); add(ding(-22, 2093), T("g2", "send") + 0.27)
vend = LINES["g2"]["end"] + 0.35
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
