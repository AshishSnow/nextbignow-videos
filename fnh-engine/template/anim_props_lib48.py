# ================= anim_props6.py = lib48 (ep 48, 17 Nov): "Does eating ice cream in winter give you a cold?" (Part 2 of ep 44) — ACCENT = STRAWBERRY PINK
# (the ice cream, the question words, the chips). The virus keeps its olive green from lib44 (the culprit); the night outside is cool blue.
# NEW PLACE: set_wedding(t, blur, top_y, dim) = a WINTER WEDDING tent at night (shamiana stripes in maroon + saffron, marigold strings, fairy-light swags,
# cold blue fog in the open sides) + wedding_front(f, top_y) = the dessert counter (white cloth, pink + gold swags) drawn AFTER Chubby.
# NEW INK PROPS: icecream_cup_el(mood, look, melt), cone_el(mood, look, drip, bite), lolly_el(mood, look), jamun_bowl_el(mood) + ladle (the shared serving spoon),
# nhs_card_el(k) is drawn live on the board in anim_shots.
# NEW ACTING (Chubby INK): shiver(t, amt, s) -> kwargs for chub (fast small tremble, chattering teeth, hunched lean; every 1.6 s a breath puff via fog_puffs);
# stole(f, x, y, s, lean) = a maroon wedding shawl over his shoulders. =================
ACC = (234, 112, 150); ACC_S = (176, 52, 96); ACC_L = (250, 186, 206); ACC_XL = (254, 228, 236)      # strawberry pink = the ice cream / the question
VAN = (252, 244, 220); VAN_S = (226, 210, 170)                                                       # vanilla scoop
CUP = (250, 248, 242); CUP_S = (212, 206, 196)
WAF = (226, 168, 96); WAF_S = (176, 116, 54)                                                         # wafer cone
LOL = (246, 140, 70); LOL_S = (196, 92, 40)                                                          # orange ice lolly
JAM = (128, 62, 36); JAM_S = (86, 38, 20); SYR = (232, 176, 90)                                      # gulab jamun + syrup
MAROON = (138, 40, 58); MAROON_S = (96, 24, 40); GOLD = (232, 182, 70)
NIGHT = (52, 70, 112)
SRC_VIR48 = "Source: Mayo Clinic; Penn Medicine; India TV (doctor)"
SRC_THROAT = "Source: Mayo Clinic News Network"
SRC_NHS = "Source: NHS 111 Wales; nidirect"
SRC_WIN48 = "Source: Penn Medicine; Mayo Clinic"
SC3 = 3


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


