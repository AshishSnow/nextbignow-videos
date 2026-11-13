# ================= HOW TO START EP 9: start childminding in England — the two-hour line (whiteboard). Held object: ONE small house
# ("YOUR PLACE") with a wall clock in its gable and a door tag that a tiny eraser rubs out and rewrites per step
# (? → 2 HOURS → THE LINE → REGISTERED → CHECKED → MAX 6). Kids are small stick figures (never realistic children).
# New drawings (this episode → board.py): home_m (house + gable clock + door tag), kid_m (small stick child, hat / scarf),
# baby_m, shield_m (insurance), healthform_m, notice_m (plain letter), moon_m, pricetag_m, two_houses (swap arrows), hourbar_m.
# Opening move (new): frame 0 is the house with its clock already sweeping red from 3 pm, two little kids at the door and the pen
# hovering over a "?" on the door tag; on "two-hour" the wedge completes and the pen draws a thick red LINE at its edge.
# Visual upgrade (14 Nov): LINE BOIL — every marker line is re-inked in 3 variants cycling every 3 frames (set_boil in rs()), borrowed
# from the owner's 13 Nov doodle look; held drawings no longer sit frozen. =================
L0 = lambda i: LINES[i]["start"]; L1 = lambda i: LINES[i]["end"]


def TT(lid, w, frac=0.5, nth=0):
    try: return T(lid, w, nth)
    except Exception: return L0(lid) + (L1(lid) - L0(lid)) * frac


import sys as _sys, os as _os
_sys.path.insert(0, _D if "_D" in globals() else f"{B}/scripts")
from nbnkit import *        # noqa
from nbnkit.board import *  # noqa
from nbnkit.board import _path, _sc   # noqa
import skia

TEALK = (40, 170, 170); YELK = (240, 196, 40)


# ---------------------------------------------------------------- new marker props (this episode)
def home_m(c, x, y, s, t, t0, tag="?", new=None, t_sw=1e9, fill_t=-9.0, hours=2.0, col=GR, tag_col=RD, line_t=None):
    """the held house: house_m + a wall clock in the gable (red wedge from 3 pm) + a door tag that is rubbed out and rewritten"""
    house_m(c, x, y, s, t, t0, col)
    clock_m(c, x, y - 128 * s, t, t0 + 0.25, r=30 * s, h0=15.0, hours=hours, fill_t=fill_t, col=RD)
    if line_t is not None and t > line_t:   # the LINE: a thick red stroke out of the clock at the wedge's edge
        a_ = math.radians((15 % 12) * 30 + hours * 30)
        cx, cy = x, y - 128 * s
        ink(c, [[(cx + 0.2 * 30 * s * math.sin(a_), cy - 0.2 * 30 * s * math.cos(a_)), (cx + 1.6 * 30 * s * math.sin(a_), cy - 1.6 * 30 * s * math.cos(a_))]],
            pr(t, line_t, 0.3), RD, 12, pen_=False)
    if tag is not None or new is not None:
        ownertag(c, x, y - 112 * s + 40 + 60 * s, t, t0 + 0.4, tag or "", new, t_sw, tag_col, None)


def kid_m(c, x, y, s, t, look=(0, 0), girl_=False, col=TEALK, hat=None, scarf=False, pose="stand", a=1.0):
    """a small stick child (scale ~0.4-0.6 of an adult); optional little cap, or the hero's orange scarf (= yours)"""
    if s <= 0: return
    if girl_: girl(c, x, y, s, POSES[pose], Face("open", "smile", look=look), t, dress=col, scarf=ORANGE if scarf else None, a=a)
    else: hero(c, x, y, s, POSES[pose], Face("open", "smile", look=look), t, scarf=ORANGE if scarf else col, a=a)
    hy = y - 330 * s   # roughly the top of the head
    if hat: c.drawPath(_path([(x - 40 * s, hy + 6 * s), (x, hy - 50 * s), (x + 40 * s, hy + 6 * s), (x - 40 * s, hy + 6 * s)]), paint(hat, a))


def baby_m(c, x, y, s, t, t0):
    """a baby in a tiny basket (no realistic child): half-oval basket, round head, bonnet arc"""
    k = pr(t, t0, 0.4)
    if k <= 0: return
    ink(c, [wob(circ_pts(x, y, 90 * s, 0, 180, 24, ry=50 * s), 611, 0.5), [(x - 90 * s, y), (x + 90 * s, y)]], k, MK, 6)
    if k >= 1:
        hatch(c, _path(circ_pts(x, y, 88 * s, 0, 180, 20, ry=48 * s)), 1, YELK, gap=14, w=5, bbox=(x - 90 * s, y, x + 90 * s, y + 52 * s), a=0.5)
        c.drawCircle(x - 20 * s, y - 24 * s, 34 * s, paint(WHITE)); c.drawCircle(x - 20 * s, y - 24 * s, 34 * s, stroke(MK, 5))
        c.drawArc(R.MakeXYWH(x - 64 * s, y - 70 * s, 88 * s, 84 * s), 160, 200, False, stroke(PINK, 8))
        c.drawCircle(x - 30 * s, y - 28 * s, 4, paint(MK)); c.drawCircle(x - 10 * s, y - 28 * s, 4, paint(MK))


def shield_m(c, x, y, t, t0, s=1.0, col=BLU, label=None):
    k = pr(t, t0, 0.45)
    if k <= 0: return
    pts = _sc(x, y, s, [(-80, -100), (0, -130), (80, -100), (80, 0), (0, 110), (-80, 0), (-80, -100)])
    if k > 0.6: hatch(c, _path(pts), pr(k, 0.6, 0.4), col, gap=16, w=6, bbox=(x - 90 * s, y - 140 * s, x + 90 * s, y + 120 * s), a=0.45)
    ink(c, [wob(pts, 621, 0.6), [(x - 36 * s, y - 10 * s), (x - 6 * s, y + 24 * s), (x + 44 * s, y - 40 * s)]], k, MK, 7)
    if label: mtext(c, label, x, y + 190 * s, int(44 * s), col, pr(t, t0 + 0.4, 0.3), "pm")


