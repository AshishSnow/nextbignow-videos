# ================= anim_props6.py = lib38 (ep 38, 15 Nov): "Why does your mouth water when you just look at food?" — SAFFRON accent (food / sugar /
# the order), saliva = clear water-blue. METAPHOR: a restaurant KITCHEN inside you: the brain = head chef in a toque who gets the ORDER ticket, the spit
# glands = two taps, amylase = a little prep cook with scissors that snips starch chains into sugar pairs, the stomach = a stove that lights early.
# Chubby's MOUTH-WATERING acting kit (the ep 38 visual upgrade): mouth_xy, drool() (a saliva drip from the lip corner with anticipation + snap + gravity),
# lick() (a tongue tip that sweeps across the top lip), gulp() (a swallow: the throat bob + a squash), scent() (an aroma ribbon that travels from the food
# and HOOKS his nose, pulling him in nose-first). Ink props: jalebi_el, toque_el, ticket_el, scissors_el, amylase_el, roti_el, tray38_el. =================
ACC = (232, 128, 30); ACC_S = (176, 82, 14); ACC_L = (248, 196, 128); ACC_XL = (252, 232, 200)      # saffron = jalebi, sugar, the order
SPIT = (200, 228, 246); SPIT_S = (70, 130, 190); SPIT_H = (252, 254, 255)                           # saliva: clear water-blue
STARCH = (236, 222, 186); STARCH_S = (170, 146, 96)
ROTI = (232, 196, 132); ROTI_S = (182, 128, 66); ROTI_D = (140, 86, 40)
TONGUE = (222, 96, 112)
SRC_CC = "Source: Cleveland Clinic; StatPearls (NIH)"
SRC_SWEET = "Source: Chemical Senses 2019 (chewing starch -> maltose)"
SRC_ACID = "Source: Feldman & Richardson, Gastroenterology 1986"
SC3 = 3


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


# ---------------- props (ink language: one warm-ink wobbly outline, flat fill, shade + hatch on the shadow side) ----------------
def jalebi_el(seed=381, s_=1.0):
    """a jalebi: a saffron spiral of fried batter, glossy with syrup."""
    def mk():
        w, h = 260, 220; im, d, S = _cv(w, h)
        pts = []
        for i in range(140):
            a = i / 140 * 2 * math.pi * 3.2; r = 14 + 84 * i / 140
            pts.append((130 + r * math.cos(a) * 1.08, 110 + r * math.sin(a) * 0.86))
        P = _wob(pts, 1.2, seed)
        d.line([(x * SC3, y * SC3) for x, y in P], fill=INKC + (255,), width=30 * SC3, joint="curve")
        d.line([(x * SC3, y * SC3) for x, y in P], fill=ACC + (255,), width=20 * SC3, joint="curve")
        d.line([(x * SC3 - 4 * SC3, y * SC3 - 5 * SC3) for x, y in P[::3]], fill=ACC_L + (200,), width=5 * SC3, joint="curve")     # syrup shine
        for j in range(9):                                                         # crisp dark spots
            k = 15 + j * 14; x, y = P[k]; d.ellipse(S(x - 3, y + 2, x + 3, y + 7), fill=ACC_S + (230,))
        return _done(im, w, h)
    return gcache(("jalebi38", seed), mk)


def tray38_el(kind="steel", seed=382):
    """a steel shop tray (front view, the sweets are composited on top in the shot)."""
    def mk():
        w, h = 420, 220; im, d, S = _cv(w, h)
        _ink_poly(d, [(20, 150), (400, 150), (380, 200), (40, 200)], (210, 214, 218), seed, INK_W)
        _shade(im, lambda q, S_: q.polygon(_P([(20, 150), (400, 150), (380, 200), (40, 200)]), fill=255), lambda q, S_, c: q.rectangle(S_(20, 178, 400, 200), fill=c), (150, 156, 164), 120)
        return _done(im, w, h)
    return gcache(("tray38", kind, seed), mk)


