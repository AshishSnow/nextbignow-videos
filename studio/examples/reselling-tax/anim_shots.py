# ================= HOW TO START EP 5: How to start reselling, and when the tax office cares. nbnkit (NextBigNow's rig). One held world: a night stockroom with a clothes rack that IS the roadmap. =================
L0 = lambda i: LINES[i]["start"]; L1 = lambda i: LINES[i]["end"]


def TT(lid, w, frac=0.5, nth=0):
    """word time, falling back to a position in the line if ASR wrote the word differently"""
    try: return T(lid, w, nth)
    except Exception: return L0(lid) + (L1(lid) - L0(lid)) * frac


SHOTLIST = [("S_hook", 0.0, "cut"), ("S_closet", L0("i2") - 0.12, "focus"), ("S_old", L0("i3") - 0.1, "cut"), ("S_thrift", L0("i4") - 0.12, "whip"),
            ("S_income", TT("i5", "This", 0.0) - 0.1, "cut"), ("S_steps", TT("i5", "So", 0.5) - 0.1, "focus"),
            ("S_s1", L0("a1") - 0.12, "whip"), ("S_ask", L0("a2") - 0.08, "focus"),
            ("S_s2", L0("b1") - 0.12, "whip"), ("S_pct", L0("b2") - 0.08, "focus"), ("S_rcpt", L0("b3") - 0.08, "cut"), ("S_keep", L0("b4") - 0.06, "zoom"),
            ("S_s3", L0("c1") - 0.12, "whip"), ("S_list", L0("c2") - 0.08, "cut"),
            ("S_s4", L0("d1") - 0.12, "whip"), ("S_us", L0("d2") - 0.08, "focus"), ("S_irs", L0("d3") - 0.06, "punch"), ("S_400", L0("d4") - 0.08, "cut"),
            ("S_uk", L0("d5") - 0.12, "whip"), ("S_old30", L0("d6") - 0.06, "cut"), ("S_buy", L0("d7") - 0.08, "whip"),
            ("S_both", L0("t1") - 0.12, "focus"), ("S_keep2", L0("t2") - 0.08, "whip"), ("S_end", L0("z1") - 0.12, "focus")]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}


def lt(t, sid): return t - SHOT[sid]["start"]


import sys as _sys, os as _os
_sys.path.insert(0, _D if "_D" in globals() else f"{B}/scripts")
from nbnkit import *        # noqa  (NextBigNow rig + OMB helpers; R becomes skia.Rect from here on)
from nbnkit import _rot_stick
import skia


def say(c, t, t0, small, big, col=WHITE, t1=None, size=250, y=650, t_big=None, smallc=(240, 232, 255)):
    # t1 - 0.2: the old caption is fully gone before the next rises (no ghost overlap on the cut)
    two_tier(c, t, t0, small, big, y=y, big_size=size, big_col=col, small_col=smallc, shadow=True, t1=None if t1 is None else t1 - 0.2, t_big=t_big, maxw=800)


def fnote(c, t, t0, text, t1=None, y=1466, x=540, size=27):
    if t < t0 or (t1 is not None and t > t1): return
    a = min(pr(t, t0, 0.25), 1.0 if t1 is None else 1 - pr(t, t1 - 0.2, 0.2)); src_chip(c, text, a, y=y, x=x, size=size)


def pop_(t, t0, d=0.32, s=1.7): return eback(pr(t, t0, d), s)
def sl(t, t0, d=0.28): return eback(pr(t, t0, d), 2.6) if t >= t0 else 0.0     # a stamp slam: fast, overshoots


def swing(t, t0, a=7.0): return a * math.exp(-max(t - t0, 0) * 2.4) * math.sin(max(t - t0, 0) * 8.5) if t >= t0 else 0.0


RED2 = (255, 96, 86); GREEN2 = (70, 214, 130); SHIRT_B = (70, 120, 200); SHIRT_R = (200, 80, 70); THRIFT = (60, 160, 120); MD = "MADE-UP NUMBERS"
WARM = ((90, 40, 30), (190, 100, 50)); WARMD = (255, 190, 90)
VIO = ((44, 28, 110), (110, 60, 170)); VIOD = (255, 210, 120)
TEA = ((10, 70, 80), (30, 140, 130)); TEAD = (255, 220, 130)
NAVY = ((16, 28, 80), (40, 70, 150)); NAVD = (120, 170, 255)
UKT = ((14, 62, 92), (24, 120, 140)); UKD = (60, 150, 160)


def rack(c, y=772, x0=70, x1=1010, floor=FLOOR):
    """the clothes rack: one thin pipe across the room, two posts. This episode's held object (and the roadmap)."""
    dk = (196, 202, 220)
    for x in (x0, x1):
        c.drawLine(x, y, x, floor - 6, stroke((20, 22, 44), 16)); c.drawLine(x, y, x, floor - 6, stroke((96, 104, 136), 7))
    c.drawLine(x0 - 12, y, x1 + 12, y, stroke((20, 22, 44), 18)); c.drawLine(x0 - 12, y, x1 + 12, y, stroke(dk, 8))


