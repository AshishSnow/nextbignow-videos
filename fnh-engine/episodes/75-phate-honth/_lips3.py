
# ================= lips v3: topic-born ideas, not a reusable template
# chapped lips = cold dry winter air -> frost creeps in from the corners + drifting snow + wind streaks;
# scene changes = a giant tongue LICKS across the screen (the habit itself is the transition).
def _glow_mint():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - CX) / W) ** 2 + ((yy - 1000) / H * 1.1) ** 2); a = np.clip(1 - r * 1.5, 0, 1)[..., None]
    base = np.array(rgb('0A3B33'), np.float32) * (1 - a) + np.array(rgb('25A383'), np.float32) * a
    rng = np.random.default_rng(6); n = cv2.GaussianBlur(rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32), (0, 0), 1.2)
    return np.clip(base + cv2.resize(n, (W, H))[..., None] * 4, 0, 255).astype(np.uint8)
_PP['p'] = _glow_mint()

def _branches(seed, n=5):
    rng = np.random.default_rng(seed); segs = []
    def grow(x, y, a, L, d, t0):
        if d > 4 or L < 8: return
        x2, y2 = x + L * math.cos(a), y + L * math.sin(a); segs.append((x, y, x2, y2, t0, d))
        for s in (-1, 1):
            if rng.random() < .85: grow(x + (x2 - x) * .5, y + (y2 - y) * .5, a + s * (.9 + .3 * rng.random()), L * .45, d + 1, t0 + .12)
        grow(x2, y2, a + rng.normal(0, .15), L * .72, d + 1, t0 + .1)
    for i in range(n): grow(0, 0, i / (n - 1) * math.pi / 2, 150 + rng.random() * 60, 0, i * .04)
    return segs
FROST = [(_branches(11), 0, 0, 0), (_branches(12), W, 0, math.pi / 2), (_branches(13), W, H, math.pi), (_branches(14), 0, H, -math.pi / 2)]
SNOW = np.random.default_rng(9).random((40, 4))
def frost_layer(T, t, cream):
    def dr(c):
        col = (.55, .85, 1) if cream else (.88, .97, 1)
        for segs, ox, oy, rot in FROST:
            c.save(); c.translate(ox, oy); c.rotate(rot)
            for x, y, x2, y2, t0, d in segs:
                p = clamp((t - t0) / .35)
                if p <= 0: continue
                c.move_to(x, y); c.line_to(x + (x2 - x) * p, y + (y2 - y) * p)
                c.set_source_rgba(*col, .18); c.set_line_width(max(6, 18 - d * 3)); c.stroke()
                c.move_to(x, y); c.line_to(x + (x2 - x) * p, y + (y2 - y) * p)
                c.set_source_rgba(1, 1, 1, .85 - d * .12); c.set_line_width(max(1.5, 5 - d * 1.0)); c.stroke()
                if d >= 3 and p >= 1: snowflake(c, x2, y2, 7, .8, d)
            c.restore()
        for i, (sx, sy, sp, sz) in enumerate(SNOW):                 # drifting snow, blown sideways
            x = (sx * W + T * 60 * (1 + sp)) % W; y = (sy * H + T * 90 * (.5 + sp)) % H
            c.arc(x, y, 2 + 4 * sz, 0, 2 * math.pi); c.set_source_rgba(*col, .7 if not cream else .5); c.fill()
        ph = (T * .35) % 1                                           # occasional cold wind streaks
        if ph < .35:
            for k in range(3):
                y = 700 + k * 260; x0 = -400 + ph / .35 * (W + 800)
                c.move_to(x0, y); c.curve_to(x0 + 120, y - 30, x0 + 240, y + 30, x0 + 380, y)
                c.set_source_rgba(1, 1, 1, .35 * math.sin(ph / .35 * math.pi)); c.set_line_width(5); c.stroke()
    return cairo_layer(dr)

def ebg(fr, mode, T=0.0):
    _ebg0(fr, mode, T)
    if LT[1] not in NOLEAF: overlay(fr, frost_layer(T, LT[0] if V != 'thumb' else 2.0, mode != 'black'))

TR = .2
def transition(fr, T):
    for i, x in enumerate(TL[1:]):
        u = T - x['start']
        if -TR < u < TR:
            p = (u + TR) / (2 * TR)                                  # 0..1 across the cut
            cx = lerp(-700, W + 700, ease(p)); dirn = 1 if i % 2 == 0 else -1
            if dirn < 0: cx = W - cx
            def dr(c):
                c.save(); c.translate(cx, 1000); c.rotate(-math.pi / 2 * dirn); c.scale(7.5, 9)
                c.move_to(-70, -40); c.curve_to(-80, 60, -40, 120, 0, 120); c.curve_to(40, 120, 80, 60, 70, -40); c.close_path()
                g = cairo.LinearGradient(0, -40, 0, 120); g.add_color_stop_rgb(0, .95, .42, .52); g.add_color_stop_rgb(1, .86, .25, .38)
                c.set_source(g); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(2); c.stroke()
                c.move_to(0, -30); c.line_to(0, 90); c.set_source_rgba(.62, .14, .25, .8); c.set_line_width(4); c.stroke()
                c.restore()
            overlay(fr, cairo_layer(dr)); return
