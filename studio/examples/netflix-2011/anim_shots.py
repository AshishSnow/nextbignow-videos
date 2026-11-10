# ================= HOW THEY GOT SO BIG EP 4: Netflix lost ~800,000 US members in Jul–Sep 2011 and did it to itself (whiteboard).
# Held object: ONE red envelope ("DVD") and a dashed screen it wants to become; the envelope is split from the screen by a wall
# (Qwikster), the wall is erased, and at the end the screen is drawn solid while the envelope drops into the mailbox one last time.
# Mini map: stepmap(2) = the two moves. NEW this episode (story upgrade, 11 Nov): a MEMBER COUNTER under the pill (`tally`) that
# runs down in the first 1.6 s and again live while members leave (a4 → c2) — a number that keeps moving through the middle of the
# video, where same cart lost its viewers (PERFORMANCE insight AP). New drawings: redenv_m (hatched red envelope), plancard_m (plan
# card that tears in two), wall_m (brick wall between two things, erasable), atbubble_m (plain '@' bubble, no platform logo),
# chart_drop_m (line chart off a cliff), dashed_tv, tally (the counter).
# Opening move (new): frame 0 = the red envelope rocking in a mailbox, a big red −800,000 already written, a dashed screen to its
# right, and the counter under the pill already running down. =================
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

LIGHT = (150, 156, 170); PINK = (236, 92, 150); YEL = (255, 232, 110)


# ---------------------------------------------------------------- new marker props (this episode)
def redenv_m(c, x, y, t, t0, s=1.0, text="DVD", tilt=0.0, a=1.0):
    """the red envelope: outline + flap drawn on, then hatched red; word on a small white card"""
    k = pr(t, t0, 0.45); w, h = 260 * s, 170 * s
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt)
    box = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)]
    c.drawPath(_path(box), paint(WHITE, a))
    if k > 0.5:
        hatch(c, _path(box), pr(k, 0.5, 0.5), RD, gap=13, w=6, bbox=(-w / 2, -h / 2, w / 2, h / 2), seed=701, a=0.8 * a)
    ink(c, [wob(box, 702, 0.6), [(-w / 2, -h / 2), (0, 10 * s), (w / 2, -h / 2)]], k, MK, 6, a=a, pen_=False)
    if text and k >= 1:
        f = font("pm", int(50 * s)); tw_ = tw(f, text) + 30 * s
        c.drawRoundRect(R.MakeXYWH(-tw_ / 2, 22 * s, tw_, 60 * s), 10, 10, paint(WHITE, 0.95 * a))
        mtext(c, text, 0, 70 * s, int(50 * s), MK, 1, "pm", a=a)
    c.restore()


def plancard_m(c, x, y, t, t0, title="STREAMING + 1 DVD", split=0.0, s=1.0):
    """a plan card; split 0..1 tears it in two along a zig-zag and slides the halves apart"""
    k = pr(t, t0, 0.5); w, h = 620 * s, 300 * s
    if k <= 0: return
    zz = [((14 if i % 2 else -14) * s, -h / 2 + i * h / 10) for i in range(11)]
    gap = 80 * eio(split)
    for side in ((-1,) if split <= 0 else (-1, 1)):
        c.save(); c.translate(x + side * gap, y)
        if split <= 0:
            box = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)]
        elif side < 0:
            box = [(-w / 2, -h / 2)] + zz + [(-w / 2, h / 2), (-w / 2, -h / 2)]
        else:
            box = [(w / 2, -h / 2)] + zz + [(w / 2, h / 2), (w / 2, -h / 2)]
        c.drawPath(_path(box), paint(WHITE))
        ink(c, [wob(box, 711 + side, 0.6)], k if split <= 0 else 1, MK, 7, pen_=False)
        c.restore()
    if split <= 0 and title:
        mtext(c, title, x, y - h / 2 + 70 * s, int(46 * s), MK, pr(t, t0 + 0.4, 0.4), "pm")


def wall_m(c, x, y0, y1, t, t0, erase=0.0):
    """a brick wall drawn between two things; erase 0..1 rubs it out from the top"""
    k = pr(t, t0, 0.6)
    if k <= 0 or erase >= 1: return
    yb = y0 + (y1 - y0) * erase; w = 70
    rows = int((y1 - y0) / 50)
    polys = [[(x - w / 2, y0), (x - w / 2, y1)], [(x + w / 2, y0), (x + w / 2, y1)]]
    for r_ in range(rows + 1): polys.append([(x - w / 2, y0 + r_ * 50), (x + w / 2, y0 + r_ * 50)])
    for r_ in range(rows):
        xo = x if r_ % 2 else x - 12
        polys.append([(xo, y0 + r_ * 50), (xo, y0 + r_ * 50 + 50)])
    c.save(); c.clipRect(R.MakeLTRB(x - w, yb, x + w, y1 + 10))
    c.drawRect(R.MakeLTRB(x - w / 2, y0, x + w / 2, y1), paint((246, 226, 214), k))
    ink(c, polys, k, (150, 70, 50), 6, pen_=False)
    c.restore()


