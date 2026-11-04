# ================= HOW IT WORKS EP 1: Why 999 plays can pay zero. Drawn with NextBigNow's own kit (nbnkit = whatif-v3 toon rig) =================
L0 = lambda i: LINES[i]["start"]; L1 = lambda i: LINES[i]["end"]
SHOTLIST = [("S_hook", 0.0, "cut"), ("S_singer", L0("i2") - 0.12, "whip"), ("S_four", L0("i4") - 0.12, "focus"),
            ("S_pot", L0("a1") - 0.12, "whip"), ("S_pour", L0("a2") - 0.08, "cut"), ("S_many", L0("a3") - 0.1, "zoom"),
            ("S_slice", L0("b1") - 0.12, "whip"), ("S_dots", L0("b2") - 0.08, "focus"), ("S_100", L0("b3") - 0.1, "whip"), ("S_200", L0("b5") - 0.1, "whip"),
            ("S_line", L0("c1") - 0.12, "whip"), ("S_out", L0("c4") - 0.06, "punch"), ("S_penny", L0("c5") - 0.1, "focus"), ("S_share", L0("c6") - 0.08, "cut"),
            ("S_booth", L0("d1") - 0.12, "whip"), ("S_deal", L0("d3") - 0.08, "cut"),
            ("S_sofa", L0("e1") - 0.12, "whip"), ("S_flow", L0("e2") - 0.08, "cut"), ("S_study", L0("e4") - 0.1, "focus"), ("S_swing", L0("e5") - 0.1, "whip"),
            ("S_take", L0("t1") - 0.12, "whip"), ("S_end", L0("z1") - 0.12, "focus")]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}


def lt(t, sid): return t - SHOT[sid]["start"]


import sys as _sys, os as _os
_sys.path.insert(0, _D if "_D" in globals() else f"{B}/scripts")
from nbnkit import *        # noqa  (NextBigNow rig + OMB helpers; R becomes skia.Rect from here on)
from nbnkit import _rot_stick
import skia


def say(c, t, t0, small, big, col=WHITE, t1=None, size=250, y=650, t_big=None, smallc=(240, 232, 255)):
    two_tier(c, t, t0, small, big, y=y, big_size=size, big_col=col, small_col=smallc, shadow=True, t1=t1, t_big=t_big, maxw=800)


def fnote(c, t, t0, text, t1=None, y=1466):
    if t < t0 or (t1 is not None and t > t1): return
    a = min(pr(t, t0, 0.25), 1.0 if t1 is None else 1 - pr(t, t1 - 0.2, 0.2)); src_chip(c, text, a, y=y)


def pop_(t, t0, d=0.32, s=1.7): return eback(pr(t, t0, d), s)


# ---- places ----
WALL_TOP, WALL_BOT = (40, 26, 72), (92, 54, 120)    # the venue at night: same world as the hook (NBN stays in one place)


def trusses(c, t):
    # a truss with hanging stage lamps frames the top (like NBN's stalactites): dark silhouettes + soft cones
    dk = (16, 10, 30)
    c.drawRect(R.MakeLTRB(0, 0, W, 66), paint(dk))
    for i in range(0, 12):
        x = i * 100 - 10
        c.drawLine(x, 0, x + 50, 66, stroke(mix(dk, (90, 80, 120), 0.25), 5)); c.drawLine(x + 100, 0, x + 50, 66, stroke(mix(dk, (90, 80, 120), 0.25), 5))
    for x, col, sw in ((150, (255, 120, 170), 0.8), (420, LAMP, 0.0), (700, LAMP, 1.6), (950, (120, 180, 255), 2.4)):
        ang = 7 * math.sin(t * 0.42 + sw) + (x - 540) * -0.02
        c.save(); c.translate(x, 60); c.rotate(ang)
        c.drawPath(poly([(-22, 74), (22, 74), (250, 1150), (-250, 1150)], True), paint(shader=lin(0, 74, 0, 1150, [argb(col, 0.20), argb(col, 0.03)])))
        c.drawRoundRect(R.MakeXYWH(-26, 0, 52, 76), 12, 12, paint(dk)); c.drawOval(R.MakeXYWH(-22, 68, 44, 14), paint(col, 0.95))
        c.restore()


def speakers(c):
    dk = (22, 14, 40)
    for x, sc in ((60, 1.0), (1020, 1.0)):
        c.drawRect(R.MakeXYWH(x - 56 * sc, FLOOR - 300 * sc, 112 * sc, 300 * sc), paint(dk))
        c.drawRect(R.MakeXYWH(x - 56 * sc, FLOOR - 300 * sc, 112 * sc, 300 * sc), stroke(INK, 5))
        for yy, r_ in ((-210, 36), (-90, 46)):
            c.drawCircle(x, FLOOR + yy * sc, r_ * sc, paint((48, 34, 72))); c.drawCircle(x, FLOOR + yy * sc, r_ * sc * 0.4, paint((14, 8, 26)))
    # cable + floor wedge
    p = skia.Path(); p.moveTo(40, FLOOR + 66); p.cubicTo(220, FLOOR + 30, 300, FLOOR + 96, 470, FLOOR + 58); c.drawPath(p, stroke((16, 10, 26), 6))


