# ================= HOW IT WORKS EP 6: paying cash can help pay for someone else's card rewards (whiteboard, 12 Nov 2026).
# Held object: ONE $5 coffee cup whose price tag carries a hatched FEE slice; a MONEY ROUTE map under the pill (4 stops:
# SHOP -> PRICE -> BANK -> YOU) ticks off stop by stop. Opening move (new): frame 0 = cup + $5 tag centre, a cash note left, a card right,
# and a coin already mid-air hopping from the cash side to the card side on a loop, pen hovering over a pulsing "?".
# Visual upgrade (owner 11 Nov "make my video colourful"): COLOUR SPOTS - a big hand-hatched highlighter disc behind the key drawing of
# every shot (the whiteboard cousin of the bright sets' big colour circle), colour-coded by stop: shop = orange, price = yellow,
# bank = purple, you = green, other countries = blue. New drawings: spot, route_map, terminal_m, gift_m, feetag, pricebd_m, coin_hop.
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

GOLD = (236, 176, 40); LIGHT = (150, 156, 170); PINK = (236, 92, 150)
SP_OR = (255, 196, 120); SP_YE = (255, 226, 90); SP_PU = (196, 170, 255); SP_GR = (150, 226, 170); SP_BL = (150, 196, 255); SP_PK = (255, 170, 200)


# ---------------------------------------------------------------- new marker drawings (this episode)
def spot(c, x, y, r, col, k, seed=1, a=0.55):
    """COLOUR SPOT: a big highlighter disc laid in with wide diagonal strokes; pops from the centre"""
    if k <= 0: return
    rr = r * eback(min(1.0, k), 1.3)
    p = skia.Path(); p.addCircle(x, y, rr)
    c.drawCircle(x, y, rr, paint(col, a * 0.55))
    hatch(c, p, 1.0, col, gap=34, w=30, ang=-30, bbox=(x - rr, y - rr, x + rr, y + rr), seed=seed, a=a)


def route_map(c, active, done=(), a=1.0, y=392):
    """the money route under the pill: 4 stops (SHOP, PRICE, BANK, YOU) on a dashed line; active = coloured + bigger, done = ticked"""
    if a <= 0: return
    names = ("SHOP", "PRICE", "BANK", "YOU"); cols = (OR, GOLD, PU, GR); xs = (210, 410, 610, 810)
    for i in range(3):
        x0, x1 = xs[i] + 40, xs[i + 1] - 40
        for j in range(5):
            u0, u1 = j / 5, (j + 0.55) / 5
            c.drawLine(x0 + (x1 - x0) * u0, y - 22, x0 + (x1 - x0) * u1, y - 22, stroke(GR if i in done else LIGHT, 4, a))
    for i, (nm, col, x) in enumerate(zip(names, cols, xs)):
        on = (i == active); r = 30 if on else 22
        c.drawCircle(x, y - 22, r, paint(col if on else WHITE, a))
        c.drawCircle(x, y - 22, r, stroke(MK if on else (col if i in done else LIGHT), 5 if on else 3, a))
        f = font("pm", 30 if on else 24); c.drawString(str(i + 1), x - tw(f, str(i + 1)) / 2, y - 22 + (11 if on else 9), f, paint(WHITE if on else (col if i in done else LIGHT), a))
        mtext(c, nm, x, y + 34, 30 if on else 24, col if (on or i in done) else LIGHT, a, "pm")
        if i in done: ink(c, [[(x + 14, y - 40), (x + 26, y - 28), (x + 50, y - 62)]], 1, GR, 6, pen_=False)


