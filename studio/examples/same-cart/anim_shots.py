# ================= HOW IT WORKS EP 5: same eggs, same store, five prices at once — the Instacart price tests (whiteboard).
# Held object: ONE egg carton with a swing price tag; the tag's number keeps changing (five tags fan out → two phones → your tag only
# → five tags slide together into ONE tag → two phones compare). New drawings: shopfront_m (awning + window), hand_m (a big hand from
# the top with a word on its cuff), receipt_m (a till receipt that grows), newspaper_m, pin_m (location pin), sticky_m, ny_m (plain box
# state label), coinpile_m, and the QUESTION MAP (qmap: the hook's two questions as pills under the brand pill — WHO PICKS? and STILL? —
# the current one coloured, answered ones ticked).
# Opening move (new): frame 0 already shows the carton and three price tags; tags 4 and 5 land at 0.35 s and 0.7 s with a till ding,
# so the surprise (five prices) is on screen before the 3-second mark; the 5th tag wobbles red and the pen hovers. =================
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

GOLD = (236, 176, 40); LIGHT = (150, 156, 170); PINK = (236, 92, 150); YEL = (255, 232, 110)
PRICES = ["$3.99", "$4.28", "$4.59", "$4.69", "$4.79"]
TAGPOS = [(190, 930, -14), (360, 860, -7), (540, 835, 0), (720, 860, 7), (890, 930, 14)]


# ---------------------------------------------------------------- new marker props (this episode)
def shopfront_m(c, x, y, t, t0, s=1.0, label="STORE", col=RD):
    """a small shop front: striped awning (hatched), window, door; label written on the sign"""
    k = pr(t, t0, 0.6); w, h = 360 * s, 300 * s
    body = [(x - w / 2, y), (x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y), (x - w / 2, y)]
    awn = [(x - w / 2 - 20 * s, y - h), (x + w / 2 + 20 * s, y - h), (x + w / 2, y - h + 70 * s), (x - w / 2, y - h + 70 * s), (x - w / 2 - 20 * s, y - h)]
    sign = [(x - w / 2 + 20 * s, y - h - 90 * s), (x + w / 2 - 20 * s, y - h - 90 * s), (x + w / 2 - 20 * s, y - h - 10 * s), (x - w / 2 + 20 * s, y - h - 10 * s), (x - w / 2 + 20 * s, y - h - 90 * s)]
    door = [(x + 40 * s, y), (x + 40 * s, y - 170 * s), (x + 130 * s, y - 170 * s), (x + 130 * s, y)]
    win = [(x - 140 * s, y - 70 * s), (x - 140 * s, y - 190 * s), (x - 10 * s, y - 190 * s), (x - 10 * s, y - 70 * s), (x - 140 * s, y - 70 * s)]
    if k > 0.6:
        c.save(); c.clipPath(_path(awn))
        for i in range(9):
            if i % 2 == 0: c.drawRect(R.MakeXYWH(x - w / 2 - 20 * s + i * 45 * s, y - h, 45 * s, 70 * s), paint(col, 0.55 * pr(k, 0.6, 0.4)))
        c.restore()
    ink(c, [wob(body, 501, 0.8), wob(awn, 502, 0.8), wob(sign, 503, 0.6), wob(door, 504, 0.6), wob(win, 505, 0.6)], k, MK, 7)
    if label: mtext(c, label, x, y - h - 34 * s, int(48 * s), MK, pr(t, t0 + 0.5, 0.3), "pm")


def hand_m(c, x, y, t, t0, word=None, col=BLU, reach=1.0):
    """a big drawn hand coming down from the top (cuff up, fingers pointing down); word written on the cuff"""
    k = pr(t, t0, 0.5); y = y - 260 * (1 - eio(min(1.0, reach)))
    arm = [[(x - 70, 730), (x - 70, y - 220)], [(x + 70, 730), (x + 70, y - 220)]]
    cuff = [(x - 90, y - 220), (x + 90, y - 220), (x + 90, y - 120), (x - 90, y - 120), (x - 90, y - 220)]
    palm = [(x - 80, y - 120), (x - 95, y - 20), (x - 60, y + 40), (x - 30, y + 70), (x + 10, y + 75), (x + 50, y + 55), (x + 80, y + 10), (x + 85, y - 120)]
    fingers = [[(x - 40, y + 10), (x - 44, y + 110)], [(x - 4, y + 20), (x - 2, y + 130)], [(x + 34, y + 14), (x + 40, y + 110)]]
    if k >= 1: c.drawPath(_path(cuff), paint(col, 0.25)); c.drawPath(_path(palm), paint(WHITE))
    ink(c, [wob(p, 510 + i, 0.6) for i, p in enumerate(arm)] + [wob(cuff, 515, 0.6), wob(palm, 516, 0.8)] + [wob(f, 517 + i, 0.5) for i, f in enumerate(fingers)], k, MK, 7)
    if word: mtext(c, word, x, y - 150, 52, col, pr(t, t0 + 0.4, 0.3), "pm")


