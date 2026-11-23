import sys, os, json, math
sys.path.insert(0, '/home/claude/breath')
from kit import *
D = '/home/claude/breath'
L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + 0.3; TOTAL = END + 1.6
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


def bg(fr, T, tint='D3E8F2', m=.55): fr[:] = paper(tint, m)

def puffs(fr, T, x, y, n=6, spread=160, lab=True, t0=0.0):
    def dr(c):
        for k in range(n):
            f = ((T - t0) * .45 + k / n) % 1
            if T - t0 < k / n / .45: continue
            px = x + spread * math.sin(k * 2.1 + f * 2); py = y - f * 520; r = 30 + 50 * f
            c.arc(px, py, r, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, .85 * (1 - f)); c.fill_preserve()
            c.set_source_rgba(*hx('1C1614', .6 * (1 - f))); c.set_line_width(4); c.stroke()
            if lab and r > 45:
                c.select_font_face('Luckiest Guy'); c.set_font_size(r * .55); e = c.text_extents('CO2')
                c.move_to(px - e.width / 2, py + e.height / 2); c.set_source_rgba(*hx('1C1614', 1 - f)); c.show_text('CO2')
    overlay(fr, cairo_layer(dr))

def lungs(fr, T, x=CX, y=1150, w=520, t=1.0):
    s_ = st('lungs', w=w)
    if s_ is not None: put_rgba(fr, s_, x, y, back(clamp(t / .35)) * (1 + .05 * math.sin(T * 2.6)), 1.0, 0)

def s_hook(fr, T):
    bg(fr, T, 'C9E4F2'); rays(fr, T, 'FFFFFF', .14)
    lungs(fr, T, CX, 1180, 560, T + .3)
    puffs(fr, T, CX, 900, 7, 180)
    tp = wfind(0, 'pound')
    if T > tp - .2: title(fr, '1.5 LB A DAY', 610, T - tp + .2, size=124, fill=YEL, rot=-2)
    tape(fr, 'YOU BREATHE OUT', CX, 470, T, col='FFFFFF', size=58, font=LUCKY, rot=-2)

def s_mult(fr, T):
    lt = T - S[1]; fr[:] = paper('0B1730', .9)
    ph = st('earth', w=620)
    if ph is not None: put_rgba(fr, ph, CX, 1050, back(clamp(lt / .35)), 1.0, 0)
    for k in range(5):
        a = k / 5 * 2 * math.pi + lt * .3
        puffs(fr, T, CX + 330 * math.cos(a), 1050 + 330 * math.sin(a) + 200, 3, 30, False, S[1])
    title(fr, 'x EVERYONE', 620, lt, size=130, fill=YEL)

def s_total(fr, T):
    lt = T - S[2]; bg(fr, T, 'E8E1D0')
    tn = wfind(2, 'two billion')
    def blocks(c):
        n = int(clamp((T - tn) / 1.6) * 40) if T > tn else 0
        for k in range(n):
            r_, q = divmod(k, 8); x = 170 + q * 105; y = 1300 - r_ * 95
            c.rectangle(x - 46 + 6, y - 42 + 6, 92, 84); c.set_source_rgba(0, 0, 0, .25); c.fill()
            c.rectangle(x - 46, y - 42, 92, 84); c.set_source_rgba(*hx(['8A8F98', '6F747C'][k % 2])); c.fill_preserve(); ink(c, 4); c.stroke()
    overlay(fr, cairo_layer(blocks))
    tape(fr, 'SCIENTISTS JUST DID THE MATH', CX, 470, lt, col='FFFFFF', size=50, font=LUCKY, rot=-2)
    if T > tn:
        v = 2.0 * eout(clamp((T - tn) / 1.2)); title(fr, f'{v:.1f} BILLION TONS', 610, T - tn, size=104, fill=YEL)
    if T > wfind(2, 'alive'): chip(fr, 'JUST FROM STAYING ALIVE', CX, 740, T - wfind(2, 'alive'), RED, 42, 2)

