"""Mix: narrator VO + ducked/carved bossa score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP).
New foley (ep 18, also added to sfx_lib): simmer (a rolling boil: random low plips + a soft rumble), foam_rise (the foam climbing: a
band-passed noise swell that rises in pitch and loudness), spill_sizzle (milk hitting the flame: sharp sizzle + a steam hiss burst),
pop_bubble (a dry little steam-bubble pop), knob (the gas knob click + a short gas whoosh); reused: whoosh/pop/ding/thud/boom/boing/
buzzer/plip/sizzle/hiss/fizz/wash/squelch/clang/tick/crinkle/clack/gulp/rec_scratch/chaching."""
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
TOVER = T("i1", "over,") - 0.1
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
exec(open(f"{_D}/sfx_lib.py").read())


def simmer(level=-28, dur=2.0, rate=9):
    """a rolling boil: random low plips over a soft rumble."""
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [80, 400], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * 0.25
    for k in range(int(dur * rate)):
        i = int(rng.uniform(0, dur - 0.08) * SR); seg = t2[: int(0.07 * SR)]; f0 = rng.uniform(300, 900)
        y[i:i + len(seg)] += np.sin(2 * np.pi * np.cumsum(f0 * (1 + 0.8 * np.exp(-seg / 0.01))) / SR) * np.exp(-seg / 0.02) * rng.uniform(0.4, 1.0)
    y *= np.sin(np.pi * np.clip(t2 / dur, 0, 1)) ** 0.3
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 120)


def foam_rise(level=-22, dur=1.6):
    """the foam climbing: a band-passed noise swell rising in pitch and loudness, with little pops on top."""
    t2 = np.arange(int(dur * SR)) / SR; x = t2 / dur
    nz = rng.standard_normal(len(t2))
    f_, tt_, Z = signal.stft(nz, SR, nperseg=1024); fc = 400 * (3000 / 400) ** (tt_ / dur)
    mask = np.exp(-0.5 * ((np.log2(np.maximum(f_, 20))[:, None] - np.log2(fc)[None]) / 0.9) ** 2)
    _, y = signal.istft(Z * mask, SR, nperseg=1024); y = y[: len(t2)] * (0.15 + 0.85 * x ** 1.6)
    for k in range(18):
        i = int(rng.uniform(0.2, dur - 0.05) * SR); seg = t2[: int(0.03 * SR)]
        y[i:i + len(seg)] += np.sin(2 * np.pi * rng.uniform(900, 2200) * seg) * np.exp(-seg / 0.006) * 0.8
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 100)


def spill_sizzle(level=-16, dur=1.4):
    """milk hitting the flame: a sharp sizzle burst + a steam hiss that decays."""
    t2 = np.arange(int(dur * SR)) / SR
    sz = signal.sosfilt(signal.butter(2, [2000, 9000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 37 * t2)))
    hs = signal.sosfilt(signal.butter(2, [800, 4000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2)))
    y = sz * np.exp(-t2 / 0.35) * 1.2 + hs * np.exp(-t2 / 0.9) * 0.6 + np.sin(2 * np.pi * 70 * t2) * np.exp(-t2 / 0.06)
    return _st(y / np.abs(y).max() * db(level), 80)


