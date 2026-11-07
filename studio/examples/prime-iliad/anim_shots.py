# ================= HOW IT WORKS EP 4: Amazon named its Prime cancel flow 'Iliad' (whiteboard). Held object: TWO DOORS (IN / OUT).
# New drawings: crossed spears, office building, highlighted memo, courthouse, gavel, money bags, quote card, balance scale, envelope,
# mailbox, straight hallway, claim form, the mini DOOR MAP (top band: which door we're in, ticked once it's rebuilt).
# Opening move (new): frame 0 is already a finished picture in motion — a parchment scroll titled CANCEL PRIME with a pulsing red
# '???' and a Greek helmet rocking beside it; the answer ILIAD is written over the ??? on the reveal beat. =================
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

GOLD = (236, 176, 40); LIGHT = (150, 156, 170)


# ---------------------------------------------------------------- new marker props (this episode)
def spears_m(c, x, y, t, t0, s=1.0):
    """two crossed spears (an X with leaf tips)"""
    k = pr(t, t0, 0.5)
    for i, (a, b) in enumerate((((-150, 150), (150, -150)), ((150, 150), (-150, -150)))):
        p0 = (x + a[0] * s, y + a[1] * s); p1 = (x + b[0] * s, y + b[1] * s)
        ink(c, [wob([p0, p1], 140 + i, 0.8)], k, (120, 84, 50), 9, pen_=False)
        if k >= 1:
            ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0]); ca, sa = math.cos(ang), math.sin(ang)
            tip = [(p1[0] + 46 * ca * s, p1[1] + 46 * sa * s), (p1[0] - 14 * sa * s, p1[1] + 14 * ca * s), (p1[0] - 10 * ca * s, p1[1] - 10 * sa * s), (p1[0] + 14 * sa * s, p1[1] - 14 * ca * s)]
            c.drawPath(poly(tip, True), paint(LIGHT)); c.drawPath(poly(tip, True), stroke(MK, 4))


def doormap(c, active, fixed=(False, False), a=1.0):
    """mini map under the pill: two small doors IN / OUT; the active one is coloured, a rebuilt one gets a green tick"""
    if a <= 0: return
    for i, (lab, x) in enumerate((("IN", 470), ("OUT", 610))):
        on = (active == i) or active == 2
        w, h = (46, 64) if on else (38, 54); y = 392
        rr = R.MakeXYWH(x - w / 2, y - h, w, h)
        c.drawRect(rr, paint(WHITE, a)); c.drawRect(rr, paint((BLU if i == 0 else RD), (0.35 if on else 0.0) * a))
        c.drawRect(rr, stroke(MK if on else LIGHT, 5 if on else 3, a)); c.drawCircle(x + w / 2 - 10, y - h / 2, 4, paint(MK if on else LIGHT, a))
        f = font("pm", 30 if on else 24); c.drawString(lab, x + w / 2 + 10, y - 12, f, paint(MK if on else LIGHT, a))
        if fixed[i]: ink(c, [[(x - 16, y - 30), (x - 4, y - 16), (x + 22, y - 50)]], 1, GR, 7, pen_=False)


def office_m(c, x, y, t, t0, label="INSIDE AMAZON"):
    k = pr(t, t0, 0.6); w, h = 420, 520
    body = [(x - w / 2, y), (x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y)]
    ink(c, [wob(body, 151, 0.8)], k, MK, 8)
    for r_ in range(4):
        for q in range(3):
            kk = pr(t, t0 + 0.4 + (r_ * 3 + q) * 0.03, 0.2)
            if kk > 0:
                bx, by = x - w / 2 + 50 + q * 120, y - h + 60 + r_ * 100
                c.drawRect(R.MakeXYWH(bx, by, 80, 60), paint((255, 236, 170), 0.8 * kk)); c.drawRect(R.MakeXYWH(bx, by, 80, 60), stroke(MK, 4, kk))
    mtext(c, label, x, y - h - 30, 52, MK, pr(t, t0 + 0.5, 0.4), "pm")


