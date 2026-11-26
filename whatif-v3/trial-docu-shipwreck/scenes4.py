import sys, os, json, math
sys.path.insert(0, '/home/claude/docu')
from kit import *
import cv2
D = '/home/claude/docu'
L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + 0.35; TOTAL = END + 1.8
def wt(i, frac): return S[i] + L[i]['dur'] * frac
def wfind(i, word):
    tx = L[i]['text'].lower(); k = tx.find(word.lower()); return wt(i, k / max(1, len(tx)))
T_ = wfind
exec(open(D + '/common_part.py').read())

FI = '/usr/share/fonts/opentype/inter/'
HB = FI + 'InterDisplay-Black.otf'; HX = FI + 'InterDisplay-ExtraBold.otf'; HS = FI + 'InterDisplay-SemiBold.otf'; HM = FI + 'InterDisplay-Medium.otf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
REDc = (226, 30, 38); INKc = (18, 18, 18)
FOCUS = {'hull2': (.15, .65), 'wreck': (.5, .62), 'coast2': (.8, .5)}

# ---------------------------------------------------------------- grade (ref: muted, matte blacks, cool-neutral, soft glow)
PH = {}
def graded(name, bw=False):
    k = (name, bw)
    if k in PH: return PH[k]
    im = Image.open(f'{D}/ph/{name}.jpg').convert('RGB')
    tw, th = int(W * 1.3), int(H * 1.3); fx, fy = FOCUS.get(name, (.5, .5))
    s = max(tw / im.width, th / im.height); im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    x0 = int((im.width - tw) * fx); y0 = int((im.height - th) * fy); im = im.crop((x0, y0, x0 + tw, y0 + th))
    a = np.asarray(im).astype(np.float32) / 255
    g = (a * [.3, .59, .11]).sum(2, keepdims=True)
    a = g + (a - g) * (0.0 if bw else .62)                       # desaturate hard
    a = np.clip((a - .45) * 1.18 + .45, 0, 1)                    # contrast
    a = a ** 1.18                                                # darker mids
    a = a * .86 + .045                                           # matte: lifted blacks, rolled highlights
    a = a + (1 - g) * np.array([-.012, .0, .02])                 # slightly cool shadows
    glow = cv2.GaussianBlur(np.clip(a - .62, 0, 1), (0, 0), 18) * .55   # halation on highlights
    a = np.clip(a + glow, 0, 1)
    a = cv2.GaussianBlur(a, (0, 0), .7)                          # soft, filmic
    PH[k] = (a * 255).astype(np.uint8); return PH[k]

def ease_kb(lt, dur): u = clamp(lt / max(dur, .01)); return ease(u) * .7 + u * .3
def shot(fr, name, lt, dur, z0=1.0, z1=1.12, px=0.0, py=0.0, dim=0.0, bw=False):
    src = graded(name, bw); u = ease_kb(lt, dur)
    z = lerp(z0, z1, u); h, w = src.shape[:2]; cw, ch = w / (1.3 * z), h / (1.3 * z)
    cx = w / 2 + px * u; cy = h / 2 + py * u
    x0 = clamp(cx - cw / 2, 0, w - cw); y0 = clamp(cy - ch / 2, 0, h - ch)
    M = np.float32([[W / cw, 0, -x0 * W / cw], [0, H / ch, -y0 * H / ch]])
    fr[:] = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if dim: fr[:] = (fr * (1 - dim)).astype(np.uint8)

def crop_img(name, w, h, bw=False):
    src = graded(name, bw); s = max(w / src.shape[1], h / src.shape[0]) * 1.02
    im = cv2.resize(src, (int(src.shape[1] * s) + 1, int(src.shape[0] * s) + 1), interpolation=cv2.INTER_AREA)
    y0 = (im.shape[0] - h) // 2; x0 = (im.shape[1] - w) // 2; return im[y0:y0 + h, x0:x0 + w]

def card(fr, name, cx, cy, w, h, t, rot=0.0, z=1.0, bw=False, border=0, shadow=110):
    if t <= 0: return
    im = crop_img(name, w, h, bw)
    pad = 50; rg = np.zeros((h + pad * 2, w + pad * 2, 4), np.uint8)
    sh = np.zeros(rg.shape[:2], np.uint8); sh[pad + 16:pad + h + 16, pad + 8:pad + w + 8] = shadow
    rg[..., 3] = cv2.GaussianBlur(sh, (0, 0), 16)
    if border: rg[pad - border:pad + h + border, pad - border:pad + w + border] = (236, 233, 226, 255)
    rg[pad:pad + h, pad:pad + w, :3] = im; rg[pad:pad + h, pad:pad + w, 3] = 255
    p = eout(clamp(t / .35)); put_rgba(fr, rg, cx, cy + 50 * (1 - p), z * (.9 + .1 * p), p, rot)

