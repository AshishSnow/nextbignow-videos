"""FreshNestHub comic-editorial short: bhutta. Cream newsprint + halftone, real photo stickers, ink panels,
small word-synced paper-strip subtitles, FNH leaf logo, no music.
usage: python3 comic.py stills id@frac ... | python3 comic.py seg i0 i1"""
import sys, os, json, math, subprocess, functools
import numpy as np, cairo, cv2
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

D = os.path.dirname(os.path.abspath(__file__))
WM = '/tmp/claude-0/-home-claude/4c982c74-c0ff-5291-9023-17c6a121fb77/scratchpad/wm'
LUCKY = '/home/claude/studio/fonts/comic/LuckiestGuy-Regular.ttf'
ELITE = '/home/claude/studio/fonts/comic/SpecialElite-Regular.ttf'
HI_B = '/home/claude/studio/fonts/hi/baloo-2-800.ttf'
HI_M = '/home/claude/studio/fonts/hi/mukta-700.ttf'
CREAM = (252, 241, 210)
INKC = (28, 22, 20)
CX = W // 2
PAL = dict(red='E63946', blue='2D6CDF', yellow='FFC93C', cyan='3EC1D3', green='3FAE5A', pink='FF7AA8', orange='FF8C1A', purple='8E5CD9')

TL = json.load(open(D + '/timing.json'))
SUBS = json.load(open(D + '/subs.json'))
TOTAL = TL[-1]['start'] + TL[-1]['dur'] + 3.2       # + brand card
BRAND0 = TL[-1]['start'] + TL[-1]['dur'] + 0.2

# ---------------------------------------------------------------- assets
def load_rgba(p, h=None, w=None):
    im = Image.open(p).convert('RGBA')
    if h: im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    if w: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    return np.array(im)

HERO = load_rgba(WM + '/st_hero.png', h=1000)
COB7 = load_rgba(WM + '/st_c7.png', h=620)
COB3 = load_rgba(WM + '/st_c3.png', w=760)
SILK = Image.open(WM + '/silk_panel.jpg').convert('RGB')