def venue(c, t, lamp=(560, 1180), lamp_a=0.5, dark=0.0):
    top, bot = mix(WALL_TOP, (6, 4, 16), dark), mix(WALL_BOT, (16, 10, 30), dark)
    night_bg(c, t, top, bot, lamp=lamp, lamp_a=lamp_a, floor=None)
    trusses(c, t)
    speakers(c)
    c.drawRect(R.MakeLTRB(0, FLOOR, W, H), paint(shader=lin(0, FLOOR, 0, H, [argb(mix(bot, (0, 0, 0), 0.42)), argb(mix(bot, (0, 0, 0), 0.72))])))
    for i in range(7):    # floor boards, in perspective
        xa = 540 + (i - 3) * 110; xb = 540 + (i - 3) * 330
        c.drawLine(xa, FLOOR, xb, H, stroke((0, 0, 0), 3, 0.28))
    c.drawLine(0, FLOOR, W, FLOOR, stroke(INK, 5))
    fg_dust(c, t, n=8, seed=5, a=0.22)


def blink_stand(t, a="stand", b="stand", t0=0, d=0.3): return lerp_pose(POSES[a], POSES[b], eio(pr(t, t0, d)))


def hook_frame(c, t, base=0.0, count="999", arm=0.0, coin_t=None, you_x=240, gx=610, gw=560):
    venue(c, t)
    sh = 0.0
    if coin_t is not None and 0 <= t - coin_t < 0.3: sh = 7 * (1 - (t - coin_t) / 0.3) * math.sin(t * 90)
    gate(c, gx, count=count, arm=arm, shake=sh, w=gw)
    mic_stand(c, 170, FLOOR, 1.05)


# ---- scenes ----
def S_hook(c, t):
    tz = T("i1", "zero?"); hook_frame(c, t, coin_t=T("i1", "pay"))
    # coin keeps bouncing off the barrier
    tb = T("i1", "pay") ; pose = lerp_pose(POSES["hold"], POSES["shock"], eio(pr(t, tz - 0.2, 0.3)))
    hero(c, 280, FLOOR, 1.15, pose, Face("wide" if t > tz - 0.3 else "open", "o" if t > tz - 0.3 else "smile", look=(1, -1)), t)
    for i in range(3):
        u = (t + i * 1.1) % 3.3
        if u < 1.3:
            q = u / 1.3; cx = lerp(940, 640, min(q * 2, 1)) + (max(q - 0.5, 0)) * 800; cy = 1090 + (-260 * math.sin(math.pi * cl(q * 2)) if q < 0.5 else (q - 0.5) * 2 * 330 - 260 * math.sin(math.pi * (q - 0.5)))
            coin(c, cx, min(cy, FLOOR - 26), 30, spin=u * 7, a=min(1, u * 6) * min(1, (1.3 - u) * 6))
    top_shade(c, 0.6)
    say(c, t, -1, "your song got", "999 PLAYS", YEL, t1=T("i1", "Why") - 0.08, size=240)
    say(c, t, T("i1", "Why") - 0.04, "the recording paid", "$0", (255, 96, 86), t1=SHOT["S_singer"]["start"] + 0.2, size=270)
    fnote(c, t, 0.4, "ON SPOTIFY · IN THE PAST 12 MONTHS")


def S_singer(c, t):
    t_no = T("i3", "It"); tag_k = pop_(t, T("i2", "tiny") - 0.15)
    venue(c, t, lamp=(500, 1000), lamp_a=0.62)
    mic_stand(c, 610, FLOOR, 1.35)
    sing = t < t_no
    hero(c, 450, FLOOR, 1.42, POSES["hold"] if sing else lerp_pose(POSES["hold"], POSES["shrug"], eio(pr(t, t_no, 0.3))),
         Face("happy" if sing else "open", "grin" if sing else "o", look=(1, 0)), t)
    if sing: notes(c, 700, 1180, t, n=4, seed=3)
    x_k = pop_(t, t_no, 0.26, 2.2)
    if tag_k > 0:
        label_card(c, 770, 930, "$ PER PLAY?", 64, RED_C, k=tag_k, tilt=-4)
        if x_k > 0:
            c.save(); c.translate(770, 930); c.scale(x_k, x_k)
            c.drawLine(-180, -60, 180, 60, stroke(RED_C, 16)); c.drawLine(-180, 60, 180, -60, stroke(RED_C, 16))
            c.restore()
    top_shade(c, 0.55)
    say(c, t, SHOT["S_singer"]["start"] + 0.05, "you're the", "SINGER", WHITE, t1=T("i2", "heard") - 0.1)
    say(c, t, T("i2", "heard") - 0.05, "streaming pays", "PER PLAY?", YEL, t1=t_no - 0.08, size=230)
    say(c, t, t_no, "spotify says", "NOT PER PLAY", WHITE, t1=L1("i3") + 0.3, size=210)
    fnote(c, t, T("i3", "Spotify"), "NO MAJOR SERVICE · SPOTIFY LOUD & CLEAR, MAR 2026")


def _icon(c, kind, t, hot=0.0):
    if kind == 0:
        pot(c, 0, 40, 92, 0.7)
    elif kind == 1:
        pie_wedge(c, 0, 0, 44, 0.2)
    elif kind == 2:
        c.drawLine(-50, -30, -50, 44, stroke(INK, 10)); c.drawLine(50, -30, 50, 44, stroke(INK, 10)); c.drawRoundRect(R.MakeXYWH(-52, -2, 104, 22), 9, 9, paint(RED_C)); c.drawRoundRect(R.MakeXYWH(-52, -2, 104, 22), 9, 9, stroke(INK, 4))
    else:
        booth(c, 0, 46, 94, " ", sign=(255, 196, 60))