def receipt_m(c, x, y, t, t0, length=300, grow_t=None, grow=0.0, total=None, col=MK):
    """a till receipt hanging down from (x, y); from grow_t it gets `grow` px longer; zig-zag bottom edge"""
    k = pr(t, t0, 0.4)
    if k <= 0: return
    L = length + (grow * eio(pr(t, grow_t, 0.9)) if grow_t is not None else 0)
    w = 150; Lk = L * k
    zz = [(x - w / 2 + i * w / 8, y + Lk + (10 if i % 2 else 0)) for i in range(9)]
    outline = [(x - w / 2, y), (x + w / 2, y)] + zz[::-1] + [(x - w / 2, y)]
    outline = [(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + Lk)] + zz[::-1][1:] + [(x - w / 2, y)]
    c.drawPath(_path(outline), paint(WHITE)); c.drawPath(_path(outline), stroke(col, 5))
    for i in range(max(0, int(Lk // 38) - 1)):
        yy = y + 30 + i * 38; ww = 90 if i % 3 else 60
        c.drawLine(x - w / 2 + 20, yy, x - w / 2 + 20 + ww, yy, stroke(LIGHT, 5))
    if total and k >= 1: mtext(c, total, x, y + Lk - 22, 34, RD, 1, "pm")


def newspaper_m(c, x, y, t, t0, head="PRICES", tilt=-5):
    k = pr(t, t0, 0.5); w, h = 400, 300
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt)
    pg = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)]
    if k >= 1: c.drawPath(_path(pg), paint(WHITE))
    ink(c, [wob(pg, 531, 0.6), [(-w / 2 + 20, -h / 2 + 90), (w / 2 - 20, -h / 2 + 90)]], k, MK, 6, pen_=False)
    mtext(c, head, 0, -h / 2 + 70, 50, MK, pr(t, t0 + 0.3, 0.3), "pm")
    for i in range(4):
        for col_ in range(2):
            c.drawLine(-w / 2 + 24 + col_ * 190, -h / 2 + 125 + i * 36, -w / 2 + 24 + col_ * 190 + 150 - (i % 2) * 40, -h / 2 + 125 + i * 36, stroke(LIGHT, 6, pr(t, t0 + 0.4 + i * 0.05, 0.2)))
    c.restore()


def pin_m(c, x, y, t, t0, s=1.0, col=RD):
    k = pr(t, t0, 0.4)
    if k <= 0: return
    pts = [(x, y)] + [(x + 60 * s * math.cos(math.radians(a_)), y - 110 * s + 60 * s * math.sin(math.radians(a_))) for a_ in range(150, 391, 15)] + [(x, y)]
    if k >= 1: c.drawPath(_path(pts), paint(col, 0.75)); c.drawCircle(x, y - 110 * s, 22 * s, paint(WHITE))
    ink(c, [wob(pts, 541, 0.5)], k, MK, 6, pen_=False)


def sticky_m(c, x, y, t, t0, text, s=1.0, tilt=6, col=RD):
    k = pop_(t, t0)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k * s, k * s)
    c.drawRect(R.MakeXYWH(-170 + 6, -110 + 10, 340, 220), paint((0, 0, 0), 0.12, blur=8))
    c.drawRect(R.MakeXYWH(-170, -110, 340, 220), paint(YEL)); c.drawRect(R.MakeXYWH(-170, -110, 340, 34), paint((240, 210, 80)))
    sz = 50; f = font("pm", sz)
    while tw(f, text) > 300: sz -= 2; f = font("pm", sz)
    c.drawString(text, -tw(f, text) / 2, 30, f, paint(col)); c.restore()


def ny_m(c, x, y, t, t0, label="NEW YORK"):
    """a plain hand-drawn state shape (not map data): a rough box with one bumpy side, label inside"""
    k = pr(t, t0, 0.6)
    pts = [(x - 200, y + 70), (x - 200, y - 20), (x - 110, y - 40), (x - 40, y - 110), (x + 140, y - 120), (x + 170, y - 40), (x + 200, y + 70), (x - 200, y + 70)]
    if k > 0.6: hatch(c, _path(pts), pr(k, 0.6, 0.4), BLU, gap=18, w=5, bbox=(x - 210, y - 130, x + 210, y + 80), a=0.35)
    ink(c, [wob(pts, 551, 1.0)], k, MK, 7)
    mtext(c, label, x, y + 30, 46, MK, pr(t, t0 + 0.5, 0.3), "pm")


def coinpile_m(c, x, y, t, t0, n=9):
    for i in range(n):
        tk = t0 + i * 0.07
        if t < tk: continue
        u = pr(t, tk, 0.3); row = 0 if i < 4 else (1 if i < 7 else 2); col_ = i if i < 4 else (i - 4 if i < 7 else i - 7)
        cx = x - 90 + col_ * 60 + row * 30; cy = y - row * 40
        coin(c, cx, cy - 200 * (1 - eio(u)), 34, spin=t * 3 if u < 1 else 0)


def qmap(c, active, done=(), a=1.0, y=380):
    """the hook's two questions as small pills under the brand pill; active coloured, done ticked"""
    if a <= 0: return
    for i, (txt, x) in enumerate((("WHO PICKS?", 360), ("STILL?", 690))):
        on = (i == active); col = RD if on else (GR if i in done else LIGHT)
        sz = 36 if on else 30; f = font("pm", sz); w = tw(f, txt) + 50; h = 60 if on else 50
        c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), h / 2, h / 2, paint(WHITE, a))
        c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), h / 2, h / 2, stroke(col, 5 if on else 3, a))
        c.drawString(txt, x - tw(f, txt) / 2, y + sz * 0.36, f, paint(col, a))
        if i in done: ink(c, [[(x + w / 2 - 6, y - 4), (x + w / 2 + 10, y + 14), (x + w / 2 + 40, y - 26)]], 1, GR, 7, pen_=False)


