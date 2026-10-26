# ================= reusable prop library from ep 09 (spicy): chili, capsaicin key-molecule, tongue, heat-alarm sensor, brain,
# teacup, medal, drink glasses, milk protein, bird, mouse, seeds, chili plant, padlock + key, fire_cone, flames_row, thermo, sweat =================
CHILI = (226, 30, 36); CHILI_D = (150, 8, 20); STEM = (60, 160, 60); STEM_D = (24, 100, 40)
CAPS = (255, 92, 40); CAPS_D = (190, 40, 20); NERVE = (255, 214, 70); NERVE_D = (200, 150, 20)
TONG = (246, 128, 146); TONG_D = (200, 74, 100); BRAIN = (255, 170, 190); BRAIN_D = (214, 106, 140)
MILK = (250, 250, 246); PROT = (120, 200, 255)


def _outline(im, allm, k=15, col=INK):
    m = Image.new("L", im.size, 0); allm(ImageDraw.Draw(m))
    im.paste(Image.new("RGBA", im.size, tuple(col) + (255,)), (0, 0), m.filter(ImageFilter.MaxFilter(k)))
    return m


def _masked(im, mask, fn):
    L_ = Image.new("RGBA", im.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L_))
    a = Image.fromarray(np.minimum(np.asarray(L_.getchannel("A")), np.asarray(mask)), "L"); L_.putalpha(a); im.alpha_composite(L_)


def _eyes(d, S, sc, pts, r=16, look=(0, 0), sly=False, happy=False):
    for (ex, ey) in pts:
        if happy:
            d.arc(S(ex - r, ey - r * 0.6, ex + r, ey + r), 200, 340, fill=INK + (255,), width=5 * sc); continue
        d.ellipse(S(ex - r, ey - r * 1.15, ex + r, ey + r * 1.15), fill=(255, 255, 255, 255), outline=INK + (255,), width=4 * sc)
        pr = r * 0.5; px, py = ex + look[0] * r * 0.4, ey + look[1] * r * 0.4 + 2
        d.ellipse(S(px - pr, py - pr, px + pr, py + pr), fill=INK + (255,))
        d.ellipse(S(px - pr * 0.4, py - pr * 0.8, px + pr * 0.1, py - pr * 0.3), fill=(255, 255, 255, 255))
        if sly: d.rectangle(S(ex - r - 3, ey - r * 1.2 - 3, ex + r + 3, ey - r * 0.25), fill=(0, 0, 0, 0))


# ---------------- chili pepper (vertical, stem up, tip curling down-left) ----------------
def chili_el(face=False, mood="n", bite=False):
    def mk():
        w, h, sc = 260, 520, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        def body(m):
            m.ellipse(S(52, 70, 212, 230), fill=255)
            m.polygon(S(56, 150, 210, 150, 196, 300, 150, 420, 90, 500, 70, 470, 96, 380, 70, 260), fill=255)
            m.ellipse(S(64, 440, 112, 506), fill=255)
        def stem(m):
            m.rounded_rectangle(S(118, 18, 146, 96), 12 * sc, fill=255)
            m.ellipse(S(70, 64, 194, 116), fill=255)
        _outline(im, lambda m: (body(m), stem(m)), 13)
        bm = Image.new("L", im.size, 0); body(ImageDraw.Draw(bm))
        shape_grad(im, body, (255, 80, 70), CHILI_D)
        _masked(im, bm, lambda q: q.line(S(92, 120, 84, 330), fill=(255, 210, 210, 170), width=16 * sc))
        _masked(im, bm, lambda q: q.ellipse(S(150, 120, 196, 200), fill=(120, 0, 10, 70)))
        shape_grad(im, stem, (110, 210, 100), STEM_D)
        if bite: d.ellipse(S(40, 400, 120, 470), fill=(0, 0, 0, 0))
        if face:
            _eyes(d, S, sc, [(108, 190), (162, 190)], 17, (0.3, 0), sly=(mood == "sly"), happy=(mood == "happy"))
            if mood == "angry":
                d.line(S(86, 156, 122, 170), fill=INK + (255,), width=7 * sc); d.line(S(184, 156, 148, 170), fill=INK + (255,), width=7 * sc)
            if mood == "happy": d.chord(S(110, 220, 160, 262), 0, 180, fill=(70, 14, 24, 255))
            elif mood == "sly": d.arc(S(110, 214, 166, 252), 10, 150, fill=INK + (255,), width=6 * sc)
            else: d.arc(S(112, 228, 158, 256), 200, 340, fill=INK + (255,), width=6 * sc)
        return _done(im, w, h)
    return gcache(("chili", face, mood, bite), mk)