def S_four(c, t):
    venue(c, t, lamp=(540, 1120), lamp_a=0.5)
    ts = [SHOT["S_four"]["start"] + 0.2 + i * 0.3 for i in range(4)]
    t3 = T("i4", "three"); hot = pr(t, t3, 0.3)
    hero(c, 540, FLOOR, 1.15, POSES["point_up"], Face("open", "smile", look=(0, -1)), t)
    for i in range(4):
        kk = pop_(t, ts[i], 0.3)
        if kk <= 0: continue
        x = 220 + i * 213; y = 920
        sc = kk * (1 + (0.28 * hot if i == 2 else 0) - (0.1 * hot if i != 2 else 0))
        c.save(); c.translate(x, y); c.scale(sc, sc)
        if i == 2 and hot > 0: c.drawCircle(0, 0, 130, paint(shader=rad(0, 0, 130, [argb((255, 70, 60), 0.6 * hot), argb((255, 70, 60), 0)])))
        c.drawCircle(0, 0, 90, paint(WHITE)); c.drawCircle(0, 0, 90, stroke(RED_C if (i == 2 and hot > 0) else INK, 8 if i != 2 else 10))
        _icon(c, i, t)
        c.restore()
        lab = ("POT", "SLICE", "LINE", "MIDDLEMAN")[i]
        f = font("ant", 34); c.drawString(lab, x - f.measureText(lab) / 2, y + 138 * sc, f, paint(WHITE, min(1, kk)))
    top_shade(c, 0.55)
    say(c, t, SHOT["S_four"]["start"] + 0.05, "your money passes", "4 GATES", WHITE, t1=t3 - 0.1)
    say(c, t, t3 - 0.05, "gate three", "STOPS YOU", (255, 96, 86))


PURP = ((52, 28, 110), (120, 52, 150)); GOLD = (250, 196, 80)


def S_pot(c, t):
    diagram_bg(c, *PURP, disc=GOLD, cx=540, cy=1080, r=380, k=pr(t, SHOT["S_pot"]["start"], 0.32))
    pot(c, 540, 1360, 560, 0.0, k=pop_(t, SHOT["S_pot"]["start"] + 0.06))
    hero(c, 170, 1480, 0.8, POSES["point"], Face("open", "smile", look=(1, 0)), t)
    fg_dust(c, t, n=6, a=0.2, col=(255, 255, 255)); top_shade(c, 0.4, (20, 10, 50))
    say(c, t, SHOT["S_pot"]["start"] + 0.05, "gate one", "THE POT", WHITE)


def S_pour(c, t):
    t0 = SHOT["S_pour"]["start"]; k = pr(t, t0 + 0.2, L1("a2") - t0)
    diagram_bg(c, *PURP, disc=GOLD, cx=540, cy=1080, r=380)
    for i in range(14):
        ph = (t * 0.9 + hsh(i, 7)) % 1.0; cx = 540 + 200 * (hsh(i, 8) - 0.5) + 50 * math.sin(i + ph * 3)
        coin(c, cx, 730 + ph * 410, 24, spin=t * 6 + i)
    pot(c, 540, 1360, 560, 0.05 + 0.6 * k, glow=0.3 * k)
    t_c = T("a2", "country,") - 0.2
    calendar(c, 870, 880, 0.72, "EVERY", "MONTH", k=pop_(t, T("a2", "Every") - 0.1))
    label_card(c, 190, 880, "1 COUNTRY", 50, INK, k=pop_(t, t_c))
    hero(c, 170, 1480, 0.8, POSES["arms_up"], Face("happy", "grin", look=(1, -1)), t)
    fg_dust(c, t, n=6, a=0.2, col=(255, 255, 255)); top_shade(c, 0.4, (20, 10, 50))
    say(c, t, t0 + 0.02, "subscriptions", "+ ADS", WHITE, size=260)
    fnote(c, t, T("a2", "pours") - 0.1, "ABOUT 2/3 OF ITS MUSIC MONEY · SPOTIFY")


def S_many(c, t):
    t0 = SHOT["S_many"]["start"]; z = eo(pr(t, t0, 0.8))
    diagram_bg(c, (28, 22, 90), (92, 44, 140), disc=None)
    for i, (x, y, w) in enumerate(((190, 980, 250), (540, 980, 250), (890, 980, 250), (190, 1240, 250), (540, 1240, 250), (890, 1240, 250))):
        k = pop_(t, t0 + 0.05 + 0.08 * i, 0.3)
        c.drawCircle(x, y - 80, 150 * k, paint(GOLD, 0.25))
        pot(c, x, y, w, 0.6 + 0.1 * math.sin(i), k=k)
        if k > 0.9:
            for j in range(3):
                ph = (t * 0.8 + hsh(j, i)) % 1.0; coin(c, x + (j - 1) * 28, y - 190 - (1 - ph) * 110 + 30, 11, spin=t * 6 + j, a=0.9)
    hero(c, 840, 1490, 0.72, POSES["shock"], Face("wide", "o", look=(-1, -1)), t)
    fg_dust(c, t, n=6, a=0.2, col=(255, 255, 255)); top_shade(c, 0.4, (20, 10, 50))
    say(c, t, t0 + 0.02, "last year, spotify paid out", "$11 BILLION+", YEL, size=230)
    fnote(c, t, T("a3", "industry") - 0.5, "ALL COUNTRIES · THE MUSIC INDUSTRY, 2025 · SPOTIFY", y=1466)


TEAL_BG = ((10, 60, 90), (20, 130, 130)); CRM = (250, 228, 170)


