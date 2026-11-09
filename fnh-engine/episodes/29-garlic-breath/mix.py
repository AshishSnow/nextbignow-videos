"""Mix: narrator VO + ducked/carved tarantella score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP). New foley (ep 29): stink_puff (a soft breathy 'pfff' + low rumble),
crush (a knife-flat smash), floss (a thin squeak run), tiptoe (soft pizz-like taps), exhale."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(29)
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
M[: int(LINES["i1"]["end"] * SR)] *= db(-3)
exec(open(f"{_D}/sfx_lib.py").read())
SHOT_END = lambda sid: next((SHOTLIST[i + 1][1] for i, s in enumerate(SHOTLIST) if s[0] == sid and i + 1 < len(SHOTLIST)), END)


def _st2(y): return np.stack([y, y], 1).astype(np.float32)


def stink_puff(level=-24, dur=0.6):
    """a soft breathy 'pfff' (band-passed noise, fast attack, slow tail) + a low wobbly rumble = a cartoon stink cloud."""
    n_ = int(dur * SR); x = rng.standard_normal(n_)
    x = signal.sosfilt(signal.butter(2, [500, 2600], "band", fs=SR, output="sos"), x)
    tt = np.arange(n_) / SR; e = np.minimum(1, tt / 0.03) * np.exp(-tt / (dur * 0.35))
    rum = np.sin(2 * np.pi * (70 + 15 * np.sin(2 * np.pi * 6 * tt)) * tt) * np.exp(-tt / (dur * 0.4)) * 0.6
    y = (x / (np.abs(x).max() + 1e-9) * e + rum * e); y = y / (np.abs(y).max() + 1e-9) * db(level)
    return _st2(y)


def crush(level=-14):
    """the flat of a knife smashing a clove: a dull thump + a short crunchy crackle."""
    n_ = int(0.35 * SR); tt = np.arange(n_) / SR
    th = np.sin(2 * np.pi * (110 * np.exp(-tt * 12)) * tt) * np.exp(-tt / 0.06)
    cr = signal.sosfilt(signal.butter(2, 3000, "high", fs=SR, output="sos"), rng.standard_normal(n_)) * np.exp(-tt / 0.05) * (rng.random(n_) > 0.7)
    y = th + 0.4 * cr; y = y / (np.abs(y).max() + 1e-9) * db(level)
    return _st2(y)


def floss(level=-30, dur=0.8):
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    y = np.sin(2 * np.pi * (2400 + 600 * np.sin(2 * np.pi * 9 * tt)) * tt) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * tt)) * np.exp(-tt / dur)
    return _st2(y / (np.abs(y).max() + 1e-9) * db(level))


def exhale(level=-28, dur=0.9):
    n_ = int(dur * SR); x = signal.sosfilt(signal.butter(2, [300, 1800], "band", fs=SR, output="sos"), rng.standard_normal(n_))
    tt = np.arange(n_) / SR; e = np.sin(np.pi * tt / dur) ** 1.5
    return _st2(x / (np.abs(x).max() + 1e-9) * e * db(level))


BOARD = {"S0b", "S4", "S4b", "S5", "S5b", "S7", "S7b", "S9", "S9b", "S10", "S10b", "S11", "S13", "S15", "S15b", "S18", "S18b", "S19", "S20", "S21", "S21b", "S22b", "S23", "S23b", "S24"}
for i, s in enumerate(SHOTLIST[1:], 1):
    k = s[2]; st = s[1]
    if k == "erase": add(eraser(-27), st)
    elif k == "morph": add(whoosh(0.45, peak=0.5, f_lo=500, f_hi=2600, level=-27), st - 0.05); add(shimmer(-30, 0.5), st + 0.05)
    elif k == "whip": add(whoosh(0.4, level=-25), st - 0.22)
    elif k in ("punch", "flash"): add(pop(-25, 700 + 60 * i), st + 0.02)
    if s[0] in BOARD: add(pen_draw(-31, 0.9, i), st + 0.15)
# hook: office murmur + the garlic clouds already rolling
for j in range(3): add(stink_puff(-22, 0.7), max(0.0, -0.6 + j * 0.8 + 0.6))
add(boing(-26, 180, 0.35), 0.35)
for j in range(3): add(stink_puff(-26, 0.6), S["S0b"] + 0.3 + j * 0.45)
# brushing x2 + the colleague backing off
add(scrub(-24, max(0.5, S["S1b"] - S["S1"] - 0.1), 7.0), S["S1"] + 0.05)
for j in range(3): add(footstep(-26, 0.8), S["S1b"] + 0.2 + j * 0.45)
add(stink_puff(-24, 0.7), S["S1b"] + 0.2)
# the bulb lands, a clove pops; the sniff; cut + CRUSH
add(thud(-20), S["S2"] + 0.4); add(pop(-24, 900), T("a0", "clove") - 0.1)
add(sniff(-22, 0.45), S["S2b"] + 0.1)
add(snip(-20), T("a1", "cut") - 0.1); add(crush(-13), T("a1", "crush") - 0.15)
for j in range(4): add(stink_puff(-23, 0.7), T("a1", "crush") - 0.1 + j * 0.12)
# the cell breaks, they meet, allicin pops, falls apart into gases
add(shell_crack(-20), T("a2", "breaks") - 0.1); add(ding(-24, 1568), T("a2", "meet") - 0.1)
add(clack(-26), S["S5"] + 0.1); add(pop(-20, 1100), T("a3", "allicin") - 0.1)
add(tooth_crack(-18), T("a3", "apart") - 0.15)
for j in range(5): add(stink_puff(-26, 0.5), T("a3", "apart") - 0.1 + j * 0.06)
# two places
add(boom(-20, 0.35), T("b0", "two") - 0.1)
# mouth: wisps; brushing + flossing, the puffs pop
for j in range(2): add(stink_puff(-30, 0.5), S["S7b"] + 0.3 + j * 0.7)
add(scrub(-24, max(0.4, T("b2", "flossing") - S["S8"] - 0.2), 6.0), S["S8"] + 0.05); add(floss(-28, 0.9), T("b2", "flossing") - 0.05)
for tp in (S["S8"] + 0.3, S["S8"] + 0.9, T("b2", "flossing") + 0.2): add(bubble_pop(-20), tp)
add(press(-18), T("b2", "really") - 0.1)
# AMS sneaks: the bassoon carries it; gulps from the gut + liver; the slip into blood
for j in range(3): add(gulp(-24), S["S10"] + 0.5 + j * 0.35)
add(boing(-26, 260, 0.35), T("b4", "cant") - 0.2); add(soft_flop(-24), T("b4", "cant") + 1.1)
add(drip_big(-18), T("b4", "slips") + 0.2)
add(ding(-22, 1760), T("b5", "lungs") - 0.2)
for j in range(3): add(exhale(-26, 0.8), S["S11b"] + j * 0.8)
# sweat: footsteps + a drop
for j in range(int((S["S13"] - S["S12"]) / 0.54)): add(footstep(-27, 0.8), S["S12"] + 0.05 + j * 0.54)
add(drip_big(-22), T("b6", "sweat") - 0.2); add(soft_flop(-24), T("b6", "sweat") + 0.75)
add(shimmer(-26, 0.6), T("b7", "clean") - 0.2); add(boing(-24, 300, 0.3), T("b7", "talking") - 0.15)
# the clock + 24 hours + the meeting
for j in range(int((S["S15"] - S["S14"]) / 0.25)): add(tick(-26), S["S14"] + j * 0.25)
add(ding(-21, 2093), T("c1", "twentyfour") - 0.2); add(whoosh(0.5, level=-27), S["S15b"] + 0.2)
add(stink_puff(-24, 1.0), S["S16"] + 0.15); add(squelch(-26, 0.4), T("c2", "dinner") - 0.25)
# fight + lab
add(boom(-17, 0.4), T("d0", "fight") - 0.2)
add(munch_sfx(-26, 0.8), T("d1", "chewed") - 0.1)
for j in range(5): add(pop(-28, 900 + 120 * j), T("d1", "foods") - 0.3 + j * 0.12)
add(machine_whir(-26, 1.2, 150), T("d1", "machine") - 0.2)
add(ding(-22, 1318.5), T("d2", "half") - 0.3); add(chaching(-26), T("d3", "better") - 0.1)
add(soft_flop(-22), T("d3", "all") + 0.25)
add(crunch(-22), T("d4", "won") - 0.2); add(gulp(-24), T("d4", "down") - 0.2); add(bubble_pop(-20), T("d4", "down"))
# milk + recap
add(pour(-26, 0.8), T("d5", "milk") - 0.2); add(thud(-18), T("d5", "with") - 0.2)
add(scratch(-26, 0.2), T("d5", "after") + 0.1)
for w_ in ("apple", "lettuce", "mint"): add(pop(-24, 1200), T("e0", w_) - 0.2)
for j in range(3): add(exhale(-30, 0.8), S["S24"] + j * 0.9)
add(ding(-22, 1568), T("f1", "worth") - 0.2); add(giggle(-28, 0.5), T("f1", "interview") + 0.2)
# send + logo
add(stink_puff(-22, 1.0), S["S26"] + 0.3)
add(pop(-18, 1300), T("f2", "Send") + 0.25); add(ding(-22, 2093), T("f2", "Send") + 0.27)
vend = LINES["f2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2); audio_logo(vend + 0.25, -15)

sfx *= db(-5.0)
bed = bed_carve.carve(M * db(-11.5) + sfx, vo)
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