def healthform_m(c, x, y, t, t0, s=1.0, sign_t=None, label="HEALTH FORM"):
    w, h = 230 * s, 290 * s; k = pr(t, t0, 0.4)
    if k <= 0: return
    c.drawRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), paint(WHITE, k))
    ink(c, [wob([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)], 631, 0.6)], k, MK, 6, pen_=False)
    ink(c, [[(x, y - h / 2 + 30 * s), (x, y - h / 2 + 84 * s)], [(x - 27 * s, y - h / 2 + 57 * s), (x + 27 * s, y - h / 2 + 57 * s)]], k, GR, 10, pen_=False)
    for i in range(3): ink(c, [[(x - w / 2 + 26 * s, y - 20 * s + i * 40 * s), (x + w / 2 - 26 * s, y - 20 * s + i * 40 * s)]], k, LIGHT, 5, pen_=False)
    if sign_t is not None and t > sign_t:
        sig = [(x - 70 * s + 140 * s * i / 14, y + h / 2 - 50 * s + 14 * s * math.sin(i * 1.9)) for i in range(15)]
        ink(c, [sig], pr(t, sign_t, 0.5), BLU, 5, pen_=False)
    if label: mtext(c, label, x, y + h / 2 + 64 * s, int(40 * s), MK, pr(t, t0 + 0.4, 0.3), "pm")


def notice_m(c, x, y, t, t0, s=1.0, head="NOTICE", body="STOP", col=RD):
    w, h = 460 * s, 300 * s; k = pr(t, t0, 0.45)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(-3)
    c.drawRect(R.MakeXYWH(-w / 2, -h / 2, w, h), paint(WHITE, k))
    ink(c, [wob([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)], 641, 0.6)], k, MK, 6, pen_=False)
    mtext(c, head, 0, -h / 2 + 70 * s, int(46 * s), MK, pr(t, t0 + 0.3, 0.3), "pm")
    mtext(c, body, 0, 70 * s, int(110 * s), col, pr(t, t0 + 0.5, 0.35), "pm")
    c.restore()


def moon_m(c, x, y, r, k):
    if k <= 0: return
    p = skia.Path(); p.addCircle(x, y, r); q = skia.Path(); q.addCircle(x + r * 0.45, y - r * 0.2, r * 0.85)
    m = skia.Op(p, q, skia.PathOp.kDifference_PathOp)
    c.drawPath(m, paint(YELK, 0.6 * k)); c.drawPath(m, stroke(MK, 5, k))


def pricetag_m(c, x, y, text, k, col=MK, tilt=-6, size=60, strike_t=None, t=0.0):
    if k <= 0: return
    f = font("pm", size); w = tw(f, text) + 80; h = size * 1.5
    c.save(); c.translate(x, y); c.rotate(tilt); s_ = eback(min(1, k), 1.7); c.scale(s_, s_)
    p = _path([(-w / 2, -h / 2), (w / 2 - 30, -h / 2), (w / 2, 0), (w / 2 - 30, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)])
    c.drawPath(p, paint(WHITE)); c.drawPath(p, stroke(MK, 6)); c.drawCircle(w / 2 - 34, 0, 8, stroke(MK, 4))
    c.drawString(text, -w / 2 + 28, size * 0.36, f, paint(col))
    if strike_t is not None and t > strike_t:
        ink(c, [[(-w / 2 + 14, 8), (w / 2 - 50, -10)]], pr(t, strike_t, 0.25), RD, 9, pen_=False)
    c.restore()


def hourbar_m(c, x, y, t, t0, n, fill_t=None, step=0.4, cell=150, line_at=None, line_t=None, cols=(GR, GR, RD)):
    """a row of hour blocks (3 pm → 3 pm + n); blocks fill one by one; a red LINE is drawn after block `line_at`"""
    x0 = x - cell * n / 2; k = pr(t, t0, 0.5)
    grid = [[(x0, y), (x0 + cell * n, y), (x0 + cell * n, y + 110), (x0, y + 110), (x0, y)]] + [[(x0 + cell * i, y), (x0 + cell * i, y + 110)] for i in range(1, n)]
    ink(c, [wob(g, 650 + i, 0.4) for i, g in enumerate(grid)], k, MK, 5, pen_=False)
    for i in range(n + 1): mtext(c, f"{3 + i}PM", x0 + cell * i, y + 160, 34, LIGHT, k, "kb")
    if fill_t is not None and k >= 1:
        for i in range(n):
            ki = pr(t, fill_t + i * step, 0.3)
            if ki > 0: c.drawRect(R.MakeXYWH(x0 + cell * i + 8, y + 8, (cell - 16) * ki, 94), paint(cols[min(i, len(cols) - 1)], 0.5))
    if line_at is not None and line_t is not None and t > line_t:
        lx = x0 + cell * line_at
        ink(c, [[(lx, y - 70), (lx, y + 180)]], pr(t, line_t, 0.3), RD, 14, pen_=False)


def two_houses(c, x, y, t, t0, s=0.7):
    house_m(c, x - 110, y, s, t, t0, BLU); house_m(c, x + 110, y, s, t, t0 + 0.15, OR)
    if t > t0 + 0.5:
        arrow_m(c, (x - 50, y - 210), (x + 50, y - 210), pr(t, t0 + 0.5, 0.3), MK, 7)
        arrow_m(c, (x + 50, y - 170), (x - 50, y - 170), pr(t, t0 + 0.7, 0.3), MK, 7)


def tick(c, x, y, k, col=GR, s=1.0):
    if k <= 0: return
    ink(c, [[(x - 30 * s, y), (x - 8 * s, y + 24 * s), (x + 36 * s, y - 34 * s)]], k, col, 12, pen_=False)


