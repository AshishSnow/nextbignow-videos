"""Mix: energetic narrator VO + ducked/carved cinematic score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP)."""
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
TS0 = T("i1", "stopped") - 0.12; TS5 = T("b3", "stop") - 0.1
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


def rocket(dur, level=-20, att=0.08, rel=0.35):
    """rumbling rocket roar: low brown noise + crackle."""
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    br = np.cumsum(rng.standard_normal(n_)); br = signal.sosfilt(signal.butter(2, 25, "high", fs=SR, output="sos"), br)
    br = signal.sosfilt(signal.butter(4, 700, "low", fs=SR, output="sos"), br)
    hs = signal.sosfilt(signal.butter(2, [900, 4000], "band", fs=SR, output="sos"), rng.standard_normal(n_))
    cr = (rng.random(n_) < 0.004) * rng.standard_normal(n_) * 3
    x = br / (np.abs(br).max() + 1e-9) + 0.25 * hs / (np.abs(hs).max() + 1e-9) + 0.15 * signal.sosfilt(signal.butter(2, 2500, "high", fs=SR, output="sos"), cr)
    x *= (0.85 + 0.15 * np.sin(2 * np.pi * 9 * t2 + rng.uniform(0, 6)))
    e = np.minimum(1, t2 / att) * np.clip((dur - t2) / rel, 0, 1)
    x = x * e; x = x / (np.abs(x).max() + 1e-9) * db(level)
    return np.stack([x, np.roll(x, 90)], 1)


