
# ================= lips v3: structure = 0-2 s topic intro -> full-screen animated WORLD (Kurzgesagt-style: lip surface = a pink desert)
# -> explainer cards -> animated world interlude (villains stomp the desert) -> explainer -> end
FACE = ['E9B48F', 'DDA27D', 'CB8A66', 'B57351']; LIPC = ['F4A6AD', 'E88792', 'D96A7C', 'C24F66']
LAYERS = [(.35, 980, 60, .004, 0.0), (.55, 1120, 70, .006, 1.3), (.8, 1260, 55, .009, 2.1), (1.0, 1400, 40, .012, .7)]
BOUND = 1200.0
def hill_y(li, wx):
    p, base, A, f, ph = LAYERS[li]
    return base + A * math.sin(wx * f + ph) + A * .45 * math.sin(wx * f * 2.3 + ph * 1.7)
def _cracks():
    rng = np.random.default_rng(31); out = []
    for i in range(16):
        x = BOUND + 60 + rng.random() * 1400; y = 70 + rng.random() * 380; pts = [(x, y)]; a = rng.random() * math.pi
        for k in range(7):
            a += rng.normal(0, .6); x += 42 * math.cos(a); y += 26 * math.sin(a); pts.append((x, y))
        out.append((pts, rng.random() * .5))
    return out
CRACKS = _cracks()
def world(c, T, cam, zoom=1.0, gloss=0.0, wave=None, dry=0.0, crack=0.0, sun=0.0, evap=0.0, oil=0.0, signs=0.0, snow=0.0):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .55, .45, .85); g.add_color_stop_rgb(.55, 1, .78, .7); g.add_color_stop_rgb(1, 1, .9, .8)
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    if sun > 0:                                                    # hot drying sun
        r = 120 * back(sun); c.save(); c.translate(820, 900); c.rotate(T * .5)
        for i in range(12):
            c.rotate(math.pi / 6); c.move_to(r * 1.2, 0); c.line_to(r * 1.75, -14); c.line_to(r * 1.75, 14); c.close_path()
        c.set_source_rgba(1, .85, .3, .85); c.fill(); c.restore()
        c.arc(820, 900, r, 0, 2 * math.pi); c.set_source_rgb(1, .8, .25); c.fill()
    for li, (p, base, A, f, ph) in enumerate(LAYERS):
        def sx2wx(sx): return cam + (sx - CX) / (p * zoom)
        sb = CX + (BOUND - cam) * p * zoom
        c.move_to(-20, H + 10)
        for sx in range(-20, W + 40, 14):
            y = CX * 0 + 1000 + (hill_y(li, sx2wx(sx)) - 1000) * zoom
            c.line_to(sx, y)
        c.line_to(W + 40, H + 10); c.close_path()
        cf, cl = rgb(FACE[li]), rgb(LIPC[li])
        dl = [v / 255 * (1 - .25 * dry * (li == 3)) for v in cl]
        lg = cairo.LinearGradient(sb - 60, 0, sb + 60, 0); lg.add_color_stop_rgb(0, *[v / 255 for v in cf]); lg.add_color_stop_rgb(1, *dl)
        c.set_source(lg); c.fill()
        if gloss > 0 and li >= 2:                                   # wet shine on the hill tops
            c.move_to(0, 1000 + (hill_y(li, sx2wx(0)) - 1000) * zoom + 10)
            for sx in range(0, W + 14, 14): c.line_to(sx, 1000 + (hill_y(li, sx2wx(sx)) - 1000) * zoom + 10)
            c.set_source_rgba(1, 1, 1, .55 * gloss); c.set_line_width(8); c.stroke()
    fy = lambda wx: 1000 + (hill_y(3, wx) - 1000) * zoom
    W2S = lambda wx: CX + (wx - cam) * zoom
    if wave is not None:                                           # saliva wave: a glossy blue band riding the lip surface
        x0 = max(-20, W2S(wave - 700)); x1 = min(W + 20, W2S(wave))
        if x1 > x0:
            xs = np.linspace(x0, x1, 48)
            top = [(sx, fy(cam + (sx - CX) / zoom) - 55 - 18 * math.sin(sx * .03 + T * 8)) for sx in xs]
            c.move_to(*top[0])
            for p_ in top[1:]: c.line_to(*p_)
            for sx in xs[::-1]: c.line_to(sx, fy(cam + (sx - CX) / zoom) + 30)
            c.close_path(); c.set_source_rgba(.62, .86, 1, .7); c.fill()
            c.move_to(*top[0])
            for p_ in top[1:]: c.line_to(*p_)
            c.set_source_rgba(1, 1, 1, .9); c.set_line_width(6); c.stroke()
    if crack > 0:
        for pts, d0 in CRACKS:
            p_ = clamp((crack - d0) / .5)
            if p_ <= 0: continue
            n = max(2, int(len(pts) * p_))
            for i, (x, y) in enumerate(pts[:n]):
                X = W2S(x); Y = fy(x) + y * zoom
                (c.move_to if i == 0 else c.line_to)(X, Y)
            c.set_source_rgba(.42, .12, .18, .9); c.set_line_width(5 * zoom); c.stroke()
    if evap > 0:                                                   # water leaving as little drops
        rng = np.random.default_rng(4)
        for i in range(26):
            wx = BOUND + 80 + rng.random() * 1300; u = (evap * 1.4 - rng.random() * .4)
            if u <= 0 or u > 1: continue
            drop(c, W2S(wx), fy(wx) - 20 - 520 * ease(u), 15 * zoom, 1 - u, True)
    if oil > 0:                                                    # oil glands = little golden fountains on face side only
        for j, wx in enumerate((620, 860, 1080)):
            X = W2S(wx); Y = fy(wx)
            c.save(); c.translate(X, Y); c.scale(1.2, 1.2)
            c.arc(0, 0, 34, math.pi, 0); c.set_source_rgb(.85, .62, .2); c.fill()
            for k in range(9):
                ph = (T * 1.4 + k / 9 + j * .3) % 1; a = -math.pi / 2 + (k - 4) * .12
                x = math.cos(a) * 220 * ph; y = -260 * ph + 300 * ph * ph
                c.arc(x, y, 9 * (1 - ph * .5), 0, 2 * math.pi); c.set_source_rgba(1, .82, .25, oil * (1 - ph * .3)); c.fill()
            c.restore()
    if snow > 0:
        rng = np.random.default_rng(8)
        for i in range(40):
            x = (rng.random() * W + T * 240) % W; y = (rng.random() * H + T * 130) % H
            snowflake(c, x, y, 8 + 6 * rng.random(), .8 * snow, T + i)
        ph = (T * .7) % 1
        for k in range(3):
            y = 700 + k * 200; xw = -300 + ph * (W + 600)
            c.move_to(xw, y); c.curve_to(xw + 120, y - 30, xw + 240, y + 30, xw + 380, y)
            c.set_source_rgba(1, 1, 1, .5 * snow * math.sin(ph * math.pi)); c.set_line_width(6); c.stroke()
    return W2S, fy

