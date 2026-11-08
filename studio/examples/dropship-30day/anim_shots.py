# ================= HOW TO START EP 8: start dropshipping legally — the FTC's 30-day rule (whiteboard). Held object: ONE parcel with a
# desk lamp inside; its shipping label keeps being rubbed out and rewritten (? → 30 DAYS → NEW DATE → REFUND → SELLER: YOU → 30 DAYS UK).
# New drawings: gov_m (plain government building + sign), stopwatch_m, snail_m, strip_m (day boxes that fill), tagpill_m, store page,
# relabel (the label is rubbed out by a tiny eraser and rewritten), and the RULE MAP (stepmap: four small numbered parcels under the pill,
# the current rule coloured, done rules ticked) — a generalised version of Prime's door map.
# Opening move (new): frame 0 is a finished picture in motion — the parcel with a pulsing red "?" on its label, a calendar above it whose
# pages flick, and the marker pen hovering; on the answer beat the pen circles day 30 and writes 30 DAYS on the label. =================
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


# ---------------------------------------------------------------- new marker props (this episode)
def stepmap(c, n, active, done=(), a=1.0, x0=None, y=392, labels=None):
    """mini map under the pill: n small numbered parcels; the active one coloured + bigger, finished ones ticked"""
    if a <= 0: return
    gap = 120; x0 = x0 if x0 is not None else 510 - gap * (n - 1) / 2
    for i in range(n):
        x = x0 + i * gap; on = (i == active)
        w, h = (78, 56) if on else (62, 44)
        rr = R.MakeXYWH(x - w / 2, y - h, w, h)
        c.drawRect(rr, paint(WHITE, a))
        if on: c.drawRect(rr, paint(CARD_BOARD, 0.85 * a))
        c.drawRect(rr, stroke(MK if on else LIGHT, 5 if on else 3, a))
        c.drawLine(x, y - h, x, y - h + 14, stroke(MK if on else LIGHT, 3, a))
        mtext(c, str(i + 1), x, y - h * 0.22, 38 if on else 30, RD if on else LIGHT, a, "pm")
        if i in done: ink(c, [[(x - 20, y - 70), (x - 6, y - 56), (x + 24, y - 92)]], 1, GR, 7, pen_=False)


def gov_m(c, x, y, t, t0, label="FTC", sign="CONSUMER WATCHDOG", s=1.0):
    k = pr(t, t0, 0.7); w = 440 * s
    roof = [(x - w / 2 - 30 * s, y - 330 * s), (x, y - 440 * s), (x + w / 2 + 30 * s, y - 330 * s), (x - w / 2 - 30 * s, y - 330 * s)]
    steps = [[(x - w / 2 - 40 * s, y), (x + w / 2 + 40 * s, y)], [(x - w / 2 - 20 * s, y - 26 * s), (x + w / 2 + 20 * s, y - 26 * s)]]
    cols = [[(x - w / 2 + 40 * s + i * 90 * s, y - 26 * s), (x - w / 2 + 40 * s + i * 90 * s, y - 312 * s)] for i in range(5)]
    beam = [[(x - w / 2 - 10 * s, y - 312 * s), (x + w / 2 + 10 * s, y - 312 * s)]]
    if k > 0.6: hatch(c, _path(roof), pr(k, 0.6, 0.4), BLU, gap=16, w=6, bbox=(x - w, y - 450 * s, x + w, y - 320 * s), a=0.4)
    ink(c, [wob(roof, 401, 0.8)] + [wob(p, 402 + i, 0.6) for i, p in enumerate(steps + cols + beam)], k, MK, 8)
    mtext(c, label, x, y - 350 * s, int(54 * s), MK, pr(t, t0 + 0.6, 0.3), "pm")
    if sign:
        ks = pr(t, t0 + 0.8, 0.3)
        if ks > 0:
            f = font("pm", int(30 * s)); sw = tw(f, sign) + 40
            c.drawRoundRect(R.MakeXYWH(x - sw / 2, y + 24 * s, sw, 54 * s), 10, 10, paint(WHITE, ks)); c.drawRoundRect(R.MakeXYWH(x - sw / 2, y + 24 * s, sw, 54 * s), 10, 10, stroke(BLU, 5, ks))
            mtext(c, sign, x, y + 62 * s, int(30 * s), BLU, ks, "pm")


def stopwatch_m(c, x, y, t, t0, r=90, run_t=None, stop_t=None, col=RD):
    """a stopwatch; the hand sweeps from run_t until stop_t"""
    k = pr(t, t0, 0.45)
    if k <= 0: return
    ink(c, [wob(circ_pts(x, y, r, -90, 270, 40), 411, 0.6), [(x - 18, y - r - 26), (x + 18, y - r - 26)], [(x, y - r), (x, y - r - 26)]], k, MK, 7)
    if k < 1: return
    for i in range(12):
        a_ = math.radians(i * 30); c.drawLine(x + 0.78 * r * math.sin(a_), y - 0.78 * r * math.cos(a_), x + 0.9 * r * math.sin(a_), y - 0.9 * r * math.cos(a_), stroke(MK, 3))
    el = 0.0
    if run_t is not None and t > run_t: el = (min(t, stop_t) if stop_t else t) - run_t
    a_ = math.radians(el * 140)
    c.drawLine(x, y, x + 0.72 * r * math.sin(a_), y - 0.72 * r * math.cos(a_), stroke(col, 7)); c.drawCircle(x, y, 8, paint(col))