def chili_side(sc_=0.42, bite=False):
    """chili lying sideways (held in Chubby's hand): rotate the vertical one."""
    return gcache(("chili_side", sc_, bite), lambda: _rot_el(scale_el(chili_el(bite=bite), sc_), -100))


def _rot_el(el, ang):
    pm, a = el; h, w = a.shape; D = int(math.hypot(w, h)) + 4
    M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, 1.0); M[0, 2] += D / 2 - w / 2; M[1, 2] += D / 2 - h / 2
    return cv2.warpAffine(pm, M, (D, D)), cv2.warpAffine(a, M, (D, D))


# ---------------- capsaicin = a little "key" molecule (ring head + zig-zag tail with key teeth) ----------------
def caps_el(mood="sly", look=(0, 0)):
    def mk():
        w, h, sc = 360, 170, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        cx, cy, R0 = 82, 85, 66
        hexa = [(cx + R0 * math.cos(math.radians(30 + 60 * i)), cy + R0 * math.sin(math.radians(30 + 60 * i))) for i in range(6)]
        tail = [(140, 85), (176, 66), (212, 85), (248, 66), (284, 85), (330, 85)]
        def allm(m):
            m.polygon(S(*sum(hexa, ())), fill=255)
            m.line(S(*sum(tail, ())), fill=255, width=26 * sc, joint="curve")
            for tx in (288, 318): m.rectangle(S(tx - 9, 85, tx + 9, 128), fill=255)
        _outline(im, allm, 13)
        shape_grad(im, lambda m: m.polygon(S(*sum(hexa, ())), fill=255), (255, 140, 70), CAPS_D)
        d.line(S(*sum(tail, ())), fill=CAPS + (255,), width=16 * sc, joint="curve")
        for tx in (288, 318): d.rectangle(S(tx - 5, 85, tx + 5, 122), fill=CAPS + (255,))
        d.ellipse(S(cx - 40, cy - 40, cx + 40, cy + 40), outline=(255, 210, 160, 255), width=4 * sc)
        _eyes(d, S, sc, [(cx - 22, cy - 6), (cx + 22, cy - 6)], 15, look, sly=(mood == "sly"), happy=(mood == "happy"))
        if mood == "sly": d.arc(S(cx - 22, cy + 6, cx + 24, cy + 34), 15, 160, fill=INK + (255,), width=5 * sc)
        elif mood == "happy": d.chord(S(cx - 20, cy + 10, cx + 20, cy + 36), 0, 180, fill=(70, 14, 24, 255))
        else: d.ellipse(S(cx - 8, cy + 14, cx + 8, cy + 32), fill=(70, 14, 24, 255))
        return _done(im, w, h)
    return gcache(("caps", mood, look), mk)


def caps(f, x, y, s, t, mood="sly", rot=0.0, op=1.0, look=(0, 0), wig=True):
    rot_comp(f, scale_el(caps_el(mood, look), s), x, y + (6 * math.sin(t * 7) if wig else 0), rot + (5 * math.sin(t * 5) if wig else 0), 1.0, op, 0.25)


# ---------------- tongue (top view) ----------------
def tongue_el():
    def mk():
        w, h, sc = 640, 780, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        def body(m):
            m.rounded_rectangle(S(40, 30, 600, 520), 130 * sc, fill=255); m.ellipse(S(40, 200, 600, 770), fill=255)
        _outline(im, body, 15)
        bm = Image.new("L", im.size, 0); body(ImageDraw.Draw(bm))
        shape_grad(im, body, (255, 160, 172), TONG_D)
        rng = np.random.default_rng(5)
        def pap(q):
            for _ in range(240):
                x, y = rng.uniform(60, 580), rng.uniform(50, 740)
                r = rng.uniform(4, 8); q.ellipse(S(x - r, y - r, x + r, y + r), fill=(255, 196, 206, 200))
        _masked(im, bm, pap)
        _masked(im, bm, lambda q: q.line(S(320, 80, 320, 600), fill=(190, 70, 96, 200), width=10 * sc))
        _masked(im, bm, lambda q: q.ellipse(S(110, 90, 260, 220), fill=(255, 255, 255, 60)))
        return _done(im, w, h)
    return gcache("tongue", mk)