def box3(c, x, y, t, t0, label, tick_t=None, w=280, h=300):
    k = pr(t, t0, 0.4)
    if k <= 0: return
    ink(c, [wob([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)], int(x) % 97, 0.6)], k, MK, 6, pen_=False)
    mtext(c, label, x, y + h / 2 + 62, 42, MK, pr(t, t0 + 0.2, 0.3), "pm")
    if tick_t is not None and t > tick_t: tick(c, x + w / 2 - 20, y - h / 2 + 10, pr(t, tick_t, 0.3), GR, 1.3)


# ---------------------------------------------------------------- shots
SHOTLIST = [("S_i1", 0.0, "cut"), ("S_i3", L0("i3") - 0.1, "wipe"), ("S_i4", L0("i4") - 0.1, "wipe"), ("S_a1", L0("a1") - 0.1, "wipe"),
            ("S_a2", L0("a2") - 0.1, "wipe"), ("S_a3", L0("a3") - 0.1, "wipe"), ("S_a4", L0("a4") - 0.1, "wipe"), ("S_a5", L0("a5") - 0.1, "wipe"),
            ("S_a6", L0("a6") - 0.1, "wipe"), ("S_b1", L0("b1") - 0.1, "wipe"), ("S_b2", L0("b2") - 0.1, "wipe"), ("S_c1", L0("c1") - 0.1, "wipe"),
            ("S_c2", L0("c2") - 0.1, "wipe"), ("S_c3", L0("c3") - 0.1, "cut"), ("S_c4", L0("c4") - 0.1, "wipe"), ("S_c5", L0("c5") - 0.1, "wipe"),
            ("S_d1", L0("d1") - 0.1, "wipe"), ("S_d2", L0("d2") - 0.1, "wipe"), ("S_d3", L0("d3") - 0.1, "cut"), ("S_e1", L0("e1") - 0.1, "wipe"),
            ("S_e2", L0("e2") - 0.1, "wipe"), ("S_e3", L0("e3") - 0.1, "wipe"), ("S_f2", L0("f2") - 0.1, "wipe"), ("S_t1", L0("t1") - 0.1, "wipe"),
            ("S_end", L0("z1") - 0.1, "wipe")]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
HX, HY = 540, 1430    # the held house's home spot


def S_i1(c, t):
    """frame 0: the house with its clock wedge already sweeping from 3 pm, two little kids at the door, the pen over the '?' tag;
    on 'two-hour' the wedge completes and the pen draws the red LINE; on i2 the two things past the line are drawn"""
    t2 = L0("i2"); tl = TT("i1", "two-hour", 0.6); tr_ = TT("i2", "register", 0.4); tch = TT("i2", "checks.", 0.3)
    hx = HX if t < t2 - 0.2 else HX - 200 * eio(pr(t, t2 - 0.2, 0.5))
    home_m(c, hx, HY, 2.5, t, -2.0, "?", "2 HOURS", tl, fill_t=-0.9, line_t=tl)
    kid_m(c, hx + 340, HY, 0.62, t, look=(-1, 0), girl_=True, col=PINK)
    kid_m(c, hx + 450, HY, 0.68, t, look=(-1, 0))
    if 0.12 < t < tl - 0.2: pen(c, hx + 180 + 18 * math.sin(t * 3), HY - 380 + 10 * math.cos(t * 4))
    if t > t2:
        c.save(); c.translate(850, 900); c.scale(0.7, 0.7); form_m(c, 0, 0, t, tr_ - 0.3); c.restore()
        mtext(c, "REGISTER", 850, 1060, 48, BLU, pr(t, tr_, 0.3), "pm")
        if t > tch - 0.4:
            card_m(c, 850, 1230, 200, pop_(t, tch - 0.4), BLU, -6)
            magnifier_m(c, 880, 1220, 70, pr(t, tch - 0.2, 0.3))
            mtext(c, "CHECKS", 850, 1390, 48, RD, pr(t, tch, 0.3), "pm")
    say(c, t, -2.0, "do you know minding kids for pay has a", "2-HOUR LINE?", MK, t1=t2 - 0.3, under=RD)
    say(c, t, t2 - 0.25, "cross it and you", "REGISTER FIRST", RD, under=RD)
    note(c, t, -2.0, "ENGLAND · EDUCATION ONLY, NOT LEGAL ADVICE")


def S_i3(c, t):
    t0 = SHOT["S_i3"]["start"]; tf = TT("i3", "family", 0.4); tc = TT("i3", "cash.", 0.3)
    home_m(c, 220, HY, 1.6, t, t0 - 3, "?", fill_t=-9)
    hero(c, 440, FLOOR, 0.85, POSES["wave"] if t > tf + 0.4 else POSES["stand"], Face("open", "smile", look=(1, 0)), t)
    u = pr(t, tf - 0.4, 1.4); px = 1000 - 200 * eio(u)
    girl(c, px, FLOOR, 0.85, POSES["hold"] if t > tc - 0.3 else POSES["stand"], Face("open", "smile", look=(-1, 0)), t, flip=True, dress=GR)
    kid_m(c, px - 130, FLOOR, 0.58, t, look=(-1, 0), girl_=True, col=PINK)
    kid_m(c, px - 220, FLOOR, 0.6, t, look=(-1, 0), col=BLU)
    if t > tc - 0.3: cash_m(c, px - 90, 1010, t, tc - 0.3, 0.55, "£", tilt=-8)
    if t > tf: tagpill_m(c, 740, 860, "AFTER SCHOOL", pop_(t, tf), OR, 44)
    say(c, t, t0 + 0.08, "you're in england · a family down the road", "AFTER SCHOOL", MK, under=OR, size=150)


