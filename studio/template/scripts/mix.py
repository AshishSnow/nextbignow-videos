"""Mix: energetic narrator VO + ducked/carved funk score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1.5 dBTP)."""
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
LINE_DB = {}   # e.g. {"c2": -2.5, "a4": +1.0}
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
# S0: vault door creaks open, money spills, big number
add(creak(-27, 0.5), 0.3); add(thud(-18), 0.62); add(clink(0.66, -24, 2600), 0) if False else clink(0.66, -24, 2600)
for j in range(6): add(scratch(-33, 0.12), 0.8 + j * 0.12)
to = T("i1", "one") - 0.15; add(chaching(-20), to); add(ding(-25, 1568), to + 0.08)
add(pop(-22, 900), T("i1", "your") - 0.1)
# S0b banks pop
for i in range(3): add(pop(-25, 600 + 150 * i), T("i2", "banks") - 0.15 + i * 0.1)
# S1 morph
add(whoosh(0.5, peak=0.7, f_lo=300, f_hi=5000, level=-24), T("i3", "became") - 0.6); add(boom(-17, 0.35), T("i3", "became") - 0.2)
# S2a reload
tl = T("a1", "load") - 0.1; add(whoosh(0.3, level=-27), tl); add(ding(-22, 1760), tl + 0.35); add(pop(-23, 800), T("a1", "before") - 0.1)
# S2b +$25 +$50, millions
for tt_ in (T("a2", "Twenty-five") - 0.1, T("a2", "Fifty") - 0.1): add(whoosh(0.3, level=-28), tt_); add(chaching(-25), tt_ + 0.3)
tm = T("a2", "Millions") - 0.12
for j in range(24): add(pop(-32, 500 + 30 * j), tm + 0.02 * ((j * 7) % 24))
# S2c today / later
for j in range(5): add(scratch(-33, 0.1), SHOTS[5]["start"] + 0.3 + 0.18 * j)
add(thud(-19), T("a3", "today…") - 0.25); add(ding(-24, 1318.5), T("a3", "later.") - 0.25)
# S3a stamp, S3b coins / $0
add(thud(-12), T("b1", "zero") + 0.06)
ti = T("b2", "interest") - 0.15
for j in range(5): clink(ti + j * 0.08, -26, 2400 + 200 * (j % 3))
add(buzzer(-24, 0.35), T("b2", "nothing!") - 0.2); add(thud(-16), T("b2", "nothing!") - 0.2)
# S4 never spent / forgotten / $200M / revenue
add(whoosh(0.8, peak=0.5, f_lo=200, f_hi=1200, level=-28), T("c1", "never") - 0.3)
add(creak(-28, 0.5), T("c2", "Forgotten") - 0.1); add(pop(-23, 700), T("c2", "few") - 0.15)
for j in range(18): add(thud(-31), SHOTS[10]["start"] + 0.15 + j * 0.13)
add(chaching(-20), T("c3", "two") - 0.15); add(boom(-18, 0.3), T("c3", "two") - 0.15)
for j in range(4): add(scratch(-32, 0.1), SHOTS[11]["start"] + 0.3 + j * 0.22)
add(ding(-23, 1046.5), T("c4", "revenue…") - 0.2); add(buzzer(-26, 0.25), T("c4", "no") - 0.12)
# S5 4 in 10
for i in range(4): add(pop(-25, 900 + 120 * i), T("d1", "four") - 0.15 + 0.08 * i)
# S6 funding a bank
add(click(-20), T("e1", "top") - 0.1); add(ding(-24, 1760), T("e1", "top") + 0.1)
add(boom(-17, 0.35), T("e1", "funding") - 0.2)
# S7 send + sting
add(pop(-21, 900), SHOTS[-1]["start"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
vend = LINES["e2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
for j, f0 in enumerate((1046.5, 1318.5, 1568, 2093)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-12.0) + sfx, vo)
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
