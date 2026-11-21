import sys, os, json, math
sys.path.insert(0, '/home/claude/myco')
from kit import *
D = '/home/claude/myco'
L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + 0.3; TOTAL = END + 2.6
def wt(i, frac): return S[i] + L[i]['dur'] * frac
def wfind(i, word):
    tx = L[i]['text'].lower(); k = tx.find(word.lower()); return wt(i, k / max(1, len(tx)))
def st(name, **kw):
    return load_st(name, **kw) if os.path.exists(f'{D}/st/{name}.png') else None
PHOTO = {}
def photo(name, w, h, focus=(.5, .5)):
    k = (name, w, h, focus)
    if k not in PHOTO:
        p = f'{D}/ph/{name}.jpg'
        PHOTO[k] = panel_img(comic_photo(p, w, h, focus)) if os.path.exists(p) else None
    return PHOTO[k]
exec(open(D + '/common_part.py').read())
def chip(fr, txt, cx, cy, t, col=CYAN, size=40, rot=0): tape(fr, txt, cx, cy, t, col=col, size=size, font=INTER, rot=rot)
def sk(fr, im, x, y, T, k, sc, rot=0, t=1.0):
    if im is not None: sticker(fr, im, x, y, T, k, sc, rot, t)
def stat(fr, big, small, cx, cy, t, col=RED, rot=-3, size=130):
    if t <= 0: return
    title(fr, big, cy, t, size=size, fill='FFFFFF' if col == RED else YEL, rot=rot, cx=cx)
    tape(fr, small, cx, cy + size * .8, t - .1, col=col, size=40, font=LUCKY, rot=rot + 1, tcol='FFFFFF' if col == RED else '1C1614')

BURG = st('vburger', w=560)
def _carton():
    S_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, 420, 700); c = cairo.Context(S_); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.move_to(60 + 14, 160 + 16); c.line_to(360 + 14, 160 + 16); c.line_to(360 + 14, 660 + 16); c.line_to(60 + 14, 660 + 16); c.close_path(); c.set_source_rgba(.11, .09, .08, 1); c.fill()
    c.move_to(60, 160); c.line_to(210, 40); c.line_to(360, 160); c.line_to(360, 660); c.line_to(60, 660); c.close_path(); c.set_source_rgba(.98, .96, .9, 1); c.fill_preserve(); c.set_source_rgba(.11, .09, .08, 1); c.set_line_width(10); c.stroke()
    c.rectangle(60, 300, 300, 220); c.set_source_rgba(.24, .68, .35, 1); c.fill_preserve(); c.set_source_rgba(.11, .09, .08, 1); c.set_line_width(7); c.stroke()
    for k in range(5): c.move_to(120 + k * 45, 470); c.curve_to(110 + k * 45, 400, 140 + k * 45, 360, 125 + k * 45, 330); c.set_source_rgba(.98, .85, .4, 1); c.set_line_width(9); c.stroke()
    buf = np.ndarray((700, 420, 4), np.uint8, S_.get_data()).copy(); a = buf[..., 3:4].astype(np.float32)
    out = np.empty_like(buf); out[..., :3] = np.clip(np.where(a > 0, buf[..., 2::-1] * 255.0 / np.maximum(a, 1), 0), 0, 255); out[..., 3] = buf[..., 3]
    im = Image.fromarray(out); ImageDraw.Draw(im).text((210, 230), 'OAT', font=ImageFont.truetype(LUCKY, 80), fill=INK, anchor='mm'); return np.array(im)
OAT = _carton(); SAUS = None; GRAIN = None; BEANS = None