# ---------------- props (ink language: one warm-ink wobbly outline, flat fill, shade + hatch on the shadow side) ----------------
def icecream_cup_el(mood="happy", look=(0, 0), melt=0.0, scoops=2, seed=481):
    """a wedding-counter PAPER CUP of ice cream: a pink + a vanilla scoop, a little wooden spoon, a face on the cup; melt 0..1 = drips down the cup."""
    mk_m = round(clamp(melt) * 4) / 4
    def mk():
        w, h = 300, 340; im, d, S = _cv(w, h)
        cup = [(62, 160), (238, 160), (212, 320), (88, 320)]
        _ink_poly(d, cup, CUP, seed, INK_W, amp=1.0)
        for j in range(4):                                                                    # pink stripes on the paper cup
            x0 = 80 + j * 46
            d.polygon(_P([(x0, 166), (x0 + 18, 166), (x0 + 12, 316), (x0 - 4, 316)]), fill=ACC_L + (255,))
        _shade(im, lambda q, S_: q.polygon(_P(cup), fill=255), lambda q, S_, c: q.rectangle(S_(170, 150, 260, 330), fill=c), CUP_S, 110)
        _hatch_in(im, (176, 166, 240, 316), lambda q, S_: q.polygon(_P(cup), fill=255), -40, 10, 30)
        _ink_poly(d, cup, None, seed, INK_W, amp=1.0)
        if scoops >= 2:
            _ink_ell(d, 112, 132, 62, 54, VAN, seed + 1, INK_W - 1, amp=1.2)
            d.arc(S(70, 92, 130, 150), 200, 260, fill=(255, 255, 255, 255), width=5 * SC3)
        _ink_ell(d, 188, 118, 66, 60, ACC, seed + 2, INK_W - 1, amp=1.2)
        _shade(im, lambda q, S_: q.ellipse(S_(122, 58, 254, 178), fill=255), lambda q, S_, c: q.ellipse(S_(186, 80, 300, 220), fill=c), ACC_S, 110)
        for (x, y) in ((168, 96), (204, 120), (180, 140), (220, 98)):                         # strawberry bits
            d.ellipse(S(x - 5, y - 4, x + 5, y + 4), fill=ACC_S + (230,))
        d.arc(S(140, 70, 200, 120), 200, 260, fill=(255, 255, 255, 230), width=5 * SC3)
        _ink_poly(d, [(206, 92), (262, 20), (274, 28), (222, 100)], (214, 170, 110), seed + 3, 4, amp=0.6)   # the little wooden spoon
        if mk_m > 0:
            for j, x in enumerate((96, 150, 204)):
                L = 40 * mk_m * (0.6 + 0.4 * ((j * 7) % 3) / 2)
                col = ACC if j != 0 else VAN
                d.line(S(x, 160, x - 2, 160 + L), fill=col + (255,), width=10 * SC3)
                d.ellipse(S(x - 9, 160 + L - 6, x + 7, 160 + L + 10), fill=col + (255,), outline=INKC + (255,), width=2 * SC3)
        _face(d, S, 150, 250, 1.5, mood, look)
        return _done(im, w, h)
    return gcache(("icup48", mood, look, mk_m, scoops, seed), mk)


def cone_el(mood="happy", look=(0, 0), drip=0.0, bite=False, seed=482):
    """an ice cream CONE: a waffle cone (cross-hatch) with a pink scoop; drip 0..1 = a drip running down; bite = a bite out of the scoop."""
    dk = round(clamp(drip) * 4) / 4
    def mk():
        w, h = 260, 400; im, d, S = _cv(w, h)
        cone = [(52, 150), (208, 150), (130, 384)]
        _ink_poly(d, cone, WAF, seed, INK_W, amp=0.8)
        for j in range(7):                                                                    # waffle lines
            d.line(S(56 + j * 26, 152, 130 + (j - 3) * 6, 380), fill=WAF_S + (200,), width=3 * SC3)
            d.line(S(204 - j * 26, 152, 130 - (j - 3) * 6, 380), fill=WAF_S + (200,), width=3 * SC3)
        _ink_poly(d, cone, None, seed, INK_W, amp=0.8)
        sc = _arcpts(130, 132, 92, 86, 180, 360, 26) + [(222, 150), (196, 166), (166, 152), (130, 168), (96, 152), (64, 166), (38, 150)]
        _ink_poly(d, sc, ACC, seed + 1, INK_W - 1, amp=1.2)
        _shade(im, lambda q, S_: q.polygon(_P(sc), fill=255), lambda q, S_, c: q.ellipse(S_(140, 60, 260, 200), fill=c), ACC_S, 110)
        d.arc(S(70, 60, 150, 140), 200, 260, fill=(255, 255, 255, 230), width=6 * SC3)
        if bite: d.ellipse(S(170, 40, 240, 100), fill=(0, 0, 0, 0)); _ink_ell(d, 210, 70, 30, 26, None, seed + 4, 4, amp=0.6)
        if dk > 0:
            d.line(S(84, 160, 82, 160 + 90 * dk), fill=ACC + (255,), width=12 * SC3)
            _ink_ell(d, 82, 166 + 90 * dk, 9, 11, ACC, seed + 5, 3, amp=0.4)
        _face(d, S, 130, 110, 1.4, mood, look)
        return _done(im, w, h)
    return gcache(("cone48", mood, look, dk, bite, seed), mk)