def memo_m(c, x, y, t, t0, hl_t, quote="\"a bit of a shady world\"", tilt=-3):
    w, h = 640, 380; k = pr(t, t0, 0.5)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt)
    c.drawRect(R.MakeXYWH(-w / 2 + 8, -h / 2 + 12, w, h), paint((0, 0, 0), 0.10 * k, blur=10)); c.drawRect(R.MakeXYWH(-w / 2, -h / 2, w, h), paint(WHITE, k))
    ink(c, [wob([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)], 161, 1.0)], k, MK, 6)
    mtext(c, "INTERNAL", -w / 2 + 40, -h / 2 + 70, 46, LIGHT, pr(t, t0 + 0.3, 0.3), "pm", align="l")
    for i in range(2): ink(c, [[(-w / 2 + 40, -h / 2 + 120 + i * 46), (w / 2 - 60 - i * 90, -h / 2 + 120 + i * 46)]], pr(t, t0 + 0.5 + i * 0.1, 0.25), LIGHT, 7, pen_=False)
    yy = -h / 2 + 250
    if t > hl_t:
        fq = font("kb", 50); wq = tw(fq, quote)
        c.drawRect(R.MakeXYWH(-wq / 2 - 14, yy - 52, (wq + 28) * min(1, pr(t, hl_t, 0.5)), 72), paint((255, 222, 60), 0.8))
    mtext(c, quote, 0, yy, 50, MK, pr(t, t0 + 0.7, 0.6), "kb")
    ink(c, [[(-w / 2 + 40, yy + 70), (w / 2 - 160, yy + 70)]], pr(t, t0 + 0.9, 0.25), LIGHT, 7, pen_=False)
    c.restore()


def court_m(c, x, y, t, t0, label="SEATTLE"):
    k = pr(t, t0, 0.7); w = 560
    roof = [(x - w / 2 - 30, y - 420), (x, y - 560), (x + w / 2 + 30, y - 420), (x - w / 2 - 30, y - 420)]
    steps = [[(x - w / 2 - 40, y), (x + w / 2 + 40, y)], [(x - w / 2 - 20, y - 30), (x + w / 2 + 20, y - 30)]]
    cols = [[(x - w / 2 + 50 + i * 115, y - 30), (x - w / 2 + 50 + i * 115, y - 400)] for i in range(5)]
    beam = [[(x - w / 2 - 10, y - 400), (x + w / 2 + 10, y - 400)]]
    if k > 0.6: hatch(c, _path(roof), pr(k, 0.6, 0.4), GOLD, gap=16, w=6, bbox=(x - w, y - 570, x + w, y - 410), a=0.5)
    ink(c, [wob(roof, 171, 0.8)] + [wob(p, 172 + i, 0.6) for i, p in enumerate(steps + cols + beam)], k, MK, 8)
    mtext(c, label, x, y - 446, 44, MK, pr(t, t0 + 0.6, 0.3), "pm")


def gavel_m(c, x, y, t, t_hit, s=1.0):
    """a gavel that swings down at t_hit (rests raised before)"""
    u = eo(pr(t, t_hit - 0.35, 0.35)); ang = -55 + 55 * u
    c.drawRoundRect(R.MakeXYWH(x - 130, y + 74, 180, 40), 10, 10, paint((150, 100, 60))); c.drawRoundRect(R.MakeXYWH(x - 130, y + 74, 180, 40), 10, 10, stroke(MK, 5))
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-14, -10, 260, 26), 10, 10, paint((150, 100, 60))); c.drawRoundRect(R.MakeXYWH(-14, -10, 260, 26), 10, 10, stroke(MK, 5))
    c.drawRoundRect(R.MakeXYWH(-70, -70, 110, 140), 18, 18, paint((120, 76, 44))); c.drawRoundRect(R.MakeXYWH(-70, -70, 110, 140), 18, 18, stroke(MK, 6))
    c.restore()
    if t > t_hit:
        kb = pr(t, t_hit, 0.3)
        for dx_ in (-1, 1): ink(c, [[(x - 40 + dx_ * 120, y + 80), (x - 40 + dx_ * 170, y + 40)]], kb, MK, 6, pen_=False)


def bag_m(c, x, y, t, t0, text, col=GR, s=1.0, label=None):
    k = pr(t, t0, 0.5)
    body = _sc(x, y, s, [(-90, -150), (-150, -40), (-150, 60), (-100, 120), (100, 120), (150, 60), (150, -40), (90, -150), (-90, -150)])
    neck = _sc(x, y, s, [(-70, -150), (-50, -200), (50, -200), (70, -150)])
    if k > 0.5: hatch(c, _path(body), pr(k, 0.5, 0.5), col, gap=17, w=6, bbox=(x - 160 * s, y - 210 * s, x + 160 * s, y + 130 * s), a=0.45)
    ink(c, [wob(body, 181, 1.0), wob(neck, 182, 0.6)], k, MK, 8)
    mtext(c, text, x, y + 30 * s, int(76 * s), MK, pr(t, t0 + 0.4, 0.3), "pm")
    if label: mtext(c, label, x, y + 200 * s, int(48 * s), col, pr(t, t0 + 0.6, 0.3), "pm")


def heads_m(c, x0, x1, y, t, t0, n=9, col=BLU):
    for i in range(n):
        kk = pop_(t, t0 + i * 0.05)
        if kk <= 0: continue
        hx = x0 + (x1 - x0) * i / (n - 1)
        c.save(); c.translate(hx, y); c.scale(kk, kk)
        c.drawCircle(0, -40, 22, paint(WHITE)); c.drawCircle(0, -40, 22, stroke(MK, 5))
        c.drawPath(_path([(-28, 20), (-22, -10), (22, -10), (28, 20)]), stroke(col, 6)); c.restore()


