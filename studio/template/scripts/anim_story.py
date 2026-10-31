# ================= story kit (exec'd after anim_sets.py) — STORY.md signature beats + sets/props for YOUR MOVE episodes =================
# Signature beats (same look every episode = brand memory, STORY.md §2):
#   cold_open(f, "1996", "SEATTLE", "YOU: STUDENT, 21")         -> year · place · your role card (top-left, safe zone)
#   series_badge(f, "YOUR MOVE", "EP 1 · THE PEPSI JET")         -> series badge (top-right)
#   oops_beat(f, t, t0, x=540, y=760)                            -> the one "Oops." stamp per video (pop + tilt)
#   choice_card(f, "YOUR MOVE", "JET", "DROP", y=1380, t, t0)   -> end card: question + two choice pills
#   quote_card(f, "exaggerated adolescent fantasy", "Leonard v. PepsiCo (S.D.N.Y. 1999)", y=620)  -> real quotes only
# Sets added to set_view(): bedroom90s, schoolyard (dusk), courtroom. set_front(f, "courtroom", box, ...same camera as set_view...)
#   re-draws a part of the set OVER the cast (a judge behind the bench, a clerk behind a counter).  Props: jumpjet_el (generic jump-jet, no insignia),
# crt_tv_el (screen content element), mailbox_el, coupon_el, catalog_el.


def cold_open(f, year, place, role=None, op=1.0):
    hud_clock(f, year, place, role, op=op)


def series_badge(f, series="YOUR MOVE", title=None, x=760, y=330):
    part_badge(f, series, title, x=x, y=y)


def oops_beat(f, t, t0, x=540, y=760, size=150, col=(232, 36, 44)):
    k = clamp((t - t0) / 0.16)
    if k <= 0: return
    el = gcache(("oops", size, col), lambda: _oops_el(size, col))
    s = 1.6 - 0.6 * eback(k)
    rot_comp(f, el, x, y, -8 * eo(k), scale=s, op=min(1.0, k * 2))