# ---------------- heat alarm (siren dome with a keyhole) — the TRPV1 sensor, drawn simply ----------------
def alarm_el(ring=False, key_in=False):
    def mk():
        w, h, sc = 220, 240, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(20, 170, 200, 232), 16 * sc, fill=INK + (255,))
        shape_grad(im, lambda m: m.rounded_rectangle(S(28, 176, 192, 224), 12 * sc, fill=255), (120, 124, 140), (60, 62, 74))
        d.chord(S(34, 30, 186, 250), 180, 360, fill=INK + (255,))
        top = (255, 90, 80) if ring else (200, 40, 50); bot = (255, 220, 120) if ring else (120, 10, 20)
        shape_grad(im, lambda m: m.chord(S(42, 38, 178, 242), 180, 360, fill=255), top if not ring else (255, 250, 200), bot if not ring else (255, 60, 40))
        _ov(im, lambda q: q.ellipse(S(66, 62, 104, 110), fill=(255, 255, 255, 140)))
        # keyhole
        kc = (40, 10, 14, 255)
        d.ellipse(S(94, 98, 126, 130), fill=kc); d.polygon(S(100, 120, 120, 120, 128, 160, 92, 160), fill=kc)
        if key_in:
            d.rounded_rectangle(S(100, 104, 120, 156), 6 * sc, fill=CAPS + (255,), outline=INK + (255,), width=3 * sc)
        return _done(im, w, h)
    return gcache(("alarm", ring, key_in), mk)


def alarm(f, x, y, s, t, ring=0.0, key_in=False):
    """alarm at (x, y) (centre); ring 0..1 adds a glow, shake and sound-wave arcs."""
    sh = 6 * ring * math.sin(t * 60)
    if ring > 0.05: glow(f, x, y - 30 * s, 160 * s, (255, 90, 40), 0.55 * ring)
    rot_comp(f, scale_el(alarm_el(ring > 0.3, key_in), s), x + sh, y, 4 * ring * math.sin(t * 47), 1.0, 1.0, 0.2)
    if ring > 0.3:
        for j in range(3):
            ph = (t * 2.6 + j / 3) % 1.0; r_ = (90 + 140 * ph) * s; op = (1 - ph) * ring
            ov = f.copy()
            for sg in (-1, 1):
                cv2.ellipse(ov, (int(x), int(y - 40 * s)), (int(r_), int(r_)), 0, (200 if sg < 0 else -20) , (250 if sg < 0 else 30), C((255, 240, 120)), int(9 * s), cv2.LINE_AA)
            f[:] = f * (1 - op) + ov * op


# ---------------- brain (side view), optional face ----------------
def brain_el(face=False, mood="n", alarm_lit=False):
    def mk():
        w, h, sc = 420, 340, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        lobes = [(30, 70, 220, 240), (120, 30, 300, 200), (200, 60, 390, 250), (60, 150, 260, 320), (190, 150, 380, 310)]
        def body(m):
            for b in lobes: m.ellipse(S(*b), fill=255)
        _outline(im, body, 15)
        bm = Image.new("L", im.size, 0); body(ImageDraw.Draw(bm))
        shape_grad(im, body, (255, 196, 210) if not alarm_lit else (255, 150, 120), BRAIN_D if not alarm_lit else (230, 60, 50))
        def folds(q):
            for (a0, b0, a1, b1, st, en) in ((70, 90, 190, 190, 200, 340), (150, 50, 280, 160, 190, 330), (220, 90, 350, 210, 200, 350),
                                             (90, 190, 220, 290, 190, 320), (210, 180, 340, 290, 200, 340), (120, 120, 250, 230, 10, 170)):
                q.arc(S(a0, b0, a1, b1), st, en, fill=(180, 70, 110, 255), width=6 * sc)
        _masked(im, bm, folds)
        _masked(im, bm, lambda q: q.ellipse(S(110, 50, 200, 110), fill=(255, 255, 255, 90)))
        if face:
            _eyes(d, S, sc, [(170, 170), (250, 170)], 22, (0, 0))
            if mood == "shout":
                d.ellipse(S(180, 210, 240, 280), fill=(70, 14, 24, 255)); d.ellipse(S(194, 246, 226, 276), fill=(236, 90, 110, 255))
            elif mood == "worried":
                d.arc(S(180, 220, 240, 260), 200, 340, fill=INK + (255,), width=6 * sc)
            else:
                d.arc(S(180, 200, 240, 240), 20, 160, fill=INK + (255,), width=6 * sc)
        return _done(im, w, h)
    return gcache(("brain", face, mood, alarm_lit), mk)