def signpost(fr, x, y, txt, k, col):
    if k <= 0: return
    def dr(c):
        c.rectangle(x - 7, y - 150 * k, 14, 150 * k); c.set_source_rgb(.36, .22, .14); c.fill()
    overlay(fr, cairo_layer(dr))
    _put0(fr, card_line_img(((txt, 1 if col else 0),), 46, 'cream', 0), x, y - 170 * k, k, 1.0, -3)

# ---------- intro (0-2.0): topic in one beat
def sc_i1(fr, T, t, l):
    thumb = V == 'thumb'; tt = 1.2 if thumb else t
    ebg(fr, 'black', T)
    dive = 0.0 if thumb else clamp((t - 1.55) / .45)
    s = math.exp(lerp(math.log(.95), math.log(5.5), ease(dive)))
    _put0(fr, LIPS, CX, 1060, s * back(clamp(tt / .3)), 1.0 - .9 * clamp((t - 1.85) / .15) if not thumb else 1.0, -3 * (1 - dive))
    sw = clamp((tt - .25) / 1.2)
    def dr(c):
        if (0 < sw < 1 and dive < .2) or thumb:
            p = .5 if thumb else sw; tongue(c, lerp(240, 840, p), 1000 + 30 * math.sin(p * 9), 1.7)
        sparks(c, 230, 830, tt - .2)
    overlay(fr, cairo_layer(dr))
    if dive < .5: title_line(fr, [('फटे होंठ?', 3)], 380, tt + 1.0, 132)
    if dive < .5: title_line(fr, [('होंठ चाटना बंद करो', 0)], 575, tt + .6, 100)

