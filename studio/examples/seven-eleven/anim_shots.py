# ================= HOW THEY GOT SO BIG EP 5: America's 7-Eleven is owned in Tokyo by the partner that once couldn't get a meeting
# (whiteboard, 13 Nov 2026). Held object: ONE little store (plain handwritten "7-ELEVEN", blue hatched awning) with an OWNER tag hanging
# under it that is rubbed out and rewritten through the story (TOKYO -> DALLAS -> TOKYO (LICENSE) -> CHAPTER 11 -> TOKYO 70% -> TOKYO 100%).
# Mini map: stepmap(3) = the three moves; live counter: tally OWNED IN TOKYO (100 % on frame 0, back to 0 % in 1973, 70 % in 1991, 100 % in 2005).
# Visual upgrade (new): TWO-CITY BOARD — Dallas always sits on the LEFT, Tokyo always on the RIGHT, and every move between the cities is a
# camera PAN across the board in that direction (instead of an eraser wipe), so geography is carried by motion. Opening move (new): frame 0 is
# the store between two map pins with the dashed Dallas -> Tokyo arrow already drawn and the counter pulsing at 100 %.
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
SP_OR = (255, 196, 120); SP_YE = (255, 226, 90); SP_PU = (196, 170, 255); SP_GR = (150, 226, 170); SP_BL = (150, 196, 255); SP_PK = (255, 170, 200)
SP_DAL = SP_OR; SP_TOK = SP_BL   # colour code: Dallas = orange, Tokyo = blue
DAL_X, TOK_X = 200, 860


# ---------------------------------------------------------------- new marker drawings (this episode)
def rubtext(c, x, y, old, new, t, t_sw, size=46, col=MK, new_col=None, key="pm"):
    """a word that a tiny eraser rubs out at t_sw (0.35 s) and the new word is written on"""
    new_col = new_col or col
    if t < t_sw or new is None:
        if old: mtext(c, old, x, y, size, col, 1, key)
        return
    u = pr(t, t_sw, 0.35)
    if u < 1:
        if old: mtext(c, old, x, y, size, col, 1, key, a=1 - u)
        f = font(key, size); wv = max(tw(f, old or "X"), 60)
        ex = x - wv / 2 + wv * (0.5 + 0.5 * math.sin(u * 9))
        c.drawRoundRect(R.MakeXYWH(ex - 26, y - size * 0.9, 52, size * 1.1), 8, 8, paint((60, 66, 84)))
        c.drawRect(R.MakeXYWH(ex - 26, y + size * 0.05, 52, 12), paint((210, 210, 214)))
    else:
        mtext(c, new, x, y, size, new_col, pr(t, t_sw + 0.35, 0.35), key)


def ownertag(c, x, y, t, t0, text, new=None, t_sw=1e9, col=RD, new_col=None, w=None):
    """the OWNER tag hanging under the store on a string; its word is rubbed out and rewritten (the held object's state)"""
    k = pr(t, t0, 0.4)
    if k <= 0: return
    f = font("pm", 42)
    ww = w or max(tw(f, text), tw(f, new or "")) + 70
    c.drawLine(x, y - 70, x, y - 30, stroke(MK, 4, k))
    rr = R.MakeXYWH(x - ww / 2, y - 30, ww, 74)
    c.drawRoundRect(rr, 14, 14, paint(WHITE, k)); c.drawRoundRect(rr, 14, 14, stroke(MK, 5, k))
    c.drawCircle(x, y - 14, 6, stroke(MK, 3, k))
    if k >= 1: rubtext(c, x, y + 26, text, new, t, t_sw, 40, col, new_col)


def store(c, x, y, t, t0, s=1.0, sign="7-ELEVEN", owner=None, new=None, t_sw=1e9, ocol=RD, ncol=None, sign_new=None, sign_sw=1e9):
    """THE held store: shopfront with a blue hatched awning, the sign written on, OWNER tag hanging under it"""
    shopfront_m(c, x, y, t, t0, s, label=None, col=BLU)
    if pr(t, t0, 0.6) >= 1:
        rubtext(c, x, y - 300 * s - 34 * s, sign, sign_new, t, sign_sw, int(48 * s), MK)
    if owner: ownertag(c, x, y + 100 * s, t, t0 + 0.4, owner, new, t_sw, ocol, ncol)


def citypin(c, x, y, t, t0, name, col):
    pin_m(c, x, y, t, t0, 1.0, col)
    mtext(c, name, x, y + 60, 44, col, pr(t, t0 + 0.3, 0.3), "pm")


def mini_store(c, x, y, s, col, k=1.0):
    """a tiny shop icon (for counts): box + hatched awning stripe"""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k * s, k * s)
    c.drawRect(R.MakeXYWH(-24, -40, 48, 40), paint(WHITE)); c.drawRect(R.MakeXYWH(-28, -52, 56, 14), paint(col, 0.6))
    c.drawRect(R.MakeXYWH(-24, -40, 48, 40), stroke(MK, 3)); c.drawRect(R.MakeXYWH(-28, -52, 56, 14), stroke(MK, 3))
    c.drawRect(R.MakeXYWH(4, -24, 12, 24), stroke(MK, 2)); c.restore()


def store_stack(c, x, base, n, t, t0, col, step=0.05, cols=4):
    """n tiny shops stacked into a tower, popping one by one"""
    for i in range(n):
        tk = t0 + i * step
        if t < tk: continue
        r_, q = divmod(i, cols)
        mini_store(c, x + (q - (cols - 1) / 2) * 62, base - r_ * 56, 1.0, col, pop_(t, tk, 0.25))


def grocery_m(c, x, y, kind, k):
    """milk bottle / egg pair / bread loaf, drawn small, popping in"""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    if kind == "milk":
        p = [(-34, 0), (-34, -110), (-18, -140), (-18, -170), (18, -170), (18, -140), (34, -110), (34, 0), (-34, 0)]
        c.drawPath(_path(p), paint(WHITE)); c.drawRect(R.MakeXYWH(-34, -90, 68, 40), paint(SP_BL, 0.8))
        ink(c, [p, [(-22, -170), (22, -170)]], 1, MK, 6, pen_=False); mtext(c, "MILK", 0, -60, 22, BLU, 1, "pm")
    elif kind == "eggs":
        for dx in (-30, 30):
            c.drawOval(R.MakeXYWH(dx - 28, -80, 56, 76), paint(EGG)); c.drawOval(R.MakeXYWH(dx - 28, -80, 56, 76), stroke(MK, 5))
    else:
        p = circ_pts(0, -40, 70, 180, 360, 24, ry=50) + [(70, 0), (-70, 0), (-70, -40)]
        c.drawPath(_path(p), paint(SP_OR, 0.7)); ink(c, [p], 1, MK, 6, pen_=False)
        for dx in (-30, 0, 30): c.drawLine(dx - 10, -70, dx + 10, -50, stroke(MK, 4))
    c.restore()