def diag(c, t, sid, pal, disc, cx=540, cy=1080, r=400):
    diagram_bg(c, *pal, disc=disc, cx=cx, cy=cy, r=r, k=pr(t, SHOT[sid]["start"], 0.3) if disc else 1.0)


def finish(c, t, a=0.4, col=(14, 8, 40)):
    fg_dust(c, t, n=6, a=0.18, col=(255, 255, 255)); top_shade(c, a, col)


def mini(c, x, y, w, col, k=1.0, tilt=0.0): jacket(c, x, y, w, col=col, k=k, tilt=tilt, hanger=False)


# ---------------------------------------------------------------- hook
def two_jackets(c, t, y=772, w=300, x0=290, x1=790, t0=-2.0):
    """the frame-1 composition: the rack + the two jackets (also the loop ending)"""
    rack(c, y)
    s0 = 5.0 * math.sin(t * 1.3) * 0.25
    jacket(c, x0, y - 4, w, col=SHIRT_B, tilt=swing(t, t0) + s0)
    jacket(c, x1, y - 4, w, col=SHIRT_R, tilt=-swing(t, t0 + 0.15) - s0)


def S_hook(c, t):
    tn = TT("i1", "no", 0.34); tcan = TT("i1", "can.", 0.72); tw = TT("i1", "Why?", 0.95)
    pack_room(c, t)
    two_jackets(c, t, t0=0.0)
    stamp(c, 290, 985, "USUALLY NO TAX", GRN, k=sl(t, tn), size=44)
    stamp(c, 790, 985, "TAX?", RED_C, k=sl(t, tcan), tilt=8, size=74)
    look = (-1, -1) if t < tcan - 0.3 else (1, -1)
    hero(c, 540, FLOOR, 1.1, POSES["shrug"] if t > tw - 0.3 else POSES["stand"], Face("wide" if t > tw - 0.3 else "open", "o" if t > tw - 0.3 else "smile", look=look), t)
    top_shade(c, 0.5)
    say(c, t, -1, "both sold online", "TWO JACKETS", YEL, t1=tw - 0.1, size=210)
    say(c, t, tw - 0.05, "what's the difference?", "WHY?", WHITE, size=270)
    fnote(c, t, 0.3, "HOW TO START RESELLING · US + UK")


def S_closet(c, t):
    t0 = SHOT["S_closet"]["start"]; tc = TT("i2", "closet", 0.8); g = eio(pr(t, tc - 0.25, 0.5))
    pack_room(c, t, lamp=(420, 1120), lamp_a=0.58)
    rack(c)
    for x, col, wn in ((770, (150, 120, 180), 1), (930, (120, 140, 90), 1)):
        jacket(c, x, 768, 230, col=col, worn=wn, tilt=swing(t, tc, 3.0))
    jacket(c, lerp(610, 430, g), lerp(768, 880, g), lerp(230, 300, g), col=SHIRT_B, worn=1, tilt=lerp(0, -6, g), hanger=g < 0.6)
    parcel(c, 700, FLOOR, 210, k=pop_(t, t0 + 0.1))
    hero(c, 270, FLOOR, 1.2, lerp_pose(POSES["stand"], POSES["hold"], eio(pr(t, tc - 0.3, 0.4))), Face("happy" if g > 0.5 else "open", "grin" if g > 0.5 else "smile", look=(1, -1)), t)
    top_shade(c, 0.5)
    say(c, t, t0 + 0.04, "you want to start", "RESELLING", WHITE, t1=TT("i2", "So", 0.55) - 0.08, size=250)
    say(c, t, TT("i2", "So", 0.55) - 0.04, "so first, clear", "YOUR CLOSET", YEL, size=240)


def S_old(c, t):
    t0 = SHOT["S_old"]["start"]; t80 = TT("i3", "eighty", 0.35); t20 = TT("i3", "twenty.", 0.62); tl = TT("i3", "lost", 0.75); tn = TT("i3", "no", 0.92)
    pack_room(c, t, lamp=(650, 1120), lamp_a=0.55)
    rack(c)
    jacket(c, 690, 768, 390, col=SHIRT_B, worn=1, tilt=swing(t, t80, 2.5))
    price_tag(c, 860, 900, "$80", k=pop_(t, t80), tilt=-8, size=76)
    if t > t20:     # the $80 gets crossed out on the word "twenty"
        kk = eo(pr(t, t20, 0.2)); c.drawLine(790, 918, lerp(790, 950, kk), lerp(918, 870, kk), stroke(RED_C, 11))
    price_tag(c, 860, 1040, "$20", k=pop_(t, t20), tilt=5, size=84, col=(180, 40, 40))
    stamp(c, 690, 1230, "NO TAX", GRN, k=sl(t, tn), size=78)
    p = POSES["hug"] if tl - 0.1 < t < tn else (POSES["arms_up"] if t >= tn else POSES["hold"])
    hero(c, 240, FLOOR, 1.15, p, Face("happy" if t >= tn else "open", "grin" if t >= tn else ("frown" if t > t20 else "smile"), "worried" if tl - 0.1 < t < tn else "none", look=(1, -1)), t)
    top_shade(c, 0.5)
    say(c, t, t0 + 0.03, "these numbers are", "MADE UP", WHITE, t1=TT("i3", "Your", 0.2) - 0.06, size=250)
    say(c, t, TT("i3", "Your", 0.2) - 0.02, "your old jacket cost", "$80", WHITE, t1=t20 - 0.08, size=270)
    say(c, t, t20 - 0.04, "it sells for", "$20", YEL, t1=tl - 0.08, size=270)
    say(c, t, tl - 0.04, "you lost money, so", "NO TAX", GREEN2, size=270)
    fnote(c, t, t0 + 0.1, MD, t1=tl - 0.05)
    fnote(c, t, tl, "SOLD AT A PROFIT? THE GAIN IS TAXABLE · IRS", size=25)


