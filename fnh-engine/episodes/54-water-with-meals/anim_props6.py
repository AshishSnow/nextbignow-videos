# ================= anim_props6.py = lib54 (ep 54, 19 Nov): "Does drinking water while you eat water down your stomach acid?" — ACCENT = ACID LIME
# (the stomach acid, the sensor bells, the acid tap, the question words). Water keeps the clear blue of ep 52 as the story's second colour (only on water).
# NEW PLACE: set_dhaba(t, blur, top_y, dim) = a roadside DHABA at noon (ochre wall, a hand-painted menu board, a big steel WATER DRUM with a tap, a glowing
# tandoor, a string of bulbs, a neem tree past the open side) + dhaba_front(f, top_y) = the long wooden table edge drawn AFTER the people.
# NEW CHARACTER: uncle(f, ...) = THAT UNCLE (chub + cream kurta + a thick moustache + a bald crown with grey sides + a watch).
# NEW CRAFT (ep 54) = LIQUID FX ANIMATION (2D effects animation of water): splash_crown / pour_stream / fly_drops2 / ripples — the splash curves UP and OUT
# (never straight up and down), every tongue + drop has its own speed (uneven timing: water that all lands together looks 'heavy like mud'), drops that
# break off keep the splash's energy (same velocity at the break), big / medium / small drops, and the splash ends in micro-splashes + ripples that slow
# down instead of stopping. A pour stream NARROWS as it falls (it speeds up, so the same water gets thinner), wobbles in waves that travel down it, and
# lands in a small continuous splash. =================
ACC = (150, 190, 30); ACC_S = (92, 126, 10); ACC_L = (214, 236, 150); ACC_XL = (240, 248, 214)   # acid lime = stomach acid / the question
ACID = (186, 214, 60); ACID_S = (120, 156, 20)
WAT = (150, 206, 246); WAT_S = (84, 160, 222); WAT_H = (240, 250, 255)
RED = (176, 40, 44)
KURTA = (238, 232, 214)
SRC_MAYO54 = "Source: Mayo Clinic (2025); Hackensack Meridian Health"
SRC_PHYS54 = "Source: StatPearls 'Physiology, Stomach' (NCBI / NIH)"
SRC_BLOAT54 = "Source: Mayo Clinic; Dr Manan Vora via India TV (2026)"
SC3 = 3


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


def _blend(f, ov, op):
    if op >= 0.999: f[:] = ov
    else: f[:] = f * (1 - op) + ov * op


# ---------------- LIQUID FX kit (also copied into template/anim_fx.py) ----------------
def ripples(f, x, y, t, t0, r=80, n=3, col=None, op=1.0, squash=0.28, life=1.1):
    """rings that spread from a landing point and SLOW DOWN (ease-out) while they fade; each ring starts a little later (uneven)."""
    u = t - t0
    if u < 0: return
    col = col or WAT_S
    for j in range(n):
        v = (u - 0.09 * j * (1 + 0.3 * j)) / (life * (0.8 + 0.25 * j))
        if v <= 0 or v >= 1: continue
        rr = r * (0.3 + 1.6 * (1 - (1 - v) ** 3))
        a = (1 - v) ** 1.5 * op
        ov = f.copy()
        cv2.ellipse(ov, (int(x), int(y)), (int(rr), max(2, int(rr * squash))), 0, 0, 360, C(col), max(2, int(r * 0.05)), cv2.LINE_AA)
        f[:] = f * (1 - a) + ov * a


