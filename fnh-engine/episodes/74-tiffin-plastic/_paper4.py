
# ================= Paper v5: headlines on solid cards (max contrast on a phone), Anek Devanagari Condensed 800
ANEK = '/home/claude/studio/fonts/doc/anek-c-800.ttf'; ANEKL = '/home/claude/studio/fonts/doc/anek-latin-800.ttf'
def _runs(s):
    out = []; cur = ''; lat = None
    for ch in s:
        l = ord(ch) < 0x0900 and ch != ' '
        if ch == ' ': l = lat if lat is not None else False
        if lat is None or l == lat: cur += ch; lat = l
        else: out.append((cur, lat)); cur = ch; lat = l
    if cur: out.append((cur, lat))
    return out
@functools.lru_cache(maxsize=400)
def card_line_img(segs, size, mode, tilt):
    fd = ImageFont.truetype(ANEK, size, layout_engine=ImageFont.Layout.RAQM); fl = ImageFont.truetype(ANEKL, int(size * .92), layout_engine=ImageFont.Layout.RAQM)
    pieces = []
    for s, hi in segs:
        for r, lat in _runs(s): pieces.append((r, hi, fl if lat else fd))
    ws = [f.getlength(r) for r, _, f in pieces]; tw = int(sum(ws))
    kind = 3 if any(h == 3 for _, h in segs) else (2 if any(h == 2 for _, h in segs) else 0)
    bg = {3: YLP, 2: INKP, 0: 'FBF7EE'}[kind]
    px, py = 34, int(size * .2); h = int(size * 1.45); w = tw + 2 * px
    im = Image.new('RGBA', (w + 20, h + 22), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 12, w + 10, h + 12), 18, fill=(20, 10, 34, 255))
    d.rounded_rectangle((0, 0, w, h), 18, fill=rgb(bg) + (255,), outline=rgb(INKP) + (255,), width=5)
    xx = px
    for (r, hi, f), wd in zip(pieces, ws):
        if kind == 2: col = YLP
        elif hi == 1: col = REDP
        else: col = INKP
        d.text((xx, py - int(size * .12) + (int(size * .06) if f is fl else 0)), r, font=f, fill=rgb(col) + (255,)); xx += wd
    return np.array(im)

def title_line(fr, segs, y, t, size=112, mode=None, x=LX, wipe=True, sel=False):
    if t <= 0: return
    mode = mode or MODE[0]; tilt = -1.6 if y < 470 else 1.4
    im = card_line_img(tuple(segs), int(size * .95), mode, tilt)
    h, w = im.shape[:2]; s0 = min(1.0, (W - 110) / w)
    k = clamp(t / .28); pop = 1 + .3 * (1 - back(k)) if k < 1 else 1.0
    step = int(CUR[0] * 8); jig = tilt + .6 * math.sin(step * 2.7 + y * .01)
    _put0(fr, im, CX, y + h * s0 / 2, s0 * pop, min(1, k * 3), jig)
    if sel and t > .25:
        sw_, sh_ = w * s0 * 1.04, h * s0 * 1.12; x0, y0 = CX - sw_ / 2, y - h * s0 * .06
        lc = PAPER if mode == 'black' else INKP
        def dr(c):
            c.set_source_rgba(*hx(lc, .9)); c.set_line_width(3); c.set_dash([12, 8]); c.rectangle(x0, y0, sw_, sh_); c.stroke()
            c.move_to(0, y0); c.line_to(W, y0); c.move_to(0, y0 + sh_); c.line_to(W, y0 + sh_); c.set_source_rgba(*hx(lc, .35)); c.stroke(); c.set_dash([])
            for qx, qy in ((x0, y0), (x0 + sw_, y0), (x0, y0 + sh_), (x0 + sw_, y0 + sh_)):
                c.rectangle(qx - 9, qy - 9, 18, 18); c.set_source_rgba(*hx(lc)); c.fill()
        overlay(fr, cairo_layer(dr))