# ---------------------------------------------------------------- type (ref: Helvetica-like grotesk, tight tracking)
TI = {}
def txt(s, font, size, fill=(255, 255, 255), track=-.03, shadow=.55, alpha=255):
    k = (s, font, size, fill, track, shadow, alpha)
    if k in TI: return TI[k]
    f = ImageFont.truetype(font, size); tr = track * size
    ws = [f.getlength(ch) for ch in s]; tw = int(sum(ws) + tr * (len(s) - 1)) + 4
    asc, desc = f.getmetrics(); pad = int(size * .35) + 10
    im = Image.new('RGBA', (tw + pad * 2, asc + desc + pad * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = pad
    for ch, w_ in zip(s, ws): d.text((x, pad), ch, font=f, fill=fill + (alpha,)); x += w_ + tr
    a = np.array(im)
    if shadow:
        sh = cv2.GaussianBlur(a[..., 3], (0, 0), max(3, size * .08)).astype(np.float32) * shadow
        out = np.zeros_like(a); out[..., 3] = np.maximum(a[..., 3], sh).astype(np.uint8)
        al = a[..., 3:4] / 255; out[..., :3] = (a[..., :3] * al).astype(np.uint8); a = out
    TI[k] = a; return a

def word(fr, s, cx, cy, size=60, font=HX, fill=(255, 255, 255), a=1.0, sc=1.0, rot=0.0, track=-.03, shadow=.55):
    put_rgba(fr, txt(s, font, size, fill, track, shadow), cx, cy, sc, a, rot)

def hero(fr, s, cx, cy, t, size=220, fill=(236, 236, 232), font=HB, track=-.045, shadow=.5, a=.92):
    """big grotesk word, slightly translucent (ref: SUBPRIME / YEARS). Punch in from 112%."""
    if t <= 0: return
    p = eout(clamp(t / .16)); word(fr, s, cx, cy, size, font, fill, a * p, 1.12 - .12 * p, 0, track, shadow)

def blurword(fr, s, cx, cy, t, size=230, fill=REDc):
    """letters slide in one by one with motion blur (ref: red 'AND')."""
    if t <= 0: return
    f = ImageFont.truetype(HB, size); tr = -.05 * size; ws = [f.getlength(ch) for ch in s]
    tot = sum(ws) + tr * (len(s) - 1); x = cx - tot / 2
    for k, (ch, w_) in enumerate(zip(s, ws)):
        u = eout(clamp((t - k * .045) / .18))
        if u <= 0: x += w_ + tr; continue
        im = txt(ch, HB, size, fill, 0, 0).copy()
        if u < 1:
            n = int(40 * (1 - u)) | 1; ker = np.zeros((1, n), np.float32); ker[0] = 1 / n
            im = cv2.filter2D(im, -1, ker)
        put_rgba(fr, im, int(x + w_ / 2 + 120 * (1 - u)), cy, 1.0, u, -4 * (1 - u)); x += w_ + tr

def labels(fr, lines, cx, cy, t0s, T, size=64):
    """black boxes, white text, stacked (ref: 'Boring / Conservative')."""
    y = cy
    for s, t0 in zip(lines, t0s):
        if T > t0:
            f = ImageFont.truetype(HS, size); w = int(f.getlength(s) * .97) + 36; h = int(size * 1.3)
            im = Image.new('RGBA', (w, h), (14, 14, 14, 235)); d = ImageDraw.Draw(im)
            x = 18
            for ch in s: d.text((x, h / 2), ch, font=f, fill=(245, 245, 245, 255), anchor='lm'); x += f.getlength(ch) - .03 * size
            put_rgba(fr, np.array(im), cx - 0 + (w // 2 - 200 if False else 0), y, 1.0, eout(clamp((T - t0) / .12)), 0)
        y += int(size * 1.4)

def capword(fr, T, y=1150, dark=False, skip=()):
    """ONE word at a time, centred, bold grotesk, tight tracking."""
    for i, l in enumerate(L):
        if i in skip: continue
        if S[i] - .02 <= T < E[i] + .05:
            tx = l['text']; p = 0; cur = None
            for w_ in tx.split():
                k = tx.find(w_, p); p = k + len(w_)
                if wt(i, k / len(tx)) - .03 <= T: cur = w_
            if cur:
                word(fr, cur.strip('.,?'), CX, y, 62, HX, INKc if dark else (246, 246, 246), 1.0, 1.0, 0, -.035, 0 if dark else .6)
            return

def typewriter(fr, s, cx, cy, t, cps=16, size=50, col=(232, 232, 232), cursor=True, left=None):
    if t <= 0: return
    n = int(clamp(t * cps, 0, len(s))); sub = s[:n]
    f = ImageFont.truetype(MONO, size); cw = f.getlength('M')
    x0 = left if left is not None else cx - cw * len(s) / 2
    if sub:
        im = Image.new('RGBA', (int(cw * len(sub)) + 10, int(size * 1.4)), (0, 0, 0, 0)); ImageDraw.Draw(im).text((0, size * .7), sub, font=f, fill=col + (255,), anchor='lm')
        fr_y0 = cy - im.height // 2; a = np.array(im); x1 = int(x0); reg = fr[fr_y0:fr_y0 + a.shape[0], x1:x1 + a.shape[1]]
        al = a[:reg.shape[0], :reg.shape[1], 3:4] / 255; reg[:] = (reg * (1 - al) + a[:reg.shape[0], :reg.shape[1], :3] * al).astype(np.uint8)
    if cursor and (n < len(s) or int(t * 2.2) % 2 == 0):
        xx = int(x0 + cw * n + 4); fr[cy - size // 2:cy + size // 2, xx:xx + 5] = col

def tag(fr, s, cx, cy, t, bgc=REDc, size=42):
    if t <= 0: return
    f = ImageFont.truetype(HX, size); w = int(f.getlength(s)) + 40; h = int(size * 1.5)
    p = eout(clamp(t / .22)); ww = max(2, int(w * p))
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rectangle((0, 0, ww, h), fill=bgc + (255,))
    if p > .6: d.text((20, h / 2), s, font=f, fill=(255, 255, 255, 255), anchor='lm')
    put_rgba(fr, np.array(im), cx, cy, 1.0, 1.0, 0)

# ---------------------------------------------------------------- backgrounds
def make_paper():
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - CX) / W) ** 2 + ((yy - H / 2) / H) ** 2 * .7)
    base = np.clip(214 - r * 150, 120, 214)[..., None] * np.array([1, .995, .985])
    rs = np.random.RandomState(7); a = base + rs.randn(H, W, 1) * 2.5
    for _ in range(140):                                         # dust specks
        x, y = rs.randint(0, W), rs.randint(0, H); cv2.circle(a, (x, y), rs.randint(1, 3), (110, 110, 108), -1)
    return np.clip(a, 0, 255).astype(np.uint8)
PAPER = make_paper()
def paper_bg(fr): fr[:] = PAPER

def make_cork():
    rs = np.random.RandomState(3); n = rs.randn(H // 4, W // 4).astype(np.float32)
    n = cv2.resize(cv2.GaussianBlur(n, (0, 0), 1.2), (W, H)) * 9 + rs.randn(H, W).astype(np.float32) * 6
    a = np.stack([24 + n, 74 + n, 46 + n * .8], 2)
    return np.clip(a, 0, 255).astype(np.uint8)
CORK = make_cork()

def corkboard(fr, T, t0, pins):
    """evidence board: pinned photo cards + purple string + sticky notes (ref Dimon board)."""
    lt = T - t0; z = 1.0 + .06 * lt
    M = cv2.getRotationMatrix2D((CX, H / 2), 0, z); fr[:] = cv2.warpAffine(CORK, M, (W, H), borderMode=cv2.BORDER_REFLECT)
    pts = [(x, y) for _, x, y, _, _ in pins]
    def dr(c):
        for k in range(len(pts) - 1):
            u = clamp((lt - .25 - k * .25) / .3)
            if u <= 0: continue
            (x0, y0), (x1, y1) = pts[k], pts[k + 1]; c.move_to(x0, y0 - 160); c.line_to(lerp(x0, x1, u), lerp(y0 - 160, y1 - 160, u))
            c.set_source_rgba(.42, .3, .85, 1); c.set_line_width(5); c.stroke()
    for k, (name, x, y, w, h) in enumerate(pins):
        card(fr, name, x, y, w, h, lt - k * .22, (-5, 4, -3, 5)[k % 4], 1.0, False, 12, 140)
    overlay(fr, cairo_layer(dr))
    def pinsd(c):
        for k, (x, y) in enumerate(pts):
            if lt - k * .22 > .2: c.arc(x, y - 160, 14, 0, 6.29); c.set_source_rgba(.45, .32, .9, 1); c.fill()
    overlay(fr, cairo_layer(pinsd))

def sticky(fr, s, cx, cy, t, col=(240, 160, 170), rot=6):
    if t <= 0: return
    im = Image.new('RGBA', (260, 240), col + (255,)); d = ImageDraw.Draw(im); f = ImageFont.truetype(MONO, 34)
    d.text((130, 120), s, font=f, fill=(60, 40, 40, 255), anchor='mm'); a = np.array(im)
    put_rgba(fr, a, cx, cy, eout(clamp(t / .25)), 1.0, rot)

def grid_wall(fr, T, t0, names, center, cname_t=None):
    """photo grid wall with gutters, camera pulls in to the centre tile (ref: Palmer 'Bolt' grid)."""
    lt = T - t0; fr[:] = 18; z = lerp(1.0, 2.2, ease(clamp(lt / 1.0)))
    cw, ch, gx = 330, 250, 14; cols, rows = 3, 7; ox = CX - (cols * (cw + gx)) / 2 + cw / 2; oy = H / 2 - (rows * (ch + gx)) / 2 + ch / 2
    tile = np.zeros_like(fr); tile[:] = 18; k = 0
    for r in range(rows):
        for cidx in range(cols):
            x = int(ox + cidx * (cw + gx)); y = int(oy + r * (ch + gx)); is_c = (r == 3 and cidx == 1)
            nm = center if is_c else names[k % len(names)]; k += 1
            im = crop_img(nm, cw, ch, not is_c)
            if not is_c: im = (im * .55).astype(np.uint8)
            tile[y - ch // 2:y + ch // 2, x - cw // 2:x + cw // 2] = im
    cy0 = int(oy + 3 * (ch + gx))
    M = cv2.getRotationMatrix2D((CX, cy0), 0, z); M[1, 2] += H / 2 - cy0
    fr[:] = cv2.warpAffine(tile, M, (W, H), borderValue=(18, 18, 18))

# ---------------------------------------------------------------- finish / transitions
GRAIN = [(np.random.RandomState(k).randn(H // 2, W // 2) * 4.0).repeat(2, 0).repeat(2, 1).astype(np.float32) for k in range(6)]
VIG = None
def finish(fr, T, g=1.0):
    global VIG
    if VIG is None:
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - CX) / W) ** 2 + ((yy - H / 2) / H) ** 2 * .75)
        VIG = np.clip(1 - (r - .22) * 1.35, .35, 1).astype(np.float32)[..., None]
    fr[:] = np.clip(fr * VIG + GRAIN[int(T * 8) % 6][..., None] * g, 0, 255).astype(np.uint8)

def whip(fr, k):
    n = int(10 + 110 * k) | 1; ker = np.zeros((1, n), np.float32); ker[0] = 1 / n
    fr[:] = np.roll(cv2.filter2D(fr, -1, ker), int(140 * k), 1)
def zoomblur(fr, k):
    acc = fr.astype(np.float32); n = 6
    for j in range(1, n):
        s = 1 + .05 * k * j; M = cv2.getRotationMatrix2D((CX, H / 2), 0, s); acc += cv2.warpAffine(fr, M, (W, H), borderMode=cv2.BORDER_REFLECT)
    fr[:] = (acc / n).astype(np.uint8)
def glitch(fr, T, k):
    o = int(26 * k); fr[..., 0] = np.roll(fr[..., 0], o, 1); fr[..., 2] = np.roll(fr[..., 2], -o, 1)
    rs = np.random.RandomState(int(T * 60))
    for _ in range(int(7 * k)):
        y = rs.randint(0, H - 80); h = rs.randint(8, 70); fr[y:y + h] = np.roll(fr[y:y + h], rs.randint(-100, 100), 1)
CUTS = []
def trans(fr, T):
    for t, kind in CUTS:
        d = T - t
        if -.1 < d < .1:
            k = 1 - abs(d) / .1
            if kind == 'whip': whip(fr, k)
            elif kind == 'zoom': zoomblur(fr, k)
            elif kind == 'glitch': glitch(fr, T, k)
            elif kind == 'flash': fr[:] = np.clip(fr + 200 * k, 0, 255).astype(np.uint8)

def diag3(fr, T, t0, names):
    """three photos split by diagonals (ref: Palmer/Karp triangle split)."""
    lt = T - t0; ims = []
    for k, nm in enumerate(names):
        tmp = np.zeros_like(fr); shot(tmp, nm, lt, 5, 1.1, 1.2, (-30, 30, 0)[k], 0); ims.append(tmp)
    yy, xx = np.mgrid[0:H, 0:W]
    m1 = (yy < 1150 - (xx - CX) * .6)                            # upper-left
    m2 = (yy < 1150 + (xx - CX) * .6) & ~m1                      # upper-right
    fr[:] = ims[2]; fr[m1] = ims[0][m1]; fr[m2] = ims[1][m2]
    lines = np.zeros(fr.shape[:2], np.uint8)
    cv2.line(lines, (0, int(1150 + CX * .6)), (W, int(1150 - CX * .6)), 255, 7); cv2.line(lines, (0, int(1150 - CX * .6)), (W, int(1150 + CX * .6)), 255, 7)
    fr[lines > 0] = (16, 16, 16)

def doc(fr, T, t0, rows, hls):
    paper_bg(fr); f = ImageFont.truetype(MONO, 42)
    im = Image.new('RGBA', (920, 130 + 78 * len(rows)), (246, 244, 238, 255)); d = ImageDraw.Draw(im)
    for k, s in enumerate(rows):
        y = 64 + 78 * k
        if k in hls:
            pp = ease(clamp((T - hls[k]) / .45)); w = f.getlength(s) + 24
            if pp > 0: d.rectangle((44, y - 8, 44 + w * pp, y + 52), fill=(255, 212, 0, 255))
        d.text((56, y), s, font=f, fill=(22, 22, 22, 255))
    a = np.array(im); pad = 50; rg = np.zeros((a.shape[0] + pad * 2, a.shape[1] + pad * 2, 4), np.uint8)
    rg[pad + 16:pad + 16 + a.shape[0], pad + 8:pad + 8 + a.shape[1], 3] = 120; rg[..., 3] = cv2.GaussianBlur(rg[..., 3], (0, 0), 18)
    rg[pad:pad + a.shape[0], pad:pad + a.shape[1]] = a
    p = eout(clamp((T - t0) / .4)); put_rgba(fr, rg, CX, 820 + 60 * (1 - p), 1.0 + .025 * (T - t0), p, -1.5)


# ---------------------------------------------------------------- hook v5: photo cards slam in (3D tilt + motion blur), receipt card, push-through
def card_rgba(name, w, h, border=14, bw=False):
    im = crop_img(name, w, h, bw); a = np.zeros((h + border * 2, w + border * 2, 4), np.uint8)
    a[..., :3] = (238, 235, 228); a[..., 3] = 255; a[border:border + h, border:border + w, :3] = im; return a

def receipt_rgba(T):
    w, h = 560, 620; im = Image.new('RGBA', (w, h), (246, 244, 236, 255)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(MONO, 34); fb = ImageFont.truetype(HX, 52)
    d.text((w / 2, 70), 'REPAIR RECEIPT', font=fb, fill=(20, 20, 20, 255), anchor='mm')
    d.line((40, 120, w - 40, 120), fill=(40, 40, 40, 255), width=3)
    rows = [('SHIP', 'ROMAN-ERA'), ('AGE', '~2,200 YRS'), ('COATS', '???'), ('WHERE', '???')]
    for k, (a_, b_) in enumerate(rows):
        y = 175 + k * 78; d.text((50, y), a_, font=f, fill=(40, 40, 40, 255)); d.text((w - 50, y), b_, font=f, fill=(200, 20, 30, 255) if '?' in b_ else (40, 40, 40, 255), anchor='ra')
        for x in range(50, w - 50, 14): d.point((x, y + 52), fill=(150, 150, 150, 255))
    for x in range(0, w, 28): d.polygon([(x, h), (x + 14, h - 18), (x + 28, h)], fill=(0, 0, 0, 0))   # torn bottom edge
    return np.array(im)

def card3d(fr, a, cx, cy, sc, rot, tilt, alpha=1.0, blur=0.0):
    """perspective card: tilt = rotation around the vertical axis (deg), rot = in-plane rotation."""
    h, w = a.shape[:2]; sh = np.zeros((h + 80, w + 80, 4), np.uint8); sh[40:40 + h, 40:40 + w] = a
    s2 = np.zeros_like(sh); s2[58:58 + h, 50:50 + w, 3] = 150; s2[..., 3] = cv2.GaussianBlur(s2[..., 3], (0, 0), 14)
    al = sh[..., 3:4] / 255.; comp = s2.astype(np.float32); comp[..., :3] = comp[..., :3] * (1 - al) + sh[..., :3] * al; comp[..., 3] = np.maximum(s2[..., 3], sh[..., 3])
    comp = comp.astype(np.uint8); H2, W2 = comp.shape[:2]
    t = math.radians(tilt); k = .25 * math.sin(t); sx = math.cos(t)
    src = np.float32([[0, 0], [W2, 0], [W2, H2], [0, H2]])
    dst = np.float32([[W2 * (1 - sx) / 2, H2 * k], [W2 * (1 + sx) / 2, -H2 * k], [W2 * (1 + sx) / 2, H2 * (1 + k)], [W2 * (1 - sx) / 2, H2 * (1 - k)]])
    M = cv2.getPerspectiveTransform(src, dst); comp = cv2.warpPerspective(comp, M, (W2, H2))
    if blur > .5:
        n = int(blur) | 1; ker = np.zeros((n, n), np.float32); ker[n // 2] = 1 / n; comp = cv2.filter2D(comp, -1, ker)
    put_rgba(fr, comp, cx, cy, sc, alpha, rot)

HOOK_CARDS = [('coast2', -.30, 300, 1110, -11, 420, 300, (-900, -300)), ('pollen', -.12, 790, 1040, 9, 400, 300, (900, -400)),
              ('mosaic', .10, 310, 1400, 7, 400, 290, (-900, 500)), ('resin', .28, 780, 1410, -8, 380, 290, (900, 600)),
              ('wreck', .48, CX, 1220, -2, 600, 430, (0, 900))]
CARDIMG = {}
def hook5(fr, T):
    bgimg = graded('wreck'); z = 1.0 + .04 * T
    b = cv2.GaussianBlur(cv2.resize(bgimg, (W, H)), (0, 0), 22); M = cv2.getRotationMatrix2D((CX, H / 2), 0, z)
    fr[:] = (cv2.warpAffine(b, M, (W, H), borderMode=cv2.BORDER_REFLECT) * .45).astype(np.uint8)
    tr = T_(0, 'and it still') - .05
    for name, t0, x, y, rot, w, h, (fx, fy) in HOOK_CARDS:
        if name not in CARDIMG: CARDIMG[name] = card_rgba(name, w, h)
        u = clamp((T - t0) / .28)
        if u <= 0: continue
        e = eout(u); bounce = 1 + .06 * math.sin(clamp((T - t0 - .28) / .25) * math.pi) if u >= 1 else 1
        dim = 1.0 if T < tr else 1 - .5 * clamp((T - tr) / .3)
        ci = CARDIMG[name] if dim >= 1 else np.dstack([(CARDIMG[name][..., :3] * dim).astype(np.uint8), CARDIMG[name][..., 3]])
        card3d(fr, ci, int(x + fx * (1 - e)), int(y + fy * (1 - e)), (1.5 - .5 * e) * bounce, rot + 25 * (1 - e), 38 * (1 - e) + 4 * math.sin(T * 1.5 + x), 1.0, 40 * (1 - e))
    if T > tr:                                                    # receipt slides up on top
        u = eout(clamp((T - tr) / .35)); card3d(fr, receipt_rgba(T), CX, int(1230 + 700 * (1 - u)), .95, 4 * (1 - u) + 3, 18 * (1 - u), 1.0, 30 * (1 - u))
    hero(fr, 'WHERE HAS', CX, 560, T + .5, 140, (240, 240, 236), HB, -.04, .6, 1.0)
    p = eout(clamp((T + .5) / .25)); y0, y1 = 655, 805
    fr[y0:y1, 110:970] = (fr[y0:y1, 110:970] * (1 - p) + np.array(REDc) * p).astype(np.uint8)
    hero(fr, 'THIS SHIP BEEN?', CX, 728, T + .5, 112, (255, 255, 255), HB, -.04, 0, 1.0)
    pz = clamp((T - (S[1] - .35)) / .35)                           # push through into next shot
    if pz > 0:
        zz = 1 + 1.6 * pz ** 2; M = cv2.getRotationMatrix2D((CX, 1200), 0, zz); fr[:] = cv2.warpAffine(fr, M, (W, H), borderMode=cv2.BORDER_REFLECT)
        zoomblur(fr, pz)
FOCUS['garage'] = (.5, .5)
# hard punch-in on nouns: alternating 1.0 / 1.09 crop at these word onsets = a "cut" on every key noun (ref: 70%+ of cuts land on a word onset)
PUNCH = {0: ['sank', 'receipts'], 1: ['car', 'receipt'], 3: ['fixed', 'hull', 'pine'], 4: ['sticky', 'air'], 7: ['samples', 'four'], 11: ['home', 'receipts']}
def punch(fr, T):
    for i, ws in PUNCH.items():
        if S[i] <= T < E[i] + .2:
            k = sum(T >= T_(i, w) - .02 for w in ws)
            if k % 2 == 1:
                z = 1.09; cw, ch = int(W / z), int(H / z); x0, y0 = (W - cw) // 2, (H - ch) // 2
                fr[:] = cv2.resize(fr[y0:y0 + ch, x0:x0 + cw], (W, H), interpolation=cv2.INTER_LINEAR)
            return

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8); cap = True; dark = False; gr = 1.0; pun = False
    if T < S[1]:
        hook5(fr, T); cap = False; capword(fr, T, 872)
    elif T < S[2]:
        shot(fr, 'garage', T - S[1], S[2] - S[1], 1.05, 1.16, 0, 0, bw=True); cap = False; pun = True
        labels(fr, ['basically a car', 'with every', 'service receipt'], CX, 860, [T_(1, 'basically') - .05, T_(1, 'kept') - .05, T_(1, 'service') - .05], T, 70)
    elif T < S[3]:
        shot(fr, 'hull2', T - S[2], S[3] - S[2], 1.3, 1.45, -30, 0, dim=.45)
        tw = T_(2, 'water'); tsec = T_(2, 'secret')
        if T > tw - .05:
            hero(fr, 'KEEP WATER OUT', CX, 760, T - tw + .05, 118, (236, 236, 232), HB, -.04, .6, .95)
            if T > T_(2, 'ended') - .05:
                u = eout(clamp((T - T_(2, 'ended') + .05) / .25)); fr[752:766, int(CX - 420):int(CX - 420 + 840 * u)] = REDc
        blurword(fr, 'KEEP A SECRET IN', CX, 930, T - tsec + .05, 118)
    elif T < S[4]:
        tp = T_(3, 'workers') - .05
        if T < tp: diag3(fr, T, S[3], ['hull2', 'mosaic', 'resin'])
        else:
            shot(fr, 'resin', T - tp, S[4] - tp, 1.05, 1.25, 0, -40)
            blurword(fr, 'HOT PINE TAR', CX, 860, T - T_(3, 'hot') + .05, 150)
        pun = True
    elif T < S[5]:
        shot(fr, 'pollen', T - S[4], S[5] - S[4], 1.0, 1.45); pun = True
        ta = T_(4, 'pollen')
        if T < ta: fr[:] = (fr * (1 - .45 * clamp((T - T_(4, 'grabbed')) / .5))).astype(np.uint8)
        else: hero(fr, 'POLLEN', CX, 860, T - ta, 250)
    elif T < S[6]:
        corkboard(fr, T, S[5] - .05, [('pollen', 290, 860, 380, 300), ('coast2', 790, 760, 360, 280), ('brindisi', 760, 1300, 380, 290), ('hull2', 300, 1360, 360, 280)])
        sticky(fr, 'where?', 560, 1080, T - T_(5, 'where'), rot=-5); cap = False
        hero(fr, 'FINGERPRINT', CX, 560, T - T_(5, 'fingerprint'), 120, (245, 245, 240), HB, -.04, .7, 1.0)
    elif T < S[7]:
        fr[:] = 10; cap = False; gr = .7
        typewriter(fr, '2,200 years later,', CX, 960, T - S[6] + .05, 18, 56)
    elif T < S[8]:
        doc(fr, T, S[7] - .05, ['WRECK: ILOVIK-PARZINE 1', 'AGE: ~2,200 YEARS', 'SAMPLES SCRAPED: 10', 'MAIN COAT: PINE TAR', 'DIFFERENT COATS: 4 OR 5'], {2: T_(7, 'ten'), 4: T_(7, 'four')})
        dark = True; gr = .6; pun = True
    elif T < S[9]:
        tc = T_(8, 'some from') - .05
        grid_wall(fr, T, S[8] if T < tc else tc, ['hull2', 'mosaic', 'resin', 'pollen', 'wreck', 'garage'], 'brindisi' if T < tc else 'coast2')
        tag(fr, 'NEAR ITALY' if T < tc else 'NEAR CROATIA', CX, 760, T - (T_(8, 'italy') if T < tc else T_(8, 'croatia')) + .15, REDc, 46)
    elif T < S[10]:
        paper_bg(fr); dark = True; cap = False; gr = .6
        if T > T_(9, 'same') - .03: word(fr, 'Same', 250, 700, 72, HX, INKc, 1, 1, 0, -.035, 0)
        card(fr, 'mosaic', CX, 900, 340, 240, T - S[9] + .1, -2)
        if T > T_(9, 'ship') - .03: word(fr, 'ship.', 830, 700, 72, HX, INKc, 1, 1, 0, -.035, 0)
        blurword(fr, 'DIFFERENT', CX, 1200, T - T_(9, 'different') + .05, 170)
        if T > T_(9, 'repair') - .03: hero(fr, 'repair shops.', CX, 1360, T - T_(9, 'repair'), 96, INKc, HX, -.035, 0, 1.0)
    elif T < S[11]:
        shot(fr, 'garage', T - S[10], S[11] - S[10], 1.2, 1.3, 0, 60, dim=.55, bw=True); cap = False
        typewriter(fr, 'tag the friend who', CX, 900, T - T_(10, 'friend') + .25, 34, 50, left=150)
        typewriter(fr, 'never services their car.', CX, 970, T - T_(10, 'never'), 34, 50, (255, 90, 90), left=150)
    elif T < END:
        shot(fr, 'wreck', T - S[11], END - S[11], 1.25, 1.45, 0, 60, bw=T > T_(11, 'but')); pun = True
        tn = T_(11, 'receipts')
        if T > tn: hero(fr, 'ITS RECEIPTS', CX, 820, T - tn, 128, (240, 240, 236), HB, -.04, .6, 1.0)
        if T > T_(11, 'did'): blurword(fr, 'DID.', CX, 1000, T - T_(11, 'did'), 200)
    else:
        paper_bg(fr); lt = T - END
        big = Image.open('/home/claude/nextbignow-videos/NextBigNow_logo_transparent.png').convert('RGBA'); big.thumbnail((340, 340))
        put_rgba(fr, np.array(big), CX, 820, eout(clamp(lt / .3)), 1.0, 0)
        if plat == 'ig':
            typewriter(fr, 'send this to someone', CX, 1100, lt - .2, 30, 46, (25, 25, 25), False)
            typewriter(fr, 'who loves history.', CX, 1170, lt - .7, 30, 46, REDc)
        else:
            typewriter(fr, 'subscribe for', CX, 1100, lt - .2, 30, 46, (25, 25, 25), False)
            typewriter(fr, 'what happens next.', CX, 1170, lt - .7, 30, 46, REDc)
        finish(fr, T, .5); return fr
    if pun: punch(fr, T)
    if cap: capword(fr, T, 1300 if dark else 1180, dark)
    trans(fr, T)
    finish(fr, T, gr)
    if T < END: credit(fr, 'Research: Charrie-Duhaut et al., Frontiers in Materials (2026). Photos: Wikimedia Commons, illustrative.')
    logo(fr)
    return fr

CUTS[:] = [ (S[2], 'glitch'), (S[3], 'whip'), (T_(3, 'workers') - .05, 'glitch'), (S[4], 'zoom'), (S[5], 'whip'), (S[6], 'glitch'), (S[7], 'flash'),
           (S[8], 'zoom'), (T_(8, 'some from') - .05, 'whip'), (S[9], 'glitch'), (S[10], 'whip'), (S[11], 'zoom'), (END, 'flash')]

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
