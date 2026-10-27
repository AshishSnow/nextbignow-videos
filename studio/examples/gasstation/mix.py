"""Mix: narrator VO (per-line level automation + room tone) + ducked/carved surf-rock score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1 dBTP)."""
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

# ---- VO level automation (this run's audio upgrade): intimate "secret" lines a bit quieter, reveal lines a bit louder ----
LINE_DB = {"c2": -2.5, "c3": -1.0, "a4": +1.0, "b3": +1.0, "c1": +1.0, "e1": +0.5}
gl = np.zeros(NS, np.float32)
for lid, L in LINES.items():
    a0, a1 = int(L["start"] * SR), int(L["end"] * SR); gl[a0:a1] = LINE_DB.get(lid, 0.0)
ramp = int(0.08 * SR); gl = np.convolve(gl, np.ones(ramp) / ramp, "same").astype(np.float32)
vo = vo * 10 ** (gl / 20)
# room tone: very low filtered noise so the gaps between lines aren't digital silence (A/B: UTMOS 4.30 -> 4.29, within noise)
_rt = rng.standard_normal(NS); _rt = signal.sosfilt(signal.butter(2, [120, 3500], "band", fs=SR, output="sos"), _rt)
_rt = (_rt / np.sqrt(np.mean(_rt ** 2)) * 10 ** (-60 / 20)).astype(np.float32)
_fade = np.clip(np.arange(NS) / (0.3 * SR), 0, 1) * np.clip((NS - np.arange(NS)) / (0.8 * SR), 0, 1)
vo = vo + _rt * _fade.astype(np.float32)
VO = np.stack([vo, vo], 1)
exec(open(f"{_D}/sfx_lib.py").read())


for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-23), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-26), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-25), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-21, 700 + 120 * i), st + 0.02); add(thud(-20), st + 0.02)
# S0 hook: pump ticking, coin drops, "pennies?"
for j in range(int(3.6 / 0.11)): add(click(-33), 0.05 + j * 0.11)
tm = T("i1", "money…") - 0.15; clink(tm + 0.55, -22, 3300); add(pop(-22, 1000), tm + 0.1)
add(thud(-17), T("i1", "gas?") - 0.2)
# S1 stores pop in
for j in range(16): add(pop(-32, 800 + 40 * j), SHOT["S1"]["start"] + 0.06 * j)
# S1b gas can + coin
tf = T("i2", "forty") - 0.25; add(boom(-17, 0.35), tf); add(chaching(-21), tf + 0.05); add(pop(-23, 1200), tf + 0.3)
# S2 receipt prints, stamp
for j in range(10): add(click(-29), SHOT["S2"]["start"] + 0.08 * j)
ts6 = T("a1", "six") - 0.25; add(thud(-13), ts6); add(boom(-20, 0.3), ts6)
# S3 footsteps, door opens
for j in range(5): add(click(-30), SHOT["S3"]["start"] + 0.3 * j)
add(doorbell(-24), T("a2", "Look") - 0.1)
# S4 bars rise
add(whoosh(0.6, peak=0.6, f_lo=200, f_hi=2400, level=-25), T("a3", "ten") - 0.3); add(thud(-18), T("a3", "ten") + 0.4)
add(whoosh(0.6, peak=0.6, f_lo=200, f_hi=2400, level=-25), T("a3", "inside") - 0.55); add(thud(-18), T("a3", "inside") + 0.15)
# S5 cash piles + stamp
for j in range(16): add(pop(-34, 600 + 30 * j), SHOT["S5"]["start"] + 0.09 * j)
tw = T("a4", "twice") - 0.25; add(thud(-13), tw); add(chaching(-19), tw + 0.05); add(boom(-17, 0.4), tw)
# S6-S8 coins fill
for lid, w, lv in (("b1", "fourteen", -20), ("b2", "Forty", -19), ("b3", "fifty", -17)):
    tc = T(lid, w) - 0.25; add(chaching(lv), tc); add(boom(lv + 1, 0.3), tc)
add(pop(-22, 900), T("b3", "pizza") - 0.2); add(pop(-22, 1100), T("b3", "fountain") - 0.2); bubbles(T("b3", "fountain"), 5, -30)
# S9 leaderboard
for j in range(5): add(pop(-26, 700 + 100 * j), SHOT["S9"]["start"] + 0.15 + 0.12 * j)
t5 = T("c1", "fifth") - 0.25; add(boom(-15, 0.45), t5); add(ding(-22, 1568), t5 + 0.05)
# S10 curtain re-hook
tgi = T("c2", "giant") - 0.2; add(whoosh(0.8, peak=0.5, f_lo=200, f_hi=3000, level=-22), tgi - 0.1); add(boom(-15, 0.5), tgi)
# S11 car, road
add(whoosh(1.2, peak=0.4, f_lo=150, f_hi=1500, level=-24), SHOT["S11"]["start"]); add(honk(-24, 0.3), T("c3", "in.") - 0.25)
# S11b snacks pile up
for j in range(5): add(pop(-24, 900 + 120 * j), SHOT["S11b"]["start"] + 0.12 + 0.18 * j)
# S12 stacked bars
add(whoosh(0.6, peak=0.6, f_lo=200, f_hi=2400, level=-25), T("d1", "industry") - 0.15); add(thud(-17), T("d1", "sixty") - 0.3)
add(boom(-15, 0.4), T("d1", "under") - 0.25)
# S13 card in, beep, check
tp = T("d2", "pay") - 0.2; card_in(tp + 0.3, -24); add(beep(-25, 2200, 0.1), tp + 0.5); add(ding(-24, 1760), tp + 0.6)
for j in range(12): add(click(-34), SHOT["S13b"]["start"] + 0.18 * j)
# S14 reveal + loop back to the sign
add(boom(-16, 0.4), SHOT["S14b"]["start"] + 0.02); add(whoosh(0.5, peak=0.8, f_lo=300, f_hi=3000, level=-23), T("e1", "giant") - 0.3); add(thud(-15), T("e1", "giant") - 0.2)
# S15 send + sting
add(pop(-21, 900), SHOT["S15"]["start"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
vend = LINES["e2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
for j, f0 in enumerate((1318.5, 1568, 1975.5, 2637)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-12.0) + sfx, vo)
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
