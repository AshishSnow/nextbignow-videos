# ================= props for "Planet Fitness: $15 a month" (generic gym props, no logos / trade dress) =================
STEEL = (150, 158, 172); RUBBER = (44, 46, 56); TEALG = (0, 170, 160); GLASSB = (170, 220, 255)


def dumbbell_el(col=RUBBER, w=520, h=200):
    """generic hex dumbbell"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(20, h - 40, w - 10, h - 6), 16 * sc, fill=(0, 0, 0, 50)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(130, h / 2 - 22, w - 130, h / 2 + 22), 18 * sc, fill=255), (230, 234, 240), (130, 136, 150))
        for x0 in (10, w - 150):
            shape_grad(im, lambda m, x0=x0: m.rounded_rectangle(S(x0, 14, x0 + 140, h - 30), 30 * sc, fill=255),
                       tuple(min(255, c + 60) for c in col), col)
            d.rounded_rectangle(S(x0, 14, x0 + 140, h - 30), 30 * sc, outline=INK + (255,), width=5 * sc)
            _ov(im, lambda q, x0=x0: q.rounded_rectangle(S(x0 + 18, 30, x0 + 40, h - 50), 10 * sc, fill=(255, 255, 255, 70)))
        for k_ in range(5): d.line(S(190 + k_ * 30, h / 2 - 18, 200 + k_ * 30, h / 2 + 18), fill=(110, 116, 130, 255), width=3 * sc)
        return _done(im, w, h)
    return gcache(("dumbbell", col, w, h), mk)


def gym_el(w=640, h=560, lit=True, label="GYM"):
    """generic gym building: big glass front, flat roof sign with a dumbbell icon + text, double doors"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(26, 120, w - 2, h - 2), 20 * sc, fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(10, 110, w - 20, h - 16), 20 * sc, fill=255), (250, 250, 252), (204, 210, 222))
        d.rounded_rectangle(S(10, 110, w - 20, h - 16), 20 * sc, outline=INK + (255,), width=6 * sc)
        # roof sign
        d.rounded_rectangle(S(90, 10, w - 100, 120), 24 * sc, fill=INK + (255,))
        d.text(((w - 10) / 2 * sc + 50 * sc, 66 * sc), label, font=font(F_BLACK, 74 * sc), fill=(255, 255, 255, 255), anchor="mm")
        cx0 = (w - 10) / 2 - 110
        d.rounded_rectangle(S(cx0 - 50, 60, cx0 + 50, 72), 5 * sc, fill=(255, 255, 255, 255))
        for dx in (-50, 50): d.rounded_rectangle(S(cx0 + dx - 12, 42, cx0 + dx + 12, 90), 6 * sc, fill=(255, 92, 40, 255))
        # windows
        wc = (255, 236, 160) if lit else GLASSB
        for i in range(3):
            x = 50 + i * ((w - 120) / 3)
            d.rounded_rectangle(S(x, 160, x + (w - 160) / 3, 330), 10 * sc, fill=wc + (255,), outline=INK + (255,), width=4 * sc)
            _ov(im, lambda q, x=x: q.polygon(S(x + 14, 170, x + 50, 170, x + 20, 320, x + 14, 320), fill=(255, 255, 255, 110)))
        # doors
        dx0 = (w - 10) / 2
        d.rounded_rectangle(S(dx0 - 110, 360, dx0 + 110, h - 16), 8 * sc, fill=GLASSB + (255,), outline=INK + (255,), width=5 * sc)
        d.line(S(dx0, 360, dx0, h - 16), fill=INK + (255,), width=5 * sc)
        for xx in (dx0 - 22, dx0 + 22): d.line(S(xx, 430, xx, 480), fill=INK + (255,), width=6 * sc)
        return _done(im, w, h)
    return gcache(("gym", w, h, lit, label), mk)


def treadmill_el(w=560, h=420, webs=0.0):
    """side-view treadmill; webs 0..1 adds cobwebs + dust (unused machine)"""
    webs = round(webs, 2)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.ellipse(S(20, h - 50, w - 20, h - 10), fill=(0, 0, 0, 60)))
        # deck
        shape_grad(im, lambda m: m.rounded_rectangle(S(20, h - 120, w - 40, h - 50), 30 * sc, fill=255), (90, 96, 110), (40, 42, 52))
        d.rounded_rectangle(S(40, h - 128, w - 60, h - 108), 10 * sc, fill=(30, 30, 36, 255))
        # upright + console
        d.line(S(w - 110, h - 110, w - 160, 120), fill=(70, 74, 86, 255), width=22 * sc)
        d.line(S(w - 170, 150, w - 280, 170), fill=(70, 74, 86, 255), width=14 * sc)
        d.rounded_rectangle(S(w - 250, 70, w - 70, 160), 18 * sc, fill=(40, 44, 56, 255), outline=INK + (255,), width=4 * sc)
        d.rounded_rectangle(S(w - 230, 88, w - 90, 140), 8 * sc, fill=(40, 90, 120, 255) if webs < 0.5 else (60, 64, 74, 255))
        if webs < 0.5: d.text(((w - 160) * sc, 114 * sc), "0.0", font=font(F_BLACK, 34 * sc), fill=(120, 230, 255, 255), anchor="mm")
        if webs > 0:
            a = int(220 * webs)
            cx, cy = w - 250, 70
            for k_ in range(6):
                ang = math.radians(90 + k_ * 18); d.line(S(cx, cy, cx + 150 * math.cos(ang) * -1 + 0, cy + 150 * math.sin(ang)), fill=(255, 255, 255, a), width=2 * sc)
            for rr in (40, 80, 120):
                pts = [(cx - rr * math.cos(math.radians(90 + k_ * 18)), cy + rr * math.sin(math.radians(90 + k_ * 18))) for k_ in range(6)]
                d.line([(x * sc, y * sc) for x, y in pts], fill=(255, 255, 255, a), width=2 * sc)
            for k_ in range(26):
                x = 50 + (k_ * 37) % (w - 120); y = h - 126 + (k_ * 13) % 14
                d.ellipse(S(x, y, x + 6, y + 4), fill=(190, 180, 160, a))
        return _done(im, w, h)
    return gcache(("tread", w, h, webs), mk)