def quote_m(c, x, y, t, t0, lines_, who):
    w, h = 820, 330; k = pr(t, t0, 0.5)
    if k <= 0: return
    c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), 30, 30, paint(WHITE, k))
    ink(c, [wob([(x - w / 2 + 30, y - h / 2), (x + w / 2 - 30, y - h / 2), (x + w / 2, y - h / 2 + 30), (x + w / 2, y + h / 2 - 30), (x + w / 2 - 30, y + h / 2),
                 (x - w / 2 + 30, y + h / 2), (x - w / 2, y + h / 2 - 30), (x - w / 2, y - h / 2 + 30), (x - w / 2 + 30, y - h / 2)], 191, 0.8)], k, BLU, 7)
    mtext(c, "“", x - w / 2 + 60, y - h / 2 + 110, 120, BLU, k, "pm")
    for i, ln in enumerate(lines_): mtext(c, ln, x + 20, y - 50 + i * 70, 54, MK, pr(t, t0 + 0.2 + i * 0.25, 0.3), "kb")
    mtext(c, who, x, y + h / 2 - 40, 40, BLU, pr(t, t0 + 0.7, 0.3), "pm")


def scale_m(c, x, y, t, t0, tilt=0.0):
    k = pr(t, t0, 0.5)
    ink(c, [wob([(x, y), (x, y - 260)], 201, 0.5), wob([(x - 90, y), (x + 90, y)], 202, 0.5)], k, MK, 8)
    if k < 1: return
    a = math.radians(tilt); L = 200
    lx, ly = x - L * math.cos(a), y - 260 - L * math.sin(a); rx, ry = x + L * math.cos(a), y - 260 + L * math.sin(a)
    c.drawPath(_path([(lx, ly), (rx, ry)]), stroke(MK, 8)); c.drawCircle(x, y - 260, 12, paint(MK))
    for px, py in ((lx, ly), (rx, ry)):
        c.drawPath(_path([(px, py), (px - 60, py + 110)]), stroke(MK, 4)); c.drawPath(_path([(px, py), (px + 60, py + 110)]), stroke(MK, 4))
        c.drawPath(_path(circ_pts(px, py + 110, 70, 0, 180, 16, ry=26)), stroke(MK, 6))


def envelope_m(c, x, y, t, t0, s=1.0, text="$"):
    k = pr(t, t0, 0.4); w, h = 260 * s, 170 * s
    if k <= 0: return
    c.drawRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), paint(WHITE, k))
    ink(c, [wob([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)], 211, 0.6),
            [(x - w / 2, y - h / 2), (x, y + 10 * s), (x + w / 2, y - h / 2)]], k, MK, 6, pen_=False)
    mtext(c, text, x, y + 60 * s, int(56 * s), GR, k, "pm")


def mailbox_m(c, x, y, t, t0, flag=0.0):
    k = pr(t, t0, 0.5)
    box = [(x - 130, y - 300), (x + 130, y - 300), (x + 130, y - 160), (x - 130, y - 160)]
    ink(c, [wob([(x, y), (x, y - 160)], 221, 0.5), wob(box + [box[0]], 222, 0.6), wob(circ_pts(x, y - 300, 130, 180, 360, 18, ry=60), 223, 0.6)], k, MK, 8)
    if k >= 1:
        hatch(c, _path(box + [box[0]]), 1, BLU, gap=18, w=6, bbox=(x - 140, y - 310, x + 140, y - 150), a=0.3)
        a = math.radians(-90 * flag); fx, fy = x + 130, y - 220
        c.drawPath(_path([(fx, fy), (fx + 110 * math.cos(a), fy + 110 * math.sin(a))]), stroke(RD, 10))
        c.drawRect(R.MakeXYWH(fx + 110 * math.cos(a) - 18, fy + 110 * math.sin(a) - 18, 36, 36), paint(RD))


def hallway_m(c, x, y, t, t0, w=300, h=520):
    """the OUT door redrawn as a short straight hallway with EXIT at the end"""
    k = pr(t, t0, 0.6)
    fr = [(x - w / 2, y), (x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y)]
    inner = [(x - 50, y - 180), (x - 50, y - 340), (x + 50, y - 340), (x + 50, y - 180), (x - 50, y - 180)]
    lines_ = [[(x - w / 2, y - h), (x - 50, y - 340)], [(x + w / 2, y - h), (x + 50, y - 340)], [(x - w / 2, y), (x - 50, y - 180)], [(x + w / 2, y), (x + 50, y - 180)]]
    ink(c, [wob(fr, 231, 0.8), wob(inner, 232, 0.5)] + lines_, k, MK, 7)
    if k >= 1:
        c.drawRect(R.MakeXYWH(x - 50, y - 340, 100, 160), paint(GR, 0.3)); mtext(c, "EXIT", x, y - 250, 34, GR, 1, "pm")
        ink(c, [[(x, y - 30), (x, y - 160)], [(x - 22, y - 136), (x, y - 166), (x + 22, y - 136)]], pr(t, t0 + 0.6, 0.3), GR, 8, pen_=False)