def S_slice(c, t):
    t0 = SHOT["S_slice"]["start"]
    diagram_bg(c, *TEAL_BG, disc=CRM, cx=540, cy=1060, r=390, k=pr(t, t0, 0.32))
    pie_wedge(c, 540, 1060, 310, 0.12, k=pop_(t, t0 + 0.08))
    hero(c, 170, 1480, 0.8, POSES["point"], Face("open", "smile", look=(1, -1)), t)
    fg_dust(c, t, n=6, a=0.18, col=(255, 255, 255)); top_shade(c, 0.4, (4, 20, 40))
    say(c, t, t0 + 0.05, "gate two", "YOUR SLICE", WHITE, size=240)


def S_dots(c, t):
    t0 = SHOT["S_dots"]["start"]; k = pr(t, t0 + 0.15, 1.8)
    diagram_bg(c, *TEAL_BG)
    dot_grid(c, 540, 1040, 120, mine=9, w=760, k=k, flash=0.4 + 0.4 * math.sin(t * 5) if k >= 1 else 0.0)
    hero(c, 170, 1480, 0.8, POSES["point"], Face("open", "smile", look=(1, -1)), t)
    fg_dust(c, t, n=6, a=0.18, col=(255, 255, 255)); top_shade(c, 0.4, (4, 20, 40))
    say(c, t, t0 + 0.02, "your plays ÷", "ALL PLAYS", WHITE, size=240)
    fnote(c, t, t0 + 0.6, "IN THAT COUNTRY, THAT MONTH", y=1466)


MADEUP = "MADE-UP NUMBERS"


def S_100(c, t):
    t0 = SHOT["S_100"]["start"]; t4 = L0("b4")
    t_h = T("b3", "hundred", 1) if False else L0("b3") + (L1("b3") - L0("b3")) * 0.52
    diagram_bg(c, (40, 22, 100), (110, 40, 140))
    mv = eio(pr(t, t_h - 0.15, 0.45))
    diagram_disc = (1 - mv)
    if diagram_disc > 0.01: c.drawCircle(540, 1040, 360 * diagram_disc, paint(GOLD))
    pot(c, lerp(540, 150, mv), lerp(1290, 910, mv), lerp(520, 180, mv), 0.55, k=pop_(t, t0 + 0.05))
    label_card(c, lerp(540, 150, mv), lerp(1370, 960, mv), "$100", lerp(84, 54, mv), INK, k=pop_(t, t0 + 0.2))
    k = pr(t, t_h, 0.8)
    fl = pr(t, t4 - 0.05, 0.4)
    dot_grid(c, 610, 1000, 100, mine=5, w=600, cols=10, k=k, flash=fl * (0.6 + 0.4 * math.sin(t * 6)))
    yk = pop_(t, T("b4", "So") - 0.05)
    label_card(c, 660, 1390, "YOU: $5", 74, RED_C, k=yk, tilt=-2)
    hero(c, 170, 1480, 0.8, POSES["point"] if t < t4 else POSES["arms_up"], Face("happy" if t > T("b4", "So") else "open", "grin" if t > T("b4", "So") else "smile", look=(1, -1)), t)
    fg_dust(c, t, n=6, a=0.18, col=(255, 255, 255)); top_shade(c, 0.4, (20, 8, 50))
    say(c, t, t0 + 0.02, "picture a tiny pot", "$100", YEL, t1=t_h - 0.05, size=260)
    say(c, t, t_h, "and in all", "100 PLAYS", WHITE, t1=t4 - 0.08)
    say(c, t, t4 - 0.04, "yours", "5 OF 100", (255, 170, 80), size=260)
    src_chip(c, MADEUP + " · TO SHOW THE MATHS", min(1, pr(t, t0 + 0.1, 0.2)), y=1466, x=620, size=25)


def S_200(c, t):
    t0 = SHOT["S_200"]["start"]; t6 = L0("b6"); td = T("b5", "double.")
    diagram_bg(c, (40, 22, 100), (110, 40, 140))
    pot(c, 150, 720 + 190, 180, 0.55)
    label_card(c, 150, 960, "$100", 54, INK)
    cal = pop_(t, t0 + 0.02)
    calendar(c, 150, 1130, 0.6, "NEXT", "MONTH", k=cal)
    k = pr(t, T("b5", "But") - 0.1, 1.1)
    # orange dots stay put; everybody else's double around them
    total = int(100 + 100 * eo(k))
    dot_grid(c, 610, 1000, 200, mine=5, w=600, cols=15, k=(total / 200.0), flash=pr(t, t6, 0.3) * 0.8)
    if t > t6:
        label_card(c, 660, 1390, "YOU: $2.50", 74, RED_C, k=pop_(t, t6, 0.26, 2.2), tilt=-2)
    else:
        label_card(c, 660, 1390, "YOU: $5", 74, INK, tilt=-2)
    hero(c, 170, 1480, 0.8, POSES["hug"] if t > t6 else POSES["point"], Face("wide" if t > td else "open", "frown" if t > t6 else "o", "worried" if t > t6 else "none", look=(1, -1)), t)
    fg_dust(c, t, n=6, a=0.18, col=(255, 255, 255)); top_shade(c, 0.4, (20, 8, 50))
    say(c, t, t0 + 0.02, "same pot, but", "200 PLAYS", WHITE, t1=t6 - 0.08)
    say(c, t, t6 - 0.04, "your plays now earn", "HALF", (255, 96, 86), size=270, t1=T("b6", "And") - 0.1)
    say(c, t, T("b6", "And") - 0.04, "not one fan", "LOST", WHITE, size=270)
    src_chip(c, MADEUP, 1.0, y=1466, x=620, size=25)


def _gatekeeper(c, t, x=900, pose="stand", face=None):
    extra(c, x, FLOOR, 1.0, POSES[pose], face or Face("open", "flat", look=(-1, 0)), t, scarf=(70, 140, 250), hat=(40, 90, 200))


