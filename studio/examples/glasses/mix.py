"""Mix: narrator VO + ducked/carved disco score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1.5 dBTP)."""
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
LINE_DB = {"i1": +1.0, "i3": +0.5, "a5": +0.5, "d1": -1.5, "d3": +1.0, "s4": +1.0, "s5": +0.5, "t1": +1.0}   # quiet "sneaky door", louder reveals
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
# # new SFX for this video: a door swinging open (latch click + creak + air), a smart-glasses "capture" beep (generic synthesis)
def door_open(t0, lv=-24):
    add(click(lv - 2), t0); add(creak(lv - 2, 0.5), t0 + 0.05); add(whoosh(0.5, peak=0.6, f_lo=200, f_hi=2500, level=lv - 2), t0 + 0.15)


def beep(level=-28, f0=2400, dur=0.09):
    tt = np.arange(int(dur * SR)) / SR; env = np.clip(tt / 0.005, 0, 1) * np.clip((dur - tt) / 0.03, 0, 1)
    x = (np.sin(2 * np.pi * f0 * tt) * env * db(level)).astype(np.float32); return np.stack([x, x], 1)


add(pop(-25, 900), T("i1", "shop,") - 0.2); add(pop(-24, 1100), T("i1", "insurance") - 0.25); add(thud(-18), T("i1", "one") - 0.1)
for j in range(4): add(thud(-23), T("i3", "four") - 0.15 + 0.12 * j)
add(thud(-14), T("i3", "sneakiest") - 0.15); add(boom(-19, 0.3), T("i3", "sneakiest") - 0.15)
for sid in ("S3", "S8", "S11", "S20"): door_open(SHOT[sid]["start"] + 0.2)
for w_ in ("Ray-Ban.", "Oakley.", "Persol.", "Oliver"): add(pop(-23, 1000), T("a2", w_) - 0.15)
add(thud(-17), T("a2", "All") - 0.1)
for w_ in ("Chanel,", "Prada,", "Armani,", "Versace,", "Michael"): add(pop(-25, 1400), T("a3", w_) - 0.12)
add(scratch(-27, 0.25), T("a4", "licence") - 0.2); add(thud(-20), T("a4", "licence"))
add(whoosh(0.5, peak=0.6, f_lo=600, f_hi=5000, level=-26), T("a5", "one") - 0.2); add(thud(-17), T("a5", "one") + 0.25)
for j in range(14): add(click(-27), SHOT["S9"]["start"] + 0.05 + j * 0.05)
add(whoosh(0.6, peak=0.5, level=-25), T("b2", "joined") - 0.1); add(thud(-15), T("b2", "joined") + 0.55)
clink(T("b3", "same") - 0.35, -24); add(thud(-17), T("b3", "same") - 0.15)
add(doorbell(-27), SHOT["S12"]["start"] + 0.1); add(thud(-16), T("c2", "same") - 0.15)
for j in range(10): add(click(-28), T("c3", "twenty") - 0.15 + j * 0.11)
add(scratch(-24, 0.35), T("c4", "Oakley.") - 0.25)
for j in range(14): add(click(-27), SHOT["S15"]["start"] + 0.05 + j * 0.05)
add(thud(-14), T("s2", "bought") - 0.15)
add(whoosh(0.5, peak=0.5, f_lo=200, f_hi=1500, level=-25), T("s3", "fewer") - 0.2)
add(boom(-14, 0.6), T("s4", "fell") - 0.15)
for j in range(14): add(click(-27), SHOT["S19"]["start"] + 0.05 + j * 0.05)
add(chaching(-22), T("s5", "billion") - 0.2)
add(thud(-17), T("d3", "same") - 0.1); add(boom(-18, 0.4), T("d3", "same") - 0.1)
for j in range(3): add(beep(-27, 2400 + 300 * j), T("d4", "smart") + 0.05 + 0.12 * j)
add(ding(-24, 1568), T("d4", "three") - 0.1)
for w_ in ("frame,", "lens,", "shop,", "plan"): add(pop(-22, 900), T("t1", w_) - 0.2)
add(thud(-13), T("t1", "pays.") - 0.15)
add(scratch(-27, 0.2), T("e0", "free") - 0.3); add(ding(-24, 2093), T("e0", "free") - 0.1)
for j in range(4): add(pop(-24, 800 + 150 * j), T("e1", "anywhere") + 0.1 + 0.1 * j)
# S27 send + sting
add(pop(-21, 900), SHOTS[-1]["start"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
vend = LINES["e2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
for j, f0 in enumerate((1046.5, 1318.5, 1568, 2093)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-9.5) + sfx, vo)
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
