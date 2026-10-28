"""Mix: narrator VO + ducked/carved calypso score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1.5 dBTP)."""
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
# ---- VO level automation: per-line dB offsets (quiet "secret" lines ~-2.5, reveal lines ~+1) + -60 dB room tone in the gaps ----
LINE_DB = {"i1": +1.0, "i3": +0.5, "a6": +0.5, "b5": -1.5, "b8": +1.0, "c1": -1.0, "t1": +1.0, "t2": +0.5}   # quiet "spores wait", louder reveals
gl = np.zeros(NS, np.float32)
for lid, L in LINES.items():
    a0, a1 = int(L["start"] * SR), int(L["end"] * SR); gl[a0:a1] = LINE_DB.get(lid, 0.0)
ramp = int(0.08 * SR); gl = np.convolve(gl, np.ones(ramp) / ramp, "same").astype(np.float32)
vo = vo * 10 ** (gl / 20)
_rt = np.random.default_rng(77).standard_normal(NS); _rt = signal.sosfilt(signal.butter(2, [120, 3500], "band", fs=SR, output="sos"), _rt)
_rt = (_rt / np.sqrt(np.mean(_rt ** 2)) * 10 ** (-60 / 20)).astype(np.float32)
vo = vo + _rt * (np.clip(np.arange(NS) / (0.3 * SR), 0, 1) * np.clip((NS - np.arange(NS)) / (0.8 * SR), 0, 1)).astype(np.float32)
VO = np.stack([vo, vo], 1)
exec(open(f"{_D}/sfx_lib.py").read())

for i, s_ in enumerate(SHOTS[1:], 1):
    k = s_["trans"]; st = s_["start"]
    if k == "whip": add(whoosh(0.4, level=-23), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-26), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-25), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-21, 700 + 120 * i), st + 0.02); add(thud(-20), st + 0.02)
# new SFX for this video: photocopier scan (generic synthesis)
def copier_scan(level=-30, dur=0.55):
    tt = np.arange(int(dur * SR)) / SR; env = np.clip(tt / 0.05, 0, 1) * np.clip((dur - tt) / 0.12, 0, 1)
    nz = signal.sosfilt(signal.butter(2, [900, 6000], "band", fs=SR, output="sos"), np.random.default_rng(5).standard_normal(len(tt)))
    hum = np.sin(2 * np.pi * 120 * tt) * 0.4
    x = (nz * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * tt)) + hum) * env; x = (x / (np.abs(x).max() + 1e-9) * db(level)).astype(np.float32)
    return np.stack([x, x], 1)


def copier_run(t0, t1, per=0.85, lv=-31):
    t = t0 + (per - (t0 % per)) % per
    while t < t1 - 0.3:
        add(copier_scan(lv), t); add(pop(lv + 2, 1500), t + 0.45); t += per


