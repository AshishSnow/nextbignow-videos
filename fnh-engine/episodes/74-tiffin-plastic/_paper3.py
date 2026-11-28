
# ================= Paper v3: readable Modak (ink outline + hard shadow), colour first frame, photo-burst intro with shutter clicks
@functools.lru_cache(maxsize=400)
def modak_line(segs, size, mode):
    f = ImageFont.truetype(MODAK, size, layout_engine=ImageFont.Layout.RAQM)
    onp = mode == 'black'; sw = max(5, size // 11)
    widths = [int(f.getlength(s)) for s, _ in segs]; pad = 40 + sw
    w = sum(widths) + 2 * pad + 36 * len(segs); h = int(size * 1.7) + 2 * sw
    im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    xx = pad; parts = []
    for (s, hi), wd in zip(segs, widths):
        if hi in (2, 3): xx += 16
        parts.append((xx, s, hi, wd)); xx += wd + (16 if hi in (2, 3) else 0)
    for x0, s, hi, wd in parts:                                       # sticker cards
        if hi in (2, 3):
            d.rounded_rectangle((x0 - 24 + 8, int(size * .2) + 10, x0 + wd + 24 + 8, int(size * 1.48) + 10), 16, fill=(20, 10, 34, 150))
            d.rounded_rectangle((x0 - 24, int(size * .2), x0 + wd + 24, int(size * 1.48)), 16, fill=rgb(YLP if hi == 3 else 'FBF7EE') + (255,), outline=rgb(INKP) + (255,), width=5)
    ty = int(size * .08)
    for x0, s, hi, wd in parts:                                       # hard shadow
        if hi not in (2, 3): d.text((x0 + 8, ty + 10), s, font=f, fill=rgb('140A22') + (255,), stroke_width=sw, stroke_fill=rgb('140A22') + (255,))
    for x0, s, hi, wd in parts:
        if hi in (2, 3): fill, st = INKP, None
        elif hi == 1: fill, st = (YLP if onp else REDP), INKP
        else: fill, st = (PAPER if onp else PUR), INKP
        if st: d.text((x0, ty), s, font=f, fill=rgb(fill) + (255,), stroke_width=sw, stroke_fill=rgb(st) + (255,))
        else: d.text((x0, ty), s, font=f, fill=rgb(fill) + (255,))
    return np.array(im)

def title_line(fr, segs, y, t, size=112, mode=None, x=LX, wipe=True, sel=False):
    if t <= 0: return
    mode = mode or MODE[0]; im = modak_line(tuple(segs), int(size * 1.0), mode)
    h, w = im.shape[:2]; s0 = min(1.0, (W - 70) / w)
    k = clamp(t / .3); pop = 1 + .3 * (1 - back(k)) if k < 1 else 1.0
    step = int(CUR[0] * 8); jig = 1.0 * math.sin(step * 2.7 + y * .01)
    _put0(fr, im, CX, y + h * s0 / 2, s0 * pop, min(1, k * 3), jig)
    if sel and t > .25:
        sw_, sh_ = w * s0 * .94, h * s0 * .86; x0, y0 = CX - sw_ / 2, y + h * s0 * .06
        lc = INKP if mode != 'black' else PAPER
        def dr(c):
            c.set_source_rgba(*hx(lc, .85)); c.set_line_width(3); c.set_dash([12, 8]); c.rectangle(x0, y0, sw_, sh_); c.stroke()
            c.move_to(0, y0); c.line_to(W, y0); c.move_to(0, y0 + sh_); c.line_to(W, y0 + sh_); c.set_source_rgba(*hx(lc, .35)); c.stroke(); c.set_dash([])
            for px, py in ((x0, y0), (x0 + sw_, y0), (x0, y0 + sh_), (x0 + sw_, y0 + sh_)):
                c.rectangle(px - 9, py - 9, 18, 18); c.set_source_rgba(*hx(lc)); c.fill()
        overlay(fr, cairo_layer(dr))

# ---- intro photo burst: real photos slam in one after another (shutter clicks in the mix)
def _fc(name, fx0, fy0, fx1, fy1, w=500):
    im = Image.open(A73 + name); a, b = im.size
    return film_card(A73 + name, (int(fx0 * a), int(fy0 * b), int(fx1 * a), int(fy1 * b)), w)
BURST = [(_fc('boxes.jpg', .05, .05, .95, .95), -7, -20, 980), (_fc('mw_in.jpg', .08, .1, .92, .95), 6, 120, 1010),
         (_fc('takeaway.jpg', .0, .37, 1.0, .66), -4, -90, 1090), (_fc('rect_boxes.jpg', .02, .05, .98, .95), 8, 100, 940),
         (_fc('lunch1.jpg', .0, .0, 1.0, .36), -3, 0, 1030)]
BT = [-0.3, 0.42, 0.79, 1.16, 1.53]
def sc_s1(fr, T, t, l):
    thumb = V == 'thumb'; tt = 1.7 if thumb else t
    ebg(fr, 'black', T)
    dive = ease(clamp((tt - 2.4) / 1.1))
    for i, (img, rot, dx, y) in enumerate(BURST):
        u = tt - BT[i]
        if u < 0: continue
        k = clamp(u / .14); s = lerp(1.7, 1.0, ease(k)) * lerp(1, 1.6, dive)
        _put0(fr, img, CX + dx * lerp(1, 1.8, dive), y + 120 * dive, s, min(1, k * 4) * (1 - dive), rot + (1 - k) * 10)
        if u < .06: fr[:] = np.clip(fr.astype(np.int16) + 70, 0, 255).astype(np.uint8)       # flash on each click
    hb = tt - 1.95
    if hb > 0:
        k = clamp(hb / .16); s = lerp(1.9, 1.25, ease(k)) * lerp(1, 1.45, dive)
        _put0(fr, BOXR, CX, 1060 + 40 * dive, s, min(1, k * 4), -6 + (1 - k) * 12 + .8 * math.sin(int(CUR[0] * 8) * 2.3))
    if dive > .3:
        overlay(fr, cairo_layer(lambda c: magnifier(c, CX, 1060, 300 * back(clamp((tt - 2.7) / .4)), clamp((tt - 2.7) / .2))))
    title_line(fr, [('अपना टिफ़िन', 0)], 380, tt + 1.0, 118)
    title_line(fr, [('अंदर से देखो', 3)], 560, 1.0 if thumb else tt - 2.0, 118)
    note(fr, 'अभी उठाओ', 230, 1350, 1.0 if thumb else tt - 2.2, 56, YL, 5)

SCENES['s1'] = sc_s1
