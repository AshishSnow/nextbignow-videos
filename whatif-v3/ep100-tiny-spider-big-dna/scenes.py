import sys, os, json, math
sys.path.insert(0, '/home/claude/spider')
from kit import *
D = '/home/claude/spider'
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






def bird(c, x, y, s, T, fly=0.0, flip=False, col='8A93A6'):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    flap = math.sin(T * 22) if fly > 0 else 0
    c.save(); c.scale(1.4, 1); c.arc(0, 0, 80, 0, 6.29); c.restore(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    c.move_to(100, -10); c.line_to(170, -40); c.line_to(160, 30); c.close_path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(-95, -60, 50, 0, 6.29); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(-80, -30, 34, .5, 2.6); c.set_source_rgba(*hx('6FB39A', .8)); c.set_line_width(10); c.stroke()
    c.move_to(-140, -65); c.line_to(-175, -55); c.line_to(-140, -48); c.close_path(); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 4); c.stroke()
    c.arc(-108, -70, 9, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    wy = -60 * fly * (1 + flap)
    c.move_to(-20, -20); c.curve_to(10, -60 + wy, 70, -60 + wy, 90, -30 + wy * .6); c.curve_to(60, 0, 20, 10, -20, -20); c.set_source_rgba(*hx('6D7587')); c.fill_preserve(); ink(c, 6); c.stroke()
    if fly < .5:
        for lx in (-20, 20): c.move_to(lx, 75); c.line_to(lx, 120); c.set_source_rgba(*hx('E07A5F')); c.set_line_width(8); c.stroke()
    c.restore()

def person(c, x, y, s, T, walk=0.0, hair=False, col=BLUE, flip=False):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    sw = 25 * math.sin(T * 8) * walk
    for d in (-1, 1):
        c.move_to(-15 * d, 120); c.line_to(-15 * d + sw * d, 300); c.set_source_rgba(*hx('2B2B33')); c.set_line_width(30); c.set_line_cap(1); c.stroke()
    c.move_to(-70, -60); c.curve_to(-80, 60, -60, 130, 0, 130); c.curve_to(60, 130, 80, 60, 70, -60); c.curve_to(40, -80, -40, -80, -70, -60)
    c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    if hair:
        c.move_to(-62, -150); c.curve_to(-90, -60, -70, -20, -40, -30); c.line_to(40, -30); c.curve_to(70, -20, 90, -60, 62, -150); c.close_path(); c.set_source_rgba(*hx('6B3E26')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(0, -135, 58, 0, 6.29); c.set_source_rgba(*hx('F2C9A0')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(0, -168, 58, 3.3, 6.1); c.set_source_rgba(*hx('6B3E26' if hair else '3A2A20')); c.fill()
    for ex in (-20, 20): c.arc(ex, -130, 7, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.restore()




GOLD = 'C9CED6'

def spider(c, x, y, s, T, wig=1.0, col='5A3A28'):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    for side in (-1, 1):
        for k in range(4):
            a0 = math.radians(-60 + k * 38); ph = math.sin(T * 9 + k * 1.3 + side) * .12 * wig
            kx, ky = side * 120 * math.cos(a0 + ph), -40 + 120 * math.sin(a0 + ph) - 40
            fx, fy = side * 220 * math.cos(a0 * .8 + ph), 80 + 70 * math.sin(a0 + ph) + k * 20
            c.move_to(side * 30, -10 + k * 12); c.line_to(kx, ky); c.line_to(fx, fy)
            c.set_source_rgba(*hx('1C1614')); c.set_line_width(22); c.set_line_cap(1); c.set_line_join(1); c.stroke()
            c.move_to(side * 30, -10 + k * 12); c.line_to(kx, ky); c.line_to(fx, fy)
            c.set_source_rgba(*hx(col)); c.set_line_width(12); c.stroke()
    c.save(); c.scale(1, 1.2); c.arc(0, 70 / 1.2, 85, 0, 6.29); c.restore(); c.set_source_rgba(*hx('7A5238')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.save(); c.scale(1.1, 1); c.arc(0, -40, 62, 0, 6.29); c.restore(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 8); c.stroke()
    for ex in (-18, 18):
        c.arc(ex, -62, 13, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 3); c.stroke()
        c.arc(ex + 2, -60, 6, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    for ex in (-40, 40): c.arc(ex, -48, 6, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.restore()

def quarter(c, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s * .42)
    c.arc(0, 40, 260, 0, 6.29); c.set_source_rgba(*hx('8E949C')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(0, 0, 260, 0, 6.29); c.set_source_rgba(*hx('D7DBE0')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(0, 0, 225, 0, 6.29); c.set_source_rgba(*hx('A7ADB5')); c.set_line_width(6); c.stroke()
    c.restore()

def helix(c, x, y, h, T, col1=RED, col2=CYAN, w=90, al=1.0):
    n = int(h / 30)
    for k in range(n):
        yy = y - h / 2 + k * 30; ph = T * 2 + k * .45
        x1, x2 = x + w * math.sin(ph), x - w * math.sin(ph)
        c.move_to(x1, yy); c.line_to(x2, yy); c.set_source_rgba(1, 1, 1, .7 * al); c.set_line_width(5); c.stroke()
        for xx, col in ((x1, col1), (x2, col2)):
            c.arc(xx, yy, 13, 0, 6.29); c.set_source_rgba(*hx(col, al)); c.fill_preserve(); ink(c, 3, al); c.stroke()

def dunes(c, T, y0=1150):
    c.rectangle(0, y0 - 300, W, 300); c.set_source_rgba(*hx('5FB0E0')); c.fill()
    for k, (yy, col) in enumerate(((y0 - 60, 'E8C98A'), (y0 + 40, 'DDB66E'), (y0 + 150, 'E8C98A'))):
        c.move_to(0, yy)
        for x in range(0, W + 20, 20): c.line_to(x, yy - 60 * math.sin(x / 180 + k * 1.7))
        c.line_to(W, H); c.line_to(0, H); c.close_path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()

def bar(c, x, y, w, hgt, col, lab=None):
    c.rectangle(x + 10, y - hgt + 12, w, hgt); c.set_source_rgba(0, 0, 0, .25); c.fill()
    c.rectangle(x, y - hgt, w, hgt); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()

def SP(fr, T, x, y, s, wig=1.0, rot=0):
    st_ = st('spider', w=int(560 * s)) if s > .01 else None
    if st_ is not None: put_rgba(fr, st_, x, y + 6 * math.sin(T * 3), 1.0, 1.0, rot + 3 * math.sin(T * 2))
    else: overlay(fr, cairo_layer(lambda c: spider(c, x, y, s, T, wig)))

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .16)
    overlay(fr, L_(lambda c: (helix(c, 150, 1120, 520, T, al=.6), helix(c, 930, 1120, 520, T + 1, al=.6), quarter(c, CX, 1260, 1.0, T))))
    SP(fr, T, CX, 1120, 1.0 * back(clamp((T + .5) / .5)))
    tape(fr, 'THIS TINY SPIDER', CX, 470, T + .4, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'IT BEATS YOUR', 600, T + .4, size=112, fill='FFFFFF', rot=-2); title(fr, 'GENOME BY 50%', 730, T + .3, size=124, fill=YEL, rot=-2)
    if T > wfind(0, 'quarter'): chip(fr, 'SIZE OF A QUARTER', 820, 1380, T - wfind(0, 'quarter'), 'FFFFFF', 32, 4)

def s_more(fr, T):
    fr[:] = essay_slide(T, [('NOT A LITTLE.', 'grey'), ('~50% BIGGER.', 'hl')], [S[1], wfind(1, 'fifty')], size=124)
    lt = T - S[1]; u = eout(clamp((lt - .3) / 1.2))
    def dr(c):
        bar(c, 220, 1340, 220, 260 * u, CYAN); bar(c, 640, 1340, 220, 390 * u, RED)
    overlay(fr, L_(dr))
    chip(fr, 'YOU', 330, 1390, lt - .3, 'FFFFFF', 36, -3); chip(fr, 'SPIDER', 750, 1390, lt - .4, YEL, 36, 3)

def s_dunes(fr, T):
    lt = T - S[2]; bg(fr, T, 'C9DDF0')
    overlay(fr, L_(lambda c: dunes(c, T)))
    tape(fr, 'CALIFORNIA DUNES', CX, 470, lt, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')
    SP(fr, T, 700, 1180, .45, .6)
    if T > wfind(2, 'trapdoor'): title(fr, 'A TRAPDOOR SPIDER', 620, T - wfind(2, 'trapdoor'), size=100, fill=YEL)

def s_door(fr, T):
    lt = T - S[3]; bg(fr, T, 'F7E3C8')
    tape(fr, 'THE AMBUSH', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    op = clamp((T - wfind(3, 'dinner')) / .4) if T > wfind(3, 'dinner') else 0
    def dr(c):
        c.rectangle(0, 900, W, 900); c.set_source_rgba(*hx('B58A5A')); c.fill()
        c.move_to(0, 900); c.line_to(W, 900); ink(c, 8); c.stroke()
        c.rectangle(440, 900, 200, 420); c.set_source_rgba(*hx('5E3F28')); c.fill_preserve(); ink(c, 6); c.stroke()
        c.save(); c.translate(440, 900); c.rotate(-1.2 * op); c.rectangle(0, -26, 220, 30); c.set_source_rgba(*hx('C9A66B')); c.fill_preserve(); ink(c, 6); c.stroke(); c.restore()
        ax = lerp(1100, 700, clamp(lt / 2.5))
        for k in range(3): c.arc(ax + k * 30, 870, 14 + 4 * (k == 1), 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    overlay(fr, L_(dr))
    SP(fr, T, 540, 1100 - 120 * op, .55, .4)
    if T > wfind(3, 'dinner'): title(fr, 'DINNER, DELIVERED', 620, T - wfind(3, 'dinner'), size=100, fill=YEL); burst(fr, 'SNAP!', 820, 760, T - wfind(3, 'dinner'), r=110, col=YEL, size=44, rot=8)

def s_read(fr, T):
    lt = T - S[4]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'FIRST FULL GENOME', CX, 470, lt, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        helix(c, 230, 1060, 640, T)
        c.select_font_face('Inter', 0, 1); c.set_font_size(54)
        rng = np.random.default_rng(int(T * 12))
        for r in range(9):
            s_ = ''.join(rng.choice(list('ATGC'), 14)); c.move_to(380, 800 + r * 70); c.set_source_rgba(*hx(['1C1614', RED, '2D6CDF'][r % 3], .8)); c.show_text(s_)
    overlay(fr, L_(dr))
    if T > wfind(4, 'four'):
        u = eout(clamp((T - wfind(4, 'four')) / 1.2)); title(fr, f'{4.6 * u:.1f} BILLION LETTERS', 640, T - wfind(4, 'four'), size=92, fill=YEL)

def s_yours(fr, T):
    lt = T - S[5]; bg(fr, T, 'D6EEF0'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'YOURS?', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    u = eout(clamp(lt / .8))
    def dr(c):
        person(c, 330, 1000, .8, T, 0, False, BLUE); bar(c, 220, 1360, 220, 200 * u, CYAN)
        bar(c, 640, 1360, 220, 300 * u, RED)
    overlay(fr, L_(dr))
    SP(fr, T, 750, 950, .4, .5)
    title(fr, '~3 BILLION', 640, lt, size=120, fill=YEL)

def s_repeat(fr, T):
    lt = T - S[6]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THE TWIST', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    n = int(clamp(lt / 3.5) * 40)
    def dr(c):
        for k in range(40):
            x, y = 150 + (k % 8) * 100, 780 + (k // 8) * 110
            rep = k < 31
            if k < n or not rep:
                c.rectangle(x, y, 86, 90); c.set_source_rgba(*hx(RED if rep else '3FAE5A')); c.fill_preserve(); ink(c, 5); c.stroke()
                c.select_font_face('Inter', 0, 1); c.set_font_size(34); c.set_source_rgba(1, 1, 1, 1); c.move_to(x + 14, y + 58); c.show_text('AT' if rep else 'G')
    overlay(fr, L_(dr))
    if T > wfind(6, 'repeats'): title(fr, '77% REPEATS', 620, T - wfind(6, 'repeats'), size=120, fill=YEL)
    if T > wfind(6, 'copied'): chip(fr, 'COPY. PASTE. COPY. PASTE.', CX, 1370, T - wfind(6, 'copied'), YEL, 34, -2)

def s_genes(fr, T):
    fr[:] = essay_slide(T, [('MORE DNA', 'grey'), ("ISN'T MORE GENES.", 'hl')], [S[7], wfind(7, 'genes')], size=110)
    overlay(fr, L_(lambda c: helix(c, CX, 1180, 380, T, al=.9)))

def s_threat(fr, T):
    lt = T - S[8]; bg(fr, T, 'F7D9C4')
    sea_u = clamp((T - wfind(8, 'seas')) / 1.5) if T > wfind(8, 'seas') else 0
    def dr(c):
        dunes(c, T, 1150)
        c.rectangle(0, 850, W, 180 * sea_u + 1); c.set_source_rgba(*hx('2D6CDF', .7)); c.fill()
        if T > wfind(8, 'fires'):
            for k in range(5):
                x = 640 + k * 80; f = 60 + 20 * math.sin(T * 9 + k)
                c.move_to(x - 30, 1080); c.curve_to(x - 40, 1080 - f, x, 1040 - f, x, 1000 - f); c.curve_to(x + 10, 1040 - f, x + 40, 1080 - f, x + 30, 1080); c.close_path()
                c.set_source_rgba(*hx('F28C28')); c.fill_preserve(); ink(c, 4); c.stroke()
    overlay(fr, L_(dr))
    tape(fr, 'IT NEEDS HELP', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    SP(fr, T, 380, 1170, .4, .3)
    if T > wfind(8, 'seas'): chip(fr, 'RISING SEAS', 300, 760, T - wfind(8, 'seas'), 'FFFFFF', 38, -4)
    if T > wfind(8, 'fires'): chip(fr, 'FIRES', 800, 820, T - wfind(8, 'fires'), YEL, 42, 4)

def s_end(fr, T):
    lt = T - S[9]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .16)
    overlay(fr, L_(lambda c: (helix(c, 150, 1050, 560, T, al=.6), helix(c, 930, 1050, 560, T + 1, al=.6), quarter(c, CX, 1220, 1.0, T))))
    SP(fr, T, CX, 1080, 1.0)
    tape(fr, 'NEXT TIME YOU SPOT ONE', CX, 470, lt, col='FFFFFF', size=52, font=LUCKY, rot=-2)
    if T > wfind(9, 'beat') - .3: title(fr, 'ITS DNA MIGHT BEAT YOURS', 620, T - wfind(9, 'beat') + .3, size=86, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_more), (S[3], s_dunes), (S[4], s_door), (S[5], s_read), (S[6], s_yours), (S[7], s_repeat), (S[8], s_genes), (S[9], s_threat), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(1, 'fifty'), wfind(3, 'dinner'), wfind(6, 'twist')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Study: Bond et al., Journal of Heredity (2026)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
