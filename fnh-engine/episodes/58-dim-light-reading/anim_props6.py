# ================= anim_props6.py = lib58 (ep 58, 21 Nov): "Does reading in dim light ruin your eyes?" — ACCENT = SUNSHINE YELLOW
# (the sun, the daylight, the hook question, the focus effort). Everything else stays paper / ink / mint / skin; the candle is its own warm orange.
# NEW CRAFT (ep 58) = FLAME + SMOKE EFFECTS ANIMATION (2D effects animation of fire): candle_flame(...) is drawn ON TWOS (12 drawings a second), its
# BASE (the ball round the wick) never moves (it only swells and shrinks a little, like a soap bubble), the body rises in S-curves that morph into
# C-curves and back, the TIP points the opposite way from the previous drawing, a tongue BREAKS OFF near the top every cycle and rises, shrinks and
# pops; the cycle timing is irregular (no metronome); colour layers = a yellow inner flame inside an orange outer shape with a warm outline, a small
# blue root at the wick. The flame drives its own LIGHT: flick(t) (on twos, irregular) sets the glow on the room and on Chubby's face, so the light
# shivers WITH the flame. smoke_wisp(...) = after a blow-out: a thin ribbon that rises, curls wider and slower as it climbs, breaks into separate wisps
# and fades. (Sources in improvements.md G: Clip Studio 'How to animate flames' (ascent, swelling, division, reduction; LINE / CENTER / BASE / GLOW
# layers, an environment light layer); Flash FX '#12 Fire' (the core 'doesn't really move', 'decide on a point that it can break off', S to C curves,
# yellow interior / orange outer); Wacom 'Easy flame animation' (longer and shorter parts, keep the bottom the same).)
# NEW PLACE: set_park(t) = a sunny NOON PARK (bright sky + one big sun, round ink trees, a swing frame + slide, a path, grass) + park_front(f) (hedge).
# set_powercut(t, fl) = the study desk (lib57) in a POWER CUT: lamp and laptop off, only the candle's flickering pool.
# Board: eye_board(...) = a side-view eyeball (cornea, iris + pupil, lens with its focusing ring muscle, retina) whose lens squeezes + sweats, whose
# pupil widens in dim light, and which can GROW TOO LONG (light focuses in front of the retina = nearsighted).
# Props: candle_el, book_el, curtain_window(...), eye_chart_el, mom58(...), kid58(...). =================
ACC = (250, 196, 40); ACC_S = (178, 118, 0); ACC_L = (254, 226, 140); ACC_XL = (254, 242, 204)      # sunshine yellow
FL_OUT = (255, 146, 40); FL_IN = (255, 228, 120); FL_LINE = (214, 96, 24); FL_ROOT = (110, 150, 255)
WAX = (250, 244, 226); WAX_S = (220, 208, 182); BRASS = (214, 168, 74); BRASS_S = (164, 118, 40)
SKY = (150, 206, 244); GRASS = (124, 186, 96); GRASS_S = (84, 146, 70)
RED = (176, 40, 44); OKG = (40, 140, 80)
COAT = (246, 248, 250)
MOM_TOP = (196, 70, 110); MOM_HAIR2 = (58, 38, 32)
SRC_HOP = "Source: Johns Hopkins Medicine (2026); Univ. of Utah Health"
SRC_STRAIN = "Source: Johns Hopkins Medicine; Cleveland Clinic eye institute (WebMD)"
SRC_OUT = "Source: American Academy of Ophthalmology; US National Academies (2024)"
SRC_LONG = "Source: American Academy of Ophthalmology"
SRC_CHECK = "Source: Johns Hopkins Medicine; American Academy of Ophthalmology"
SC3 = 3
from gfx import text_el


# ---------------- FLAME + SMOKE (ep 58 craft) ----------------
def _twos(t): return math.floor(t * 12 + 1e-6) / 12.0                     # on twos: 12 drawings a second at 24 fps