# ---------- WORLD 1 (2.0-10.84): wet -> sun -> drops leave -> cracks; then pan out: face has oil fountains, lips none
def sc_w1(fr, T, t, l):
    a = T; MODE[0] = 'cream'                                                      # absolute time drives events (voice-synced)
    cam = 1800 if a < 5.5 else lerp(1800, 1150, ease(clamp((a - 5.5) / 1.6)))
    if a > 8.9: cam = lerp(1150, 1700, ease(clamp((a - 8.9) / 1.6)))
    zoom = math.exp(lerp(math.log(1.6), math.log(1.0), ease(clamp((t) / .9))))
    if 5.5 < a < 8.9: zoom = math.exp(lerp(0, math.log(.72), ease(clamp((a - 5.5) / 1.6))))
    if a >= 8.9: zoom = math.exp(lerp(math.log(.72), math.log(1.15), ease(clamp((a - 8.9) / 1.6))))
    wave = lerp(900, 3200, clamp((a - 2.2) / 1.0)) if 2.2 < a < 3.4 else None
    gloss = clamp((a - 2.6) / .3) * (1 - clamp((a - 3.4) / 1.6))
    sun = clamp((a - 3.3) / .3); evap = clamp((a - 3.5) / 2.2); crack = clamp((a - 3.6) / 2.0) + clamp((a - 9.4) / 1.2) * .4
    oil = clamp((a - 6.6) / .4); dry = clamp((a - 3.5) / 3)
    def dr(c): world(c, T, cam, zoom, gloss, wave, dry, crack, sun, evap, oil, 0, 0)
    overlay(fr, cairo_layer(dr))
    if t < .25: fr[:] = np.clip(fr.astype(np.int16) + int(160 * (1 - t / .25)), 0, 255).astype(np.uint8)   # arrive from the dive
    W2S = lambda wx: CX + (wx - cam) * zoom
    sk = back(clamp((a - 6.0) / .35))
    if sk > 0:
        signpost(fr, W2S(760), 1000 + (hill_y(3, 760) - 1000) * zoom - 10, 'चेहरा', sk, False)
        signpost(fr, W2S(1600), 1000 + (hill_y(3, 1600) - 1000) * zoom - 10, 'होंठ', sk, True)
    if 1.9 < a < 3.35: _put0(fr, brush_banner('अच्छा लगा', 64), CX, 760, back(clamp((a - 1.95) / .25)), 1.0, -3)
    if a > 3.3: title_line(fr, [('यहीं गलती है', 3)], 380, a - 3.3, 124)
    if a > 6.8: title_line(fr, [('तेल ग्रंथि: ', 0), ('ज़ीरो', 1)], 560, a - 6.8, 112)
    if a > 9.5: title_line(fr, [('जल्दी सूखते हैं', 3)], 560, a - 9.5, 112)

# ---------- WORLD 2 interlude (29.0-34.64): cold only starts it; the giant tongue + balm do the damage
def sc_w2(fr, T, t, l):
    a = T; MODE[0] = 'cream'
    snow = clamp((a - 29.0) / .4) * (1 - clamp((a - 31.0) / .6))
    tx = lerp(-700, W + 700, clamp((a - 31.8) / 1.0)) if 31.8 < a < 32.9 else None
    wave = lerp(1200, 3400, clamp((a - 31.9) / .9)) if 31.9 < a < 33.0 else None
    stomp = clamp((a - 33.2) / .18)
    crack = .25 + .3 * clamp((a - 30.0) / 1.0) + .45 * clamp((a - 33.38) / .6)
    zoom = 1.05 + .05 * t / l['dur']
    def dr(c):
        world(c, T, 1750, zoom, 0, wave, .6 + .4 * clamp((a - 33.4) / .5), crack, 0, 0, 0, 0, snow)
        if tx is not None:
            c.save(); c.translate(tx, 1180); c.rotate(-math.pi / 2); tongue(c, 0, 0, 4.2); c.restore()
        if stomp > 0:
            y = lerp(-500, 900, ease(stomp)) if stomp < 1 else 900 + 6 * math.sin(T * 20) * (1 - clamp((a - 33.4) / .5))
            balm_guy(c, 760, y, 2.6, T, 'evil')
    overlay(fr, cairo_layer(dr))
    if a < 31.0: title_line(fr, [('ठंड बस शुरुआत', 0)], 380, a - 29.0, 120)
    if a > 31.9: title_line(fr, [('विलेन: जीभ + बाम', 3)], 380, a - 31.9, 116, sel=True)

SCENES.update(s1=sc_i1, w1=sc_w1, w2=sc_w2)
SHAKES = [(3.3, 22), (4.4, 12), (22.6, 26), (27.4, 14), (31.95, 16), (33.38, 34), (43.3, 12), (50.7, 18)]
FOCUS.update(w1=1000, w2=1000)