def snail_m(c, x, y, t, t0, s=1.0):
    k = pr(t, t0, 0.5)
    if k <= 0: return
    sp = [(x + (14 + 4.2 * a_ / 30) * s * math.cos(math.radians(a_)), y - 60 * s + (14 + 4.2 * a_ / 30) * s * math.sin(math.radians(a_))) for a_ in range(0, 720, 20)]
    body = [(x - 90 * s, y), (x + 90 * s, y), (x + 120 * s, y - 30 * s), (x + 96 * s, y - 40 * s)]
    if k >= 1: c.drawCircle(x, y - 60 * s, 62 * s, paint(GOLD, 0.45))
    ink(c, [wob(body, 421, 0.6), sp, wob(circ_pts(x, y - 60 * s, 62 * s, -90, 270, 30), 422, 0.6), [(x + 104 * s, y - 36 * s), (x + 120 * s, y - 90 * s)], [(x + 90 * s, y - 36 * s), (x + 96 * s, y - 92 * s)]], k, MK, 6)
    if k >= 1: c.drawCircle(x + 120 * s, y - 94 * s, 6 * s, paint(MK)); c.drawCircle(x + 96 * s, y - 96 * s, 6 * s, paint(MK))


def strip_m(c, x, y, n, t, t0, fill_t=None, step=0.12, cell=None, col=GR, label=None, lab_col=MK, mark_last=None):
    """a row of n day-boxes; from fill_t they fill one by one; mark_last = text on the last box"""
    cell = cell or min(96, 880 / n); x0 = x - cell * n / 2
    k = pr(t, t0, 0.5)
    grid = [[(x0, y), (x0 + cell * n, y), (x0 + cell * n, y + cell), (x0, y + cell), (x0, y)]] + [[(x0 + cell * i, y), (x0 + cell * i, y + cell)] for i in range(1, n)]
    ink(c, [wob(g, 430 + i, 0.4) for i, g in enumerate(grid)], k, MK, 5, pen_=False)
    if fill_t is not None and t > fill_t and k >= 1:
        m_ = min(n, int((t - fill_t) / step) + 1)
        for i in range(m_):
            ki = pr(t, fill_t + i * step, 0.12)
            c.drawRect(R.MakeXYWH(x0 + cell * i + 6, y + 6, (cell - 12) * ki, cell - 12), paint(col, 0.55))
            mtext(c, str(i + 1), x0 + cell * (i + 0.5), y + cell * 0.66, int(cell * 0.42), MK, ki, "kb")
    if label: mtext(c, label, x, y + cell + 64, 44, lab_col, pr(t, t0 + 0.4, 0.3), "pm")


def tagpill_m(c, x, y, text, k, col=BLU, size=46, fill=False):
    if k <= 0: return
    f = font("pm", size); w = tw(f, text) + 56; h = size * 1.55
    c.save(); c.translate(x, y); s = eback(min(1, k), 1.7); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2, paint(col if fill else WHITE, 0.95))
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2, stroke(col, 7))
    c.drawString(text, -tw(f, text) / 2, size * 0.36, f, paint(WHITE if fill else col)); c.restore()


def relabel(c, x, y, t, t0, old, new, t_sw, s=1.0, old_col=RD, new_col=RD, open_=0.0):
    """the held parcel: its label reads `old`; at t_sw a tiny eraser rubs it out (0.35 s) and `new` is written on"""
    if t < t_sw:
        parcel_m(c, x, y, t, t0, s, label=old, label_t=None if old else None, label_col=old_col, open_=open_)
        return
    parcel_m(c, x, y, t, t0, s, label=None, open_=open_)
    u = pr(t, t_sw, 0.35)
    lb_x, lb_y = x - 120 * s, y - 10 * s
    if u < 1 and old:   # the old word fades under the eraser's strokes
        mtext(c, old, x - 20 * s, y + 52 * s, int(40 * s), old_col, 1, "pm", a=1 - u)
        ex = lb_x + 200 * s * (0.5 + 0.5 * math.sin(u * 9))
        c.drawRoundRect(R.MakeXYWH(ex - 28 * s, lb_y + 10 * s, 56 * s, 70 * s), 8, 8, paint((60, 66, 84)))
        c.drawRect(R.MakeXYWH(ex - 28 * s, lb_y + 66 * s, 56 * s, 14 * s), paint((210, 210, 214)))
    else:
        parcel_m(c, x, y, t, t0, s, label=new, label_t=t_sw + 0.35, label_col=new_col, open_=open_)