def toque_el(seed=383):
    """a chef's toque: puffy white crown + a pleated band."""
    def mk():
        w, h = 220, 200; im, d, S = _cv(w, h)
        for cx, cy, r in ((70, 80, 46), (150, 80, 46), (110, 60, 54)):
            _ink_ell(d, cx, cy, r, r * 0.92, (252, 250, 244), seed + cx, INK_W, amp=1.0)
        _ink_poly(d, [(46, 100), (174, 100), (166, 176), (54, 176)], (252, 250, 244), seed + 1, INK_W)
        _shade(im, lambda q, S_: q.polygon(_P([(46, 100), (174, 100), (166, 176), (54, 176)]), fill=255), lambda q, S_, c: q.rectangle(S_(130, 100, 180, 180), fill=c), (214, 206, 190), 140)
        for x in range(70, 160, 22): d.line(S(x, 112, x - 2, 168), fill=INKC + (160,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("toque38", seed), mk)


def ticket_el(text="ORDER!", seed=384):
    """an order ticket (a paper slip with a torn bottom edge) — the 'order' your brain places."""
    def mk():
        w, h = 300, 210; im, d, S = _cv(w, h)
        P = [(30, 20), (270, 24), (266, 170)] + [(266 - 236 * k / 10, 170 + (10 if k % 2 else 0)) for k in range(11)] + [(30, 170)]
        _ink_poly(d, P, (252, 248, 236), seed, INK_W)
        d.rectangle(S(30, 20, 270, 58), fill=ACC + (255,)); d.line(S(30, 58, 270, 58), fill=INKC + (255,), width=4 * SC3)
        fnt = ImageFont.truetype(F_HAND, 46 * SC3)
        tw = d.textlength(text, font=fnt); d.text(((150 * SC3 - tw / 2), 78 * SC3), text, font=fnt, fill=INKC + (255,))
        for y in (140, 152): d.line(S(60, y, 240, y), fill=INKC + (90,), width=2 * SC3)
        return _done(im, w, h)
    return gcache(("ticket38", text, seed), mk)


def scissors_el(open_k=1.0, seed=385):
    """kitchen scissors: two saffron handle loops + steel blades; open_k 0 (shut) .. 1 (open)."""
    ok = round(clamp(open_k) * 6) / 6
    def mk():
        w, h = 260, 200; im, d, S = _cv(w, h)
        a = 0.08 + 0.42 * ok
        for sg in (-1, 1):
            ang = sg * a; c, s_ = math.cos(ang), math.sin(ang)
            R = lambda x, y: (100 + x * c - y * s_, 100 + x * s_ + y * c)
            blade = [R(0, -8), R(150, -2), R(150, 4), R(0, 10)]
            _ink_poly(d, blade, (214, 222, 230), seed + sg, INK_W - 1)
            hx, hy = R(-50, 0); _ink_ell(d, hx, hy, 30, 22, ACC, seed + 3 + sg, INK_W - 1, amp=0.6); _ink_ell(d, hx, hy, 15, 10, PAPER, seed + 5 + sg, 3, amp=0.4)
        _ink_ell(d, 100, 100, 7, 7, (160, 166, 172), seed + 9, 3)
        return _done(im, w, h)
    return gcache(("sciss38", ok, seed), mk)


def amylase_el(mood="happy", look=(0, 0), seed=386):
    """AMYLASE: a little water-blue prep-cook drop with a face and a tiny toque (it lives in your spit)."""
    def mk():
        w, h = 220, 260; im, d, S = _cv(w, h)
        P = [(110, 40)] + _arcpts(110, 160, 78, 78, -40, 220, 24)
        _ink_poly(d, P, SPIT, seed, INK_W, amp=1.0)
        _shade(im, lambda q, S_: q.polygon(S_(*sum(P, ())), fill=255), lambda q, S_, c: q.ellipse(S_(90, 140, 260, 300), fill=c), (150, 190, 226), 120)
        d.ellipse(S(70, 120, 92, 150), fill=SPIT_H + (230,))
        _face(d, S, 112, 176, 1.25, mood, look)
        for cx, cy, r in ((90, 58, 20), (130, 58, 20), (110, 46, 24)): _ink_ell(d, cx, cy, r, r, (252, 250, 244), seed + cx, 4, amp=0.6)
        _ink_poly(d, [(84, 66), (136, 66), (132, 90), (88, 90)], (252, 250, 244), seed + 2, 4)
        return _done(im, w, h)
    return gcache(("amyl38", mood, look, seed), mk)


def roti_el(bite=0, seed=387):
    """a plain roti (flatbread): a round light-brown disc with darker toasted spots; bite 0..2 = bites taken from the right edge."""
    def mk():
        w, h = 300, 300; im, d, S = _cv(w, h)
        P = _arcpts(150, 150, 126, 122, 0, 360, 40)[:-1]
        if bite:
            Q = []
            for (x, y) in P:
                for b in range(bite):
                    bx, by = 262 - 10 * b, 110 + 70 * b
                    if (x - bx) ** 2 + (y - by) ** 2 < 46 ** 2:
                        a = math.atan2(y - by, x - bx); x, y = bx + 46 * math.cos(a) * 0.98 - 20, by + 46 * math.sin(a)
                Q.append((x, y))
            P = Q
        _ink_poly(d, P, ROTI, seed, INK_W, amp=1.2)
        _shade(im, lambda q, S_: q.polygon(S_(*sum(P, ())), fill=255), lambda q, S_, c: q.ellipse(S_(80, 120, 360, 380), fill=c), ROTI_S, 90)
        r = np.random.default_rng(seed)
        for j in range(14):
            x, y = 150 + r.uniform(-90, 90), 150 + r.uniform(-86, 86)
            if (x - 150) ** 2 + (y - 150) ** 2 < 100 ** 2: d.ellipse(S(x - 8, y - 5, x + 8, y + 6), fill=ROTI_D + (150,))
        _hatch_in(im, (30, 30, 280, 280), lambda q, S_: q.ellipse(S_(150, 160, 290, 290), fill=255))
        return _done(im, w, h)
    return gcache(("roti38", bite, seed), mk)


# ---------------- Chubby's MOUTH-WATERING acting kit (ep 38) ----------------
def mouth_xy(x, y, s, t=None, lean=0.0, squash=0.0):
    """where Chubby INK's mouth corner is for chub(f, x, y, s, ...) (from his nose tip, ~34 px * s below it)."""
    nx, ny = nose_xy(x, y, s, t, lean, squash)
    return nx + 14 * s, ny + 34 * s


def drool(f, mx, my, s, t, t0, period=1.8, amt=1.0, seed=0):
    """a SALIVA drip from the lip corner: drip() (lib34: swell -> snap -> gravity -> springy stub) re-coloured clear water-blue."""
    global MUC, MUC_S, MUC_H
    old = (MUC, MUC_S, MUC_H); MUC, MUC_S, MUC_H = SPIT, SPIT_S, SPIT_H
    try: return drip(f, mx - 10 * s, my - 4 * s, s, t, t0, period, amt, seed, side=1)
    finally: MUC, MUC_S, MUC_H = old


def lick(f, mx, my, s, t, t0, dur=0.55):
    """a LIP LICK: the tongue tip pokes out at the left corner and sweeps across the top lip to the right (ease in-out), then pulls back in."""
    q = (t - t0) / dur
    if not (0 <= q < 1): return
    out = math.sin(math.pi * q) ** 0.6
    xx = mx - 46 * s + 64 * s * eio(clamp(q * 1.15))
    rx, ry = 14 * s * out + 2, 10 * s * out + 2
    cv2.ellipse(f, (int(xx), int(my - 6 * s)), (int(rx), int(ry)), 0, 0, 360, C(TONGUE), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(xx), int(my - 6 * s)), (int(rx), int(ry)), 0, 0, 360, C(INKC), max(2, int(3 * s)), cv2.LINE_AA)
    cv2.line(f, (int(xx), int(my - 6 * s - ry * 0.6)), (int(xx), int(my - 6 * s + ry * 0.2)), C((170, 60, 76)), max(1, int(2 * s)), cv2.LINE_AA)