def desk_m(c, x, y, t, t0, sign, sub):
    """a planner's desk: table top + legs, a name sign standing on it"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    ink(c, [wob([(x - 260, y), (x + 260, y)], 901, 0.6), wob([(x - 230, y), (x - 230, y + 150)], 902, 0.4), wob([(x + 230, y), (x + 230, y + 150)], 903, 0.4)], k, MK, 8)
    if k < 1: return
    sw = 400; rr = R.MakeXYWH(x - sw / 2, y - 130, sw, 120)
    c.drawRoundRect(rr, 10, 10, paint(WHITE)); c.drawRoundRect(rr, 10, 10, stroke(BLU, 5))
    mtext(c, sign, x, y - 78, 40, BLU, pr(t, t0 + 0.4, 0.3), "pm"); mtext(c, sub, x, y - 30, 30, MK, pr(t, t0 + 0.6, 0.3), "kb")


def license_m(c, x, y, t, t0, s=1.0, signed=0.0, tilt=-5, title="LICENSE"):
    """a license document: title, three lines, a signature line that gets signed (signed 0..1)"""
    k = pop_(t, t0, 0.35, 1.5)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k * s, k * s)
    rr = R.MakeXYWH(-170, -120, 340, 240)
    c.drawRect(R.MakeXYWH(-164, -112, 340, 240), paint((0, 0, 0), 0.10, blur=6)); c.drawRect(rr, paint(WHITE)); c.drawRect(rr, stroke(MK, 6))
    mtext(c, title, 0, -66, 40, PU, 1, "pm")
    for i in range(3): c.drawLine(-120, -24 + i * 28, 120, -24 + i * 28, stroke(LIGHT, 4))
    c.drawLine(-120, 84, 120, 84, stroke(MK, 3))
    if signed > 0:
        pts = [(-110 + 220 * j / 30, 72 - 14 * math.sin(j * 0.9) - 6 * math.cos(j * 2.1)) for j in range(31)]
        ink(c, [pts], signed, BLU, 5, pen_=False)
    c.restore()


def magnifier(c, x, y, r, k, col=MK):
    if k <= 0: return
    c.drawCircle(x, y, r * k, paint(SP_BL, 0.25)); ink(c, [wob(circ_pts(x, y, r * k, -90, 270, 40), 921, 0.5)], 1, col, 8, pen_=False)
    ink(c, [[(x + r * 0.7 * k, y + r * 0.7 * k), (x + r * 1.5 * k, y + r * 1.5 * k)]], 1, col, 14, pen_=False)


def notebook_m(c, x, y, t, t0, lines_=3, label=None):
    k = pr(t, t0, 0.4)
    if k <= 0: return
    rr = R.MakeXYWH(x - 120, y - 150, 240, 300)
    c.drawRect(rr, paint(WHITE, k)); ink(c, [wob([(x - 120, y - 150), (x + 120, y - 150), (x + 120, y + 150), (x - 120, y + 150), (x - 120, y - 150)], 931, 0.5)], k, MK, 6)
    for i in range(lines_):
        c.drawLine(x - 90, y - 90 + i * 50, x + 30 + 50 * ((i * 7) % 3) / 3, y - 90 + i * 50, stroke(BLU, 5, pr(t, t0 + 0.3 + i * 0.15, 0.2)))
    if label: mtext(c, label, x, y + 110, 34, RD, pr(t, t0 + 0.6, 0.3), "pm")


def till_m(c, x, y, t, t0, s=1.0):
    """a shop till with a small screen; a receipt grows out of its top"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    P = lambda pts: _sc(x, y, s, pts)
    body = P([(-130, 0), (-110, -150), (110, -150), (130, 0), (-130, 0)])
    scr = P([(-60, -150), (-50, -240), (90, -240), (80, -150)])
    c.drawPath(_path(body), paint(WHITE, k)); c.drawPath(_path(scr), paint(SP_GR, 0.5 * k))
    ink(c, [wob(body, 941, 0.5), wob(scr, 942, 0.4)], k, MK, 6)
    if k >= 1:
        for r_ in range(2):
            for q in range(4): c.drawCircle(x + (-75 + q * 50) * s, y + (-95 + r_ * 45) * s, 9 * s, paint(MK))


def risingline(c, x, y, w, h, t, t0, label, col=GR):
    k = pr(t, t0, 0.8)
    if k <= 0: return
    pts = [(x + w * i / 8, y - h * (0.15 + 0.85 * (i / 8) ** 1.4) + (14 if i % 2 else 0)) for i in range(9)]
    ink(c, [[(x, y + 10), (x + w + 20, y + 10)], [(x, y + 10), (x, y - h - 20)]], 1, MK, 5, pen_=False)
    ink(c, [pts], k, col, 9, pen_=False)
    if k >= 1: mtext(c, label, x + w / 2, y + 70, 44, col, pr(t, t0 + 0.8, 0.3), "pm")


def yearcard(c, x, y, t, t0, text, col=MK, size=64, new=None, t_sw=1e9):
    """a small torn-off calendar page with the year/month written on (rubbed and rewritten for a time jump)"""
    k = pop_(t, t0, 0.3, 1.5)
    if k <= 0: return
    f = font("pm", size); wv = max(tw(f, text), tw(f, new or "")) + 60
    c.save(); c.translate(x, y); c.scale(k, k)
    rr = R.MakeXYWH(-wv / 2, -size, wv, size * 1.6)
    c.drawRect(rr, paint(WHITE)); c.drawRect(R.MakeXYWH(-wv / 2, -size, wv, 22), paint(RD, 0.8)); c.drawRect(rr, stroke(MK, 5))
    c.restore()
    if k >= 1: rubtext(c, x, y + size * 0.42, text, new, t, t_sw, size, col)