def form_m(c, x, y, t, t0, cross_t=None):
    w, h = 260, 320; k = pr(t, t0, 0.4)
    if k <= 0: return
    c.drawRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), paint(WHITE, k))
    ink(c, [wob([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)], 241, 0.6)], k, MK, 6, pen_=False)
    mtext(c, "CLAIM FORM", x, y - h / 2 + 56, 34, MK, k, "pm")
    for i in range(4):
        yy = y - h / 2 + 110 + i * 50
        c.drawRect(R.MakeXYWH(x - w / 2 + 30, yy - 14, 24, 24), stroke(MK, 3, k)); ink(c, [[(x - w / 2 + 70, yy), (x + w / 2 - 30, yy)]], k, LIGHT, 5, pen_=False)
    if cross_t is not None and t > cross_t:
        cross(c, x - w / 2 - 20, y - h / 2 - 20, x + w / 2 + 20, y + h / 2 + 20, pr(t, cross_t, 0.2), RD, 14, 3)
        cross(c, x + w / 2 + 20, y - h / 2 - 20, x - w / 2 - 20, y + h / 2 + 20, pr(t, cross_t + 0.15, 0.2), RD, 14, 4)


def laptop2(c, x, y, t, t0, w=440, h=290, screen=None):
    k = pr(t, t0, 0.5)
    scr = [(x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y), (x - w / 2, y), (x - w / 2, y - h)]
    base = [(x - w / 2 - 50, y + 10), (x + w / 2 + 50, y + 10), (x + w / 2 + 20, y + 44), (x - w / 2 - 20, y + 44), (x - w / 2 - 50, y + 10)]
    c.drawPath(_path(scr), paint(WHITE, k)); ink(c, [wob(scr, 251, 0.8), wob(base, 252, 0.8)], k, MK, 7)
    if screen and k >= 1: screen(c, x, y - h / 2)


# ---------------------------------------------------------------- shots
SHOTLIST = [("S_i1", 0.0, "cut"), ("S_i3", L0("i3") - 0.1, "wipe"), ("S_i4", L0("i4") - 0.1, "wipe"), ("S_a1", L0("a1") - 0.1, "wipe"),
            ("S_a3", L0("a3") - 0.1, "wipe"), ("S_b1", L0("b1") - 0.1, "wipe"), ("S_b3", L0("b3") - 0.1, "wipe"), ("S_c1", L0("c1") - 0.1, "wipe"),
            ("S_d1", L0("d1") - 0.1, "wipe"), ("S_d2", L0("d2") - 0.1, "wipe"), ("S_d3", L0("d3") - 0.1, "wipe"), ("S_e1", L0("e1") - 0.1, "wipe"),
            ("S_e3", L0("e3") - 0.1, "wipe"), ("S_t1", L0("t1") - 0.1, "wipe"), ("S_end", L0("z1") - 0.1, "wipe")]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
DX, DY, DW, DH = 300, 1400, 300, 520     # the two doors: IN at x=300, OUT at x=780, standing on y=1400


def S_i1(c, t):
    """frame 0 is already a picture: an open scroll titled CANCEL PRIME, a pulsing red ???, a rocking helmet; ILIAD lands on the beat"""
    t2 = L0("i2"); tl = TT("i2", "long,", 0.4)
    scroll_m(c, 540, 1000, 720, 470, t, -2.0, [], [])
    mtext(c, "AMAZON'S NAME FOR ITS", 540, 870, 44, LIGHT, 1, "pm"); mtext(c, "PRIME CANCEL PROCESS", 540, 930, 54, MK, 1, "pm")
    if t < t2 - 0.05:
        q = 1 + 0.06 * math.sin(t * 7)
        c.save(); c.translate(540, 1070); c.scale(q, q); mtext(c, "???", 0, 50, 170, RD, 1, "pm"); c.restore()
        if t > 0.2: pen(c, 720 + 20 * math.sin(t * 3), 1050 + 10 * math.cos(t * 4))
    else:
        mtext(c, "ILIAD", 540, 1140, 190, PU, pr(t, t2 - 0.05, 0.45), "pm", pen_=True)
        ink(c, [wob([(330, 1170), (750, 1162)], 9, 1.2)], pr(t, t2 + 0.45, 0.25), PU, 11, pen_=False)
    c.save(); c.translate(170, 1395); c.rotate(6 * math.sin(t * 2.2)); helmet_m(c, 0, 0, t, -2.0, 0.6); c.restore()
    if t > tl - 0.2: spears_m(c, 880, 1360, t, tl - 0.2, 0.5)
    say(c, t, -2.0, "do you know what Amazon's team called", "CANCELLING PRIME?", MK, t1=t2 - 0.3, under=RD, size=140)
    say(c, t, t2 - 0.2, "like Homer's poem about a", "LONG, HARD WAR", RD, under=RD, size=140)
    note(c, t, t2 + 0.5, "FTC COMPLAINT, 21 JUNE 2023, PARAGRAPH 7")