def report_el(lines=(), hi=-1, k_hi=1.0, w=640, h=760, title="ANNUAL REPORT", year="2025"):
    """generic annual report page: title band, quote lines; line `hi` gets a highlighter swipe (k_hi 0..1)"""
    k_hi = round(k_hi, 2)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rectangle(S(18, 20, w - 2, h - 2), fill=(0, 0, 0, 60)))
        d.rectangle(S(0, 0, w - 18, h - 20), fill=(255, 255, 255, 255))
        d.rectangle(S(0, 0, w - 18, 130), fill=(28, 52, 140, 255))
        d.text(((w - 18) / 2 * sc, 52 * sc), title, font=font(F_BLACK, 50 * sc), fill=(255, 255, 255, 255), anchor="mm")
        d.text(((w - 18) / 2 * sc, 104 * sc), year, font=font(F_BOLD, 32 * sc), fill=(255, 214, 92, 255), anchor="mm")
        y = 180
        for i in range(3):
            d.rounded_rectangle(S(50, y + i * 34, w - 70 - (i % 2) * 90, y + i * 34 + 14), 6 * sc, fill=(214, 218, 228, 255))
        y = 310; fn = font(F_BLACK, 40 * sc)
        for i, ln in enumerate(lines):
            if i == hi and k_hi > 0:
                tw = fn.getlength(ln) / sc
                _ov(im, lambda q, y=y, tw=tw: q.rectangle(S((w - 18) / 2 - tw / 2 - 12, y - 26, (w - 18) / 2 - tw / 2 - 12 + (tw + 24) * k_hi, y + 26), fill=(255, 226, 40, 200)))
            d.text(((w - 18) / 2 * sc, y * sc), ln, font=fn, fill=INK + (255,), anchor="mm"); y += 62
        for i in range(3):
            yy = h - 150 + i * 34
            d.rounded_rectangle(S(50, yy, w - 70 - (i % 2) * 120, yy + 14), 6 * sc, fill=(214, 218, 228, 255))
        return _done(im, w, h)
    return gcache(("report", tuple(lines), hi, k_hi, w, h, title, year), mk)


def ticket_el(top="DAY PASS", big="$10", col=(255, 199, 30), w=520, h=260):
    """admission-ticket style pass with notches and perforation"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(14, 16, w - 2, h - 2), 22 * sc, fill=(0, 0, 0, 60)))
        d.rounded_rectangle(S(0, 0, w - 14, h - 16), 22 * sc, fill=tuple(col) + (255,), outline=INK + (255,), width=5 * sc)
        for cy in (0, h - 16):
            d.ellipse(S(w * 0.68 - 22, cy - 22, w * 0.68 + 22, cy + 22), fill=(0, 0, 0, 0))
        for y in range(30, h - 40, 22): d.line(S(w * 0.68, y, w * 0.68, y + 10), fill=INK + (255,), width=4 * sc)
        d.text((w * 0.34 * sc, 70 * sc), top, font=font(F_BLACK, 40 * sc), fill=INK + (255,), anchor="mm")
        d.text((w * 0.34 * sc, 160 * sc), big, font=font(F_BLACK, 96 * sc), fill=INK + (255,), anchor="mm")
        d.text((w * 0.84 * sc, 120 * sc), "1x", font=font(F_BLACK, 60 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("ticket", top, big, col, w, h), mk)


def month_el(checked=(), w=700, h=640, title="THIS MONTH"):
    """month grid (5 rows x 7) with green ticks on `checked` day indices"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(12, 30, w - 2, h - 2), 30 * sc, fill=(0, 0, 0, 60)))
        d.rounded_rectangle(S(0, 20, w - 12, h - 12), 30 * sc, fill=(255, 255, 255, 255))
        d.rounded_rectangle(S(0, 20, w - 12, 130), 30 * sc, fill=RED_ + (255,)); d.rectangle(S(0, 100, w - 12, 130), fill=RED_ + (255,))
        for x in (150, w - 160): d.rounded_rectangle(S(x - 12, 0, x + 12, 54), 10 * sc, fill=(60, 60, 70, 255))
        d.text(((w - 12) / 2 * sc, 80 * sc), title, font=font(F_BLACK, 48 * sc), fill=(255, 255, 255, 255), anchor="mm")
        cw = (w - 72) / 7; ch = (h - 190) / 5
        for i in range(35):
            r_, c_ = divmod(i, 7); x = 30 + c_ * cw; y = 150 + r_ * ch
            on = i in checked
            d.rounded_rectangle(S(x + 4, y + 4, x + cw - 4, y + ch - 4), 10 * sc, fill=(220, 250, 226, 255) if on else (240, 241, 246, 255))
            if i < 30: d.text(((x + 16) * sc, (y + 20) * sc), str(i + 1), font=font(F_BOLD, 18 * sc), fill=(150, 154, 166, 255), anchor="lm")
            if on:
                d.line(S(x + cw * 0.28, y + ch * 0.55, x + cw * 0.45, y + ch * 0.75, x + cw * 0.78, y + ch * 0.3), fill=GRN_ + (255,), width=8 * sc, joint="curve")
        return _done(im, w, h)
    return gcache(("month", tuple(checked), w, h, title), mk)