# ---------------- teacup with tea ----------------
def teacup_el():
    def mk():
        w, h, sc = 300, 220, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(10, 170, 290, 214), fill=INK + (255,)); d.ellipse(S(18, 174, 282, 206), fill=(240, 240, 246, 255))
        d.arc(S(196, 70, 270, 150), 270, 90, fill=INK + (255,), width=16 * sc); d.arc(S(196, 70, 270, 150), 270, 90, fill=(255, 255, 255, 255), width=8 * sc)
        def cup(m): m.chord(S(40, -10, 230, 190), 0, 180, fill=255); m.rectangle(S(40, 30, 230, 92), fill=255)
        _outline(im, cup, 11)
        shape_grad(im, cup, (255, 255, 255), (200, 210, 230))
        d.ellipse(S(48, 22, 222, 52), fill=INK + (255,)); d.ellipse(S(52, 25, 218, 49), fill=(160, 90, 40, 255))
        d.rectangle(S(40, 96, 230, 116), fill=(60, 170, 200, 255))
        return _done(im, w, h)
    return gcache("teacup", mk)


# ---------------- medal (generic gold medal, no logo) ----------------
def medal_el(text="2021"):
    def mk():
        w, h, sc = 300, 420, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.polygon(S(80, 0, 140, 0, 170, 170, 120, 170), fill=(40, 90, 200, 255)); d.polygon(S(160, 0, 220, 0, 180, 170, 130, 170), fill=(220, 40, 50, 255))
        d.ellipse(S(30, 140, 270, 380), fill=INK + (255,))
        shape_grad(im, lambda m: m.ellipse(S(38, 148, 262, 372), fill=255), (255, 226, 120), (200, 140, 30))
        d.ellipse(S(66, 176, 234, 344), outline=(170, 110, 20, 255), width=5 * sc)
        for i in range(9):
            a = math.radians(200 + i * 17); a2 = math.radians(-20 - i * 17)
            for aa in (a, a2):
                x_, y_ = 150 + 70 * math.cos(aa), 260 + 70 * math.sin(aa)
                d.ellipse(S(x_ - 9, y_ - 5, x_ + 9, y_ + 5), fill=(160, 110, 20, 255))
        d.text((150 * sc, 262 * sc), text, font=font(F_BLACK, 50 * sc), fill=(120, 70, 10, 255), anchor="mm")
        _ov(im, lambda q: q.ellipse(S(70, 170, 130, 220), fill=(255, 255, 255, 120)))
        return _done(im, w, h)
    return gcache(("medal", text), mk)


# ---------------- drink glasses (generic, no brands) ----------------
DRINKS = {"water": ((170, 220, 255), (110, 180, 245), False, 0), "cola": ((120, 60, 30), (60, 24, 10), True, 0),
          "sweet": ((255, 70, 110), (200, 20, 70), False, 0), "seltzer": ((210, 240, 255), (160, 210, 240), True, 0),
          "beer": ((255, 196, 60), (220, 140, 20), True, 1), "skim": ((250, 252, 255), (210, 220, 236), False, 0),
          "whole": ((255, 252, 240), (236, 226, 200), False, 0)}