def lolly_el(mood="happy", look=(0, 0), seed=483):
    """an ICE LOLLY: a rounded orange bar on a wooden stick, frost specks, a face."""
    def mk():
        w, h = 200, 380; im, d, S = _cv(w, h)
        _ink_poly(d, [(88, 250), (112, 250), (112, 366), (88, 366)], (222, 186, 130), seed + 1, 5, amp=0.5)
        bar = _arcpts(100, 92, 70, 70, 180, 360, 16) + [(170, 260), (30, 260)]
        _ink_poly(d, bar, LOL, seed, INK_W, amp=1.0)
        _shade(im, lambda q, S_: q.polygon(_P(bar), fill=255), lambda q, S_, c: q.rectangle(S_(110, 20, 200, 270), fill=c), LOL_S, 110)
        _hatch_in(im, (118, 40, 168, 256), lambda q, S_: q.polygon(_P(bar), fill=255), -40, 10, 30)
        d.line(S(52, 80, 52, 220), fill=(255, 230, 200, 220), width=7 * SC3)
        for (x, y) in ((70, 60), (140, 120), (60, 200), (130, 230)):
            d.line(S(x - 5, y, x + 5, y), fill=(255, 255, 255, 230), width=2 * SC3); d.line(S(x, y - 5, x, y + 5), fill=(255, 255, 255, 230), width=2 * SC3)
        _face(d, S, 100, 160, 1.5, mood, look)
        return _done(im, w, h)
    return gcache(("lolly48", mood, look, seed), mk)


def jamun_bowl_el(mood="n", look=(0, 0), seed=484):
    """the buffet's steel BOWL of gulab jamun in syrup (the bowl has the face); the big shared LADLE is drawn by ladle()."""
    def mk():
        w, h = 380, 240; im, d, S = _cv(w, h)
        body = _arcpts(190, 96, 168, 130, 0, 180, 30)
        _ink_poly(d, body, STEEL, seed, INK_W, amp=1.0)
        _shade(im, lambda q, S_: q.polygon(_P(body), fill=255), lambda q, S_, c: q.ellipse(S_(200, 40, 400, 260), fill=c), STEEL_S, 120)
        d.arc(S(50, 40, 170, 210), 120, 200, fill=STEEL_H + (230,), width=7 * SC3)
        _ink_ell(d, 190, 96, 170, 22, SYR, seed + 1, INK_W - 1, amp=0.8)
        for j, (x, y) in enumerate(((110, 84), (170, 76), (232, 82), (290, 90), (140, 100), (206, 100), (262, 104))):
            _ink_ell(d, x, y, 30, 22, JAM, seed + 10 + j, 4, amp=0.6)
            d.arc(S(x - 20, y - 16, x + 6, y + 4), 200, 260, fill=(220, 150, 110, 255), width=4 * SC3)
        _face(d, S, 190, 170, 1.5, mood, look)
        return _done(im, w, h)
    return gcache(("jamun48", mood, look, seed), mk)


def ladle(f, x, y, ang=-55, s=1.0, germs=0):
    """the shared serving LADLE: a steel cup at (x, y) and a long handle up at angle ang (deg from the +x axis, screen y down). Returns the handle grip (gx, gy)."""
    a = math.radians(ang); L = 380 * s
    gx, gy = x + L * math.cos(a), y + L * math.sin(a)
    cv2.line(f, (int(x), int(y)), (int(gx), int(gy)), C(INKC), int(26 * s), cv2.LINE_AA)
    cv2.line(f, (int(x), int(y)), (int(gx), int(gy)), C(STEEL), int(16 * s), cv2.LINE_AA)
    cv2.line(f, (int(x + 4), int(y - 4)), (int(gx + 4), int(gy - 4)), C(STEEL_H), int(4 * s), cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y)), (int(54 * s), int(38 * s)), 0, 0, 360, C(STEEL), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y)), (int(54 * s), int(38 * s)), 0, 0, 360, C(INKC), max(2, int(6 * s)), cv2.LINE_AA)
    return gx, gy