def S_line(c, t):
    t0 = SHOT["S_line"]["start"]; tr = T("c2", "thousand"); tc2 = L0("c2")
    k = pr(t, tc2 + 0.6, tr - tc2 - 0.5)
    n_ = int(eio(k) * 1000); arm = eo(pr(t, tr + 0.1, 0.5))
    venue(c, t, lamp=(600, 1100), lamp_a=0.5)
    gate(c, 610, count=f"{n_:,}" if n_ else "0", arm=arm, col_ok=arm > 0.5)
    wx = lerp(-80, 250, eo(pr(t, t0, 1.1)))
    walking = t < t0 + 1.1
    hero(c, wx, FLOOR, 1.15, walk_pose(t * 1.5, 0.9) if walking else (POSES["arms_up"] if arm > 0.5 else POSES["stand"]),
         Face("happy" if arm > 0.5 else "open", "grin" if arm > 0.5 else "smile", look=(1, -1)), t)
    _gatekeeper(c, t, 940, "point" if False else "stand")
    if arm > 0.4:
        u = t - (tr + 0.4)
        for j in range(3):
            q = ((u + j * 0.35) % 1.2) / 1.2
            coin(c, lerp(300, 1120, q), FLOOR - 200 - 90 * math.sin(q * math.pi), 28, spin=u * 7 + j)
    top_shade(c, 0.6)
    say(c, t, t0 + 0.05, "gate three", "THE LINE", WHITE, t1=tc2 - 0.08)
    say(c, t, tc2 - 0.04, "a track needs, per year", "1,000 PLAYS", YEL, size=230)
    fnote(c, t, tc2 + 0.1, "SPOTIFY RULE · SINCE APRIL 2024 · RECORDING ROYALTIES", t1=T("c2", "thousand") - 0.1)
    fnote(c, t, T("c2", "thousand") + 0.1, "+ ENOUGH LISTENERS · NUMBER NOT PUBLIC")


def S_out(c, t):
    t0 = SHOT["S_out"]["start"]; tn = T("c4", "nothing.")
    fall = pr(t, t0 + 0.05, 0.22)
    sh = 9 * math.sin(t * 80) * (1 - pr(t, t0 + 0.2, 0.3))
    venue(c, t, lamp=(600, 1100), lamp_a=0.42, dark=0.15)
    gate(c, 610, count="999", arm=1 - eo(fall), shake=sh, flash=(1 - pr(t, t0 + 0.2, 0.5)))
    hero(c, 250, FLOOR, 1.15, POSES["shock"] if t < tn else POSES["hug"], Face("wide", "o" if t < tn else "frown", "worried", look=(1, -1)), t)
    _gatekeeper(c, t, 940)
    u = t - t0
    if u < 1.3:
        coin(c, 560 - 300 * u, min(FLOOR - 28, FLOOR - 160 + 130 * abs(math.sin(u * 5)) + 80 * u), 28, spin=u * 9)
    else:
        coin(c, 170, FLOOR - 28, 28, spin=0)
    top_shade(c, 0.6)
    say(c, t, t0 + 0.02, "nine ninety-nine means", "OUT", (255, 96, 86), size=270, t1=tn - 0.5)
    say(c, t, tn - 0.45, "the recording earns", "NOTHING", WHITE, size=260)
    fnote(c, t, t0 + 0.6, "SONGWRITER ROYALTIES ARE SEPARATE")


def S_penny(c, t):
    t0 = SHOT["S_penny"]["start"]; tp = T("c5", "pennies"); tn = T("c5", "never")
    venue(c, t, lamp=(540, 1320), lamp_a=0.42, dark=0.68)
    c.drawPath(poly([(470, 66), (610, 66), (820, FLOOR + 40), (260, FLOOR + 40)], True), paint(shader=lin(0, 66, 0, FLOOR, [argb(LAMP, 0.26), argb(LAMP, 0.05)])))
    c.drawOval(R.MakeXYWH(260, FLOOR + 10, 560, 60), paint(LAMP, 0.22, blur=10))
    gone = pr(t, tn, 0.7)     # "those pennies often never arrived": the coin fades away on the word
    coin(c, 540, FLOOR + 6 - 26 * eo(gone), 34, spin=t * 2.2, a=1 - gone)
    label_card(c, 500, 1130, "ABOUT 3¢ A MONTH", 70, INK, k=pop_(t, tp), sub="TRACKS UNDER 1,000 · AVERAGE · SPOTIFY")
    if t > tn - 0.3:
        hero(c, 880, FLOOR, 0.95, POSES["shrug"], Face("open", "flat", "worried", look=(-1, 0)), t)
    top_shade(c, 0.55)
    say(c, t, t0 + 0.02, "why so harsh?", "PENNIES", YEL, size=270)
    fnote(c, t, tn - 0.2, "OFTEN BELOW THE $2-$50 WITHDRAWAL MINIMUM")