def clipboard_el(w=520, h=700, title="MY WORKOUT PLAN", items=("MON  LEGS", "WED  CARDIO", "FRI  ARMS", "SUN  ABS")):
    """clipboard with a hopeful workout plan; empty checkboxes"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(16, 30, w - 2, h - 2), 26 * sc, fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, 20, w - 16, h - 12), 26 * sc, fill=255), (220, 160, 96), (176, 116, 60))
        d.rounded_rectangle(S(30, 70, w - 46, h - 40), 10 * sc, fill=(255, 255, 255, 255))
        d.rounded_rectangle(S(w / 2 - 100, 0, w / 2 + 84, 70), 16 * sc, fill=STEEL + (255,), outline=INK + (255,), width=4 * sc)
        d.text(((w - 16) / 2 * sc, 128 * sc), title, font=font(F_BLACK, 36 * sc), fill=INK + (255,), anchor="mm")
        for i, it in enumerate(items):
            y = 220 + i * 110
            d.rounded_rectangle(S(60, y - 30, 120, y + 30), 10 * sc, outline=INK + (255,), width=5 * sc)
            d.text((150 * sc, y * sc), it, font=font(F_BLACK, 40 * sc), fill=INK + (255,), anchor="lm")
        return _done(im, w, h)
    return gcache(("clip", w, h, title, tuple(items)), mk)


def cancel_phone_el(pressed=False, w=420, h=760):
    """phone showing a membership screen with a tiny grey 'cancel' link and a big 'KEEP' button"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(16, 18, w - 2, h - 2), 56 * sc, fill=(0, 0, 0, 70)))
        d.rounded_rectangle(S(0, 0, w - 16, h - 16), 56 * sc, fill=INK + (255,))
        d.rounded_rectangle(S(18, 18, w - 34, h - 34), 42 * sc, fill=(246, 248, 252, 255))
        d.text(((w - 16) / 2 * sc, 110 * sc), "MEMBERSHIP", font=font(F_BLACK, 40 * sc), fill=INK + (255,), anchor="mm")
        d.text(((w - 16) / 2 * sc, 250 * sc), "$15", font=font(F_BLACK, 140 * sc), fill=GRN_ + (255,), anchor="mm")
        d.text(((w - 16) / 2 * sc, 350 * sc), "per month", font=font(F_BOLD, 34 * sc), fill=(120, 124, 136, 255), anchor="mm")
        d.rounded_rectangle(S(60, 440, w - 76, 540), 30 * sc, fill=(GRN_ if not pressed else (12, 120, 50)) + (255,))
        d.text(((w - 16) / 2 * sc, 490 * sc), "KEEP IT", font=font(F_BLACK, 46 * sc), fill=(255, 255, 255, 255), anchor="mm")
        d.text(((w - 16) / 2 * sc, 620 * sc), "cancel", font=font(F_BOLD, 26 * sc), fill=(170, 174, 186, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("cphone", pressed, w, h), mk)


def crowd(f, cx, cy, cols, rows, k=1.0, r=46, gap=8, t=0.0, seed=0, jitter=0.0):
    """grid of mini heads appearing row by row as k goes 0..1"""
    n = cols * rows; shown = int(round(n * clamp(k)))
    rng = np.random.default_rng(seed); off = rng.uniform(-1, 1, (n, 2))
    step = r * 2 + gap - 20
    x0 = cx - (cols - 1) * step / 2; y0 = cy - (rows - 1) * step / 2
    order = np.argsort(rng.uniform(0, 1, n))
    el = mini_head(r, True)
    for j in order[:shown]:
        rr, cc = divmod(int(j), cols)
        jx = off[j, 0] * jitter * math.sin(t * 11 + j); jy = off[j, 1] * jitter * math.cos(t * 13 + j)
        comp(f, el, x0 + cc * step + jx, y0 + rr * step + jy)