def tags_fan(c, t, times, hot=None, s=0.78):
    for i, ((x, y, tl), tm) in enumerate(zip(TAGPOS, times)):
        if t < tm: continue
        ink(c, [wob([(x, y + 40), (540, 1090)], 560 + i, 0.4)], pr(t, tm, 0.3), LIGHT, 3, pen_=False)
        kk = pop_(t, tm, 0.3, 1.5)
        c.save(); c.translate(x, y); c.scale(kk, kk)
        tag_m(c, 0, 0, PRICES[i], t, tm, col=RD if i == 4 else BLU, tilt=tl, s=s, hot=(hot is not None and t > hot and i == 4))
        c.restore()


def eggphone(c, x, y, t, t0, price, col=BLU, s=0.8):
    """a phone showing the carton and its price"""
    def scr(c_, cx, cy, w, h):
        carton_m(c_, cx, cy + 40 * s, t, t0 + 0.2, 0.42 * s / 0.8, 1.0)
        if price: mtext(c_, price, cx, cy + 200 * s, int(70 * s / 0.8), col, pr(t, t0 + 0.5, 0.3), "pm")
        mtext(c_, "EGGS · 12", cx, cy - 150 * s, int(36 * s / 0.8), MK, pr(t, t0 + 0.4, 0.3), "kb")
    phone_m(c, x, y, t, t0, s, screen=scr)


# ---------------------------------------------------------------- shots
SHOTLIST = [("S_i1", 0.0, "cut"), ("S_i2", L0("i2") - 0.1, "wipe"), ("S_i3", L0("i3") - 0.1, "wipe"), ("S_i4", L0("i4") - 0.1, "wipe"),
            ("S_a1", L0("a1") - 0.1, "wipe"), ("S_a3", L0("a3") - 0.1, "wipe"), ("S_a4", L0("a4") - 0.1, "wipe"), ("S_a5", L0("a5") - 0.1, "wipe"),
            ("S_b1", L0("b1") - 0.1, "wipe"), ("S_b3", L0("b3") - 0.1, "wipe"), ("S_c2", L0("c2") - 0.1, "wipe"), ("S_c3", L0("c3") - 0.1, "wipe"),
            ("S_c4", L0("c4") - 0.1, "wipe"), ("S_d1", L0("d1") - 0.1, "wipe"), ("S_d2", L0("d2") - 0.1, "wipe"), ("S_d3", L0("d3") - 0.1, "wipe"),
            ("S_e1", L0("e1") - 0.1, "wipe"), ("S_e3", L0("e3") - 0.1, "wipe"), ("S_e4", L0("e4") - 0.1, "wipe"), ("S_t1", L0("t1") - 0.1, "wipe"),
            ("S_end", L0("z1") - 0.1, "wipe")]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
TAG_T = [-2.0, -2.0, -2.0, 0.35, 0.7]


def S_i1(c, t):
    """frame 0 = carton + three tags already up; tags 4 and 5 land at 0.35 / 0.7 s (till dings); the red one wobbles; pen hovers"""
    tf = TT("i1", "five", 0.6)
    carton_m(c, 540, 1180, t, -2.0, 1.15, 0.0)
    tags_fan(c, t, TAG_T, hot=tf)
    if t > tf - 0.1: mtext(c, "×5", 880, 1180, 90, RD, pr(t, tf - 0.1, 0.3), "pm")
    if t < L1("i1"): pen(c, 860 + 20 * math.sin(t * 3), 1040 + 10 * math.cos(t * 4))
    say(c, t, -2.0, "same eggs · same store · same time", "5 PRICES", RD, under=RD)
    note(c, t, -2.0, "ONE STORE, WASHINGTON DC · CONSUMER REPORTS + GROUNDWORK, DEC 2025")


def S_i2(c, t):
    t0 = SHOT["S_i2"]["start"]; tr = TT("i2", "real", 0.5)
    hero(c, 170, FLOOR, 0.95, POSES["hold"], Face("open", "smile", look=(1, 0)), t)
    eggphone(c, 410, 1080, t, t0 + 0.05, None, s=0.7)
    mtext(c, "INSTACART", 410, 820, 50, MK, pr(t, t0 + 0.3, 0.4), "pm", pen_=True)
    shopfront_m(c, 800, 1400, t, tr - 0.5, 0.8, "STORE")
    if t > tr - 0.2: arrow_m(c, (560, 1180), (650, 1240), pr(t, tr - 0.2, 0.35), BLU, 8, bend=0.2)
    say(c, t, t0 + 0.08, "an app shops it for you", "INSTACART", MK, under=BLU)
    note(c, t, t0 + 0.6, "A US GROCERY DELIVERY APP · A SHOPPER BUYS IT IN A REAL STORE")