def thrift_set(c, t, sid, tag5=1.0, tag30=1.0):
    diag(c, t, sid, WARM, WARMD)
    jacket(c, 540, 790, 380, col=THRIFT, tilt=swing(t, SHOT[sid]["start"], 2.5))
    price_tag(c, 290, 1120, "$5", k=tag5, tilt=-8, size=86)
    price_tag(c, 800, 1120, "$30", k=tag30, tilt=5, size=96, col=(20, 120, 76))


def S_thrift(c, t):
    t0 = SHOT["S_thrift"]["start"]; t5 = TT("i4", "five", 0.4); t30 = TT("i4", "thirty.", 0.88); tj = TT("i4", "just", 0.55)
    thrift_set(c, t, "S_thrift", pop_(t, t5), pop_(t, t30))
    q = pr(t, t30 - 0.1, 0.9)
    parcel(c, lerp(540, 1250, eio(q)), lerp(1400, 1150, q) - 120 * math.sin(math.pi * q), 150, k=pop_(t, tj))
    hero(c, 170, 1490, 0.82, POSES["point"] if t < t30 else POSES["arms_up"], Face("happy" if t > t30 else "open", "grin", look=(1, -1)), t)
    finish(c, t)
    say(c, t, t0 + 0.03, "next", "A THRIFT JACKET", WHITE, t1=t5 - 0.42, size=200)
    say(c, t, t5 - 0.36, "you pay, just to sell it", "$5", WHITE, t1=t30 - 0.1, size=270)
    say(c, t, t30 - 0.06, "what if it sells for", "$30", YEL, size=270)
    fnote(c, t, t0 + 0.15, MD, x=620, size=25)


def S_income(c, t):
    t0 = SHOT["S_income"]["start"]; ti = TT("i5", "income.", 0.32)
    thrift_set(c, t, "S_income")
    stamp(c, 540, 1120, "INCOME", RED_C, k=sl(t, ti), size=96)
    hero(c, 170, 1490, 0.82, POSES["point"], Face("open", "o" if t > ti else "smile", look=(1, -1)), t)
    finish(c, t)
    say(c, t, t0 + 0.03, "this sale made money", "ON PURPOSE", WHITE, t1=ti - 0.1, size=230)
    say(c, t, ti - 0.06, "that's", "INCOME", YEL, size=270)
    fnote(c, t, ti + 0.1, 'IN THE UK: PROBABLY "TRADING" · HMRC', x=620, size=25)


STEP_NAMES = ("REAL PRICE", "THE CUT", "RECEIPTS", "TAX OFFICE")
STEP_COLS = ((90, 130, 230), (40, 170, 150), (240, 150, 60), (230, 70, 80))


def S_steps(c, t):
    t0 = SHOT["S_steps"]["start"]; tf = TT("i5", "four", 0.75); ts = TT("i5", "Step", 0.82); hot = pr(t, ts, 0.3)
    pack_room(c, t, lamp=(540, 1130), lamp_a=0.5)
    rack(c)
    xs = (190, 420, 650, 880)
    for i in range(4):
        tk = (tf - 0.1) + i * 0.17; kk = pop_(t, tk, 0.3)
        sc = kk * (1 + (0.16 * hot if i == 3 else 0) - (0.1 * hot if i != 3 else 0))
        if kk <= 0: continue
        if i == 3 and hot > 0: c.drawCircle(xs[i], 930, 170, paint(shader=rad(xs[i], 930, 170, [argb(RED2, 0.55 * hot), argb(RED2, 0)])))
        jacket(c, xs[i], 768, 175 * sc, col=STEP_COLS[i], tilt=swing(t, tk, 5.0))
        ctext(c, str(i + 1), xs[i], 900, "ant", 62 * sc, WHITE)
        label_card(c, xs[i], 1045, STEP_NAMES[i], 34, RED_C if i == 3 and hot > 0.5 else INK, k=kk, pad=22)
    hero(c, 540, FLOOR, 1.05, POSES["point_up"], Face("open", "smile", look=(1, -1)), t)
    top_shade(c, 0.5)
    say(c, t, t0 + 0.03, "so before you start", "4 STEPS", WHITE, t1=ts - 0.08, size=270)
    say(c, t, ts - 0.04, "step four is", "THE SURPRISE", RED2, size=220)