_say0 = say
_CUR = [None]


def say(c, t, t0, small, big, col=MK, t1=None, size=170, y=640, **kw):
    """board two-tier caption; sits 60 px lower on shots that show the step map so the map never touches it"""
    if _CUR[0] in _MAP: y += 60
    _say0(c, t, t0, small, big, col, t1, size, y, **kw)


# ---------------------------------------------------------------- shots
SHOTLIST = [("S_i1", 0.0, "cut"), ("S_i2", L0("i2") - 0.1, "wipe"), ("S_i3", L0("i3") - 0.1, "panR"), ("S_i4", L0("i4") - 0.1, "wipe"),
            ("S_i5", L0("i5") - 0.1, "panL"), ("S_i7", L0("i7") - 0.1, "wipe"),
            ("S_a1", L0("a1") - 0.1, "wipe"), ("S_a2", L0("a2") - 0.1, "wipe"), ("S_a3", L0("a3") - 0.1, "wipe"), ("S_a4", L0("a4") - 0.1, "cut"),
            ("S_a5", L0("a5") - 0.1, "panR"), ("S_b1", L0("b1") - 0.1, "wipe"), ("S_b3", L0("b3") - 0.1, "wipe"), ("S_b4", L0("b4") - 0.1, "wipe"),
            ("S_b5", L0("b5") - 0.1, "wipe"), ("S_c1", L0("c1") - 0.1, "panL"), ("S_c3", L0("c3") - 0.1, "wipe"), ("S_c4", L0("c4") - 0.1, "wipe"),
            ("S_d1", L0("d1") - 0.1, "panR"), ("S_d2", L0("d2") - 0.1, "wipe"), ("S_d3", L0("d3") - 0.1, "wipe"),
            ("S_t1", L0("t1") - 0.1, "wipe"), ("S_end", L0("z1") - 0.1, "wipe")]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
_TALLY = [0.0]   # value set by each shot (OWNED IN TOKYO %)


def S_i1(c, t):
    """frame 0: the store between DALLAS (left) and TOKYO (right), dashed arrow already drawn, tag OWNER: TOKYO, counter at 100 %, pulsing ?"""
    to_ = TT("i1", "owned", 0.3)
    spot(c, 540, 1130, 330, SP_TOK, 1.0, seed=3)
    citypin(c, DAL_X, 1250, t, -2.0, "DALLAS", OR); citypin(c, TOK_X, 1250, t, -2.0, "TOKYO", BLU)
    dash_line(c, (DAL_X + 40, 950), (TOK_X - 40, 950), 1.0, LIGHT, 6)
    if t > to_ - 0.2: arrow_m(c, (DAL_X + 40, 950), (TOK_X - 50, 950), pr(t, to_ - 0.2, 0.6), BLU, 9, bend=-0.25)
    store(c, 540, 1330, t, -2.0, 0.85, owner="OWNER: TOKYO", ocol=BLU)
    if t > to_: ink(c, [wob([(420, 1460), (660, 1456)], 11, 1.0)], pr(t, to_, 0.35), RD, 8, pen_=False)
    q = 1 + 0.12 * math.sin(t * 7)
    mtext(c, "?", 860, 860, int(100 * q), RD, 1, "pm")
    if t < L1("i1"): pen(c, 800 + 20 * math.sin(t * 3), 820 + 10 * math.cos(t * 4))
    _TALLY[0] = 100.0
    say(c, t, -2.0, "america's 7-eleven is", "OWNED IN TOKYO", BLU, under=RD, size=150)
    note(c, t, 0.4, "SEVEN & i HOLDINGS (TOKYO) OWNS 100% OF 7-ELEVEN, INC. SINCE NOV 2005")


def S_i2(c, t):
    t0 = SHOT["S_i2"]["start"]; tm = TT("i2", "meeting.", 0.3)
    spot(c, 540, 1120, 360, SP_PK, pr(t, t0, 0.4), seed=5)
    marks = [("x", t0 + 0.2 + i * 0.07) for i in range(26)]
    c.save(); c.translate(360, 1110); c.scale(0.72, 0.72); c.translate(-360, -1110); calendar_m(c, 360, 1110, t, t0 + 0.05, marks); c.restore()
    phone_m(c, 820, 1110, t, t0 + 0.3, 0.7, screen=lambda c_, cx, cy, w_, h_: (mtext(c_, "NO", cx, cy - 10, 48, RD, pr(t, t0 + 0.8, 0.3), "pm"), mtext(c_, "REPLY", cx, cy + 50, 48, RD, pr(t, t0 + 0.9, 0.3), "pm")), buzz_t=t0 + 0.5)
    if t > tm - 0.3: mtext(c, "1 YEAR+", 360, 1340, 84, RD, pr(t, tm - 0.3, 0.4), "pm", pen_=True)
    _TALLY[0] = 100.0
    say(c, t, t0 + 0.08, "the same company once couldn't get", "A MEETING", RD, under=RD)


def S_i3(c, t):
    t0 = SHOT["S_i3"]["start"]; ty = TT("i3", "seventy-three.", 0.3); tw_ = TT("i3", "want", 0.3)
    spot(c, 560, 1150, 360, SP_TOK, pr(t, t0, 0.4), seed=7)
    citypin(c, TOK_X, 940, t, t0 - 3, "TOKYO", BLU)
    desk_m(c, 600, 1300, t, t0 + 0.1, "ITO-YOKADO", "supermarkets")
    hero(c, 290, FLOOR, 1.0, POSES["point"] if t > tw_ else POSES["stand"], Face("open", "smile", look=(1, 0)), t)
    if t > tw_ - 0.3:
        speech(c, 330, 960, 300, 100, "THOSE STORES!", pop_(t, tw_ - 0.3), 40, OR, tail=-1)
    yearcard(c, 640, 960, t, ty - 0.4, "1973", MK, 60)
    _TALLY[0] = 100.0 * (1 - eio(pr(t, ty - 0.3, 1.2)))
    say(c, t, t0 + 0.08, "you're a planner in tokyo", "1973", BLU, under=BLU, size=190)