def terminal_m(c, x, y, t, t0, s=1.0, beep_t=None):
    """a small card terminal on the counter; screen flashes green on the tap, contactless arcs"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    P = lambda pts: _sc(x, y, s, pts)
    body = P([(-70, 0), (-80, -230), (80, -230), (70, 0), (-70, 0)])
    scr = P([(-55, -205), (55, -205), (55, -140), (-55, -140), (-55, -205)])
    c.drawPath(_path(body), paint(WHITE, k))
    if beep_t is not None and t > beep_t: c.drawPath(_path(scr), paint(GR, 0.6 * (1 - pr(t, beep_t + 0.5, 0.6)) + 0.2))
    ink(c, [wob(body, 801, 0.6), wob(scr, 802, 0.4)], k, MK, 6)
    for r_ in range(3):
        for q in range(3):
            c.drawCircle(x + (-34 + q * 34) * s, y + (-105 + r_ * 30) * s, 8 * s, paint(MK, k))
    if beep_t is not None and beep_t < t < beep_t + 0.6:
        u = pr(t, beep_t, 0.6)
        for j in range(3):
            rr = (40 + 30 * j + 40 * u) * s
            c.drawArc(R.MakeXYWH(x - rr, y - 300 * s - rr, 2 * rr, 2 * rr), 220, 100, False, stroke(GR, 5, 1 - u))


def gift_m(c, x, y, t, t0, s=1.0, label="REWARDS", col=PU):
    """a little gift box with a bow, label written under"""
    k = pop_(t, t0, 0.3, 1.6)
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k * s, k * s)
    box = [(-80, -60), (80, -60), (80, 70), (-80, 70), (-80, -60)]; lid = [(-92, -95), (92, -95), (92, -60), (-92, -60), (-92, -95)]
    c.drawPath(_path(box), paint(WHITE)); hatch(c, _path(box), 1, col, gap=16, w=6, bbox=(-80, -60, 80, 70), a=0.5)
    c.drawPath(_path(lid), paint(WHITE)); hatch(c, _path(lid), 1, col, gap=12, w=5, bbox=(-92, -95, 92, -60), a=0.35)
    ink(c, [box, lid, [(0, -95), (0, 70)], [(0, -95), (-40, -140), (-50, -110), (0, -95)], [(0, -95), (40, -140), (50, -110), (0, -95)]], 1, MK, 6, pen_=False)
    c.restore()
    if label: mtext(c, label, x, y + 130 * s, int(42 * s), col, pr(t, t0 + 0.2, 0.3), "pm")


def feetag(c, x, y, t, t0, price="$5", fee_t=None, inside=0.0, s=1.0, col=BLU, tilt=-8, fee_col=RD):
    """the cup's $5 swing tag; from fee_t a hatched FEE slice sits off its right end; inside (0..1) slides it back into the tag"""
    tag_m(c, x, y, price, t, t0, col, tilt, s)
    if fee_t is None or t < fee_t: return
    k = pr(t, fee_t, 0.4)
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    out = (1 - eio(min(1.0, inside))) * 110
    sl = [(70 + out, -60), (90 + out, -60), (140 + out, 0), (90 + out, 60), (70 + out, 60), (70 + out, -60)]
    hatch(c, _path(sl), k, fee_col, gap=10, w=5, bbox=(60 + out, -62, 142 + out, 62), a=0.8)
    ink(c, [sl], k, fee_col, 5, pen_=False)
    mtext(c, "FEE", 100 + out, 105, 34, fee_col, pr(t, fee_t + 0.2, 0.3), "pm")
    c.restore()