def S_i3(c, t):
    t0 = SHOT["S_i3"]["start"]; tf = TT("i3", "four", 0.3); ts = TT("i3", "same", 0.4); tn = TT("i3", "Neither", 0.3)
    eggphone(c, 300, 1100, t, t0 + 0.05, "$3.99", BLU, 0.75)
    eggphone(c, 740, 1100, t, tf - 0.4, "$4.79", RD, 0.75)
    if t > ts - 0.2: dash_line(c, (520, 800), (520, 1400), pr(t, ts - 0.2, 0.6), MK, 7)
    if t > tn - 0.1:
        for x in (300, 740): mtext(c, "?", x, 770, 80, LIGHT, pop_(t, tn - 0.1 + (0.15 if x > 500 else 0)), "pm")
    say(c, t, t0 + 0.08, "same carton", "$3.99 vs $4.79", MK, under=RD, size=150)
    note(c, t, t0 + 0.6, "PRICES FROM THE REPORT · SAME STORE, SAME TIME")


def S_i4(c, t):
    t0 = SHOT["S_i4"]["start"]; tw_ = TT("i4", "Who", 0.3); ts = TT("i4", "still", 0.3)
    hero(c, 220, FLOOR, 0.95, POSES["shrug"] if t > tw_ else POSES["hold"], Face("open", "o", look=(1, -1)), t)
    tag_m(c, 560, 1180, "$?", t, t0 + 0.05, RD, -6, 0.9)
    hand_m(c, 560, 1000, t, tw_ - 0.5, "WHO?", BLU, pr(t, tw_ - 0.5, 0.8))
    if t > ts - 0.3:
        calendar(c, 830, 1200, 0.8, "DEC 2025", "NOW?", pop_(t, ts - 0.3))
        mtext(c, "STILL?", 830, 1380, 56, RD, pr(t, ts, 0.3), "pm")
    say(c, t, t0 + 0.08, "two questions", "WHO PICKS IT?", MK, under=RD, size=150)


def S_a1(c, t):
    t0 = SHOT["S_a1"]["start"]; tv = TT("a1", "volunteers", 0.3); ts = TT("a1", "same", 0.3)
    for i in range(40):
        r, q = divmod(i, 8); tk = t0 + 0.2 + i * 0.035
        if t < tk: continue
        x = 170 + q * 105; y = 860 + r * 92; kk = pop_(t, tk, 0.25)
        c.drawCircle(x, y, 26 * kk, paint(WHITE)); c.drawCircle(x, y, 26 * kk, stroke(MK, 5))
        c.drawCircle(x - 8, y - 3, 3.5 * kk, paint(MK)); c.drawCircle(x + 8, y - 3, 3.5 * kk, paint(MK))
        if t > ts - 0.2 + q * 0.03: c.drawRect(R.MakeXYWH(x + 20, y + 10, 30, 16), paint(CARD_BOARD, pr(t, ts - 0.2 + q * 0.03, 0.2)))
    cnt = int(437 * min(1.0, pr(t, t0 + 0.2, max(0.5, tv - t0))))
    if t > t0 + 0.25: mtext(c, f"{cnt} PEOPLE", 540, 1400, 80, BLU, 1, "pm")
    if t > ts: mtext(c, "AT THE SAME MOMENT", 540, 800, 46, RD, pr(t, ts, 0.4), "pm")
    say(c, t, t0 + 0.08, "volunteers shopping at once", "437", BLU, under=BLU)
    note(c, t, t0 + 0.8, "CONSUMER REPORTS · GROUNDWORK COLLABORATIVE · MORE PERFECT UNION")


def S_a3(c, t):
    t0 = SHOT["S_a3"]["start"]; td = TT("a3", "different", 0.3)
    x0, y0, cell = 540 - 5 * 60, 800, 60
    order = sorted(range(100), key=lambda i: (i * 37) % 100)
    rank = {i: n for n, i in enumerate(order)}
    for i in range(100):
        r_, q = divmod(i, 10); bx, by = x0 + q * cell, y0 + r_ * cell
        k = pr(t, t0 + 0.1 + i * 0.008, 0.15)
        if k <= 0: continue
        red = (i % 4 != 3) and t > td - 0.4 + rank[i] * 0.008
        c.drawRect(R.MakeXYWH(bx + 5, by + 5, cell - 10, cell - 10), paint((255, 228, 224) if red else (236, 240, 246), k))
        c.drawRect(R.MakeXYWH(bx + 5, by + 5, cell - 10, cell - 10), stroke(RD if red else MK, 3, k))
    say(c, t, t0 + 0.08, "came up at different prices", "3 IN 4 ITEMS", RD, under=RD)
    note(c, t, t0 + 0.6, "ABOUT 3/4 OF ITEMS (74%) · GROUNDWORK + CONSUMER REPORTS")