def S_i4(c, t):
    t0 = SHOT["S_i4"]["start"]; tt_ = TT("i4", "Three", 0.3); tw_ = TT("i4", "whole", 0.3)
    spot(c, 540, 1140, 360, SP_YE, pr(t, t0, 0.4), seed=9)
    sticky_m(c, 230, 1010, t, t0 + 0.1, "MEETING?", 0.7, -6, RD)
    if t > tt_ - 0.2: dash_line(c, (330, 1060), (580, 1160), pr(t, tt_ - 0.2, 0.8), MK, 6)
    for i in range(3):
        tk = tt_ + i * 0.3
        if t > tk: mtext(c, str(i + 1), 360 + i * 95, 1200 - i * 40 + 120, 64, RD, pr(t, tk, 0.25), "pm")
    store(c, 760, 1330, t, t0 + 0.2, 0.75, owner="OWNER: YOU?", ocol=OR)
    if t > tw_: ink(c, [wob(circ_pts(760, 1150, 210, -150, 215, 40, ry=230), 13, 1.2)], pr(t, tw_, 0.4), OR, 8, pen_=False)
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "three moves to", "OWN IT ALL", OR, under=OR)


def S_i5(c, t):
    t0 = SHOT["S_i5"]["start"]; t6 = L0("i6"); ti = TT("i5", "ice", 0.3)
    spot(c, 520, 1160, 370, SP_DAL, pr(t, t0, 0.4), seed=11)
    citypin(c, DAL_X, 960, t, t0 + 0.05, "DALLAS", OR)
    yearcard(c, 720, 900, t, t0 + 0.4, "1927", MK, 56)
    ice_m(c, 540, 1360, t, ti - 0.3, 1.3)
    for i, kind in enumerate(("milk", "eggs", "bread")):
        tk = TT("i6", ("Milk,", "eggs", "bread,")[i], 0.3) - 0.15
        if t > tk: grocery_m(c, 430 + i * 110, 1220 - 70 * 1.3 - (10 if kind == "milk" else 0), kind, pop_(t, tk, 0.3, 1.8))
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "where the stores started", "AN ICE COMPANY", OR, t1=t6 - 0.25, under=OR, size=150)
    say(c, t, t6 - 0.2, "sold off the ice dock", "MILK, EGGS, BREAD", BLU, under=BLU, size=140)
    note(c, t, t0 + 0.6, "BRITANNICA · HANDBOOK OF TEXAS (TSHA) · DALLAS, 1927", t1=t6)
    note(c, t, t6 + 0.3, "THE IDEA OF EMPLOYEE JOHN JEFFERSON GREEN (ENCYCLOPEDIA.COM)")


def S_i7(c, t):
    t0 = SHOT["S_i7"]["start"]; th = TT("i7", "hours.", 0.3); te = TT("i7", "eleven", 0.3)
    spot(c, 540, 1150, 360, SP_YE, pr(t, t0, 0.4), seed=13)
    store(c, 330, 1400, t, t0 - 3, 0.75, sign="TOTE'M", sign_new="7-ELEVEN", sign_sw=th - 0.2)
    clock_m(c, 790, 1080, t, t0 + 0.1, 150, h0=7.0, hours=4.0, fill_t=TT("i7", "seven.", 0.2), col=OR)
    if t > TT("i7", "seven.", 0.2): mtext(c, "7 AM", 650, 900, 48, OR, pr(t, TT("i7", "seven.", 0.2), 0.3), "pm")
    if t > te - 0.2: mtext(c, "11 PM", 650, 1290, 48, PU, pr(t, te - 0.2, 0.3), "pm")
    if t > th: mtext(c, "1946", 330, 980, 60, MK, pr(t, th, 0.3), "pm", pen_=True)
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "named after its hours", "7 AM TO 11 PM", OR, under=PU, size=150)
    note(c, t, t0 + 0.6, "BRITANNICA: RENAMED 7-ELEVEN IN 1946 \"TO CALL ATTENTION TO THEIR EXTENDED HOURS\"")


def S_a1(c, t):
    t0 = SHOT["S_a1"]["start"]
    spot(c, 540, 1130, 360, SP_PU, pr(t, t0, 0.4), seed=21)
    license_m(c, 540, 1110, t, t0 + 0.1, 1.35, 0.0, -4, "LICENSE")
    mtext(c, "TO RUN THE STORES IN JAPAN", 540, 1420, 44, PU, pr(t, t0 + 0.6, 0.3), "kb")
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "move one", "GET THE LICENSE", PU, under=PU, size=150)


def S_a2(c, t):
    t0 = SHOT["S_a2"]["start"]; ti = TT("a2", "isn't", 0.3); ty = TT("a2", "year", 0.3)
    spot(c, 360, 1160, 300, SP_DAL, pr(t, t0, 0.4), seed=23)
    citypin(c, DAL_X, 1350, t, t0 - 3, "DALLAS", OR)
    if t > ti - 0.3: speech(c, 380, 990, 420, 110, "NOT INTERESTED", pop_(t, ti - 0.3), 44, RD, tail=-1)
    marks = [("x", ty - 0.5 + i * 0.05) for i in range(24)]
    c.save(); c.translate(720, 1250); c.scale(0.55, 0.55); c.translate(-720, -1250); calendar_m(c, 720, 1250, t, t0 + 0.2, marks); c.restore()
    if t > ty: mtext(c, "1 YEAR+", 720, 1450, 70, RD, pr(t, ty, 0.3), "pm", pen_=True)
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "southland says no · just to start talks", "1 YEAR+", RD, under=RD)
    note(c, t, t0 + 0.6, "SEVEN & i: SOUTHLAND \"HAD NO INTEREST IN ENTERING THE JAPANESE MARKET\"")


def S_a3(c, t):
    t0 = SHOT["S_a3"]["start"]; tq = TT("a3", "words,", 0.3); to_ = TT("a3", "opposed", 0.3)
    spot(c, 540, 1140, 380, SP_PK, pr(t, t0, 0.4), seed=25)
    if t < tq - 0.2:
        heads_m(c, 140, 900, 1240, t, t0 + 0.1, 11, LIGHT)
        if t > t0 + 0.9: cross(c, 120, 1150, 920, 1290, pr(t, t0 + 0.9, 0.4), RD, 12)
        mtext(c, "AT HOME", 520, 1400, 54, MK, pr(t, t0 + 0.4, 0.3), "pm")
    else:
        quote_m(c, 520, 1150, t, tq - 0.2, ["99% of people", "opposed the idea"], "TOSHIFUMI SUZUKI · LED THE PROJECT")
        if t > to_: ink(c, [wob([(300, 1170), (760, 1166)], 15, 1.0)], pr(t, to_, 0.35), RD, 8, pen_=False)
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "and at home?", "99% SAID NO", RD, under=RD)
    note(c, t, tq, "QUOTE: SEVEN & i HOLDINGS, TOSHIFUMI SUZUKI MEMORIAL PAGE (2026)")