def S_i3(c, t):
    t0 = SHOT["S_i3"]["start"]; to = TT("i3", "out.", 0.5)
    floor_line(c, t, t0)
    def scr(c_, x, y):
        mtext(c_, "PRIME", x, y - 10, 64, BLU, pr(t, t0 + 0.4, 0.3), "pm"); mtext(c_, "every month", x, y + 56, 40, LIGHT, pr(t, t0 + 0.6, 0.3), "kb")
    laptop2(c, 720, 1380, t, t0 + 0.1, screen=scr)
    hero(c, 300, FLOOR, 1.0, POSES["point"] if t > to else POSES["stand"], Face("open", "flat" if t < to else "o", look=(1, 0)), t)
    if t > to - 0.2:
        kb = pop_(t, to - 0.2)
        c.save(); c.translate(360, 960); c.scale(kb, kb)
        c.drawCircle(0, 0, 110, paint(WHITE)); c.drawCircle(0, 0, 110, stroke(MK, 6))
        for j, r_ in enumerate((16, 10)): c.drawCircle(-40 - j * 30, 130 + j * 40, r_, stroke(MK, 5))
        arrow_m(c, (-60, 30), (60, 30), 1, GR, 10); mtext(c, "EXIT", 0, -20, 48, GR, 1, "pm"); c.restore()
    say(c, t, t0 + 0.08, "you pay for Prime, and you want", "OUT", RD, under=RD)
    note(c, t, t0 + 0.6, "US CUSTOMERS · THE FTC'S CASE")


def S_i4(c, t):
    t0 = SHOT["S_i4"]["start"]; t5 = L0("i5"); tf = TT("i5", "fair?", 0.5); tb = TT("i5", "both", 0.3)
    door_m(c, DX, DY, t, t0 + 0.05, DW, DH, label="IN", col=BLU)
    door_m(c, 780, DY, t, t0 + 0.35, DW, DH, label="OUT", col=RD)
    if t > t5 - 0.1:
        if t > tb - 0.2:
            for i, x in enumerate((DX, 780)): cross(c, x - 80, 1080, x + 80, 1180, pr(t, tb + i * 0.2, 0.2), RD, 12, 5 + i)
        if t > tf - 0.2:
            kq = pop_(t, tf - 0.2); c.save(); c.translate(540, 1150); c.scale(kq, kq); mtext(c, "?", 0, 60, 200, RD, 1, "pm"); c.restore()
    say(c, t, t0 + 0.08, "in the end, to settle, Amazon paid", "$2.5 BILLION", GR, t1=t5 - 0.3, under=GR)
    say(c, t, t5 - 0.25, "two doors · the FTC says both", "WORKED AGAINST YOU", RD, under=RD, size=130)
    note(c, t, t0 + 0.6, "FTC SETTLEMENT, 25 SEP 2025", t1=t5)
    note(c, t, t5 + 0.2, "THE FTC'S ALLEGATIONS · AMAZON SETTLED")


def S_a1(c, t):
    t0 = SHOT["S_a1"]["start"]; t2 = L0("a2"); ts = TT("a2", "skip", 0.3); tfr = TT("a2", "free", 0.4)
    door_m(c, 540, 1460, t, t0 + 0.05, 640, 680, col=BLU)
    mtext(c, "CHECKOUT", 540, 880, 56, MK, pr(t, t0 + 0.4, 0.3), "pm")
    button_m(c, 540, 1060, "JOIN PRIME", t, TT("a1", "offered", 0.3) - 0.3, w=500, h=130, col=OR)
    if t > ts - 0.3:
        button_m(c, 540, 1250, "No, I don't want Free Shipping", t, ts - 0.3, small=True)
        if t > tfr + 0.2: ink(c, [wob(circ_pts(540, 1236, 330, -170, 200, 44, ry=62), 55, 1.4)], pr(t, tfr + 0.2, 0.4), RD, 8, pen_=False)
    say(c, t, t0 + 0.08, "door one is", "THE WAY IN", BLU, t1=t2 - 0.3, under=BLU)
    say(c, t, t2 - 0.25, "back then, the button to skip it", "NO FREE SHIPPING?", RD, under=RD, size=140)
    note(c, t, t2 + 0.4, "THE 2025 ORDER BANS THIS WORDING · FTC")


