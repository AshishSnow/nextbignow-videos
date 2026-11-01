"""Mix: narrator VO + ducked/carved midnight-tango score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP).
New foley (ep 20, also added to sfx_lib): cctv_hum (a security camera: mains hum + a tiny servo whir), micro_hum (a microwave running: 100 Hz
hum + turntable rattle) + micro_beep (the 3 end beeps), shell_crack (a spore's armour cracking: dry woody snap + crumbs), giggle (a germ
giggle: a fast pitched chirp run), pedal_bin (lid flip clang + the drop thud); reused: whoosh/pop/ding/thud/boom/boing/tick/crunch/
chaching/stamp/fridge_hum/suction/wind/hiss/simmer/knob/crt_off/rec_scratch/squelch/bubble_pop/chatter/sizzle/wash."""
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
TISNT = T("i1", "isn't") - 0.12
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


def cctv_hum(level=-32, dur=3.0):
    """security camera: 50 Hz mains hum with harmonics + a faint servo whir that rises and falls."""
    t2 = np.arange(int(dur * SR)) / SR
    y = sum(np.sin(2 * np.pi * 50 * k * t2) / k for k in (1, 2, 3, 5)) * 0.4
    y += signal.sosfilt(signal.butter(2, [1800, 4200], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * (0.15 + 0.15 * np.sin(2 * np.pi * 0.7 * t2))
    y *= np.minimum(1, np.minimum(t2 / 0.2, (dur - t2) / 0.3))
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def micro_hum(level=-28, dur=2.0):
    """microwave running: a 100 Hz transformer hum + a soft turntable rattle."""
    t2 = np.arange(int(dur * SR)) / SR
    y = (np.sin(2 * np.pi * 100 * t2) + 0.5 * np.sin(2 * np.pi * 200 * t2) + 0.25 * np.sign(np.sin(2 * np.pi * 100 * t2))) * 0.5
    y += signal.sosfilt(signal.butter(2, [400, 1600], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * 0.12 * (0.5 + 0.5 * np.sin(2 * np.pi * 3 * t2))
    y *= np.minimum(1, np.minimum(t2 / 0.05, (dur - t2) / 0.1))
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def micro_beep(t0, level=-24):
    for j in range(3): add(beep(level, 2000, 0.16), t0 + j * 0.28)


def shell_crack(level=-20):
    """a spore's armour cracking: a dry woody snap (band-passed click burst) + a few crumbs."""
    t2 = np.arange(int(0.4 * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [700, 3500], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.012)
    for k in range(4):
        i = int((0.05 + 0.06 * k + rng.uniform(0, 0.02)) * SR); seg = t2[: int(0.015 * SR)]
        y[i:i + len(seg)] += signal.sosfilt(signal.butter(2, [2000, 6000], "band", fs=SR, output="sos"), rng.standard_normal(len(seg))) * np.exp(-seg / 0.003) * 0.5
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def giggle(level=-27, dur=0.5):
    """a germ giggle: a fast run of pitched chirps going up and down."""
    t2 = np.arange(int(dur * SR)) / SR; y = np.zeros(len(t2))
    for k in range(7):
        i = int(k * dur / 7 * SR); seg = t2[: int(0.045 * SR)]; f0 = 1200 + 300 * math.sin(k * 1.3)
        y[i:i + len(seg)] += np.sin(2 * np.pi * np.cumsum(f0 * (1 + 0.4 * np.sin(2 * np.pi * 30 * seg))) / SR) * np.exp(-seg / 0.02)
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 80)


def pedal_bin(t, lv=-20):
    add(clang(lv - 2, 700, 0.4), t); add(thud(lv), t + 0.3); add(crunch(lv - 4), t + 0.33)


def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)


def sparkle_sfx(t, lv=-24): add(ding(lv, 2637), t); add(ding(lv - 3, 3520), t + 0.05); add(ding(lv - 6, 4186), t + 0.1)


for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-24), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-27), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-26), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-22, 700 + 60 * (i % 8)), st + 0.02); add(thud(-21), st + 0.02)
# HOOK: CCTV hum + clock ticks + a big yawn-thud of footsteps; crash zoom on ISN'T = whoosh-in + boom
add(cctv_hum(-30, max(1.0, S["S0b"])), 0.0)
for j in range(int(max(0.5, TISNT - 0.2) / 0.5)): add(tick(-29), 0.25 + 0.5 * j)
for j in range(3): add(thud(-28), 1.0 + 0.45 * j)
add(whoosh(0.25, peak=0.85, f_lo=600, f_hi=6000, level=-22), TISNT - 0.2); add(boom(-17, 0.45), TISNT); stamp(TISNT + 0.05, -18)
add(simmer(-31, 2.0, 7), S["S0b"] + 0.1); add(tick(-27), T("i2", "hours") - 0.1); add(tick(-27), T("i2", "hours") + 0.25); add(fridge_hum(-30, 1.2), T("i2", "fridge.") - 0.3); stamp(T("i2", "fridge.") - 0.12, -20)
add(fridge_hum(-30, 2.5), S["S1"]); clink(T("i3", "pebbles") - 0.25, -20, 3300); clink(T("i3", "pebbles") - 0.05, -22, 2900); add(boing(-24, 200, 0.5), T("i3", "pebbles") - 0.1)
add(whoosh(0.2, peak=0.9, f_lo=600, f_hi=6000, level=-24), T("i3", "pebbles") - 0.25)
# part 1
add(boom(-19, 0.35), S["S2"] + 0.05); card_in(S["S2"] + 0.1, -26); add(rustle(-26, 0.5), S["S2"] + 0.3); add(whoosh(0.5, peak=0.6, f_lo=400, f_hi=3000, level=-25), T("a1", "stowaway,") - 0.25); add(ding(-24, 1760), T("a1", "stowaway,") - 0.05)
add(giggle(-24, 0.5), S["S2b"] + 0.2); stamp(T("a1", "Bacillus") - 0.12, -19)
add(stretch(-26, 0.5, False), T("a2", "hides") - 0.1); add(lock_click(-22), T("a2", "hides") + 0.3); stamp(T("a2", "spore,") - 0.12, -20)
add(pop(-23, 900), T("a2", "seed") - 0.1); add(clang(-25, 1100, 0.3), T("a2", "armour.") - 0.12); add(pop(-23, 1300), T("a2", "armour.") + 0.2)
add(knob(-24), S["S4"] + 0.02); add(simmer(-26, 3.0, 10), S["S4"] + 0.1); add(clang(-22, 900, 0.4), T("a3", "crack") - 0.12); add(boing(-25, 320, 0.4), T("a3", "crack"))
add(hiss(-30, 1.2), S["S4b"] + 0.1); add(whoosh(0.5, peak=0.6, f_lo=300, f_hi=2500, level=-27), S["S4b"] + 0.1)
for j in range(3): add(boing(-30, 160 + 20 * j, 0.6), T("a3", "asleep.") - 0.15 + 0.4 * j)
add(chaching(-25), T("a4", "fine.") - 0.1)
# part 2: the warm hours
add(crt_off(-26, 0.5), S["S6"] + 0.02); card_in(S["S6"] + 0.1, -27); add(cctv_hum(-34, 3.0), S["S6"])
for j in range(int((S["S6b"] - S["S6"]) / 0.35)): add(tick(-28), S["S6"] + 0.2 + 0.35 * j)
add(boom(-21, 0.5), T("b1", "hours.") - 0.12)
for j in range(5): add(shell_crack(-21 - j), T("b1", "wakes") - 0.1 + 0.12 * j)
add(giggle(-24, 0.6), T("b1", "wakes") + 0.6)
add(shell_crack(-22), T("b2", "hatch,") - 0.1); add(nibble(-26, 0.5, 14), T("b2", "eat,") - 0.1); add(squelch(-24, 0.5), T("b2", "multiply.") - 0.05); add(bubble_pop(-22), T("b2", "multiply.") + 0.15)
add(tick(-26), T("b2", "twenty") - 0.1); add(tick(-26), T("b2", "twenty") + 0.25); add(squelch(-24, 0.5), T("b2", "double") - 0.05); add(pop(-22, 1100), T("b2", "double") + 0.3)
add(pop(-22, 900), S["S8"] + 0.1); add(pop(-22, 1000), T("b3", "four") - 0.1); add(pop(-22, 1150), T("b3", "eight,") - 0.1); add(giggle(-26, 0.4), T("b3", "eight,"))
add(giggle(-25, 1.0), S["S8b"] + 0.3); add(giggle(-24, 0.8), T("b3", "crowd.") - 0.2); stamp(T("b3", "crowd.") - 0.12, -18)
add(giggle(-23, 1.2), S["S9"] + 0.1); add(squelch(-20, 0.9), T("b4", "toxin.") - 0.15); add(boom(-17, 0.5), T("b4", "toxin.") - 0.12); stamp(T("b4", "poison.") - 0.15, -20)
add(knob(-24), S["S10"] + 0.02); add(sizzle(-26, 2.0), S["S10"] + 0.1); add(whoosh(0.2, peak=0.85, f_lo=600, f_hi=6000, level=-24), T("b5", "shrugs") - 0.2); stamp(T("b5", "shrugs") - 0.12, -19); add(boing(-24, 260, 0.4), T("b5", "shrugs"))
add(micro_hum(-27, max(0.5, T("b5", "steaming,") - S["S10b"])), S["S10b"] + 0.05); micro_beep(T("b5", "steaming,") - 0.1, -24); add(hiss(-27, 0.8), T("b5", "steaming,") + 0.2)
add(whoosh(0.3, peak=0.6, f_lo=300, f_hi=3000, level=-26), T("b5", "still") - 0.35); stamp(T("b5", "still") - 0.02, -17); add(giggle(-24, 0.5), T("b5", "still") + 0.2)
add(buzzer(-26, 0.3), T("b6", "blame,") - 0.1); add(tick(-27), T("b6", "earlier,") - 0.1); add(tick(-27), T("b6", "earlier,") + 0.3); add(boom(-21, 0.4), T("b6", "earlier,") - 0.12)
add(growl(-22, 1.0), T("b7", "throwing") - 0.2); add(squelch(-24, 0.6), T("b7", "throwing") + 0.2)
add(boom(-20, 0.35), S["S12b"] + 0.05); stamp(T("b7", "classic") - 0.12, -16)
# the guess
add(fridge_hum(-28, max(1.0, S["S14"] - S["S13"])), S["S13"]); add(crt_off(-27, 0.4), S["S13"] + 0.02)
for j in range(4): add(tick(-28), S["S13"] + 0.4 + 0.5 * j)
add(pop(-23, 1000), T("c1", "kill") - 0.1)
stamp(S["S13b"] + 0.05, -15); add(boom(-18, 0.4), S["S13b"] + 0.05); add(wind(-28, 1.4), T("c2", "slows") - 0.1); add(chatter(-29, 0.6, 14), T("c2", "slows") + 0.3); stamp(T("c2", "fast.") - 0.15, -20)
# part 3
add(suction(-24), S["S14"] + 0.05); card_in(S["S14"] + 0.1, -27); add(crunch(-14), T("d1", "hard") - 0.12); add(tooth_crack(-20), T("d1", "hard") - 0.05); add(boing(-24, 180, 0.5), T("d1", "hard") + 0.1)
add(bubble_pop(-24), T("d2", "water") - 0.1); add(stretch(-25, 0.6, True), T("d2", "swells.") - 0.12); add(ding(-25, 1568), T("d2", "fluffy.") - 0.1)
add(stretch(-25, 0.8, False), T("d3", "squeeze") - 0.1); add(ice_crack(-24, 0.5), T("d3", "crystals.") - 0.12)
stamp(T("d4", "retrogradation.") - 0.15, -17); add(pop(-24, 900), T("d4", "Fancy") - 0.1); add(ding(-25, 1318.5), T("d4", "setting") - 0.1)
add(hiss(-26, 1.0), S["S17"] + 0.1); add(rattle(-26, 0.5, 26), T("d5", "shakes") - 0.05); add(boing(-24, 300, 0.4), T("d5", "soft") - 0.1)
add(chaching(-24), T("d5", "cold") - 0.1)
# part 4
add(boom(-19, 0.35), S["S18"] + 0.05); card_in(S["S18"] + 0.1, -26); stamp(T("e1", "four") - 0.12, -19)
add(suction(-24), S["S19"] + 0.1); add(fridge_hum(-30, 2.0), S["S19"]); add(tick(-27), S["S19"] + 0.4); add(tick(-27), S["S19"] + 0.9); stamp(T("e2", "hour.") - 0.12, -20)
add(whoosh(0.5, peak=0.6, f_lo=300, f_hi=3000, level=-26), T("e2", "wide") - 0.2); add(wind(-30, 1.0), T("e2", "quicker.") - 0.2); add(ding(-24, 1760), T("e2", "quicker.") - 0.1)
for j, w in enumerate(("Two,", "Three,", "Four,")): add(pop(-21, 900 + 150 * j), T("e3", w) - 0.1); add(clack(-26, 1600), T("e3", w) - 0.08)
micro_beep(T("e3", "once.") - 0.1, -27); add(hiss(-27, 0.8), T("e3", "steaming") - 0.05)
add(rec_scratch(-26), S["S21"] + 0.05); add(buzzer(-27, 0.3), T("e4", "gamble") - 0.1); pedal_bin(T("e4", "Bin") - 0.1, -18); add(boom(-20, 0.4), T("e4", "Bin") - 0.1)
add(nibble(-26, 0.8, 12), S["S22"] + 0.2); sparkle_sfx(T("f1", "fine,") - 0.1, -23); add(pop(-24, 1000), T("f1", "fast") - 0.1); add(pop(-24, 1150), T("f1", "day") - 0.1)
for j, w in enumerate(("cool", "eat", "once,", "hot.")): add(pop(-21, 900 + 150 * j), T("g1", w) - 0.1); add(ding(-25, (1318.5, 1568, 1760, 2093)[j]), T("g1", w) - 0.08)
add(pop(-21, 900), S["S24"] + 0.05)
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