def S_a4(c, t):
    t0 = SHOT["S_a4"]["start"]; tn = TT("a4", "ninety-nine.", 0.3)
    spot(c, 540, 1180, 330, SP_YE, pr(t, t0, 0.4), seed=27)
    heads_m(c, 400, 960, 1250, t, t0 - 3, 7, LIGHT)
    hero(c, 230, FLOOR, 1.1, POSES["shrug"], Face("open", "o" if t > tn else "smile", look=(0, 0)), t)
    if t > tn - 0.2:
        ink(c, [wob(circ_pts(493, 1215, 60, -90, 270, 30), 17, 1.0)], pr(t, tn - 0.2, 0.35), OR, 7, pen_=False)
        mtext(c, "ME", 493, 1110, 56, OR, pr(t, tn, 0.3), "pm")
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.04, "honestly?", "I'D SAY NO TOO", OR, under=OR, size=150)


def S_a5(c, t):
    t0 = SHOT["S_a5"]["start"]; tf = TT("a5", "first", 0.3); ts = TT("a5", "sunglasses.", 0.2)
    spot(c, 560, 1130, 370, SP_TOK, pr(t, t0, 0.4), seed=31)
    citypin(c, TOK_X, 920, t, t0 - 3, "TOKYO", BLU)
    store(c, 380, 1300, t, t0 + 0.05, 0.75, owner="DALLAS", new="TOKYO (LICENSE)", t_sw=tf, ocol=OR, ncol=BLU)
    yearcard(c, 380, 880, t, t0 + 0.4, "MAY 1974", MK, 48)
    if t > ts - 0.4:
        sunglasses_m(c, 780, 1260, t, ts - 0.4, 0.8, MK, "FIRST SALE")
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "the first store opens · first sale?", "SUNGLASSES", BLU, under=OR, size=150)
    note(c, t, t0 + 0.6, "SEVEN & i: TOYOSU STORE, TOKYO, MAY 1974 · JAPAN TIMES (17 MAY 2024): FIRST ITEM SOLD")


def S_b1(c, t):
    t0 = SHOT["S_b1"]["start"]; t2 = L0("b2"); to_ = TT("b1", "open", 0.3); tn = TT("b2", "one.", 0.2)
    spot(c, 560, 1140, 370, SP_GR, pr(t, t0, 0.4), seed=41)
    manual_m(c, 600, 1150, t, t0 + 0.05, 1.3, "MANUAL", pr(t, to_, 0.7), BLU)
    hero(c, 200, FLOOR, 0.9, POSES["point"], Face("open", "flat" if t > tn else "smile", look=(1, 0)), t)
    if t > tn: mtext(c, "NO SECRET", 600, 1430, 64, RD, pr(t, tn, 0.35), "pm", pen_=True)
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "move two · find the secret", "IN THE MANUALS", GR, t1=t2 - 0.2, under=GR, size=150)
    say(c, t, t2 - 0.15, "the secret?", "THERE ISN'T ONE", RD, under=RD, size=150)
    note(c, t, t2 + 0.3, "SEVEN & i: AFTER STUDYING THE MANUALS, THE TEAM \"COULD FIND NO 'SECRET'\"")


def S_b3(c, t):
    t0 = SHOT["S_b3"]["start"]; ty = TT("b3", "yourselves.", 0.3)
    spot(c, 540, 1140, 360, SP_GR, pr(t, t0, 0.4), seed=43)
    notebook_m(c, 260, 1150, t, t0 + 0.05, 3, None)
    mtext(c, "ACCOUNTING", 260, 1360, 40, GR, pr(t, t0 + 0.5, 0.3), "pm")
    if t > t0 + 0.8: ink(c, [[(200, 990), (240, 1030), (320, 940)]], pr(t, t0 + 0.8, 0.3), GR, 10, pen_=False)
    rr = R.MakeXYWH(470, 960, 440, 380)
    if t > ty - 0.6:
        k = pr(t, ty - 0.6, 0.4); c.drawRect(rr, paint(WHITE, k)); ink(c, [wob([(470, 960), (910, 960), (910, 1340), (470, 1340), (470, 960)], 45, 0.6)], k, MK, 6)
        mtext(c, "EVERYTHING", 690, 1120, 56, BLU, pr(t, ty - 0.3, 0.4), "pm", pen_=True)
        mtext(c, "ELSE: OURS", 690, 1200, 56, BLU, pr(t, ty, 0.4), "pm", pen_=True)
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "apart from the accounting", "BUILD IT ALL", BLU, under=GR)
    note(c, t, t0 + 0.6, "SEVEN & i: BUILT \"VIRTUALLY EVERY ASPECT\" THEMSELVES, \"APART FROM THE ACCOUNTING SYSTEM\"")