def store_page(c, x, y, t, t0, line=None, line_t=None, line_col=GR, strike_t=None):
    """laptop with a tiny shop page: a lamp photo, a price, and one shipping line that can be written / struck through"""
    def scr(c_, cx, cy):
        lamp_m(c_, cx - 150, cy + 110, t, t0 + 0.3, 0.45)
        mtext(c_, "MY STORE", cx + 60, cy - 70, 40, MK, pr(t, t0 + 0.4, 0.3), "pm")
        mtext(c_, "$39", cx + 80, cy, 46, BLU, pr(t, t0 + 0.6, 0.3), "pm")
        if line and line_t is not None and t > line_t:
            mtext(c_, line, cx + 70, cy + 76, 34, line_col, pr(t, line_t, 0.4), "pm")
            if strike_t is not None and t > strike_t:
                ink(c_, [[(cx - 30, cy + 64), (cx + 180, cy + 60)]], pr(t, strike_t, 0.2), RD, 8, pen_=False)
    laptop2(c, x, y, t, t0, w=460, h=300, screen=scr)


def grid30_m(c, x, y, t, t0, fill_t=None, step=0.07, upto=0, hl=None, cw=128, ch=78):
    """a 30-day month (6 x 5 boxes): days count on from fill_t (or `upto` days already written); hl = time day 30 gets circled red"""
    x0 = x - cw * 3; k = pr(t, t0, 0.6)
    grid = [[(x0, y), (x0 + cw * 6, y), (x0 + cw * 6, y + ch * 5), (x0, y + ch * 5), (x0, y)]]
    grid += [[(x0 + cw * i, y), (x0 + cw * i, y + ch * 5)] for i in range(1, 6)] + [[(x0, y + ch * j), (x0 + cw * 6, y + ch * j)] for j in range(1, 5)]
    ink(c, [wob(g, i + 470, 0.5) for i, g in enumerate(grid)], k, MK, 5, pen_=False)
    if k < 1: return
    m_ = upto
    if fill_t is not None and t > fill_t: m_ = max(m_, min(30, int((t - fill_t) / max(step, 1e-3)) + 1))
    for d in range(m_):
        i, j = d % 6, d // 6
        mtext(c, str(d + 1), x0 + cw * (i + 0.5), y + ch * (j + 0.5) + 14, 38, (BLU if d < 29 else RD) if upto == 0 else LIGHT, 1, "kb")
    if hl is not None and t > hl - 0.05:
        cx, cy = x0 + cw * 5.5, y + ch * 4.5
        c.drawRect(R.MakeXYWH(cx - cw / 2 + 4, cy - ch / 2 + 4, cw - 8, ch - 8), paint(RD, 0.15 * pr(t, hl, 0.3)))
        ink(c, [wob(circ_pts(cx, cy, 64, -150, 215, 30, ry=44), 12, 1.0)], pr(t, hl, 0.35), RD, 9, pen_=False)
        mtext(c, "30", cx, cy + 16, 48, RD, pr(t, hl + 0.1, 0.25), "pm")


def dash_line(c, a, b, prog, col=MK, w=7):
    if prog <= 0: return
    n = 14; (x0, y0), (x1, y1) = a, b
    for i in range(int(n * prog)):
        u0, u1 = i / n, (i + 0.55) / n
        c.drawLine(x0 + (x1 - x0) * u0, y0 + (y1 - y0) * u0, x0 + (x1 - x0) * u1, y0 + (y1 - y0) * u1, stroke(col, w))


# ---------------------------------------------------------------- shots
SHOTLIST = [("S_i1", 0.0, "cut"), ("S_i3", L0("i3") - 0.1, "wipe"), ("S_i4", L0("i4") - 0.1, "wipe"), ("S_a1", L0("a1") - 0.1, "wipe"),
            ("S_a3", L0("a3") - 0.1, "wipe"), ("S_b1", L0("b1") - 0.1, "wipe"), ("S_b2", L0("b2") - 0.1, "wipe"), ("S_b3", L0("b3") - 0.1, "wipe"),
            ("S_c1", L0("c1") - 0.1, "wipe"), ("S_c3", L0("c3") - 0.1, "wipe"), ("S_d1", L0("d1") - 0.1, "wipe"), ("S_d2", L0("d2") - 0.1, "wipe"),
            ("S_d3", L0("d3") - 0.1, "wipe"), ("S_e1", L0("e1") - 0.1, "wipe"), ("S_e2", L0("e2") - 0.1, "wipe"), ("S_t1", L0("t1") - 0.1, "wipe"),
            ("S_end", L0("z1") - 0.1, "wipe")]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
PX, PY = 540, 1310     # the held parcel's home spot