def atbubble_m(c, x, y, t, t0, handle="@QWIKSTER"):
    """a plain speech bubble with an @handle (no platform logo)"""
    k = pop_(t, t0)
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    speech(c, 0, 0, 470, 140, handle, 1, 56, BLU, tail=1)
    c.restore()


def chart_drop_m(c, x, y, t, t0, drop_t, w=620, h=330, col=RD):
    """a hand-drawn line chart: wiggles sideways, then falls off a cliff at drop_t"""
    k = pr(t, t0, 0.4)
    ink(c, [wob([(x - w / 2, y + h / 2), (x + w / 2, y + h / 2)], 721, 0.6), wob([(x - w / 2, y + h / 2), (x - w / 2, y - h / 2)], 722, 0.6)], k, MK, 6, pen_=False)
    pts = [(x - w / 2 + 20 + i * (w - 140) / 10, y - h / 2 + 60 + 22 * math.sin(i * 1.3)) for i in range(11)]
    ink(c, [wob(pts, 723, 0.8)], pr(t, t0 + 0.2, 0.8), BLU, 8, pen_=False)
    if t > drop_t:
        lx, ly = pts[-1]
        ink(c, [[(lx, ly), (lx + 30, ly + 40), (lx + 50, y + h / 2 - 40), (lx + 80, y + h / 2 - 30)]], pr(t, drop_t, 0.35), col, 9, pen_=False)


def tally(c, val, a=1.0, falling=False, x=765, y=372):
    """story upgrade 11 Nov: the member counter under the pill (US members, in millions), one row so it never meets the caption"""
    if a <= 0: return
    f1 = font("pm", 22); f2 = font("pm", 40)
    txt = f"{val:.2f}M"; w1 = tw(f1, "US MEMBERS"); w2 = tw(f2, txt); w = w1 + w2 + 54; h = 58
    c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), h / 2, h / 2, paint(WHITE, a))
    c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), h / 2, h / 2, stroke(RD if falling else MK, 4, a))
    c.drawString("US MEMBERS", x - w / 2 + 20, y + 8, f1, paint(BLU, a))
    c.drawString(txt, x - w / 2 + 34 + w1, y + 14, f2, paint(RD if falling else MK, a))