def flick(t, seed=0):
    """the flame's light level (about 0.78..1.12), on twos, irregular: three detuned waves + a rare dip (a draught)."""
    u = _twos(t) + seed * 0.37
    v = 0.95 + 0.07 * math.sin(u * 7.3) + 0.05 * math.sin(u * 12.9 + 1.1) + 0.03 * math.sin(u * 23.7 + 2.3)
    dip = max(0.0, math.sin(u * 0.9 + seed) - 0.93) * 2.2                      # now and then the flame ducks
    return v - dip


def candle_flame(f, x, y, t, s=1.0, on=1.0, gust=0.0, seed=0, light=True):
    """a hand-drawn candle flame standing on the wick top (x, y). on 0..1 = size (0 = out), gust = lean to the right (+) / left (-) in px at s 1.
    Returns the light level for the room (flick * on)."""
    if on <= 0.02: return 0.0
    u = _twos(t); ph = u * 1.15 + 0.18 * math.sin(u * 2.3 + seed) + seed * 0.21          # irregular cycle (~0.9 s, never metronomic)
    cyc = ph % 1.0; side = 1 if int(ph * 6) % 2 == 0 else -1                             # the tip flips side from drawing to drawing
    hgt = (118 + 16 * math.sin(2 * math.pi * cyc * 2 + 1.0) + 8 * math.sin(u * 5.1)) * s * on
    rb = 24 * s * on * (1 + 0.06 * math.sin(2 * math.pi * cyc + 0.5))                    # the base ball: swells / shrinks, never moves
    tipx = x + (gust * s + side * (7 + 5 * math.sin(u * 3.7)) * s) * on
    midx = x - side * 4 * s * on + 0.4 * gust * s * on                                      # S-curve: the middle bends the other way
    def body(scale):
        pts = []
        n = 14
        for i in range(n + 1):                                                            # right edge from the base up to the tip
            a = i / n; yy = y - a * hgt * scale
            w = rb * scale * (math.sin(math.pi * (0.5 + 0.5 * a)) ** 0.8) * (1.0 - 0.15 * a) + 0.5
            cx = x + (midx - x) * math.sin(math.pi * a) + (tipx - x) * a ** 2
            pts.append((cx + w, yy))
        for i in range(n, -1, -1):
            a = i / n; yy = y - a * hgt * scale
            w = rb * scale * (math.sin(math.pi * (0.5 + 0.5 * a)) ** 0.8) * (1.0 - 0.15 * a) + 0.5
            cx = x + (midx - x) * math.sin(math.pi * a) + (tipx - x) * a ** 2
            pts.append((cx - w, yy))
        for k in range(10):                                                               # the round bottom of the base
            a = math.pi * k / 9; pts.append((x - rb * scale * math.cos(a), y + rb * scale * 0.85 * math.sin(a)))
        return np.int32([(px * 4, py * 4) for px, py in pts])
    lv = flick(t, seed) * on
    if light:
        glow(f, x, y - hgt * 0.4, 150 * s, (255, 190, 110), 0.22 * lv)
    cv2.fillPoly(f, [body(1.0)], C(FL_LINE), cv2.LINE_AA, shift=2)                          # warm outline (drawn as a slightly bigger shape)
    cv2.fillPoly(f, [body(0.9)], C(FL_OUT), cv2.LINE_AA, shift=2)
    cv2.fillPoly(f, [body(0.55)], C(FL_IN), cv2.LINE_AA, shift=2)
    cv2.ellipse(f, (int(x), int(y + 2 * s)), (max(1, int(5 * s * on)), max(1, int(7 * s * on))), 0, 0, 360, C(FL_ROOT), -1, cv2.LINE_AA)
    # the break-off tongue: leaves the tip at cyc ~0.55, rises, shrinks, pops by cyc ~0.95
    if 0.55 < cyc < 0.95:
        k = (cyc - 0.55) / 0.40
        bx = tipx + side * 6 * s * k; by = y - hgt - (10 + 70 * k) * s
        r = max(1, int(9 * s * on * (1 - k)))
        cv2.ellipse(f, (int(bx), int(by)), (r + 2, int(r * 1.6) + 2), 0, 0, 360, C(FL_LINE), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(bx), int(by)), (r, int(r * 1.6)), 0, 0, 360, C(FL_OUT), -1, cv2.LINE_AA)
    cv2.line(f, (int(x), int(y + 14 * s)), (int(x + 2 * s), int(y - 6 * s)), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)   # the wick
    return lv