def drink_el(kind, level=0.8):
    level = round(level * 10) / 10
    def mk():
        w, h, sc = 180, 300, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        top, bot, fizz, foam = DRINKS[kind]
        glass = lambda m: m.polygon(S(14, 10, 166, 10, 146, 290, 34, 290), fill=255)
        _outline(im, glass, 11)
        shape_grad(im, glass, (236, 246, 255), (200, 220, 240))
        y0 = 290 - 270 * level
        gm = Image.new("L", im.size, 0); glass(ImageDraw.Draw(gm))
        _masked(im, gm, lambda q: q.rectangle(S(0, y0, 180, 300), fill=top + (255,)))
        _masked(im, gm, lambda q: q.rectangle(S(0, (y0 + 290) / 2, 180, 300), fill=bot + (150,)))
        if foam: _masked(im, gm, lambda q: q.rectangle(S(0, y0 - 26, 180, y0 + 6), fill=(255, 250, 236, 255)))
        if fizz:
            rng = np.random.default_rng(3)
            _masked(im, gm, lambda q: [q.ellipse(S(x - 5, y - 5, x + 5, y + 5), outline=(255, 255, 255, 220), width=2 * sc)
                                       for x, y in zip(rng.uniform(40, 140, 12), rng.uniform(y0 + 10, 280, 12))])
        _masked(im, gm, lambda q: q.line(S(36, 30, 48, 270), fill=(255, 255, 255, 150), width=10 * sc))
        return _done(im, w, h)
    return gcache(("drink", kind, level), mk)


# ---------------- milk protein helper (little white blob with arms) ----------------
def protein_el(happy=True):
    def mk():
        w, h, sc = 150, 150, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        def body(m):
            for (x, y, r) in ((60, 70, 44), (95, 64, 38), (80, 98, 40)): m.ellipse(S(x - r, y - r, x + r, y + r), fill=255)
        _outline(im, body, 11)
        shape_grad(im, body, (255, 255, 255), (200, 225, 245))
        _eyes(d, S, sc, [(64, 68), (96, 68)], 11, (0.3, 0), happy=False)
        d.chord(S(66, 84, 96, 104), 0, 180, fill=(70, 14, 24, 255))
        return _done(im, w, h)
    return gcache(("prot", happy), mk)


# ---------------- bird (side view, facing right) ----------------
def bird_el(flap=0, beak_open=False, happy=True):
    def mk():
        w, h, sc = 300, 240, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        body = lambda m: (m.ellipse(S(40, 70, 220, 210), fill=255), m.ellipse(S(150, 40, 250, 140), fill=255), m.polygon(S(50, 130, 4, 110, 10, 170, 70, 170), fill=255))
        beak = [(240, 82, 296, 96, 240, 108)] if not beak_open else [(240, 78, 294, 76, 244, 94), (240, 100, 290, 116, 242, 110)]
        def allm(m):
            body(m)
            for b in beak: m.polygon(S(*b), fill=255)
        _outline(im, allm, 11)
        shape_grad(im, body, (90, 170, 240), (30, 90, 180))
        _ov(im, lambda q: q.ellipse(S(80, 130, 200, 205), fill=(255, 240, 210, 220)))
        for b in beak: d.polygon(S(*b), fill=(255, 170, 30, 255))
        _eyes(d, S, sc, [(212, 78)], 14, (0.4, 0), happy=happy and not beak_open)
        wy = {0: (60, 120, 170, 160), 1: (60, 40, 170, 140), 2: (70, 120, 170, 210)}[flap]
        d.chord(S(*wy), 0, 360, fill=INK + (255,)); d.chord(S(wy[0] + 6, wy[1] + 6, wy[2] - 6, wy[3] - 6), 0, 360, fill=(50, 120, 210, 255))
        d.line(S(120, 205, 110, 236), fill=(255, 150, 30, 255), width=5 * sc); d.line(S(150, 205, 156, 236), fill=(255, 150, 30, 255), width=5 * sc)
        return _done(im, w, h)
    return gcache(("bird", flap, beak_open, happy), mk)


# ---------------- mouse (side view, facing left) ----------------
def mouse_el(chew=False, scared=False):
    def mk():
        w, h, sc = 300, 200, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.arc(S(200, 40, 300, 190), 180, 320, fill=INK + (255,), width=6 * sc)
        body = lambda m: (m.ellipse(S(70, 60, 250, 190), fill=255), m.polygon(S(90, 90, 10, 140, 90, 170), fill=255))
        _outline(im, lambda m: (body(m), m.ellipse(S(80, 20, 150, 90), fill=255)), 11)
        shape_grad(im, body, (190, 190, 200), (120, 120, 136))
        d.ellipse(S(86, 26, 144, 84), fill=(160, 160, 172, 255)); d.ellipse(S(98, 38, 132, 72), fill=(255, 170, 190, 255))
        d.ellipse(S(2, 130, 22, 150), fill=(255, 120, 150, 255))
        _eyes(d, S, sc, [(70, 116)], 12 if not scared else 15, (-0.4, 0))
        for k in (-8, 6): d.line(S(20, 140 + k, -10, 132 + k * 2), fill=INK + (255,), width=2 * sc)
        if chew: d.rectangle(S(24, 150, 36, 166), fill=(255, 255, 255, 255), outline=INK + (255,), width=2 * sc)
        return _done(im, w, h)
    return gcache(("mouse", chew, scared), mk)