def splash_crown(f, x, y, t, t0, r=80, col=None, rim=None, seed=0, n=9, op=1.0, g=None, spread=1.0):
    """a SPLASH where something lands in water / hits a surface at (x, y) at t0. Tongues curve up and OUT along arcs, each with its own speed;
    near its peak each tongue's tip breaks off as a drop that keeps the tongue's velocity, falls, and makes a micro-splash; ripples close it."""
    u = t - t0
    if u < 0 or u > 1.6: return
    col = col or WAT; rim = rim or WAT_S
    rng = np.random.default_rng(seed + 541)
    g = g or r * 38.0
    ov = f.copy()
    bw = r * (0.55 + 0.75 * (1 - (1 - clamp(u / 0.18)) ** 2)); ba = clamp(1 - (u - 0.35) / 0.5)          # the flat base oval
    if ba > 0:
        cv2.ellipse(ov, (int(x), int(y)), (int(bw), max(3, int(bw * 0.26))), 0, 0, 360, C(col), -1, cv2.LINE_AA)
        cv2.ellipse(ov, (int(x), int(y)), (int(bw), max(3, int(bw * 0.26))), 0, 0, 360, C(rim), max(2, int(r * 0.05)), cv2.LINE_AA)
    for i in range(n):
        side = -1 if i % 2 == 0 else 1
        a = side * (0.25 + 0.85 * rng.random()) * spread                       # angle from vertical, OUT to both sides
        sp = r * rng.uniform(6.5, 10.5) * (1.15 - 0.3 * abs(a))                 # uneven launch speeds
        vx, vy = sp * math.sin(a), -sp * math.cos(a)
        x0 = x + side * bw * rng.uniform(0.25, 0.8)
        tpk = -vy / g; tb = tpk * rng.uniform(0.75, 1.05)                       # breaks off near the peak
        dl = rng.uniform(0.0, 0.05)                                             # staggered start
        uu = u - dl
        if uu <= 0: continue
        wd = r * rng.choice([0.16, 0.11, 0.07])                                 # big / medium / small
        if uu < tb:                                                             # the TONGUE: a tapered arc from the base to its tip
            P = []
            for q in np.linspace(0, 1, 9):
                tq = uu * q
                P.append((x0 + vx * tq * 0.85, y + vy * tq + 0.5 * g * tq * tq))
            for k in range(len(P) - 1):
                w = max(2, int(wd * (0.4 + 0.9 * k / (len(P) - 1)) * 1.4))
                cv2.line(ov, (int(P[k][0]), int(P[k][1])), (int(P[k + 1][0]), int(P[k + 1][1])), C(col), w, cv2.LINE_AA)
            cv2.circle(ov, (int(P[-1][0]), int(P[-1][1])), max(3, int(wd * 0.9)), C(col), -1, cv2.LINE_AA)
            cv2.circle(ov, (int(P[-1][0]), int(P[-1][1])), max(3, int(wd * 0.9)), C(rim), 2, cv2.LINE_AA)
        else:                                                                   # the DROP: same energy, ballistic, then a micro-splash
            td = uu
            px, py = x0 + vx * td * 0.85, y + vy * td + 0.5 * g * td * td
            land = y + r * 0.15 * side * 0.5
            if py < land:
                rr = max(3, int(wd * 0.85))
                cv2.ellipse(ov, (int(px), int(py)), (rr, int(rr * 1.25)), math.degrees(math.atan2(vy + g * td, vx)) - 90, 0, 360, C(col), -1, cv2.LINE_AA)
                cv2.ellipse(ov, (int(px), int(py)), (rr, int(rr * 1.25)), math.degrees(math.atan2(vy + g * td, vx)) - 90, 0, 360, C(rim), 2, cv2.LINE_AA)
                cv2.circle(ov, (int(px - rr * 0.3), int(py - rr * 0.35)), max(1, rr // 3), C(WAT_H), -1, cv2.LINE_AA)
            else:                                                               # where it lands: a tiny crown + one ripple
                tl = (-vy + math.sqrt(max(0.0, vy * vy + 2 * g * (land - y)))) / g
                ms = uu - tl
                if 0 <= ms < 0.25:
                    lx = x0 + vx * tl * 0.85
                    for sg in (-1, 1):
                        cv2.line(ov, (int(lx), int(land)), (int(lx + sg * wd * 2.2 * (0.4 + ms * 4)), int(land - wd * 2.0 * (1 - ms * 4) * 1.4)), C(col), max(2, int(wd * 0.5)), cv2.LINE_AA)
    _blend(f, ov, op)
    ripples(f, x, y + 4, t, t0 + 0.3, r * 1.2, 3, rim, op * 0.8)


def pour_stream(f, x0, y0, x1, y1, t, w=26, col=None, rim=None, head=1.0, tail=0.0, seed=0, op=1.0, land=True):
    """a POUR from a spout (x0, y0) landing at (x1, y1): a parabola that NARROWS as it falls (it speeds up), with wobble waves travelling down;
    head 0..1 = how far the front has fallen (start of the pour), tail 0..1 = how much has already left the spout (end of the pour)."""
    col = col or WAT; rim = rim or WAT_S
    if head <= tail + 1e-3: return
    N = 40
    qs = np.linspace(tail, head, N)
    P = []; Wd = []
    for q in qs:
        px = x0 + (x1 - x0) * (1 - (1 - q) ** 2)                               # leaves sideways, then falls (ballistic look)
        py = y0 + (y1 - y0) * q * q
        wob = 0.10 * w * math.sin(q * 18 - t * 22 + seed) * q
        P.append((px + wob, py)); Wd.append(w * (1 / math.sqrt(1 + 6 * q)) * (0.75 + 0.25 * math.sin(q * 11 - t * 17 + seed)))
    L, R_ = [], []
    for i, (p, ww) in enumerate(zip(P, Wd)):
        j = min(i + 1, N - 1); k = max(i - 1, 0)
        dx, dy = P[j][0] - P[k][0], P[j][1] - P[k][1]; nn = math.hypot(dx, dy) + 1e-6
        nx, ny = -dy / nn, dx / nn
        L.append((p[0] + nx * ww / 2, p[1] + ny * ww / 2)); R_.append((p[0] - nx * ww / 2, p[1] - ny * ww / 2))
    poly = np.int32(np.round(np.array(L + R_[::-1])))
    ov = f.copy()
    cv2.fillPoly(ov, [poly], C(col), cv2.LINE_AA)
    cv2.polylines(ov, [poly], True, C(rim), 3, cv2.LINE_AA)
    hl = np.int32([(p[0] - ww * 0.18, p[1]) for p, ww in zip(P, Wd)][2:-2])
    if len(hl) > 1: cv2.polylines(ov, [hl], False, C(WAT_H), max(2, int(w * 0.12)), cv2.LINE_AA)
    _blend(f, ov, op)
    if land and head >= 0.999 and tail < 0.95:                                 # continuous small splash where it lands
        rng = np.random.default_rng(seed + 7)
        for j in range(6):
            ph = (t * rng.uniform(2.6, 3.8) + rng.random()) % 1
            a = (-1 if j % 2 else 1) * rng.uniform(0.3, 1.1)
            sp = w * rng.uniform(2.5, 4.2)
            px = x1 + math.sin(a) * sp * ph * 1.4; py = y1 - math.cos(a) * sp * ph * 2.4 + 0.5 * w * 9 * ph * ph
            rr = max(2, int(w * rng.choice([0.22, 0.15, 0.1]) * (1 - ph * 0.5)))
            cv2.circle(f, (int(px), int(py)), rr, C(col), -1, cv2.LINE_AA); cv2.circle(f, (int(px), int(py)), rr, C(rim), 1, cv2.LINE_AA)
        cv2.ellipse(f, (int(x1), int(y1)), (int(w * 1.3), int(w * 0.35)), 0, 0, 360, C(col), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(x1), int(y1)), (int(w * 1.3), int(w * 0.35)), 0, 0, 360, C(rim), 2, cv2.LINE_AA)


def fly_drops2(f, x, y, vx, vy, t, t0, n=7, r=10, seed=0, col=None, rim=None, g=1900.0, floor=None, op=1.0):
    """a spray of drops thrown from (x, y) at t0 with a mean velocity (vx, vy) px/s: each drop gets its own speed + size (uneven), falls on gravity,
    stretches along its path, and pops into a micro-splash at floor."""
    u = t - t0
    if u < 0: return
    col = col or WAT; rim = rim or WAT_S
    rng = np.random.default_rng(seed + 99)
    for j in range(n):
        dvx, dvy = vx * rng.uniform(0.6, 1.3) + rng.uniform(-120, 120), vy * rng.uniform(0.6, 1.25) + rng.uniform(-90, 90)
        uu = u - rng.uniform(0, 0.06)
        if uu < 0: continue
        px, py = x + dvx * uu, y + dvy * uu + 0.5 * g * uu * uu
        rr = r * rng.choice([1.3, 0.9, 0.6])
        if floor is not None and py > floor:
            tl = (-dvy + math.sqrt(max(0.0, dvy * dvy + 2 * g * (floor - y)))) / g; ms = uu - tl
            if ms < 0.22:
                lx = x + dvx * tl
                for sg in (-1, 1): cv2.line(f, (int(lx), int(floor)), (int(lx + sg * rr * 2 * (0.5 + ms * 5)), int(floor - rr * 2 * (1 - ms * 4.5))), C(col), max(2, int(rr * 0.5)), cv2.LINE_AA)
            continue
        if py > H + 50: continue
        vyy = dvy + g * uu; ang = math.degrees(math.atan2(vyy, dvx)) - 90
        st = 1 + min(0.8, math.hypot(dvx, vyy) / 2600)
        ov = f.copy()
        cv2.ellipse(ov, (int(px), int(py)), (max(2, int(rr)), max(2, int(rr * st))), ang, 0, 360, C(col), -1, cv2.LINE_AA)
        cv2.ellipse(ov, (int(px), int(py)), (max(2, int(rr)), max(2, int(rr * st))), ang, 0, 360, C(rim), 2, cv2.LINE_AA)
        _blend(f, ov, op)


# ---------------- props (ink language) ----------------
def drum_el(seed=541):
    """the dhaba's big steel WATER DRUM with a brass tap near the bottom and a steel lid."""
    def mk():
        w, h = 300, 420; im, d, S = _cv(w, h)
        body = [(40, 60), (260, 60), (266, 380), (34, 380)]
        _ink_poly(d, body, STEEL, seed, INK_W, amp=0.8)
        _shade(im, lambda q, S_: q.polygon(_P(body), fill=255), lambda q, S_, c: q.rectangle(S_(190, 40, 300, 400), fill=c), STEEL_S, 120)
        _hatch_in(im, (196, 64, 262, 376), lambda q, S_: q.polygon(_P(body), fill=255), -40, 9, 34)
        for y in (120, 250): d.line(S(40, y, 262, y), fill=STEEL_S + (220,), width=4 * SC3)
        d.polygon(_P([(80, 70), (96, 70), (92, 370), (76, 370)]), fill=STEEL_H + (220,))
        _ink_ell(d, 150, 60, 112, 22, (196, 204, 212), seed + 1, INK_W - 1, amp=0.6)
        _ink_ell(d, 150, 46, 30, 10, STEEL_S, seed + 2, INK_W - 2, amp=0.5)
        _ink_poly(d, [(140, 320), (196, 320), (196, 338), (176, 338), (176, 360), (160, 360), (160, 338), (140, 338)], (214, 170, 70), seed + 3, 4, amp=0.4)
        return _done(im, w, h)
    return gcache(("drum54", seed), mk)


def jug54_el(seed=542, mood=None):
    """a steel water JUG (dhaba style: round belly, tall neck, a spout lip and a loop handle) - generic, no brand."""
    def mk():
        w, h = 240, 300; im, d, S = _cv(w, h)
        body = [(70, 60), (150, 60), (150, 110), (196, 170), (196, 250), (160, 286), (60, 286), (24, 250), (24, 170), (70, 110)]
        _ink_poly(d, body, STEEL, seed, INK_W, amp=0.8)
        _shade(im, lambda q, S_: q.polygon(_P(body), fill=255), lambda q, S_, c: q.rectangle(S_(130, 40, 240, 300), fill=c), STEEL_S, 120)
        _ink_poly(d, [(66, 60), (40, 40), (76, 48)], STEEL, seed + 1, 5, amp=0.4)                     # spout lip (left)
        d.arc(S(170, 110, 236, 230), -90, 90, fill=INKC + (255,), width=10 * SC3)                    # handle
        d.arc(S(170, 110, 236, 230), -90, 90, fill=STEEL_S + (255,), width=5 * SC3)
        d.polygon(_P([(56, 170), (66, 170), (62, 270), (52, 270)]), fill=STEEL_H + (220,))
        if mood: _face(d, S, 110, 200, 1.2, mood)
        return _done(im, w, h)
    return gcache(("jug54", seed, mood), mk)


def menu_board_el(seed=543):
    """a hand-painted dhaba menu board (green with yellow letters): DAL / ROTI / CHAI / LASSI with prices as squiggles."""
    def mk():
        w, h = 300, 220; im, d, S = _cv(w, h)
        _ink_poly(d, [(12, 12), (288, 12), (288, 208), (12, 208)], (46, 110, 76), seed, 6, amp=0.6)
        fnt = font(F_HAND, 30 * SC3)
        for j, tx in enumerate(("DAL", "ROTI", "CHAI", "LASSI")):
            if fnt: d.text((30 * SC3, (24 + 44 * j) * SC3), tx, font=fnt, fill=(250, 214, 90, 255))
            d.line(S(170, 46 + 44 * j, 260, 46 + 44 * j), fill=(250, 214, 90, 255), width=4 * SC3)
        return _done(im, w, h)
    return gcache(("menu54", seed), mk)


def acid_tap_el(open_k=0.0, seed=544):
    """the ACID TAP on the board: an ink tap (handle turns with open_k), lime drip ready at the nozzle."""
    ok = round(clamp(open_k) * 6) / 6
    def mk():
        w, h = 240, 200; im, d, S = _cv(w, h)
        _ink_poly(d, [(0, 70), (120, 70), (150, 92), (170, 150), (140, 150), (126, 106), (0, 106)], (212, 216, 224), seed, INK_W, amp=0.6)
        _shade(im, lambda q, S_: q.polygon(_P([(0, 92), (120, 92), (150, 150), (0, 106)]), fill=255), lambda q, S_, c: q.rectangle(S_(0, 92, 240, 200), fill=c), STEEL_S, 120)
        a = math.radians(-90 + 80 * ok)
        cx, cy = 96, 60
        d.line(S(cx, cy, cx + 70 * math.cos(a), cy + 70 * math.sin(a)), fill=INKC + (255,), width=16 * SC3)
        d.line(S(cx, cy, cx + 70 * math.cos(a), cy + 70 * math.sin(a)), fill=ACC + (255,), width=9 * SC3)
        _ink_ell(d, cx, cy, 16, 16, (212, 216, 224), seed + 1, 5, amp=0.3)
        return _done(im, w, h)
    return gcache(("acidtap54", ok, seed), mk)


# ---------------- other people: THAT UNCLE ----------------
def uncle(f, x, y, s, t, la=(24, 12), ra=(24, 12), hand_l="open", hand_r="open", mouth=0, expr="n", brow="sus", look=(0, 0), turn=0.0, lean=0.0,
          hold=None, hold_off=(0, 0), hold_front=False, sit=False):
    """THAT UNCLE: chub with a cream kurta (shirt), a bald crown with grey side hair, a thick black moustache, a steel watch."""
    kw_ = dict(hold=hold, hold_off=hold_off, hold_front=hold_front) if hold is not None else {}
    chub(f, x, y, s, t=t, shirt=KURTA, la=la, ra=ra, hand_l=hand_l, hand_r=hand_r, mouth=mouth, expr=expr, brow=brow, look=look, turn=turn, lean=lean, sit=sit, **kw_)
    hx, hy = x + lean * 2 * s + turn * 14 * s, y - 420 * s
    cv2.ellipse(f, (int(hx), int(hy - 70 * s)), (int(84 * s), int(46 * s)), 0, 180, 360, C(INK_SKIN), -1, cv2.LINE_AA)  # bald crown
    cv2.ellipse(f, (int(hx), int(hy - 70 * s)), (int(84 * s), int(46 * s)), 0, 180, 360, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    for sg in (-1, 1):                                                                                                 # grey side tufts
        cv2.ellipse(f, (int(hx + sg * 86 * s), int(hy - 40 * s)), (int(22 * s), int(36 * s)), 0, 0, 360, C((200, 200, 204)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(hx + sg * 86 * s), int(hy - 40 * s)), (int(22 * s), int(36 * s)), 0, 0, 360, C(INKC), max(2, int(3 * s)), cv2.LINE_AA)
    mx = hx + turn * 18 * s + look[0] * 4 * s; my = hy + 40 * s                                                       # the moustache
    M = np.int32([(mx - 58 * s, my + 12 * s), (mx - 30 * s, my - 10 * s), (mx, my - 4 * s), (mx + 30 * s, my - 10 * s), (mx + 58 * s, my + 12 * s), (mx + 30 * s, my + 6 * s), (mx, my + 10 * s), (mx - 30 * s, my + 6 * s)])
    cv2.fillPoly(f, [M], C((52, 40, 34)), cv2.LINE_AA)


# ---------------- NEW PLACE: the DHABA at noon ----------------
DHA_TOP = 1330


def set_dhaba(t=0.0, blur=5, top_y=DHA_TOP, dim=0.0):
    """THE DHABA: warm ochre wall with a lighter plaster band, a hand-painted menu board, a big steel water drum with a tap on a stand (right),
    an open side with a neem tree in noon sun (left), a glowing tandoor mouth (far right, low), a sagging string of bulbs. Paper-softened."""
    def mk():
        f = _vgrad((244, 214, 160), (224, 182, 124), 0, top_y)
        cv2.rectangle(f, (0, 0), (W, 200), C((196, 150, 100)), -1)                                                    # roof beam shadow
        for x in range(0, W, 140): cv2.rectangle(f, (x, 150), (x + 26, 230), C((150, 104, 70)), -1)                 # rafters
        cv2.rectangle(f, (0, top_y - 140), (W, top_y), C((214, 168, 114)), -1)                                       # dado
        cv2.rectangle(f, (40, 330), (330, 900), C((252, 238, 196)), -1, cv2.LINE_AA)                                 # the open side: bright noon
        for j, (cx, cy, rr) in enumerate(((120, 560, 120), (250, 500, 140), (200, 650, 110), (300, 640, 90))):
            cv2.circle(f, (cx, cy), rr, C((150, 196, 120) if j % 2 else (130, 180, 104)), -1, cv2.LINE_AA)          # neem crown
        cv2.rectangle(f, (180, 680), (210, 900), C((140, 104, 76)), -1)
        cv2.rectangle(f, (40, 820), (330, 900), C((226, 206, 160)), -1)                                              # road
        cv2.rectangle(f, (40, 330), (330, 900), C((150, 104, 70)), 14, cv2.LINE_AA)
        ex = menu_board_el(); comp(f, ex, 560, 520)
        cv2.rectangle(f, (760, 860), (1000, top_y - 140), C((150, 104, 70)), -1)                                     # drum stand
        comp(f, scale_el(drum_el(), 0.95), 880, 680)
        cv2.circle(f, (1010, top_y - 60), 120, C((150, 90, 60)), -1, cv2.LINE_AA)                                    # tandoor (clay)
        cv2.ellipse(f, (1010, top_y - 150), (70, 26), 0, 0, 360, C((60, 30, 20)), -1, cv2.LINE_AA)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("dhaba54", blur, top_y), mk).copy()
    for j in range(9):                                                                                               # string of bulbs (sway)
        u = j / 8; bx = 380 + 640 * u; by = 250 + 70 * math.sin(math.pi * u) + 4 * math.sin(t * 2 + j)
        cv2.circle(f, (int(bx), int(by)), 9, C((255, 236, 170)), -1, cv2.LINE_AA)
        glow(f, bx, by, 40, (255, 220, 150), 0.10)
    lamp_glow(f, 1010, top_y - 150, 260, (255, 150, 80), 0.18 + 0.03 * math.sin(t * 7))
    god_rays(f, 180, 360, t, amt=0.18, ang0=0.9)
    dust_motes(f, t, 80, 380, 600, 1200, amt=0.5)
    if dim > 0: f = f * (1 - 0.5 * dim)
    return inkify(f)


def dhaba_front(f, top_y=DHA_TOP):
    """the long dhaba TABLE edge (drawn AFTER the people): a thick wooden plank top with grain, a steel strip, a bench below."""
    cv2.rectangle(f, (0, top_y), (W, top_y + 70), C((176, 120, 72)), -1)
    for y in (top_y + 22, top_y + 46): cv2.line(f, (0, y), (W, y), C((150, 100, 60)), 3, cv2.LINE_AA)
    cv2.rectangle(f, (0, top_y + 70), (W, top_y + 84), C((206, 212, 220)), -1)
    cv2.line(f, (0, top_y), (W, top_y), C(INKC), 6, cv2.LINE_AA); cv2.line(f, (0, top_y + 84), (W, top_y + 84), C(INKC), 5, cv2.LINE_AA)
    cv2.rectangle(f, (0, top_y + 84), (W, H), C((120, 84, 56)), -1)
    _hatch_band(f, top_y + 90, H)