def S_b4(c, t):
    t0 = SHOT["S_b4"]["start"]; tr_ = TT("b4", "Rice", 0.3); tt_ = TT("b4", "truck", 0.3); tc = TT("b4", "computer", 0.3)
    spot(c, 540, 1160, 380, SP_YE, pr(t, t0, 0.4), seed=47)
    riceball_m(c, 230, 990, t, tr_ - 0.3, 0.85)
    mtext(c, "1978", 230, 1150, 42, MK, pr(t, tr_ + 0.2, 0.3), "pm")
    if t > tt_ - 0.4:
        drive = 90 * eio(pr(t, tt_ + 0.3, 1.2))
        truck_m(c, 620, 1090, t, tt_ - 0.4, 0.75, "MILK", BLU, drive)
        mtext(c, "MANY DAIRIES · 1 TRUCK", 640, 1150, 36, MK, pr(t, tt_ + 0.2, 0.3), "kb")
    if t > tc - 0.4:
        till_m(c, 380, 1440, t, tc - 0.4, 0.75)
        if t > tc: receipt_m(c, 570, 1240, t, tc, 60, grow_t=tc, grow=150)
        mtext(c, "EVERY SALE", 800, 1340, 44, GR, pr(t, tc + 0.3, 0.3), "pm"); mtext(c, "LOGGED · 1983", 800, 1395, 36, GR, pr(t, tc + 0.4, 0.3), "kb")
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "made for your shelves", "RICE BALLS", MK, t1=tt_ - 0.4, under=OR)
    say(c, t, tt_ - 0.35, "one truck, several dairies", "SHARED TRUCK", BLU, t1=tc - 0.4, under=BLU, size=150)
    say(c, t, tc - 0.35, "a computer at the counter", "EVERY SALE", GR, under=GR)
    note(c, t, t0 + 0.6, "SEVEN & i: OWN RICE BALLS 1978 · COMBINED DELIVERY 1980 · POS SYSTEM 1983")


def S_b5(c, t):
    t0 = SHOT["S_b5"]["start"]; tm = TT("b5", "more", 0.3)
    spot(c, 300, 1160, 230, SP_TOK, pr(t, t0, 0.4), seed=51); spot(c, 760, 1160, 230, SP_DAL, pr(t, t0 + 0.15, 0.4), seed=52)
    store_stack(c, 300, 1340, 26 if t > tm else 14, t, t0 + 0.2, BLU, 0.05)
    store_stack(c, 760, 1340, 24, t, t0 + 0.3, OR, 0.05)
    mtext(c, "JAPAN", 300, 1430, 48, BLU, pr(t, t0 + 0.3, 0.3), "pm"); mtext(c, "US + CANADA", 760, 1430, 48, OR, pr(t, t0 + 0.4, 0.3), "pm")
    if t > tm: mtext(c, "6,269", 300, 900, 58, BLU, pr(t, tm, 0.3), "pm", pen_=True); mtext(c, "5,986", 760, 900, 58, OR, pr(t, tm + 0.2, 0.3), "pm", pen_=True)
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "by the mid-nineties", "JAPAN HAS MORE", BLU, under=BLU, size=150)
    note(c, t, t0 + 0.6, "SOUTHLAND 10-K (SEC), END OF 1995: 6,269 IN JAPAN VS 5,986 IN THE US + CANADA")


def S_c1(c, t):
    t0 = SHOT["S_c1"]["start"]; t2 = L0("c2"); tf = TT("c2", "family", 0.3); th = TT("c2", "hostile", 0.3)
    spot(c, 520, 1160, 370, SP_DAL, pr(t, t0, 0.4), seed=61)
    citypin(c, DAL_X, 930, t, t0 - 3, "DALLAS", OR)
    store(c, 520, 1380, t, t0 - 3, 0.75, owner="DALLAS", ocol=OR)
    if t > t2:
        yearcard(c, 820, 900, t, t2, "1987", MK, 56)
    if t > tf - 0.3:   # the family's roof drawn over the store
        k = pr(t, tf - 0.3, 0.6)
        ink(c, [wob([(250, 1180), (520, 950), (790, 1180)], 63, 1.0)], k, PU, 12, pen_=False)
        mtext(c, "FAMILY", 520, 1050, 46, PU, pr(t, tf, 0.3), "pm")
    if t > th - 0.5:
        u = pr(t, th - 0.5, 0.6); bx = 1000 - 120 * eio(u) + (30 * pr(t, th + 0.1, 0.2) if t > th + 0.1 else 0)
        hand_side = [(bx, 1180), (bx - 70, 1170), (bx - 90, 1210), (bx - 60, 1240), (bx, 1240)]
        ink(c, [hand_side], 1, RD, 7, pen_=False); mtext(c, "TAKEOVER", bx - 20, 1300, 34, RD, pr(t, th - 0.2, 0.3), "pm")
        ink(c, [wob([(820, 1120), (820, 1340)], 64, 1.2)], pr(t, th - 0.3, 0.3), MK, 10, pen_=False)
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "move three · back in dallas", "THE OTHER WAY", OR, t1=t2 - 0.2, under=OR, size=150)
    say(c, t, t2 - 0.15, "to stop a hostile takeover", "GOING PRIVATE", PU, under=PU, size=150)
    note(c, t, t2 + 0.4, "HANDBOOK OF TEXAS (TSHA): THE FAMILY'S BUYOUT FENDED OFF A HOSTILE TAKEOVER")


def S_c3(c, t):
    t0 = SHOT["S_c3"]["start"]; tb = TT("c3", "borrowed.", 0.3)
    spot(c, 540, 1180, 360, SP_DAL, pr(t, t0, 0.4), seed=65)
    store(c, 540, 1080, t, t0 - 3, 0.6, owner=None)
    coinpile_m(c, 520, 1400, t, t0 + 0.2, 9)
    if t > t0 + 0.9: tagpill_m(c, 820, 1330, "$5 BILLION", pop_(t, t0 + 0.9), RD, 46)
    if t > tb - 0.2:
        rr = R.MakeXYWH(390, 1250, 290, 200); p = skia.Path(); p.addRect(rr)
        hatch(c, p, pr(t, tb - 0.2, 0.6), RD, gap=16, w=6, bbox=(390, 1250, 680, 1450), a=0.6)
        mtext(c, "BORROWED", 300, 1260, 46, RD, pr(t, tb, 0.3), "pm", pen_=True)
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "most of it borrowed", "~$5 BILLION", RD, under=RD)
    note(c, t, t0 + 0.6, "AP, 7 MAR 1991: THE \"$5 BILLION\" LEVERAGED BUYOUT OF 1987")