def step_jacket(c, t, i):
    jacket(c, 150, 768, 175, col=STEP_COLS[i], tilt=swing(t, SHOT[("S_s1", "S_s2", "S_s3", "S_s4")[i]]["start"], 8.0))
    ctext(c, str(i + 1), 150, 900, "ant", 62, WHITE)


# ---------------------------------------------------------------- step 1
def S_s1(c, t):
    t0 = SHOT["S_s1"]["start"]; tf = TT("a1", "Find", 0.45)
    pack_room(c, t, lamp=(540, 1100), lamp_a=0.56)
    rack(c); step_jacket(c, t, 0)
    listing_card(c, 540, 1090, 330, "$ ?", "WHAT SOLD?", k=pop_(t, tf - 0.1), tilt=-2, col=GRN)
    wk = pr(t, t0, 0.9); gx = lerp(1160, 860, eo(wk))
    girl(c, gx, FLOOR, 1.1, walk_pose(t * 1.5, 0.9) if wk < 1 else POSES["point"], Face("open", "smile", look=(-1, 0)), t, flip=True, dress=TEAL_C)
    hero(c, 220, FLOOR, 1.1, POSES["hug"], Face("open", "o", look=(1, -1)), t)
    top_shade(c, 0.5)
    say(c, t, t0 + 0.04, "step one", "WHAT IT SOLD FOR", YEL, size=190)


def S_ask(c, t):
    t0 = SHOT["S_ask"]["start"]; tf = TT("a2", "actually", 0.62); dim = pr(t, tf - 0.1, 0.3)
    diag(c, t, "S_ask", VIO, VIOD, r=390)
    wob = 2.0 * math.sin(t * 5.0) * (1 - dim)
    mv = eio(pr(t, tf - 0.25, 0.35)); ax = lerp(540, 300, mv); aw = lerp(430, 310, mv)     # alone in the middle while it is the only idea, steps aside when the real price arrives
    listing_card(c, ax, 1090, aw, "$100", "ASKING", k=pop_(t, t0 + 0.05), tilt=-4 + wob)
    if dim > 0.01:
        kk = eo(dim); c.drawLine(170, 1240, lerp(170, 430, kk), lerp(1240, 950, kk), stroke(RED_C, 13))
    listing_card(c, 780, 1080, 400, "$30", "SOLD", k=pop_(t, tf), tilt=3)
    finish(c, t)
    say(c, t, t0 + 0.03, "anyone can ask", "$100", WHITE, t1=tf - 0.08, size=270)
    say(c, t, tf - 0.04, "search what actually sold", "NOT ASKING", YEL, size=230)
    fnote(c, t, tf + 0.05, 'ON EBAY: THE "SOLD ITEMS" FILTER · LAST 90 DAYS', size=26)


# ---------------------------------------------------------------- step 2
def S_s2(c, t):
    t0 = SHOT["S_s2"]["start"]
    pack_room(c, t, lamp=(600, 1160), lamp_a=0.56)
    rack(c); step_jacket(c, t, 1)
    parcel(c, 660, FLOOR, 420, k=pop_(t, t0 + 0.05))
    q = eio(pr(t, t0 + 0.15, 0.9))      # tape runs along the box
    c.drawRect(R.MakeXYWH(450, FLOOR - 182, 420 * q, 46), paint((236, 206, 150)))
    c.drawRect(R.MakeXYWH(450, FLOOR - 182, 420 * q, 46), stroke(INK, 4))
    hero(c, 310, FLOOR, 1.15, POSES["press"], Face("open", "smile", look=(1, 1)), t)
    top_shade(c, 0.5)
    say(c, t, t0 + 0.04, "step two", "COUNT THE CUT", WHITE, size=220)


def S_pct(c, t):
    t0 = SHOT["S_pct"]["start"]; t14 = TT("b2", "fourteen", 0.62); to = TT("b2", "order", 0.9)
    diag(c, t, "S_pct", TEA, TEAD, cy=1060, r=390)
    pie_wedge(c, 540, 1060, 300, 0.14 * eo(pr(t, t14 - 0.35, 0.6)), k=pop_(t, t0 + 0.05))
    if t > to - 0.1:
        label_card(c, 800, 1320, "+ ORDER FEE", 50, INK, k=pop_(t, to - 0.1), tilt=-3)
        coin(c, 620, 1330, 34, spin=t * 4, a=min(1, (t - to + 0.1) * 5))
    hero(c, 170, 1490, 0.8, POSES["point"], Face("open", "smile", look=(1, -1)), t)
    finish(c, t, 0.4, (4, 20, 40))
    say(c, t, t0 + 0.03, "on ebay in america", "ABOUT 14%", YEL, size=260)
    fnote(c, t, t0 + 0.4, "MOST CATEGORIES · 13.6% + UP TO $0.40 AN ORDER", x=590, size=24)


RROWS = [("SOLD", "$30"), ("FEES, ABOUT", "-$5"), ("JACKET", "-$5")]