@functools.lru_cache(maxsize=16)
def paper(tint=None, dots='D9C9A0'):
    a = np.zeros((H, W, 3), np.uint8); a[:] = CREAM
    if tint:
        col = np.array(hx(tint)[:3]) * 255; a[:] = (a * .25 + col * .75).astype(np.uint8)
    im = Image.fromarray(a); d = ImageDraw.Draw(im)
    dc = tuple(int(v * .82) for v in a[0, 0]) if tint else tuple(int(dots[i:i + 2], 16) for i in (0, 2, 4))
    for y in range(0, H, 22):
        for x in range((y // 22 % 2) * 11, W, 22):
            r = 2.2 + 1.6 * math.sin(x * .004 + y * .003)
            d.ellipse((x - r, y - r, x + r, y + r), fill=dc)
    a = np.array(im).astype(np.int16)
    n = np.random.default_rng(3).integers(-6, 7, (H, W, 1)); a = np.clip(a + n, 0, 255).astype(np.uint8)
    return a

@functools.lru_cache(maxsize=256)
def ttext(txt, size, font, fill='FFFFFF', stroke='1C1614', sw=None, shadow=True):
    sw = max(4, size // 9) if sw is None else sw
    f = ImageFont.truetype(font, size, layout_engine=ImageFont.Layout.RAQM)
    bb = f.getbbox(txt, stroke_width=sw); w, h = bb[2] - bb[0] + 40, bb[3] - bb[1] + 40
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if shadow: d.text((20 - bb[0] + 9, 20 - bb[1] + 10), txt, font=f, fill=(28, 22, 20, 255), stroke_width=sw, stroke_fill=(28, 22, 20, 255))
    d.text((20 - bb[0], 20 - bb[1]), txt, font=f, fill='#' + fill, stroke_width=sw, stroke_fill='#' + stroke)
    return np.array(im)

def title(fr, txt, cy, t, size=120, fill='FFC93C', rot=-2.0, font=HI_B, cx=CX):
    put_rgba(fr, ttext(txt, size, font, fill), cx, cy, back(t / .3), clamp(t / .1), rot)

@functools.lru_cache(maxsize=128)
def tape_img(txt, size, col, font, tcol='1C1614'):
    f = ImageFont.truetype(font, size, layout_engine=ImageFont.Layout.RAQM)
    bb = f.getbbox(txt); w, h = bb[2] - bb[0] + 60, bb[3] - bb[1] + 34
    im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((14, 14, w + 14, h + 14), fill=(28, 22, 20, 140))
    c = hx(col); d.polygon([(4, 6), (w, 2), (w + 4, h), (8, h + 4)], fill=tuple(int(v * 255) for v in c[:3]) + (240,))
    d.text((30 - bb[0], 17 - bb[1]), txt, font=f, fill='#' + tcol)
    return np.array(im)

def tape(fr, txt, cx, cy, t, col='FFC93C', size=46, font=HI_M, rot=-3, tcol='1C1614'):
    if t <= 0: return
    put_rgba(fr, tape_img(txt, size, col, font, tcol), cx, cy, back(t / .3), clamp(t / .1), rot)

@functools.lru_cache(maxsize=32)
def burst_img(txt, r, col, font, size, n=14):
    s = int(r * 2.6); im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c0 = s / 2
    pts = []
    for i in range(n * 2):
        a = i * math.pi / n; rr = r if i % 2 == 0 else r * .68
        pts.append((c0 + math.cos(a) * rr, c0 + math.sin(a) * rr))
    d.polygon([(x + 10, y + 12) for x, y in pts], fill=(28, 22, 20, 255))
    d.polygon(pts, fill='#' + col, outline=(28, 22, 20, 255), width=8)
    t = ttext(txt, size, font, 'FFFFFF', shadow=False); ti = Image.fromarray(t)
    im.alpha_composite(ti, (int(c0 - ti.width / 2), int(c0 - ti.height / 2)))
    return np.array(im)

def burst(fr, txt, cx, cy, t, r=150, col='E63946', font=LUCKY, size=80, rot=8):
    if t <= 0: return
    put_rgba(fr, burst_img(txt, r, col, font, size), cx, cy, back(t / .28), 1.0, rot + 4 * math.sin(t * 6))

def panel(fr, img, cx, cy, w, h, t, rot=-2.0, border=10):
    """photo panel with thick border + offset shadow."""
    if t <= 0: return
    im = Image.fromarray(img) if isinstance(img, np.ndarray) else img
    sc = max(w / im.width, h / im.height); im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
    l, tp = (im.width - w) // 2, (im.height - h) // 2; im = im.crop((l, tp, l + w, tp + h))
    can = Image.new('RGBA', (w + 2 * border + 18, h + 2 * border + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(can)
    d.rectangle((18, 20, w + 2 * border + 17, h + 2 * border + 19), fill=(28, 22, 20, 255))
    d.rectangle((0, 0, w + 2 * border - 1, h + 2 * border - 1), fill=(28, 22, 20, 255))
    can.paste(im.convert('RGBA'), (border, border))
    put_rgba(fr, np.array(can), cx, cy, back(t / .3), 1.0, rot)

def sticker(fr, rgba, cx, cy, T, k=0, sc=1.0, rot=0.0, t=1.0):
    if t <= 0: return
    put_rgba(fr, rgba, cx, cy + 10 * math.sin(T * 2.2 + k), sc * back(t / .3), 1.0, rot + 2 * math.sin(T * 1.6 + k))

def cairo_layer(draw):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND); draw(c)
    buf = np.ndarray((H, W, 4), np.uint8, s.get_data()).copy()
    rgba = np.empty_like(buf); a = buf[..., 3:4].astype(np.float32)
    rgb = np.where(a > 0, buf[..., 2::-1] * 255.0 / np.maximum(a, 1), 0)
    rgba[..., :3] = np.clip(rgb, 0, 255); rgba[..., 3] = buf[..., 3]
    return rgba

def overlay(fr, rgba):
    a = rgba[..., 3:4].astype(np.float32) / 255
    fr[:] = (fr * (1 - a) + rgba[..., :3] * a).astype(np.uint8)

def shake(T, at, dur=.35, amp=18):
    k = (T - at) / dur
    if 0 <= k < 1: return amp * (1 - k) * math.sin(T * 90), amp * (1 - k) * math.cos(T * 77)
    return 0, 0

# ---------------------------------------------------------------- drawn props (ink)
def ink(c, w=7): c.set_source_rgba(*hx('1C1614')); c.set_line_width(w)

def eye(c, x, y, r, T, glow=0.0):
    c.save(); c.translate(x, y)
    c.arc(14, 16, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(0, 0, r, 0, 2 * math.pi); c.set_source_rgba(*hx('FFFFFF')); c.fill_preserve(); ink(c, 9); c.stroke()
    # lens at left, retina back wall
    c.arc(0, 0, r * .9, math.radians(-70), math.radians(70)); c.set_source_rgba(*hx('FF8A80')); c.set_line_width(26); c.stroke()
    c.save(); c.translate(-r * .82, 0); c.scale(.35, 1); c.arc(0, 0, r * .42, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('9FD8FF')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(-r * 1.0, 0, r * .28, math.radians(110), math.radians(250)); c.set_source_rgba(*hx('2D6CDF')); c.set_line_width(14); c.stroke()
    # macula spot
    gx = r * .9; c.arc(gx, 0, 26 + 10 * glow, 0, 2 * math.pi); c.set_source_rgba(*hx('FFC93C')); c.fill_preserve(); ink(c, 6); c.stroke()
    if glow > 0:
        for k in range(10):
            a = k * math.pi / 5 + T; c.move_to(gx + math.cos(a) * 46, math.sin(a) * 46); c.line_to(gx + math.cos(a) * (64 + 12 * glow), math.sin(a) * (64 + 12 * glow))
            c.set_source_rgba(*hx('FFC93C', glow)); c.set_line_width(7); c.stroke()
    c.move_to(r, 0); c.line_to(r + 90, 30); ink(c, 12); c.stroke()   # optic nerve
    c.restore()

def pot(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    for k in range(3):
        c.move_to(-60 + k * 60, -120); c.curve_to(-90 + k * 60, -180, -30 + k * 60, -200, -60 + k * 60, -260 - 15 * math.sin(T * 3 + k))
        c.set_source_rgba(1, 1, 1, .85); c.set_line_width(12); c.stroke()
    c.rectangle(-150, -110, 300, 200); c.set_source_rgba(*hx('B8C2CC')); c.fill_preserve(); ink(c); c.stroke()
    c.rectangle(-170, -120, 340, 26); c.set_source_rgba(*hx('8A94A3')); c.fill_preserve(); ink(c, 6); c.stroke()
    for k in range(9): c.move_to(-120 + k * 30, -112); c.curve_to(-110 + k * 30, -80, -130 + k * 30, -60, -115 + k * 30, -40); c.set_source_rgba(*hx('E8D27A')); c.set_line_width(5); c.stroke()
    for k in range(5): c.move_to(-110 + k * 55, 120); c.curve_to(-90 + k * 55, 150 + 10 * math.sin(T * 9 + k), -130 + k * 55, 170, -110 + k * 55, 200); c.set_source_rgba(*hx('FF8C1A')); c.set_line_width(14); c.stroke()
    c.restore()

def strainer(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-130, -60); c.curve_to(-130, 90, 130, 90, 130, -60); c.close_path(); c.set_source_rgba(*hx('D9DDE3')); c.fill_preserve(); ink(c); c.stroke()
    for i in range(-110, 120, 22):
        c.move_to(i, -55); c.line_to(i * .8, 50); c.set_source_rgba(*hx('8A94A3')); c.set_line_width(3); c.stroke()
    c.move_to(130, -60); c.line_to(300, -100); ink(c, 18); c.stroke()
    for k in range(6):
        dy = ((T * 1.6 + k / 6) % 1) * 160; c.arc(-40 + k * 16, 90 + dy, 9, 0, 2 * math.pi); c.set_source_rgba(*hx('E8D27A')); c.fill()
    c.restore()

def mishri_glass(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-90, -150); c.line_to(90, -150); c.line_to(70, 150); c.line_to(-70, 150); c.close_path(); c.set_source_rgba(*hx('EAF6FF', .8)); c.fill_preserve(); ink(c); c.stroke()
    c.move_to(-82, -60); c.line_to(82, -60); c.line_to(70, 145); c.line_to(-70, 145); c.close_path(); c.set_source_rgba(*hx('F3E08A')); c.fill()
    for k, (mx, my) in enumerate(((150, 60), (200, 120), (150, 150))):
        c.save(); c.translate(mx, my); c.rotate(k * .6); c.rectangle(-26, -26, 52, 52); c.set_source_rgba(*hx('FFFFFF')); c.fill_preserve(); ink(c, 5); c.stroke(); c.restore()
    c.restore()

def flask(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-40, -200); c.line_to(40, -200); c.line_to(40, -60); c.line_to(140, 160); c.line_to(-140, 160); c.line_to(-40, -60); c.close_path()
    c.set_source_rgba(*hx('EAF6FF', .85)); c.fill_preserve(); ink(c); c.stroke()
    c.move_to(-90, 60); c.line_to(90, 60); c.line_to(140, 160); c.line_to(-140, 160); c.close_path(); c.set_source_rgba(*hx('3FAE5A')); c.fill()
    for k in range(5):
        dy = ((T * .8 + k / 5) % 1) * 160; c.arc(-50 + k * 25, 150 - dy, 10, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, .7); c.fill()
    c.restore()

def mouse(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(140, 20); c.curve_to(230, 0, 260, 80, 320, 40); c.set_source_rgba(*hx('FF9EB5')); c.set_line_width(10); c.stroke()
    c.save(); c.scale(1.5, 1); c.arc(0, 0, 100, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('E3E7EE')); c.fill_preserve(); ink(c); c.stroke()
    for ex in (-110, -40):
        c.arc(ex, -90, 42, 0, 2 * math.pi); c.set_source_rgba(*hx('FFB0C8')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(-120, -10, 12, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(-160, 20, 10, 0, 2 * math.pi); c.set_source_rgba(*hx('FF7AA8')); c.fill()
    c.restore()

def person_q(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.arc(0, -150, 80, 0, 2 * math.pi); c.set_source_rgba(*hx('F2B48A')); c.fill_preserve(); ink(c); c.stroke()
    c.move_to(-130, 160); c.curve_to(-130, -40, 130, -40, 130, 160); c.close_path(); c.set_source_rgba(*hx('2D6CDF')); c.fill_preserve(); ink(c); c.stroke()
    c.restore()

def doctor(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-170, 220); c.curve_to(-170, 10, 170, 10, 170, 220); c.close_path(); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c); c.stroke()
    c.move_to(-30, 30); c.line_to(0, 120); c.line_to(30, 30); c.set_source_rgba(*hx('3EC1D3')); c.fill()
    c.arc(0, -100, 95, 0, 2 * math.pi); c.set_source_rgba(*hx('F2B48A')); c.fill_preserve(); ink(c); c.stroke()
    c.arc(0, -150, 98, math.pi, 2 * math.pi); c.set_source_rgba(*hx('3A2418')); c.fill()
    for ex in (-35, 35): c.arc(ex, -100, 10, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(0, -65, 30, .2, math.pi - .2); ink(c, 7); c.stroke()
    c.move_to(-70, 40); c.curve_to(-90, 140, 60, 150, 60, 100); ink(c, 8); c.stroke(); c.arc(60, 92, 16, 0, 2 * math.pi); c.set_source_rgba(*hx('8A94A3')); c.fill()
    c.rectangle(80, 60, 70, 70); c.set_source_rgba(*hx('E63946')); c.fill(); c.rectangle(105, 70, 20, 50); c.set_source_rgba(1, 1, 1, 1); c.fill(); c.rectangle(90, 85, 50, 20); c.fill()
    c.restore()

def phone_s(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-150 + 16, -290 + 18, 300, 580); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-150, -290, 300, 580); c.set_source_rgba(*hx('2A2D3A')); c.fill_preserve(); ink(c); c.stroke()
    c.rectangle(-125, -250, 250, 500); c.set_source_rgba(*hx('EAF6FF')); c.fill()
    c.restore()

def logo(c, x, y, r):
    c.save(); c.translate(x, y)
    c.arc(6, 8, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614', .6)); c.fill()
    c.arc(0, 0, r, 0, 2 * math.pi); c.set_source_rgba(*hx('FFF8E7')); c.fill_preserve(); c.set_source_rgba(*hx('1F5B3A')); c.set_line_width(r * .1); c.stroke()
    for sx, col in ((-1, '1F7A45'), (1, '2E9E5B')):
        c.save(); c.scale(sx, 1); c.move_to(0, r * .45); c.curve_to(r * .05, -r * .05, r * .35, -r * .5, r * .62, -r * .48)
        c.curve_to(r * .6, -r * .1, r * .35, r * .3, 0, r * .45); c.close_path(); c.set_source_rgba(*hx(col)); c.fill(); c.restore()
    c.move_to(0, r * .5); c.line_to(0, r * .05); c.set_source_rgba(*hx('FFF8E7')); c.set_line_width(r * .05); c.stroke()
    c.restore()

# ---------------------------------------------------------------- subtitles
@functools.lru_cache(maxsize=512)
def sub_img(words, hi):
    f = ImageFont.truetype(HI_M, 38, layout_engine=ImageFont.Layout.RAQM)
    ws = words.split(' '); sp = 12; widths = [f.getlength(w) for w in ws]
    tw = int(sum(widths) + sp * (len(ws) - 1)); w, h = tw + 90, 74
    im = Image.new('RGBA', (w + 14, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((12, 12, w + 12, h + 12), fill=(28, 22, 20, 120))
    d.polygon([(0, 4), (w, 0), (w - 2, h), (2, h - 2)], fill=(255, 250, 235, 255), outline=(28, 22, 20, 255), width=3)
    d.ellipse((18, h / 2 - 9, 36, h / 2 + 9), fill=(230, 57, 70, 255))
    x = 56
    for i, wd in enumerate(ws):
        if i == hi:
            d.rectangle((x - 6, 12, x + widths[i] + 6, h - 12), fill=(255, 201, 60, 255))
        d.text((x, h / 2 - 2), wd, font=f, fill=(28, 22, 20, 255), anchor='lm')
        x += widths[i] + sp
    return np.array(im)

def subtitle(fr, T):
    for g in SUBS:
        if g['s'] <= T < g['e']:
            hi = max([i for i, ts in enumerate(g['t']) if ts <= T] or [0])
            put_rgba(fr, sub_img(' '.join(g['w']), hi), CX, 1440, 1.0, 1.0, -1.2); return

# ---------------------------------------------------------------- credits + logo
@functools.lru_cache(maxsize=4)
def credit_img(txt):
    f = ImageFont.truetype(ELITE, 20); bb = f.getbbox(txt)
    im = Image.new('RGBA', (bb[2] + 20, bb[3] + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((10, 4), txt, font=f, fill=(28, 22, 20, 190)); return np.array(im.rotate(90, expand=True))

CREDIT = 'Photos: Shikha Sh, Manjeshwari poet mysore, Namitakhaire, Rasbak / Wikimedia Commons, CC BY-SA'

LOGO = cairo_layer(lambda c: logo(c, 112, 316, 52))
@functools.lru_cache(maxsize=2)
def logo_word():
    return ttext('FreshNestHub', 34, LUCKY, 'FFFFFF', sw=5, shadow=False)

# ---------------------------------------------------------------- scenes
def L(i): return TL[i]
SC = {l['id']: l for l in TL}

def sc_hook(fr, T, t, l):
    k = l['id']; dx, dy = shake(T, SC['h3']['start'] + .2, .4, 22)
    fr[:] = paper('FFC93C' if k in ('h1', 'h2') else 'FFB0C8' if k == 'h3' else None)
    hk = T  # time since video start
    sticker(fr, HERO, CX + dx, 1030 + dy, T, 0, .78, -8)
    title(fr, 'भुट्टा मत खाना?!', 540, hk + 1.0, 128, 'FFFFFF', -2.5)
    burst(fr, '?!', 860, 820, hk + 1.0, 120, 'E63946', LUCKY, 90)
    if T >= SC['h2']['start']:
        tape(fr, 'मक्का', 270, 900, T - SC['h2']['start'] - .2, 'FFFFFF', 54, rot=-6)
        tape(fr, 'भुट्टा', 820, 1180, T - SC['h2']['start'] - .9, 'FFFFFF', 54, rot=5)
    if T >= SC['h3']['start'] + .2:
        burst(fr, 'NO!', 300, 1250, T - SC['h3']['start'] - .2, 140, '2D6CDF', LUCKY, 92, -10)
    if T >= SC['h4']['start']:
        tape(fr, 'मिलेगा ही क्या?', CX + 150, 1300, T - SC['h4']['start'] - .2, 'FFC93C', 58, rot=-2)

def sc_f1(fr, T, t, l):
    fr[:] = paper()
    title(fr, 'मिलेगा क्या?', 520, t, 116, 'FFC93C', -2)
    sticker(fr, COB3, CX, 760, T, 1, .95, -4, t)
    cards = (('फ़ाइबर', 'E63946', .1), ('प्रोटीन', '2D6CDF', 1.0), ('B विटामिन', '3FAE5A', 2.9))
    for i, (txt, col, at) in enumerate(cards):
        tk = t - at
        if tk > 0:
            x = 230 + i * 310; y = 1100 + (30 if i == 1 else 0)
            def dr(c, x=x, y=y, col=col):
                c.rectangle(x - 130 + 14, y - 110 + 16, 260, 220); c.set_source_rgba(*hx('1C1614')); c.fill()
                c.rectangle(x - 130, y - 110, 260, 220); c.set_source_rgba(*hx('FFF8E7')); c.fill_preserve(); ink(c, 8); c.stroke()
                c.rectangle(x - 130, y - 110, 260, 56); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()
            lay = cairo_layer(dr); sc = back(tk / .3)
            if sc < .999:
                M = cv2.getRotationMatrix2D((x, y), (-3 + 3 * i), sc); lay = cv2.warpAffine(lay, M, (W, H))
            overlay(fr, lay)
            put_rgba(fr, ttext(txt, 50, HI_B, 'FFFFFF', sw=6), x, y + 30, sc, 1.0, -3 + 3 * i)
            put_rgba(fr, ttext('थोड़ा' if i < 2 else 'कुछ', 30, HI_M, 'FFFFFF', sw=4, shadow=False), x, y - 82, sc, 1.0, -3 + 3 * i)

def sc_f2(fr, T, t, l):
    fr[:] = paper('3EC1D3')
    title(fr, '2 खास कैरोटीनॉइड्स', 520, t, 92, 'FFFFFF', -2)
    sticker(fr, COB7, 300, 1050, T, 2, .9, 10, t)
    tape(fr, 'LUTEIN', 760, 920, t - 3.5, 'FFC93C', 56, ELITE, 4)
    tape(fr, 'ZEAXANTHIN', 740, 1080, t - 3.9, 'FF8C1A', 50, ELITE, -3)
    if t > 3.6: burst(fr, '2!', 880, 760, t - 3.6, 90, 'E63946', LUCKY, 76)

def sc_f3(fr, T, t, l):
    fr[:] = paper('2D6CDF')
    title(fr, 'आँख का परदा', 520, t, 112, 'FFC93C', -2)
    glow = clamp((t - 1.5) / .8)
    overlay(fr, cairo_layer(lambda c: eye(c, CX - 60, 1000, 260, T, glow)))
    if t > 1.5:
        tape(fr, 'मैक्युला', CX + 250, 820, t - 1.5, 'FFC93C', 56, rot=4)
    if t > 3.2: tape(fr, 'आँखों के लिए अच्छे माने जाते हैं', CX, 1290, t - 3.2, 'FFFFFF', 44, rot=-2)

def sc_f4(fr, T, t, l):
    fr[:] = paper('FFC93C')
    sticker(fr, HERO, CX, 1040, T, 3, .7, 6, t + 1)
    title(fr, 'इससे ज़्यादा... क्या?', 520, t, 104, 'FFFFFF', -2)
    burst(fr, 'HA!', 820, 800, t - .2, 120, 'FF7AA8', LUCKY, 86)

def sc_s1(fr, T, t, l):
    fr[:] = paper('3FAE5A')
    title(fr, 'भुट्टे के बाल', 520, t, 124, 'FFC93C', -2)
    panel(fr, SILK, CX, 1000, 700, 560, t - .3, 2.5)
    if t > 2.6:
        tape(fr, 'कचरा?', 300, 1310, t - 2.6, 'FFFFFF', 64, rot=-6)
        if t > 3.1: burst(fr, 'X', 300, 1310, t - 3.1, 90, 'E63946', LUCKY, 90)

def sc_s2(fr, T, t, l):
    fr[:] = paper()
    title(fr, 'बहुत लोग कहते हैं...', 520, t, 96, 'FF8C1A', -2)
    steps = ((pot, 'उबालो', 2.1, 'FF7AA8'), (strainer, 'छानो', 2.85, '3EC1D3'), (mishri_glass, 'मिश्री', 3.6, 'FFC93C'))
    for i, (fn, txt, at, col) in enumerate(steps):
        tk = t - at
        if tk > 0:
            x = 220 + i * 320; y = 1000 + (40 if i == 1 else 0)
            def dr(c, x=x, y=y, fn=fn, col=col):
                c.rectangle(x - 150 + 14, y - 190 + 16, 300, 380); c.set_source_rgba(*hx('1C1614')); c.fill()
                c.rectangle(x - 150, y - 190, 300, 380); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 8); c.stroke()
                fn(c, x - (40 if fn is strainer else 0), y + 10, .55, T)
            lay = cairo_layer(dr); sc = back(tk / .3)
            if sc < .999: lay = cv2.warpAffine(lay, cv2.getRotationMatrix2D((x, y), -2 + 2 * i, sc), (W, H))
            overlay(fr, lay); tape(fr, txt, x, y + 230, tk - .1, 'FFFFFF', 48, rot=-3 + 3 * i)

def sc_s3(fr, T, t, l):
    fr[:] = paper('FFC93C')
    title(fr, 'दावा', 470, t, 110, 'FFFFFF', -3)
    def card(y, txt, at, col):
        tk = t - at
        if tk > 0: put_rgba(fr, tape_img(txt, 60, col, HI_B), CX - 60, y, back(tk / .3), 1.0, -2)
    card(820, 'जलन 1-2 बार में शांत?', .2, 'FFFFFF')
    card(1060, 'पथरी टूटकर बाहर?', 3.0, 'FFFFFF')
    burst(fr, '?', 900, 820, t - .9, 80, 'E63946', LUCKY, 90)
    burst(fr, '?', 880, 1060, t - 3.6, 80, '2D6CDF', LUCKY, 90)
    sticker(fr, COB7, 220, 1260, T, 4, .4, -25, t)

def sc_r1(fr, T, t, l):
    dx, dy = shake(T, l['start'] + .05, .4, 24)
    fr[:] = paper('FF7AA8')
    if t < .12: fr[:] = (fr * .3 + 255 * .7).astype(np.uint8)
    title(fr, 'रुको!', 500 + dy, t, 170, 'FFFFFF', -4)
    def dr(c):
        c.rectangle(110 + 14, 700 + 16, 860, 520); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.rectangle(110, 700, 860, 520); c.set_source_rgba(*hx('FFF8E7')); c.fill_preserve(); ink(c, 9); c.stroke()
        flask(c, 340, 980, .9, T); mouse(c, 720, 1050, .75, T)
    if t > .6: overlay(fr, cairo_layer(dr))
    tape(fr, 'रिसर्च: लैब + जानवर', CX, 1300, t - 1.4, 'FFC93C', 54, rot=-2)

def sc_r2(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 1.4, .4, 22)
    fr[:] = paper('8E5CD9')
    overlay(fr, cairo_layer(lambda c: person_q(c, CX + dx, 1000 + dy, 1.4, T)))
    burst(fr, '?', CX + 220, 760, t - .3, 100, 'FFC93C', LUCKY, 110)
    title(fr, 'इंसानों में', 500, t, 110, 'FFFFFF', -2)
    if t > 1.4: put_rgba(fr, tape_img('पक्का सबूत नहीं', 70, 'E63946', HI_B, 'FFFFFF'), CX + dx, 1290 + dy, back((t - 1.4) / .25), 1.0, -4)

def sc_r3(fr, T, t, l):
    fr[:] = paper('3EC1D3')
    title(fr, 'जलन = अक्सर इन्फ़ेक्शन', 520, t, 86, 'FFFFFF', -2)
    overlay(fr, cairo_layer(lambda c: doctor(c, CX, 1040, 1.25 * back(min(1, t / .35)) if t < .35 else 1.25, T)))
    tape(fr, 'इलाज: डॉक्टर की दवा', CX, 1300, t - 2.5, 'FFC93C', 56, rot=-2)

def sc_e1(fr, T, t, l):
    fr[:] = paper('FFC93C')
    sticker(fr, HERO, 360, 1030, T, 5, .62, -14, t + 1)
    sticker(fr, COB7, 780, 1060, T, 6, .78, 12, t)
    title(fr, 'भुट्टा मज़े से खाओ!', 520, t, 108, 'FFFFFF', -2)
    tape(fr, 'जलन हो? तो डॉक्टर', CX, 1300, t - 1.6, '3EC1D3', 56, rot=-2)

def sc_e2(fr, T, t, l):
    fr[:] = paper('FF7AA8')
    overlay(fr, cairo_layer(lambda c: phone_s(c, CX - 140, 1000, 1.0, T)))
    sticker(fr, COB3, CX - 140, 1000, T, 7, .38, -70, t)
    title(fr, 'भेजो उस दोस्त को', 520, t, 104, 'FFFFFF', -2)
    tape(fr, 'जो भुट्टे का शौक़ीन है', CX + 160, 1300, t - .9, 'FFC93C', 52, rot=3)
    burst(fr, 'SEND!', 830, 900, t - .5, 120, '3FAE5A', LUCKY, 60)

def sc_brand(fr, T, t):
    fr[:] = paper('3FAE5A')
    overlay(fr, cairo_layer(lambda c: logo(c, CX, 860, 200 * back(min(1, t / .4)) if t < .4 else 200)))
    title(fr, 'FreshNestHub', 1150, t - .3, 110, 'FFFFFF', -2, LUCKY)
    tape(fr, '@fnhtruths  |  @FreshnestHub', CX, 1300, t - .7, 'FFC93C', 40, ELITE, -1)

SCENES = dict(h1=sc_hook, h2=sc_hook, h3=sc_hook, h4=sc_hook, f1=sc_f1, f2=sc_f2, f3=sc_f3, f4=sc_f4, s1=sc_s1, s2=sc_s2, s3=sc_s3,
              r1=sc_r1, r2=sc_r2, r3=sc_r3, e1=sc_e1, e2=sc_e2)

def frame(T):
    fr = np.zeros((H, W, 3), np.uint8)
    if T >= BRAND0:
        sc_brand(fr, T, T - BRAND0)
    else:
        l = TL[0]
        for x in TL:
            if x['start'] <= T: l = x
        t = T - l['start']
        SCENES[l['id']](fr, T, t, l)
        # whip-in on scene change (not between hook parts)
        if 0 <= t < .14 and l['id'] not in ('h1', 'h2', 'h3', 'h4'):
            k = 1 - t / .14; sh = int(k * 120); fr[:] = np.roll(fr, sh, axis=1)
            fr[:] = (fr * (1 - .35 * k) + 255 * .35 * k).astype(np.uint8)
        subtitle(fr, T)
    overlay(fr, LOGO)
    put_rgba(fr, logo_word(), 112 + 200, 316, 1.0, 1.0, -2)
    if T < BRAND0: put_rgba(fr, credit_img(CREDIT), 30, 960, 1.0, 1.0, 0)
    return fr

def seg(i0, i1):
    os.makedirs(D + '/segs', exist_ok=True)
    f0, f1 = int(i0 * FPS), int(min(i1, TOTAL) * FPS)
    tmp = f'{D}/segs/seg_{i0:05.1f}.tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for fi in range(f0, f1): p.stdin.write(frame(fi / FPS).tobytes())
    p.stdin.close(); p.wait(); os.rename(tmp, tmp.replace('.tmp', ''))

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for a in sys.argv[2:]:
            T = float(a); Image.fromarray(frame(T)).save(f'/tmp/cs_{a}.png')
    elif sys.argv[1] == 'seg':
        seg(float(sys.argv[2]), float(sys.argv[3]))
    elif sys.argv[1] == 'total':
        print(TOTAL)
