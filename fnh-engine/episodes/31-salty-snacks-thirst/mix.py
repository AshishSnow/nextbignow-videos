"""Mix ep 31: VO + LAYERED foley + ROOM TONE per place -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0).
CRAFT SKILL (ep 31): SOUND DESIGN WITHOUT A MUSIC BED (Morphic 'How to layer sound effects' + 'Sound design basics'; Violet Recording 'Sound design for animation' 2026;
Krotos 'When silence is best' 2026; Sound On Sound 'Sound design for visual media' 2013):
 - every BIG hit = 4 layers whose transients land on the same frame: SUB (40-90 Hz falling sine, the weight), BODY (the loudest layer, 150-1500 Hz), TRANSIENT click
   (2-8 kHz, lower, tells the ear WHEN), TAIL (filtered noise decay 0.6-1.6 s, sets distance). The body/transient are high-passed so only the sub owns the lows.
 - ROOM TONE per place (TV-room hiss + fridge hum, capsule air-handling, kitchen, sea, the board's quiet paper room) keeps the space continuous across cuts,
   very low and ducked under the voice ('if the ambience is too loud, dialogue gets buried'; 'dialogue almost always wins').
 - DROP-OUT: ~0.25 s before the 5 biggest moments, the room tone + foley dip ~15 dB, so the hit lands out of silence ('leave a beat of silence before the impact').
 - Save the big sounds for the big moments: only 5 full layered hits; the rest are single small foley. Sync to the frame of the action."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(31)
db = lambda x: 10 ** (x / 20)
S = {k: st for k, st, _ in SHOTLIST}
ORDER = [k for k, _, _ in SHOTLIST]
SEND = lambda sid: (SHOTLIST[ORDER.index(sid) + 1][1] if ORDER.index(sid) + 1 < len(SHOTLIST) else END)
v, _ = sf.read(f"{B}/work/vo.wav", dtype="float32")
vo = np.zeros(NS, np.float32); vo[: min(NS, len(v))] = v[:NS]
VO = np.stack([vo, vo], 1)
win = int(0.03 * SR); env = np.sqrt(np.convolve(vo ** 2, np.ones(win) / win, "same"))
env = np.clip(env / (np.percentile(env[env > 1e-4], 95) + 1e-9) * 1.6, 0, 1)
g = np.zeros_like(env); prev = 0.0; aa, ar = np.exp(-1 / (0.03 * SR)), np.exp(-1 / (0.4 * SR))
for i in range(0, NS, 48):
    x = env[i]; a_ = aa if x > prev else ar; prev = a_ * prev + (1 - a_) * x; g[i:i + 48] = prev
exec(open(f"{_D}/sfx_lib.py").read())


def _st2(y): return np.stack([y, y * 0.96], 1).astype(np.float32)


def _bp(x, lo, hi): return signal.sosfilt(signal.butter(2, [lo, hi], "band", fs=SR, output="sos"), x)


def _hp(x, f0): return signal.sosfilt(signal.butter(2, f0, "high", fs=SR, output="sos"), x)


def _lp(x, f0): return signal.sosfilt(signal.butter(2, f0, "low", fs=SR, output="sos"), x)


# ---------------- the layered hit (ep 31 skill) ----------------
def layered_hit(t, level=-14, sub_f=(90, 42), body=(180, 1400), tail=1.0, bright=1.0):
    """4 layers, transients on the same sample: SUB (falling sine) + BODY (band thump, loudest) + TRANSIENT (click, -8 dB) + TAIL (filtered decay, -14 dB)."""
    n_ = int((tail + 0.4) * SR); tt = np.arange(n_) / SR
    fr = sub_f[1] + (sub_f[0] - sub_f[1]) * np.exp(-tt / 0.08)
    sub = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / 0.32) * np.minimum(1, tt / 0.002)
    bd = _hp(_bp(rng.standard_normal(n_), *body), 150) * np.exp(-tt / 0.07) * np.minimum(1, tt / 0.001)
    bd = bd / (np.abs(bd).max() + 1e-9)
    tr = _hp(rng.standard_normal(n_), 2500) * np.exp(-tt / 0.006); tr = tr / (np.abs(tr).max() + 1e-9)
    tl = _lp(_hp(rng.standard_normal(n_), 300), 3500 * bright) * np.exp(-tt / (tail * 0.35)) * np.minimum(1, tt / 0.02); tl = tl / (np.abs(tl).max() + 1e-9)
    y = 0.8 * sub + 1.0 * bd + db(-8) * tr + db(-14) * tl
    y = y / (np.abs(y).max() + 1e-9) * db(level)
    st = np.stack([y, np.roll(y, 90) * 0.95], 1).astype(np.float32)               # a hair of width on the tail
    add(st, t)


def bell(level=-22, f0=1760, dur=1.0, rate=18):
    """an alarm bell ringing (struck partials + a fast hammer tremolo)."""
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    x = sum(a * np.sin(2 * np.pi * f0 * m * tt) for m, a in ((1, 1), (2.76, 0.5), (5.4, 0.25)))
    x *= (0.55 + 0.45 * np.abs(np.sin(np.pi * rate * tt))) * np.minimum(1, tt / 0.005) * np.clip((dur - tt) / 0.15, 0, 1)
    return _st2(x / (np.abs(x).max() + 1e-9) * db(level))


def shaker_rattle(level=-26, dur=0.8, rate=9):
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    x = _bp(rng.standard_normal(n_), 3000, 9000) * np.abs(np.sin(np.pi * rate * tt)) ** 4
    return _st2(x / (np.abs(x).max() + 1e-9) * db(level) * np.clip((dur - tt) / 0.1, 0, 1))


def tumble(level=-28, dur=1.0):
    """a dry tumbleweed: scratchy brush noise bumping along + a whistle of wind."""
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    x = _bp(rng.standard_normal(n_), 1500, 6000) * (0.3 + 0.7 * np.abs(np.sin(2 * np.pi * 4.5 * tt)) ** 3)
    w = np.sin(2 * np.pi * (700 + 200 * np.sin(2 * np.pi * 0.7 * tt)) * tt) * 0.15
    y = (x / (np.abs(x).max() + 1e-9) + w) * np.sin(np.pi * tt / dur)
    return _st2(y / (np.abs(y).max() + 1e-9) * db(level))


def drain(level=-24, dur=1.2):
    """a battery draining: a falling square-ish tone that slows down."""
    n_ = int(dur * SR); tt = np.arange(n_) / SR; fr = 600 * np.exp(-tt * 1.4) + 90
    y = np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * 0.4 * np.exp(-tt / dur)
    return _st2(_lp(y, 2500) / 0.4 * db(level))


def magnet_zing(level=-26, dur=0.6):
    n_ = int(dur * SR); tt = np.arange(n_) / SR; fr = 300 + 900 * tt / dur
    y = np.sin(2 * np.pi * np.cumsum(fr) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 30 * tt)) * np.sin(np.pi * tt / dur)
    return _st2(y * db(level))


def deflate(level=-24, dur=0.7):
    """shrinking cells: a little falling 'wheee' + air."""
    n_ = int(dur * SR); tt = np.arange(n_) / SR; fr = 900 * np.exp(-tt * 2.5) + 180
    y = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / dur) + 0.3 * _bp(rng.standard_normal(n_), 800, 3000) * np.exp(-tt / 0.2)
    return _st2(y / (np.abs(y).max() + 1e-9) * db(level))


def waves(level=-30, dur=3.0):
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    x = _lp(rng.standard_normal(n_), 1400) * (0.35 + 0.65 * np.sin(np.pi * ((tt / 2.2) % 1)) ** 2)
    return _st2(x / (np.abs(x).max() + 1e-9) * db(level) * np.minimum(1, np.minimum(tt / 0.4, (dur - tt) / 0.4)))


def hatch_hiss(level=-26, dur=0.9):
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    x = _hp(rng.standard_normal(n_), 2000) * np.exp(-tt / 0.35) + 0.5 * np.sin(2 * np.pi * 70 * tt) * np.exp(-tt / 0.08)
    return _st2(x / (np.abs(x).max() + 1e-9) * db(level))


# ---------------- ROOM TONE per place (continuous, very low, ducked under the voice) ----------------
PLACE = {"S0": "tv", "S0b": "tv", "S2": "tv", "S6": "tv", "S6b": "tv", "S11": "tv", "S23": "tv", "S26": "tv",
         "S1": "cap", "S1b": "cap", "S17": "cap", "S18": "cap", "S18b": "cap", "S19": "cap", "S22": "cap", "S22b": "cap",
         "S12": "kit", "S25": "kit", "S15": "sea"}


def tone(kind, n_):
    tt = np.arange(n_) / SR; w = rng.standard_normal(n_)
    if kind == "tv":   x = _lp(w, 2500) * 0.5 + 0.25 * np.sin(2 * np.pi * 60 * tt) + _bp(rng.standard_normal(n_), 4000, 9000) * 0.08 * (rng.random(n_) < 0.02)
    elif kind == "cap": x = _lp(w, 700) * 0.8 + 0.35 * np.sin(2 * np.pi * 120 * tt) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.3 * tt))
    elif kind == "kit": x = _lp(w, 1800) * 0.4 + 0.2 * np.sin(2 * np.pi * 100 * tt)
    elif kind == "sea": x = _lp(w, 1200) * (0.4 + 0.6 * np.sin(np.pi * ((tt / 2.2) % 1)) ** 2)
    else:              x = _bp(w, 200, 2500) * 0.3                                    # the board: a quiet paper room
    return x / (np.abs(x).max() + 1e-9)


LVL = {"tv": -44, "cap": -42, "kit": -46, "sea": -38, "board": -52}
amb = np.zeros(NS, np.float32)
for i, (sid, st, _) in enumerate(SHOTLIST):
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE.get(sid, "board")
    seg = tone(kind, b - a) * db(LVL[kind]); fd = min(int(0.02 * SR), (b - a) // 2)   # 20 ms crossfades at the cut points
    seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd); amb[a:b] += seg
amb *= (1 - 0.5 * g)                                                                   # dialogue wins: -6 dB under the voice
AMB = np.stack([amb, np.roll(amb, 240)], 1)

# ---------------- spotting list: one sound per action ----------------
for i, s in enumerate(SHOTLIST[1:], 1):
    k = s[2]; st = s[1]
    if k == "whip": add(whoosh(0.4, level=-25), st - 0.22)
    elif k == "erase": add(eraser(-27), st - 0.02)
    elif k == "morph": add(whoosh(0.45, peak=0.6, f_lo=250, f_hi=2400, level=-27), st - 0.2)
    elif k in ("punch", "flash"): add(pop(-24, 700 + 60 * i), st + 0.02)
for sid in ORDER:                                                                       # a marker scratch on every board shot
    if PLACE.get(sid, "board") == "board": add(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15)
# S0: crunches every 0.42 s while he munches, the question words
for j in range(int(S["S0b"] / 0.42) + 1): add(crunch(-20), j * 0.42 + 0.02)
add(crinkle(-28, 0.5), 0.05); add(scratch(-30, 0.3), 1.4)
# S0b tumbleweed
add(tumble(-26, 1.0), S["S0b"] + 0.05)
# S1 capsule hatch + shaker, S1b LESS (BIG 1: layered, out of a drop-out)
add(hatch_hiss(-26), S["S1"] + 0.1); add(shaker_rattle(-24, 0.9), T("i2", "salt") - 0.2)
BIG = [T("i2", "less") - 0.15, T("b3", "alarm") - 0.25, T("c3", "back") - 0.4, T("d3", "less") - 0.3, T("d5", "hungry") - 0.3]
layered_hit(BIG[0], -15, (80, 40), (150, 900), 1.2)
# S2 the take
add(boing(-22, 300, 0.45), T("i3", "Less") - 0.02); add(rec_scratch(-26), T("i3", "backwards") - 0.25)
# S3 chip lands, salt crystals pop on; S3b they hop off the tongue
add(thud(-20), S["S3"] + 0.05)
for j in range(3): add(pop(-26, 1300 + 200 * j), S["S3"] + 0.4 + 0.12 * j)
for j in range(3): add(boing(-28, 500 + 80 * j, 0.3), T("a0", "tongue") - 0.3 + 0.12 * j)
# S4 salt through the wall (squelch), S4b SALTIER
add(squelch(-26, 0.6), T("a1", "wall") + 0.2); add(plip(-26, 700), T("a1", "blood") - 0.2)
for j in range(6): add(pop(-30, 1000 + 120 * j), S["S4b"] + 0.15 + 0.15 * j)
add(ding(-24, 1568), T("a1", "saltier") - 0.15)
# S5 magnet zing + drops sliding; S5b deflating cells
add(magnet_zing(-24), T("a2", "magnet") - 0.3)
for j in range(4): add(plip(-28, 900 + 80 * j), T("a2", "magnet") + 0.05 + 0.15 * j)
add(deflate(-22), T("a2", "shrink") - 0.3)
# S6 the '?' ; S6b tongue X + BRAIN
add(pop(-24, 600), T("a3", "notices") - 0.2); add(buzzer(-26, 0.3), S["S6b"] + 0.15); add(ding(-22, 2093), T("a3", "brain") - 0.25)
# S7 inset zoom; S7b X / tick
add(whoosh(0.35, peak=0.7, f_lo=400, f_hi=4000, level=-28), T("b1", "tiny"))
add(buzzer(-27, 0.25), T("b1", "water") + 0.1); add(ding(-23, 1760), T("b1", "salt") + 0.05)
# S8 the checker pops up
add(boing(-24, 380, 0.4), T("b2", "checker") - 0.35)
# S9 the dial ticks up, THE ALARM (BIG 2)
for j in range(7): add(tick(-28), T("b3", "shifts") - 0.1 + (BIG[1] - T("b3", "shifts")) * j / 7)
layered_hit(BIG[1], -15, (95, 45), (300, 2200), 0.9, 1.3); add(bell(-21, 1760, 1.3), BIG[1] + 0.02)
# S10 courier flies (whoosh), kidney; S10b water circling
add(whoosh(1.2, peak=0.5, f_lo=500, f_hi=3000, level=-27), T("b4", "vasopressin") - 0.3); add(bell(-30, 1760, 0.5), S["S10"] + 0.1)
add(squeeze(-26), T("b4", "keep") - 0.1)
# S11 parched: a dry rasp + reach
add(scratch(-28, 0.4), T("b5", "dry") - 0.1); add(crinkle(-30, 0.4), T("b5", "thirst") - 0.2)
# S12 the glass: gulps + relief
add(drink(-20, 4, 0.22), T("c0", "drink") - 0.1); add(shimmer(-28, 1.0), T("c0", "better") - 0.2)
# S13 clock ticks; S13b question pop
for j in range(int((SEND("S13") - S["S13"]) / 0.5)): add(tick(-30), S["S13"] + 0.2 + 0.5 * j)
add(pop(-23, 500), S["S13b"] + 0.2)
# S14 gulps going down + SHORTCUT sneak; S14b bell stops, OFF
add(glug(-26, 3, 0.25), T("c2", "mouth") - 0.1); add(whoosh(0.5, peak=0.6, f_lo=800, f_hi=4000, level=-27), T("c2", "gut"))
add(bell(-28, 1760, max(0.3, T("c2", "off") - S["S14b"] - 0.3)), S["S14b"] + 0.05); add(lock_click(-20), T("c2", "off") - 0.3)
# S15 the sea + sip + ahh; S15b the alarm comes BACK (BIG 3)
add(waves(-30, SEND("S15") - S["S15"] + 0.3), S["S15"]); add(sip(-24), S["S15"] + 0.45)
layered_hit(BIG[2], -16, (85, 45), (300, 2000), 0.8, 1.2); add(bell(-22, 1760, 1.0), BIG[2] + 0.02)
# S16 mouse nibbles + early bell; S16b sneaky approach
add(nibble(-26, 1.0, 14), S["S16"] + 0.2); add(bell(-27, 1760, 0.6), T("c4", "eating") - 0.3)
add(whoosh(0.8, peak=0.7, f_lo=300, f_hi=1500, level=-29), S["S16b"] + 0.1)
# S17 PART 2 title + capsule beeps; S18 crew; S18b counter ticks; S19 tray clinks
add(thud(-18), S["S17"] + 0.05); add(beep(-28, 2400, 0.08), S["S17"] + 0.5); add(beep(-28, 2900, 0.08), S["S17"] + 0.62)
add(hatch_hiss(-27), S["S18"] + 0.2)
for j in range(16): add(tick(-30), S["S18b"] + 0.2 + 0.1 * j)
add(ding(-24, 1318.5), S["S18b"] + 1.85)
clink(S["S19"] + 0.1, -26); add(pen_draw(-28, 1.6, seed=19), S["S19"] + 0.4)
# S20 bars: up (rising), then LESS (BIG 4)
add(stretch(-26, 0.5, True), T("d3", "up") - 0.2)
layered_hit(BIG[3], -14, (70, 38), (150, 800), 1.4, 0.8)
# S21 kidney hugs water; S21b urea tugs a rope
add(squeeze(-26), S["S21"] + 0.1); add(creak(-24, 0.6), T("d4", "pulls") - 0.3); add(stretch(-27, 0.6, False), T("d4", "pulls") + 0.2)
# S22 battery drains; S22b tummies growl (BIG 5: a soft one)
add(drain(-28, 1.3), S["S22"] + 0.2)
layered_hit(BIG[4], -21, (60, 35), (100, 500), 0.8, 0.6); add(growl(-25, 1.0), BIG[4] + 0.05)
# S23 a shrug pop; S23b question pops
add(pop(-24, 800), T("e0", "short") - 0.25)
for j in range(3): add(pop(-27, 600 + 150 * j), T("e0", "scientists") - 0.3 + 0.15 * j)
# S24 recap: a ding per link
for j, w in enumerate(("Salt", "water", "checker", "drink", "switch")): add(ding(-25, (1046.5, 1174.7, 1318.5, 1568, 2093)[j]), T("e1", w) - 0.2)
# S25 water tick + chips stop
add(ding(-23, 1568), T("e2", "water") - 0.1); add(buzzer(-26, 0.3), T("e2", "Another") + 0.1)
# S26 the friend glugs, phone ping, then the audio logo
add(glug(-24, 4, 0.2), T("e3", "bottle") - 0.3); add(ding(-24, 2093), T("e3", "Send") + 0.3)
vend = LINES["e3"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-24), vend - 0.2); audio_logo(vend + 0.25, -17)

# ---------------- DROP-OUTS before the big hits (room tone + foley dip ~15 dB for 0.25 s, then back on the hit) ----------------
dip = np.ones(NS, np.float32)
for tb in BIG:
    a, b = int((tb - 0.27) * SR), int((tb - 0.01) * SR); r = int(0.04 * SR)
    dip[a:b] = db(-15); dip[a - r:a] = np.linspace(1, db(-15), r); dip[b:b + r] = np.linspace(db(-15), 1, r)
sfx *= db(-2.0) * dip[:, None]; AMB *= dip[:, None]
BED = float(os.environ.get('BED', '0'))          # owner 9 Nov: no music bed; there is no score in this episode at all
bed = bed_carve.carve(sfx + AMB, vo)
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