def S_rcpt(c, t):
    t0 = SHOT["S_rcpt"]["start"]; tf = TT("b3", "five", 0.3); tt_ = TT("b3", "Then", 0.5)
    diag(c, t, "S_rcpt", TEA, TEAD, cy=1080, r=390)
    prog = 1 / 3 if t < tf - 0.05 else (2 / 3 if t < tt_ + 0.5 else 1.0)
    receipt(c, 560, 1080, 620, RROWS, prog=prog, k=pop_(t, t0 + 0.02, 0.28, 1.2))
    hero(c, 150, 1490, 0.74, POSES["point"], Face("open", "smile", look=(1, -1)), t)
    finish(c, t, 0.4, (4, 20, 40))
    say(c, t, t0 + 0.03, "on your jacket, fees of", "ABOUT $5", WHITE, t1=tt_ - 0.08, size=260)
    say(c, t, tt_ - 0.04, "then the $5", "YOU PAID", YEL, size=260)
    fnote(c, t, t0 + 0.2, "THE FEE COUNTS SALES TAX + POSTAGE · EBAY", x=590, size=24)


def S_keep(c, t):
    t0 = SHOT["S_keep"]["start"]; tk = TT("b4", "twenty,", 0.42); tp = TT("b4", "postage", 0.68)
    diag(c, t, "S_keep", TEA, TEAD, cy=1080, r=390)
    receipt(c, 560, 1060, 620, RROWS, total=("KEEP, ABOUT", "$20"), prog=0.76 if t < tk - 0.2 else 1.0)
    if t > tp - 0.1: label_card(c, 610, 1370, "POSTAGE STILL TO COME", 50, RED_C, k=pop_(t, tp - 0.1), tilt=-3)
    hero(c, 150, 1490, 0.74, POSES["shock"] if t > tp else POSES["arms_up"], Face("wide" if t > tp else "happy", "o" if t > tp else "grin", look=(1, -1)), t)
    finish(c, t, 0.4, (4, 20, 40))
    say(c, t, t0 + 0.03, "so you keep", "ABOUT $20", GREEN2, t1=tp - 0.08, size=260)
    say(c, t, tp - 0.04, "postage still", "COMES OUT", WHITE, size=260)
    fnote(c, t, t0 + 0.1, "MADE-UP SALE", x=620, size=25)


# ---------------------------------------------------------------- step 3
def S_s3(c, t):
    t0 = SHOT["S_s3"]["start"]; tk = TT("c1", "keep", 0.62)
    pack_room(c, t, lamp=(520, 1120), lamp_a=0.56)
    rack(c); step_jacket(c, t, 2)
    pile = ((560, 1330, -7), (720, 1345, 6), (640, 1250, 2), (830, 1290, -3), (520, 1180, 8))
    for i, (x, y, tl_) in enumerate(pile):
        d0 = t0 + 0.35 + i * 0.42; q = pr(t, d0, 0.35)
        if q <= 0: continue
        yy = lerp(760, y, eio(q))
        receipt(c, x + 30 * math.sin((1 - q) * 6), yy, 200, [("PAID", "$" + str((5, 12, 3, 8, 20)[i]))], tilt=tl_ + (1 - q) * 22)
    if t > tk - 0.1:
        line_tally(c, 780, 1010, 480, [("$5", "$30", "$4.48")], k=pop_(t, tk - 0.1), prog=1.0)
    hero(c, 280, FLOOR, 1.15, POSES["arms_up"] if t < tk else POSES["point"], Face("wide" if t < tk else "open", "o" if t < tk else "smile", look=(1, -1)), t)
    top_shade(c, 0.5)
    say(c, t, t0 + 0.04, "step three, save", "EVERY RECEIPT", WHITE, t1=tk - 0.08, size=220)
    say(c, t, tk - 0.04, "and keep", "ONE LIST", YEL, size=270)


TALLY = [("$5", "$30", "$4.48"), ("$12", "$40", "$5.84")]


def S_list(c, t):
    t0 = SHOT["S_list"]["start"]; tp = TT("c2", "profit,", 0.66); th = TT("c2", "That", 0.42)
    pack_room(c, t, lamp=(640, 1100), lamp_a=0.5)
    line_tally(c, 640, 1040, 720, TALLY, k=pop_(t, t0 + 0.02), prog=pr(t, t0 + 0.1, max(0.3, th - t0)))
    girl(c, 150, FLOOR, 1.05, POSES["point"], Face("open", "smile", look=(1, -1)), t, dress=TEAL_C)
    if t > tp - 0.1: stamp(c, 720, 1250, "PROFIT, NOT JUST SALES", GRN, k=sl(t, tp - 0.1), size=54, tilt=-3)
    top_shade(c, 0.5)
    say(c, t, t0 + 0.03, "one simple list", "PAID · SOLD · FEES", YEL, t1=th - 0.08, size=180)
    say(c, t, th - 0.04, "it shows your", "PROFIT", GREEN2, size=270)
    fnote(c, t, t0 + 0.2, 'MADE-UP ROWS · IRS: "SAVE RECEIPTS OF YOUR EXPENSES"', size=25)