def S_c4(c, t):
    t0 = SHOT["S_c4"]["start"]; tb = TT("c4", "Bankruptcy.", 0.2); tr_ = TT("c4", "rescue", 0.3)
    spot(c, 520, 1160, 370, SP_DAL, pr(t, t0, 0.4), seed=67)
    store(c, 440, 1330, t, t0 - 3, 0.75, owner="DALLAS", ocol=OR)
    yearcard(c, 760, 900, t, t0 + 0.05, "OCT 1990", MK, 48)
    if t > tb - 0.1: stamp_m(c, 440, 1230, "CHAPTER 11", pr(t, tb - 0.1, 0.25), RD, -7, 56)
    if t > tr_ - 0.3:
        u = eio(pr(t, tr_ - 0.3, 0.8))
        envelope_m(c, 980 - 180 * u, 1180, t, tr_ - 0.3, 0.7, "PLAN")
        mtext(c, "RESCUE · FROM TOKYO", 780, 1320, 36, BLU, pr(t, tr_ + 0.3, 0.3), "pm")
        arrow_m(c, (980, 1050), (870, 1130), pr(t, tr_, 0.4), BLU, 6, bend=0.2)
    _TALLY[0] = 0.0
    say(c, t, t0 + 0.08, "october 1990", "BANKRUPTCY", RD, t1=tr_ - 0.4, under=RD)
    say(c, t, tr_ - 0.35, "but the rescue is already", "LINED UP", BLU, under=BLU)
    note(c, t, t0 + 0.5, "SOUTHLAND 10-K (SEC): CHAPTER 11, OCT 1990 · AP: DEAL AGREED MAR 1990, \"PREPACKAGED\" PLAN")


def S_d1(c, t):
    t0 = SHOT["S_d1"]["start"]; ts = TT("d1", "seventy", 0.3); tc = TT("d1", "thirty", 0.3)
    spot(c, 540, 1160, 370, SP_TOK, pr(t, t0, 0.4), seed=71)
    store(c, 540, 1330, t, t0 - 3, 0.85, owner="DALLAS", new="TOKYO 70%", t_sw=ts - 0.2, ocol=OR, ncol=BLU)
    yearcard(c, 240, 900, t, t0 + 0.05, "MAR 1991", MK, 46)
    if t > tc - 0.4: tagpill_m(c, 820, 950, "$430M", pop_(t, tc - 0.4), GR, 56)
    _TALLY[0] = 70.0 * eio(pr(t, ts - 0.3, 1.2))
    say(c, t, t0 + 0.08, "your side buys about", "70% FOR $430M", BLU, under=BLU, size=140)
    note(c, t, t0 + 0.6, "SOUTHLAND 10-K (SEC): ~70% TO ITO-YOKADO + SEVEN-ELEVEN JAPAN, $430M CASH, 5 MAR 1991")


def S_d2(c, t):
    t0 = SHOT["S_d2"]["start"]; tf = TT("d2", "Fourteen", 0.3); tr_ = TT("d2", "rest.", 0.2)
    spot(c, 540, 1160, 370, SP_TOK, pr(t, t0, 0.4), seed=73)
    risingline(c, 120, 1100, 260, 200, t, t0 + 0.1, "PROFIT '93", GR)
    store(c, 690, 1330, t, t0 - 3, 0.8, owner="TOKYO 70%", new="TOKYO 100%", t_sw=tr_ - 0.2, ocol=BLU, ncol=BLU)
    yearcard(c, 690, 870, t, tf - 0.3, "1991", MK, 52, new="2005", t_sw=tf + 0.5)
    _TALLY[0] = 70.0 + 30.0 * eio(pr(t, tr_ - 0.3, 1.0))
    say(c, t, t0 + 0.08, "back in profit · then", "ALL OF IT", BLU, under=GR)
    note(c, t, t0 + 0.6, "SEVEN & i: PROFIT 1993 · SEVEN-ELEVEN JAPAN TENDER OFFER, NOV 2005")


def S_d3(c, t):
    t0 = SHOT["S_d3"]["start"]; tj = TT("d3", "twenty-two", 0.3); tn = TT("d3", "thirteen", 0.3)
    spot(c, 300, 1150, 240, SP_TOK, pr(t, t0, 0.4), seed=81); spot(c, 770, 1150, 240, SP_DAL, pr(t, tn - 0.6, 0.4), seed=82)
    store_stack(c, 300, 1360, 40, t, tj - 0.8, BLU, 0.035, cols=6)
    if t > tn - 0.6: store_stack(c, 770, 1360, 23, t, tn - 0.6, OR, 0.035, cols=6)
    mtext(c, "JAPAN", 300, 1440, 48, BLU, pr(t, t0 + 0.2, 0.3), "pm")
    if t > tj: mtext(c, "~22,000", 300, 830, 64, BLU, pr(t, tj, 0.3), "pm", pen_=True)
    if t > tn - 0.6: mtext(c, "US + CANADA", 770, 1440, 48, OR, pr(t, tn - 0.6, 0.3), "pm")
    if t > tn: mtext(c, "~13,000", 770, 1060, 64, OR, pr(t, tn, 0.3), "pm", pen_=True)
    _TALLY[0] = 100.0
    say(c, t, t0 + 0.08, "today, japan has about", "22,000 STORES", BLU, under=BLU, size=150)
    note(c, t, t0 + 0.6, "SEVEN & i 2026: JAPAN 21,927 (FEB 2026) · 7-ELEVEN, INC. US + CANADA 12,712 (DEC 2025)")


def S_t1(c, t):
    t0 = SHOT["S_t1"]["start"]; tc = TT("t1", "Check", 0.3); tl = TT("t1", "learns,", 0.3)
    spot(c, 540, 1160, 370, SP_GR, pr(t, t0, 0.4), seed=91)
    hero(c, 220, FLOOR, 1.0, POSES["hold"], Face("open", "smile", look=(1, 0)), t)
    extra(c, 860, FLOOR, 1.0, POSES["hold"], Face("open", "smile", look=(-1, 0)), t, flip=True, scarf=BLU)
    u = eio(pr(t, t0 + 0.3, 0.9))
    license_m(c, 330 + 170 * u, 1330, t, t0 + 0.05, 0.7, 1.0, -4, "LICENSE")
    if t > tc - 0.3:
        notebook_m(c, 700, 960, t, tc - 0.3, 4, None)
        magnifier(c, 640, 900, 70, pop_(t, tc, 0.3))
        mtext(c, "WHAT ARE", 700, 1170, 40, RD, pr(t, tc, 0.3), "pm"); mtext(c, "THEY LEARNING?", 700, 1220, 40, RD, pr(t, tc + 0.15, 0.3), "pm")
    if t > tl: ink(c, [wob(circ_pts(700, 1030, 190, -150, 215, 40, ry=240), 93, 1.3)], pr(t, tl, 0.4), RD, 7, pen_=False)
    _TALLY[0] = 100.0
    say(c, t, t0 + 0.08, "licensing your idea abroad?", "CHECK WHAT THEY LEARN", GR, under=GR, size=120)
    note(c, t, t0 + 0.6, "OUR TAKEAWAY FROM THIS STORY · EDUCATION ONLY")


