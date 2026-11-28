
# ================= Paper look v2: "shady" boiling headline font, stop-motion jiggle, sticker blocks, selection box, series progress bar
NSD9 = '/home/claude/studio/fonts/doc/nsd-900.ttf'; MODAK = '/home/claude/studio/fonts/doc/d_modak.ttf'
CUR = [0.0]
def boil_seed(): return int(CUR[0] * 8) % 3                      # edges re-draw 8x a second (line boil)

def _field(rng, h, w, s):
    n = rng.normal(0, 1, (h // s + 2, w // s + 2)).astype(np.float32); return cv2.resize(n, (w, h), interpolation=cv2.INTER_CUBIC)
def roughen(mask, seed, amp=1.7, freq=4):
    h, w = mask.shape; rng = np.random.default_rng(seed)
    dx = _field(rng, h, w, freq) * amp + _field(rng, h, w, 2) * amp * .5; dy = _field(rng, h, w, freq) * amp + _field(rng, h, w, 2) * amp * .5
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = cv2.remap(mask.astype(np.float32), xx + dx, yy + dy, cv2.INTER_LINEAR)
    return cv2.GaussianBlur(np.where(r > 110, 255, 0).astype(np.float32), (0, 0), .7)

@functools.lru_cache(maxsize=600)
def shady_line(segs, size, mode, seed):
    f = ImageFont.truetype(MODAK, size, layout_engine=ImageFont.Layout.RAQM)
    onp = mode == 'black'
    widths = [int(f.getlength(s)) for s, _ in segs]; pad = 40
    w = sum(widths) + 2 * pad + 30 * len(segs); h = int(size * 1.75)
    txtm = Image.new('L', (w, h), 0); dt = ImageDraw.Draw(txtm)
    cards = []; cols = []; xx = pad
    for (s, hi), sw in zip(segs, widths):
        if hi in (2, 3): xx += 14; cards.append((xx - 22, int(size * .22), xx + sw + 22, int(size * 1.5), hi))
        dt.text((xx, int(size * .05)), s, font=f, fill=255)
        if hi == 1: c = YLP if onp else REDP
        elif hi in (2, 3): c = INKP
        else: c = PAPER if onp else INKP
        cols.append((xx, xx + sw, c)); xx += sw + (14 if hi in (2, 3) else 0)
    m = np.array(txtm).astype(np.float32)
    out = np.zeros((h + 12, w + 12, 4), np.float32); allc = np.zeros((h + 12, w + 12), np.float32)
    for x0, y0, x1, y1, hi in cards:                                  # sticker cards behind key words (yellow / white)
        cm = Image.new('L', (w + 12, h + 12), 0); ImageDraw.Draw(cm).rounded_rectangle((x0, y0, x1, y1), 14, fill=255)
        cm = np.array(cm).astype(np.float32); allc = np.maximum(allc, cm); csh = cv2.GaussianBlur(np.roll(np.roll(cm, 10, 0), 6, 1), (0, 0), 6) * .45
        out[..., 3] = np.maximum(out[..., 3], csh)
        a = cm / 255; cc = np.array(rgb(YLP if hi == 3 else 'FBF7EE'), np.float32)
        out[..., :3] = out[..., :3] * (1 - a[..., None]) + cc * a[..., None]; out[..., 3] = np.maximum(out[..., 3], cm)
    sh = np.zeros((h + 12, w + 12), np.float32)
    if onp: sh[9:9 + h, 7:7 + w] = m
    else: sh[6:6 + h, 5:5 + w] = m
    sh = sh * (1 - allc / 255)
    shc = np.array(rgb('140A22' if onp else 'CDBFA5'), np.float32)
    sa = sh / 255 * (1 - out[..., 3] / 255 * 0)                         # hard offset shadow
    out[..., :3] = out[..., :3] * (1 - sa[..., None]) + shc * sa[..., None]; out[..., 3] = np.maximum(out[..., 3], sh)
    tm = np.zeros((h + 12, w + 12), np.float32); tm[:h, :w] = m
    colimg = np.zeros((h + 12, w + 12, 3), np.float32) + np.array(rgb(cols[0][2]), np.float32)
    for x0, x1, c in cols: colimg[:, x0 - 6:x1 + 10] = rgb(c)
    a = tm[..., None] / 255
    out[..., :3] = out[..., :3] * (1 - a) + colimg * a; out[..., 3] = np.maximum(out[..., 3], tm)
    return np.clip(out, 0, 255).astype(np.uint8)

def title_line(fr, segs, y, t, size=112, mode=None, x=LX, wipe=True, sel=False):
    if t <= 0: return
    mode = mode or MODE[0]; im = shady_line(tuple(segs), int(size * .92), mode, 0)
    h, w = im.shape[:2]
    if w > W - 60: s0 = (W - 60) / w
    else: s0 = 1.0
    k = clamp(t / .3); pop = 1 + .28 * (1 - back(k)) if k < 1 else 1.0
    step = int(CUR[0] * 8); jig = 1.1 * math.sin(step * 2.7 + y * .01)            # stop-motion jiggle
    put_rgba(fr, im, CX, y + h * s0 / 2, s0 * pop, min(1, k * 3), jig)
    if sel and t > .25:
        sw, sh_ = w * s0 * .96, h * s0 * .9; x0, y0 = CX - sw / 2, y + h * s0 * .05
        def dr(c):
            c.set_source_rgba(*hx(INKP if mode != 'black' else PAPER, .8)); c.set_line_width(3); c.set_dash([12, 8])
            c.rectangle(x0, y0, sw, sh_); c.stroke()
            c.move_to(0, y0); c.line_to(W, y0); c.move_to(0, y0 + sh_); c.line_to(W, y0 + sh_); c.set_source_rgba(*hx(INKP if mode != 'black' else PAPER, .35)); c.stroke(); c.set_dash([])
            for px, py in ((x0, y0), (x0 + sw, y0), (x0, y0 + sh_), (x0 + sw, y0 + sh_)):
                c.rectangle(px - 9, py - 9, 18, 18); c.set_source_rgba(*hx(INKP if mode != 'black' else PAPER)); c.fill()
        overlay(fr, cairo_layer(dr))

_put0 = put_rgba
def put_rgba(fr, im, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    h, w = im.shape[:2]
    if 260 <= w < W - 20 and h >= 200:                                # cards / cut-outs: stepped stop-motion wobble
        step = int(CUR[0] * 8); rot = rot + .9 * math.sin(step * 2.3 + (w % 97)); cy = cy + 2.5 * math.sin(step * 3.1 + h)
    _put0(fr, im, cx, cy, scale, alpha, rot)

def film_card(path, crop, w, rad=8, border=22, inner=8):
    """vintage print: thick white border + black film edge + warm grade"""
    im = Image.open(path).convert('RGB').crop(crop); h = int(im.height * w / im.width)
    a = np.array(im.resize((w, h), Image.LANCZOS)).astype(np.float32) * np.array([1.06, 1.0, .9]); a = np.clip(a, 0, 255)
    W2, H2 = w + 2 * (border + inner), h + 2 * (border + inner)
    out = np.zeros((H2, W2, 4), np.uint8); out[..., :3] = 251; out[..., 3] = 255
    out[border:H2 - border, border:W2 - border, :3] = 18
    out[border + inner:border + inner + h, border + inner:border + inner + w, :3] = a.astype(np.uint8)
    return out
GLASSC = film_card(A73 + 'glass.jpg', (int(.1 * _gw), 0, int(.92 * _gw), _gh), 380)

@functools.lru_cache(maxsize=2)
def paper_header2(mode):
    im = Image.new('RGBA', (W, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(NSD9, 50, layout_engine=ImageFont.Layout.RAQM); txt = 'रोज़ का सच'
    tw = f.getlength(txt)
    d.rectangle((70, 26, 70 + tw + 28, 98), fill=rgb('8E5BD8') + (255,))
    d.text((84, 14), txt, font=f, fill=rgb(PAPER) + (255,))
    f2 = ImageFont.truetype(ARCH, 34); d.text((70 + tw + 46, 44), 'N° 74', font=f2, fill=rgb(PAPER if mode == 'black' else INKP) + (255,))
    return np.array(im), int(70 + tw + 28)

def frame(T):
    CUR[0] = T
    fr = np.zeros((H, W, 3), np.uint8)
    l = TL[0]
    for x in TL:
        if x['start'] <= T: l = x
    t = T - l['start']
    SCENES[l['id']](fr, T, t, l)
    camera(fr, l, t, T)
    if V != 'thumb': transition(fr, T)
    if V != 'thumb': subtitle(fr, T)
    overlay(fr, BADGE)
    g = cv2.resize(_GR[int(T * 12) % 6], (W, H))[..., None]
    return np.clip(fr.astype(np.float32) + g, 0, 255).astype(np.uint8)