def smoke_wisp(f, x, y, t, t0, dur=2.6, s=1.0, seed=0, col=(196, 196, 204)):
    """smoke after a blow-out at t0: a thin ribbon rises from (x, y), curls WIDER and SLOWER as it climbs, breaks into separate wisps, fades."""
    a = t - t0
    if a <= 0 or a > dur: return
    fade = 1 - a / dur
    lay = f.copy()
    top = min(1.0, a / 0.9)                                                               # how far up the ribbon has reached
    n = 40; pts = []
    for i in range(n + 1):
        v = i / n * top
        hy = y - v * 520 * s
        amp = (6 + 70 * v * v) * s                                                         # curls widen as they climb
        wav = math.sin(v * 9.0 - a * (3.2 - 1.6 * v) + seed)                               # and slow down near the top
        pts.append((x + amp * wav + 30 * s * v * math.sin(a * 0.8 + seed), hy))
    for i in range(n):
        v = i / n * top
        gap = math.sin(v * 22 + a * 2.0 + seed * 3) > 0.55 and v > 0.35                     # break-up into separate wisps higher up
        if gap: continue
        w = max(1, int((3 + 9 * v) * s))
        cv2.line(lay, (int(pts[i][0]), int(pts[i][1])), (int(pts[i + 1][0]), int(pts[i + 1][1])), C(col), w, cv2.LINE_AA)
    al = 0.75 * fade
    f[:] = f * (1 - al) + lay * al


def candle_el(melt=0.0):
    """a white candle in a small brass holder (ink). The wick top is at (0, -WICK_DY * s) from the element centre."""
    melt = round(clamp(melt) * 4) / 4
    def mk():
        w, h = 200, 360; im, d, S = _cv(w, h)
        top = 70 + 60 * melt
        _ink_poly(d, [(70, top), (130, top), (132, 300), (68, 300)], WAX, 581, INK_W - 1, amp=1.2)
        _shade(im, lambda q, S_: q.polygon(S_(70, top, 130, top, 132, 300, 68, 300), fill=255),
               lambda q, S_, c: q.rectangle(S_(108, top, 140, 300), fill=c), WAX_S, 150)
        d.polygon(S(72, top, 88, top, 86, top + 40, 80, top + 52, 76, top + 30), fill=(255, 255, 255, 255))      # a wax drip
        _ink_poly(d, [(86, top + 4), (92, top + 46), (98, top + 4)], WAX, 582, 3, amp=0.8)
        _ink_ell(d, 100, 306, 86, 22, BRASS, 583, INK_W - 1)                                                       # the holder dish
        _ink_poly(d, [(60, 300), (140, 300), (150, 320), (50, 320)], BRASS, 584, INK_W - 1, amp=1.0)
        _ink_ell(d, 170, 312, 22, 16, None, 585, INK_W - 2)                                                        # finger ring
        return _done(im, w, h)
    return gcache(("candle58", melt), mk)


WICK_DY = 110      # px above the candle element's centre at s 1 (top 70 -> centre 180)