def S_share(c, t):
    t0 = SHOT["S_share"]["start"]; k = pr(t, t0 + 0.1, 1.5)
    venue(c, t, lamp=(700, 1250), lamp_a=0.5, dark=0.5)
    for i in range(5):
        q = cl(k * 1.5 - i * 0.12)
        x = lerp(220 + i * 55, 760, eo(q)); y = FLOOR - 30 - (0 if q >= 1 else 0)
        if q < 1: coin(c, x, y, 30, spin=q * 12 + i)
    # the bigger track's stack grows
    h = 8 + int(k * 5)
    for i in range(h):
        c.drawOval(R.MakeXYWH(700, FLOOR - 16 - i * 22, 120, 34), paint((255, 200, 50))); c.drawOval(R.MakeXYWH(700, FLOOR - 16 - i * 22, 120, 34), stroke(INK, 5))
    girl(c, 910, FLOOR, 1.0, POSES["arms_up"] if k > 0.5 else POSES["stand"], Face("happy", "grin", look=(-1, 0)), t, dress=TEAL_C)
    hero(c, 210, FLOOR, 1.0, POSES["stand"], Face("open", "flat", look=(1, 0)), t)
    top_shade(c, 0.55)
    say(c, t, t0 + 0.02, "shared among tracks that", "QUALIFY", WHITE, size=270)
    fnote(c, t, t0 + 0.5, "SPOTIFY SAYS IT DOESN'T PROFIT FROM THIS")


COR = ((96, 40, 70), (196, 92, 58)); GD2 = (255, 210, 120)


def clerk(c, t, pose, k):
    """the label's person, seen through the booth window"""
    if k <= 0: return
    c.save(); c.clipRect(R.MakeLTRB(523, 1092, 877, 1234))
    girl(c, 700, 1240 + 150 * (1 - eo(k)) + 100, 0.72, POSES[pose], Face("open", "smile", look=(-1, 0)), t, dress=(240, 90, 140), style="bun", hair_col=(60, 34, 30))
    c.restore()


def S_booth(c, t):
    t0 = SHOT["S_booth"]["start"]; t2 = L0("d2")
    diagram_bg(c, *COR, disc=GD2, cx=620, cy=1020, r=380, k=pr(t, t0, 0.3), floor=FLOOR)
    c.drawLine(0, FLOOR, W, FLOOR, stroke(INK, 5))
    booth(c, 700, FLOOR, 500, "LABEL OR DISTRIBUTOR", k=pop_(t, t0 + 0.06))
    clerk(c, t, "stand", pr(t, t0 + 0.3, 0.3))
    if t > T("d2", "It") - 0.15 and t < L1("d2") + 0.2:
        for i in range(8):
            ph = (t * 0.85 + hsh(i, 3)) % 1.0
            coin(c, 700 + 220 * (hsh(i, 4) - 0.5), 690 + ph * 220, 24, spin=t * 6 + i, a=min(1, ph * 5) * min(1, (1 - ph) * 6))
    reach = t > t2
    hero(c, 190, FLOOR, 1.15, POSES["point"] if reach else POSES["stand"], Face("wide" if reach else "open", "frown" if reach else "smile", "worried" if reach else "none", look=(1, 0)), t)
    if reach: 
        pass
    fg_dust(c, t, n=6, a=0.18, col=(255, 255, 255)); top_shade(c, 0.45, (36, 10, 30))
    say(c, t, t0 + 0.05, "gate four", "THE MIDDLEMAN", WHITE, t1=t2 - 0.08, size=220)
    say(c, t, t2 - 0.04, "spotify doesn't pay you", "IT PAYS THEM", YEL, size=220)


def S_deal(c, t):
    t0 = SHOT["S_deal"]["start"]; tc = T("d3", "Spotify")
    diagram_bg(c, *COR, disc=GD2, cx=620, cy=1020, r=380, floor=FLOOR)
    c.drawLine(0, FLOOR, W, FLOOR, stroke(INK, 5))
    booth(c, 700, FLOOR, 500, "LABEL OR DISTRIBUTOR")
    clerk(c, t, "wave", 1.0)
    q = pr(t, t0 + 0.7, 1.0)
    if q > 0:
        coin(c, lerp(560, 260, eo(q)), lerp(1120, 1190, eo(q)) - 90 * math.sin(math.pi * q), 26, spin=q * 12)
    hero(c, 190, FLOOR, 1.15, POSES["hold"], Face("open", "smile" if t < tc else "flat", look=(1, 0)), t)
    contract(c, 290, 900, 240, k=pop_(t, t0 + 0.05), tilt=-4)
    fg_dust(c, t, n=6, a=0.18, col=(255, 255, 255)); top_shade(c, 0.45, (36, 10, 30))
    say(c, t, t0 + 0.02, "your deal", "DECIDES", WHITE, size=280)
    fnote(c, t, tc - 0.1, "SPOTIFY SAYS IT CAN'T SEE YOUR TAKE-HOME")


ROSE_T, ROSE_B = (46, 26, 84), (176, 62, 110)


def livingroom(c, t):
    night_bg(c, t, ROSE_T, ROSE_B, lamp=(300, 1140), lamp_a=0.5, floor=FLOOR, seed=31)
    # window with a moon + a poster: one simple silhouette layer
    c.drawRoundRect(R.MakeXYWH(70, 760, 260, 320), 12, 12, paint((26, 20, 62))); c.drawRoundRect(R.MakeXYWH(70, 760, 260, 320), 12, 12, stroke(INK, 7))
    c.drawCircle(240, 860, 42, paint((244, 234, 196)))
    c.drawLine(200, 760, 200, 1080, stroke(INK, 5)); c.drawLine(70, 920, 330, 920, stroke(INK, 5))
    c.drawRoundRect(R.MakeXYWH(10, 1170, 390, 250), 26, 26, paint((96, 44, 96)))   # sofa
    c.drawRoundRect(R.MakeXYWH(10, 1170, 390, 250), 26, 26, stroke(INK, 7))
    c.drawRoundRect(R.MakeXYWH(-10, 1340, 430, 84), 18, 18, paint((122, 58, 116))); c.drawRoundRect(R.MakeXYWH(-10, 1340, 430, 84), 18, 18, stroke(INK, 7))
    fg_dust(c, t, n=6, a=0.2)