def S_a3(c, t):
    t0 = SHOT["S_a3"]["start"]; tm = TT("a3", "meaning", 0.4)
    door_m(c, 840, DY, t, t0 - 1, DW, DH, label="IN", col=BLU, open_=0.8)
    for i in range(4):
        x = 110 + i * 150 + 110 * min(1.0, (t - t0) * 0.35)
        extra(c, x, FLOOR - 20, 0.72, POSES["stand"], Face("open", "flat", look=(1, 0)), t + i * 0.3, scarf=(120, 128, 146))
        if t > tm - 0.2 + i * 0.12:
            kq = pop_(t, tm - 0.2 + i * 0.12); c.save(); c.translate(x, 1050); c.scale(kq, kq); mtext(c, "?", 0, 0, 90, RD, 1, "pm"); c.restore()
    say(c, t, t0 + 0.08, "the FTC alleged plenty", "JOINED BY ACCIDENT", RD, under=RD, size=140)
    note(c, t, t0 + 0.6, "ALLEGED, NOT PROVEN · AMAZON SETTLED")


def S_b1(c, t):
    t0 = SHOT["S_b1"]["start"]; t2 = L0("b2"); tp = TT("b2", "four", 0.3); tc = TT("b2", "six", 0.3); to = TT("b2", "fifteen", 0.3)
    if t < t2:
        door_m(c, 260, 1460, t, t0 - 1, 300, 520, label="OUT", col=RD, open_=pr(t, t0 + 0.2, 0.5))
        maze_m(c, 700, 1180, t, t0 + 0.3, size=440, n=6)
    else:
        maze_m(c, 540, 1200, t, t0 - 5, size=560, n=7, seed=9)
        for i, (lab, tm, col) in enumerate((("4 PAGES", tp, BLU), ("6 CLICKS", tc, OR), ("15 OPTIONS", to, RD))):
            if t > tm - 0.2:
                kk = pop_(t, tm - 0.2); x = 210 + i * 300
                c.save(); c.translate(x, 840); c.scale(kk, kk)
                c.drawRoundRect(R.MakeXYWH(-138, -60, 276, 100), 20, 20, paint(WHITE)); c.drawRoundRect(R.MakeXYWH(-138, -60, 276, 100), 20, 20, stroke(col, 7))
                mtext(c, lab, 0, 12, 46, col, 1, "pm"); c.restore()
    say(c, t, t0 + 0.08, "door two · the complaint calls it", "LABYRINTHINE", RD, t1=t2 - 0.3, under=RD, size=140)
    say(c, t, t2 - 0.25, "on a computer, back then", "JUST TO LEAVE", MK, under=RD)
    note(c, t, t2 + 0.3, "FTC COMPLAINT, PARAGRAPH 113 · DESKTOP, BEFORE APRIL 2023")


def S_b3(c, t):
    t0 = SHOT["S_b3"]["start"]
    ts_ = t0 + 0.6; te = ts_ + (t - ts_) / 5.0 if t > ts_ else t   # the way out draws on slowly, across the whole line
    maze_m(c, 600, 1140, te, t0 - 5, size=600, n=7, seed=9, solve_t=ts_)
    hx = 150
    hero(c, hx, 1480, 0.75, POSES["shrug"], Face("open", "flat", look=(1, -1)), t)
    helmet_m(c, hx, 1255, t, t0 + 0.2, 0.4)
    say(c, t, t0 + 0.08, "six clicks isn't a war, but it's", "A MAZE", MK, under=RD)


def S_c1(c, t):
    t0 = SHOT["S_c1"]["start"]; t2 = L0("c2"); ts = TT("c2", "shady", 0.3)
    if t < t2 + 0.6: office_m(c, 540, 1460, t, t0 + 0.05)
    if t > t2 - 0.1:
        u = eo(pr(t, t2 - 0.1, 0.6))
        memo_m(c, 540, 1500 - 380 * u, t, t2 - 0.1, ts - 0.1)
    say(c, t, t0 + 0.08, "did anyone inside notice?", "THE FTC SAYS YES", MK, t1=t2 - 0.3, under=BLU, size=140)
    say(c, t, t2 - 0.25, "the FTC quotes one internal comment", "SHADY WORLD", RD, under=RD)
    note(c, t, t2 + 0.4, "QUOTED BY THE FTC, 25 SEP 2025")