def book_el(open_=1.0):
    """an open book (ink) with lines of tiny text; open_ < 1 = half closed."""
    def mk():
        w, h = 420, 260; im, d, S = _cv(w, h)
        _ink_poly(d, [(14, 70), (206, 40), (206, 232), (14, 250)], (252, 248, 236), 586, INK_W - 1, amp=1.0)
        _ink_poly(d, [(206, 40), (406, 70), (406, 250), (206, 232)], (252, 248, 236), 587, INK_W - 1, amp=1.0)
        for j in range(7):
            yy = 86 + 20 * j
            d.line(S(36, yy + 4 - j * 0.6, 186, yy - 12 - j * 0.6), fill=INKC + (120,), width=4 * SC3)
            d.line(S(226, yy - 12, 384, yy + 4), fill=INKC + (120,), width=4 * SC3)
        _ink_poly(d, [(14, 250), (206, 232), (406, 250), (406, 258), (206, 242), (14, 258)], ACC_S, 588, 3, amp=0.6)
        return _done(im, w, h)
    return gcache(("book58", open_), mk)


def eye_chart_el():
    """a doctor's eye chart (rows of letters, big to small) on a white card."""
    def mk():
        w, h = 360, 520; im, d, S = _cv(w, h)
        _ink_poly(d, [(20, 20), (340, 20), (340, 500), (20, 500)], (254, 254, 250), 589, INK_W - 1, amp=1.0)
        rows = [("E", 120), ("F P", 70), ("T O Z", 50), ("L P E D", 36), ("P E C F D", 26), ("E D F C Z P", 20)]
        yy = 40
        for txt, sz in rows:
            fnt = font(F_BLACK, sz * SC3)
            tw = d.textlength(txt, font=fnt)
            d.text((180 * SC3 - tw / 2, yy * SC3), txt, font=fnt, fill=INKC + (255,))
            yy += sz + 26
        return _done(im, w, h)
    return gcache(("chart58",), mk)


def curtain_window(f, x0, y0, x1, y1, open_k=0.0, t=0.0, sun=1.0, dark=0.0):
    """a window to a sunny day with two ink curtains; open_k 0 = shut (the sun is only a line of light at the gap), 1 = pulled wide open.
    Returns the centre of the glass."""
    cx = (x0 + x1) / 2; cy = (y0 + y1) / 2
    sky = _vgrad((140, 200, 246), (214, 236, 250), y0, y1)
    f[y0:y1, x0:x1] = sky[y0:y1, x0:x1] * (1 - 0.6 * dark)
    if sun > 0:
        glow(f, x1 - 110, y0 + 120, 160, (255, 236, 150), 0.6 * sun * (1 - dark))
        cv2.circle(f, (int(x1 - 110), int(y0 + 120)), 58, C(ACC), -1, cv2.LINE_AA); cv2.circle(f, (int(x1 - 110), int(y0 + 120)), 58, C(INKC), 5, cv2.LINE_AA)
        cv2.ellipse(f, (int(x0 + 120), int(y1 - 80)), (130, 60), 0, 0, 360, C(GRASS), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y1), C((120, 86, 60)), 14, cv2.LINE_AA); cv2.line(f, (int(cx), y0), (int(cx), y1), C((120, 86, 60)), 8)
    cw = (x1 - x0) / 2 * (1 - 0.82 * open_k) + 20
    for sg, xa in ((1, x0 - 30), (-1, x1 + 30)):                                       # each curtain hangs from the rail and bunches up as it opens
        xb = xa + sg * cw
        pts = [(xa, y0 - 40)]
        for i in range(13):
            yy = y0 - 40 + i * (y1 - y0 + 90) / 12
            pts.append((xb + sg * 10 * math.sin(i * 1.7 + t * 1.5) * (0.4 + open_k), yy))
        pts.append((xa, y1 + 50))
        P = np.int32(pts)
        cv2.fillPoly(f, [P], C(_mix((214, 120, 90), (60, 40, 50), dark)), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), 6, cv2.LINE_AA)
        for j in range(1, 4):                                                          # folds
            fx = xa + sg * cw * j / 4
            cv2.line(f, (int(fx), y0 - 30), (int(fx + sg * 6), y1 + 40), C(_mix((176, 90, 70), (40, 28, 36), dark)), 4, cv2.LINE_AA)
    cv2.line(f, (x0 - 60, y0 - 44), (x1 + 60, y0 - 44), C(INKC), 12, cv2.LINE_AA)
    return cx, cy