def gulp(t, t0, dur=0.42):
    """a SWALLOW for chub(): 2-frame anticipation up (chin lifts), then the body squashes down as the lump drops. -> dict(dy, squash, k) and
    k (0..1 = the lump's way down the throat) for gulp_mark()."""
    q = (t - t0) / dur
    if not (0 <= q < 1.4): return dict(dy=0.0, squash=0.0, k=-1.0)
    if q < 0.12: return dict(dy=-6 * q / 0.12, squash=-0.1 * q / 0.12, k=0.0)
    if q < 1.0: k = (q - 0.12) / 0.88; return dict(dy=10 * math.sin(math.pi * k), squash=0.22 * math.sin(math.pi * k), k=k)
    return dict(dy=0.0, squash=0.0, k=-1.0)


def gulp_mark(f, x, y, s, k):
    """the lump going down the throat (a small ink arc on his neck) for gulp()['k']."""
    if k < 0: return
    gy = y - 300 * s + 70 * s * k
    pts = _arcpts(x + 6 * s, gy, 16 * s, 9 * s, 200, 340, 8)
    cv2.polylines(f, [np.int32(pts)], False, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)


def scent(f, src, dst, t, t0, k=1.0, col=None, n=3, amp=26, seed=0, hook=True, op=0.9):
    """an AROMA RIBBON: n wavy lines that travel from src (the food) to dst (his nose) — the travel draws on with k 0..1 — and curl into a little
    hook at the nose (the classic cartoon 'pulled by the smell'). The waves keep moving so it reads as a smell, not a rope."""
    col = col or ACC_L
    if k <= 0.01: return
    x0, y0 = src; x1, y1 = dst
    L = math.hypot(x1 - x0, y1 - y0) + 1e-6; nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    g = f.copy()
    for j in range(n):
        off = (j - (n - 1) / 2) * 22
        pts = []
        for i in range(60):
            u = i / 59 * k
            w_ = amp * math.sin(u * 9 + t * 6 + j * 1.7) * (1 - 0.6 * u) + off * (1 - u)
            pts.append((x0 + (x1 - x0) * u + nx * w_, y0 + (y1 - y0) * u + ny * w_))
        if hook and k > 0.95:                                                        # the hook at the nose
            hx, hy = pts[-1]; pts += [(hx + 22 * math.cos(a), hy - 22 + 22 * math.sin(a)) for a in np.linspace(math.pi / 2, -math.pi, 10)]
        cv2.polylines(g, [np.int32(pts)], False, C(INKC), 11, cv2.LINE_AA)
        cv2.polylines(g, [np.int32(pts)], False, C(col), 6, cv2.LINE_AA)
    f[:] = f * (1 - op) + g * op