def s_rise(fr, T):
    lt = T - S[3]; bg(fr, T, 'F2E6CF'); rays(fr, T, 'FFFFFF', .08)
    def bars(c):
        base = 1260
        for k, (v, col, t0) in enumerate(((1.18, 'BBBBBB', S[3] + .2), (2.05, RED, wfind(3, 'seventy')))):
            if T < t0: continue
            u = eout(clamp((T - t0) / .8)); x = 330 + k * 420; hh = 600 * v / 2.05 * u
            c.rectangle(x - 120 + 10, base - hh + 10, 240, hh); c.set_source_rgba(0, 0, 0, .3); c.fill()
            c.rectangle(x - 120, base - hh, 240, hh); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
        c.move_to(90, base); c.line_to(W - 90, base); ink(c, 8); c.stroke()
    overlay(fr, cairo_layer(bars))
    tape(fr, 'BILLION TONS OF CO2', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    chip(fr, '1985', 330, 1310, lt - .2, 'FFFFFF', 40, -2)
    if T > wfind(3, 'seventy'):
        chip(fr, '2015', 750, 1310, T - wfind(3, 'seventy'), 'FFFFFF', 40, 2)
        burst(fr, '+74%', 750, 560, T - wfind(3, 'seventy') - .3, r=125, col=YEL, size=60, rot=8)

def s_more(fr, T):
    lt = T - S[4]; bg(fr, T, 'DCE8C2')
    tm = wfind(4, 'more')
    def ppl(c):
        n = 12 + (int(clamp((T - tm) / 1.2) * 60) if T > tm else 0)
        for k in range(n):
            r_, q = divmod(k, 12); x = 120 + q * 76; y = 1300 - r_ * 110
            c.arc(x, y - 52, 17, 0, 2 * math.pi); c.set_source_rgba(*hx(['1C1614', RED, '3A7BD5'][k % 3])); c.fill()
            c.move_to(x - 22, y + 10); c.line_to(x - 16, y - 30); c.line_to(x + 16, y - 30); c.line_to(x + 22, y + 10); c.close_path(); c.fill()
    overlay(fr, cairo_layer(ppl))
    tape(fr, 'NOT HARDER BREATHING...', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    if T > tm: title(fr, 'JUST MORE OF US', 620, T - tm, size=110, fill=YEL)

def s_heat(fr, T):
    lt = T - S[5]; fr[:] = paper('F7C9A0', .6); rays(fr, T, 'FFFFFF', .12)
    ph = st('earth', w=560)
    if ph is not None: put_rgba(fr, ph, CX, 1060, back(clamp(lt / .35)), 1.0, 0)
    title(fr, 'HEATING THE PLANET?', 610, lt, size=96, fill='FFFFFF')
    tn = wfind(5, 'nope')
    if T > tn - .2: xstamp(fr, CX, 1060, T - tn + .2, 1.3); burst(fr, 'NOPE', 820, 1340, T - tn, r=120, col=GREEN, size=56, rot=8)

def s_loop(fr, T):
    lt = T - S[6]; bg(fr, T, 'DCE8C2')
    pts = [(CX, 720, 'AIR', None), (840, 1000, 'PLANTS', 'wheat'), (CX, 1260, 'FOOD', 'bread'), (240, 1000, 'YOU', 'lungs')]
    def ring(c):
        u = clamp(lt / 2.5)
        c.arc(CX, 1000, 280, -math.pi / 2, -math.pi / 2 + 2 * math.pi * u); c.set_source_rgba(*hx('1C1614')); c.set_line_width(12); c.stroke()
        a = -math.pi / 2 + 2 * math.pi * u; x, y = CX + 280 * math.cos(a), 1000 + 280 * math.sin(a)
        c.arc(x, y, 20, 0, 2 * math.pi); c.set_source_rgba(*hx(RED)); c.fill()
    overlay(fr, cairo_layer(ring))
    for k, (x, y, lab, img) in enumerate(pts):
        t_ = lt - k * .55
        if t_ < 0: continue
        if img == 'bread':
            def loaf(c, x=x, y=y, t_=t_):
                u = back(clamp(t_ / .3)); c.save(); c.translate(x, y); c.scale(u, u)
                c.save(); c.scale(1.6, 1); c.arc(0, 0, 70, math.pi, 2 * math.pi); c.restore(); c.rectangle(-112, 0, 224, 50)
                c.set_source_rgba(*hx('C98A3E')); c.fill_preserve(); ink(c, 6); c.stroke()
                for k2 in (-50, 0, 50): c.move_to(k2 - 15, -40); c.line_to(k2 + 15, -10); c.set_source_rgba(*hx('F3D7A6')); c.set_line_width(8); c.stroke()
                c.restore()
            overlay(fr, cairo_layer(loaf))
        elif img:
            s_ = st(img, w=200)
            if s_ is not None: put_rgba(fr, s_, x, y, back(clamp(t_ / .3)), 1.0, 0)
        else: puffs(fr, T, x, y + 120, 3, 40, False, S[6])
        chip(fr, lab, x, y + 115 if k != 2 else y + 85, t_, [CYAN, GREEN, YEL, 'FFFFFF'][k], 36, 0)
    tape(fr, "IT'S A LOOP", CX, 470, lt, col=RED, size=64, font=LUCKY, rot=-2, tcol='FFFFFF')

def s_oil(fr, T):
    lt = T - S[7]; bg(fr, T, 'E8DCC0')
    def ground(c):
        cols = ['C9A26B', 'A97E4C', '8A6238', '6B4A2A', '3A2A1C']
        for k, col in enumerate(cols):
            c.rectangle(0, 900 + k * 110, W, 110); c.set_source_rgba(*hx(col)); c.fill()
        c.save(); c.translate(CX, 1400); c.scale(1.8, .6); c.arc(0, 0, 120, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('111111')); c.fill()
        u = clamp((lt - .6) / 1.2); c.rectangle(CX - 10, 900, 20, 500 * u); c.set_source_rgba(*hx('333333')); c.fill()
    overlay(fr, cairo_layer(ground))
    s_ = st('pump', w=380)
    if s_ is not None: put_rgba(fr, s_, CX, 760, back(clamp(lt / .35)), 1.0, 0)
    tape(fr, 'BURNING OIL IS DIFFERENT', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    if T > wfind(7, 'millions'): title(fr, 'BURIED MILLIONS OF YEARS', 610, T - wfind(7, 'millions'), size=84, fill=YEL)

def s_count(fr, T):
    lt = T - S[8]; bg(fr, T, 'F2E6CF'); rays(fr, T, 'FFFFFF', .08)
    tape(fr, 'WHY COUNT YOUR BREATH?', CX, 470, lt, col=RED, size=56, font=LUCKY, rot=-2, tcol='FFFFFF')
    def sheet(c):
        c.save(); c.translate(CX, 1040); c.rotate(-.03)
        c.rectangle(-330 + 12, -330 + 14, 660, 660); c.set_source_rgba(0, 0, 0, .3); c.fill()
        c.rectangle(-330, -330, 660, 660); c.set_source_rgba(*hx('FFFDF5')); c.fill_preserve(); ink(c, 7); c.stroke()
        for r in range(1, 6): c.move_to(-300, -330 + r * 110); c.line_to(300, -330 + r * 110); c.set_source_rgba(*hx('1C1614', .2)); c.set_line_width(3); c.stroke()
        c.restore()
    overlay(fr, cairo_layer(sheet))
    title(fr, 'CLIMATE MATH', 610, lt, size=110, fill=YEL)
    items = ['FACTORIES', 'CARS', 'FARMS', 'PLANES', 'YOU']
    te = wfind(8, 'every')
    for k, it in enumerate(items):
        t_ = T - te - k * .25
        if t_ > 0: chip(fr, it + '  +', CX, 790 + k * 110, t_, RED if it == 'YOU' else 'FFFFFF', 40, [-2, 1, -1, 2, -3][k])

def s_end(fr, T):
    lt = T - S[9]; bg(fr, T, 'C9E4F2'); rays(fr, T, 'FFFFFF', .14)
    tb = wfind(9, 'let it out')
    lungs(fr, T, CX, 1180, 560 + int(60 * math.sin(clamp(lt / 1.5) * math.pi)), 1.0)
    if T > tb: puffs(fr, T, CX, 900, 7, 180, True, tb)
    title(fr, 'TAKE A DEEP BREATH', 610, lt, size=100, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_mult), (S[3], s_total), (S[4], s_rise), (S[5], s_more), (S[6], s_heat), (S[7], s_loop), (S[8], s_oil), (S[9], s_count), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(2, 'two billion'), wfind(5, 'nope'), wfind(3, 'seventy')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Images: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
