import sys, os, json, math
sys.path.insert(0, '/home/claude/enamel')
from kit import *
D = '/home/claude/enamel'
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





def tooth_path(c):
    c.move_to(-150, -170); c.curve_to(-170, -260, -60, -270, 0, -220); c.curve_to(60, -270, 170, -260, 150, -170)
    c.curve_to(150, -60, 120, 20, 100, 60); c.curve_to(90, 180, 60, 260, 40, 260); c.curve_to(20, 260, 15, 120, 0, 110)
    c.curve_to(-15, 120, -20, 260, -40, 260); c.curve_to(-60, 260, -90, 180, -100, 60); c.curve_to(-120, 20, -150, -60, -150, -170); c.close_path()

def tooth(c, x, y, s, T, enamel=1.0, chip=0.0, shine=True, face=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.translate(12, 14); tooth_path(c); c.set_source_rgba(0, 0, 0, .25); c.fill(); c.restore()
    tooth_path(c); c.set_source_rgba(*hx('F2D9A0')); c.fill_preserve(); ink(c, 9); c.stroke()
    if enamel > 0:
        c.save(); tooth_path(c); c.clip()
        c.rectangle(-200, -400, 400, 440)
        c.set_source_rgba(1, 1, 1, enamel); c.fill()
        c.restore()
        c.move_to(-128, 40); c.curve_to(-130, -60, -130, -150, -120, -180); c.set_source_rgba(*hx('1C1614', .25 * enamel)); c.set_line_width(4); c.stroke()
    if chip > 0:
        c.move_to(60, -238); c.line_to(60 + 40 * chip, -180 + 20 * chip); c.line_to(150, -175 + 60 * chip); c.line_to(155, -230); c.close_path()
        c.set_source_rgba(*hx('F2D9A0')); c.fill_preserve(); ink(c, 6); c.stroke()
    if shine:
        c.move_to(-90, -190); c.curve_to(-100, -140, -100, -100, -95, -70); c.set_source_rgba(*hx(CYAN, .6)); c.set_line_width(14); c.set_line_cap(1); c.stroke()
    if face:
        for ex in (-50, 50): c.arc(ex, -120, 14, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
        if face > 0: c.arc(0, -90, 40, .3, 2.84)
        else: c.arc(0, -40, 40, 3.44, 5.98)
        c.set_line_width(8); c.stroke()
    c.restore()

def can(c, x, y, s, rot=0):
    c.save(); c.translate(x, y); c.rotate(math.radians(rot)); c.scale(s, s)
    c.rectangle(-90 + 12, -170 + 14, 180, 340); c.set_source_rgba(0, 0, 0, .25); c.fill()
    c.rectangle(-90, -170, 180, 340); c.set_source_rgba(*hx('2D6CDF')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.rectangle(-90, -170, 180, 30); c.set_source_rgba(*hx('C9CED6')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.rectangle(-90, 140, 180, 30); c.set_source_rgba(*hx('C9CED6')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.move_to(-90, 20); c.curve_to(-30, -40, 30, 80, 90, 0); c.set_source_rgba(1, 1, 1, .9); c.set_line_width(16); c.stroke()
    c.restore()

def drops(c, T, x0, y0, x1, y1, n=8, col='9BE15D', lab=None):
    for k in range(n):
        u = (T * .6 + k / n) % 1.0; px, py = lerp(x0, x1, u) + 20 * math.sin(k * 3 + T * 3), lerp(y0, y1, u)
        c.arc(px, py, 20, 0, 6.29); c.set_source_rgba(*hx(col, .9)); c.fill_preserve(); ink(c, 4); c.stroke()
        if lab:
            c.select_font_face('Inter', 0, 1); c.set_font_size(18); c.set_source_rgba(*hx('1C1614')); c.move_to(px - 14, py + 6); c.show_text(lab)

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'D6EEF0'); rays(fr, T, 'FFFFFF', .14)
    overlay(fr, L_(lambda c: tooth(c, CX, 1060, 1.35 * back(clamp((T + .4) / .4)), T, 1.0, 0, True, 1)))
    t1 = wfind(0, 'regrow')
    if T > t1: burst(fr, 'NO REFILLS', 820, 820, T - t1, r=140, col=YEL, size=36, rot=10)
    tape(fr, 'TOOTH ENAMEL', CX, 470, T + .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'IT CAN\'T GROW BACK', 600, T + .3, size=104, fill=YEL, rot=-2)

def s_chip(fr, T):
    fr[:] = essay_slide(T, [('CHIP IT...', 'grey'), ('GONE FOR GOOD.', 'hl')], [S[1], wfind(1, 'gone')], size=124)
    lt = T - S[1]; t1 = wfind(1, 'chip')
    overlay(fr, L_(lambda c: tooth(c, CX, 1130, .95, T, 1.0, clamp((T - t1) / .3) if T > t1 else 0, True, -1)))
    if T > wfind(1, 'until'): chip(fr, 'UNTIL MAYBE NOW', CX, 1380, T - wfind(1, 'until'), YEL, 40, -2)

def s_acid(fr, T):
    lt = T - S[2]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'HARDEST THING IN YOU', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    t1 = wfind(2, 'acid')
    e = 1.0 - .6 * clamp((T - t1) / 3) if T > t1 else 1.0
    def dr(c):
        tooth(c, 380, 1040, 1.05, T, e, 0, True, 0)
        if T > t1 - .3:
            can(c, 820, 960, .9 * back(clamp((T - t1 + .3) / .35)), 15)
            drops(c, T, 760, 820, 470, 980, 7, '9BE15D')
    overlay(fr, L_(dr))
    if T > t1: chip(fr, 'ACID', 760, 1240, T - t1, '9BE15D', 44, 4); title(fr, 'SODA EATS IT', 620, T - t1, size=110, fill=YEL)

def s_fluor(fr, T):
    fr[:] = essay_slide(T, [('FLUORIDE PATCHES.', 'grey'), ("IT CAN'T REBUILD.", 'hl')], [S[3], wfind(3, 'rebuild')], size=110)
    lt = T - S[3]
    def dr(c):
        c.save(); c.translate(360, 1120); c.rotate(-.3)
        c.rectangle(-180, -50, 330, 100); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
        c.rectangle(150, -30, 50, 60); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 6); c.stroke()
        c.rectangle(-120, -50, 120, 100); c.set_source_rgba(*hx(CYAN)); c.fill(); c.restore()
        tooth(c, 770, 1120, .7, T, .35, 1.0, False, -1)
    overlay(fr, L_(dr))

def s_gel(fr, T):
    lt = T - S[4]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'ENGLAND LAB', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        c.save(); c.translate(CX, 1060); s_ = back(clamp(lt / .35)); c.scale(s_, s_)
        c.rectangle(-150 + 12, -60 + 14, 300, 300); c.set_source_rgba(0, 0, 0, .25); c.fill()
        c.rectangle(-150, -60, 300, 300); c.set_source_rgba(*hx('B8E6F0', .9)); c.fill_preserve(); ink(c, 9); c.stroke()
        c.rectangle(-170, -150, 340, 100); c.set_source_rgba(*hx('FFFFFF')); c.fill_preserve(); ink(c, 9); c.stroke()
        for k in range(6):
            c.arc(-90 + k * 36, 60 + 50 * math.sin(T * 2 + k), 14, 0, 6.29); c.set_source_rgba(1, 1, 1, .8); c.fill()
        c.restore()
    overlay(fr, L_(dr))
    if T > wfind(4, 'protein'): chip(fr, 'PROTEIN GEL', CX, 1350, T - wfind(4, 'protein'), YEL, 44, -2); title(fr, 'A TOOTH GEL', 620, T - wfind(4, 'protein'), size=110, fill=YEL)
    if T > wfind(4, 'copies'): chip(fr, 'COPIES HOW TEETH FORM', CX, 780, T - wfind(4, 'copies'), CYAN, 36, 2)

def s_spit(fr, T):
    lt = T - S[5]; bg(fr, T, 'F7E3C8'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'HOW IT WORKS', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    t1 = wfind(5, 'calcium')
    def dr(c):
        tooth(c, CX, 1050, 1.15, T, .5, 0, False, 0)
        u = clamp(lt / 1.2)
        c.move_to(300, 840); c.curve_to(420, 760, 660, 760, 780, 840 + 0 * u); c.set_source_rgba(*hx('6FD3E8', .9 * u)); c.set_line_width(40); c.set_line_cap(1); c.stroke()
        if T > t1: drops(c, T, 120, 1350, 480, 900, 6, 'FFFFFF', 'Ca'); drops(c, T + .5, 980, 1350, 640, 900, 6, 'FFFFFF', 'Ca')
    overlay(fr, L_(dr))
    if T > wfind(5, 'cracks'): chip(fr, 'PAINTED INTO CRACKS', 330, 700, T - wfind(5, 'cracks'), CYAN, 34, -3)
    if T > wfind(5, 'spit'): title(fr, 'CALCIUM FROM SPIT', 620, T - wfind(5, 'spit'), size=96, fill=YEL); burst(fr, 'SALIVA!', 840, 1300, T - wfind(5, 'spit'), r=120, col=YEL, size=40, rot=8)

def s_grow(fr, T):
    lt = T - S[6]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'LINED UP', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        for k in range(10):
            x = 160 + k * 78
            c.rectangle(x, 1100, 52, 200); c.set_source_rgba(*hx('E4E4E4')); c.fill_preserve(); ink(c, 5); c.stroke()
            h = 280 * eout(clamp((lt - .3 - k * .12) / .6))
            if h > 1: c.rectangle(x, 1100 - h, 52, h); c.set_source_rgba(*hx('DFF6FB')); c.fill_preserve(); ink(c, 5); c.stroke()
    overlay(fr, L_(dr))
    chip(fr, 'OLD ENAMEL', 300, 1350, lt - .2, 'FFFFFF', 34, -2)
    if lt > 1: chip(fr, 'NEW CRYSTALS', 760, 760, lt - 1, YEL, 36, 3)
    if T > wfind(6, 'lined'): title(fr, 'SAME DIRECTION', 620, T - wfind(6, 'lined'), size=104, fill=YEL)

def s_lab(fr, T):
    lt = T - S[7]; bg(fr, T, 'D6EEF0'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'LAB TESTS', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: tooth(c, CX, 1060, 1.2 * back(clamp(lt / .35)), T, 1.0, 0, True, 1)))
    t1 = wfind(7, 'healthy')
    if T > t1: burst(fr, 'LIKE NEW', 830, 1290, T - t1, r=140, col=YEL, size=40, rot=8); title(fr, 'ACTS LIKE REAL ENAMEL', 620, T - t1, size=88, fill=YEL)

def s_caveat(fr, T):
    fr[:] = essay_slide(T, [('NOT TESTED', 'grey'), ('IN PATIENTS YET.', 'hl')], [S[8], wfind(8, 'patients')], size=124)
    overlay(fr, L_(lambda c: tooth(c, CX, 1150, .8, T, 1.0, 0, False, 0)))
    chip(fr, 'LAB ONLY', 830, 1000, T - S[8] - .3, YEL, 40, -3)

def s_end(fr, T):
    lt = T - S[9]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tape(fr, 'FIRST PRODUCT IN THE WORKS', CX, 470, lt, col=RED, size=50, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: tooth(c, CX, 1060, 1.25 * back(clamp(lt / .35)), T, 1.0, 0, True, 1)))
    if T > wfind(9, 'right now') - .2: title(fr, 'REGROW YOUR ENAMEL?', 620, T - wfind(9, 'right now') + .2, size=96, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_chip), (S[3], s_acid), (S[4], s_fluor), (S[5], s_gel), (S[6], s_spit), (S[7], s_grow), (S[8], s_lab), (S[9], s_caveat), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(1, 'chip'), wfind(5, 'spit'), wfind(7, 'healthy')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Study: Univ. of Nottingham, Nature Communications')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