def band_poster(c, x, y, k=1.0):
    if k <= 0: return
    card(c, x, y, 300, 250, fill=(36, 28, 70), r=12, k=k)
    ctext(c, "ONE BAND", 0, -74, "ant", 54, YEL)
    m = minis()
    for i, q in enumerate((-90, 0, 90)):
        c.drawImageRect(m[i + 3], R.MakeXYWH(q - 42, -50, 84, 140))
    card_end(c)


def sofa_hero(c, t, face, pose="sit", prop=None):
    return hero(c, 200, FLOOR + 52, 1.15, POSES[pose], face, t, prop=prop)


def S_sofa(c, t):
    t0 = SHOT["S_sofa"]["start"]
    livingroom(c, t)
    band_poster(c, 770, 960, k=pop_(t, T("e1", "one") - 0.2))
    sofa_hero(c, t, Face("happy", "grin", look=(1, 0)))
    phone(c, 320, 1250, 92)
    notes(c, 720, 1250, t, n=3, seed=5)
    top_shade(c, 0.5)
    say(c, t, t0 + 0.05, "now switch seats", "SUBSCRIBER", WHITE, size=230, t1=T("e1", "one") - 0.3)
    say(c, t, T("e1", "one") - 0.28, "all month, you play", "ONE BAND", YEL, size=250)


def S_flow(c, t):
    t0 = SHOT["S_flow"]["start"]; te3 = L0("e3")
    livingroom(c, t)
    band_poster(c, 770, 900)
    pot(c, 820, FLOOR + 20, 320, 0.62, k=pop_(t, t0 + 0.05))
    sofa_hero(c, t, Face("wide" if t < te3 else "open", "o" if t < te3 else "smile", look=(1, 0)))
    phone(c, 320, 1250, 92)
    if t < te3:
        for j in range(4):
            q = ((t - t0 + j * 0.35) % 1.4) / 1.4
            coin(c, lerp(340, 820, q), lerp(1230, 1160, q) - 200 * math.sin(q * math.pi), 24, spin=q * 12)
    else:
        arrow_line(c, [(350, 1190), (540, 1040), (640, 960)], pr(t, te3 + 0.1, 0.6), WHITE)
        q = ((t - te3) % 1.2) / 1.2
        if t > te3 + 0.5: coin(c, lerp(350, 640, q), lerp(1190, 960, q) - 60 * math.sin(q * math.pi), 24, spin=q * 12)
    top_shade(c, 0.5)
    say(c, t, t0 + 0.02, "your money still", "GOES IN THE POT", WHITE, size=190, t1=te3 - 0.08)
    say(c, t, te3 - 0.04, "only who you play?", "FAIRER?", YEL, size=270)
    fnote(c, t, t0 + 0.4, "SPLIT BY EVERYBODY'S PLAYS", t1=te3 - 0.1)
    fnote(c, t, te3 + 0.2, "IT'S CALLED USER-CENTRIC PAY")


NAVY1 = ((14, 18, 64), (54, 40, 130))


def S_study(c, t):
    t0 = SHOT["S_study"]["start"]; k = pop_(t, t0 + 0.05, 0.36, 1.3)
    diagram_bg(c, *NAVY1, disc=(230, 216, 170), cx=540, cy=1080, r=370, k=pr(t, t0, 0.3))
    if k > 0:
        card(c, 540, 1060, 760, 420, fill=(252, 250, 244), r=20, k=k, tilt=-1)
        f = font("mxb", 56)
        for i, ln in enumerate(("“a maximum of a few", "euros per year on", "average per artist”")):
            ctext(c, ln, 0, -90 + i * 74, "mxb", 54, INK)
        ctext(c, "FRENCH NATIONAL MUSIC CENTRE, JAN 2021", 0, 152, "mxb", 25, (110, 110, 124))
        hl = eo(pr(t, T("e4", "few") - 0.1, 0.5))
        if hl > 0:     # marker sweep under the words that matter, on the VO word
            c.drawRoundRect(R.MakeXYWH(-310, -30 + 22, 620 * hl, 9), 4, 4, paint((245, 170, 40)))
        card_end(c)
    girl(c, 170, 1490, 0.8, POSES["point"], Face("open", "smile", look=(1, -1)), t, dress=(240, 90, 140), style="bun", hair_col=(40, 30, 40))
    fg_dust(c, t, n=6, a=0.18, col=(255, 255, 255)); top_shade(c, 0.45, (6, 6, 30))
    say(c, t, t0 + 0.02, "outside the top 10,000 artists", "A FEW EUROS", YEL, size=230)
    fnote(c, t, t0 + 0.5, "FRANCE, 2019 DATA · IT DOESN'T SAY WHICH IS FAIRER", y=1466, )


def S_swing(c, t):
    t0 = SHOT["S_swing"]["start"]
    diagram_bg(c, *NAVY1)
    # a line that swings wildly
    pts = [(120, 1050), (230, 1040), (330, 880), (440, 1200), (560, 800), (680, 1260), (800, 890), (960, 1120)]
    k = pr(t, t0 + 0.05, 1.0)
    seg = poly(partial_pts(pts, k))
    c.drawLine(100, 1050, 980, 1050, stroke(WHITE, 4, 0.35)); c.drawPath(seg, stroke(YEL, 12))
    label_card(c, 330, 790, "1 IN 5 COULD DOUBLE", 50, (20, 130, 80), k=pop_(t, t0 + 0.5))
    label_card(c, 630, 1370, "ABOUT 4 IN 10 LOSE 40%+", 50, RED_C, k=pop_(t, t0 + 0.9))
    hero(c, 170, 1490, 0.72, POSES["shock"], Face("wide", "o", look=(1, -1)), t)
    fg_dust(c, t, n=6, a=0.18, col=(255, 255, 255)); top_shade(c, 0.45, (6, 6, 30))
    say(c, t, t0 + 0.02, "a later study found", "BIGGER SWINGS", WHITE, size=200)
    fnote(c, t, t0 + 0.4, "PRO MUSIK · 50K SOUNDCLOUD ARTISTS · VIA MBW, 2023")