def pricebd_m(c, x, y, t, t0, item="COFFEE", price="$5", fee_line="+ CARD FEE", cross_t=None, w=440):
    """a cafe price board: item + price, and a second line (written, then crossed out at cross_t)"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    h = 300; rr = R.MakeXYWH(x - w / 2, y - h / 2, w, h)
    c.drawRoundRect(rr, 16, 16, paint((44, 52, 60), k)); c.drawRoundRect(rr, 16, 16, stroke(MK, 7, k))
    mtext(c, item, x - 70, y - 40, 54, WHITE, pr(t, t0 + 0.2, 0.3), "kb"); mtext(c, price, x + 130, y - 40, 60, SP_YE, pr(t, t0 + 0.35, 0.3), "pm")
    if fee_line:
        mtext(c, fee_line, x, y + 70, 46, (255, 170, 160), pr(t, t0 + 0.5, 0.35), "kb")
        if cross_t is not None and t > cross_t:
            ink(c, [wob([(x - 170, y + 60), (x + 170, y + 50)], 811, 1.0)], pr(t, cross_t, 0.3), RD, 10, pen_=False)


def coin_hop(c, t, x0, x1, y, period=1.1, h=150, r=30, t_start=-9.0):
    """a coin hopping from x0 to x1 on a loop (keeps something moving)"""
    if t < t_start: return
    u = ((t - t_start) % period) / period
    coin(c, x0 + (x1 - x0) * eio(u), y - 4 * h * u * (1 - u), r, spin=t * 6)


def house2(c, x, y, s, t, t0, col, label):
    house_m(c, x, y, s, t, t0, col)
    mtext(c, label, x, y + 60 * s, int(40 * s), col, pr(t, t0 + 0.5, 0.3), "pm")


_say0 = say
_CUR = [None]


def say(c, t, t0, small, big, col=MK, t1=None, size=170, y=640, **kw):
    """board two-tier caption; sits 60 px lower on shots that show the route map so the map never touches it"""
    if _CUR[0] in _MAP: y += 60
    _say0(c, t, t0, small, big, col, t1, size, y, **kw)


# ---------------------------------------------------------------- shots
SHOTLIST = [("S_i1", 0.0, "cut"), ("S_i2", L0("i2") - 0.1, "wipe"), ("S_i3", L0("i3") - 0.1, "wipe"), ("S_i4", L0("i4") - 0.1, "wipe"),
            ("S_a1", L0("a1") - 0.1, "wipe"), ("S_a2", L0("a2") - 0.1, "wipe"), ("S_a3", L0("a3") - 0.1, "wipe"),
            ("S_b1", L0("b1") - 0.1, "wipe"), ("S_c1", L0("c1") - 0.1, "wipe"), ("S_d1", L0("d1") - 0.1, "wipe"),
            ("S_d3", L0("d3") - 0.1, "wipe"), ("S_d4", L0("d4") - 0.1, "wipe"), ("S_d5", L0("d5") - 0.1, "wipe"),
            ("S_e1", L0("e1") - 0.1, "wipe"), ("S_e2", L0("e2") - 0.1, "wipe"), ("S_f2", L0("f2") - 0.1, "wipe"), ("S_f3", L0("f3") - 0.1, "wipe"),
            ("S_t1", L0("t1") - 0.1, "wipe"), ("S_end", L0("z1") - 0.1, "wipe")]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}


def S_i1(c, t):
    """frame 0: cup + $5 tag in the middle, cash left, card right, a coin hopping cash -> card on a loop; '?' + pen"""
    tr_ = TT("i1", "rewards?", 0.85)
    spot(c, 540, 1080, 330, SP_YE, 1.0, seed=3)
    cup_m(c, 540, 1240, t, -2.0, 1.2)
    tag_m(c, 690, 1010, "$5", t, -2.0, BLU, 10, 0.8)
    cash_m(c, 220, 1290, t, -2.0, 0.85, "$5", -8)
    mtext(c, "CASH", 220, 1405, 44, GR, 1, "pm")
    card_m(c, 850, 1280, 230, 1.0, PU, 8)
    mtext(c, "CARD", 850, 1405, 44, PU, 1, "pm")
    coin_hop(c, t, 240, 830, 1220, 1.15, 230, 32, t_start=-0.6)
    if t > tr_ - 0.2: gift_m(c, 850, 1120, t, tr_ - 0.2, 0.7, None)
    q = 1 + 0.12 * math.sin(t * 7)
    mtext(c, "?", 540, 830, int(110 * q), RD, 1, "pm")
    if t < L1("i1"): pen(c, 610 + 20 * math.sin(t * 3), 790 + 10 * math.cos(t * 4))
    say(c, t, -2.0, "paying cash can help pay for", "THEIR REWARDS?", RD, under=RD, size=150)
    note(c, t, -2.0, "EDUCATION ONLY · NOT CARD ADVICE")


def S_i2(c, t):
    t0 = SHOT["S_i2"]["start"]; tb = TT("i2", "guy", 0.6); tt_ = TT("i2", "taps", 0.4)
    spot(c, 540, 1160, 380, SP_OR, pr(t, t0, 0.5), seed=5)
    floor_line(c, t, t0, FLOOR - 160, 120, 960)
    cup_m(c, 470, FLOOR - 160, t, t0 + 0.05, 0.75)
    tag_m(c, 560, FLOOR - 330, "$5", t, t0 + 0.25, BLU, 8, 0.55)
    hero(c, 230, FLOOR, 0.95, POSES["hold"], Face("open", "smile", look=(1, 0)), t)
    cash_m(c, 340, 1150, t, t0 + 0.2, 0.55, "$5", -10)
    if t > tb - 0.4: extra(c, 840, FLOOR, 0.9, POSES["point"] if t > tt_ else POSES["stand"], Face("open", "smile", look=(-1, 0)), t, flip=True, scarf=GR)
    terminal_m(c, 670, FLOOR - 160, t, tb - 0.2, 0.7, beep_t=tt_)
    if t > tt_ - 0.3: card_m(c, 740 - 40 * eio(pr(t, tt_ - 0.3, 0.3)), 1020, 130, pop_(t, tt_ - 0.3), PU, -10)
    say(c, t, t0 + 0.08, "you're buying", "A $5 COFFEE", MK, under=OR)


def S_i3(c, t):
    t0 = SHOT["S_i3"]["start"]; to = TT("i3", "Only", 0.3); tb = TT("i3", "back.", 0.3)
    spot(c, 300, 1150, 240, SP_GR, pr(t, t0, 0.4), seed=7); spot(c, 760, 1150, 240, SP_PU, pr(t, t0 + 0.15, 0.4), seed=8)
    for i, (x, lab, col) in enumerate(((300, "CASH", GR), (760, "CARD", PU))):
        cup_m(c, x, 1300, t, t0 + 0.05 + i * 0.2, 0.9)
        tag_m(c, x + 100, 1080, "$5", t, t0 + 0.3 + i * 0.2, BLU, 8, 0.55)
        mtext(c, lab, x, 1400, 50, col, pr(t, t0 + 0.4 + i * 0.2, 0.3), "pm")
    dash_line(c, (530, 860), (530, 1420), pr(t, t0 + 0.2, 0.5), LIGHT, 6)
    if t > to - 0.2:
        speech(c, 760, 880, 330, 110, "+ REWARDS", pop_(t, to - 0.2), 52, PU, tail=-1)
        mtext(c, "+ 0", 300, 900, 70, LIGHT, pr(t, tb - 0.2, 0.3), "pm")
    say(c, t, t0 + 0.08, "same coffee · same price · only one", "GETS SOMETHING BACK", MK, under=PU, size=120)


def S_i4(c, t):
    t0 = SHOT["S_i4"]["start"]; tf = TT("i4", "Four", 0.3); tw_ = TT("i4", "wallet.", 0.3)
    xs = (190, 400, 610, 820); cols = (SP_OR, SP_YE, SP_PU, SP_GR); names = ("SHOP", "PRICE", "BANK", "YOU")
    pts = [(xs[0], 1120), (xs[1], 980), (xs[2], 1170), (xs[3], 1030)]
    for i in range(3):
        if t > tf - 0.4 + i * 0.25: dash_line(c, pts[i], pts[i + 1], pr(t, tf - 0.4 + i * 0.25, 0.3), MK, 6)
    for i, (x, y) in enumerate(pts):
        tk = tf - 0.5 + i * 0.25
        if t < tk: continue
        spot(c, x, y, 95, cols[i], pr(t, tk, 0.3), seed=20 + i, a=0.7)
        ink(c, [wob(circ_pts(x, y, 80), 30 + i, 0.8)], pr(t, tk, 0.35), MK, 6, pen_=False)
        mtext(c, str(i + 1), x, y + 22, 64, MK, pr(t, tk + 0.1, 0.25), "pm")
        mtext(c, names[i], x, y + 140, 40, MK, pr(t, tk + 0.15, 0.25), "pm")
    if t > tw_ - 0.5: wallet_m(c, xs[3], 1330, t, tw_ - 0.5, 0.5)
    if t < tf - 0.4: cash_m(c, 540, 1100, t, t0, 0.8, "$5", -6)
    say(c, t, t0 + 0.08, "how does your cash get there?", "4 STOPS", MK, under=GR)


def S_a1(c, t):
    t0 = SHOT["S_a1"]["start"]; te = TT("a1", "every", 0.3); ts = TT("a1", "shop.", 0.3)
    spot(c, 540, 1130, 360, SP_OR, pr(t, t0, 0.4), seed=31)
    cup_m(c, 330, 1350, t, t0 - 3, 1.05)
    feetag(c, 560, 1060, t, t0 - 3, "$5", fee_t=ts - 0.4, s=0.95)
    terminal_m(c, 830, 1350, t, t0 + 0.1, 0.65, beep_t=te)
    if t > ts - 0.2: ink(c, [wob([(660, 960), (660, 1180)], 820, 1.0)], pr(t, ts - 0.2, 0.3), RD, 6, pen_=False)
    say(c, t, t0 + 0.08, "every tap", "COSTS THE SHOP", OR, under=OR)


def S_a2(c, t):
    t0 = SHOT["S_a2"]["start"]; to = TT("a2", "one", 0.3); tf = TT("a2", "fees.", 0.3)
    spot(c, 520, 1100, 340, SP_OR, pr(t, t0, 0.4), seed=33, a=0.45)
    cell = 52; x0, y0 = 520 - 5 * cell, 840
    for i in range(100):
        r_, q = divmod(i, 10); bx, by = x0 + q * cell, y0 + r_ * cell
        k = pr(t, t0 + 0.1 + i * 0.01, 0.15)
        if k <= 0: continue
        red = i == 0 and t > to - 0.1; half = i == 1 and t > to + 0.15
        c.drawCircle(bx + cell / 2, by + cell / 2, 20 * k, paint(WHITE))
        c.drawCircle(bx + cell / 2, by + cell / 2, 20 * k, stroke(RD if (red or half) else (205, 160, 40), 4))
        if red: c.drawCircle(bx + cell / 2, by + cell / 2, 17, paint(RD, 0.85))
        if half: c.drawArc(R.MakeXYWH(bx + cell / 2 - 17, by + cell / 2 - 17, 34, 34), 90, 180, True, paint(RD, 0.85))
    if t < tf - 0.3: mtext(c, "EVERY $100 OF CARD SALES", 520, 1415, 46, MK, pr(t, t0 + 0.6, 0.4), "kb")
    else: mtext(c, "$1.57 OF EVERY $100", 520, 1415, 56, RD, pr(t, tf - 0.3, 0.4), "pm", pen_=True)
    say(c, t, t0 + 0.08, "American shops paid about", "1.5% IN FEES", RD, under=RD, size=150)
    note(c, t, t0 + 0.6, "US, 2024 · NILSON REPORT (VIA PRESS RELEASE, MAR 2025)")


def S_a3(c, t):
    t0 = SHOT["S_a3"]["start"]; tb = TT("a3", "billion", 0.3)
    spot(c, 540, 1130, 340, SP_OR, pr(t, t0, 0.4), seed=35)
    for i in range(14):   # little red fee dots pour into the sack
        tk = t0 + 0.1 + i * 0.09
        if t < tk: continue
        u = pr(t, tk, 0.55)
        if u >= 1: continue
        x = 200 + (i * 53) % 640; c.drawCircle(x + (540 - x) * eio(u), 800 + 340 * eio(u), 14, paint(RD, 0.9))
    bag_m(c, 540, 1200, t, t0 + 0.15, "$187B" if t > tb - 0.3 else "", OR, 1.25, None)
    if t > tb: mtext(c, "IN ONE YEAR · 2024", 540, 1420, 46, MK, pr(t, tb, 0.3), "kb")
    say(c, t, t0 + 0.08, "all those card fees", "$187 BILLION", OR, under=OR)
    note(c, t, t0 + 0.6, "NILSON REPORT: US MERCHANT PROCESSING FEES, 2024 ($187.2B)")


def S_b1(c, t):
    t0 = SHOT["S_b1"]["start"]; t2 = L0("b2"); td = TT("b2", "don't", 0.3); tbk = TT("b2", "baked", 0.3)
    spot(c, 540, 1120, 360, SP_YE, pr(t, t0, 0.4), seed=41)
    pricebd_m(c, 520, 1000, t, t0 + 0.05, "COFFEE", "$5", "+ CARD FEE", cross_t=td)
    cup_m(c, 300, 1440, t, t0 + 0.3, 0.6)
    feetag(c, 560, 1310, t, t0 + 0.3, "$5", fee_t=t0 + 0.4, inside=pr(t, tbk - 0.3, 0.6), s=0.8)
    if t > tbk: mtext(c, "INSIDE THE $5", 560, 1460, 44, RD, pr(t, tbk, 0.3), "pm")
    say(c, t, t0 + 0.08, "who covers the fee?", "ONE PRICE", GOLD, t1=tbk - 0.4, under=GOLD)
    say(c, t, tbk - 0.35, "the fee gets", "BAKED IN", RD, under=RD)
    note(c, t, t2, "MOST US SHOPS DON'T ADD A CARD SURCHARGE (SOME DO, ON CREDIT)")


def S_c1(c, t):
    t0 = SHOT["S_c1"]["start"]; t2 = L0("c2"); tbk = TT("c2", "bank", 0.3); tr_ = TT("c2", "rewards.", 0.3)
    spot(c, 560, 1120, 380, SP_PU, pr(t, t0, 0.4), seed=51)
    feetag(c, 210, 900, t, t0 - 3, "$5", fee_t=t0 - 3, s=0.7)
    u = eio(pr(t, t0 + 0.3, max(0.8, tbk - t0 - 0.2)))
    dash_line(c, (300, 960), (420, 1040), pr(t, t0 + 0.2, 0.6), PU, 6)
    fx, fy = 300 + 120 * u, 960 + 80 * u
    c.drawCircle(fx, fy, 24, paint(RD, 0.85)); mtext(c, "FEE", fx, fy - 36, 30, RD, 1, "pm")
    gov_m(c, 560, 1380, t, t0 + 0.2, "BANK", "BEHIND THE CARD", 0.85)
    if t > tr_ - 0.6:
        dash_line(c, (740, 1180), (820, 1080), pr(t, tr_ - 0.6, 0.4), PU, 6)
        gift_m(c, 840, 990, t, tr_ - 0.3, 0.7, "REWARDS")
    say(c, t, t0 + 0.08, "where does the fee go?", "THE BANK", PU, t1=tr_ - 0.4, under=PU)
    say(c, t, tr_ - 0.35, "spent on things like", "REWARDS", PU, under=PU)
    note(c, t, t2 + 0.6, "ST. LOUIS FED, APR 2026: CARD FEES HELP RUN REWARDS PROGRAMS")


def S_d1(c, t):
    t0 = SHOT["S_d1"]["start"]; th = TT("d2", "His", 0.3); tn = TT("d2", "nothing", 0.3)
    spot(c, 360, 1130, 330, SP_GR, pr(t, t0, 0.4), seed=61)
    hero(c, 260, FLOOR, 1.1, POSES["hold"], Face("open", "flat" if t > tn else "smile", look=(1, 0)), t)
    cash_m(c, 400, 1120, t, t0 - 3, 0.55, "$5", -10)
    feetag(c, 400, 880, t, t0 + 0.3, "$5", fee_t=t0 + 0.3, inside=1.0, s=0.7)
    if t > th - 0.3:
        card_m(c, 820, 960, 150, pop_(t, th - 0.3), PU, 8)
        arrow_m(c, (500, 880), (750, 940), pr(t, th, 0.4), RD, 7, bend=-0.2)
    if t > tn - 0.4: wallet_m(c, 740, 1320, t, tn - 0.4, 0.75, empty=True)
    say(c, t, t0 + 0.08, "last stop", "YOU", GR, t1=th - 0.3, under=GR)
    say(c, t, th - 0.25, "your price helped cover it", "NOTHING BACK", RD, under=RD, size=150)


def S_d3(c, t):
    t0 = SHOT["S_d3"]["start"]; td = TT("d3", "Debit", 0.3)
    spot(c, 540, 1110, 360, SP_BL, pr(t, t0, 0.4), seed=71)
    clipboard_m(c, 340, 1130, t, t0 + 0.05, ["MODEL", "2007-08 DATA"], [t0 + 0.6, t0 + 0.9])
    if t > td - 0.3:
        cash_m(c, 780, 980, t, td - 0.3, 0.55, "$", -6)
        card_m(c, 780, 1190, 170, pop_(t, td - 0.1), BLU, 6); mtext(c, "DEBIT", 780, 1200, 40, MK, pr(t, td, 0.3), "pm")
        mtext(c, "= CASH", 780, 1340, 60, GR, pr(t, td + 0.2, 0.3), "pm")
    say(c, t, t0 + 0.08, "Boston Fed economists, 2010", "DEBIT = CASH", BLU, under=BLU, size=150)
    note(c, t, t0 + 0.6, "BOSTON FED PPDP 10-3 (AUG 2010) · CASH = ALL BUT CREDIT CARDS")


def S_d4(c, t):
    t0 = SHOT["S_d4"]["start"]; th = TT("d4", "hundred", 0.3)
    spot(c, 260, 1180, 200, SP_GR, pr(t, t0, 0.4), seed=73); spot(c, 780, 1180, 200, SP_PU, pr(t, t0 + 0.15, 0.4), seed=74)
    house2(c, 260, 1330, 1.15, t, t0 + 0.05, GR, "NO CREDIT CARD")
    house2(c, 780, 1330, 1.15, t, t0 + 0.25, PU, "CREDIT CARD")
    dash_line(c, (390, 1070), (650, 1070), pr(t, t0 + 0.5, 0.5), MK, 6)
    for i in range(4):
        tk = t0 + 0.8 + i * 0.35
        if t < tk: continue
        u = ((t - tk) % 1.4) / 1.4
        coin(c, 390 + 260 * eio(u), 1050 - 60 * math.sin(math.pi * u), 22, spin=t * 5)
    if t > th - 0.3:
        mtext(c, "2010 ESTIMATE", 520, 925, 48, MK, pr(t, th, 0.3), "pm", pen_=True); boxed(c, 520, 908, 370, 80, pr(t, th + 0.2, 0.4), RD)
    say(c, t, t0 + 0.08, "their estimate", "~$150 A YEAR", RD, under=RD)
    note(c, t, t0 + 0.6, "BOSTON FED 10-3: $149 A YEAR PER CASH HOUSEHOLD")


def S_d5(c, t):
    t0 = SHOT["S_d5"]["start"]; tc = TT("d5", "coffee", 0.3)
    spot(c, 540, 1150, 320, SP_YE, pr(t, t0, 0.4), seed=81)
    hero(c, 320, FLOOR, 1.15, POSES["shrug"] if t > tc else POSES["hold"], Face("open", "o" if t > tc else "smile", look=(1, -1) if t < tc else (0, 0)), t)
    cup_m(c, 680, 1360, t, t0 - 3, 1.0)
    if t > tc - 0.1: mtext(c, "?!", 770, 1040, 100, RD, pop_(t, tc - 0.1), "pm")
    say(c, t, t0 + 0.08, "honestly? who knew", "A COFFEE?!", MK, under=OR)


def S_e1(c, t):
    t0 = SHOT["S_e1"]["start"]; ts = TT("e1", "same", 0.3)
    spot(c, 540, 1130, 360, SP_PK, pr(t, t0, 0.4), seed=91)
    gov_m(c, 280, 1300, t, t0 + 0.05, "CARDS", "INDUSTRY GROUP", 0.6)
    if t > ts - 0.4: tagpill_m(c, 290, 920, "SAME RATE", pop_(t, ts - 0.4), PU, 50)
    for i, (x, lab) in enumerate(((640, "LOWER INCOME"), (870, "HIGHER INCOME"))):
        if t < t0 + 0.5 + i * 0.2: continue
        extra(c, x, FLOOR, 0.7, POSES["hold"], Face("open", "smile"), t, scarf=(OR, BLU)[i])
        card_m(c, x + 40, 1290, 100, pop_(t, t0 + 0.6 + i * 0.2), PU, 6)
        mtext(c, lab.split()[0], x, 1050, 34, MK, pr(t, t0 + 0.7 + i * 0.2, 0.3), "pm"); mtext(c, "INCOME", x, 1090, 28, MK, pr(t, t0 + 0.8 + i * 0.2, 0.3), "pm")
        if t > ts: tagpill_m(c, x, 975, "1.8¢ PER $1", pop_(t, ts + i * 0.15), GR, 28)
    say(c, t, t0 + 0.08, "card groups push back", "SAME RATE", PU, under=PU)
    note(c, t, t0 + 0.6, "ELECTRONIC PAYMENTS COALITION (INDUSTRY-FUNDED), MAY 2024")


def S_e2(c, t):
    t0 = SHOT["S_e2"]["start"]; ta = TT("e2", "assumed", 0.3); tc = TT("e2", "couldn't", 0.3)
    spot(c, 520, 1140, 360, SP_BL, pr(t, t0, 0.4), seed=93)
    clipboard_m(c, 380, 1150, t, t0 - 3, ["MODEL", "2007-08 DATA", "FEE PASSED ON"], [t0 - 3, t0 - 3, None], hot=2, hot_t=ta)
    if t > tc - 0.2:
        mtext(c, "?", 790, 1220, 160, RD, pop_(t, tc - 0.2), "pm")
        sticky_m(c, 780, 930, t, tc, "CAN'T CHECK IT", 0.75, 8, RD)
    say(c, t, t0 + 0.08, "a catch they flagged", "ASSUMED", BLU, under=RD)
    note(c, t, t0 + 0.6, "BOSTON FED 10-3: \"THE DATA NEEDED TO VERIFY THEM ARE NOT AVAILABLE\"")


def S_f2(c, t):
    t0 = SHOT["S_f2"]["start"]; tb = TT("f2", "Banned", 0.3)
    spot(c, 520, 1110, 360, SP_BL, pr(t, t0, 0.4), seed=101)
    boxed(c, 250, 820, 200, 110, pr(t, t0 + 0.05, 0.4), BLU); mtext(c, "UK", 250, 842, 70, BLU, pr(t, t0 + 0.2, 0.3), "pm")
    pricebd_m(c, 520, 1120, t, t0 + 0.2, "COFFEE", "£3", "+ CARD FEE", cross_t=TT("f2", "can't", 0.4) + 0.2, w=480)
    if t > tb - 0.2: stamp_m(c, 520, 1380, "BANNED 2018", pr(t, tb - 0.2, 0.25), col=RD, tilt=-6, size=70)
    say(c, t, t0 + 0.08, "in the UK", "NO CARD FEE", BLU, under=BLU)
    note(c, t, t0 + 0.6, "GOV.UK, 13 JAN 2018 · CARD SURCHARGE BAN (CONSUMER PAYMENTS)")


def S_f3(c, t):
    t0 = SHOT["S_f3"]["start"]; tc = TT("f3", "capped", 0.3); tn = TT("f3", "no", 0.3)
    spot(c, 290, 1150, 240, SP_BL, pr(t, t0, 0.4), seed=103); spot(c, 760, 1150, 220, SP_OR, pr(t, tn - 0.4, 0.4), seed=104)
    gov_m(c, 290, 1360, t, t0 + 0.05, "EU", "BANK'S CUT", 0.6)
    if t > tc - 0.3:
        mtext(c, "0.3%", 290, 980, 110, BLU, pr(t, tc - 0.3, 0.4), "pm", pen_=True)
        mtext(c, "CAPPED", 290, 1060, 44, MK, pr(t, tc, 0.3), "pm")
    if t > tn - 0.4:
        boxed(c, 760, 1100, 280, 160, pr(t, tn - 0.4, 0.4), OR); mtext(c, "USA", 760, 1080, 60, OR, pr(t, tn - 0.3, 0.3), "pm")
        mtext(c, "NO CAP", 760, 1150, 52, RD, pr(t, tn, 0.3), "pm")
    say(c, t, t0 + 0.08, "the EU caps the bank's cut", "0.3%", BLU, under=BLU)
    note(c, t, t0 + 0.6, "EU REG. 2015/751, ART. 4 (CONSUMER CREDIT CARDS) · US: NO FEDERAL CREDIT-CARD CAP")


def S_t1(c, t):
    t0 = SHOT["S_t1"]["start"]; td = TT("t1", "discount.", 0.3); ta = TT("t1", "Ask", 0.3)
    spot(c, 520, 1150, 370, SP_GR, pr(t, t0, 0.4), seed=111)
    floor_line(c, t, t0, FLOOR - 160, 120, 960)
    hero(c, 240, FLOOR, 1.0, POSES["hold"] if t < ta else POSES["point"], Face("open", "smile", look=(1, 0)), t)
    cash_m(c, 360, 1140, t, t0 - 3, 0.5, "$5", -10)
    cup_m(c, 620, FLOOR - 160, t, t0 + 0.1, 0.75)
    tag_m(c, 760, 1020, "$5", t, t0 + 0.2, BLU, 8, 0.65)
    if t > td - 0.3: mtext(c, "CASH DISCOUNT?", 560, 860, 62, GR, pr(t, td - 0.3, 0.4), "pm", pen_=True)
    if t > ta: ink(c, [[(680, 1110), (710, 1140), (780, 1070)]], pr(t, ta, 0.3), GR, 10, pen_=False)
    say(c, t, t0 + 0.08, "paying cash?", "ASK", GR, under=GR, size=190)
    note(c, t, t0 + 0.6, "15 U.S.C. § 1666f: CARD ISSUERS CAN'T BAN CASH DISCOUNTS")


def S_end(c, t):
    t0 = SHOT["S_end"]["start"]; tz2 = L0("z2"); ty = TT("z1", "Yes,", 0.6); tn = TT("z1", "no?", 0.85)
    spot(c, 520, 1080, 300, SP_YE, 1.0, seed=121)
    c.save(); c.translate(0, 8 * math.sin(t * 2.4)); c.rotate(1.2 * math.sin(t * 1.7))
    cup_m(c, 520, 1180, t, t0 - 3, 0.95)
    c.restore()
    coin_hop(c, t, 240, 800, 1000, 1.3, 160, 26, t_start=t0)
    tagpill_m(c, 290, 1380, "YES", pop_(t, ty - 0.2), GR, 64)
    tagpill_m(c, 760, 1380, "NO", pop_(t, tn - 0.2), RD, 64)
    for i, (x, tm) in enumerate(((290, ty), (760, tn))):
        if t > tm: ink(c, [wob(circ_pts(x, 1370, 140, -150, 215, 40, ry=80), 95 + i, 1.4)], pr(t, tm, 0.35), MK, 7, pen_=False)
    say(c, t, t0 + 0.08, "fair to the cash payer?", "YES OR NO?", MK, t1=tz2 - 0.3, under=OR, size=160)
    say(c, t, tz2 - 0.25, "send it to the friend who pays cash", "SAVE THIS", BLU, under=OR)
    note(c, t, t0 + 0.6, "COMMENT ONE WORD · EDUCATION ONLY")


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}
SURF = surface()
IMPACTS = [(TT("a3", "billion", 0.3), 0.14, 4), (TT("d2", "nothing", 0.3), 0.12, 4), (TT("f2", "Banned", 0.3), 0.14, 5)]
# the MONEY ROUTE map: which stop we're at
_D4 = (0, 1, 2, 3)
_MAP = {"S_a1": (0, ()), "S_a2": (0, ()), "S_a3": (0, ()), "S_b1": (1, (0,)), "S_c1": (2, (0, 1)), "S_d1": (3, (0, 1, 2)),
        "S_d3": (3, (0, 1, 2)), "S_d4": (3, (0, 1, 2)), "S_d5": (-1, _D4), "S_e1": (-1, _D4), "S_e2": (-1, _D4), "S_t1": (-1, _D4)}
_TOP = {"S_a1": "STOP 1 OF 4", "S_a2": "STOP 1 OF 4", "S_a3": "STOP 1 OF 4", "S_b1": "STOP 2 OF 4", "S_c1": "STOP 3 OF 4", "S_d1": "STOP 4 OF 4",
        "S_d3": "STOP 4 OF 4", "S_d4": "STOP 4 OF 4", "S_e1": "THE OTHER SIDE", "S_e2": "THE OTHER SIDE", "S_f2": "OTHER COUNTRIES",
        "S_f3": "OTHER COUNTRIES", "S_t1": "WHAT YOU CAN DO"}


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
    _CUR[0] = sid
    RENDER[sid](c, tt)
    c.restore()
    pill(c, topline(sid))
    if sid in _MAP: route_map(c, _MAP[sid][0], _MAP[sid][1], min(1, pr(tt, s["start"], 0.3)))
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