def S_end(c, t):
    t0 = SHOT["S_end"]["start"]; tz2 = L0("z2"); tl = TT("z1", "License,", 0.4); tk = TT("z1", "keep?", 0.5)
    spot(c, 520, 1120, 320, SP_YE, 1.0, seed=101)
    store(c, 520, 1250, t, t0 - 3, 0.75, owner=None)
    c.save(); c.translate(860, 1200 + 8 * math.sin(t * 2.4)); c.rotate(6 * math.sin(t * 1.7)); c.translate(-860, -1200)
    riceball_m(c, 860, 1200, t, t0 - 3, 0.5)
    c.restore()
    tagpill_m(c, 290, 1390, "LICENSE", pop_(t, tl - 0.2), PU, 58)
    tagpill_m(c, 760, 1390, "KEEP", pop_(t, tk - 0.2), OR, 58)
    for i, (x, tm) in enumerate(((290, tl), (760, tk))):
        if t > tm: ink(c, [wob(circ_pts(x, 1380, 170, -150, 215, 40, ry=80), 95 + i, 1.4)], pr(t, tm, 0.35), MK, 7, pen_=False)
    _TALLY[0] = 100.0
    say(c, t, t0 + 0.08, "your idea, abroad?", "LICENSE OR KEEP?", MK, t1=tz2 - 0.3, under=OR, size=150)
    say(c, t, tz2 - 0.25, "send it to the friend who lives on snacks", "SAVE THIS", BLU, under=OR)
    note(c, t, t0 + 0.6, "COMMENT ONE WORD · EDUCATION ONLY")


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}
SURF = surface()
IMPACTS = [(TT("c4", "Bankruptcy.", 0.2), 0.14, 5), (TT("b2", "one.", 0.2), 0.10, 3), (TT("d2", "rest.", 0.2), 0.12, 4)]
# the three moves: which one we're on
_MAP = {"S_a1": (0, ()), "S_a2": (0, ()), "S_a3": (0, ()), "S_a4": (0, ()), "S_a5": (0, ()),
        "S_b1": (1, (0,)), "S_b3": (1, (0,)), "S_b4": (1, (0,)), "S_b5": (1, (0,)),
        "S_c1": (2, (0, 1)), "S_c3": (2, (0, 1)), "S_c4": (2, (0, 1)), "S_d1": (2, (0, 1)), "S_d2": (2, (0, 1)), "S_d3": (-1, (0, 1, 2))}
_DONE_AT = {"S_a5": ("a5", "sunglasses.", 0), "S_b5": ("b5", "more", 1), "S_d2": ("d2", "rest.", 2)}
_TOP = {"S_a1": "MOVE 1 OF 3", "S_a2": "MOVE 1 OF 3", "S_a3": "MOVE 1 OF 3", "S_a4": "MOVE 1 OF 3", "S_a5": "MOVE 1 OF 3",
        "S_b1": "MOVE 2 OF 3", "S_b3": "MOVE 2 OF 3", "S_b4": "MOVE 2 OF 3", "S_b5": "MOVE 2 OF 3",
        "S_c1": "MOVE 3 OF 3", "S_c3": "MOVE 3 OF 3", "S_c4": "MOVE 3 OF 3", "S_d1": "MOVE 3 OF 3", "S_d2": "MOVE 3 OF 3", "S_d3": "TODAY",
        "S_t1": "THE LESSON"}


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
    _CUR[0] = sid
    RENDER[sid](c, tt)
    c.restore()
    pill(c, topline(sid))
    if sid in _MAP:
        act, done = _MAP[sid]; done = set(done)
        if sid in _DONE_AT:
            lid, w_, j = _DONE_AT[sid]
            if tt > TT(lid, w_, 0.3): done.add(j)
        stepmap(c, 3, act, tuple(done), min(1, pr(tt, s["start"], 0.3)), x0=230)
    # the live counter: OWNED IN TOKYO (frame 0 pulses it; it falls back to 0 % in 1973 and climbs in 1991 / 2005)
    v = _TALLY[0]; pulse = (sid == "S_i1")
    tally(c, v, 1.0, falling=(v < 1 and sid in ("S_i3",)), x=780 if sid in _MAP else 540, y=372 if sid in _MAP else 380,
          label="OWNED IN TOKYO", fmt="{:.0f}%")
    if pulse:
        k = 0.5 + 0.5 * math.sin(tt * 6)
        c.drawRoundRect(R.MakeXYWH(540 - 175, 380 - 36, 350, 72), 36, 36, stroke(RD, 3 + 3 * k, 0.6))
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


def _pan(f, prev, p, direction):
    """camera pans across the board: direction +1 = toward Tokyo (content moves left), -1 = toward Dallas.
    Pill + counter band (top 430 px) stays put; a light motion smear sells the move."""
    u = eio(p); sh = int(W * u)
    out = f.copy()
    if direction > 0:
        out[430:, : W - sh] = prev[430:, sh:]; out[430:, W - sh:] = f[430:, : sh] if sh > 0 else out[430:, W - sh:]
    else:
        out[430:, sh:] = prev[430:, : W - sh]; out[430:, :sh] = f[430:, W - sh:] if sh > 0 else out[430:, :sh]
    if 0.05 < p < 0.95:
        k = 9; out[430:] = sum(np.roll(out[430:], i * direction * -6, axis=1) for i in range(k)) / k
    return out


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); dt = t - sh["start"]
    if i > 0 and sh["trans"] == "wipe" and dt < 0.34:
        prv = rs(SHOTS[i - 1]["id"], sh["start"] - 1e-3, n); f = _eraser(f, prv, dt / 0.34)
    elif i > 0 and sh["trans"] in ("panR", "panL") and dt < 0.5:
        prv = rs(SHOTS[i - 1]["id"], sh["start"] - 1e-3, n); f = _pan(f, prv, dt / 0.5, 1 if sh["trans"] == "panR" else -1)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
