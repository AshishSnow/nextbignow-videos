import sys, os, json, math
sys.path.insert(0, '/home/claude/tort')
from kit import *
D = '/home/claude/tort'
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


def bg(fr, T, tint='DCE8C2', m=.55): fr[:] = paper(tint, m)

def helix(c, cx, cy, T, h=760, amp=150, hl=0, hl_n=0):
    n = 26
    for k in range(n):
        y = cy - h / 2 + k * h / (n - 1); ph = T * 2.2 + k * .5
        x1 = cx + amp * math.sin(ph); x2 = cx - amp * math.sin(ph)
        c.move_to(x1, y); c.line_to(x2, y)
        lit = hl > 0 and (k * 7) % n < hl_n
        c.set_source_rgba(*hx(YEL if lit else 'FFFFFF', .95)); c.set_line_width(14 if lit else 9); c.stroke()
    for sgn, col in ((1, RED), (-1, CYAN)):
        c.move_to(cx + sgn * amp * math.sin(T * 2.2), cy - h / 2)
        for k in range(1, 80):
            y = cy - h / 2 + k * h / 79; ph = T * 2.2 + k / 79 * (n - 1) * .5
            c.line_to(cx + sgn * amp * math.sin(ph), y)
        c.set_source_rgba(*hx('1C1614')); c.set_line_width(22); c.stroke_preserve(); c.set_source_rgba(*hx(col)); c.set_line_width(14); c.stroke()

def tort(fr, T, x=CX, y=1060, h=560, t=1.0, rot=-3):
    s_ = st('jon', w=min(900, int(h * 1.45)))
    if s_ is not None: put_rgba(fr, s_, x, y + 5 * math.sin(T * 1.5), back(clamp(t / .35)), 1.0, rot)

def s_hook(fr, T):
    bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tort(fr, T, CX, 1080, 640, T + .3)
    counter = int(194 * eout(clamp(T / 1.4)))
    title(fr, f'{counter} YEARS OLD', 520, T, size=118, fill='FFFFFF', rot=-2)
    ty = wfind(0, 'young')
    if T > ty - .3: burst(fr, 'STILL YOUNG?', 820, 1330, T - ty + .3, r=140, col=YEL, size=38, rot=8)