def stole(f, x, y, s, lean=0.0, dx=0.0):
    """a maroon WEDDING SHAWL with a gold border draped over Chubby's shoulders (draw AFTER chub(f, x, y, s, ...)); two ends hang down the front."""
    hx = x + dx + lean * 1.6 * s; sy = y - 268 * s
    for sg in (-1, 1):
        P = np.array([(hx + sg * 40 * s, sy - 22 * s), (hx + sg * 150 * s, sy + 6 * s), (hx + sg * 150 * s, sy + 210 * s), (hx + sg * 96 * s, sy + 222 * s),
                      (hx + sg * 70 * s, sy + 40 * s)], np.int32)
        cv2.fillPoly(f, [P], C(MAROON), cv2.LINE_AA)
        Q = np.array([(hx + sg * 150 * s, sy + 6 * s), (hx + sg * 150 * s, sy + 210 * s), (hx + sg * 96 * s, sy + 222 * s)], np.int32)
        cv2.polylines(f, [Q], False, C(GOLD), max(2, int(9 * s)), cv2.LINE_AA)
        for j in range(4):                                                        # fringe
            fx = hx + sg * (100 + 14 * j) * s
            cv2.line(f, (int(fx), int(sy + 216 * s)), (int(fx), int(sy + 236 * s)), C(GOLD), max(1, int(3 * s)), cv2.LINE_AA)
        cv2.polylines(f, [P], True, C(INKC), max(2, int(5 * s)), cv2.LINE_AA)
        for j in range(3):                                                        # hatch on the shadow fold
            yy = sy + (70 + 40 * j) * s
            cv2.line(f, (int(hx + sg * 84 * s), int(yy)), (int(hx + sg * 120 * s), int(yy + 26 * s)), C(MAROON_S), max(1, int(4 * s)), cv2.LINE_AA)
    nk = np.array([(hx - 44 * s, sy - 22 * s), (hx, sy - 4 * s), (hx + 44 * s, sy - 22 * s), (hx + 40 * s, sy - 6 * s), (hx, sy + 14 * s), (hx - 40 * s, sy - 6 * s)], np.int32)
    cv2.fillPoly(f, [nk], C(MAROON), cv2.LINE_AA); cv2.polylines(f, [nk], True, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)


# ---------------- ACTING: the SHIVER (a cold body, not a reflex: continuous, small, fast, uneven) ----------------
def shiver(t, amt=1.0, s=1.0, seed=0):
    """kwargs-ish dict for chub: dx (add to x), lean, squash, mouth (chattering teeth 've' <-> closed), expr, brow, hair.
    Real shivering is a fast (~8-10 Hz) small tremor with irregular bursts, shoulders up (hunched = squash), teeth chatter at ~6 Hz."""
    burst = 0.55 + 0.45 * max(0.0, math.sin(t * 2.1 + seed) * math.sin(t * 0.9 + 1.3 * seed))
    a = amt * burst
    dx = a * s * (5 * math.sin(t * 59 + seed) + 2.5 * math.sin(t * 83))
    return dict(dx=dx, lean=a * 1.6 * math.sin(t * 47 + seed), squash=0.04 * amt, mouth=("ve" if int(t * 12) % 2 else 0) if amt > 0.3 else 0,
                expr="ouch" if amt > 0.6 else "n", brow="sad", hair=(dx * 0.5, 0))


def fog_puffs(f, mx, my, t, period=1.6, dir_=1, s=1.0, t_start=-9.0):
    """cold breath puffs out of a mouth at (mx, my) every `period` s (lib11 breath)."""
    k0 = math.floor((t - t_start) / period)
    for k in (k0, k0 - 1):
        t0 = t_start + k * period
        breath(f, mx, my, t, t0, dir_, s, 1.2)