# ---------------------------------------------------------------- step 4: the room goes dark
def S_s4(c, t):
    t0 = SHOT["S_s4"]["start"]; q = pr(t, t0 + 0.05, 1.5)
    pack_room(c, t, lamp=(540, 1200), lamp_a=0.42, top=(12, 14, 40), bot=(36, 40, 84))
    rack(c); step_jacket(c, t, 3)
    tax_form(c, 640 + 26 * math.sin(q * 6), lerp(720, 1090, eo(q)), 340, tilt=-3 + 9 * math.sin(q * 5) * (1 - q), k=min(1, pr(t, t0, 0.2)))
    hero(c, 300, FLOOR, 1.15, POSES["hug"], Face("wide", "flat", "worried", look=(1, -1)), t)
    top_shade(c, 0.55)
    say(c, t, t0 + 0.04, "step four", "WHEN TO TELL THEM", RED2, size=180)


def S_us(c, t):
    t0 = SHOT["S_us"]["start"]; t20 = TT("d2", "twenty", 0.62); t2 = TT("d2", "two", 0.86)
    diagram_bg(c, *NAVY, disc=None)
    label_card(c, 250, 800, "AMERICA", 56, INK, k=pop_(t, t0 + 0.04), tilt=-2)
    line_meter(c, 500, 930, 760, eo(pr(t, t0 + 0.25, t20 - t0)), "A YEAR, ON ONE PLATFORM", need="$20K", ok=t > t20, k=pop_(t, t0 + 0.1, 0.3, 1.2))
    if t > t2 - 1.0:
        line_meter(c, 500, 1120, 760, eo(pr(t, t2 - 0.9, 1.0)), "AND THIS MANY SALES", need="200", ok=t > t2 + 0.15, k=pop_(t, t2 - 1.0, 0.3, 1.2))
    if t > t2 + 0.1:
        tax_form(c, 850, lerp(1500, 1320, eo(pr(t, t2 + 0.1, 0.4))), 170, tilt=6)
    hero(c, 170, 1500, 0.72, POSES["stand"], Face("open", "smile", look=(1, -1)), t)
    finish(c, t, 0.4, (6, 10, 40))
    say(c, t, t0 + 0.03, "a form must come only past", "$20,000", YEL, t1=t2 - 1.1, size=260)
    say(c, t, t2 - 1.05, "and only past", "200 SALES", WHITE, size=260)
    fnote(c, t, t0 + 0.4, "CAN STILL COME BELOW THIS · SOME STATES LOWER", x=590, size=23)


def S_irs(c, t):
    t0 = SHOT["S_irs"]["start"]; ta = TT("d3", "all", 0.55)
    diag(c, t, "S_irs", NAVY, NAVD, cy=1080, r=390)
    tax_form(c, 320, 1090, 380, ghost=True, k=pop_(t, t0 + 0.02))
    stamp(c, 500, 1270, "REPORT IT ALL", RED_C, k=sl(t, ta), size=74, tilt=-6)
    girl(c, 830, FLOOR, 1.05, lerp_pose(POSES["stand"], POSES["point"], eio(pr(t, t0 + 0.2, 0.3))), Face("open", "smile", look=(-1, 0)), t, flip=True, dress=TEAL_C)
    finish(c, t, 0.4, (6, 10, 40))
    say(c, t, t0 + 0.02, "the irs says report it", "FORM OR NO FORM", WHITE, size=190)
    fnote(c, t, t0 + 0.2, "IRS, 2026 · ALL INCOME", size=25)


def S_400(c, t):
    t0 = SHOT["S_400"]["start"]; tl = TT("d4", "Less", 0.68); shr = eo(pr(t, tl - 0.05, 0.4))
    diag(c, t, "S_400", NAVY, NAVD, cy=1090, r=390)
    parcel(c, 300, 1330, 260, k=pop_(t, t0 + 0.2))
    price_tag(c, 650, 1050 + 40 * shr, "$400 PROFIT", k=pop_(t, t0 + 0.05), tilt=-5, size=lerp(100, 74, shr), col=INK)
    if t > tl - 0.05:
        price_tag(c, 650, 1270, "UNDER $400", k=pop_(t, tl), tilt=4, size=80, col=(30, 120, 80))
        stamp(c, 800, 1370, "STILL INCOME", RED_C, k=sl(t, tl + 0.5), size=48, tilt=-6)
    hero(c, 150, 1500, 0.72, POSES["shock"], Face("wide", "o", look=(1, -1)), t)
    finish(c, t, 0.4, (6, 10, 40))
    say(c, t, t0 + 0.03, "side job profit: file a return", "$400", YEL, t1=tl - 0.08, size=270)
    say(c, t, tl - 0.04, "less than that", "STILL COUNTS", WHITE, size=250)
    fnote(c, t, t0 + 0.3, "NET SELF-EMPLOYMENT EARNINGS · IRS", x=600, size=25)


