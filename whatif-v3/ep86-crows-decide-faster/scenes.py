import sys, os, json, math
sys.path.insert(0, '/home/claude/crow2')
from kit import *
D = '/home/claude/crow2'
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

sys.path.insert(0, '/home/claude/samples')
import essay as ES

def bg(fr, T, tint='F3E3B3', m=.55): fr[:] = paper(tint, m)
def essay_slide(T, lines, t0s, size=128):
    fr = ES.base(True); ES.headline(fr, lines, T, t0s, y=400, dark=True, size=size); return fr

def eye(c, x, y, T, t0, s=1.0):
    k = (T - t0) % 1.6; close = 1 - min(1, abs(k - .2) / .12) if k < .4 else 0
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-120, 0); c.curve_to(-60, -80, 60, -80, 120, 0); c.curve_to(60, 80, -60, 80, -120, 0); c.close_path()
    c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(0, 0, 40, 0, 6.29); c.set_source_rgba(*hx('3A7BD5')); c.fill(); c.arc(0, 0, 18, 0, 6.29); c.set_source_rgba(0, 0, 0, 1); c.fill()
    if close > 0:
        c.move_to(-122, 0); c.curve_to(-60, -80, 60, -80, 122, 0); c.line_to(122, 0)
        c.curve_to(60, -80 + 160 * close, -60, -80 + 160 * close, -122, 0); c.close_path(); c.set_source_rgba(*hx('E8B89A')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def screen(c, x, y, T, w=560, h=400):
    c.rectangle(x - w / 2 + 12, y - h / 2 + 14, w + 44, h + 44); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.rectangle(x - w / 2 - 22, y - h / 2 - 22, w + 44, h + 44); c.set_source_rgba(*hx('2A2A2E')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.rectangle(x - w / 2, y - h / 2, w, h); c.set_source_rgba(.06, .07, .09, 1); c.fill()
    rng = np.random.default_rng(7)
    for k in range(60):
        x0, y0 = rng.uniform(-w / 2 + 20, w / 2 - 20), rng.uniform(-h / 2 + 20, h / 2 - 20)
        right = k % 10 < 7; vx = 120 if right else rng.uniform(-120, 120); vy = 0 if right else rng.uniform(-120, 120)
        px = x + ((x0 + vx * T + w / 2) % (w - 30)) - w / 2 + 15; py = y + ((y0 + vy * T + h / 2) % (h - 30)) - h / 2 + 15
        c.arc(px, py, 7, 0, 6.29); c.set_source_rgba(*hx(YEL)); c.fill()
    for sx, col in ((-1, 'BBBBBB'), (1, RED)):
        c.arc(x + sx * (w / 2 + 75), y, 36, 0, 6.29); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()

def crow(fr, T, x, y, w, t=1.0, rot=-3, name='crow'):
    s_ = st(name, w=w)
    if s_ is not None: put_rgba(fr, s_, x, y + 6 * math.sin(T * 2), back(clamp(t / .35)), 1.0, rot)

def s_hook(fr, T):
    bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    crow(fr, T, 430, 1120, 700, T + .4)
    overlay(fr, cairo_layer(lambda c: eye(c, 840, 840, T, .5, .8)))
    tape(fr, 'CROWS THINK', CX, 470, T + .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'FASTER THAN A BLINK', 600, T + .3, size=104, fill=YEL, rot=-2)

def s_twice(fr, T):
    fr[:] = essay_slide(T, [('TWICE AS FAST', 'hl'), ('AS YOU.', 'main')], [S[1], wfind(1, 'you')])
    s_ = st('crow', w=520)
    if s_ is not None: put_rgba(fr, glow_outline(s_, 14, (255, 255, 255)), CX, 1110, back(clamp((T - S[1] - .1) / .35)), 1.0, 4)
    burst(fr, '2X', 840, 1260, T - wfind(1, 'twice'), r=115, col=YEL, size=84, rot=8)

def s_test(fr, T):
    lt = T - S[2]; bg(fr, T, 'C9DDF0')
    tape(fr, 'THE CROW TEST', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, cairo_layer(lambda c: screen(c, 470, 1000, T)))
    crow(fr, T, 860, 1270, 360, lt - .3, -8)
    if T > wfind(3, 'which'): title(fr, 'WHICH WAY?', 620, T - wfind(3, 'which'), size=110, fill=YEL)
    if T > wfind(3, 'peck'):
        overlay(fr, cairo_layer(lambda c: arrow(c, 800, 760, 880, 950, RED, 24)))
        chip(fr, 'PECK THAT SIDE', 760, 1430 - 70, T - wfind(3, 'peck'), RED, 38, 3)

def s_quarter(fr, T):
    fr[:] = essay_slide(T, [('A QUARTER', 'main'), ('OF A SECOND.', 'hl')], [S[4], wfind(4, 'quarter')])
    def watch(c):
        x, y = CX, 1080; c.arc(x, y, 230, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 10); c.stroke()
        c.rectangle(x - 30, y - 290, 60, 50); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 6); c.stroke()
        u = clamp((T - S[4]) / 1.6) * .25
        c.move_to(x, y); c.arc(x, y, 210, -math.pi / 2, -math.pi / 2 + 6.283 * u); c.close_path(); c.set_source_rgba(*hx(RED)); c.fill()
        c.arc(x, y, 230, 0, 6.29); ink(c, 10); c.stroke()
    overlay(fr, cairo_layer(watch))
    if T > wfind(4, 'quarter'): burst(fr, '0.235 SEC', 830, 1330, T - wfind(4, 'quarter'), r=125, col=YEL, size=38, rot=8)

def s_race(fr, T):
    lt = T - S[5]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .08)
    tape(fr, 'CROW VS PEOPLE', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    t1 = S[5] + .3; t2 = wfind(5, 'twice')
    def dr(c):
        for k, (ms, col, t0) in enumerate(((235, RED, t1), (470, 'BBBBBB', t2))):
            if T < t0: continue
            u = eout(clamp((T - t0) / (.5 + .5 * k))); y = 880 + k * 230; w_ = 820 * ms / 470 * u
            c.rectangle(130 + 10, y + 10, w_, 130); c.set_source_rgba(0, 0, 0, .3); c.fill()
            c.rectangle(130, y, w_, 130); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    overlay(fr, cairo_layer(dr))
    s_ = st('crow', w=200)
    if s_ is not None and T > t1: put_rgba(fr, s_, 130 + 820 * 235 / 470 * eout(clamp((T - t1) / .5)) + 60, 900, 1.0, 1.0, -4)
    if T > t1: chip(fr, 'CROW ~0.24 SEC', 300, 1050, T - t1 - .2, YEL, 34, -2)
    if T > t2: chip(fr, 'PEOPLE ~2X LONGER', 380, 1280, T - t2 - .3, 'FFFFFF', 34, 2); title(fr, '2X LONGER', 620, T - t2, size=110, fill=YEL)

def neurons(c, T, t0, y=1080):
    c.rectangle(110 + 12, y - 290 + 14, 860, 560); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.rectangle(110, y - 290, 860, 560); c.set_source_rgba(.08, .08, .1, 1); c.fill_preserve(); ink(c, 7); c.stroke()
    for r in range(8):
        yy = y - 220 + r * 62
        c.move_to(140, yy); c.line_to(940, yy); c.set_source_rgba(1, 1, 1, .2); c.set_line_width(2); c.stroke()
        rng = np.random.default_rng(r)
        for k in range(40):
            tt = rng.uniform(0, 1.2); xx = 140 + tt / 1.2 * 800
            if T - t0 < tt: continue
            hot = tt > .25 and r % 2 == 0
            c.move_to(xx, yy - 22); c.line_to(xx, yy + 22); c.set_source_rgba(*hx(RED if hot else 'DDDDDD')); c.set_line_width(5 if hot else 3); c.stroke()

def s_wild(fr, T):
    lt = T - S[6]; bg(fr, T, 'F7D9C4'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, "HERE'S THE WILD PART", CX, 470, lt, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, cairo_layer(lambda c: neurons(c, T, wfind(6, 'brain'))))
    if T > wfind(6, 'seventy'): title(fr, '70 MILLISECONDS', 620, T - wfind(6, 'seventy'), size=104, fill=YEL); chip(fr, 'BRAIN CELLS ALREADY CHOSE', CX, 1340, T - wfind(6, 'seventy') - .3, 'FFFFFF', 36, -2)

def s_layer(fr, T):
    lt = T - S[7]; bg(fr, T, 'F2E6CF')
    crow(fr, T, CX, 1100, 560, lt)
    tape(fr, 'NO HUMAN-STYLE BRAIN LAYER', CX, 470, lt, col='FFFFFF', size=50, font=LUCKY, rot=-2)
    if T > wfind(7, 'layer'): burst(fr, 'STILL FASTER', 830, 1330, T - wfind(7, 'layer'), r=130, col=YEL, size=36, rot=8)

def s_two(fr, T):
    fr[:] = essay_slide(T, [('ONLY 2 CROWS.', 'hl'), ('MORE TESTS NEEDED.', 'grey')], [S[8], wfind(8, 'more')], size=112)
    s_ = st('crow', w=340)
    if s_ is not None:
        for k in range(2):
            t_ = T - S[8] - .2 - k * .2
            if t_ > 0: put_rgba(fr, glow_outline(s_, 12, (255, 255, 255)), 320 + k * 440, 1110, back(clamp(t_ / .35)), 1.0, [-6, 6][k])

def s_end(fr, T):
    lt = T - S[9]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    crow(fr, T, CX, 1120, 760, 1.0, -2, 'crowhead')
    tape(fr, 'NEXT TIME A CROW STARES...', CX, 470, lt, col='FFFFFF', size=52, font=LUCKY, rot=-2)
    if T > wfind(9, 'decided') - .3: title(fr, 'IT ALREADY DECIDED', 620, T - wfind(9, 'decided') + .3, size=100, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_twice), (S[4], s_test), (S[5], s_quarter), (S[6], s_race), (S[7], s_wild), (S[8], s_layer), (S[9], s_two), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(1, 'twice'), wfind(6, 'seventy'), wfind(9, 'decided')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Images: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
