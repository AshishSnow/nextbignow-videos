"""Mix: narrator VO + ducked/carved spaghetti-western score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP). New foley (ep 23, kept here): crackle, munch_sfx. A real fizz runs under every burning fuse."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(42)
db = lambda x: 10 ** (x / 20)
S = {k: st for k, st, _ in SHOTLIST}; TF = T("i1", "first") - 0.22
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
def crackle(level=-26, dur=1.0):
    """a burning fuse / cracker crackle: sparse random clicks over a noise floor (new foley, ep 23)."""
    N_ = int(dur * SR); x = np.zeros(N_); r_ = np.random.default_rng(int(dur * 100) + 3)
    for i in range(int(dur * 42)):
        p = r_.integers(0, max(1, N_ - 900)); L_ = r_.integers(120, 800); x[p:p + L_] += r_.normal(0, 1, L_) * np.exp(-np.linspace(0, 6, L_)) * r_.uniform(0.3, 1)
    x = x / (np.abs(x).max() + 1e-9) * db(level)
    return np.stack([x, x], 1).astype(np.float32)
def munch_sfx(level=-22, dur=1.2):
    """fast happy chewing (ep 23): soft crunches with squelchy tails."""
    N_ = int(dur * SR); x = np.zeros(N_); r_ = np.random.default_rng(5); t_ = 0.0
    while t_ < dur - 0.2:
        p = int(t_ * SR); L_ = int(0.09 * SR); x[p:p + L_] += r_.normal(0, 1, L_) * np.exp(-np.linspace(0, 5, L_)) * r_.uniform(0.6, 1); t_ += r_.uniform(0.14, 0.2)
    b_ = signal.butter(2, [300, 3200], "band", fs=SR, output="sos"); x = signal.sosfilt(b_, x); x = x / (np.abs(x).max() + 1e-9) * db(level)
    return np.stack([x, x], 1).astype(np.float32)
# fuses: a real fizz under every burning shot; the POOF is a soft thud + puff (it isn't an explosion: the sweet just gives up)
def fzz(t0, t1, lv=-30): add(fizz(lv, max(0.3, t1 - t0)), t0)
def clack_list(t, f0=900, lv=-25): add(pop(lv, f0), t)
fzz(0.0, TF + 0.05, -24); add(hiss(-27, TF), 0.0); add(soft_flop(-13), TF); add(thud(-15), TF); add(suction(-24), TF + 0.03); add(boing(-24, 150, 0.4), TF + 0.1); stamp(TF + 0.02, -18)
add(rec_scratch(-27), TF + 0.05); add(creep(-26) if False else tick(-27), S["S1"] + 0.1); add(pop(-24, 700), T("i2", "tonight") - 0.15); add(squelch(-26, 0.4), S["S1"] + 0.3)
for j in range(5): add(rip(-30, 0.1), S["S1b"] + j * 0.06)
add(ding(-24, 1568), T("i2", "month") - 0.2)
add(pop(-22, 500), T("i3", "cracker") - 0.15); fzz(T("i3", "fuse") - 0.15, S["S2b"], -28); fzz(S["S2b"], S["S3"], -22); add(crackle(-26, S["S3"] - S["S2b"]), S["S2b"]); stamp(T("i3", "lit") - 0.2, -17)
add(rustle(-22, 0.8), T("a1", "food")); add(clack(-24, 700), T("a1", "list") - 0.3)
add(pop(-22, 700), T("a2", "kalaakund") - 0.15); fzz(S["S4"], S["S4b"], -27); add(munch_sfx(-22, 1.3), S["S4b"] + 0.1); add(tick(-27), S["S4b"] + 0.2); add(tick(-27), S["S4b"] + 0.5)
add(suction(-22), S["S5"]); add(fridge_hum(-30, S["S6"] - S["S5"]), S["S5"])
for w_, f0 in (("Rusgoola", 800), ("rusmalaai", 1000), ("sundaysh", 1200)): add(pop(-23, f0), T("a3", w_) - 0.1)
stamp(T("a3", "two") - 0.1, -19)
for w_, f0 in (("Milk", 800), ("payda", 1000), ("boondee", 1200)): add(pop(-23, f0), T("a4", w_) - 0.1)
for j in range(4): add(rip(-25, 0.12), T("a4", "four") - 0.15 + j * 0.14)
for j in range(7): add(tick(-25), S["S7"] + 0.1 + j * 0.06)
add(ding(-24, 1760), T("a5", "week") - 0.15)
for tq in [S["S8"] + k * 0.54 for k in range(int((S["S8b"] - S["S8"]) / 0.54) + 1)]: add(footstep(-22), tq)
add(boom(-20, 0.3), T("a6", "month") - 0.2); fzz(S["S8"], S["S8b"], -30)
for j in range(5): add(pop(-26, 700 + 120 * j), S["S8b"] + j * 0.08)
add(pop(-21, 400), T("b1", "month") - 0.3); add(plip(-16), T("b2", "water") - 0.2); sparkle_sfx(T("b2", "water") - 0.05, -28)
for w_ in ("rusgoola", "kalaakund", "milk"): add(plip(-22), T("b2", w_) - 0.1); add(sip(-27), T("b2", w_))
for w_, f0 in (("roasted", 800), ("ghee", 1000), ("sugar", 1200)): add(pop(-24, f0), T("b3", w_) - 0.12)
stamp(T("b3", "No") - 0.1, -17); add(buzzer(-29, 0.2), T("b3", "hardly") - 0.05)
add(drink(-22, 3, 0.2), S["S12"] + 0.15); add(giggle(-26), S["S12"] + 0.5); add(nibble(-24), T("b4", "meal") - 0.3); add(giggle(-24), T("b4", "meal") - 0.1); add(pop(-22, 500), T("b4", "meal") - 0.15)
for tq in [S["S13"] + k * 0.54 for k in range(4)]: add(footstep(-22), tq)
add(pop(-23, 1000), T("c2", "bacteria") - 0.15); add(pop(-23, 700), T("c2", "mould") - 0.15); add(ding(-25, 1760), T("c2", "nine") - 0.3); add(ding(-25, 1318.5), T("c2", "seven") - 0.3)
for tq in [S["S15"] + k * 0.27 for k in range(5)]: add(footstep(-23), tq)
add(ding(-24, 1568), T("c3", "zero") - 0.1); add(whoosh(0.35, peak=0.6, level=-27), S["S15b"] + 0.1); add(creep(-24), T("c3", "mould") - 0.2)
add(creep(-20), T("c4", "fuzz") - 0.5); add(boing(-24, 180, 0.3), T("c4", "fuzz") - 0.15); stamp(T("c4", "fuzz") - 0.15, -18)
for j in range(4): add(scrub(-23, 0.25), T("c5", "scrape") - 0.1 + j * 0.28)
stamp(T("c5", "scrape") - 0.05, -18); add(crt_off(-28, 0.3), S["S17b"]); add(creep(-24), S["S18"] + 0.1); add(giggle(-27), T("c6", "bacteria") - 0.1)
pedal_bin(T("c6", "bin") - 0.5, -18); add(thud(-18), T("c6", "bin") - 0.1)
add(fridge_hum(-28, S["S20"] - S["S19"]), S["S19"]); add(rustle(-24, 0.5), S["S19"] + 0.1); stamp(T("d1", "Nearly") - 0.1, -18)
add(pop(-23, 900), T("d2", "nine") - 0.1); add(whoosh(0.8, peak=0.7, f_lo=400, f_hi=2400, level=-29), T("d2", "thirty", 1) - 0.1)
add(crust_crack(-20, 0.3), T("d3", "dry") - 0.1); add(bread_knock(-17), T("d3", "hard") - 0.1); add(rustle(-25, 0.3), T("d3", "sandy") - 0.1)
add(tooth_crack(-14), T("d4", "rock") - 0.15); add(clang(-20), T("d4", "rock") - 0.13)
add(clip_snap(-13), T("d4", "airtight") - 0.1); add(pop(-23, 600), T("d4", "cardboard") - 0.15); add(buzzer(-30, 0.2), T("d4", "cardboard"))
stamp(T("e1", "regift") - 0.3, -18); add(rustle(-24, 0.4), S["S23"] + 0.1)
for w_, nth in (("gives", 0), ("pass", 0), ("gives", 1)):
    t_ = T("e2", w_, nth) - 0.05; add(whoosh(0.5, peak=0.5, f_lo=300, f_hi=2600, level=-23), t_); add(thud(-22), t_ + 0.6); add(pop(-24, 800), t_ + 0.62)
add(doorbell(-26), S["S24"] + 0.05); fzz(S["S24"], S["S25"], -31)
add(rustle(-23, 0.3), S["S25"] + 0.05); add(rec_scratch(-26), S["S25"] + 0.3); stamp(T("e3", "resets") - 0.15, -17)
add(thud(-19), T("e3", "Tuesday") - 0.15); add(boom(-22, 0.3), S["S25b"]); add(crt_off(-28, 0.3), S["S25b"])
add(doorbell(-29), S["S26"] + 0.1); add(clack(-24, 800), T("e4", "check") - 0.2); add(pop(-20, 900), T("e4", "best") - 0.15); add(ding(-23, 1568), T("e4", "best") - 0.1)
add(buzzer(-29, 0.2), S["S27"] + 0.1); add(rustle(-24, 0.3), T("e5", "list") - 0.2); fzz(T("e5", "hot") - 0.15, S["S28"], -24); add(sizzle(-28, S["S28"] - T("e5", "hot")), T("e5", "hot") - 0.1)
add(pop(-22, 800), T("f1", "first") - 0.15); add(pop(-22, 1100), T("f1", "last") - 0.15)
add(lock_click(-18), S["S29"] + 0.15); add(snap(-22), S["S29"] + 0.2)
for w_, f0 in (("Kalaakund", 880), ("rusgoola", 988), ("burfee", 1109), ("kaaju", 1319), ("luddoo", 1480)): add(pop(-23, 900), T("f2", w_) - 0.1); add(ding(-27, f0), T("f2", w_) - 0.08)
add(suction(-22), T("f3", "sour") - 0.2); add(suction(-24), T("f3", "sour") + 0.1); add(creep(-26), T("f3", "fuzz") - 0.3); pedal_bin(T("f3", "bin") - 0.3, -18); add(thud(-16), T("f3", "bin") - 0.05); stamp(T("f3", "bin") - 0.15, -18)
add(pop(-18, 1300), T("g1", "Send") + 0.3); add(ding(-22, 2093), T("g1", "Send") + 0.32); add(doorbell(-24), T("g1", "know", 1) - 0.1)
vend = LINES["g1"]["end"] + 0.35
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