def S_a4(c, t):
    t0 = SHOT["S_a4"]["start"]; tt_ = TT("a4", "twenty-three", 0.3)
    base_y = 1380
    for i, (x, col) in enumerate(((360, BLU), (680, RD))):
        hh = 300 * (1 + 0.23 * eio(pr(t, tt_ - 0.2, 0.6))) if i == 1 else 300
        rect = [(x - 90, base_y), (x - 90, base_y - hh), (x + 90, base_y - hh), (x + 90, base_y), (x - 90, base_y)]
        if t > t0 + 0.3 + i * 0.2: hatch(c, _path(rect), pr(t, t0 + 0.3 + i * 0.2, 0.5), col, gap=18, w=6, bbox=(x - 100, base_y - 420, x + 100, base_y), a=0.55)
        ink(c, [wob(rect, 600 + i, 0.6)], pr(t, t0 + 0.1 + i * 0.2, 0.5), MK, 7)
        mtext(c, "SHOPPER " + "AB"[i], x, base_y + 70, 40, col, pr(t, t0 + 0.3 + i * 0.2, 0.3), "pm")
    if t > tt_ - 0.1:
        arrow_m(c, (850, 1250), (850, 1030), pr(t, tt_ - 0.1, 0.3), RD, 10)
        mtext(c, "+23%", 850, 990, 80, RD, pr(t, tt_, 0.3), "pm")
    ink(c, [wob([(220, base_y + 4), (900, base_y)], 610, 0.6)], pr(t, t0, 0.4), MK, 6, pen_=False)
    say(c, t, t0 + 0.08, "same item, one shopper paid up to", "+23%", RD, under=RD)
    note(c, t, t0 + 0.6, "SAME ITEM, STORE AND TIME · GROUNDWORK, 9 DEC 2025", y=1530)


def S_a5(c, t):
    t0 = SHOT["S_a5"]["start"]; ts = TT("a5", "seven", 0.3)
    cart_m(c, 300, 1350, t, t0 + 0.05, 0.7, 1.0, GR)
    cart_m(c, 740, 1350, t, t0 + 0.25, 0.7, 1.0, GR)
    receipt_m(c, 300, 820, t, t0 + 0.6, 180)
    receipt_m(c, 740, 820, t, t0 + 0.7, 180, grow_t=ts - 0.4, grow=70)
    if t > ts - 0.1: mtext(c, "≈ 7%", 520, 960, 76, RD, pr(t, ts - 0.1, 0.3), "pm", pen_=True)
    say(c, t, t0 + 0.08, "whole baskets, on average", "~7% APART", RD, under=RD)
    note(c, t, t0 + 0.6, "AVERAGE GAP IN BASKET TOTALS · SAME ITEMS, SAME STORES")


def S_b1(c, t):
    t0 = SHOT["S_b1"]["start"]; tc = TT("b1", "coin", 0.3); tr = TT("b1", "random.", 0.4); t2 = L0("b2"); to = TT("b2", "own", 0.3)
    if t < t2 - 0.15:
        coin_m(c, 520, 1030, t, tc - 0.3, 80, 0.9, "?")
        extra(c, 230, FLOOR, 0.75, POSES["stand"], Face("open", "smile"), t, scarf=BLU)
        girl(c, 820, FLOOR, 0.75, POSES["stand"], Face("open", "smile"), t, flip=True, dress=PINK)
        if t > tr - 0.5:
            tagpill_m(c, 230, 1130, "GROUP A", pop_(t, tr - 0.5), BLU, 44)
            tagpill_m(c, 800, 1130, "GROUP B", pop_(t, tr - 0.3), PU, 44)
            arrow_m(c, (460, 1070), (310, 1100), pr(t, tr - 0.5, 0.3), BLU, 7); arrow_m(c, (580, 1070), (720, 1100), pr(t, tr - 0.3, 0.3), PU, 7)
    else:
        shopfront_m(c, 520, 1400, t, t2 - 0.1, 1.3, "STORE")
        tag_m(c, 840, 880, "$ ?", t, to - 0.3, GR, -6, 0.7)
    say(c, t, t0 + 0.08, "Instacart's answer", "A COIN TOSS", MK, t1=t2 - 0.3, under=BLU)
    say(c, t, t2 - 0.25, "it says", "STORES SET PRICES", GR, under=GR, size=140)
    note(c, t, t0 + 0.6, "INSTACART: SHOPPERS ASSIGNED AT RANDOM · 10 RETAIL PARTNERS", t1=t2 - 0.2)
    note(c, t, t2, "INSTACART, 22 DEC 2025: RETAILERS \"SET THEIR OWN PRICES\"")


def S_b3(c, t):
    t0 = SHOT["S_b3"]["start"]; tn = TT("b3", "never", 0.3); tg = TT("b3", "negligible.", 0.3)
    folder_m(c, 300, 1150, t, t0 + 0.05, "YOUR DATA", BLU)
    if t > tn - 0.2: speech(c, 690, 900, 400, 130, "NOT USED", pop_(t, tn - 0.2), 62, BLU, tail=-1)
    if t > tn + 0.2: mtext(c, "INSTACART SAYS", 690, 1060, 40, MK, pr(t, tn + 0.2, 0.3), "kb")
    if t > tg - 0.5:
        mtext(c, "~7%", 720, 1250, 90, RD, pr(t, tg - 0.5, 0.3), "pm")
        mtext(c, "\"negligible\"", 720, 1340, 54, BLU, pr(t, tg - 0.1, 0.4), "kb")
    say(c, t, t0 + 0.08, "Instacart says", "NO PERSONAL DATA", BLU, under=BLU, size=140)
    note(c, t, t0 + 0.6, "INSTACART'S OWN STATEMENTS, DEC 2025")