# S0 / S24 / S27: the copier keeps printing bananas
copier_run(0.0, SHOT["S0b"]["start"]); copier_run(SHOT["S24"]["start"], SHOT["S25"]["start"], lv=-32); copier_run(SHOT["S27"]["start"], SHOT["S28"]["start"])
for j in range(5): add(pop(-25, 600 + 120 * j), SHOT["S0b"]["start"] + 0.06 * j)
add(thud(-18), T("i2", "worried.") - 0.15)
for j in range(3): add(pop(-23, 700 + 200 * j), T("i3", "Three") + 0.12 * j)
add(thud(-14), T("i3", "already") - 0.1); add(boom(-19, 0.3), T("i3", "already") - 0.1)
# S4 slice + sprout + stamp
add(scratch(-26, 0.25), SHOT["S4"]["start"] + 0.05)
add(pop(-24, 1200), T("a2", "never") - 0.1); add(thud(-15), T("a2", "never") + 0.45)
# S5b clones popping in
for j in range(5): add(pop(-25, 800 + 90 * j), SHOT["S5b"]["start"] + 0.1 + 0.14 * j)
add(ding(-25, 1568), T("a4", "half") + 0.4)
# S8 helix shimmer, S8b wilting wave
add(whoosh(0.8, peak=0.6, f_lo=400, f_hi=6000, level=-28), SHOT["S8"]["start"] + 0.05)
add(boom(-16, 0.5), T("a6", "kill") - 0.2)
# S10/S11 fungus creeping, water blocked
add(creak(-27, 0.8), SHOT["S10"]["start"] + 0.2); bubbles(T("b3", "water") - 0.2, 6, -28)
add(thud(-17), T("b3", "blocks") - 0.15); add(creak(-24, 0.7), T("b3", "wilts") - 0.2)
# S12 spray + NO CURE
for j in range(4): add(whoosh(0.18, peak=0.3, f_lo=2000, f_hi=8000, level=-30), SHOT["S12"]["start"] + 0.1 + 0.4 * j)
add(thud(-13), T("b4", "No") - 0.1)
# S13 flapboard clatter
for j in range(14): add(click(-27), T("b5", "wait") - 0.1 + j * 0.05)
# S15-S17 map pins
for w_ in ("Colombia,", "Peru,", "Venezuela,"): add(pop(-21, 900), T("b7", w_) - 0.1); add(thud(-21), T("b7", w_) - 0.05)
add(boom(-15, 0.5), T("b8", "Ecuador.") - 0.15); add(pop(-20, 800), T("b8", "Ecuador.") - 0.1)
add(ding(-24, 1318.5), T("b8", "biggest") - 0.1)
add(thud(-16), T("b9", "July") - 0.2)
# S18 tape rewind, S19 flapboard
add(whoosh(0.6, peak=0.4, f_lo=1500, f_hi=7000, level=-24), T("c0", "already") - 0.15)
for j in range(10): add(click(-29), T("c0", "already") - 0.1 + j * 0.04)
for j in range(14): add(click(-27), T("c1", "happened") - 0.2 + j * 0.05)
# S20 shop bell, S21-S22 old fungus spreading
add(doorbell(-27), SHOT["S20"]["start"] + 0.1)
add(boom(-19, 0.4), T("c3", "hit") - 0.15)
for j in range(3): add(thud(-23), T("c4", "followed") - 0.25 + 0.35 * j)
# S23 the switch: slide + RESISTANT stamp + reveal
add(whoosh(0.6, peak=0.5, level=-25), SHOT["S23"]["start"] + 0.1); add(thud(-16), T("c5", "couldn't") - 0.15)
add(chaching(-23), T("c5", "Cavendish.") - 0.15)
# S25 kills it too
add(boom(-14, 0.6), T("t2", "kills") - 0.15); add(creak(-25, 0.6), T("t2", "kills"))
# S26b basket tips, bananas fall
add(creak(-24, 0.4), T("e0", "hits") - 0.3); add(thud(-14), T("e0", "hits") - 0.2)
for j in range(4): add(thud(-24), T("e0", "hits") + 0.15 + 0.08 * j)
# S28 send + sting
add(pop(-21, 900), SHOTS[-1]["start"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
vend = LINES["e2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
for j, f0 in enumerate((1046.5, 1318.5, 1568, 2093)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-10.5) + sfx, vo)
# word guard: no SFX hit / loud note within 12 dB of a word on a phone speaker (GUARD=0 disables; studio/tools/mix_check.py measures it)
if float(os.environ.get("GUARD", 12)) > 0: bed = bed_carve.guard(bed, vo, ld=float(os.environ.get("GUARD", 12)))
mix = VO + bed
sf.write(f"{B}/work/mix_pre.wav", mix, SR, subtype="FLOAT")
sf.write(f"{B}/work/stem_vo.wav", vo, SR, subtype="FLOAT"); sf.write(f"{B}/work/stem_bed.wav", bed, SR, subtype="FLOAT")
TGT = -11.0
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{B}/work/mix_pre.wav", "-af", f"loudnorm=I={TGT}:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
ln = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
print("loudnorm mode:", ln["normalization_type"], "| pre-master I", ln["input_i"], "TP", ln["input_tp"])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/mix_pre.wav", "-af",
                f"loudnorm=I={TGT}:TP=-1.5:LRA=9:measured_I={ln['input_i']}:measured_TP={ln['input_tp']}:measured_LRA={ln['input_lra']}:"
                f"measured_thresh={ln['input_thresh']}:offset={ln['target_offset']}:linear=true,aresample=48000", "-c:a", "pcm_s16le", f"{B}/work/mix.wav"], check=True)
hp = signal.butter(2, 150, "high", fs=SR, output="sos"); vv = signal.sosfilt(hp, vo); bb = signal.sosfilt(hp, bed.mean(1))
print("VO/bed dB:", " ".join(f"{lid}:{20*np.log10(np.sqrt(np.mean(vv[int(L['start']*SR):int(L['end']*SR)]**2))/np.sqrt(np.mean(bb[int(L['start']*SR):int(L['end']*SR)]**2)+1e-12)):.0f}" for lid, L in LINES.items()))