def munch(t, rate=0.36):
    """a chewing mouth (closed / open / wide) for chub(mouth=...)."""
    q = (t / rate) % 1
    return 0 if q < 0.35 else (1 if q < 0.7 else 2)


# ---------------- board helpers ----------------
def brain_chef(f, x, y, s, t, mood="happy", look=(0, 0), op=1.0):
    """the head chef: the ink brain wearing a toque."""
    comp(f, scale_el(brain_ink_el(mood, look), s), x, y, op=op)
    comp(f, scale_el(toque_el(), 0.78 * s), x + 6 * s, y - 150 * s, op=op)


def starch_chain(f, x0, y, n, t, t0, cut_k=0.0, gap=62, r=22, k_draw=1.0):
    """STARCH as a long chain of beige beads that draws on (k_draw); cut_k 0..1 snips it from the left into PAIRS of saffron beads (maltose = sugar)
    that drift apart a little. Returns the x where the scissors should be."""
    m = int(n * k_draw)
    cut_upto = int(n / 2 * cut_k)                                                     # number of pairs cut so far
    pts = []
    for i in range(m):
        pair = i // 2
        cut = pair < cut_upto
        dx = (pair * 26 if cut else cut_upto * 26) ; dy = (-18 if (cut and pair % 2) else (18 if cut else 0)) + 8 * math.sin(t * 3 + i)
        pts.append((x0 + i * gap + dx, y + (dy if cut else 10 * (1 if i % 2 else -1)), cut))
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        if (i // 2) == ((i + 1) // 2) or not (a[2] or b[2]):                           # bonds inside a pair, or in the uncut chain
            cv2.line(f, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), C(INKC), 6, cv2.LINE_AA)
    for (x, yy, cut) in pts:
        cv2.circle(f, (int(x), int(yy)), r, C(ACC if cut else STARCH), -1, cv2.LINE_AA)
        cv2.circle(f, (int(x), int(yy)), r, C(ACC_S if cut else STARCH_S), 5, cv2.LINE_AA)
    return x0 + (2 * cut_upto) * gap + cut_upto * 26 - gap * 0.5