def _mix(a, b, k): return tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(3))


# ---------------- the EYE on the board ----------------
def eye_board(f, cx, cy, t, k=1.0, R=230, pupil=0.4, squeeze=0.0, length=0.0, sweat=0.0, rays=0.0, light_amt=1.0, seed=590, labels=None):
    """a side-view eyeball on the blue-ink board, the cornea facing LEFT (light comes from the left). k = draw-on 0..1.
    pupil 0..1 = how wide the opening is; squeeze 0..1 = the focusing ring muscle working (lens fattens, ring hatched in the accent, sweat drops);
    length 0..1 = the eyeball grows too long from front to back (the back moves right); rays 0..1 = light rays draw in and meet at a focus point
    (on the retina when length 0, in front of it when long). Returns dict(focus=(x, y), retina_x=...)."""
    L = R * (1 + 0.36 * length)
    ex = cx + (L - R) * 0.5                                                             # keep the whole eye centred while it grows
    pts = []
    for i in range(49):
        a = math.radians(-160 + 320 * i / 48)
        pts.append((ex + L * math.cos(a) * (1.0 if math.cos(a) > 0 else R / L) - (L - R) * 0.0, cy + R * 0.92 * math.sin(a)))
    pts = [(p[0] - (L - R) * 0.5 * (1 if p[0] < ex else 0), p[1]) for p in pts]
    draw_on(f, pts, k, BP_INK, 8, seed=seed, tip=k < 1)
    fx0 = ex - R                                                                         # front of the eye (cornea side)
    corn = [(fx0 + 10, cy - R * 0.36), (fx0 - 34, cy - R * 0.18), (fx0 - 44, cy), (fx0 - 34, cy + R * 0.18), (fx0 + 10, cy + R * 0.36)]
    draw_on(f, corn, clamp(k * 1.4 - 0.2), BP_INK, 7, seed=seed + 1, tip=False)
    ir = R * 0.34 * (1 - 0.75 * pupil) + 10                                              # iris flaps: the gap between them = the pupil
    lx = fx0 + 46
    if k > 0.5:
        for sg in (-1, 1):
            cv2.line(f, (int(lx), int(cy + sg * R * 0.36)), (int(lx), int(cy + sg * (R * 0.36 - ir))), C(BP_INK), 12, cv2.LINE_AA)
    lr = R * (0.13 + 0.07 * squeeze); lh = R * 0.27
    lcx = lx + 34 + lr
    if k > 0.6:
        cv2.ellipse(f, (int(lcx), int(cy)), (int(lr), int(lh)), 0, 0, 360, C((236, 244, 252)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(lcx), int(cy)), (int(lr), int(lh)), 0, 0, 360, C(BP_INK), 6, cv2.LINE_AA)
        for sg in (-1, 1):                                                                 # the focusing ring muscle (above + below the lens)
            my = cy + sg * (lh + 26)
            col = _mix(BP_INK, ACC_S, squeeze)
            rr = (int(30 - 6 * squeeze), int(20 + 6 * squeeze))
            cv2.ellipse(f, (int(lcx), int(my)), rr, 0, 0, 360, C(_mix((236, 244, 252), ACC, squeeze)), -1, cv2.LINE_AA)
            cv2.ellipse(f, (int(lcx), int(my)), rr, 0, 0, 360, C(col), 5, cv2.LINE_AA)
            if squeeze > 0.2:                                                              # effort lines
                for j in (-1, 1):
                    a0 = (lcx + j * 44, my + sg * 6); a1 = (lcx + j * 62, my + sg * 18)
                    cv2.line(f, (int(a0[0]), int(a0[1])), (int(a1[0]), int(a1[1])), C(ACC_S), 4, cv2.LINE_AA)
    bx = ex + L                                                                          # the back wall = the retina
    if k > 0.8:
        ret = [(bx - 40 - 0 * L, cy - R * 0.7)]
        for i in range(17):
            a = math.radians(-50 + 100 * i / 16)
            ret.append((ex + L * math.cos(a) - 10, cy + R * 0.92 * math.sin(a)))
        draw_on(f, ret[1:], clamp(k * 5 - 4), RED, 7, seed=seed + 3, tip=False)
    if sweat > 0:
        for j, (dx, dy) in enumerate(((-30, -lh - 80), (40, -lh - 70))):
            yy = cy + dy + 40 * ((t * 1.3 + j * 0.5) % 1.0) * sweat
            cv2.ellipse(f, (int(lcx + dx), int(yy)), (9, 14), 0, 0, 360, C((150, 200, 240)), -1, cv2.LINE_AA)
            cv2.ellipse(f, (int(lcx + dx), int(yy)), (9, 14), 0, 0, 360, C(BP_INK), 3, cv2.LINE_AA)
    focus_x = bx - 12 - L * 0.55 * length * 0.62                                           # long eye: the image lands IN FRONT of the retina
    if rays > 0:
        for sg in (-1, 0, 1):
            p0 = (fx0 - 260, cy + sg * R * 0.24); p1 = (lcx, cy + sg * R * 0.2)
            kr = clamp(rays * 2)
            draw_on(f, [p0, p1], kr, _mix(ACC_S, (120, 120, 130), 1 - light_amt), 6, seed=seed + 10 + sg, tip=False)
            if rays > 0.5:
                draw_on(f, [p1, (focus_x, cy)], clamp(rays * 2 - 1), _mix(ACC_S, (120, 120, 130), 1 - light_amt), 6, seed=seed + 20 + sg, tip=False)
        if rays >= 1: cv2.circle(f, (int(focus_x), int(cy)), 13, C(ACC_S if length < 0.3 else RED), -1, cv2.LINE_AA)
    return dict(focus=(focus_x, cy), retina_x=bx, lens=(lcx, cy), front=fx0)