def S_i4(c, t):
    t0 = SHOT["S_i4"]["start"]; tf = TT("i4", "Four", 0.3); tc = TT("i4", "counting", 0.4); to = TT("i4", "own", 0.4)
    labs = ["THE LINE", "REGISTER", "CHECKS", "HEADS"]
    for i in range(4):
        tk = tf - 0.1 + i * 0.22
        if t < tk: continue
        x, y = 290 + (i % 2) * 450, 870 + (i // 2) * 320; kk = pop_(t, tk)
        c.save(); c.translate(x, y); c.scale(kk, kk)
        ink(c, [wob([(-190, -110), (190, -110), (190, 110), (-190, 110), (-190, -110)], 70 + i, 0.6)], 1, MK, 6, pen_=False)
        mtext(c, str(i + 1), -140, -30, 60, RD if i == 3 else BLU, 1, "pm")
        mtext(c, labs[i], 20, 60 if i < 3 else -10, 50, MK, 1, "pm")
        c.restore()
    if t > tc - 0.3:
        for j in range(3):
            kid_m(c, 680 + j * 80, 1290, 0.3, t, girl_=(j == 1), col=[BLU, PINK, TEALK][j], scarf=(j == 2 and t > to - 0.2))
        if t > to: mtext(c, "+ YOURS", 740, 1440, 40, OR, pr(t, to, 0.3), "pm")
    say(c, t, t0 + 0.08, "before you say yes", "4 STEPS", RD, under=RD)


def S_a1(c, t):
    t0 = SHOT["S_a1"]["start"]
    home_m(c, HX, HY, 2.7, t, t0 - 3, "2 HOURS", "THE LINE", t0 + 0.3, fill_t=-9, line_t=t0 - 1)
    say(c, t, t0 + 0.08, "first", "FIND THE LINE", RD, under=RD)


def S_a2(c, t):
    t0 = SHOT["S_a2"]["start"]; th = TT("a2", "three", 0.4)
    gov_m(c, 500, 1380, t, t0 + 0.05, label="GOV.UK", sign=None, s=0.95)
    hero(c, 140, FLOOR, 0.75, POSES["point_up"], Face("open", "smile", look=(1, -1)), t)
    if t > th - 0.2:
        for i in range(3):
            mtext(c, str(i + 1), 880, 830 + i * 100, 70, BLU, pop_(t, th - 0.2 + i * 0.15), "pm")
        tagpill_m(c, 860, 1180, "3 THINGS", pop_(t, th + 0.3), RD, 46)
    say(c, t, t0 + 0.08, "the government's site says", "REGISTER IF…", BLU, under=BLU)
    note(c, t, t0 + 0.5, "GOV.UK \"BECOME A CHILDMINDER\" (CHECKED 13 NOV 2026)")


def S_a3(c, t):
    t0 = SHOT["S_a3"]["start"]; t8 = TT("a3", "eight.", 0.5); t2 = TT("a3", "two", 0.4); tp = TT("a3", "paid.", 0.5)
    box3(c, 200, 1010, t, t0 + 0.05, "UNDER 8", tick_t=t8)
    mtext(c, "8", 175, 1065, 150, BLU, pr(t, t0 + 0.2, 0.3), "pm")
    arrow_m(c, (275, 930), (275, 1110), pr(t, t0 + 0.4, 0.3), BLU, 7)
    box3(c, 520, 1010, t, t2 - 0.6, "OVER 2 H", tick_t=t2 + 0.6)
    clock_m(c, 520, 1010, t, t2 - 0.5, r=105, fill_t=t2 - 0.3)
    box3(c, 840, 1010, t, tp - 0.7, "PAID", tick_t=tp)
    cash_m(c, 840, 1010, t, tp - 0.6, 0.72, "£", tilt=-6)
    say(c, t, t0 + 0.08, "under eight · over two hours a day", "AND PAID", GR, under=GR)
    note(c, t, t0 + 0.4, "GOV.UK: ALL THREE → REGISTER · \"MORE THAN 2 HOURS A DAY\"")


def S_a4(c, t):
    t0 = SHOT["S_a4"]["start"]; tg = TT("a4", "groceries", 0.3); tc = TT("a4", "counts.", 0.4)
    box3(c, 540, 1060, t, t0 - 3, "PAID", tick_t=tc - 0.2, w=440, h=440)
    if t < tg - 0.1: cash_m(c, 540, 1060, t, t0 - 3, 1.0, "£", tilt=-6)
    else:
        u = pr(t, tg - 0.1, 0.3)
        if u < 1: cash_m(c, 540 - 400 * eio(u), 1060, t, t0 - 3, 1.0 - 0.5 * u, "£", tilt=-6 - 20 * u)
        bag_m(c, 540, 1080, t, tg, "FOOD", GR, 0.9)
    say(c, t, t0 + 0.08, "paid in groceries?", "STILL COUNTS", GR, under=GR)
    note(c, t, t0 + 0.4, "GOV.UK: \"INCLUDING PAYMENT IN KIND\"")


def S_a5(c, t):
    t0 = SHOT["S_a5"]["start"]; te = TT("a5", "Evening", 0.3); ts = TT("a5", "swapping", 0.3)
    mtext(c, "?", 540, 1100, 200, LIGHT, pr(t, t0 + 0.1, 0.3) * (1 - pr(t, te - 0.4, 0.3)), "pm")
    if t > te - 0.3:
        moon_m(c, 140, 840, 50, pr(t, te - 0.3, 0.3))
        house_m(c, 290, 1220, 1.2, t, te - 0.3, BLU)
        mtext(c, "6PM–2AM", 290, 1330, 52, BLU, pr(t, te + 0.2, 0.3), "pm")
        mtext(c, "AT THEIR HOME", 290, 1400, 38, MK, pr(t, te + 0.4, 0.3), "kb")
        if t > te + 0.9: tick(c, 430, 900, pr(t, te + 0.9, 0.3), GR, 1.4)
    if t > ts - 0.3:
        two_houses(c, 770, 1220, t, ts - 0.3, 0.85)
        mtext(c, "SWAP", 770, 1330, 52, OR, pr(t, ts + 0.1, 0.3), "pm")
        mtext(c, "NO MONEY", 770, 1400, 38, MK, pr(t, ts + 0.3, 0.3), "kb")
        if t > ts + 0.7: tick(c, 930, 900, pr(t, ts + 0.7, 0.3), GR, 1.4)
    say(c, t, t0 + 0.08, "what doesn't count?", "NOT THESE", GR, under=GR)
    note(c, t, t0 + 0.4, "GOV.UK CHILDCARE REGISTRATION EXEMPTIONS (22 OCT 2026)")


def S_a6(c, t):
    t0 = SHOT["S_a6"]["start"]; tf = TT("a6", "friend's", 0.4); t3 = TT("a6", "three", 0.3)
    hero(c, 150, FLOOR, 0.8, POSES["wave"], Face("open", "smile", look=(1, 0)), t)
    girl(c, 300, FLOOR, 0.8, POSES["wave"], Face("open", "smile", look=(-1, 0)), t, flip=True, dress=PU)
    if t > tf: tagpill_m(c, 230, 860, "FRIENDS", pop_(t, tf), PU, 46)
    hourbar_m(c, 720, 1000, t, t0 + 0.1, 3, fill_t=t0 + 0.4, step=0.35, cell=110, line_at=2 if t < t3 - 0.1 else 3, line_t=t0 + 0.5)
    if t > t3 - 0.1:
        mtext(c, "UNDER 3 H", 720, 1330, 70, PU, pr(t, t3 - 0.1, 0.35), "pm")
    say(c, t, t0 + 0.08, "minding a friend's kids?", "UNDER 3 HOURS", PU, under=PU)
    note(c, t, t0 + 0.4, "GOV.UK: A FRIEND'S KIDS, PAID, \"LESS THAN 3 HOURS A DAY\"")


def S_b1(c, t):
    t0 = SHOT["S_b1"]["start"]; tr_ = TT("b1", "register.", 0.4); ta = TT("b1", "agency.", 0.3)
    home_m(c, 270, HY, 1.9, t, t0 - 3, "THE LINE", "REGISTERED", tr_, fill_t=-9)
    gov_m(c, 790, 1260, t, t0 + 0.2, label="OFSTED", sign=None, s=0.8)
    if t > ta - 0.3: tagpill_m(c, 770, 1380, "OR AN AGENCY", pop_(t, ta - 0.3), BLU, 40)
    say(c, t, t0 + 0.08, "step two", "REGISTER", BLU, under=BLU)


def S_b2(c, t):
    t0 = SHOT["S_b2"]["start"]; t35 = TT("b2", "thirty-five", 0.3); to = TT("b2", "older", 0.3); t103 = TT("b2", "hundred", 0.3)
    kid_m(c, 140, 1080, 0.55, t, girl_=True, col=PINK); kid_m(c, 250, 1080, 0.62, t, col=TEALK)
    mtext(c, "ANY KID 5 OR UNDER", 300, 1140, 38, MK, pr(t, t0 + 0.2, 0.3), "kb")
    pricetag_m(c, 760, 1000, "£35 A YEAR", pop_(t, t35 - 0.2), GR, -5, 64)
    if t > to - 0.3:
        kid_m(c, 140, 1380, 0.78, t, col=BLU); kid_m(c, 260, 1380, 0.82, t, girl_=True, col=PU)
        mtext(c, "ONLY OLDER KIDS", 300, 1440, 38, MK, pr(t, to - 0.3, 0.3), "kb")
    pricetag_m(c, 760, 1300, "£103 A YEAR", pop_(t, t103 - 0.2), OR, 4, 64)
    say(c, t, t0 + 0.08, "ofsted's yearly fee depends on ages", "£35 OR £103", GR, under=GR)
    note(c, t, t0 + 0.4, "GOV.UK FEES (OCT 2026): £35 EARLY YEARS · £103 IF ONLY 5+ · YEARLY")


def S_c1(c, t):
    t0 = SHOT["S_c1"]["start"]
    home_m(c, HX, HY, 2.7, t, t0 - 3, "REGISTERED", "CHECKED", t0 + 0.4, fill_t=-9)
    u = pr(t, t0 + 0.2, max(0.6, L1("c1") - t0 - 0.2))
    magnifier_m(c, 300 + 480 * eio(u), 1000 - 120 * math.sin(math.pi * u), 90, pr(t, t0 + 0.2, 0.3), BLU)
    say(c, t, t0 + 0.08, "step three · the checks", "NOT ONLY YOU", RD, under=RD)


def _cutaway(c, t, t0):
    """the house cut open: a big outline with the hero + a taller housemate inside"""
    pts = [(120, 1440), (120, 980), (540, 760), (960, 980), (960, 1440)]
    ink(c, [wob(pts, 701, 1.0), wob([(120, 1440), (960, 1440)], 702, 0.6)], pr(t, t0, 0.5), MK, 8)


def S_c2(c, t):
    t0 = SHOT["S_c2"]["start"]; td = TT("c2", "detailed", 0.3); ts = TT("c2", "sixteen", 0.3)
    _cutaway(c, t, t0 - 3)
    hero(c, 340, 1440, 0.8, POSES["hold"], Face("open", "smile", look=(1, 0)), t)
    if t > td - 0.2:
        card_m(c, 340, 1050, 170, pop_(t, td - 0.2), GR, -5)
        mtext(c, "CHECKED", 340, 970, 36, GR, pr(t, td, 0.3), "pm")
    if t > ts - 0.5:
        extra(c, 720, 1440, 0.92, POSES["stand"], Face("open", "flat", look=(-1, 0)), t, scarf=BLU)
        mtext(c, "16+", 720, 960, 64, BLU, pop_(t, ts - 0.2), "pm")
        if t > ts + 0.4: card_m(c, 720, 1050, 170, pop_(t, ts + 0.4), GR, 5)
    say(c, t, t0 + 0.08, "the most detailed criminal record check", "YOU + ANYONE 16+", RD, under=RD, size=140)
    note(c, t, t0 + 0.4, "GOV.UK: ENHANCED DBS + BARRED LISTS · ANYONE 16+ LIVING OR WORKING THERE")


def S_c3(c, t):
    t0 = SHOT["S_c3"]["start"]; tt_ = TT("c3", "teenager", 0.3); th = TT("c3", "Honestly?", 0.3)
    _cutaway(c, t, t0 - 3)
    hero(c, 340, 1440, 0.8, POSES["shock"] if tt_ < t < th else POSES["shrug"] if t >= th else POSES["hold"],
         Face("open", "o" if tt_ < t < th else "smile", look=(1, -1) if t < th else (0, 0)), t)
    extra(c, 720, 1440, 0.92, POSES["stand"], Face("open", "flat", look=(-1, 0)), t, scarf=BLU)
    if t > tt_ - 0.2:   # headphones = a teenager
        k = pr(t, tt_ - 0.2, 0.3); hy = 1440 - 330 * 0.92
        c.drawArc(R.MakeXYWH(720 - 56, hy - 34, 112, 100), 180, 180, False, stroke(MK, 9, k))
        c.drawRoundRect(R.MakeXYWH(720 - 68, hy + 10, 24, 38), 8, 8, paint(RD, k)); c.drawRoundRect(R.MakeXYWH(720 + 44, hy + 10, 24, 38), 8, 8, paint(RD, k))
        mtext(c, "TEENAGER", 720, 960, 50, BLU, k, "pm")
        card_m(c, 720, 1050, 150, pop_(t, tt_ + 0.4), GR, 5)
    if t > tt_ + 0.3: mtext(c, "?!", 420, 1000, 90, RD, pop_(t, tt_ + 0.3), "pm")
    if t > th - 0.2: tagpill_m(c, 540, 860, "EASY TO MISS", pop_(t, th - 0.2), RD, 48)
    say(c, t, t0 + 0.08, "got a teenager at home?", "THEM TOO", RD, under=RD)


def S_c4(c, t):
    t0 = SHOT["S_c4"]["start"]; tf = TT("c4", "forty-one", 0.3)
    card_m(c, 540, 1120, 420, pr(t, t0 + 0.05, 0.3), GR, -4)
    mtext(c, "ENHANCED DBS", 540, 1340, 54, MK, pr(t, t0 + 0.3, 0.3), "pm")
    pricetag_m(c, 300, 880, "£49.50", pop_(t, t0 + 0.3), LIGHT, -8, 56, strike_t=tf - 0.3, t=t)
    pricetag_m(c, 740, 870, "£41", pop_(t, tf - 0.1), GR, 6, 84)
    say(c, t, t0 + 0.08, "since october, each check", "£41", GR, under=GR)
    note(c, t, t0 + 0.4, "DBS FEES FROM 5 OCT 2026 (GOV.UK) · ENHANCED £41, WAS £49.50")


def S_c5(c, t):
    t0 = SHOT["S_c5"]["start"]; tf = TT("c5", "twelve-hour", 0.3); th = TT("c5", "health", 0.3); ti = TT("c5", "insurance.", 0.3)
    firstaid_m(c, 210, 1080, t, tf - 0.3, 0.9, GR, None)
    mtext(c, "12 HOURS", 210, 1250, 50, GR, pr(t, tf, 0.3), "pm")
    mtext(c, "FIRST AID", 210, 1310, 36, MK, pr(t, tf + 0.2, 0.3), "kb")
    healthform_m(c, 520, 1060, t, th - 0.3, 0.8, sign_t=th + 0.6, label="GP FORM")
    shield_m(c, 830, 1060, t, ti - 0.4, 0.95, BLU, "INSURANCE")
    say(c, t, t0 + 0.08, "you'll also need", "FIRST AID · FORM · COVER", MK, under=BLU, size=130)
    note(c, t, t0 + 0.4, "EYFS (SEP 2026): 12 H PAEDIATRIC FIRST AID · INSURANCE · GOV.UK: GP FORM")


def S_d1(c, t):
    t0 = SHOT["S_d1"]["start"]
    home_m(c, HX, HY, 2.7, t, t0 - 3, "CHECKED", "MAX 6", t0 + 0.35, fill_t=-9)
    say(c, t, t0 + 0.08, "last step", "COUNT HEADS", RD, under=RD)


KX = [140, 290, 440, 600, 750, 900]


def _six(c, t, t0, young_t=None, baby_t=None, own_t=None):
    for i, x in enumerate(KX):
        tk = t0 + i * 0.12
        if t < tk: continue
        if i == 5 and baby_t is not None and t > baby_t:
            baby_m(c, x, 1400, 0.9, t, baby_t); continue
        young = young_t is not None and t > young_t + i * 0.1 and i in (3, 4, 5)
        s = 0.55 if young else 0.72
        kid_m(c, x, 1420, s * pop_(t, tk), t, girl_=(i % 2 == 1), col=[BLU, PINK, TEALK, PU, GR, OR][i],
              hat=YELK if young else None, scarf=(own_t is not None and t > own_t + i * 0.12 and i in (0, 1)))


def S_d2(c, t):
    t0 = SHOT["S_d2"]["start"]; ts = TT("d2", "Six", 0.3); tth = TT("d2", "three", 0.3); to = TT("d2", "one", 0.3)
    _six(c, t, ts - 0.4, young_t=tth - 0.3, baby_t=to - 0.2)
    mtext(c, "6", 300, 930, 160, RD, pr(t, ts, 0.3), "pm")
    if t > tth:
        ink(c, [[(530, 1010), (530, 970), (990, 970), (990, 1010)]], pr(t, tth, 0.3), PU, 6, pen_=False)
        mtext(c, "3 YOUNG", 760, 935, 44, PU, pr(t, tth + 0.1, 0.3), "pm")
    if t > to: mtext(c, "1 BABY", 900, 1250, 40, PINK, pr(t, to, 0.3), "pm")
    say(c, t, t0 + 0.08, "under-eights", "SIX AT MOST", RD, under=RD)
    note(c, t, t0 + 0.4, "EYFS 3.50–3.51: 6 UNDER 8 · 3 UP TO RECEPTION AGE · 1 UNDER 1")


def S_d3(c, t):
    t0 = SHOT["S_d3"]["start"]; to = TT("d3", "own", 0.3)
    _six(c, t, t0 - 9, young_t=t0 - 9, baby_t=t0 - 9, own_t=to - 0.2)
    mtext(c, "6", 300, 930, 160, RD, 1, "pm")
    if t > to + 0.4:
        ink(c, [wob(circ_pts(215, 1290, 160, -160, 200, 36, ry=170), 711, 1.0)], pr(t, to + 0.4, 0.4), OR, 7, pen_=False)
        mtext(c, "YOURS", 215, 1070, 54, OR, pr(t, to + 0.5, 0.3), "pm")
        mtext(c, "4 LEFT", 750, 1060, 64, GR, pr(t, to + 0.9, 0.3), "pm")
    say(c, t, t0 + 0.08, "your own under-eights", "COUNT TOO", OR, under=OR)


def S_e1(c, t):
    t0 = SHOT["S_e1"]["start"]; tl = TT("e1", "later.", 0.4)
    tagpill_m(c, 250, 1000, "START", pop_(t, t0 + 0.35), GR, 86)
    if t > t0 + 0.6: arrow_m(c, (400, 1000), (520, 1000), pr(t, t0 + 0.6, 0.3), MK, 9)
    tagpill_m(c, 760, 1000, "REGISTER", pop_(t, t0 + 0.8), BLU, 86)
    hero(c, 160, FLOOR, 0.8, POSES["shrug"], Face("open", "smile", look=(1, -1)), t)
    if t > tl - 0.1:
        cross(c, 140, 920, 940, 1080, pr(t, tl - 0.1, 0.25), RD, 14, 5)
        mtext(c, "REGISTER FIRST", 540, 1290, 80, RD, pr(t, tl + 0.4, 0.4), "pm")
    say(c, t, t0 + 0.08, "the mistake to avoid", "START FIRST", RD, under=RD)


def S_e2(c, t):
    t0 = SHOT["S_e2"]["start"]; tn = TT("e2", "notice", 0.3); tk = TT("e2", "Keep", 0.3); tc = TT("e2", "criminal", 0.3); tfi = TT("e2", "fine.", 0.3)
    notice_m(c, 560, 960, t, tn - 0.4, 1.0, "OFSTED NOTICE", "STOP")
    if t > tk - 0.2:
        hero(c, 160, FLOOR, 0.8, POSES["hold"], Face("open", "flat", look=(1, -1)), t)
        mtext(c, "STILL MINDING", 380, 1150, 40, MK, pr(t, tk - 0.2, 0.3), "kb")
    if t > tc - 0.2: stamp_m(c, 640, 1260, "OFFENCE", pr(t, tc - 0.2, 0.22), col=RD, tilt=-8, size=80)
    if t > tfi - 0.2: pricetag_m(c, 800, 1400, "+ FINE", pop_(t, tfi - 0.2), RD, 6, 56)
    say(c, t, t0 + 0.08, "ofsted's notice to stop · keep going?", "CRIMINAL OFFENCE", RD, under=RD, size=150)
    note(c, t, t0 + 0.4, "CHILDCARE ACT 2006 S.33: ENFORCEMENT NOTICE, THEN AN OFFENCE + FINE")


def S_e3(c, t):
    t0 = SHOT["S_e3"]["start"]; tcl = TT("e3", "closed", 0.3)
    def scr(c_, cx, cy, *_):
        mtext(c_, "£600", cx, cy - 20, 110, GR, 1, "pm"); mtext(c_, "GRANT!", cx, cy + 70, 64, OR, 1, "pm")
    phone_m(c, 540, 1080, t, t0 + 0.05, 1.2, screen=scr)
    if t > tcl - 0.2:
        cross(c, 360, 860, 720, 1300, pr(t, tcl - 0.2, 0.25), RD, 14, 6)
        stamp_m(c, 520, 1390, "CLOSED 31 MAR 2025", pr(t, tcl, 0.22), col=RD, tilt=-5, size=58)
    say(c, t, t0 + 0.08, "that £600 grant in older videos?", "CLOSED", RD, under=RD)
    note(c, t, t0 + 0.4, "GOV.UK START-UP GRANT: RAN 30 NOV 2023 – 31 MAR 2025")


def S_f2(c, t):
    t0 = SHOT["S_f2"]["start"]; ts = TT("f2", "state", 0.3); ty = TT("f2", "yours.", 0.3)
    us_m(c, 520, 1000, 400, pr(t, t0 + 0.05, 0.6), BLU, "")
    if t > ts - 0.2:
        for i, (dx, dy, col) in enumerate([(-250, -60, OR), (-60, -30, GR), (120, 20, PU), (250, -80, RD), (-160, 60, YELK)]):
            spot(c, 520 + dx, 1000 + dy, 32, col, pr(t, ts - 0.2 + i * 0.12, 0.25), seed=i)
    if t > ty - 0.6: searchbar_m(c, 500, 1330, 800, t, ty - 0.6, "your state + child care licensing")
    say(c, t, t0 + 0.08, "watching from america?", "STATE BY STATE", BLU, under=BLU)
    note(c, t, t0 + 0.4, "CHILDCARE.GOV: LICENSING RULES VARY BY STATE AND TERRITORY")


def S_t1(c, t):
    t0 = SHOT["S_t1"]["start"]; ta = TT("t1", "hours.", 0.3); tw2 = TT("t1", "Two", 0.3)
    home_m(c, 220, HY, 1.6, t, t0 - 3, "MAX 6", fill_t=-9)
    hourbar_m(c, 690, 980, t, t0 + 0.15, 3, fill_t=ta - 0.6, step=0.35, cell=120, line_at=2, line_t=tw2)
    if t > tw2 + 0.2: mtext(c, "2 A DAY", 690, 1300, 80, RD, pr(t, tw2 + 0.2, 0.35), "pm")
    say(c, t, t0 + 0.08, "before you say yes", "ADD UP THE HOURS", RD, under=RD, size=150)


def S_end(c, t):
    t0 = SHOT["S_end"]["start"]; tz2 = L0("z2"); tst = TT("z1", "strict,", 0.4); tfa = TT("z1", "fair?", 0.4)
    home_m(c, HX, 1230, 2.1, t, t0 - 3, "2 HOURS", fill_t=-9, line_t=t0 - 1)
    tagpill_m(c, 290, 1380, "STRICT", pop_(t, tst - 0.2), RD, 56)
    tagpill_m(c, 750, 1380, "FAIR", pop_(t, tfa - 0.2), GR, 56)
    for i, (x, tm) in enumerate(((290, tst), (750, tfa))):
        if t > tm: ink(c, [wob(circ_pts(x, 1370, 160, -150, 215, 40, ry=70), 95 + i, 1.4)], pr(t, tm, 0.35), BLU, 7, pen_=False)
    say(c, t, t0 + 0.08, "save this before you start", "STRICT OR FAIR?", MK, t1=tz2 - 0.3, under=BLU)
    say(c, t, tz2 - 0.25, "send it to the friend who minds other kids", "SAVE THIS", BLU, under=OR)
    note(c, t, t0 + 0.4, "COMMENT ONE WORD · ENGLAND · EDUCATION ONLY, NOT LEGAL ADVICE")


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}
SURF = surface()
IMPACTS = [(TT("i1", "two-hour", 0.6), 0.14, 4), (TT("e2", "criminal", 0.3) - 0.2, 0.14, 5), (TT("e3", "closed", 0.3), 0.12, 4)]
# the STEP MAP: which of the 4 steps we're on, ticked once passed
_MAP = {"S_i4": (-1, ()), "S_a1": (0, ()), "S_a2": (0, ()), "S_a3": (0, ()), "S_a4": (0, ()), "S_a5": (0, ()), "S_a6": (0, ()),
        "S_b1": (1, (0,)), "S_b2": (1, (0,)), "S_c1": (2, (0, 1)), "S_c2": (2, (0, 1)), "S_c3": (2, (0, 1)), "S_c4": (2, (0, 1)), "S_c5": (2, (0, 1)),
        "S_d1": (3, (0, 1, 2)), "S_d2": (3, (0, 1, 2)), "S_d3": (3, (0, 1, 2)), "S_t1": (-1, (0, 1, 2, 3))}