def S_take(c, t):
    t0 = SHOT["S_take"]["start"]; tm = T("t1", "Making"); venue(c, t, lamp=(500, 1020), lamp_a=0.6)
    mic_stand(c, 180, FLOOR, 1.05)
    hero(c, 340, FLOOR, 1.15, POSES["point"], Face("open", "smile", look=(1, 0)), t)
    if t < tm:
        label_card(c, 720, 1150, "999 PLAYS", 88, RED_C, k=pop_(t, t0 + 0.08), sub="NOT A PAYCHECK")
    else:
        contract(c, 730, 1140, 330, k=pop_(t, tm, 0.3), tilt=3)
    top_shade(c, 0.55)
    say(c, t, t0 + 0.02, "a play count isn't a", "PAYCHECK", WHITE, size=260, t1=tm - 0.08)
    say(c, t, tm - 0.04, "making music?", "READ YOUR DEAL", YEL, size=210)


def S_end(c, t):
    t0 = SHOT["S_end"]["start"]; tz2 = L0("z2")
    hook_frame(c, t, gx=560, gw=420)                # loop: back on the frame-1 gate
    hero(c, 270, FLOOR, 1.05, POSES["point_up"] if t > tz2 else POSES["hold"], Face("open", "smile", look=(1, -1)), t)
    girl(c, 860, FLOOR, 1.05, POSES["wave"] if t > tz2 else POSES["stand"], Face("happy" if t > tz2 else "open", "grin" if t > tz2 else "smile", look=(-1, 0)), t, dress=TEAL_C, style="long", flip=True)
    top_shade(c, 0.62)
    say(c, t, t0 + 0.02, "pay only who you play?", "YES OR NO", YEL, size=250, t1=tz2 - 0.08)
    say(c, t, tz2 - 0.04, "send it to a new artist", "SAVE THIS", WHITE, size=250)
    kk = pop_(t, T("z1", "Comment") - 0.25)
    if kk > 0:
        c.save(); c.translate(540, 780); c.scale(kk, kk)
        for sx, tx, col in ((-130, "YES", GRN), (130, "NO", RED_C)):
            c.drawRoundRect(R.MakeXYWH(sx - 104, -56, 208, 112), 56, 56, paint((0, 0, 0), 0.25, blur=8))
            c.drawRoundRect(R.MakeXYWH(sx - 104, -56, 208, 112), 56, 56, paint(col)); c.drawRoundRect(R.MakeXYWH(sx - 104, -56, 208, 112), 56, 56, stroke(INK, 6))
            ctext(c, tx, sx, 28, "ant", 78, WHITE)
        c.restore()
    src_chip(c, "COMMENT ONE WORD", min(1, pr(t, T("z1", "Comment") - 0.2, 0.3)) * (1 - pr(t, tz2, 0.2)))


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}
SURF = surface()
IMPACTS = [(SHOT["S_out"]["start"] + 0.06, 0.28, 10), (T("i1", "pay"), 0.2, 4)]
TOPLINE = "OOPSMYBUSINESS · HOW IT WORKS"


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    c = SURF.getCanvas(); c.resetMatrix(); c.clear(skia.ColorBLACK)
    # slow NBN push-in on every shot
    u = pr(tt, s["start"], max(0.5, s["end"] - s["start"])); z = 1.0 + 0.022 * u
    dx = dy = 0.0
    for ti, d, a in IMPACTS:
        if ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83)
    c.save(); c.translate(W / 2 + dx, H * 0.62 + dy); c.scale(z, z); c.translate(-W / 2, -H * 0.62)
    RENDER[sid](c, tt)
    c.restore()
    pill(c, TOPLINE)
    return to_rgb(SURF).astype(np.float32)


def _bl(x, s_):
    if s_ < 0.5: return x
    sm = cv2.resize(x, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    return cv2.resize(cv2.GaussianBlur(sm, (0, 0), s_ / 4), (W, H), interpolation=cv2.INTER_LINEAR)


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); k = sh["trans"]; dt = t - sh["start"]
    if i > 0:
        if k == "focus" and dt < 0.3:
            p = dt / 0.3; prv = rs(SHOTS[i - 1]["id"], t, n); m = eio(p)
            f = _bl(prv, 40 * m) * (1 - m) + _bl(f, 40 * (1 - m)) * m
        elif k == "whip" and dt < 0.2:
            p = 1 - dt / 0.2; M = np.float32([[1, 0, -360 * p * p], [0, 1, 0]])
            f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
        elif k == "zoom" and dt < 0.2:
            p = 1 - dt / 0.2; acc = np.zeros_like(f)
            for q in range(5): acc += cam(f, 1 + 0.06 * q * p)
            f = acc / 5
        elif k == "punch" and dt < 0.14: f = cam(f, 1 + 0.08 * (1 - dt / 0.14)) + 0.14 * (1 - dt / 0.14)
    nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    if nx is not None and nx["trans"] == "whip" and sh["end"] - t < 0.12:
        p = 1 - (sh["end"] - t) / 0.12; M = np.float32([[1, 0, 360 * p * p], [0, 1, 0]])
        f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