def S_i1(c, t):
    """frame 0 is a picture in motion: parcel with a pulsing '?' label, a calendar whose top page flicks, the pen hovering;
    on 'Thirty days' the pen circles day 30 and the label is rewritten 30 DAYS; on 'fifty-three' the penalty stamp drops"""
    t2 = L0("i2"); tf = TT("i2", "fifty-three", 0.6)
    grid30_m(c, 540, 730, t, -2.0, upto=30, hl=t2)
    if t < t2 - 0.05:
        parcel_m(c, PX, PY, t, -2.0, 1.15)
        q = 1 + 0.08 * math.sin(t * 7)
        c.save(); c.translate(PX - 23, PY + 60); c.scale(q, q); mtext(c, "?", 0, 20, 96, RD, 1, "pm"); c.restore()
        if t > 0.15: pen(c, 800 + 24 * math.sin(t * 3), 1060 + 12 * math.cos(t * 4))
    else:
        relabel(c, PX, PY, t, -2.0, "?", "30 DAYS", t2 - 0.05, 1.15)
    if t > tf - 0.15: stamp_m(c, 540, 930, "UP TO $53,088", pr(t, tf - 0.15, 0.22), col=RD, tilt=-6, size=74)
    say(c, t, -2.0, "do you know your shop has a", "DEADLINE?", MK, t1=t2 - 0.3, under=RD)
    say(c, t, t2 - 0.25, "you never set it · the default is", "30 DAYS", RD, under=RD)
    note(c, t, -2.0, "US FTC MAIL ORDER RULE · EDUCATION, NOT LEGAL ADVICE", t1=t2 + 0.3)
    note(c, t, tf, "MAX CIVIL PENALTY PER VIOLATION · FTC, 2025 LEVEL KEPT FOR 2026")


def S_i3(c, t):
    t0 = SHOT["S_i3"]["start"]; ts = TT("i3", "supplier", 0.4); tb = TT("i3", "straight", 0.6)
    store_page(c, 340, 1060, t, t0 + 0.05)
    hero(c, 150, FLOOR, 0.9, POSES["press"], Face("open", "smile", look=(1, 0)), t)
    ship_m(c, 790, 860, t, ts - 0.4, 0.62, "SUPPLIER · OVERSEAS")
    if t > ts - 0.1: arrow_m(c, (575, 960), (640, 900), pr(t, ts - 0.1, 0.35), BLU, 8)
    girl(c, 740, FLOOR, 0.85, POSES["wave"] if t > tb + 0.6 else POSES["stand"], Face("open", "smile", look=(-1, 0)), t, flip=True, dress=PINK)
    house_m(c, 870, FLOOR - 4, 0.6, t, tb - 0.6, BLU)
    if t > tb - 0.3:
        u = pr(t, tb - 0.3, 1.1)
        dash_line(c, (790, 960), (840, 1240), u, MK, 6)
        lamp_m(c, 790 + 50 * eio(u) - 40, 960 + 280 * eio(u) - 10, t, tb - 0.3, 0.45)
    say(c, t, t0 + 0.08, "you're starting", "A DROPSHIP STORE", MK, under=BLU, size=150)