def grid30(c, t, t0, d, worn=0.0):
    """30 small jackets, 6 x 5, landing one by one: a count you can see."""
    cols = ((70, 120, 200), (200, 80, 70), (60, 160, 120), (150, 110, 190), (230, 160, 60))
    n_ = 0
    for i in range(30):
        q = pr(t, t0 + i * d, 0.16)
        if q <= 0: continue
        n_ += 1
        x = 130 + (i % 6) * 92; y = 790 + (i // 6) * 112
        mini(c, x, y + 60 * (1 - eo(q)), 76, mix(cols[i % 5], (130, 130, 140), 0.5 * worn), k=eo(q))
    return n_


def S_uk(c, t):
    t0 = SHOT["S_uk"]["start"]; tt_ = TT("d5", "thirty", 0.42); ttl = TT("d5", "tells", 0.8)
    diagram_bg(c, *UKT, disc=None, floor=FLOOR)
    c.drawLine(0, FLOOR, W, FLOOR, stroke(INK, 5))
    n_ = grid30(c, t, t0 + 0.05, max(0.02, (tt_ - t0 + 0.2) / 30))
    if n_: label_card(c, 830, 830, f"{n_}", 86, RED_C if n_ == 30 else INK, pad=30)
    booth(c, 830, FLOOR, 340, "TAX OFFICE", k=pop_(t, t0 + 0.1))
    q = pr(t, ttl - 0.15, 0.7)
    if 0 < q < 1:
        tax_form(c, lerp(400, 800, eo(q)), lerp(1100, 1180, q) - 160 * math.sin(math.pi * q), 150, tilt=q * 40)
    finish(c, t, 0.4, (2, 18, 40))
    say(c, t, t0 + 0.03, "in britain, in one year", "30 ITEMS", YEL, size=270)
    fnote(c, t, t0 + 0.4, "OR ABOUT £1,700 · THE PLATFORM TELLS HMRC", size=25)


def S_old30(c, t):
    t0 = SHOT["S_old30"]["start"]; tr = TT("d6", "reported", 0.62); tn = TT("d6", "nothing.", 0.95)
    diagram_bg(c, *UKT, disc=None, floor=FLOOR)
    c.drawLine(0, FLOOR, W, FLOOR, stroke(INK, 5))
    grid30(c, t, t0 - 5, 0.01, worn=1.0)
    stamp(c, 370, 1020, "REPORTED", RED_C, k=sl(t, tr), size=76, tilt=-8)
    stamp(c, 400, 1170, "OWES £0", GRN, k=sl(t, tn - 0.25), size=86, tilt=5)
    hero(c, 860, FLOOR, 1.1, POSES["hug"] if t < tn - 0.25 else POSES["arms_up"], Face("happy" if t > tn - 0.25 else "open", "grin" if t > tn - 0.25 else "flat", look=(-1, -1)), t, flip=True)
    finish(c, t, 0.4, (2, 18, 40))
    say(c, t, t0 + 0.02, "thirty old things?", "YOUR CLOSET", WHITE, t1=tr - 0.12, size=250)
    say(c, t, tr - 0.08, "you can be reported, and still", "OWE NOTHING", GREEN2, size=240)
    fnote(c, t, t0 + 0.15, "HMRC: OCCASIONAL UNWANTED ITEMS, NO TAX DUE", t1=tr + 0.8, size=25)
    fnote(c, t, tr + 0.85, "EU PLATFORMS REPORT TOO · DAC7", size=25)


def S_buy(c, t):
    t0 = SHOT["S_buy"]["start"]; tk = TT("d7", "thousand", 0.68); tt_ = TT("d7", "tell", 0.9)
    diag(c, t, "S_buy", UKT, UKD, cy=1100, r=380)
    jacket(c, 840, 790, 270, col=THRIFT, tilt=swing(t, t0 + 0.1, 4.0))
    girl(c, 170, FLOOR, 1.05, POSES["point"], Face("open", "smile", look=(1, 0)), t, dress=TEAL_C)
    line_meter(c, 560, 1270, 660, 1.04 * eo(pr(t, t0 + 0.4, tk - t0)), "", need="£1,000", ok=False, k=pop_(t, t0 + 0.1, 0.3, 1.2))
    if t > tt_ - 0.15: label_card(c, 400, 1030, "TELL THE TAX OFFICE", 54, RED_C, k=pop_(t, tt_ - 0.15), tilt=-2)
    finish(c, t, 0.4, (2, 18, 40))
    say(c, t, t0 + 0.03, "buy thrift jackets to resell?", "£1,000 A YEAR", YEL, size=230)
    fnote(c, t, t0 + 0.4, "BEFORE EXPENSES · COUNTS ALL YOUR TRADING · HMRC", x=540, size=24)


def S_both(c, t):
    t0 = SHOT["S_both"]["start"]; t2 = TT("t1", "No", 0.5)
    # both cases at once, no country names: this is the line of the episode
    diagram_bg(c, *NAVY, disc=None)
    w_ = eio(pr(t, t2 - 0.3, 0.4))
    c.drawRect(R.MakeLTRB(lerp(1080, 540, w_), 0, W, H), paint(TEAL_C, 0.45))
    tax_form(c, 270, 1060, 320, k=pop_(t, t0 + 0.04)); stamp(c, 270, 1090, "NO TAX", GRN, k=sl(t, t0 + 0.5), size=74)
    tax_form(c, 810, 1060, 320, ghost=True, k=pop_(t, t2 - 0.1)); stamp(c, 810, 1190, "TAX", RED_C, k=sl(t, t2 + 0.5), size=82, tilt=8)
    hero(c, 540, FLOOR, 1.05, POSES["shrug"], Face("wide", "o", look=(-1, -1) if t < t2 else (1, -1)), t)
    top_shade(c, 0.4, (6, 10, 40))
    say(c, t, t0 + 0.03, "a form doesn't mean", "YOU OWE", YEL, t1=t2 - 0.1, size=270)
    say(c, t, t2 - 0.06, "no form doesn't mean", "YOU DON'T", WHITE, size=270)


def S_keep2(c, t):
    t0 = SHOT["S_keep2"]["start"]; tu = TT("t2", "Unsure?", 0.45)
    pack_room(c, t, lamp=(560, 1110), lamp_a=0.58)
    rack(c)
    line_tally(c, 700, 1060, 540, TALLY, k=pop_(t, t0 + 0.03))
    hero(c, 240, FLOOR, 1.15, POSES["point"], Face("open", "smile", look=(1, -1)), t)
    if t > tu - 0.05: label_card(c, 720, 1280, "ASK A TAX PRO", 62, INK, k=pop_(t, tu), tilt=-2)
    top_shade(c, 0.5)
    say(c, t, t0 + 0.03, "keep that", "LIST", YEL, t1=tu - 0.08, size=270)
    say(c, t, tu - 0.04, "not sure?", "ASK A PRO", WHITE, size=260)
    fnote(c, t, t0 + 0.2, "EDUCATION ONLY · NOT TAX ADVICE", size=25)


def S_end(c, t):
    t0 = SHOT["S_end"]["start"]; tz2 = L0("z2"); tf = TT("z1", "Fair", 0.5); tcm = TT("z1", "Leave", 0.72)
    pack_room(c, t)
    two_jackets(c, t, y=880, w=250, x0=190, x1=890, t0=t0)
    hero(c, 420, FLOOR, 1.05, POSES["point_up"] if t > tz2 else POSES["hold"], Face("open", "smile", look=(1, -1)), t)
    girl(c, 660, FLOOR, 1.05, POSES["wave"] if t > tz2 else POSES["stand"], Face("happy" if t > tz2 else "open", "grin" if t > tz2 else "smile", look=(-1, 0)), t, dress=TEAL_C, style="long", flip=True)
    if t > tz2 + 0.4: parcel(c, 540, FLOOR + 6, 150, k=pop_(t, tz2 + 0.4))
    top_shade(c, 0.6)
    say(c, t, t0 + 0.03, "platforms must report your sales", "FAIR OR NOSY?", YEL, t1=tz2 - 0.08, size=220)
    say(c, t, tz2 - 0.04, "tell a friend with a full closet", "SAVE THIS", WHITE, size=250)
    kk = pop_(t, tf - 0.05)
    if kk > 0:
        c.save(); c.translate(540, 790); c.scale(kk, kk)
        for sx, tx, col in ((-140, "FAIR", GRN), (140, "NOSY", RED_C)):
            c.drawRoundRect(R.MakeXYWH(sx - 122, -52, 244, 104), 52, 52, paint((0, 0, 0), 0.25, blur=8))
            c.drawRoundRect(R.MakeXYWH(sx - 122, -52, 244, 104), 52, 52, paint(col)); c.drawRoundRect(R.MakeXYWH(sx - 122, -52, 244, 104), 52, 52, stroke(INK, 6))
            ctext(c, tx, sx, 26, "ant", 72, WHITE)
        c.restore()
    src_chip(c, "COMMENT ONE WORD", min(1, pr(t, tcm - 0.2, 0.3)) * (1 - pr(t, tz2, 0.2)))


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}
SURF = surface()
IMPACTS = [(TT("i1", "can.", 0.72), 0.16, 4), (TT("i3", "no", 0.92), 0.18, 5), (TT("i5", "income.", 0.32), 0.2, 6), (TT("d3", "all", 0.55), 0.2, 7), (TT("d6", "reported", 0.62), 0.16, 5), (SHOT["S_irs"]["start"] + 0.02, 0.12, 3)]
# upgrade (6 Nov): the single pill carries the chapter, so the viewer always knows how far through the 4 steps they are, with no second line on screen
_CH = {"S_s1": 1, "S_ask": 1, "S_s2": 2, "S_pct": 2, "S_rcpt": 2, "S_keep": 2, "S_s3": 3, "S_list": 3, "S_s4": 4, "S_us": 4, "S_irs": 4, "S_400": 4, "S_uk": 4, "S_old30": 4, "S_buy": 4}


def topline(sid): return f"HOW TO START · STEP {_CH[sid]} OF 4" if sid in _CH else "OOPSMYBUSINESS · HOW TO START"


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    c = SURF.getCanvas(); c.resetMatrix(); c.clear(skia.ColorBLACK)
    u = pr(tt, s["start"], max(0.5, s["end"] - s["start"])); z = 1.0 + 0.022 * u
    dx = dy = 0.0
    for ti, d, a in IMPACTS:
        if ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83)
    c.save(); c.translate(W / 2 + dx, H * 0.62 + dy); c.scale(z, z); c.translate(-W / 2, -H * 0.62)
    RENDER[sid](c, tt)
    c.restore()
    pill(c, topline(sid))
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