def S_c2(c, t):
    t0 = SHOT["S_c2"]["start"]; ty = TT("c2", "year,", 0.3); tf = TT("c2", "family", 0.3)
    mtext(c, "7%", 150, 880, 64, RD, pr(t, t0 + 0.1, 0.3), "pm")
    strip_m(c, 560, 820, 12, t, t0 + 0.1, fill_t=ty - 0.3, step=0.09, cell=58, col=OR, label="12 MONTHS")
    if t > tf - 0.5:
        for i, (x, sc, kind) in enumerate(((240, 0.8, "h"), (400, 0.8, "g"), (550, 0.55, "k"), (670, 0.5, "k2"))):
            tk = tf - 0.5 + i * 0.12
            if t < tk: continue
            kk = pop_(t, tk)
            if kind == "h": hero(c, x, FLOOR, sc * kk, POSES["hold"], Face("open", "smile"), t)
            elif kind == "g": girl(c, x, FLOOR, sc * kk, POSES["wave"], Face("open", "smile"), t, dress=PINK)
            elif kind == "k": extra(c, x, FLOOR, sc * kk, POSES["jump"], Face("open", "smile"), t, scarf=GR)
            else: girl(c, x, FLOOR, sc * kk, POSES["stand"], Face("open", "smile"), t, dress=OR)
        cart_m(c, 830, 1420, t, tf - 0.2, 0.42, 1.0, GR)
    say(c, t, t0 + 0.08, "over a whole year", "FAMILY OF 4", MK, under=OR)
    note(c, t, t0 + 0.6, "INSTACART'S OWN FAMILY-OF-FOUR GROCERY FIGURE: $17,424 A YEAR")


def S_c3(c, t):
    t0 = SHOT["S_c3"]["start"]; tt_ = TT("c3", "twelve", 0.3); te = TT("c3", "estimate,", 0.3)
    coinpile_m(c, 520, 1330, t, t0 + 0.1)
    if t > tt_ - 0.2: mtext(c, "≈ $1,200 / YEAR", 510, 1000, 88, GR, pr(t, tt_ - 0.2, 0.5), "pm", pen_=True)
    if t > te - 0.3:
        mtext(c, "ESTIMATE", 510, 1135, 60, RD, pr(t, te - 0.3, 0.3), "pm")
        boxed(c, 510, 1114, 320, 84, pr(t, te - 0.1, 0.4), RD)
    say(c, t, t0 + 0.08, "about", "$1,200 A YEAR", GR, under=GR)
    note(c, t, t0 + 0.6, "THE REPORT'S ESTIMATE (~7% × $17,424), NOT A MEASURED BILL")


def S_c4(c, t):
    t0 = SHOT["S_c4"]["start"]; to = TT("c4", "own", 0.3)
    hero(c, 240, FLOOR, 1.05, POSES["hold"] if t < to else POSES["shrug"], Face("open", "flat" if t < to else "smile", look=(1, 0)), t)
    eggphone(c, 520, 1080, t, t0 + 0.05, "$4.59", BLU, 0.75)
    for i, x in enumerate((760, 830, 900)):
        if t > t0 + 0.4 + i * 0.1:
            r_ = [(x - 30, 900), (x + 30, 900), (x + 30, 1010), (x - 30, 1010), (x - 30, 900)]
            hatch(c, _path(r_), pr(t, t0 + 0.4 + i * 0.1, 0.4), LIGHT, gap=12, w=5, bbox=(x - 32, 898, x + 32, 1012), a=0.7)
            mtext(c, "?", x, 1070, 48, LIGHT, pr(t, t0 + 0.5 + i * 0.1, 0.2), "pm")
    say(c, t, t0 + 0.08, "honestly? I'd never spot it", "YOUR PRICE ONLY", BLU, under=BLU, size=140)


def S_d1(c, t):
    t0 = SHOT["S_d1"]["start"]; tt_ = TT("d1", "Thirteen", 0.3); te = TT("d1", "ended", 0.3)
    calendar(c, 230, 900, 0.95, "DEC 2025", "9", pop_(t, t0 + 0.05))
    mtext(c, "REPORT", 230, 1050, 44, MK, pr(t, t0 + 0.3, 0.3), "pm")
    strip_m(c, 510, 1180, 13, t, t0 + 0.2, fill_t=tt_ - 0.2, step=0.07, cell=58, col=OR, label="13 DAYS")
    if t > te - 0.6: calendar(c, 800, 900, 0.95, "DEC 2025", "22", pop_(t, te - 0.6))
    if t > te - 0.15: stamp_m(c, 520, 1390, "TESTS ENDED", pr(t, te - 0.15, 0.22), col=RD, tilt=-6, size=64)
    say(c, t, t0 + 0.08, "13 days after the report", "TESTS ENDED", RD, under=RD, size=150)
    note(c, t, t0 + 0.6, "INSTACART, \"ENDING ITEM PRICE TESTS ON INSTACART\", 22 DEC 2025")