_TOP = {"S_a1": "STEP 1 OF 4", "S_a2": "STEP 1 OF 4", "S_a3": "STEP 1 OF 4", "S_a4": "STEP 1 OF 4", "S_a5": "STEP 1 OF 4", "S_a6": "STEP 1 OF 4",
        "S_b1": "STEP 2 OF 4", "S_b2": "STEP 2 OF 4", "S_c1": "STEP 3 OF 4", "S_c2": "STEP 3 OF 4", "S_c3": "STEP 3 OF 4", "S_c4": "STEP 3 OF 4",
        "S_c5": "STEP 3 OF 4", "S_d1": "STEP 4 OF 4", "S_d2": "STEP 4 OF 4", "S_d3": "STEP 4 OF 4", "S_e1": "THE MISTAKE", "S_e2": "THE MISTAKE",
        "S_e3": "OLD ADVICE", "S_f2": "IN AMERICA", "S_t1": "BEFORE YOU SAY YES"}
BOIL_ON = _os.environ.get("BOIL", "1") != "0"


def topline(sid): return f"HOW TO START · {_TOP[sid]}" if sid in _TOP else "OOPSMYBUSINESS · HOW TO START"


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    set_boil((1 + (n // 3) % 3) if BOIL_ON else 0)
    c = SURF.getCanvas(); c.resetMatrix()
    board_bg(c, tt, seed=SHOTS.index(s) * 3)
    u = pr(tt, s["start"], max(0.5, s["end"] - s["start"])); z = 1.0 + 0.018 * u
    dx = dy = 0.0
    for ti, d, a in IMPACTS:
        if ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83)
    c.save(); c.translate(W / 2 + dx, H * 0.6 + dy); c.scale(z, z); c.translate(-W / 2, -H * 0.6)
    RENDER[sid](c, tt)
    c.restore()
    pill(c, topline(sid))
    if sid in _MAP: stepmap(c, 4, _MAP[sid][0], _MAP[sid][1], min(1, pr(tt, s["start"], 0.3)))
    return to_rgb(SURF).astype(np.float32)


def _eraser(f, prev, p):
    x = int(-200 + (W + 400) * eio(p))
    out = f.copy()
    if x < W: out[:, max(0, x):] = prev[:, max(0, x):]
    x0, x1 = max(0, x - 170), min(W, x + 30)
    if x1 > x0:
        out[:, x0:x1] = out[:, x0:x1] * 0.25 + np.array(BOARD, np.float32) / 255 * 0.75
    bx0, bx1 = max(0, x - 150), min(W, x + 10)
    if bx1 > bx0:
        out[820:1180, bx0:bx1] = np.array((60, 66, 84), np.float32) / 255
        out[1150:1180, bx0:bx1] = np.array((210, 210, 214), np.float32) / 255
    return out


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); dt = t - sh["start"]
    if i > 0 and sh["trans"] == "wipe" and dt < 0.34:
        prv = rs(SHOTS[i - 1]["id"], sh["start"] - 1e-3, n); f = _eraser(f, prv, dt / 0.34)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
