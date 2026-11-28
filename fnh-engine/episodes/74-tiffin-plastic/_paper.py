
# ================= FNH "Paper" look (adapted from the OopsMyBusiness paper system)
# cream paper alternating with deep series-colour paper, flat condensed headlines (Teko = Devanagari condensed),
# small italic serif subtitles (Tiro Devanagari, sheared), die-cut white sticker edges on cut-outs, series pill + round badge, film grain.
PAPER, INKP, PUR, PURD, YLP, REDP = 'F0E8D8', '1E102C', '5C2696', '22103F', 'FFD65C', 'E8463C'
TEKO = '/home/claude/studio/fonts/doc/teko-700.ttf'; TIRO = '/home/claude/studio/fonts/doc/tiro-dev.ttf'
ARCH = '/home/claude/studio/fonts/doc/archivo-900.woff'
THEME['end_text'] = PUR

def _paper(col, seed):
    rng = np.random.default_rng(seed); base = np.zeros((H, W, 3), np.float32) + np.array(rgb(col), np.float32)
    n = cv2.GaussianBlur(rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32), (0, 0), 1.2); n = cv2.resize(n, (W, H))
    fib = np.zeros((H, W), np.float32)
    for _ in range(900):                                             # paper fibres
        x0, y0 = rng.random(2) * (W, H); a = rng.random() * math.pi; L = 8 + rng.random() * 30
        cv2.line(fib, (int(x0), int(y0)), (int(x0 + L * math.cos(a)), int(y0 + L * math.sin(a))), float(rng.random()), 1, cv2.LINE_AA)
    base = base + n[..., None] * 4 - fib[..., None] * 7
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - CX) / W) ** 2 + ((yy - 1000) / H) ** 2)
    base = base * (1 - .32 * np.clip(r - .25, 0, 1)[..., None] * 1.6)
    return np.clip(base, 0, 255).astype(np.uint8)
_PP = {}
def paper(kind):
    if kind not in _PP: _PP[kind] = _paper(PAPER if kind == 'c' else PUR, 5 if kind == 'c' else 6)
    return _PP[kind]

def ebg(fr, mode, T=0.0):
    MODE[0] = mode
    fr[:] = paper('p' if mode == 'black' else 'c')
def photo_bg():
    MODE[0] = 'cream'; return paper('c')

@functools.lru_cache(maxsize=256)
def tline_paper(segs, size, mode):
    f = ImageFont.truetype(TEKO, int(size * 1.22), layout_engine=ImageFont.Layout.RAQM)
    widths = [int(f.getlength(s)) for s, _ in segs]; w = sum(widths) + 40; h = int(size * 1.42)
    onp = mode == 'black'
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); xx = 20
    for (s, hi), sw in zip(segs, widths):
        base = PAPER if onp else INKP
        if hi == 1: col = YLP if onp else REDP
        elif hi == 2: d.rectangle((xx - 10, int(size * .18), xx + sw + 10, int(size * 1.32)), fill=rgb(YLP if onp else INKP) + (255,)); col = INKP if onp else PAPER
        elif hi == 3: d.rectangle((xx - 10, int(size * .18), xx + sw + 10, int(size * 1.32)), fill=rgb(REDP) + (255,)); col = 'FFFFFF'
        else: col = base
        d.text((xx, int(size * .02)), s, font=f, fill=rgb(col) + (255,))
        xx += sw
    return np.array(im)
def title_line(fr, segs, y, t, size=112, mode=None, x=LX, wipe=True):
    if t <= 0: return
    mode = mode or MODE[0]; im = tline_paper(tuple(segs), size, mode)
    k = ease(clamp(t / .25)); h, w = im.shape[:2]
    if k < 1:                                                        # wipe in from the left
        im = im.copy(); im[:, int(w * k):, 3] = 0
    put_rgba(fr, im, CX, y + h / 2 + 16 * (1 - k), 1.0, 1.0, 0)

_note0 = note
def note(fr, txt, x, y, t, size=54, col=YL, rot=-4, ax=None, ay=None):
    if MODE[0] in ('cream', 'end') and col == YL: col = REDP
    _note0(fr, txt, x, y, t, size, col, rot, ax, ay)