def S_d2(c, t):
    t0 = SHOT["S_d2"]["start"]; tm = TT("d2", "Same", 0.2); tp = TT("d2", "Period.", 0.3)
    carton_m(c, 520, 1300, t, t0 - 3, 1.0, 0.0)
    u = eio(pr(t, tm, max(0.6, tp - tm - 0.4)))
    for i, (x, y, tl) in enumerate(TAGPOS):
        if i != 2 and u >= 1: continue
        xx = x + (520 - x) * u; yy = y + (900 - y) * u
        tag_m(c, xx, yy, "SAME" if u >= 1 else PRICES[i], t, t0 - 3, (GR if u >= 1 else (BLU if i < 4 else RD)), tl * (1 - u), 0.78 if u < 1 else 1.0)
    if t > tp - 0.1: mtext(c, "PERIOD.", 520, 1100, 78, MK, pr(t, tp - 0.1, 0.3), "pm", pen_=True)
    say(c, t, t0 + 0.08, "same items, same time, same store", "ONE PRICE", GR, under=GR)
    note(c, t, t0 + 0.6, "INSTACART, 22 DEC 2025: \"THEY SEE THE SAME PRICES — PERIOD\"")


def S_d3(c, t):
    t0 = SHOT["S_d3"]["start"]; tc = TT("d3", "coverage", 0.3)
    newspaper_m(c, 300, 1050, t, t0 + 0.05, "EGG PRICES", -6)
    shopfront_m(c, 740, 1400, t, t0 + 0.2, 0.75, "INSTACART", BLU)
    if t > tc - 0.2: speech(c, 700, 880, 440, 130, "GOT IT WRONG", pop_(t, tc - 0.2), 54, RD, tail=1)
    say(c, t, t0 + 0.08, "it also said the coverage", "GOT IT WRONG", RD, under=RD, size=150)
    note(c, t, t0 + 0.6, "INSTACART: \"MISCONCEPTIONS AND MISINFORMATION\" IN THE COVERAGE")


def S_e1(c, t):
    t0 = SHOT["S_e1"]["start"]; t2 = L0("e2"); tm = TT("e1", "middlemen.", 0.3)
    tl = TT("e2", "location,", 0.3); tb = TT("e2", "browsing,", 0.3); tmo = TT("e2", "mouse", 0.3)
    if t < t2 - 0.15:
        a_ = max(0.0, 1 - pr(t, t0 + 0.2, 0.5))
        if a_ > 0: mtext(c, "INSTACART", 520, 860, 60, LIGHT, 1, "pm", a=a_)
        gov_m(c, 300, 1400, t, t0 + 0.6, "FTC", "CONSUMER WATCHDOG", 0.7)
        if t > tm - 0.6:
            boxed(c, 730, 1160, 420, 170, pr(t, tm - 0.6, 0.4), PU)
            mtext(c, "PRICING", 730, 1140, 46, PU, pr(t, tm - 0.4, 0.3), "pm"); mtext(c, "MIDDLEMEN", 730, 1200, 46, PU, pr(t, tm - 0.3, 0.3), "pm")
    else:
        eggphone(c, 560, 1100, t, t2 - 0.1, None, s=0.8)
        pin_m(c, 200, 1000, t, tl - 0.2, 0.9)
        if t > tb - 0.3: browser_m(c, 270, 1290, t, tb - 0.3, url="shop", title="", w=360, h=220)
        if t > tmo - 0.3: cursor_m(c, 780, 1180, t, tmo - 0.3, 1.0)
    say(c, t, t0 + 0.08, "separately, America's consumer watchdog", "STUDIED MIDDLEMEN", PU, t1=t2 - 0.3, under=PU, size=130)
    say(c, t, t2 - 0.25, "it says they can use", "EVEN YOUR MOUSE", RD, under=RD, size=150)
    note(c, t, t0 + 0.6, "FTC SURVEILLANCE PRICING STUDY, 17 JAN 2025 · NOT ABOUT INSTACART'S TESTS")


def S_e3(c, t):
    t0 = SHOT["S_e3"]["start"]; th = TT("e3", "hypothetical.", 0.3)
    eggphone(c, 300, 1100, t, t0 - 3, None, s=0.8)
    sticky_m(c, 710, 960, t, t0 + 0.2, "EXAMPLE", 0.9, 8, MK)
    if t > th - 0.2: mtext(c, "HYPOTHETICAL", 690, 1190, 50, RD, pr(t, th - 0.2, 0.4), "pm", pen_=True)
    say(c, t, t0 + 0.08, "its who-pays-more examples were", "HYPOTHETICAL", RD, under=RD, size=150)
    note(c, t, t0 + 0.6, "FTC: \"ONLY INCLUDES HYPOTHETICAL EXAMPLES\" (17 JAN 2025)")


def S_e4(c, t):
    t0 = SHOT["S_e4"]["start"]; ts = TT("e4", "say", 0.3)
    ny_m(c, 300, 920, t, t0 + 0.05)
    tag_m(c, 690, 1000, "$4.79", t, t0 + 0.4, RD, -6, 0.9)
    if t > ts - 1.2:
        k = pr(t, ts - 1.2, 0.4)
        c.drawRoundRect(R.MakeXYWH(110, 1160, 800, 150), 18, 18, paint(WHITE, k)); c.drawRoundRect(R.MakeXYWH(110, 1160, 800, 150), 18, 18, stroke(RD, 5, k))
        mtext(c, "THIS PRICE WAS SET BY AN ALGORITHM", 510, 1220, 38, MK, pr(t, ts - 1.0, 0.5), "kb")
        mtext(c, "USING YOUR PERSONAL DATA", 510, 1275, 38, MK, pr(t, ts - 0.7, 0.5), "kb")
        if t > ts: ink(c, [wob([(300, 1288), (720, 1284)], 77, 1.0)], pr(t, ts, 0.3), RD, 8, pen_=False)
    say(c, t, t0 + 0.08, "in New York the seller must", "SAY SO", RD, under=RD)
    note(c, t, t0 + 0.6, "NY GEN. BUSINESS LAW § 349-a · ENFORCED SINCE NOV 2025 · UP TO $1,000 PER VIOLATION")