def seeds(f, pts, s=1.0, op=1.0):
    g = f if op >= 0.999 else f.copy()
    for (x, y) in pts:
        cv2.ellipse(g, (int(x), int(y)), (int(14 * s), int(10 * s)), 30, 0, 360, C(INK), -1, cv2.LINE_AA)
        cv2.ellipse(g, (int(x), int(y)), (int(10 * s), int(7 * s)), 30, 0, 360, C((255, 236, 170)), -1, cv2.LINE_AA)
    if op < 0.999: f[:] = f * (1 - op) + g * op


# ---------------- chili plant (grows with k) ----------------
def plant(f, x, y, s, k, t):
    """chili plant with its base at (x, y); k 0..1 growth."""
    if k <= 0.02: return
    hh = 380 * s * eo(k)
    cv2.line(f, (int(x), int(y)), (int(x), int(y - hh)), C(INK), int(18 * s), cv2.LINE_AA)
    cv2.line(f, (int(x), int(y)), (int(x), int(y - hh)), C(STEM), int(10 * s), cv2.LINE_AA)
    for i, (fr, side) in enumerate(((0.35, -1), (0.55, 1), (0.75, -1), (0.92, 1))):
        if k < fr * 0.8: continue
        q = clamp((k - fr * 0.8) / 0.25); by = y - hh * fr; sw = math.sin(t * 2 + i) * 4
        cv2.ellipse(f, (int(x + side * 70 * s * q), int(by + sw)), (int(80 * s * q) + 1, int(30 * s * q) + 1), side * -20, 0, 360, C(INK), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(x + side * 70 * s * q), int(by + sw)), (int(72 * s * q) + 1, int(23 * s * q) + 1), side * -20, 0, 360, C((70, 190, 80)), -1, cv2.LINE_AA)
        if k > 0.7 and i % 2 == 0:
            pk = clamp((k - 0.7) / 0.3)
            rot_comp(f, scale_el(chili_el(), 0.32 * s * pk + 0.01), x - side * 60 * s, by + 70 * s, side * 10 + sw, 1.0, 1.0, 0.0)


# ---------------- padlock + key (for the "key in a lock" analogy) ----------------
def padlock_el(open_=False):
    def mk():
        w, h, sc = 260, 320, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        sy = 20 if open_ else 60
        d.arc(S(60, sy, 200, sy + 190), 180, 360, fill=INK + (255,), width=34 * sc); d.arc(S(60, sy, 200, sy + 190), 180, 360, fill=(170, 176, 190, 255), width=20 * sc)
        d.line(S(66, sy + 95, 66, 160), fill=INK + (255,), width=34 * sc); d.line(S(66, sy + 95, 66, 160), fill=(170, 176, 190, 255), width=20 * sc)
        if not open_:
            d.line(S(194, sy + 95, 194, 160), fill=INK + (255,), width=34 * sc); d.line(S(194, sy + 95, 194, 160), fill=(170, 176, 190, 255), width=20 * sc)
        d.rounded_rectangle(S(20, 150, 240, 312), 26 * sc, fill=INK + (255,))
        shape_grad(im, lambda m: m.rounded_rectangle(S(28, 158, 232, 304), 20 * sc, fill=255), (255, 214, 80), (214, 150, 20))
        d.ellipse(S(112, 196, 148, 232), fill=INK + (255,)); d.polygon(S(118, 222, 142, 222, 150, 272, 110, 272), fill=INK + (255,))
        return _done(im, w, h)
    return gcache(("padlock", open_), mk)


def key_el():
    def mk():
        w, h, sc = 300, 120, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        def allm(m):
            m.ellipse(S(8, 14, 100, 106), fill=255); m.rectangle(S(90, 48, 280, 72), fill=255)
            for tx in (230, 262): m.rectangle(S(tx - 10, 66, tx + 10, 100), fill=255)
        _outline(im, allm, 11)
        shape_grad(im, allm, (255, 226, 110), (210, 150, 30))
        d.ellipse(S(36, 42, 72, 78), fill=(0, 0, 0, 0))
        return _done(im, w, h)
    return gcache("key", mk)