def S_d1(c, t):
    t0 = SHOT["S_d1"]["start"]; ts = TT("d1", "settled.", 0.4)
    court_m(c, 400, 1470, t, t0 + 0.05)
    mtext(c, "SEP 2025", 800, 960, 56, MK, pr(t, t0 + 0.6, 0.3), "pm")
    gavel_m(c, 830, 1300, t, ts)
    if t > ts: stamp_m(c, 540, 1180, "SETTLED", pr(t, ts, 0.22), col=RD, tilt=-8, size=96)
    say(c, t, t0 + 0.08, "a trial in Seattle · days in, it", "SETTLED", RD, under=RD)
    note(c, t, t0 + 0.6, "US DISTRICT COURT, WESTERN DISTRICT OF WASHINGTON · SEP 2025")


def S_d2(c, t):
    t0 = SHOT["S_d2"]["start"]; tb = TT("d2", "back", 0.3)
    bag_m(c, 290, 1150, t, t0 + 0.1, "$1B", RD, 1.0, "PENALTY")
    bag_m(c, 760, 1130, t, TT("d2", "another", 0.2) - 0.2, "$1.5B", GR, 1.1, None)
    if t > tb - 0.2:
        heads_m(c, 600, 940, 1440, t, tb - 0.2, n=6, col=GR)
    say(c, t, t0 + 0.08, "a billion-dollar penalty, and", "$1.5B BACK", GR, under=GR)
    note(c, t, tb + 0.2, "TO ABOUT 35 MILLION CUSTOMERS · FTC")


def S_d3(c, t):
    t0 = SHOT["S_d3"]["start"]; ta = TT("d3", "says", 0.2); td = TT("d3", "didn't", 0.4)
    if t < ta - 0.3:
        mtext(c, "ADMIT?", 300, 1150, 100, MK, pr(t, t0 + 0.1, 0.3), "pm"); mtext(c, "DENY?", 760, 1150, 100, MK, pr(t, t0 + 0.3, 0.3), "pm")
        for i, x in enumerate((300, 760)): cross(c, x - 160, 1090, x + 160, 1130, pr(t, td + 0.2 + i * 0.25, 0.2), RD, 12, 7 + i)
    else:
        quote_m(c, 540, 1000, t, ta - 0.3, ["Amazon and our executives", "have always followed the law"], "AMAZON, 25 SEP 2025")
        scale_m(c, 540, 1470, t, ta + 0.6, tilt=8 * math.sin((t - ta) * 2) * max(0, 1 - (t - ta) / 3))
    say(c, t, t0 + 0.08, "Amazon didn't admit or deny", "THE CLAIMS", MK, t1=ta - 0.4, under=BLU)
    say(c, t, ta - 0.35, "it says it has always", "FOLLOWED THE LAW", BLU, under=BLU, size=140)
    note(c, t, t0 + 0.6, "STIPULATED ORDER: NEITHER ADMITS NOR DENIES THE ALLEGATIONS")


def S_e1(c, t):
    t0 = SHOT["S_e1"]["start"]; t2 = L0("e2"); tc = TT("e1", "clear", 0.3)
    door_m(c, DX, DY, t, t0 + 0.05, DW, DH, label="IN", col=BLU)
    button_m(c, DX, 1060, "JOIN", t, t0 + 0.4, w=230, h=90, col=OR, glow=False)
    if t > tc - 0.3: button_m(c, DX, 1200, "NO", t, tc - 0.3, w=230, h=90, col=(170, 178, 192), glow=False)
    if t > t2 - 0.1:
        hallway_m(c, 780, DY, t, t2 - 0.1, DW, DH); mtext(c, "OUT", 780, DY - DH - 30, 70, MK, pr(t, t2, 0.3), "pm")
        km = pr(t, TT("e2", "same", 0.3), 0.3); mtext(c, "=", 540, 1220, 160, GR, km, "pm")
    say(c, t, t0 + 0.08, "saying no now needs", "A CLEAR BUTTON", BLU, t1=t2 - 0.3, under=BLU, size=140)
    say(c, t, t2 - 0.25, "leaving works the same way as", "JOINING", GR, under=GR)
    note(c, t, t0 + 0.5, "2025 ORDER: A CLEAR WAY TO DECLINE", t1=t2 + 0.2)
    note(c, t, t2 + 0.3, "2025 ORDER: CANCEL BY THE SAME METHOD YOU SIGNED UP")