def spores(c, cx, cy, r, T, a=1.0, n=26):
    rng = np.random.default_rng(9)
    for k in range(n):
        ang = rng.uniform(0, 2 * math.pi); d = rng.uniform(0, r * .85); x = cx + math.cos(ang) * d + 6 * math.sin(T * 2 + k); y = cy + math.sin(ang) * d + 6 * math.cos(T * 2.3 + k)
        s = rng.uniform(10, 26)
        c.move_to(x, y); c.line_to(x + rng.uniform(-30, 30), y + rng.uniform(-30, 30)); c.set_source_rgba(*hx('3F6B3A', a)); c.set_line_width(4); c.stroke()
        c.arc(x, y, s, 0, 2 * math.pi); c.set_source_rgba(*hx(['7FB069', '9BC53D', 'C3D350'][k % 3], a)); c.fill_preserve(); ink(c, 3, a); c.stroke()

def lens(c, cx, cy, r, T, a=1.0):
    c.arc(cx + 12, cy + 14, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614', a)); c.fill()
    c.arc(cx, cy, r, 0, 2 * math.pi); c.set_source_rgba(*hx('F4F1DE', a)); c.fill()
    c.save(); c.arc(cx, cy, r, 0, 2 * math.pi); c.clip(); spores(c, cx, cy, r, T, a); c.restore()
    c.arc(cx, cy, r, 0, 2 * math.pi); ink(c, 18, a); c.stroke()
    c.move_to(cx + r * .7, cy + r * .7); c.line_to(cx + r * 1.15, cy + r * 1.15); ink(c, 40, a); c.stroke()

def stack_bar(c, T, t0, x=CX, base=1300, n=8, step=.45):
    for k in range(n):
        p = eout((T - t0 - k * step) / .3)
        if p <= 0: continue
        y = base - k * 64 - 60 * (1 - p)
        c.rectangle(x - 160 + 8, y - 28 + 10, 320, 56); c.set_source_rgba(*hx('1C1614', p)); c.fill()
        c.rectangle(x - 160, y - 28, 320, 56); c.set_source_rgba(*hx(['9BC53D', 'C3D350', 'FFC93C', 'FF8C1A', 'E63946'][min(4, k // 2)], p)); c.fill_preserve(); ink(c, 5, p); c.stroke()
    lim = base - 8 * 64 - 30
    c.move_to(x - 260, lim); c.line_to(x + 260, lim); c.set_source_rgba(*hx(RED)); c.set_line_width(8); c.set_dash([20, 12]); c.stroke(); c.set_dash([])

def s_hook(fr, T):
    fr[:] = paper(GREEN, .6); rays(fr, T, 'FFFFFF', .14, cy=1060)
    sk(fr, OAT, 330, 1060, T, 0, .85, -8); sk(fr, BURG, 770, 1150, T, 1, .8, 6)
    overlay(fr, cairo_layer(lambda c: lens(c, 720, 860, 150 * eout(T / .8), T)))
    tape(fr, 'EVERY ONE THEY TESTED', CX, 470, 1.0, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    title(fr, 'HAD FUNGUS TOXINS', 600, 1.0, size=98, fill=YEL, rot=-3)

def s_question(fr, T):
    lt = T - S[1]; fr[:] = paper(BLUE, .66); rays(fr, T, 'FFFFFF', .1)
    sk(fr, OAT, 310, 1060, T, 2, .75, -6, lt); sk(fr, BURG, 780, 1080, T, 3, .75, 5, lt - .2)
    burst(fr, '?!', CX, 860, lt - .6, r=90, col=RED, size=70)
    tape(fr, "WHAT'S HIDING IN", CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    title(fr, 'YOUR OAT MILK?', 590, lt - .15, size=108, fill=YEL)

def s_bought(fr, T):
    lt = T - S[2]; fr[:] = paper(None); rays(fr, T, YEL, .16)
    t212 = wfind(2, 'two hundred')
    if T > t212: stat(fr, '212', 'PRODUCTS FROM UK SHELVES', CX, 560, T - t212, RED, -3, 150)
    sk(fr, BURG, 300, 1000, T, 4, .62, -6, T - wfind(2, 'burgers') + .2)
    chip(fr, 'VEGAN SAUSAGES', 790, 900, T - wfind(2, 'sausages'), YEL, 38, 3)
    sk(fr, OAT, 790, 1150, T, 6, .55, 5, T - wfind(2, 'oat') + .2)
    chip(fr, 'ALMOND + SOY MILK', 780, 1270, T - wfind(2, 'almond'), 'FFFFFF', 38, 3)
    tape(fr, 'SCIENTISTS BOUGHT', CX, 420, lt, col='FFFFFF', size=52, font=LUCKY, rot=-2)

def s_all(fr, T):
    lt = T - S[3]; fr[:] = paper(RED, .74); rays(fr, T, 'FFFFFF', .12)
    ph = photo('mold', 560, 560)
    if ph is not None: put_rgba(fr, ph, CX, 1030, back(clamp(lt / .4)), 1.0, -3)
    else: overlay(fr, cairo_layer(lambda c: lens(c, CX, 1030, 260 * back(clamp(lt / .4)), T)))
    chip(fr, 'MOLD UNDER A MICROSCOPE', CX, 1330, lt - .5, 'FFFFFF', 32, 2)
    title(fr, '212 / 212', 560, lt, size=150, fill='FFFFFF', rot=-3)
    tape(fr, 'HAD A MYCOTOXIN', CX, 690, lt - .3, col=YEL, size=50, font=LUCKY, rot=2)
    if T > S[4]: burst(fr, 'EVERY ONE', 830, 1280, T - S[4], r=130, col=YEL, size=40)

def s_twist(fr, T):
    lt = T - S[5]; fr[:] = paper('2A2F5A', .82); rays(fr, T, YEL, .1)
    title(fr, 'BEFORE YOU', 860, lt, size=150, fill='FFFFFF'); title(fr, 'PANIC...', 1050, lt - .12, size=170, fill=YEL)
    if T > wfind(5, 'nobody'): chip(fr, "THE PART NOBODY'S POSTING", CX, 1250, T - wfind(5, 'nobody'), RED, 42, -2)

def s_below(fr, T):
    lt = T - S[6]; fr[:] = paper(GREEN, .55); rays(fr, T, 'FFFFFF', .14)
    overlay(fr, cairo_layer(lambda c: stack_bar(c, T, S[6] + .2, n=3, step=.25)))
    tape(fr, 'ALL BELOW SAFETY LIMITS', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    chip(fr, 'SAFETY LIMIT', 820, 1300 - 8 * 64 - 80, lt - .4, RED, 34, 0)
    burst(fr, 'PHEW', 260, 760, lt - .8, r=100, col=GREEN, size=50)

def s_stack(fr, T):
    lt = T - S[7]; fr[:] = paper(YEL, .55); rays(fr, T, 'FFFFFF', .12)
    overlay(fr, cairo_layer(lambda c: stack_bar(c, T, S[7] + .8, n=8, step=.55)))
    chip(fr, 'SAFETY LIMIT', 820, 1300 - 8 * 64 - 80, lt, RED, 34, 0)
    tape(fr, 'THE REAL PROBLEM: STACKING', CX, 470, lt, col=RED, size=50, font=LUCKY, rot=-2, tcol='FFFFFF')
    for k, txt in enumerate(('OAT LATTE', 'VEGGIE BURGER', 'SOY MILK', 'VEGAN SAUSAGE')):
        chip(fr, txt, 230 if k % 2 == 0 else 850, 760 + k * 130, lt - .8 - k * .55, 'FFFFFF', 28, (-3, 3)[k % 2])

def s_field(fr, T):
    lt = T - S[8]; fr[:] = paper('8EC5FF', .55); rays(fr, T, 'FFFFFF', .12)
    ph = photo('silo', 700, 460, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1210, back(clamp((T - wfind(8, 'storage')) / .35)), 1.0, 2)
    for nm, w, x, rot in (('grain', 'grains', 300, -4), ('beans', 'beans', 780, 4)):
        ph2 = photo(nm, 400, 320); tw = wfind(8, w)
        if ph2 is not None and T > tw - .2: put_rgba(fr, ph2, x, 860, back(clamp((T - tw + .2) / .3)), 1.0, rot)
    overlay(fr, cairo_layer(lambda c: spores(c, CX, 880, 420, T, clamp(lt / 1.0), 18)))
    tape(fr, 'MOLD GETS IN EARLY', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    chip(fr, 'IN THE FIELD + IN STORAGE', CX, 600, T - wfind(8, 'field'), YEL, 40, 2)

def s_next(fr, T):
    lt = T - S[9]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHAT', 860, lt, size=170, fill='FFFFFF'); title(fr, 'HAPPENS NEXT?', 1060, lt - .15, size=130, fill=YEL)

def s_rules(fr, T):
    lt = T - S[10]; fr[:] = paper(None); rays(fr, T, RED, .1)
    def book(c):
        c.rectangle(CX - 240 + 14, 800 + 16, 480, 520); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.rectangle(CX - 240, 800, 480, 520); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 9); c.stroke()
        for k in range(6): c.move_to(CX - 180, 880 + k * 70); c.line_to(CX + 180, 880 + k * 70); ink(c, 4, .2); c.stroke()
    overlay(fr, cairo_layer(book))
    put_rgba(fr, ttext('RULEBOOK', 56, LUCKY, '1C1614', 'FFFFFF', shadow=False), CX, 860, 1.0, 1.0, 0)
    tape(fr, 'MYCOTOXIN RULES FOR NEW FOODS?', CX, 470, lt, col='FFFFFF', size=44, font=LUCKY, rot=-2)
    if T > wfind(10, 'no rules'): burst(fr, 'NONE YET', CX, 1100, T - wfind(10, 'no rules'), r=150, col=RED, size=48)

def s_catch(fr, T):
    lt = T - S[11]; fr[:] = paper(CYAN, .55); rays(fr, T, 'FFFFFF', .14)
    ph = photo('lab', 760, 520, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1010, back(clamp(lt / .35)), 1.0, -2)
    tape(fr, 'SCIENTISTS WANT TESTING', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    if T > wfind(11, 'menu'): title(fr, 'TO CATCH UP', 600, T - wfind(11, 'menu') + .4, size=110, fill=YEL)

def s_mix(fr, T):
    lt = T - S[12]; fr[:] = paper(PINK, .55); rays(fr, T, 'FFFFFF', .14)
    sk(fr, OAT, CX, 1050, T, 9, .85, -4, lt)
    tape(fr, "DON'T QUIT YOUR OAT LATTE", CX, 470, lt, col='FFFFFF', size=52, font=LUCKY, rot=-2)
    if T > wfind(12, 'mix'): title(fr, 'JUST MIX IT UP', 600, T - wfind(12, 'mix'), size=110, fill=RED)

def s_end(fr, T):
    lt = T - S[13]; fr[:] = paper(GREEN, .6); rays(fr, T, 'FFFFFF', .12)
    sk(fr, BURG, CX, 1050, T, 10, .9, -4)
    title(fr, 'CHANGED YOUR MIND?', 560, lt, size=100, fill=YEL)
    if T > S[14]:
        burst(fr, 'YES', 250, 1270, T - S[14], r=110, col=RED, size=56, rot=-8)
        burst(fr, 'NO', 830, 1270, T - S[14] - .15, r=110, col=BLUE, size=56, rot=8)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_question), (S[3], s_bought), (S[5], s_all), (S[6], s_twist), (S[7], s_below), (S[8], s_stack), (S[9], s_field),
           (S[10], s_next), (S[11], s_rules), (S[12], s_catch), (S[13], s_mix), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (S[3], S[4], wfind(10, 'no rules')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Photos: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