def splash_sfx(level=-17, dur=1.4):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = signal.sosfilt(signal.butter(2, [400, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_))
    x *= np.minimum(1, t2 / 0.01) * np.exp(-t2 / 0.35) * (1 + 0.4 * (rng.random(n_) < 0.01))
    lo = signal.sosfilt(signal.butter(2, 300, "low", fs=SR, output="sos"), rng.standard_normal(n_)) * np.exp(-t2 / 0.2)
    x = x / (np.abs(x).max() + 1e-9) + 0.6 * lo / (np.abs(lo).max() + 1e-9)
    x = x / np.abs(x).max() * db(level); return np.stack([x * 0.9, x], 1)


def crack(level=-20):
    n_ = int(0.25 * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_) * (rng.random(n_) < 0.08) * np.exp(-t2 / 0.06)
    x = signal.sosfilt(signal.butter(2, 1200, "high", fs=SR, output="sos"), x); x = x / (np.abs(x).max() + 1e-9) * db(level)
    return np.stack([x, x], 1)


for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-23), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-26), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-25), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-21, 700 + 120 * i), st + 0.02); add(thud(-20), st + 0.02)
# S0 hook: rocket roar, slam stop + splash, stopwatch
add(rocket(TS0 - 0.05, -19, 0.15, 0.12), 0.05); add(whoosh(0.5, peak=0.4, level=-21), 0.0)
add(boom(-14, 0.5), TS0); add(splash_sfx(-16, 1.6), TS0 + 0.02); add(thud(-14), TS0)
add(pop(-21, 1200), T("i1", "seconds?") - 0.3); add(ding(-24, 1568), T("i1", "seconds?") - 0.25)
# S0b on purpose stamp, body rings
add(thud(-15), T("i2", "purpose!") - 0.15)
for j in range(3): add(pop(-25, 900 + 200 * j), T("i2", "And") - 0.1 + 0.18 * j)
# S1 dossier + nickname
card_in(S["S1"] + 0.05, -23); add(pop(-23, 1100), T("a1", "Air") + 0.05)
# S1b X over dummy, stamp
add(scratch(-24, 0.25), T("a1", "himself!") - 0.2); add(thud(-14), T("a1", "himself!") - 0.15)
# S2 weight + deadly
add(whoosh(0.5, peak=0.8, f_lo=200, f_hi=1500, level=-25), T("a2", "eighteen") - 0.4); add(thud(-17), T("a2", "eighteen") - 0.1)
add(creak(-26), T("a2", "times") - 0.1); add(boom(-17, 0.35), T("a2", "kill") - 0.1); add(thud(-14), T("a2", "kill") - 0.05)
# S2b wrong stamp
add(thud(-14), T("a3", "wrong.") - 0.2); add(buzzer(-27, 0.35), T("a3", "wrong.") - 0.15)
# S2c straps click + tag
for j in range(2): add(click(-22), T("a3", "strapped") + 0.15 + 0.12 * j)
add(pop(-21, 900), T("a3", "rocket") - 0.2)
# S3a calendar + sign
add(thud(-18), S["S3a"] + 0.05); add(pop(-22, 1000), T("b1", "New") - 0.15)
# S3b nine ignitions + fire
for j in range(9): add(beep(-27, 900 + 90 * j, 0.06), T("b1", "Nine") - 0.05 + 0.065 * j)
add(rocket(1.7, -15, 0.03, 0.4), T("b1", "fire!") - 0.15); add(boom(-14, 0.5), T("b1", "fire!") - 0.15)
# S4 run: roar building, 632 hit
add(rocket(S["S5"] - S["S4"], -19, 0.4, 0.2), S["S4"]); add(whoosh(0.8, peak=0.85, f_lo=200, f_hi=4000, level=-22), T("b2", "six") - 0.7)
add(thud(-15), T("b2", "six") - 0.1); add(pop(-22, 1300), T("b2", "six") + 0.35)
# S5 coasting roar -> water brake slam + splash, stopwatch ticks
add(rocket(TS5 - S["S5"] + 0.1, -22, 0.05, 0.1), S["S5"]); add(boom(-13, 0.55), TS5); add(splash_sfx(-15, 2.0), TS5 + 0.02)
for j in range(5): add(click(-27), TS5 + 0.25 + 0.28 * j)
add(ding(-23, 1318.5), T("b3", "seconds.") - 0.1)
# S6 needle slam
add(whoosh(0.35, peak=0.8, f_lo=500, f_hi=5000, level=-24), T("c1", "forty-six") - 0.4); add(boom(-14, 0.5), T("c1", "forty-six") - 0.1)
glitch(T("c1", "forty-six"), -26)
# S7 scale counting + crack
for j in range(10): add(beep(-31, 1400 + 60 * j, 0.04), T("c2", "weighed") + j * (T("c2", "thousand") - T("c2", "weighed") + 0.2) / 10)
add(crack(-18), T("c2", "thousand") + 0.2); add(thud(-14), T("c2", "thousand") + 0.2); add(creak(-25, 0.6), T("c2", "thousand") + 0.3)
# S8 eye: heartbeat thumps, burst, darkness
for j in range(5): add(thud(-23), S["S8"] + 0.3 + j * 0.9); add(thud(-27), S["S8"] + 0.52 + j * 0.9)
glitch(T("c3", "burst.") - 0.25, -24); add(boom(-18, 0.3), T("c3", "burst.") - 0.2)
add(whoosh(0.6, peak=0.7, f_lo=150, f_hi=900, level=-24), T("c3", "couldn't") - 0.2); add(crt_off(-22, 0.5), T("c3", "couldn't") - 0.05)
# S9 tooth: forceps clink, yank pop, stamp
clink(T("c4", "tooth") - 0.15, -24); add(pop(-16, 500), T("c4", "pulled...") - 0.05); add(scratch(-25, 0.2), T("c4", "pulled...") - 0.08)
add(thud(-15), T("c4", "no") - 0.15)
# S10 sight back: sparkle dings
for j, f0 in enumerate((1318.5, 1568, 2093)): add(ding(-26, f0), T("d1", "sight") + 0.1 + 0.12 * j)
# S11a bars + myth
add(whoosh(0.5, peak=0.8, f_lo=200, f_hi=2500, level=-26), S["S11a"] + 0.05); add(thud(-14), T("e1", "G.") - 0.25)
# S11b belt click
add(whoosh(0.3, peak=0.8, f_lo=600, f_hi=3000, level=-27), T("e1", "seat") - 0.35)
add(click(-16), T("e1", "belts") - 0.05); add(click(-19), T("e1", "belts") + 0.02); add(ding(-24, 1568), T("e1", "belts") + 0.05)
# S12 send + sting
add(pop(-21, 900), S["S12"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
vend = LINES["e2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
for j, f0 in enumerate((1046.5, 1318.5, 1568, 2093)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-10.5) + sfx, vo)
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