def S_e3(c, t):
    t0 = SHOT["S_e3"]["start"]; t4 = L0("e4"); tt_ = TT("e3", "two", 0.3); ta = TT("e4", "automatic.", 0.3); tf = TT("e4", "form", 0.3)
    if t < t4 - 0.1:
        u = min(1.0, (t - t0) * 0.6)
        envelope_m(c, 260 + 60 * u, 1300 - 120 * math.sin(math.pi * u), t, t0 + 0.1)
        mtext(c, "$51", 760, 1100, 110, MK, pr(t, t0 + 0.4, 0.3), "pm")
        if t > tt_ - 0.4: cross(c, 670, 1040, 850, 1080, pr(t, tt_ - 0.4, 0.2), RD, 12, 8)
        if t > tt_ - 0.2: mtext(c, "$200", 760, 1270, 130, GR, pr(t, tt_ - 0.2, 0.3), "pm"); mtext(c, "TOTAL CAP", 760, 1350, 46, GR, pr(t, tt_ + 0.1, 0.3), "kb")
    else:
        mailbox_m(c, 300, 1480, t, t4 - 0.2, flag=pr(t, ta, 0.3))
        envelope_m(c, 300, 1100 + 60 * eo(pr(t, t4 - 0.1, 0.5)), t, t4 - 0.2, 0.7)
        form_m(c, 770, 1170, t, t4, cross_t=tf)
    say(c, t, t0 + 0.08, "payments still going out · some get", "UP TO $200", GR, t1=t4 - 0.3, under=GR)
    say(c, t, t4 - 0.25, "the new payments are", "AUTOMATIC", GR, under=GR)
    note(c, t, t0 + 0.6, "TOTAL CAP FOR ELIGIBLE US CUSTOMERS · FTC, 17 SEP 2026", t1=t4)
    note(c, t, t4 + 0.3, "NO CLAIM NEEDED · REFUNDS THROUGH APRIL 2027 · FTC")


def S_t1(c, t):
    t0 = SHOT["S_t1"]["start"]; ts = TT("t1", "scam.", 0.3)
    def scr(c_, x, y, w, h): c_.drawRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), paint((255, 240, 236)))
    phone_m(c, 540, 1180, t, t0 + 0.05, 1.0, screen=scr, buzz_t=t0 + 0.4, caller="\"FTC\"")
    if t > ts - 0.2: stamp_m(c, 540, 1200, "LIKELY A SCAM", pr(t, ts - 0.2, 0.22), col=RD, tilt=-10, size=84)
    say(c, t, t0 + 0.08, "someone claiming to be the FTC?", "LIKELY A SCAM", RD, under=RD)
    note(c, t, t0 + 0.6, "FTC: IF SOMEONE CLAIMS TO BE WITH THE FTC, IT IS LIKELY A SCAM")


def S_end(c, t):
    t0 = SHOT["S_end"]["start"]; tz2 = L0("z2"); ty = TT("z1", "yes", 0.4)
    door_m(c, DX, DY, t, t0 + 0.05, DW, DH, col=BLU)
    hallway_m(c, 780, DY, t, t0 + 0.2, DW, DH)
    mtext(c, "=", 540, 1220, 160, GR, pr(t, t0 + 0.6, 0.3), "pm")
    for i, (word, col, x) in enumerate((("YES", GR, 330), ("NO", RD, 750))):
        mtext(c, word, x, 830, 90, col, pr(t, ty - 0.1 + i * 0.3, 0.3), "pm")
        ink(c, [wob(circ_pts(x, 800, 120, -120, 245, 40, ry=62), 95 + i, 1.4)], pr(t, ty + 0.2 + i * 0.3, 0.35), col, 8, pen_=False)
    say(c, t, t0 + 0.08, "cancel as easy as joining, by law?", "YES OR NO?", MK, t1=tz2 - 0.3, under=BLU)
    say(c, t, tz2 - 0.25, "send it to the friend who forgot a subscription", "SAVE THIS", BLU, under=OR)
    note(c, t, t0 + 0.6, "COMMENT ONE WORD · EDUCATION ONLY · UK RULES PLANNED FOR 2027")


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}
SURF = surface()
IMPACTS = [(TT("i4", "two", 0.3), 0.12, 4), (TT("d1", "settled.", 0.4), 0.16, 6), (TT("t1", "scam.", 0.3) - 0.2, 0.14, 5)]
# the mini DOOR MAP (story upgrade, 8 Nov): which door the viewer is in, ticked once the order rebuilt it
_MAP = {"S_i4": (2, (False, False)), "S_a1": (0, (False, False)), "S_a3": (0, (False, False)), "S_b1": (1, (False, False)), "S_b3": (1, (False, False)),
        "S_e1": (2, (True, True)), "S_end": (2, (True, True))}
_TOP = {"S_a1": "DOOR 1 · THE WAY IN", "S_a3": "DOOR 1 · THE WAY IN", "S_b1": "DOOR 2 · THE WAY OUT", "S_b3": "DOOR 2 · THE WAY OUT", "S_e1": "BOTH DOORS · REBUILT"}


def topline(sid): return f"HOW IT WORKS · {_TOP[sid]}" if sid in _TOP else "OOPSMYBUSINESS · HOW IT WORKS"


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
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
    if sid in _MAP: doormap(c, _MAP[sid][0], _MAP[sid][1], min(1, pr(tt, s["start"], 0.3)))
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