def _oops_el(size, col):
    fn = font(F_ANTON, size); tw = fn.getlength("OOPS"); w, h = int(tw + 90), int(size * 1.55); sc = 2
    im = Image.new("RGBA", (w * sc, h * sc), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([8 * sc, 8 * sc, (w - 8) * sc, (h - 8) * sc], 22 * sc, fill=(255, 255, 255, 235), outline=tuple(col) + (255,), width=12 * sc)
    fn2 = font(F_ANTON, size * sc)
    d.text((w * sc / 2, h * sc / 2), "OOPS", font=fn2, fill=tuple(col) + (255,), anchor="mm")
    return el_from(im.resize((w, h), Image.LANCZOS))


def choice_card(f, question, a, b, y=1380, t=None, t0=None, col_a=(36, 186, 88), col_b=(226, 52, 52)):
    """YOUR MOVE end card: question line + two one-word choice pills side by side (inside the safe width)"""
    def mk():
        q = _stxt_el(question, 70, stroke=6); pa = _pill_el(a, col_a); pb = _pill_el(b, col_b); orr = _stxt_el("or", 52, stroke=5)
        gap = 26; row_w = pa.size[0] + orr.size[0] + pb.size[0] + 2 * gap; w = max(q.size[0], row_w) + 20
        h = q.size[1] + max(pa.size[1], pb.size[1]) + 10
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        im.alpha_composite(q, ((w - q.size[0]) // 2, 0))
        x = (w - row_w) // 2; yy = q.size[1] + 4
        im.alpha_composite(pa, (x, yy)); x += pa.size[0] + gap
        im.alpha_composite(orr, (x, yy + (pa.size[1] - orr.size[1]) // 2)); x += orr.size[0] + gap
        im.alpha_composite(pb, (x, yy))
        return el_from(im)
    el = gcache(("choice", question, a, b, col_a, col_b), mk); s = min(1.0, 860 / el[1].shape[1])
    if t is not None and t0 is not None:
        k = clamp((t - t0) / 0.22)
        if k <= 0: return
        s *= 0.8 + 0.2 * eback(k)
    comp(f, el, 540, y, scale=s)


def _pill_el(text, col):
    t = _stxt_el(text, 84); w, h = t.size[0] + 70, t.size[1] + 10
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, w + 3, h + 3], h // 2, fill=tuple(col) + (255,), outline=(255, 255, 255, 255), width=5)
    im.alpha_composite(t, (4 + 35, 4 + 5)); return im


def quote_card(f, text, source, y=620, t=None, t0=None, w=820):
    """dark card with a real quote (documents only) + source chip; centred, wraps to the safe width"""
    def mk():
        fq = font(F_PFI, 58); words = text.split(); lines, cur = [], ""
        for wd in words:
            nxt = (cur + " " + wd).strip()
            if fq.getlength(nxt) > w - 180 and cur: lines.append(cur); cur = wd
            else: cur = nxt
        lines.append(cur)
        lh = 74; h = 96 + lh * len(lines) + 90
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w - 1, h - 1], 28, fill=(16, 16, 22, 228), outline=(255, 210, 90, 200), width=3)
        d.text((w // 2, 4), "“", font=font(F_PF9, 110), fill=(255, 206, 70, 255), anchor="mt")
        for i, ln in enumerate(lines):
            d.text((w // 2, 96 + i * lh), ln, font=fq, fill=(255, 255, 255, 255), anchor="mt")
        fs = font(F_SEMI, 28); sw = int(fs.getlength(source)) + 36
        d.rounded_rectangle([(w - sw) // 2, h - 66, (w + sw) // 2, h - 22], 20, fill=(255, 206, 70, 255))
        d.text((w // 2, h - 44), source, font=fs, fill=(20, 20, 24, 255), anchor="mm")
        return el_from(im)
    el = gcache(("quote", text, source, w), mk); s = 1.0; op = 1.0
    if t is not None and t0 is not None:
        k = clamp((t - t0) / 0.25)
        if k <= 0: return
        s = 0.92 + 0.08 * eo(k); op = k
    comp(f, el, 540, y, scale=s, op=op)


def set_front(f, name, box, t=0.0, zoom=1.0, cx=W / 2, cy=H / 2, blur=0.0, drift=4.0, feather=3):
    """foreground occluder: paste the set's pixels inside box=(x0, y0, x1, y1) (frame coords, same camera args as set_view)
    over whatever was drawn, so characters stand BEHIND furniture"""
    g = set_view(name, t, zoom, cx, cy, blur, drift)
    x0, y0, x1, y1 = (int(v) for v in box); m = np.zeros((H, W), np.float32); m[max(0, y0):y1, max(0, x0):x1] = 1
    if feather: m = cv2.GaussianBlur(m, (0, 0), feather)
    f[:] = f * (1 - m[..., None]) + g * m[..., None]


# ---------------- props ----------------
def jumpjet_el(w=900, nozzle=90):
    """generic side-view jump-jet facing right (no insignia, no markings), lit like the cast. nozzle: 0 = back, 90 = down"""
    def mk():
        s = w / 900.0; Wd, Hd = int(940 * s), int(420 * s)
        fg = _Fig(0, 0, Wd, Hd, s=s, clip=False)
        U = lambda *v: [x * s for x in v]; P = lambda pts: [(x * s, y * s) for x, y in pts]
        grey, dark, glass = (150, 160, 172), (92, 100, 112), (90, 150, 210)
        fg.poly(P([(130, 150), (230, 120), (300, 40), (340, 40), (330, 140)]), dark, r0=10 * s)                     # tail fin
        fg.poly(P([(90, 205), (300, 180), (300, 210), (120, 236)]), dark, r0=8 * s)                                   # tailplane
        fg.poly(P([(60, 200), (130, 170), (520, 150), (760, 158), (880, 200), (760, 240), (520, 262), (130, 240)]), grey, r0=46 * s, gloss=0.25)  # fuselage
        fg.poly(P([(700, 150), (740, 120), (800, 128), (840, 170), (760, 172)]), glass, r0=26 * s, gloss=0.9, soft=0.25)   # canopy
        fg.ellipse(U(560, 205), U(46, 40), (40, 44, 52), r0=12 * s)                                                   # intake
        fg.poly(P([(330, 168), (620, 168), (560, 190), (350, 190)]), dark, r0=8 * s)                                  # shoulder wing (edge-on)
        fg.poly(P([(380, 176), (470, 176), (300, 110), (250, 110)]), (120, 130, 142), r0=10 * s)                      # wing sweep (far side)
        for nx in (500, 420):                                                                                          # swivel nozzles
            ca, sa = math.cos(math.radians(nozzle)), math.sin(math.radians(nozzle))
            p0 = (nx * s, 245 * s); p1 = (nx * s - ca * 70 * s, 245 * s + sa * 70 * s)
            fg.capsule(p0, p1, 46 * s, (70, 74, 84), r0=18 * s, gloss=0.3)
        rgb, a = fg.shade()
        im = Image.fromarray((np.dstack([rgb, a]) * 255).astype(np.uint8), "RGBA")
        return el_from(im)
    return gcache(("jumpjet", w, nozzle, _LID[0]), mk)


def crt_tv_el(w=560, screen=None, glow=(150, 200, 255)):
    """chunky 1990s CRT television on a stand; screen = element drawn into the (curved) screen area"""
    def mk():
        s = w / 560.0; Wd, Hd = int(560 * s), int(500 * s)
        fg = _Fig(0, 0, Wd, Hd, s=s, clip=False)
        fg.rrect(0, 0, Wd, int(430 * s), 46 * s, (196, 186, 170), r0=40 * s, gloss=0.15)        # beige case
        fg.rrect(int(40 * s), int(40 * s), int(430 * s), int(370 * s), 60 * s, (30, 34, 40), r0=14 * s)   # screen bezel
        fg.ellipse((480 * s, 120 * s), (22 * s, 22 * s), (120, 112, 100), r0=10 * s)          # knobs
        fg.ellipse((480 * s, 200 * s), (22 * s, 22 * s), (120, 112, 100), r0=10 * s)
        for k in range(6): fg.rrect(int(452 * s), int((260 + k * 16) * s), int(510 * s), int((268 + k * 16) * s), 3 * s, (150, 142, 128), r0=2 * s, ow=0)
        fg.rrect(int(160 * s), int(430 * s), int(400 * s), int(500 * s), 10 * s, (70, 66, 62), r0=8 * s)   # stand
        rgb, a = fg.shade()
        im = Image.fromarray((np.dstack([rgb, a]) * 255).astype(np.uint8), "RGBA")
        return im
    base = gcache(("crt", w), mk)
    im = base.copy(); s = w / 560.0
    sx0, sy0, sx1, sy1 = int(60 * s), int(60 * s), int(410 * s), int(350 * s)
    scr = Image.new("RGBA", (sx1 - sx0, sy1 - sy0), tuple(int(v * 0.35) for v in glow) + (255,))
    if screen is not None:
        pm, a = screen
        rgba = np.dstack([np.where(a[..., None] > 1e-4, pm / np.maximum(a[..., None], 1e-4), 0), a])
        sim = Image.fromarray((np.clip(rgba, 0, 1) * 255).astype(np.uint8), "RGBA")
        sim.thumbnail((scr.size[0], scr.size[1]), Image.LANCZOS)
        scr.alpha_composite(sim, ((scr.size[0] - sim.size[0]) // 2, (scr.size[1] - sim.size[1]) // 2))
    sa = np.asarray(scr, np.float32) / 255
    yy = np.linspace(0, 1, scr.size[1])[:, None]; xx = np.linspace(0, 1, scr.size[0])[None, :]
    vig = 1 - 0.45 * ((xx - 0.5) ** 2 + (yy - 0.5) ** 2) * 2.2
    lines = 0.92 + 0.08 * (np.arange(scr.size[1]) % 4 < 2)[:, None]
    sa[..., :3] = np.clip(sa[..., :3] * vig[..., None] * lines[..., None] + 0.12 * np.exp(-((xx - 0.3) ** 2 + (yy - 0.25) ** 2) / 0.02)[..., None], 0, 1)
    scr = Image.fromarray((sa * 255).astype(np.uint8), "RGBA")
    m = Image.new("L", scr.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, scr.size[0] - 1, scr.size[1] - 1], int(48 * s), fill=255)
    im.paste(scr, (sx0, sy0), m)
    return el_from(im)


def mailbox_el(w=260):
    def mk():
        s = w / 260.0; Wd, Hd = int(260 * s), int(460 * s)
        fg = _Fig(0, 0, Wd, Hd, s=s, clip=False)
        fg.rrect(int(100 * s), int(250 * s), int(160 * s), int(460 * s), 8 * s, (60, 64, 70), r0=14 * s)
        fg.rrect(0, int(40 * s), Wd, int(270 * s), 110 * s, (54, 120, 96), r0=60 * s, gloss=0.3, soft=0.2)
        fg.rrect(int(40 * s), int(110 * s), int(220 * s), int(140 * s), 10 * s, (30, 40, 36), r0=6 * s, ao=0)
        rgb, a = fg.shade()
        im = Image.fromarray((np.dstack([rgb, a]) * 255).astype(np.uint8), "RGBA"); d = ImageDraw.Draw(im)
        d.text((Wd // 2, int(205 * s)), "MAIL", font=font(F_ANTON, int(48 * s)), fill=(246, 240, 220, 255), anchor="mm")
        return el_from(im)
    return gcache(("mailbox", w), mk)


def coupon_el(text="FREE COLA", w=360, col=(238, 70, 60)):
    def mk():
        h = int(w * 0.5); sc = 2; im = Image.new("RGBA", (w * sc, h * sc), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([4 * sc, 4 * sc, (w - 4) * sc, (h - 4) * sc], 18 * sc, fill=(252, 246, 228, 255), outline=(60, 50, 40, 255), width=4 * sc)
        for x in range(16, w - 16, 18): d.line([(x * sc, 18 * sc), ((x + 9) * sc, 18 * sc)], fill=tuple(col) + (255,), width=3 * sc)
        for x in range(16, w - 16, 18): d.line([(x * sc, (h - 18) * sc), ((x + 9) * sc, (h - 18) * sc)], fill=tuple(col) + (255,), width=3 * sc)
        d.text((w * sc // 2, int(h * 0.45) * sc), text, font=font(F_ANTON, 64 * sc), fill=tuple(col) + (255,), anchor="mm")
        d.text((w * sc // 2, int(h * 0.75) * sc), "COUPON", font=font(F_SEMI, 26 * sc), fill=(60, 50, 40, 255), anchor="mm")
        return el_from(im.resize((w, h), Image.LANCZOS))
    return gcache(("coupon", text, w, col), mk)


def catalog_el(title="PRIZE CATALOG", w=420, col=(40, 90, 170)):
    def mk():
        h = int(w * 1.3); sc = 2; im = Image.new("RGBA", (w * sc, h * sc), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([6 * sc, 6 * sc, (w - 6) * sc, (h - 6) * sc], 14 * sc, fill=(250, 248, 240, 255), outline=(40, 40, 50, 255), width=4 * sc)
        d.rectangle([6 * sc, 6 * sc, (w - 6) * sc, int(h * 0.24) * sc], fill=tuple(col) + (255,))
        d.text((w * sc // 2, int(h * 0.12) * sc), title, font=font(F_ANTON, 50 * sc), fill=(255, 255, 255, 255), anchor="mm")
        for i, (lab, pts) in enumerate((("T-SHIRT", "75"), ("SHADES", "175"), ("JACKET", "1450"))):
            y = int(h * (0.32 + i * 0.17))
            d.rounded_rectangle([24 * sc, y * sc, 120 * sc, (y + 76) * sc], 10 * sc, fill=(220, 226, 236, 255))
            d.text((140 * sc, (y + 22) * sc), lab, font=font(F_XB, 30 * sc), fill=(30, 30, 40, 255), anchor="lm")
            d.text((140 * sc, (y + 56) * sc), "PTS", font=font(F_SEMI, 22 * sc), fill=(90, 90, 100, 255), anchor="lm")
        for k in range(5): d.line([(24 * sc, (int(h * 0.86) + k * 9) * sc), ((w - 24) * sc, (int(h * 0.86) + k * 9) * sc)], fill=(150, 150, 160, 255), width=2 * sc)
        return el_from(im.resize((w, h), Image.LANCZOS))
    return gcache(("catalog", title, w, col), mk)


# ---------------- sets ----------------
def _bedroom90s():
    f = np.zeros((H, W, 3), np.float32); y0 = 1300
    _srect(f, 0, 0, W, y0, (70, 92, 140), (52, 66, 108))                                   # dusky blue walls
    for x in range(0, W, 90): cv2.line(f, (x, 0), (x, y0), _scv((62, 82, 128)), 3, cv2.LINE_AA)
    _swindow(f, 640, 180, 1000, 640, frame=(236, 230, 220), glass_top=(40, 50, 110), glass_bot=(230, 130, 110))   # dusk window
    for (x0, y0p, x1, y1, c) in ((70, 160, 330, 520, (236, 180, 60)), (360, 230, 560, 470, (60, 190, 180))):   # posters (abstract)
        _srect(f, x0, y0p, x1, y1, tuple(min(255, int(v * 1.1)) for v in c), tuple(int(v * 0.8) for v in c), (30, 26, 30), 3)
        cv2.circle(f, ((x0 + x1) // 2, (y0p + y1) // 2), (x1 - x0) // 4, _scv((250, 240, 220)), 6, cv2.LINE_AA)
    _srect(f, 0, 1000, 520, 1300, (230, 90, 80), (190, 60, 60), (40, 20, 24), 3)          # bed (side)
    _srect(f, 0, 950, 520, 1010, (246, 240, 230), (220, 214, 204), (40, 30, 30), 2)       # pillow line
    _srect(f, 620, 900, 1080, 1300, (150, 104, 70), (110, 74, 50), (40, 26, 20), 3)       # dresser (TV stands on it)
    for yy in (980, 1080, 1180): cv2.line(f, (640, yy), (1060, yy), _scv((80, 54, 38)), 3, cv2.LINE_AA)
    f[y0:] = 0; _sfloor(f, y0, 540, (120, 96, 130), (80, 62, 92), tile=False, planks=False, line_col=(70, 56, 80))
    _sglow(f, 820, 420, 360, (255, 160, 120), 0.35); _sglow(f, 300, 900, 500, (255, 210, 150), 0.18)
    _atmos(f, "bedroom90s")
    f *= (0.9 + 0.16 * np.exp(-(((_xx - W / 2) / 700) ** 2 + ((_yy - 800) / 900) ** 2)))[..., None]
    return np.clip(f, 0, 1).astype(np.float32)


def _schoolyard():
    f = np.zeros((H, W, 3), np.float32); y0 = 1240
    k = np.clip(_yy / 900, 0, 1)[..., None]
    f[:] = _mix(_c((60, 56, 120)), _c((255, 160, 96)), k ** 1.2)                         # dusk sky
    _sglow(f, 900, 700, 420, (255, 200, 130), 0.6)
    _srect(f, -20, 520, W + 20, y0, (180, 92, 70), (140, 66, 52), (60, 30, 24), 3)        # brick school
    for y in range(540, y0, 30):
        off = 0 if ((y - 540) // 30) % 2 == 0 else 36
        cv2.line(f, (0, y), (W, y), _scv((120, 56, 44)), 2, cv2.LINE_AA)
        for x in range(off, W, 72): cv2.line(f, (x, y), (x, y + 30), _scv((120, 56, 44)), 2, cv2.LINE_AA)
    _srect(f, -20, 470, W + 20, 540, (226, 214, 196), (196, 182, 164), (60, 50, 40), 3)    # cornice
    for x0 in (40, 300, 720):                                                               # windows (warm lit)
        for yy in (620, 900):
            _swindow(f, x0, yy, x0 + 200, yy + 200, frame=(236, 230, 220), glass_top=(255, 214, 140), glass_bot=(230, 160, 90))
    _srect(f, 470, 900, 650, y0, (90, 60, 50), (70, 44, 36), (30, 20, 16), 3)              # doors
    _srect(f, 400, 846, 720, 912, (226, 214, 196), (196, 182, 164), (60, 50, 40), 2)
    fs = font(F_ANTON, 44); im = Image.new("L", (300, 60), 0); ImageDraw.Draw(im).text((150, 30), "HIGH SCHOOL", font=fs, fill=255, anchor="mm")
    m = np.asarray(im, np.float32) / 255; f[849:909, 410:710] = f[849:909, 410:710] * (1 - m[..., None]) + _c((60, 50, 40)) * m[..., None]
    cv2.line(f, (980, 300), (980, y0), _scv((200, 204, 210)), 8, cv2.LINE_AA)               # flagpole (no flag)
    f[y0:] = 0; _sfloor(f, y0, 540, (120, 116, 124), (70, 68, 76), tile=False, line_col=(90, 88, 96))
    for x in range(120, W, 260): cv2.line(f, (x, y0 + 300), (x + 120, y0 + 300), _scv((240, 220, 120)), 8, cv2.LINE_AA)   # yard lines
    for i in range(7):                                                                      # bike rack
        cx = 60 + i * 56; cv2.ellipse(f, (cx, y0 + 30), (24, 60), 0, 180, 360, _scv((200, 204, 210)), 6, cv2.LINE_AA)
    _atmos(f, "schoolyard")
    return np.clip(f, 0, 1).astype(np.float32)


def _courtroom():
    f = np.zeros((H, W, 3), np.float32); y0 = 1280
    _srect(f, 0, 0, W, y0, (150, 98, 60), (112, 70, 42))                                   # wood panels
    for x in range(0, W, 180):
        _srect(f, x + 14, 80, x + 166, 520, (162, 108, 68), (128, 82, 50), (70, 42, 26), 2)
        _srect(f, x + 14, 560, x + 166, 900, (162, 108, 68), (128, 82, 50), (70, 42, 26), 2)
    _swindow(f, 60, 120, 300, 640, frame=(230, 220, 200), glass_top=(120, 110, 170), glass_bot=(250, 170, 110))
    _swindow(f, 780, 120, 1020, 640, frame=(230, 220, 200), glass_top=(120, 110, 170), glass_bot=(250, 170, 110))
    cv2.circle(f, (540, 330), 120, _scv((220, 180, 90)), -1, cv2.LINE_AA); cv2.circle(f, (540, 330), 120, _scv((90, 60, 30)), 6, cv2.LINE_AA)   # blank emblem
    cv2.circle(f, (540, 330), 86, _scv((240, 206, 120)), 4, cv2.LINE_AA)
    _srect(f, 180, 640, 900, 1000, (120, 74, 44), (88, 52, 30), (40, 24, 14), 4)            # judge's bench
    _srect(f, 160, 610, 920, 660, (150, 96, 58), (120, 74, 44), (40, 24, 14), 3)
    _srect(f, 0, 1060, W, 1100, (140, 90, 54), (110, 70, 42), (40, 24, 14), 3)              # rail
    for x in range(20, W, 60): cv2.line(f, (x, 1100), (x, y0), _scv((110, 70, 42)), 10, cv2.LINE_AA)
    f[y0:] = 0; _sfloor(f, y0, 540, (150, 60, 50), (100, 40, 34), tile=False, line_col=(90, 36, 30))   # red carpet floor
    _sglow(f, 180, 380, 420, (255, 190, 120), 0.4); _sglow(f, 900, 380, 420, (255, 190, 120), 0.4)
    _atmos(f, "courtroom")
    f *= (0.9 + 0.16 * np.exp(-(((_xx - W / 2) / 700) ** 2 + ((_yy - 800) / 900) ** 2)))[..., None]
    return np.clip(f, 0, 1).astype(np.float32)


_STORY_SETS = {"bedroom90s": _bedroom90s, "schoolyard": _schoolyard, "courtroom": _courtroom}
_FLOOR.update(bedroom90s=1300, schoolyard=1240, courtroom=1280)
SET_LIGHT.update(bedroom90s="warm", schoolyard="dusk", courtroom="warm")
SETS = tuple(_FLOOR)
_set_base_sets = _set_base


def _set_base(name):   # noqa: F811 — story sets first, then the library in anim_sets.py
    if name in _STORY_SETS: return _STORY_SETS[name]()
    return _set_base_sets(name)