def s_dna(fr, T):
    lt = T - S[1]; bg(fr, T, 'C9DDF0')
    overlay(fr, cairo_layer(lambda c: helix(c, CX, 1040, T, 760, 170)))
    tape(fr, 'SCIENTISTS READ HIS DNA', CX, 470, lt, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')

def s_timeline(fr, T):
    lt = T - S[2]; bg(fr, T, 'F3E3B3')
    tape(fr, 'MEET JONATHAN', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    ph0 = photo('old', 440, 320, (.5, .5))
    if ph0 is not None: put_rgba(fr, ph0, 290, 880, back(clamp(lt / .35)), 1.0, -4)
    if lt > .3: chip(fr, 'JONATHAN, 1880s', 290, 1060, lt - .3, YEL, 30, -3)
    th = wfind(2, 'hatched'); tp = wfind(2, 'photo')
    def line(c):
        y = 1290; u = eout(clamp((T - th) / 1.2)) if T > th else 0
        c.move_to(110, y); c.line_to(110 + 860 * u, y); ink(c, 10); c.stroke()
        for xx, on in ((140, T > th), (420, T > tp), (930, T > tp + .8)):
            if on: c.arc(xx, y, 22, 0, 2 * math.pi); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 5); c.stroke()
    overlay(fr, cairo_layer(line))
    if T > th: chip(fr, 'HATCHED ~1832', 230, 1365, T - th, YEL, 34, -3)
    if T > tp:
        ph = photo('daguerre', 520, 380, (.5, .5))
        if ph is not None: put_rgba(fr, ph, 740, 900, back(clamp((T - tp) / .3)), 1.0, 3)
        chip(fr, 'FIRST PHOTO OF A PERSON: 1838', 600, 1140, T - tp, 'FFFFFF', 32, 2)
    if T > tp + .8: chip(fr, 'TODAY', 880, 1365, T - tp - .8, CYAN, 34, 3)

def s_compare(fr, T):
    lt = T - S[3]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .08)
    tape(fr, 'GIANT TORTOISE LIFESPAN', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    t1 = S[3] + .3; t2 = wfind(3, 'doubled')
    def bars(c):
        base = 1250
        for k, (v, col, t0) in enumerate(((100, 'BBBBBB', t1), (194, YEL, t2))):
            if T < t0: continue
            u = eout(clamp((T - t0) / .8)); x = 320 + k * 440; hh = 620 * v / 194 * u
            c.rectangle(x - 120 + 10, base - hh + 10, 240, hh); c.set_source_rgba(0, 0, 0, .3); c.fill()
            c.rectangle(x - 120, base - hh, 240, hh); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
        c.move_to(90, base); c.line_to(W - 90, base); ink(c, 8); c.stroke()
    overlay(fr, cairo_layer(bars))
    if T > t1: title(fr, '~100', 1250 - 620 * 100 / 194 * eout(clamp((T - t1) / .8)) - 70, T - t1, size=84, fill='FFFFFF', cx=320); chip(fr, 'USUAL', 320, 1310, T - t1, 'FFFFFF', 36, -2)
    if T > t2:
        title(fr, '194', 1250 - 620 * eout(clamp((T - t2) / .8)) - 70, T - t2, size=96, fill=YEL, cx=760); chip(fr, 'JONATHAN', 760, 1310, T - t2, YEL, 36, 2)
        s_ = st('jon', h=200)
        if s_ is not None: put_rgba(fr, s_, 760, 1150, back(clamp((T - t2 - .6) / .3)), 1.0, 0)

def s_swab(fr, T):
    lt = T - S[4]; bg(fr, T, 'F2E6CF')
    tort(fr, T, 620, 1080, 520, lt, -2)
    def swab(c):
        u = ease(clamp(lt / .8)); x = lerp(-250, 330, u); y = 1020
        c.save(); c.translate(x, y); c.rotate(.3)
        c.rectangle(-380, -8, 380, 16); c.set_source_rgba(*hx('E9EEF2')); c.fill_preserve(); ink(c, 5); c.stroke()
        c.save(); c.scale(1.7, 1); c.arc(0, 0, 26, 0, 2 * math.pi); c.restore(); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 5); c.stroke(); c.restore()
    overlay(fr, cairo_layer(swab))
    tape(fr, 'CHEEK SWAB TIME', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    tb = wfind(4, 'bacteria')
    if T > tb - .3:
        def bugs(c):
            for k in range(16):
                rng = np.random.default_rng(k); x = rng.uniform(140, 560); y = rng.uniform(760, 1200) + 8 * math.sin(T * 5 + k)
                c.save(); c.translate(x, y); c.rotate(rng.uniform(0, 3)); c.scale(1, .45); c.arc(0, 0, 20, 0, 2 * math.pi); c.restore()
                c.set_source_rgba(*hx(GREEN)); c.fill_preserve(); ink(c, 3); c.stroke()
        overlay(fr, cairo_layer(bugs))
        title(fr, 'MOUTH BACTERIA', 620, T - tb + .3, size=104, fill=YEL); xstamp(fr, 340, 980, T - tb, 1.0)

def s_genes(fr, T):
    lt = T - S[5]; bg(fr, T, 'C9DDF0')
    tn = wfind(5, 'two hundred')
    n_on = int(26 * clamp((T - tn) / 1.2)) if T > tn else 0
    overlay(fr, cairo_layer(lambda c: helix(c, 300, 1050, T, 720, 120, 1, n_on)))
    tape(fr, 'TRY TWO WORKED', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > tn:
        v = int(287 * eout(clamp((T - tn) / 1.2))); stat(fr, str(v), 'RARE GENE CHANGES', 720, 900, T - tn, YEL, 3, 150)
    if T > wfind(5, 'aging'): chip(fr, 'TIED TO AGING', 720, 1180, T - wfind(5, 'aging'), 'FFFFFF', 44, -2)

def s_jobs(fr, T):
    lt = T - S[6]; bg(fr, T, 'F2E6CF'); rays(fr, T, 'FFFFFF', .08)
    tape(fr, 'WHAT THOSE GENES DO', CX, 470, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    tf = wfind(6, 'fix'); tp = wfind(6, 'protect')
    if T > tf:
        def fix(c):
            u = clamp((T - tf) / .8); x, y = 300, 960
            c.move_to(x - 120, y - 90); c.line_to(x - 20, y - 10); c.set_source_rgba(*hx(RED)); c.set_line_width(26); c.stroke()
            c.move_to(x + 120 - 100 * (1 - u), y + 90 - 80 * (1 - u)); c.line_to(x + 20, y + 10); c.set_source_rgba(*hx(RED)); c.set_line_width(26); c.stroke()
            c.arc(x, y, 34 * u, 0, 2 * math.pi); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 5); c.stroke()
        overlay(fr, cairo_layer(fix)); chip(fr, 'FIX BROKEN DNA', 270, 1180, T - tf, YEL, 40, -3)
    if T > tp:
        def caps(c):
            x, y = 780, 960
            c.rectangle(x - 26, y - 150, 52, 300); c.set_source_rgba(*hx(CYAN)); c.fill_preserve(); ink(c, 6); c.stroke()
            u = back(clamp((T - tp) / .4))
            for sy in (-1, 1):
                c.arc(x, y + sy * 160, 40 * u, 0, 2 * math.pi); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 6); c.stroke()
        overlay(fr, cairo_layer(caps)); chip(fr, 'GUARD CHROMOSOME TIPS', 790, 1250, T - tp, CYAN, 34, 3)

def s_batt(fr, T):
    lt = T - S[7]; bg(fr, T, 'DCE8C2')
    tape(fr, 'HIS CELL BATTERIES', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    tn = wfind(7, 'neat')
    def batts(c):
        for k in range(3):
            x = 220 + k * 320; y = 1000; u = back(clamp((lt - .2 * k) / .4))
            if u <= 0: continue
            c.save(); c.translate(x, y); c.scale(u, u)
            c.rectangle(-90 + 8, -150 + 10, 180, 300); c.set_source_rgba(0, 0, 0, .3); c.fill()
            c.rectangle(-90, -150, 180, 300); c.set_source_rgba(1, 1, 1, 1); c.fill()
            f = .85 if T > tn else .5 + .3 * math.sin(T * 3 + k)
            c.rectangle(-90, 150 - 300 * f, 180, 300 * f); c.set_source_rgba(*hx(GREEN)); c.fill()
            c.rectangle(-90, -150, 180, 300); ink(c, 7); c.stroke()
            c.rectangle(-40, -180, 80, 30); c.set_source_rgba(*hx('DDDDDD')); c.fill_preserve(); ink(c, 5); c.stroke()
            c.restore()
    overlay(fr, cairo_layer(batts))
    chip(fr, 'MITOCHONDRIA', CX, 640, lt - .3, CYAN, 40, 2)
    if T > tn: burst(fr, 'STILL NEAT', CX, 1290, T - tn, r=140, col=YEL, size=44, rot=-4)

def s_caveat(fr, T):
    lt = T - S[8]; bg(fr, T, 'F2E6CF')
    tort(fr, T, CX, 1060, 520, lt, 2)
    tape(fr, "IT'S ONE TORTOISE", CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > wfind(8, 'nobody'): title(fr, 'NOT PROOF... YET', 620, T - wfind(8, 'nobody'), size=110, fill=YEL)

def s_next(fr, T):
    lt = T - S[9]; bg(fr, T, 'F7D9C4'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'WHAT HAPPENS NEXT', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    tb = wfind(9, 'blood')
    if T > tb - .2:
        def drop(c):
            u = back(clamp((T - tb + .2) / .4)); x, y = CX, 980
            c.save(); c.translate(x, y); c.scale(u, u)
            c.move_to(0, -200); c.curve_to(110, -60, 150, 30, 150, 80); c.arc(0, 80, 150, 0, math.pi); c.curve_to(-150, 30, -110, -60, 0, -200)
            c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 8); c.stroke(); c.restore()
        overlay(fr, cairo_layer(drop)); chip(fr, 'A BLOOD SAMPLE', CX, 640, T - tb, 'FFFFFF', 46, 2)
    if T > wfind(9, 'all of us'): title(fr, 'HOW WE ALL AGE?', 1330, T - wfind(9, 'all of us'), size=96, fill=YEL)

def s_end(fr, T):
    lt = T - S[10]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tort(fr, T, CX, 1080, 640, 1.0)
    title(fr, 'OLDER THAN', 470, lt, size=120, fill='FFFFFF'); title(fr, 'THE CAMERA', 610, lt - .15, size=120, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_dna), (S[3], s_timeline), (S[4], s_compare), (S[5], s_swab), (S[6], s_genes), (S[7], s_jobs), (S[8], s_batt),
           (S[9], s_caveat), (S[10], s_next), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(4, 'bacteria'), wfind(5, 'two hundred'), wfind(7, 'neat')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Images: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