# ---------------- NEW PLACE: THE WINTER WEDDING TENT (night) ----------------
def set_wedding(t=0.0, blur=6, top_y=1330, dim=0.0, fog=True):
    """NEW PLACE (ep 48) THE WINTER WEDDING: inside a shamiana tent at night — maroon + saffron tent stripes, marigold strings hanging down, fairy-light
    swags across the top, warm bokeh of the party; the open sides of the tent show the cold blue foggy night. Warm key from the swags, cool rim from the
    sides. Paper-softened for Chubby INK. dim 0..1 = lights down."""
    def mk():
        f = _vgrad((92, 34, 48), (150, 70, 60), 0, top_y)
        for i in range(12):                                                        # tent stripes (maroon / saffron), wider at the bottom
            x0 = -60 + i * 110; col = (140, 52, 66) if i % 2 == 0 else (206, 140, 84)
            P = np.array([(x0 + 30, 0), (x0 + 110 + 30, 0), (x0 + 120, top_y), (x0, top_y)], np.int32)
            cv2.fillPoly(f, [P], C(_mix(col, (176, 140, 132), 0.38)), cv2.LINE_AA)
        for side in (0, 1):                                                        # open sides: the cold foggy night
            x0, x1 = (0, 170) if side == 0 else (910, 1080)
            f[300:top_y, x0:x1] = _vgrad((40, 56, 96), (86, 104, 140), 300, top_y)[300:top_y, x0:x1]
            for j in range(5):
                cv2.circle(f, (x0 + 30 + 28 * j, 900 + 40 * (j % 2)), 4, C((250, 226, 170)), -1, cv2.LINE_AA)   # far street lights
            cv2.line(f, (x1 if side == 0 else x0, 300), (x1 if side == 0 else x0, top_y), C((96, 30, 44)), 18, cv2.LINE_AA)
        for i in range(7):                                                         # marigold strings hanging down
            x = 210 + i * 110
            for j in range(16):
                y = 250 + j * 34
                cv2.circle(f, (x + int(4 * math.sin(j)), y), 15, C((244, 150, 30) if j % 3 else (252, 206, 60)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (0, top_y - 90), (W, top_y), C((70, 30, 40)), -1)        # the far guests' table edge (dark)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("set_wedding48", blur, top_y), mk).copy()
    if fog:                                                                        # fog drifting in the open sides
        for side in (0, 1):
            x0 = 0 if side == 0 else 910
            m = np.zeros((H, 170), np.float32)
            for j in range(4):
                cy = 700 + 180 * j + 40 * math.sin(t * 0.4 + j)
                m[int(cy - 90):int(cy + 90)] += 0.18
            m = cv2.GaussianBlur(m, (0, 0), 30)[..., None]
            f[:, x0:x0 + 170] = f[:, x0:x0 + 170] * (1 - m) + np.array(C((210, 222, 240)), np.float32) * m
    for r in range(3):                                                             # fairy-light swags across the top (twinkle)
        for i in range(19):
            u = i / 18; x = 30 + 1020 * u; y = 90 + 70 * r + 80 * math.sin(math.pi * u) * (1 if r % 2 == 0 else 0.6)
            a = 0.5 + 0.5 * math.sin(t * 3 + i * 1.7 + r)
            glow(f, x, y, 24, (255, 214, 140), 0.08 + 0.07 * a)
            cv2.circle(f, (int(x), int(y)), 5, C(_mix((255, 214, 140), (255, 255, 255), a)), -1, cv2.LINE_AA)
    bokeh(f, t, 10, 7, 600, 1200, 18, 46, amt=0.22)
    lamp_glow(f, 540, 300, 620, (255, 206, 140), 0.22)
    if dim > 0: f = f * (1 - 0.55 * dim)
    return inkify(f)


def wedding_front(f, top_y=1330):
    """the dessert COUNTER in front of Chubby: white cloth top, pink + gold swags along the front, a marigold line (props stand on it at y ~ top_y - 10)."""
    def mk():
        g = np.zeros((H, W, 4), np.float32)
        cv2.rectangle(g, (0, top_y), (W, H), (0.97, 0.95, 0.91, 1.0), -1)
        cv2.rectangle(g, (0, top_y), (W, top_y + 26), (0.99, 0.98, 0.95, 1.0), -1)
        cv2.line(g, (0, top_y), (W, top_y), (*[v / 255 for v in INKC], 1.0), 6, cv2.LINE_AA)
        for i in range(5):                                                         # swags
            x0 = i * 216; pts = np.array([(x0 + 216 * u, top_y + 40 + 70 * math.sin(math.pi * u)) for u in np.linspace(0, 1, 20)], np.int32)
            pts2 = pts + np.array([0, 34])
            poly = np.vstack([pts, pts2[::-1]])
            cv2.fillPoly(g, [poly], (*[v / 255 for v in ACC_L], 1.0), cv2.LINE_AA)
            cv2.polylines(g, [pts2], False, (*[v / 255 for v in GOLD], 1.0), 6, cv2.LINE_AA)
            cv2.polylines(g, [pts], False, (*[v / 255 for v in INKC], 1.0), 4, cv2.LINE_AA)
            cv2.circle(g, (x0, top_y + 44), 22, (*[v / 255 for v in (244, 150, 30)], 1.0), -1, cv2.LINE_AA)
        for j in range(8):                                                         # cloth folds (hatch)
            x = 60 + j * 135
            cv2.line(g, (x, top_y + 160), (x - 20, H), (0.86, 0.83, 0.78, 1.0), 4, cv2.LINE_AA)
        return g
    g = gcache(("wedfront48", top_y), mk)
    a = g[..., 3:4]; f[:] = f * (1 - a) + g[..., :3] * a


def tremble_marks(f, x, y, s, t):
    """cartoon SHIVER marks: short double ink arcs that flicker beside the shoulders (reads as 'shaking' even in a still frame)."""
    if int(t * 10) % 3 == 2: return
    for sg in (-1, 1):
        cx = x + sg * 200 * s; cy = y - 300 * s
        for j in range(2):
            r = int((26 + 16 * j) * s)
            a0 = -40 if sg > 0 else 140
            cv2.ellipse(f, (int(cx), int(cy)), (r, r), 0, a0, a0 + 80, C((60, 110, 170)), max(2, int(4 * s)), cv2.LINE_AA)


def lota(f, x, y, s=1.0, rot=-35):
    """a steel LOTA (water pot) for the wedding hand-wash: round body, a neck and a lip, tipped by rot (deg); pours from the lip."""
    g = np.zeros((420, 420, 3), np.float32); m = np.zeros((420, 420), np.float32)
    cv2.circle(g, (210, 250), 120, C(STEEL), -1, cv2.LINE_AA); cv2.circle(m, (210, 250), 120, 1, -1, cv2.LINE_AA)
    cv2.rectangle(g, (160, 90), (260, 150), C(STEEL), -1); cv2.rectangle(m, (160, 90), (260, 150), 1, -1)
    cv2.ellipse(g, (250, 260), (70, 100), 0, -60, 90, C(STEEL_S), -1, cv2.LINE_AA)
    cv2.ellipse(g, (160, 220), (24, 60), 20, 0, 360, C(STEEL_H), -1, cv2.LINE_AA)
    cv2.circle(g, (210, 250), 120, C(INKC), 7, cv2.LINE_AA)
    cv2.line(g, (160, 150), (160, 90), C(INKC), 6, cv2.LINE_AA); cv2.line(g, (260, 150), (260, 90), C(INKC), 6, cv2.LINE_AA)
    cv2.ellipse(g, (210, 88), (70, 20), 0, 0, 360, C(STEEL_H), -1, cv2.LINE_AA); cv2.ellipse(m, (210, 88), (70, 20), 0, 0, 360, 1, -1, cv2.LINE_AA)
    cv2.ellipse(g, (210, 88), (70, 20), 0, 0, 360, C(INKC), 6, cv2.LINE_AA)
    M = cv2.getRotationMatrix2D((210, 210), -rot, s)
    M[0, 2] += x - 210; M[1, 2] += y - 210
    gw = cv2.warpAffine(g, M, (W, H)); mw = cv2.warpAffine(m, M, (W, H))[..., None]
    f[:] = f * (1 - mw) + gw * mw