def dashed_tv(c, x, y, t, t0, w=360, h=230):
    """the screen Netflix wants to become, still only a dashed outline"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    x0, y0 = x - w / 2, y - h / 2
    for (a_, b_) in (((x0, y0), (x0 + w, y0)), ((x0 + w, y0), (x0 + w, y0 + h)), ((x0 + w, y0 + h), (x0, y0 + h)), ((x0, y0 + h), (x0, y0))):
        dash_line(c, a_, b_, k, LIGHT, 6)
    tri = [(x - 30, y - 40), (x + 42, y), (x - 30, y + 40), (x - 30, y - 40)]
    if k >= 1: ink(c, [tri], 1, LIGHT, 5, pen_=False)


def qwik_label(c, x, y, k=1.0):
    c.drawRoundRect(R.MakeXYWH(x - 150, y - 50, 300, 76), 12, 12, paint(WHITE, k))
    c.drawRoundRect(R.MakeXYWH(x - 150, y - 50, 300, 76), 12, 12, stroke(RD, 4, k))
    mtext(c, "QWIKSTER", x, y + 10, 56, RD, k, "pm")


# ---------------------------------------------------------------- shots
SHOTLIST = [("S_i1", 0.0, "cut"), ("S_i2", L0("i2") - 0.1, "wipe"), ("S_i3", L0("i3") - 0.1, "wipe"), ("S_i4", L0("i4") - 0.1, "wipe"),
            ("S_a1", L0("a1") - 0.1, "wipe"), ("S_a2", L0("a2") - 0.1, "cut"), ("S_a3", L0("a3") - 0.1, "cut"), ("S_a4", L0("a4") - 0.1, "wipe"),
            ("S_b1", L0("b1") - 0.1, "wipe"), ("S_b2", L0("b2") - 0.1, "wipe"), ("S_b4", L0("b4") - 0.1, "cut"), ("S_b5", L0("b5") - 0.05, "cut"),
            ("S_b6", L0("b6") - 0.1, "wipe"), ("S_c1", L0("c1") - 0.1, "wipe"), ("S_c2", L0("c2") - 0.1, "cut"), ("S_c3", L0("c3") - 0.1, "wipe"),
            ("S_c4", L0("c4") - 0.1, "cut"), ("S_d1", L0("d1") - 0.1, "wipe"), ("S_d2", L0("d2") - 0.1, "cut"), ("S_d3", L0("d3") - 0.1, "wipe"),
            ("S_d4", L0("d4") - 0.1, "wipe"), ("S_t1", L0("t1") - 0.1, "wipe"), ("S_end", L0("z1") - 0.1, "wipe")]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
M0, M1 = 24.59, 23.79   # US members (millions), end Jun → end Sep 2011, Netflix Q3 2011 letter


def S_i1(c, t):
    """frame 0: envelope rocking in the mailbox + big −800,000 + dashed screen, all already drawn; the counter runs down"""
    tj = TT("i1", "July", 0.6)
    mailbox_m(c, 300, 1440, t, -2.0, 1.0)
    rk = 5 * math.sin(t * 3.2)
    redenv_m(c, 300, 1080 - 12 * abs(math.sin(t * 1.6)), t, -2.0, 0.8, "DVD", -12 + rk)
    dashed_tv(c, 780, 1130, t, -2.0)
    arrow_m(c, (450, 1110), (580, 1120), 1.0, LIGHT, 7, bend=0.15)
    mtext(c, "?", 515, 1060, 70, RD, 1, "pm", a=0.5 + 0.5 * abs(math.sin(t * 4)))
    mtext(c, "−800,000", 510, 880, 120, RD, 1, "pm")
    if t < L1("i1"): pen(c, 560 + 18 * math.sin(t * 3), 1010 + 10 * math.cos(t * 4))
    if t > tj - 0.3:
        for i, mth in enumerate(("JUL", "AUG", "SEP")):
            tk = tj + i * 0.18
            if t < tk: continue
            kk = pop_(t, tk)
            c.drawRoundRect(R.MakeXYWH(600 + i * 120 - 50, 1300, 100 * kk, 56), 8, 8, stroke(RD, 4))
            mtext(c, mth, 600 + i * 120, 1342, 34, RD, pr(t, tk, 0.2), "pm")
    say(c, t, -2.0, "netflix once lost", "800,000 MEMBERS", RD, under=RD, size=150)
    note(c, t, -2.0, "US MEMBERS, END JUN TO END SEP 2011 · NETFLIX Q3 2011 LETTER")


def S_i2(c, t):
    t0 = SHOT["S_i2"]["start"]; tp = TT("i2", "price", 0.4); tn = TT("i2", "name.", 0.4)
    redenv_m(c, 270, 1150, t, t0 - 3, 0.85, "DVD")
    dashed_tv(c, 780, 1150, t, t0 - 3)
    arrow_m(c, (420, 1150), (590, 1150), 1.0, LIGHT, 7)
    if t > tp - 0.3: tag_m(c, 430, 960, "$", t, tp - 0.3, RD, -10, 0.7)
    if t > tn - 0.4: sticky_m(c, 700, 940, t, tn - 0.4, "NAME ???", 0.6, 8, RD)
    say(c, t, t0 + 0.08, "it did that to", "ITSELF", RD, under=RD)
    note(c, t, t0 + 0.6, "TWO OWN GOALS: A PRICE CHANGE, THEN A NEW NAME")


def S_i3(c, t):
    t0 = SHOT["S_i3"]["start"]; tr = TT("i3", "running", 0.3); td = TT("i3", "DVDs", 0.3)
    hero(c, 250, FLOOR, 1.0, POSES["hold"], Face("open", "smile", look=(1, 0)), t)
    ink(c, [wob([(420, 1250), (960, 1250)], 731, 0.6), wob([(450, 1250), (450, 1420)], 732, 0.5), wob([(930, 1250), (930, 1420)], 733, 0.5)], pr(t, t0 + 0.1, 0.5), MK, 8)
    mtext(c, "NETFLIX", 690, 1360, 60, MK, pr(t, tr - 0.2, 0.4), "pm", pen_=True)
    for i in range(5):
        tk = td - 0.5 + i * 0.1
        if t > tk: redenv_m(c, 640 + (i - 2) * 12, 1200 - i * 34, t, tk, 0.55, "DVD" if i == 4 else None, -4 + i * 2)
    if t > td + 0.3: coinpile_m(c, 860, 1210, t, td + 0.3, 6)
    say(c, t, t0 + 0.08, "you're running it", "2011", MK, under=OR)
    note(c, t, t0 + 0.6, "2011: DVDS BY MAIL + A YOUNG STREAMING SERVICE, ONE PLAN")


def S_i4(c, t):
    t0 = SHOT["S_i4"]["start"]; tw2 = TT("i4", "two", 0.3); tn = TT("i4", "Neither", 0.3)
    redenv_m(c, 250, 1120, t, t0 - 3, 0.75, "DVD")
    dashed_tv(c, 780, 1120, t, t0 + 0.1)
    mtext(c, "STREAMING", 780, 1320, 44, BLU, pr(t, t0 + 0.4, 0.4), "pm")
    if t > tw2 - 0.2:
        arrow_m(c, (390, 1120), (580, 1120), pr(t, tw2 - 0.2, 0.4), BLU, 9)
        for i in range(2): mtext(c, str(i + 1), 440 + i * 80, 1080, 50, OR, pr(t, tw2 + i * 0.2, 0.2), "pm")
    if t > tn - 0.1: mtext(c, "?", 485, 1000, 100, RD, pop_(t, tn - 0.1), "pm")
    say(c, t, t0 + 0.08, "two moves to get there", "FAST", MK, under=BLU)


def S_a1(c, t):
    t0 = SHOT["S_a1"]["start"]; ts = TT("a1", "split", 0.4)
    plancard_m(c, 510, 1110, t, t0 + 0.05, "STREAMING + 1 DVD", split=pr(t, ts + 0.3, 0.5))
    if ts - 0.1 < t < ts + 0.4:
        ink(c, [[(510 + (14 if i % 2 else -14), 960 + i * 30) for i in range(11)]], pr(t, ts - 0.1, 0.3), RD, 8)
    if t > ts + 0.6:
        mtext(c, "STREAMING", 275, 1120, 40, BLU, pr(t, ts + 0.6, 0.3), "pm")
        mtext(c, "DVD", 745, 1120, 50, RD, pr(t, ts + 0.7, 0.3), "pm")
    say(c, t, t0 + 0.08, "move one, july", "SPLIT THE PLAN", MK, under=RD, size=150)
    note(c, t, t0 + 0.6, "NETFLIX PRESS RELEASE, 12 JUL 2011")


def S_a2(c, t):
    t0 = SHOT["S_a2"]["start"]; tn = TT("a2", "nine", 0.3)
    plancard_m(c, 510, 1150, t, t0 - 3, "STREAMING + 1 DVD", 0.0)
    redenv_m(c, 400, 1210, t, t0 + 0.05, 0.5, None)
    tv_m(c, 630, 1200, t, t0 + 0.3, 170, 110)
    if t > tn - 0.3: tag_m(c, 700, 920, "$9.99", t, tn - 0.3, BLU, -8, 0.85)
    say(c, t, t0 + 0.08, "before, both together", "$9.99", BLU, under=BLU)
    note(c, t, t0 + 0.6, "OLD PLAN: STREAMING + 1 DVD AT A TIME, $9.99/MONTH (CNN MONEY, 12 JUL 2011)")


def S_a3(c, t):
    t0 = SHOT["S_a3"]["start"]; tb = TT("a3", "both?", 0.3); tf = TT("a3", "fifteen", 0.3); ts = TT("a3", "sixty", 0.3)
    plancard_m(c, 510, 1150, t, t0 - 3, "", 1.0)
    mtext(c, "STREAMING", 275, 1160, 40, BLU, 1, "pm"); mtext(c, "DVD", 745, 1160, 48, RD, 1, "pm")
    tag_m(c, 275, 1370, "$7.99", t, t0 + 0.1, BLU, -6, 0.7)
    tag_m(c, 745, 1370, "$7.99", t, t0 + 0.6, RD, 6, 0.7)
    if t > tb - 0.2: mtext(c, "+", 505, 1395, 90, MK, pr(t, tb - 0.2, 0.2), "pm")
    if t > tf - 0.3: mtext(c, "= $15.98", 470, 935, 100, RD, pr(t, tf - 0.3, 0.5), "pm", pen_=True)
    if t > ts - 0.3:
        arrow_m(c, (760, 960), (820, 860), pr(t, ts - 0.3, 0.3), RD, 10)
        mtext(c, "+60%", 840, 830, 60, RD, pr(t, ts - 0.1, 0.3), "pm")
    say(c, t, t0 + 0.08, "want both?", "$15.98", RD, under=RD)
    note(c, t, t0 + 0.6, "NEW PRICE FOR EXISTING MEMBERS FROM 1 SEP 2011 · NETFLIX, 12 JUL 2011")


def S_a4(c, t):
    t0 = SHOT["S_a4"]["start"]; tc = TT("a4", "cancelling.", 0.3); tt_ = TT("a4", "two", 0.3)
    tag_m(c, 510, 960, "$15.98", t, t0 - 3, RD, -6, 0.9, hot=True)
    for i in range(6):
        tk = t0 + 0.2 + i * 0.1
        if t < tk: continue
        hx = 210 + i * 120; kk = pop_(t, tk); u_ = eio(pr(t, tc + 0.2 + i * 0.15, 0.7)); dx = 120 * u_
        if u_ >= 1: continue
        c.save(); c.translate(hx + dx, 1250); c.scale(kk, kk); c.saveLayerAlpha(None, int(255 * (1 - u_)))
        c.drawCircle(0, -40, 30, paint(WHITE)); c.drawCircle(0, -40, 30, stroke(MK, 5))
        c.drawLine(-16, -60, -4, -52, stroke(MK, 4)); c.drawLine(16, -60, 4, -52, stroke(MK, 4))
        c.drawPath(_path(circ_pts(0, -22, 10, 200, 340, 10)), stroke(MK, 4))
        c.drawPath(_path([(-34, 20), (-28, -8), (28, -8), (34, 20)]), stroke(BLU, 6)); c.restore(); c.restore()
    if t > tt_ - 0.2: mtext(c, "MOVE 2 IS STILL COMING", 510, 1400, 50, OR, pr(t, tt_ - 0.2, 0.5), "pm")
    say(c, t, t0 + 0.08, "members start", "CANCELLING", RD, under=RD)


def S_b1(c, t):
    t0 = SHOT["S_b1"]["start"]; tm = TT("b1", "first", 0.3) + 0.4
    if t < tm - 0.6: laptop_m(c, 620, 1180, t, t0 + 0.1, "COMPANY BLOG", 2)
    else: quote_m(c, 540, 1040, t, tm - 0.6, ["I messed up. I owe", "everyone an explanation."], "REED HASTINGS, CEO · 18 SEP 2011")
    if t < tm - 0.6: hero(c, 200, FLOOR, 0.8, POSES["shrug"], Face("open", "flat", brows="worried", look=(1, -1)), t)
    say(c, t, t0 + 0.08, "september, on the company blog", "I MESSED UP", RD, under=RD, size=150)
    note(c, t, t0 + 0.6, "QUOTE: HASTINGS BLOG POST, 18 SEP 2011 (AS REPRINTED BY BUZZFEED / CBS NEWS)")


def S_b2(c, t):
    t0 = SHOT["S_b2"]["start"]; to = TT("b2", "own", 0.3); tb = TT("b2", "bill", 0.3); tq = L0("b3")
    tv_m(c, 790, 1100, t, t0 + 0.05, 330, 210)
    ex = 270 - 40 * eio(pr(t, t0 + 0.2, 0.6))
    redenv_m(c, ex, 960, t, t0 - 3, 0.8, "DVD" if t < tq else None)
    wall_m(c, 520, 940, 1300, t, t0 + 0.4)
    if t > to - 0.3: laptop_m(c, 240, 1400, t, to - 0.3, "OWN WEBSITE", 1)
    if t > tb - 0.2: tag_m(c, 330, 800, "OWN BILL", t, tb - 0.2, RD, -8, 0.5)
    if t > tq - 0.1: qwik_label(c, ex, 1040, pr(t, tq - 0.1, 0.5))
    say(c, t, t0 + 0.08, "the dvd side gets", "ITS OWN NAME", MK, t1=tq - 0.2, under=OR)
    say(c, t, tq - 0.15, "the new name", "QWIKSTER", RD, under=RD)
    note(c, t, t0 + 0.6, "HASTINGS BLOG, 18 SEP 2011: SEPARATE WEBSITES, TWO CHARGES ON YOUR CARD")


def S_b4(c, t):
    t0 = SHOT["S_b4"]["start"]; ts = TT("b4", "Somebody", 0.3); tw_ = TT("b4", "Twitter.", 0.3)
    redenv_m(c, 250, 1080, t, t0 - 3, 0.8, None)
    qwik_label(c, 250, 1160)
    if t > ts - 0.3: atbubble_m(c, 700, 960, t, ts - 0.3)
    if t > tw_ - 0.2: stamp_m(c, 720, 1200, "TAKEN", pr(t, tw_ - 0.2, 0.25), RD, -8, 76)
    say(c, t, t0 + 0.08, "on twitter, that name was", "TAKEN", RD, under=RD)
    note(c, t, t0 + 0.6, "@QWIKSTER ALREADY BELONGED TO SOMEONE ELSE · NBC NEWS, SEP 2011")


def S_b5(c, t):
    """the one OOPS beat: the hero (in the seat) faces camera, arms up, red OOPS stamp"""
    t0 = SHOT["S_b5"]["start"]; to = TT("b5", "Oops.", 0.2)
    hero(c, 510, FLOOR, 1.3, POSES["shock"] if t > to - 0.1 else POSES["stand"], Face("wide", "o", brows="up", look=(0, 0)), t)
    if t > to - 0.05: stamp_m(c, 510, 900, "OOPS!", pr(t, to - 0.05, 0.25), RD, -7, 120)


def S_b6(c, t):
    t0 = SHOT["S_b6"]["start"]; t22 = TT("b6", "Twenty-two", 0.3); tw_ = TT("b6", "website", 0.4); tn = TT("b6", "no", 0.4)
    tv_m(c, 790, 1120, t, t0 - 3, 330, 210)
    ex = 250 + 200 * eio(pr(t, tw_, 0.6))
    redenv_m(c, ex, 1100, t, t0 - 3, 0.8, "DVD" if t > tw_ else None)
    wall_m(c, 520, 960, 1300, t, t0 - 3, erase=pr(t, tw_ - 0.4, 0.5))
    if t < tw_:
        qwik_label(c, 250, 1180)
        cross(c, 100, 1120, 400, 1220, pr(t, t22 + 0.3, 0.3), RD, 12)
    if t > t22 - 0.3:
        calendar(c, 250, 860, 0.75, "OCT 2011", "10", pop_(t, t22 - 0.3))
        mtext(c, "22 DAYS LATER", 680, 880, 64, OR, pr(t, t22, 0.4), "pm", pen_=True)
    if t > tn - 0.3: stamp_m(c, 520, 1370, "NO QWIKSTER", pr(t, tn - 0.3, 0.25), RD, -5, 60)
    say(c, t, t0 + 0.08, "in other words", "NO QWIKSTER", RD, under=RD, size=150)
    note(c, t, t0 + 0.6, "NETFLIX BLOG, 10 OCT 2011 (VIA CONSUMERIST)")


def S_c1(c, t):
    t0 = SHOT["S_c1"]["start"]; ts = TT("c1", "stays.", 0.3); tc = TT("c1", "count", 0.3)
    tag_m(c, 320, 1050, "$15.98", t, t0 + 0.05, RD, -6, 0.9)
    if t > ts - 0.2: ink(c, [wob(circ_pts(320, 1050, 190, -160, 210, 40, ry=110), 741, 1.2)], pr(t, ts - 0.2, 0.4), GR, 7, pen_=False)
    if t > tc - 0.4:
        mtext(c, "THE COUNT", 740, 950, 56, MK, pr(t, tc - 0.4, 0.4), "pm", pen_=True)
        for i, m_ in enumerate(("JUL", "AUG", "SEP")): tagpill_m(c, 740, 1060 + i * 100, m_, pop_(t, tc - 0.2 + i * 0.15), BLU, 46)
        if t > tc + 0.4: mtext(c, "?", 740, 1400, 90, RD, pop_(t, tc + 0.4), "pm")
    say(c, t, t0 + 0.08, "but the price split", "STAYS", GR, under=GR)


def S_c2(c, t):
    t0 = SHOT["S_c2"]["start"]; te = TT("c2", "eight", 0.3); tg = TT("c2", "gone", 0.3)
    for i in range(10):
        hx = 170 + i * 75; out = eio(pr(t, t0 + 0.2 + i * 0.12, 0.5)) if i >= 3 else 0.0
        a_ = 1 - out
        if a_ <= 0: continue
        c.save(); c.translate(hx + 500 * out, 1340)
        c.drawCircle(0, -40, 26, paint(WHITE, a_)); c.drawCircle(0, -40, 26, stroke(MK, 5, a_))
        c.drawPath(_path([(-30, 20), (-24, -8), (24, -8), (30, 20)]), stroke(BLU if i < 3 else RD, 6, a_)); c.restore()
    if t > te - 0.2: mtext(c, "−800,000", 510, 1040, 130, RD, pr(t, te - 0.2, 0.5), "pm", pen_=True)
    if t > tg: mtext(c, "24.59M TO 23.79M", 510, 1150, 50, MK, pr(t, tg, 0.5), "pm")
    say(c, t, t0 + 0.08, "gone by the end of september", "−800,000", RD, under=RD)
    note(c, t, t0 + 0.6, "US MEMBERS 24.59M TO 23.79M · Q3 2011 SHAREHOLDER LETTER (24 OCT 2011)")


def S_c3(c, t):
    t0 = SHOT["S_c3"]["start"]; tt_ = TT("c3", "thirty-five", 0.3)
    chart_drop_m(c, 430, 1130, t, t0 + 0.05, tt_ - 0.3, 560, 330)
    if t > tt_ - 0.1:
        mtext(c, "−35%", 800, 1180, 100, RD, pr(t, tt_ - 0.1, 0.3), "pm")
        mtext(c, "IN ONE DAY", 800, 1260, 44, MK, pr(t, tt_ + 0.2, 0.3), "pm")
    say(c, t, t0 + 0.08, "the next day, the shares", "−35%", RD, under=RD)
    note(c, t, t0 + 0.6, "CNN MONEY, 25 OCT 2011 · A 2011 EVENT, NOT INVESTMENT ADVICE")


def S_c4(c, t):
    t0 = SHOT["S_c4"]["start"]; ts = TT("c4", "scrapped", 0.3)
    chart_drop_m(c, 650, 980, t, t0 - 3, t0 - 3, 400, 220)
    hero(c, 240, FLOOR, 1.1, POSES["point"] if t > ts else POSES["stand"], Face("open", "flat", brows="up", look=(0 if t > ts else 1, 0)), t)
    tag_m(c, 690, 1270, "$15.98", t, t0 + 0.1, RD, 6, 0.8)
    if t > ts - 0.2:
        ex = 690 + 60 * math.sin((t - ts) * 8); k = pr(t, ts - 0.2, 0.3)
        c.drawRoundRect(R.MakeXYWH(ex - 40, 1130, 80, 90), 10, 10, paint((60, 66, 84), k)); c.drawRect(R.MakeXYWH(ex - 40, 1200, 80, 20), paint((210, 210, 214), k))
    say(c, t, t0 + 0.08, "honestly? I'd scrap the", "PRICE SPLIT", MK, under=OR, size=150)


def S_d1(c, t):
    t0 = SHOT["S_d1"]["start"]; tk = TT("d1", "kept", 0.3); tl = TT("d1", "letter", 0.3); tq = TT("d1", "quickly", 0.3)
    if t < tl: stamp_m(c, 510, 1100, "KEPT IT", pr(t, tk - 0.2, 0.25), GR, -6, 90)
    else:
        quote_m(c, 510, 1080, t, tl, ["What we misjudged was", "how quickly to move there."], "NETFLIX · Q3 2011 LETTER")
        if t > tq: ink(c, [wob([(300, 1100), (740, 1096)], 751, 0.8)], pr(t, tq, 0.3), OR, 9, pen_=False)
    say(c, t, t0 + 0.08, "netflix kept it. the letter said", "HOW QUICKLY", MK, under=OR, size=150)
    note(c, t, t0 + 0.6, "NETFLIX Q3 2011 SHAREHOLDER LETTER, 24 OCT 2011")


def S_d2(c, t):
    t0 = SHOT["S_d2"]["start"]; tw_ = TT("d2", "where.", 0.3); tf = TT("d2", "fast.", 0.3); tp = TT("d2", "streaming.", 0.3)
    redenv_m(c, 220, 1150, t, t0 - 3, 0.7, "DVD")
    if t > tp - 0.4: tv_m(c, 790, 1150, t, tp - 0.4, 300, 190)
    else: dashed_tv(c, 790, 1150, t, t0 - 3, 300, 190)
    arrow_m(c, (350, 1150), (620, 1150), pr(t, t0 + 0.1, 0.5), BLU, 9)
    if t > tw_ - 0.2:
        mtext(c, "WHERE", 450, 1030, 54, GR, pr(t, tw_ - 0.2, 0.3), "pm")
        ink(c, [[(540, 1020), (558, 1040), (592, 995)]], pr(t, tw_, 0.2), GR, 8, pen_=False)
    if t > tf - 0.2:
        mtext(c, "HOW FAST", 470, 1300, 54, RD, pr(t, tf - 0.2, 0.3), "pm")
        cross(c, 630, 1255, 680, 1305, pr(t, tf, 0.2), RD, 8)
    say(c, t, t0 + 0.08, "not where", "HOW FAST", RD, under=RD)


def S_d3(c, t):
    t0 = SHOT["S_d3"]["start"]; tm = TT("d3", "More", 0.3)
    tv_m(c, 510, 1150, t, t0 + 0.05, 520, 320)
    if t > tm - 0.3:
        mtext(c, "325M+", 510, 930, 120, GR, pr(t, tm - 0.3, 0.5), "pm", pen_=True)
        mtext(c, "END OF 2025", 510, 1400, 46, MK, pr(t, tm + 0.3, 0.3), "pm")
    say(c, t, t0 + 0.08, "paid members", "325 MILLION+", GR, under=GR, size=150)
    note(c, t, t0 + 0.6, "NETFLIX Q4 2025 RESULTS, JAN 2026 (VIA VARIETY, AXIOS) · WORLDWIDE")


def S_d4(c, t):
    t0 = SHOT["S_d4"]["start"]; tl = TT("d4", "last", 0.3); tb = TT("d4", "billion", 0.3)
    mailbox_m(c, 300, 1440, t, t0 + 0.05, flag=pr(t, tl + 0.4, 0.4))
    dy = 260 * eio(pr(t, tl, 0.6))
    c.save(); c.clipRect(R.MakeLTRB(0, 0, W, 1140)); redenv_m(c, 300, 900 + dy, t, t0 + 0.2, 0.7, "DVD"); c.restore()
    disc_m(c, 760, 1020, t, t0 + 0.4, 120, None, RD, spin=40)
    if t > tl: mtext(c, "LAST ONES: 29 SEP 2023", 730, 1300, 38, RD, pr(t, tl, 0.5), "pm")
    if t > tb - 0.2: mtext(c, "5 BILLION+", 730, 1385, 56, MK, pr(t, tb - 0.2, 0.4), "pm")
    say(c, t, t0 + 0.08, "the red envelopes", "LAST ONES OUT", RD, under=RD, size=150)
    note(c, t, t0 + 0.6, "NETFLIX (SARANDOS), 18 APR 2023 · 5BN+: CBS LA, ENGADGET")


def S_t1(c, t):
    t0 = SHOT["S_t1"]["start"]; te = TT("t1", "explaining", 0.3); tw_ = TT("t1", "why", 0.3)
    if t > te - 0.2: speech(c, 320, 1000, 300, 130, "WHY?", pop_(t, te - 0.2), 70, BLU, tail=1)
    tag_m(c, 690, 1200, "$ UP", t, t0 + 0.2, RD, -6, 1.0)
    if t > tw_ - 0.2:
        arrow_m(c, (330, 1080), (560, 1170), pr(t, tw_ - 0.2, 0.3), BLU, 8, bend=0.2)
        mtext(c, "1", 320, 1200, 60, OR, pr(t, tw_, 0.2), "pm"); mtext(c, "2", 680, 1340, 60, OR, pr(t, tw_ + 0.15, 0.2), "pm")
    say(c, t, t0 + 0.08, "raising a price?", "SAY WHY FIRST", OR, under=OR, size=150)
    note(c, t, t0 + 0.6, "Q3 2011 LETTER: \"OUR LACK OF EXPLANATION ABOUT THE RISING COST…\"")


def S_end(c, t):
    t0 = SHOT["S_end"]["start"]; tz2 = L0("z2"); tk = TT("z1", "Keep", 0.4); ts = TT("z1", "split,", 0.4, 1)
    c.save(); c.translate(0, 6 * math.sin(t * 2.2))
    mailbox_m(c, 510, 1240, t, t0 - 3, 1.0)
    redenv_m(c, 510, 880 + 8 * math.sin(t * 2.6), t, t0 - 3, 0.6, "DVD", 5 * math.sin(t * 1.8))
    c.restore()
    tagpill_m(c, 290, 1340, "KEEP", pop_(t, tk - 0.2), GR, 60)
    tagpill_m(c, 730, 1340, "SPLIT", pop_(t, ts - 0.2), RD, 60)
    for i, (x, tm) in enumerate(((290, tk), (730, ts))):
        if t > tm: ink(c, [wob(circ_pts(x, 1330, 160, -150, 215, 40, ry=80), 95 + i, 1.4)], pr(t, tm, 0.35), OR, 7, pen_=False)
    say(c, t, t0 + 0.08, "split off what pays the bills?", "KEEP OR SPLIT?", MK, t1=tz2 - 0.3, under=BLU, size=150)
    say(c, t, tz2 - 0.25, "send it to whoever still owns a dvd player", "SAVE THIS", BLU, under=OR)
    note(c, t, t0 + 0.6, "COMMENT ONE WORD · EDUCATION ONLY")


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}
SURF = surface()
IMPACTS = [(TT("b5", "Oops.", 0.2), 0.16, 6), (TT("c3", "thirty-five", 0.3) - 0.1, 0.14, 5), (TT("a3", "fifteen", 0.3), 0.12, 4)]
# the MOVE map (stepmap: 2 moves) and the MEMBER COUNTER (story upgrade 11 Nov)
_MAP = {"S_a1": (0, ()), "S_a2": (0, ()), "S_a3": (0, ()), "S_a4": (1, (0,)), "S_b1": (1, (0,)), "S_b2": (1, (0,)), "S_b4": (1, (0,)),
        "S_b6": (1, (0,)), "S_c1": (-1, (0, 1)), "S_c2": (-1, (0, 1)), "S_c3": (-1, (0, 1))}
_TOP = {"S_a1": "MOVE 1 OF 2", "S_a2": "MOVE 1 OF 2", "S_a3": "MOVE 1 OF 2", "S_a4": "MOVE 1 OF 2", "S_b1": "MOVE 2 OF 2", "S_b2": "MOVE 2 OF 2",
        "S_b4": "MOVE 2 OF 2", "S_b6": "MOVE 2 OF 2", "S_c1": "THE COUNT", "S_c2": "THE COUNT", "S_c3": "THE COUNT", "S_d1": "WHAT IT DID NEXT",
        "S_d2": "WHAT IT DID NEXT", "S_d3": "WHAT IT DID NEXT", "S_d4": "WHAT IT DID NEXT", "S_t1": "THE LESSON"}
_TALLY = {"S_i1", "S_a3", "S_a4", "S_b1", "S_b2", "S_b4", "S_b6", "S_c1", "S_c2"}


def tally_val(t):
    """the counter: runs down in the hook (frame-0 move); from move 1 it starts full again and leaks while members leave, landing at c2"""
    if t < L0("i2"):
        return M0 - (M0 - M1) * eio(pr(t, 0.15, 1.6))
    ta, tz = TT("a4", "cancelling.", 0.3), TT("c2", "gone", 0.3)
    return M0 - (M0 - M1) * eio(pr(t, ta - 0.4, tz - ta + 0.4))


def topline(sid): return f"HOW THEY GOT SO BIG · {_TOP[sid]}" if sid in _TOP else "OOPSMYBUSINESS · HOW THEY GOT SO BIG"


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
    if sid in _MAP: stepmap(c, 2, _MAP[sid][0], _MAP[sid][1], min(1, pr(tt, s["start"], 0.3)), x0=360)
    if sid in _TALLY:
        v = tally_val(tt); tally(c, v, 1.0 if sid == "S_i1" else min(1, pr(tt, s["start"], 0.3)), falling=v < M0 - 0.005)
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