def S_i4(c, t):
    t0 = SHOT["S_i4"]["start"]; tf = TT("i4", "Four", 0.3); tbl = TT("i4", "blame.", 0.5)
    hero(c, 240, FLOOR, 1.0, POSES["arms_up"], Face("open", "o", look=(1, -1)), t)
    u = min(1.0, max(0.0, (t - t0 - 0.2) / 1.6))
    bx = 60 + 400 * eio(u); by = 1000 - 120 * math.sin(math.pi * u)
    parcel_m(c, bx, by, t, t0 - 1, 0.5)
    dash_line(c, (60, 1000), (460, 1000), pr(t, t0 + 0.2, 1.4), LIGHT, 5)
    for i in range(4):
        tk = tf - 0.2 + i * 0.18
        if t < tk: continue
        x, y = 650 + (i % 2) * 180, 1060 + (i // 2) * 200; kk = pop_(t, tk)
        c.save(); c.translate(x, y); c.scale(kk, kk); parcel_m(c, 0, 0, t, -9, 0.45, label=str(i + 1), label_col=RD if i == 3 else MK); c.restore()
    if t > tbl - 0.3:
        ink(c, [wob(circ_pts(830, 1260, 110, -150, 215, 30, ry=90), 31, 1.0)], pr(t, tbl - 0.3, 0.35), RD, 8, pen_=False)
        mtext(c, "BLAME?", 830, 1420, 52, RD, pr(t, tbl - 0.1, 0.3), "pm")
    say(c, t, t0 + 0.08, "you never touch the box, but", "4 RULES", RD, under=RD)


def S_a1(c, t):
    t0 = SHOT["S_a1"]["start"]; t2 = L0("a2"); t2b = L0("a2b"); tr = TT("a2", "real", 0.5); tp = TT("a2b", "prove", 0.6)
    if t < t2b - 0.1:
        gov_m(c, 610, 1300, t, t0 + 0.05 if t < t2 else t0 - 3, sign="CONSUMER WATCHDOG" if t > t2 - 0.1 else None)
        if t > t2:   # the hero walks up to the FTC with a question, then gets the answer (keeps the 7-s shot moving)
            u = pr(t, t2, 2.2); hx = 70 + 110 * eio(u)
            hero(c, hx, FLOOR, 0.8, POSES["point"] if t > tr else POSES["stand"], Face("open", "smile" if t > tr else "flat", look=(1, -1)), t)
            if t < tr: mtext(c, "?", hx + 40, 1080, 90, RD, pop_(t, t2 + 0.6), "pm")
            else: ink(c, [[(hx + 10, 1060), (hx + 34, 1086), (hx + 80, 1020)]], pr(t, tr, 0.3), GR, 11, pen_=False)
    else:
        store_page(c, 340, 1150, t, t2b - 0.15, "SHIPS IN 2 DAYS", t2b + 0.1, GR)
        stopwatch_m(c, 820, 1000, t, t2b + 0.4, 85, run_t=t2b + 0.6)
        mtext(c, "PROOF?", 820, 1200, 74, RD, pr(t, tp - 0.3, 0.3), "pm")
        if t > tp + 0.3: ink(c, [[(740, 1270), (790, 1320), (900, 1220)]], pr(t, tp + 0.3, 0.3), GR, 12, pen_=False)
    say(c, t, t0 + 0.08, "rule one", "BACK IT UP", MK, t1=t2 - 0.3, under=GR)
    say(c, t, t2 - 0.25, "the FTC says you need", "A REAL REASON", GR, t1=t2b - 0.3, under=GR, size=150)
    say(c, t, t2b - 0.25, "promise two days?", "PROVE IT", RD, under=RD)
    note(c, t, t2 - 0.1, "FTC: \"A REASONABLE BASIS\" TO EXPECT YOU CAN SHIP ON TIME")


def S_a3(c, t):
    t0 = SHOT["S_a3"]["start"]; tn = TT("a3", "nothing", 0.4); tt_ = TT("a3", "thirty", 0.5)
    grid30_m(c, 540, 730, t, t0 + 0.1, fill_t=t0 + 0.6, step=(tt_ - t0 - 0.8) / 30, hl=tt_)
    relabel(c, 540, 1290, t, t0 + 0.2, None, "30 DAYS", tt_, 0.8)
    say(c, t, t0 + 0.08, "say nothing at all? the clock is", "30 DAYS", RD, under=RD)
    note(c, t, t0 + 0.6, "IF NO TIME IS STATED · 16 CFR 435.2(a) · FROM A COMPLETE ORDER")


def S_b1(c, t):
    t0 = SHOT["S_b1"]["start"]; tl = TT("b1", "late.", 0.5)
    ship_m(c, 330, 1260, t, t0 + 0.05, 1.0, "SUPPLIER")
    parcel_m(c, 330, 1080, t, t0 + 0.2, 0.45)
    snail_m(c, 790, 1420, t, tl - 0.4, 0.8)
    grid30_m(c, 740, 780, t, t0 + 0.3, upto=30, hl=tl - 0.3, cw=70, ch=46)
    if t > tl - 0.1:
        mtext(c, "DAY 30 · NOT SHIPPED", 740, 1080, 40, RD, pr(t, tl, 0.3), "pm")
    say(c, t, t0 + 0.08, "rule two · the lamp's running", "LATE", RD, under=RD)


def S_b2(c, t):
    t0 = SHOT["S_b2"]["start"]; tn = TT("b2", "new", 0.4); tc = TT("b2", "cancel", 0.5)
    hero(c, 150, FLOOR, 0.85, POSES["point"], Face("open", "flat", look=(1, 0)), t)
    girl(c, 910, FLOOR, 0.85, POSES["stand"], Face("open", "smile", look=(-1, 0)), t, flip=True, dress=PINK)
    u = min(1.0, max(0.0, (t - t0 - 0.2) / 1.0))
    envelope_m(c, 260 + 360 * eio(u), 1180 - 160 * math.sin(math.pi * u), t, t0 + 0.15, 0.9, "!")
    tagpill_m(c, 600, 900, "NEW DATE", pop_(t, tn - 0.2), BLU, 56)
    tagpill_m(c, 600, 1030, "CANCEL = FULL REFUND", pop_(t, tc - 0.2), RD, 50)
    say(c, t, t0 + 0.08, "before the deadline, tell them", "NEW DATE OR CANCEL", MK, under=BLU, size=140)
    note(c, t, t0 + 0.6, "BEFORE THE DEADLINE · 16 CFR 435.2(b)")


def S_b3(c, t):
    t0 = SHOT["S_b3"]["start"]; ty = TT("b3", "yes.", 0.3); tg = TT("b3", "again,", 0.4); tr = TT("b3", "real", 0.5)
    girl(c, 300, FLOOR, 0.85, POSES["stand"], Face("open", "flat"), t, dress=PINK)
    envelope_m(c, 300, 960, t, t0 + 0.1, 0.6, "+30")
    mtext(c, "...", 300, 1110, 90, LIGHT, pr(t, t0 + 0.6, 0.3), "pm")
    if t > ty - 0.3:
        ink(c, [[(200, 840), (260, 900), (400, 760)]], pr(t, ty - 0.3, 0.3), GR, 14, pen_=False)
        mtext(c, "= YES", 300, 740, 64, GR, pr(t, ty - 0.1, 0.3), "pm")
    if t > tg - 0.4:
        girl(c, 780, FLOOR, 0.85, POSES["stand"], Face("open", "flat"), t, flip=True, dress=PINK)
        envelope_m(c, 780, 960, t, tg - 0.4, 0.6, "+30")
        mtext(c, "AGAIN", 780, 870, 44, MK, pr(t, tg - 0.2, 0.3), "pm")
        mtext(c, "...", 780, 1110, 90, LIGHT, pr(t, tg - 0.1, 0.3), "pm")
    if t > tr - 0.3:
        cross(c, 690, 900, 870, 1030, pr(t, tr - 0.3, 0.2), RD, 12, 7); cross(c, 870, 900, 690, 1030, pr(t, tr - 0.15, 0.2), RD, 12, 8)
        tagpill_m(c, 780, 1210, "NEEDS A REAL YES", pop_(t, tr), RD, 42)
    say(c, t, t0 + 0.08, "first delay: silence counts once", "REAL YES", RD, under=RD)
    note(c, t, t0 + 0.6, "FIRST DELAY UP TO 30 DAYS: SILENCE = CONSENT · LATER: NO")


def S_c1(c, t):
    t0 = SHOT["S_c1"]["start"]; t2 = L0("c2"); ts = TT("c2", "seven", 0.4); tst = TT("c2", "store", 0.4); tdc = TT("c2", "doesn't", 0.5)
    if t < tst - 0.3:
        hero(c, 150, FLOOR, 0.8, POSES["hold"], Face("open", "smile"), t)
        girl(c, 870, FLOOR, 0.8, POSES["stand"], Face("open", "smile", look=(-1, 0)), t, flip=True, dress=PINK)
        u = min(1.0, max(0.0, (t - t0 - 0.4) / 1.4))
        for i in range(3):
            coin_m(c, 260 + 520 * eio(max(0, u - i * 0.1)), 1240 - 150 * math.sin(math.pi * min(1, u)) - i * 26, t, t0 + 0.3, 46, 1.0, "$")
        if t > t2: strip_m(c, 540, 800, 7, t, t2, fill_t=ts - 0.3, step=0.11, label="WORKING DAYS")
    else:
        strip_m(c, 540, 800, 7, t, t0 - 5, fill_t=t0 - 5, label="WORKING DAYS")
        giftcard_m(c, 540, 1200, t, tst - 0.3, 1.3, "STORE CREDIT", cross_t=tdc - 0.1)
    say(c, t, t0 + 0.08, "rule three", "THE MONEY", GR, t1=t2 - 0.3, under=GR)
    say(c, t, t2 - 0.25, "cancelled? refund within", "7 WORKING DAYS", GR, under=GR, size=150)
    note(c, t, t2 + 0.3, "16 CFR 435.1 · FTC GUIDE: NO CREDIT TOWARD FUTURE PURCHASES")


def S_c3(c, t):
    t0 = SHOT["S_c3"]["start"]; tg = TT("c3", "instead.", 0.4); t20 = TT("c3", "twenty", 0.3); tn = TT("c3", "nine", 0.4)
    ink(c, [wob([(130, 1440), (130, 1000), (470, 1000), (470, 1440)], 451, 0.8)], pr(t, t0 + 0.05, 0.5), MK, 8)
    mtext(c, "FASHION NOVA", 300, 960, 46, MK, pr(t, t0 + 0.4, 0.3), "pm")
    for r_ in range(3):
        for q in range(2): c.drawRect(R.MakeXYWH(170 + q * 160, 1060 + r_ * 110, 100, 70), stroke(MK, 4, pr(t, t0 + 0.5 + r_ * 0.05, 0.2)))
    for i in range(3):
        if t > tg - 0.4 + i * 0.15:
            u = pr(t, tg - 0.4 + i * 0.15, 0.6)
            giftcard_m(c, 470 + 230 * eio(u), 1130 + i * 130, t, tg - 0.4 + i * 0.15, 0.5, "GIFT CARD", tilt=-6 + i * 5)
    if t > t20 - 0.2: stamp_m(c, 700, 830, "SETTLED · 2020", pr(t, t20 - 0.2, 0.22), col=RD, tilt=-7, size=60)
    if t > tn - 0.2: mtext(c, "$9.3M", 760, 1040, 110, GR, pr(t, tn - 0.2, 0.4), "pm", pen_=True)
    say(c, t, t0 + 0.08, "the FTC said it gave gift cards · it paid", "$9.3M TO SETTLE", GR, under=GR, size=140)
    note(c, t, t0 + 0.6, "FTC, 21 APR 2020 · ALLEGATIONS, SETTLED · MONEY FOR CONSUMER REFUNDS")


def S_d1(c, t):
    t0 = SHOT["S_d1"]["start"]; tf = TT("d1", "supplier's", 0.4)
    hero(c, 220, FLOOR, 0.95, POSES["point"], Face("open", "smile", brows="up", look=(1, -1)), t)
    ship_m(c, 760, 1240, t, t0 + 0.1, 0.9, "SUPPLIER")
    relabel(c, 760, 960, t, t0 + 0.2, "LATE", "LATE", t0 + 99, 0.55)
    if t > tf - 0.2: speech(c, 380, 840, 520, 140, "THEIR FAULT!", pop_(t, tf - 0.2), 60, RD, tail=-1)
    say(c, t, t0 + 0.08, "last rule · your supplier's fault,", "RIGHT?", MK, under=RD)


def S_d2(c, t):
    t0 = SHOT["S_d2"]["start"]; ts = TT("d2", "seller.", 0.4); tw_ = TT("d2", "whoever", 0.4)
    hero(c, 200, FLOOR, 0.95, POSES["shock"], Face("open", "o", look=(1, -1)), t)
    ship_m(c, 760, 1320, t, t0 - 3, 0.62, None)
    if t > tw_ - 0.2: tagpill_m(c, 760, 1180, "just ships it", pop_(t, tw_ - 0.2), LIGHT, 36)
    relabel(c, 560, 1010, t, t0 - 3, "LATE", "SELLER: YOU", ts - 0.35, 1.0)
    if t > ts + 0.2:
        arrow_m(c, (440, 1100), (260, 1180), pr(t, ts + 0.2, 0.35), RD, 9)
    say(c, t, t0 + 0.08, "the one taking the order", "IS THE SELLER", RD, under=RD, size=150)
    note(c, t, t0 + 0.6, "FTC GUIDE: \"THE PERSON SOLICITING THE ORDER … IS THE SELLER\"")


def S_d3(c, t):
    t0 = SHOT["S_d3"]["start"]; tm = TT("d3", "most", 0.3); th = TT("d3", "Honestly?", 0.3); tn = TT("d3", "tonight.", 0.4)
    if t < th - 0.2:
        for i in range(12):
            x, y = 140 + (i % 4) * 250, 920 + (i // 4) * 230; tk = t0 + 0.15 + i * 0.07
            if t < tk: continue
            parcel_m(c, x, y, t, tk, 0.38)
            if t > tm - 0.3 + i * 0.06: mtext(c, "$", x + 70, y - 60, 60, RD, pr(t, tm - 0.3 + i * 0.06, 0.2), "pm")
    else:
        ship_m(c, 380, 1300, t, th - 0.3, 0.9, "YOUR SUPPLIER")
        stopwatch_m(c, 790, 1080, t, th, 120, run_t=th + 0.3)
        hero(c, 790, FLOOR + 40, 0.7, POSES["point_up"], Face("open", "smile", look=(0, -1)), t)
    say(c, t, t0 + 0.08, "the most, per violation", "$53,088", RD, t1=th - 0.3, under=RD)
    say(c, t, th - 0.25, "honestly? I'd do it tonight", "TIME YOUR SUPPLIER", BLU, under=BLU, size=140)
    note(c, t, t0 + 0.6, "UP TO $53,088 PER VIOLATION (MAXIMUM CIVIL PENALTY) · FTC", t1=th)


def S_e1(c, t):
    t0 = SHOT["S_e1"]["start"]; td = TT("e1", "deliver", 0.4); tu = TT("e1", "Unless", 0.4)
    ink(c, [wob([(80, 1080), (80, 820), (300, 820), (300, 1080), (80, 1080)], 461, 0.8)], pr(t, t0 + 0.05, 0.4), MK, 7)
    mtext(c, "UK", 190, 990, 110, BLU, pr(t, t0 + 0.3, 0.3), "pm")
    girl(c, 740, FLOOR, 0.8, POSES["stand"] if t < td else POSES["arms_up"], Face("open", "smile", look=(-1, 0)), t, flip=True, dress=PINK)
    house_m(c, 870, FLOOR - 4, 0.55, t, t0 + 0.2, BLU)
    u = pr(t, td - 0.6, 1.0)
    relabel(c, 280 + 260 * eio(u), 1330, t, t0 + 0.2, None, "30 DAYS UK", t0 + 0.6, 0.6)
    if t > td: mtext(c, "AT THE DOOR", 640, 1140, 48, GR, pr(t, td, 0.3), "pm")
    if t > tu - 0.2: mtext(c, "unless you both agreed", 640, 870, 46, BLU, pr(t, tu - 0.2, 0.5), "kb")
    say(c, t, t0 + 0.08, "UK: not ship it,", "DELIVER IN 30 DAYS", BLU, under=BLU, size=140)
    note(c, t, t0 + 0.6, "CONSUMER RIGHTS ACT 2015, s.28 · UNLESS AGREED OTHERWISE")


def S_e2(c, t):
    t0 = SHOT["S_e2"]["start"]; tf = TT("e2", "fourteen", 0.3); ta = TT("e2", "arrives.", 0.5)
    house_m(c, 170, 1260, 0.9, t, t0 - 3, BLU)
    parcel_m(c, 340, 1250, t, t0 - 3, 0.45)
    strip_m(c, 560, 960, 14, t, t0 + 0.1, fill_t=tf - 0.2, step=0.1, cell=56, label="DAY 1 = IT ARRIVES")
    if t > ta: tagpill_m(c, 680, 1200, "CANCEL", pop_(t, ta), RD, 56)
    say(c, t, t0 + 0.08, "they can still cancel for", "14 DAYS", RD, under=RD)
    note(c, t, t0 + 0.6, "CONSUMER CONTRACTS REGULATIONS 2013, REG. 30 · UK")


def S_t1(c, t):
    t0 = SHOT["S_t1"]["start"]; tc = TT("t1", "Check", 0.4); ta = TT("t1", "few,", 0.3); tp = TT("t1", "page.", 0.4)
    if t < ta - 0.3:
        hero(c, 220, FLOOR, 0.85, POSES["wave"], Face("open", "smile"), t)
        house_m(c, 220, 1100, 0.7, t, t0 + 0.05, OR); mtext(c, "YOUR DOOR", 220, 1150, 40, OR, pr(t, t0 + 0.4, 0.3), "pm")
        u = pr(t, t0 + 0.3, 1.4)
        parcel_m(c, 900 - 560 * eio(u), 1260 - 120 * math.sin(math.pi * u), t, t0 + 0.2, 0.45)
        stopwatch_m(c, 760, 900, t, t0 + 0.2, 100, run_t=t0 + 0.4, stop_t=tc + 0.2)
        if t > tc: mtext(c, "9 DAYS", 760, 1080, 60, RD, pr(t, tc, 0.3), "pm")
    else:
        store_page(c, 470, 1300, t, ta - 0.3, "SHIPS IN 12 DAYS", tp - 0.5, GR)
        mtext(c, "9 + A FEW", 470, 920, 80, RD, pr(t, ta - 0.2, 0.4), "pm", pen_=True)
        if t > tp - 0.6: arrow_m(c, (470, 950), (560, 1180), pr(t, tp - 0.6, 0.3), RD, 8)
    say(c, t, t0 + 0.08, "before you launch", "TEST ORDER", OR, under=OR)
    note(c, t, t0 + 0.6, "MADE-UP NUMBERS · ONE ORDER ALONE ISN'T PROOF, SO ADD A BUFFER")


def S_end(c, t):
    t0 = SHOT["S_end"]["start"]; tz2 = L0("z2"); tfa = TT("z1", "fast,", 0.4); tch = TT("z1", "cheap?", 0.4)
    c.save(); c.translate(0, 10 * math.sin(t * 2.4)); c.rotate(1.5 * math.sin(t * 1.7))
    relabel(c, PX, 1020, t, t0 - 3, "30 DAYS", "30 DAYS", t0 + 99, 1.1)
    c.restore()
    tagpill_m(c, 290, 1340, "SHIP FAST", pop_(t, tfa - 0.2), GR, 52)
    tagpill_m(c, 720, 1340, "SHIP CHEAP", pop_(t, tch - 0.2), OR, 52)
    for i, (x, tm) in enumerate(((290, tfa), (720, tch))):
        if t > tm: ink(c, [wob(circ_pts(x, 1330, 190, -150, 215, 40, ry=74), 95 + i, 1.4)], pr(t, tm, 0.35), RD, 7, pen_=False)
    say(c, t, t0 + 0.08, "save this before you open a store", "FAST OR CHEAP?", MK, t1=tz2 - 0.3, under=BLU)
    say(c, t, tz2 - 0.25, "send it to the friend who wants a store", "SAVE THIS", BLU, under=OR)
    note(c, t, t0 + 0.6, "COMMENT ONE WORD · EDUCATION, NOT LEGAL ADVICE")


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}
SURF = surface()
IMPACTS = [(TT("i2", "fifty-three", 0.6) - 0.15, 0.14, 5), (TT("c3", "twenty", 0.3) - 0.2, 0.14, 5), (TT("d2", "seller.", 0.4), 0.14, 4)]
# the RULE MAP (story upgrade, 9 Nov): which of the 4 rules we're on, ticked once passed
_MAP = {"S_i4": (-1, ()), "S_a1": (0, ()), "S_a3": (0, ()), "S_b1": (1, (0,)), "S_b2": (1, (0,)), "S_b3": (1, (0,)),
        "S_c1": (2, (0, 1)), "S_c3": (2, (0, 1)), "S_d1": (3, (0, 1, 2)), "S_d2": (3, (0, 1, 2)), "S_d3": (3, (0, 1, 2)), "S_t1": (-1, (0, 1, 2, 3))}
_TOP = {"S_a1": "RULE 1 OF 4", "S_a3": "RULE 1 OF 4", "S_b1": "RULE 2 OF 4", "S_b2": "RULE 2 OF 4", "S_b3": "RULE 2 OF 4",
        "S_c1": "RULE 3 OF 4", "S_c3": "RULE 3 OF 4", "S_d1": "RULE 4 OF 4", "S_d2": "RULE 4 OF 4", "S_d3": "RULE 4 OF 4",
        "S_e1": "SELLING IN THE UK", "S_e2": "SELLING IN THE UK", "S_t1": "BEFORE YOU LAUNCH"}


def topline(sid): return f"HOW TO START · {_TOP[sid]}" if sid in _TOP else "OOPSMYBUSINESS · HOW TO START"


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