# ---------------- fire breath: flame cone from (x, y) toward angle (deg, 0 = right, -90 = up) ----------------
def fire_cone(f, x, y, ang, L, w, t, op=1.0, seed=0):
    if L < 5 or op <= 0.01: return
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); vx, vy = -uy, ux
    ov = f.copy()
    for li, (col, fl, fw) in enumerate((((255, 70, 20), 1.0, 1.0), ((255, 160, 30), 0.78, 0.66), ((255, 240, 150), 0.5, 0.34))):
        P = []
        n = 9
        for i in range(n + 1):
            q = i / n; wob = math.sin(t * 31 + i * 1.7 + li + seed) * 0.12
            r_ = L * fl * q; half = w * fw * (0.25 + 0.75 * math.sin(math.pi * min(1, q * 1.15)) ** 0.7) * (1 + wob) / 2
            P.append((x + ux * r_ + vx * half, y + uy * r_ + vy * half))
        tipx, tipy = x + ux * L * fl * (1.08 + 0.06 * math.sin(t * 40 + li)), y + uy * L * fl * 1.08
        P2 = []
        for i in range(n, -1, -1):
            q = i / n; wob = math.sin(t * 29 + i * 2.1 + li + seed) * 0.12
            r_ = L * fl * q; half = w * fw * (0.25 + 0.75 * math.sin(math.pi * min(1, q * 1.15)) ** 0.7) * (1 + wob) / 2
            P2.append((x + ux * r_ - vx * half, y + uy * r_ - vy * half))
        poly = np.array(P + [(tipx, tipy)] + P2, np.int32)
        cv2.fillPoly(ov, [poly], C(col), cv2.LINE_AA)
    f[:] = f * (1 - op) + ov * op
    glow(f, x + ux * L * 0.5, y + uy * L * 0.5, 80 + L * 0.35, (255, 120, 30), 0.3 * op)


def flames_row(f, x, y, w, t, h_=150, op=1.0):
    ov = f.copy()
    for layer, (col, sc_) in enumerate((((255, 90, 20), 1.0), ((255, 170, 30), 0.72), ((255, 236, 120), 0.42))):
        for i in range(9):
            fx = x - w / 2 + (i + 0.5) * w / 9; hh = h_ * sc_ * (0.75 + 0.25 * math.sin(t * 13 + i * 1.7 + layer))
            bw = w / 9 * 0.75 * (0.6 + 0.4 * sc_)
            P = np.array([[fx - bw, y], [fx - bw * 0.5, y - hh * 0.5], [fx + 8 * math.sin(t * 9 + i), y - hh], [fx + bw * 0.5, y - hh * 0.5], [fx + bw, y]], np.int32)
            cv2.fillPoly(ov, [P], C(col), cv2.LINE_AA)
    f[:] = f * (1 - op) + ov * op


def thermo(f, x, y, k, h_=420, col=(230, 40, 40)):
    """thermometer with bulb at (x, y); k 0..1 fill."""
    cv2.rectangle(f, (int(x - 30), int(y - h_)), (int(x + 30), int(y)), C(INK), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), 56, C(INK), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - 20), int(y - h_ + 10)), (int(x + 20), int(y)), C((250, 250, 255)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), 46, C(col), -1, cv2.LINE_AA)
    top = y - 20 - (h_ - 40) * clamp(k)
    cv2.rectangle(f, (int(x - 12), int(top)), (int(x + 12), int(y)), C(col), -1, cv2.LINE_AA)
    for i in range(6): cv2.line(f, (int(x + 22), int(y - 60 - i * (h_ - 80) / 5)), (int(x + 40), int(y - 60 - i * (h_ - 80) / 5)), C(INK), 5, cv2.LINE_AA)


def sweat(f, x, y, t, n=3, s=1.0):
    for j in range(n):
        ph = (t * 1.4 + j / n) % 1.0
        px = x + (j - 1) * 70 * s; py = y + 80 * ph * s
        cv2.ellipse(f, (int(px), int(py)), (int(10 * s), int(15 * s)), 0, 0, 360, C(INK), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(px), int(py)), (int(7 * s), int(11 * s)), 0, 0, 360, C((140, 210, 255)), -1, cv2.LINE_AA)