def S_t1(c, t):
    t0 = SHOT["S_t1"]["start"]; tc = TT("t1", "Compare", 0.3); t2 = L0("t2"); tp = TT("t2", "phones.", 0.3)
    hero(c, 130, FLOOR, 0.8, POSES["hold"], Face("open", "smile", look=(1, 0)), t)
    girl(c, 900, FLOOR, 0.8, POSES["hold"], Face("open", "smile", look=(-1, 0)), t, flip=True, dress=PINK)
    eggphone(c, 340, 1060, t, t0 + 0.1, "$4.28", BLU, 0.62)
    eggphone(c, 690, 1060, t, t0 + 0.35, "$4.69", RD, 0.62)
    if t > tc - 0.2:
        arrow_m(c, (450, 830), (580, 830), pr(t, tc - 0.2, 0.3), MK, 8); arrow_m(c, (580, 830), (450, 830), pr(t, tc, 0.3), MK, 8)
        mtext(c, "COMPARE", 515, 790, 52, OR, pr(t, tc, 0.3), "pm")
    if t > tp - 0.2:
        for x in (340, 690): ink(c, [[(x - 40, 1260), (x - 10, 1290), (x + 50, 1220)]], pr(t, tp - 0.2, 0.3), GR, 10, pen_=False)
    say(c, t, t0 + 0.08, "the attorney general's tip", "COMPARE", OR, t1=t2 - 0.3, under=OR)
    say(c, t, t2 - 0.25, "same store, same item", "TWO PHONES", OR, under=OR)
    note(c, t, t0 + 0.6, "ADVICE: NEW YORK ATTORNEY GENERAL (NOV 2025)")


def S_end(c, t):
    t0 = SHOT["S_end"]["start"]; tz2 = L0("z2"); tfa = TT("z1", "fair,", 0.4); tcr = TT("z1", "creepy?", 0.4)
    c.save(); c.translate(0, 8 * math.sin(t * 2.4)); c.rotate(1.2 * math.sin(t * 1.7))
    carton_m(c, 520, 1060, t, t0 - 3, 0.8, 0.0)
    tag_m(c, 680, 920, "$?", t, t0 - 3, RD, 8, 0.6)
    c.restore()
    tagpill_m(c, 290, 1330, "FAIR", pop_(t, tfa - 0.2), GR, 60)
    tagpill_m(c, 730, 1330, "CREEPY", pop_(t, tcr - 0.2), PU, 60)
    for i, (x, tm) in enumerate(((290, tfa), (730, tcr))):
        if t > tm: ink(c, [wob(circ_pts(x, 1320, 170, -150, 215, 40, ry=80), 95 + i, 1.4)], pr(t, tm, 0.35), RD, 7, pen_=False)
    say(c, t, t0 + 0.08, "testing prices on shoppers?", "FAIR OR CREEPY?", MK, t1=tz2 - 0.3, under=BLU, size=150)
    say(c, t, tz2 - 0.25, "send it to whoever does the weekly shop", "SAVE THIS", BLU, under=OR)
    note(c, t, t0 + 0.6, "COMMENT ONE WORD · EDUCATION ONLY")


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}
SURF = surface()
IMPACTS = [(TT("i1", "five", 0.6), 0.14, 4), (TT("d1", "ended", 0.3) - 0.15, 0.14, 5), (TT("a4", "twenty-three", 0.3), 0.12, 4)]
# the QUESTION MAP (story upgrade, 10 Nov): the hook's two questions under the pill, answered in order
_MAP = {"S_i4": (-1, ()), "S_a1": (0, ()), "S_a3": (0, ()), "S_a4": (0, ()), "S_a5": (0, ()), "S_b1": (0, ()), "S_b3": (0, ()),
        "S_c2": (0, ()), "S_c3": (0, ()), "S_c4": (0, ()), "S_d1": (1, (0,)), "S_d2": (1, (0,)), "S_d3": (1, (0,)),
        "S_e1": (-1, (0, 1)), "S_e3": (-1, (0, 1)), "S_e4": (-1, (0, 1)), "S_t1": (-1, (0, 1))}
_TOP = {"S_a1": "THE TEST", "S_a3": "THE TEST", "S_a4": "THE TEST", "S_a5": "THE TEST", "S_b1": "INSTACART'S SIDE", "S_b3": "INSTACART'S SIDE",
        "S_c2": "A WHOLE YEAR", "S_c3": "A WHOLE YEAR", "S_d1": "STILL HAPPENING?", "S_d2": "STILL HAPPENING?", "S_d3": "STILL HAPPENING?",
        "S_e1": "THE BIGGER PICTURE", "S_e3": "THE BIGGER PICTURE", "S_e4": "THE BIGGER PICTURE", "S_t1": "WHAT YOU CAN DO"}


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
    if sid in _MAP: qmap(c, _MAP[sid][0], _MAP[sid][1], min(1, pr(tt, s["start"], 0.3)))
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