def pop_bubble(level=-24, f0=1200):
    t2 = np.arange(int(0.08 * SR)) / SR
    y = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 2.0 * np.exp(-t2 / 0.006))) / SR) * np.exp(-t2 / 0.014)
    y += signal.sosfilt(signal.butter(2, [2500, 8000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.004) * 0.6
    return _st(y / np.abs(y).max() * db(level))


def knob(level=-24):
    """gas knob: a click + a short gas whoosh."""
    t2 = np.arange(int(0.5 * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [1500, 6000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.005) * 2
    y += signal.sosfilt(signal.butter(2, [300, 2000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-((t2 - 0.12) / 0.08) ** 2) * 0.5
    return _st(y / np.abs(y).max() * db(level))


def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)


def sparkle_sfx(t, lv=-24): add(ding(lv, 2637), t); add(ding(lv - 3, 3520), t + 0.05); add(ding(lv - 6, 4186), t + 0.1)


def pops_at(t0, n_=5, gap=0.12, lv=-25):
    for j in range(n_): add(pop_bubble(lv, 900 + 200 * (j % 4)), t0 + gap * j)


for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-24), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-27), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-26), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-22, 700 + 60 * (i % 8)), st + 0.02); add(thud(-21), st + 0.02)
# HOOK: the boil is already rolling at frame 0, the foam rises, SPILL on 'over', water pot bubbles pop
add(simmer(-26, TOVER + 0.3, 10), 0.0); add(foam_rise(-21, TOVER - 0.05), 0.05)
add(spill_sizzle(-14, 1.5), TOVER); add(boom(-18, 0.4), TOVER); add(clang(-26, 900, 0.4), TOVER + 0.05); add(thud(-20), TOVER + 0.42)
add(pop_bubble(-24), T("i1", "water") - 0.05); pops_at(T("i1", "water") + 0.2, 4, 0.22, -27)
add(simmer(-29, 6.0, 8), S["S1"]); pops_at(S["S1"] + 0.4, 8, 0.3, -27); add(foam_rise(-24, 1.2), T("i2", "climbs") - 0.3)
add(spill_sizzle(-19, 1.0), T("i2", "climbs") + 0.8); add(rec_scratch(-26), T("i2", "climbs") + 0.3); add(pop(-23, 1200), T("i2", "climbs") + 0.9)
add(clack(-24, 1700), S["S2"] + 0.6); add(simmer(-30, 4.0, 7), S["S2"]); add(tick(-28), T("i3", "seconds.") - 0.1); add(tick(-28), T("i3", "seconds.") + 0.3); add(buzzer(-28, 0.3), T("i3", "seconds.") + 0.4)
add(creak(-26, 0.6), S["S2b"] + 0.2); add(ding(-24, 2093), T("i3", "works") - 0.1)
# part 1 water
add(boom(-19, 0.35), S["S3"] + 0.05); card_in(S["S3"] + 0.1, -26); add(simmer(-28, 5.0, 9), S["S3"])
pops_at(T("a1", "pop.") - 0.1, 6, 0.09, -20); add(pop(-22, 1500), T("a1", "Gone.") - 0.1)
add(simmer(-30, 3.0, 8), S["S4"]); pops_at(S["S4"] + 0.3, 5, 0.4, -28); add(ding(-25, 1568), T("a2", "never") - 0.1)
# part 2 milk
add(boom(-19, 0.35), S["S5"] + 0.05); card_in(S["S5"] + 0.1, -26); add(wash(-26, 1.2), T("b1", "ninety") - 0.3)
for j in range(9): add(tick(-30), T("b1", "ninety") - 0.1 + 0.11 * j)
add(chaching(-26), T("b1", "everything.") - 0.15); sparkle_sfx(T("b1", "everything.") - 0.1, -23)
for j, w in enumerate(("protein", "fat,", "sugar.")): add(pop(-23, 800 + 150 * j), T("b2", w) - 0.1); add(clack(-28, 1500), T("b2", w) - 0.08)
for j in range(5): add(boing(-28, 300 + 40 * j, 0.3), S["S6b"] + 0.15 + 0.1 * j)
add(squelch(-27, 0.6), T("b2", "edge") - 0.05); sparkle_sfx(T("b2", "edge") + 0.3, -26)
add(simmer(-30, 3.0, 7), S["S7"]); add(plip(-26, 700), S["S7"] + 0.3); add(crinkle(-27, 0.5), T("b3", "jacket.") - 0.3); stamp(T("b3", "jacket.") - 0.15, -19)
add(plip(-25, 900), S["S7b"] + 0.3); add(boing(-24, 220, 0.4), T("b3", "doesn't") - 0.1); add(buzzer(-27, 0.25), T("b3", "doesn't") + 0.1)
add(boom(-21, 0.35), S["S8"] + 0.02); stamp(T("b4", "surfactant.") - 0.15, -18); add(pop(-24, 1000), T("b4", "name:") - 0.1)
add(squirt(-24, 0.35), S["S8b"] + 0.1); add(fizz(-25, 1.4), S["S8b"] + 0.3); pops_at(S["S8b"] + 0.5, 7, 0.17, -27); add(ding(-24, 2093), T("b4", "foam.") - 0.1)
# part 3 foam + skin
add(boom(-19, 0.35), S["S9"] + 0.05); card_in(S["S9"] + 0.1, -26); pops_at(T("c1", "pile") - 0.05, 14, 0.09, -27); add(foam_rise(-25, 1.5), T("c1", "pile") - 0.1); stamp(T("c1", "foam.") - 0.15, -18)
add(crt_off(-30, 0.4), S["S10"] + 0.02); add(boom(-18, 0.45), T("c2", "worse.") - 0.1); add(hiss(-26, 1.4), T("c2", "evaporates") - 0.1)
for j in range(3): add(whoosh(0.3, peak=0.5, f_lo=500, f_hi=3000, level=-29), T("c2", "evaporates") + 0.1 * j)
for j in range(10): add(plip(-29, 600 + 40 * j), S["S10b"] + 0.15 + 0.18 * j)
add(squelch(-24, 0.8), T("c2", "thicker.") - 0.2); add(thud(-21), T("c2", "thicker.") - 0.15)
add(crinkle(-23, 0.6), T("c3", "skin.") - 0.3); stamp(T("c3", "skin.") - 0.12, -20); add(rustle(-27, 0.4), T("c3", "wrinkly") - 0.05)
add(clang(-22, 700, 0.6), T("c4", "lid.") - 0.12); add(thud(-18), T("c4", "lid.") - 0.12); pops_at(S["S12"] + 0.3, 6, 0.35, -28); add(buzzer(-27, 0.3), T("c4", "can't") - 0.05)
add(foam_rise(-20, max(0.8, T("c4", "over") - 0.15 - S["S12b"])), S["S12b"]); add(plip(-24, 500), T("c4", "up...") - 0.1); add(plip(-24, 600), T("c4", "up", 1) - 0.1)
add(spill_sizzle(-13, 1.6), T("c4", "over") - 0.1); add(boom(-17, 0.5), T("c4", "over") - 0.1); add(clang(-25, 900, 0.5), T("c4", "over") - 0.05)
for j, w in enumerate(("proteins,", "jacket,", "skin,", "lid.")): add(buzzer(-27, 0.18), T("c5", w) - 0.1); add(pop(-26, 500 + 60 * j), T("c5", w) - 0.08)
add(pop(-24, 1300), S["S13"] + 0.35)
# part 4 proof
add(boom(-19, 0.35), S["S14"] + 0.05); card_in(S["S14"] + 0.1, -26); add(simmer(-29, 8.0, 7), S["S14"]); pops_at(S["S14"] + 0.5, 10, 0.5, -29)
add(squirt(-26, 0.25), T("d1", "drop") - 0.1); add(plip(-18, 1400), T("d1", "drop") + 0.3); add(ding(-26, 2637), T("d1", "drop") + 0.32)
add(knob(-24), T("d1", "boil") - 0.1); add(simmer(-26, 3.0, 11), T("d1", "boil"))
add(foam_rise(-20, max(0.8, T("d2", "over.") - 0.2 - S["S15"])), S["S15"]); add(spill_sizzle(-15, 1.4), T("d2", "over.") - 0.15); add(boom(-18, 0.45), T("d2", "over.") - 0.15)
add(rec_scratch(-25), T("d2", "over.") - 0.4); add(chaching(-24), T("d2", "different") - 0.1); sparkle_sfx(T("d2", "different") - 0.05, -24)
# part 5 fixes
add(boom(-19, 0.35), S["S16"] + 0.1); card_in(S["S16"] + 0.15, -26); add(rustle(-26, 0.4), S["S16"] + 0.3)
for j, w in enumerate(("America's", "tried", "classics.")): add(pop(-24, 900 + 120 * j), T("e1", w) - 0.1); add(clack(-28, 1600), T("e1", w) - 0.08)
add(clack(-24, 1700), S["S17"] + 0.1); add(simmer(-30, 5.0, 7), S["S17"])
for j in range(6): add(tick(-29), S["S17"] + 0.3 + 0.3 * j)
add(buzzer(-26, 0.35), S["S17"] + 1.9)
add(squelch(-26, 0.5), S["S17b"] + 0.1); add(simmer(-30, 5.0, 7), S["S17b"])
for j in range(6): add(tick(-29), S["S17b"] + 0.3 + 0.3 * j)
add(buzzer(-26, 0.35), S["S17b"] + 1.9)
add(foam_rise(-22, 0.9), T("e2", "still") - 0.6); add(spill_sizzle(-15, 1.4), T("e2", "still") - 0.1); add(boom(-18, 0.4), T("e2", "still") - 0.1); add(boing(-24, 200, 0.5), T("e2", "still") + 0.1)
add(whoosh(0.5, peak=0.6, f_lo=400, f_hi=4000, level=-24), T("e3", "wide") - 0.4); add(rustle(-24, 0.5), T("e3", "wide") - 0.35)
add(chaching(-21), T("e3", "wide") - 0.12); sparkle_sfx(T("e3", "wide") - 0.05, -22); add(clang(-24, 1100, 0.5), T("e3", "wide") - 0.1)
stamp(T("e3", "four") - 0.1, -18); add(pop(-24, 800), T("e3", "half") - 0.1)
add(simmer(-28, 6.0, 8), S["S19"]); pops_at(T("e4", "pop,") - 0.1, 5, 0.12, -21); add(ding(-25, 1568), T("e4", "pop,") + 0.4)
add(knob(-22), T("e5", "moderate") - 0.1); add(hiss(-28, 0.8), T("e5", "moderate") + 0.1); add(ding(-25, 1318.5), T("e5", "moderate") + 0.2)
add(clack(-26, 1700), T("e5", "stir") - 0.1); add(wash(-23, 1.4), T("e5", "stir") + 0.1); add(wash(-25, 1.2), T("e5", "stir") + 1.3); add(squelch(-27, 0.5), T("e5", "skin") - 0.05)
for j in range(3): add(whoosh(0.3, peak=0.5, f_lo=500, f_hi=3000, level=-29), T("e5", "skin") + 0.2 + 0.15 * j)
add(simmer(-29, 5.0, 8), S["S21"]); add(click(-26), S["S21"] + 0.3); add(click(-28), S["S21"] + 0.6)
add(foam_rise(-22, 1.0), T("e6", "exact") - 0.2); add(spill_sizzle(-17, 1.2), T("e6", "exact") + 0.7); add(rec_scratch(-25), T("e6", "phone.") - 0.15)
add(simmer(-29, 5.0, 8), S["S22"]); add(foam_rise(-24, 1.4), S["S22"] + 0.2); add(spill_sizzle(-20, 1.0), S["S22"] + 1.6); stamp(T("f1", "starch.") - 0.15, -19)
for j, w in enumerate(("proteins", "skin", "foam")): add(pop(-21, 900 + 150 * j), T("g1", w) - 0.15)
for j, w in enumerate(("Wide", "lower", "stir.")): add(ding(-24, (1318.5, 1568, 1976)[j]), T("g1", w) - 0.1)
add(pop(-21, 900), S["S24"] + 0.05)
add(pop(-18, 1300), T("g2", "Send") + 0.3); add(ding(-22, 2093), T("g2", "Send") + 0.32)
vend = LINES["g2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2); add(pop_bubble(-24), vend + 0.5)
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