@functools.lru_cache(maxsize=512)
def sub_paper(words, hi, mode):
    f = ImageFont.truetype(TIRO, 46, layout_engine=ImageFont.Layout.RAQM); sp = f.getlength(' ')
    words = words.replace('?', '').replace(',', '').replace('FreshNestHub', 'फ्रेशनेस्टहब')
    ws = words.split(' '); wl = [f.getlength(w) for w in ws]; w = int(sum(wl) + sp * (len(ws) - 1) + 60); h = 90
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); xx = 30
    onp = mode == 'black'
    for i, (s, sw) in enumerate(zip(ws, wl)):
        col = (YLP if onp else REDP) if i == hi else (PAPER if onp else INKP)
        d.text((xx, 12), s, font=f, fill=rgb(col) + (255,)); xx += sw + sp
    a = np.array(im); M = np.float32([[1, -.2, 16], [0, 1, 0]])                       # fake italic shear
    return cv2.warpAffine(a, M, (w + 20, h), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
def subtitle(fr, T):
    for g in SUBS:
        if g['s'] <= T < g['e']:
            hi = max([i for i, ts in enumerate(g['t']) if ts <= T] or [0])
            put_rgba(fr, sub_paper(' '.join(g['w']), hi, MODE[0]), CX, 1452, 1.0, 1.0, 0); return

def die_cut(rgba, pad=34, edge=15):
    a = np.pad(rgba, ((pad, pad), (pad, pad), (0, 0))); al = a[..., 3]
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * edge + 1, 2 * edge + 1)); dil = cv2.dilate(al, k)
    dil = cv2.GaussianBlur(dil, (0, 0), 1.2)
    sh = cv2.GaussianBlur(np.roll(np.roll(dil, 12, 0), 8, 1).astype(np.float32), (0, 0), 10) * .35
    out = np.zeros_like(a, np.float32)
    out[..., :3] = 0; out[..., 3] = sh
    wa = dil.astype(np.float32) / 255
    out[..., :3] = out[..., :3] * (1 - wa[..., None]) + 255 * wa[..., None]; out[..., 3] = np.maximum(out[..., 3], dil)
    oa = al.astype(np.float32)[..., None] / 255
    out[..., :3] = out[..., :3] * (1 - oa) + a[..., :3] * oa
    return np.clip(out, 0, 255).astype(np.uint8)
BOXR = die_cut(BOXR)

@functools.lru_cache(maxsize=1)
def paper_header():
    im = Image.new('RGBA', (W, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(ARCH, 30); txt = 'FRESHNESTHUB'; tw = f.getlength(txt) + 1.5 * len(txt)
    d.rounded_rectangle((70, 30, 70 + tw + 44, 82), 26, fill=rgb(PUR) + (255,))
    xx = 92
    for ch in txt: d.text((xx, 36), ch, font=f, fill=(255, 255, 255, 255)); xx += f.getlength(ch) + 1.5
    return np.array(im)
BADGE = cairo_layer(lambda c: (c.arc(900, 316, 50, 0, 2 * math.pi), c.set_source_rgba(*hx('111111')), c.fill(), logo(c, 900, 318, 38)))
_GR = [np.random.default_rng(40 + i).normal(0, 5.5, (H // 2, W // 2, 1)).astype(np.float32) for i in range(6)]

def frame(T):
    fr = np.zeros((H, W, 3), np.uint8)
    l = TL[0]
    for x in TL:
        if x['start'] <= T: l = x
    t = T - l['start']
    SCENES[l['id']](fr, T, t, l)
    camera(fr, l, t, T)
    if V != 'thumb': transition(fr, T)
    if V != 'thumb': subtitle(fr, T)
    put_rgba(fr, paper_header(), CX, 316, 1.0, 1.0, 0)
    overlay(fr, BADGE)
    g = cv2.resize(_GR[int(T * 12) % 6], (W, H))[..., None]
    return np.clip(fr.astype(np.float32) + g, 0, 255).astype(np.uint8)