# ---------------- people ----------------
def mom58(f, x, y, s, t, la=(24, 12), ra=(24, 12), hand_l="open", hand_r="open", mouth=0, expr="n", brow="n", look=(0, 0), turn=0.0, lean=0.0):
    """MOM: long dark hair behind the head (drawn first), a rose kurta (shirt=), a bun, a mint dupatta over one shoulder, small bindi."""
    hx, hy = x + lean * 2 * s + turn * 14 * s, y - 420 * s
    P = np.array([(hx - 120 * s, hy - 30 * s), (hx + 120 * s, hy - 30 * s), (hx + 112 * s, hy + 150 * s), (hx - 112 * s, hy + 150 * s)], np.int32)
    cv2.fillPoly(f, [P], C(MOM_HAIR2), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    hands = chub(f, x, y, s, t=t, shirt=MOM_TOP, la=la, ra=ra, hand_l=hand_l, hand_r=hand_r, mouth=mouth, expr=expr, brow=brow, look=look, turn=turn, lean=lean)
    cv2.ellipse(f, (int(hx), int(hy - 64 * s)), (int(98 * s), int(50 * s)), 0, 180, 360, C(MOM_HAIR2), int(20 * s), cv2.LINE_AA)
    cv2.circle(f, (int(hx + 6 * s), int(hy - 116 * s)), int(36 * s), C(INKC), -1, cv2.LINE_AA)
    cv2.circle(f, (int(hx + 6 * s), int(hy - 116 * s)), int(28 * s), C(MOM_HAIR2), -1, cv2.LINE_AA)
    cv2.circle(f, (int(hx + turn * 10 * s), int(hy - 40 * s)), max(2, int(7 * s)), C((200, 40, 60)), -1, cv2.LINE_AA)
    D = np.array([(hx - 110 * s, y - 330 * s), (hx - 50 * s, y - 330 * s), (hx + 80 * s, y - 130 * s), (hx + 26 * s, y - 112 * s)], np.int32)
    cv2.fillPoly(f, [D], C(INK_MINT), cv2.LINE_AA); cv2.polylines(f, [D], True, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    return hands


def kid58(f, x, y, s, t, shirt=(240, 150, 60), cap=True, **kw):
    """another kid in the park: chub with a different shirt + a cap (dress 'cousin')."""
    h = chub(f, x, y, s, t=t, shirt=shirt, **kw)
    if cap: dress(f, x, y, s, "cousin", kw.get("lean", 0.0))
    return h


# ---------------- NEW PLACE: the sunny NOON PARK ----------------
PARK_GROUND = 1330


def set_park(t=0.0, blur=4, ground_y=PARK_GROUND, sun_amt=1.0):
    """a bright NOON PARK: blue sky softened toward paper, one big ink sun high on the right, puffy clouds, a far row of houses, round ink trees,
    a swing frame + a slide, a path; the grass starts at ground_y. Sun rays + floating dust (pollen) move."""
    def mk():
        f = _vgrad((128, 192, 240), (214, 236, 246), 0, ground_y)
        for cx_, cy_, sc in ((230, 520, 1.0), (760, 640, 0.8), (520, 380, 0.6)):
            for dx, dy, r in ((0, 0, 60), (60, -20, 70), (130, 0, 56), (60, 20, 60)):
                cv2.circle(f, (int(cx_ + dx * sc), int(cy_ + dy * sc)), int(r * sc), C((252, 252, 250)), -1, cv2.LINE_AA)
        for j in range(9):                                                              # far houses
            bx = j * 130 - 20; bh = 120 + (j * 47) % 90
            cv2.rectangle(f, (bx, ground_y - 260 - bh), (bx + 110, ground_y - 200), C((176, 196, 214)), -1)
            for k in range(2): cv2.rectangle(f, (bx + 20 + 44 * k, ground_y - 230 - bh + 40), (bx + 44 + 44 * k, ground_y - 230 - bh + 70), C((226, 234, 240)), -1)
        f = _soft(f, blur + 2)
        cv2.rectangle(f, (0, ground_y - 210), (W, ground_y), C((150, 204, 120)), -1)       # far lawn
        for tx, ty, tr in ((90, ground_y - 330, 150), (330, ground_y - 300, 120), (990, ground_y - 340, 160)):
            cv2.rectangle(f, (tx - 18, ty), (tx + 18, ground_y - 160), C((120, 84, 56)), -1); cv2.rectangle(f, (tx - 18, ty), (tx + 18, ground_y - 160), C(INKC), 5)
            cv2.circle(f, (tx, ty - tr // 2), tr, C(GRASS), -1, cv2.LINE_AA); cv2.circle(f, (tx, ty - tr // 2), tr, C(INKC), 6, cv2.LINE_AA)
            cv2.ellipse(f, (tx + tr // 3, ty - tr // 3), (tr // 2, tr // 2), 0, -30, 120, C(GRASS_S), 10, cv2.LINE_AA)
        for sx in (560, 820):                                                           # swing frame A-legs
            cv2.line(f, (sx - 50, ground_y - 160), (sx, ground_y - 520), C((214, 90, 70)), 14, cv2.LINE_AA)
            cv2.line(f, (sx + 50, ground_y - 160), (sx, ground_y - 520), C((214, 90, 70)), 14, cv2.LINE_AA)
        cv2.line(f, (560, ground_y - 520), (820, ground_y - 520), C((214, 90, 70)), 14, cv2.LINE_AA)
        f = _soft(f, 1.5)
        f[ground_y - 160:] = _vgrad((140, 200, 108), (96, 160, 80), ground_y - 160, H)[ground_y - 160:]
        rng = np.random.default_rng(58)
        P = np.int32([(380, H), (700, H), (600, ground_y - 160), (520, ground_y - 160)])
        cv2.fillPoly(f, [P], C((236, 220, 186)), cv2.LINE_AA)                          # a sandy path
        for i in range(320):
            x = rng.uniform(0, W); y = rng.uniform(ground_y - 150, H); hgt = rng.uniform(8, 24)
            cv2.line(f, (int(x), int(y)), (int(x + rng.uniform(-5, 5)), int(y - hgt)), C(GRASS_S if i % 2 else (160, 214, 120)), 2, cv2.LINE_AA)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("park58", blur, ground_y), mk).copy()
    for k_, sx in enumerate((640, 740)):                                               # the two swings (live)
        a = 0.35 * math.sin(t * 2.2 + k_ * 1.6)
        px, py = sx, ground_y - 520
        bx_, by_ = px + 300 * math.sin(a), py + 300 * math.cos(a)
        cv2.line(f, (px, py), (int(bx_), int(by_)), C(INKC), 3, cv2.LINE_AA)
        cv2.rectangle(f, (int(bx_ - 26), int(by_)), (int(bx_ + 26), int(by_ + 10)), C((120, 84, 56)), -1)
    glow(f, 880, 760, 260, (255, 240, 170), 0.55 * sun_amt)
    cv2.circle(f, (880, 760), 70, C(ACC), -1, cv2.LINE_AA); cv2.circle(f, (880, 760), 70, C(INKC), 6, cv2.LINE_AA)
    for i in range(12):
        a = i * math.pi / 6 + t * 0.3
        cv2.line(f, (int(880 + 92 * math.cos(a)), int(760 + 92 * math.sin(a))), (int(880 + 124 * math.cos(a)), int(760 + 124 * math.sin(a))), C(INKC), 6, cv2.LINE_AA)
    god_rays(f, 880, 760, t, (255, 236, 170), 0.16 * sun_amt, 9, 1700, 1.6, 2.0, 3)
    dust_motes(f, t, 0, 600, W, ground_y, 16, 58, 0.5)
    return inkify(f)


def park_front(f, top_y=1600):
    """a low hedge across the bottom (drawn AFTER the kids) = depth."""
    rng = np.random.default_rng(581)
    for x in range(-40, W + 80, 70):
        r = int(rng.uniform(56, 80))
        cv2.circle(f, (x, top_y + 30), r, C(GRASS_S), -1, cv2.LINE_AA); cv2.circle(f, (x, top_y + 30), r, C(INKC), 5, cv2.LINE_AA)
    cv2.rectangle(f, (0, top_y + 40), (W, H), C(GRASS_S), -1)
    for x in range(-20, W + 60, 70):
        cv2.ellipse(f, (x + 18, top_y + 10), (22, 14), -30, 0, 360, C((150, 206, 110)), -1, cv2.LINE_AA)


# ---------------- the POWER CUT at the study desk ----------------
CANDLE = (300, DESK_TOP - 125)      # the candle element's centre on the desk (wick top = (300, DESK_TOP - 125 - WICK_DY * s))


def set_powercut(t=0.0, blur=5, lv=1.0, cx=None, cy=None):
    """lib57 set_desk with the power OUT: everything at ~32 %, a cool moonlight edge, and the candle's warm pool (lv = flick level)."""
    f = set_desk(t, blur, door=0.0)
    f = f * 0.30 + np.array(C((22, 24, 40)), np.float32) * 0.10
    x = CANDLE[0] if cx is None else cx; y = (CANDLE[1] - WICK_DY * 1.1 - 50) if cy is None else cy
    glow(f, x, y, 620, (255, 170, 90), 0.42 * lv)
    glow(f, x, y, 260, (255, 210, 140), 0.30 * lv)
    return f
