import sys, os, json, math
sys.path.insert(0, '/home/claude/coffin')
from kit import *
D = '/home/claude/coffin'
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





STONE = 'D9CFC0'

def coffin(c, x, y, s, T, lid=0.0, cross=True, text=True):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-330 + 14, -110 + 16, 660, 260); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.rectangle(-330, -110, 660, 260); c.set_source_rgba(*hx(STONE)); c.fill_preserve(); ink(c, 9); c.stroke()
    if text:
        c.rectangle(-200, -70, 400, 150); c.set_source_rgba(*hx('C9BDA8')); c.fill_preserve(); ink(c, 5); c.stroke()
        c.select_font_face('Inter', 0, 1); c.set_font_size(30); c.set_source_rgba(*hx('5E5448'))
        for k, t in enumerate(('MEMORIAE', 'VALERI', 'AMANDINI')):
            e = c.text_extents(t); c.move_to(-e.width / 2, -25 + k * 42); c.show_text(t)
    for sx in (-1, 1):
        for k in range(4): c.move_to(sx * 230 + sx * k * 20, -100); c.line_to(sx * 230 + sx * k * 20, 140); c.set_source_rgba(*hx('8E8270', .5)); c.set_line_width(5); c.stroke()
    c.save(); c.translate(lid * 150, -lid * 110); c.rotate(lid * .22)
    c.rectangle(-350, -170, 700, 70); c.set_source_rgba(*hx('CFC4B2')); c.fill_preserve(); ink(c, 9); c.stroke()
    if cross:
        c.move_to(0, -160); c.line_to(0, -110); c.move_to(-30, -140); c.line_to(30, -140); c.set_source_rgba(*hx(RED)); c.set_line_width(10); c.stroke()
    c.restore(); c.restore()

def skull(c, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(.1 * math.sin(T * 3))
    c.arc(0, 0, 80, math.pi, 0); c.line_to(60, 60); c.line_to(-60, 60); c.close_path(); c.set_source_rgba(*hx('F7F1E3')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.rectangle(-45, 60, 90, 40); c.set_source_rgba(*hx('F7F1E3')); c.fill_preserve(); ink(c, 6); c.stroke()
    for k in range(4): c.move_to(-30 + k * 20, 62); c.line_to(-30 + k * 20, 98); ink(c, 4); c.stroke()
    for ex in (-30, 30): c.arc(ex, 5, 22, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.move_to(0, 30); c.line_to(-10, 48); c.line_to(10, 48); c.close_path(); c.fill()
    c.restore()

def bonehand(c, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-.3 + .15 * math.sin(T * 6))
    c.rectangle(-18, 0, 36, 140); c.set_source_rgba(*hx('F7F1E3')); c.fill_preserve(); ink(c, 5); c.stroke()
    for k in range(4):
        c.save(); c.translate(-30 + k * 20, 0); c.rotate(-.2 + .1 * k + .2 * math.sin(T * 8 + k)); c.rectangle(-6, -80, 12, 80); c.set_source_rgba(*hx('F7F1E3')); c.fill_preserve(); ink(c, 4); c.stroke(); c.restore()
    c.restore()

def abbey(c, x, y, s):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    for sx in (-1, 1):
        c.rectangle(sx * 200 - 70, -420, 140, 560); c.set_source_rgba(*hx('E8DCC4')); c.fill_preserve(); ink(c, 7); c.stroke()
        c.move_to(sx * 200 - 70, -420); c.line_to(sx * 200, -520); c.line_to(sx * 200 + 70, -420); c.close_path(); c.set_source_rgba(*hx('C9BDA8')); c.fill_preserve(); ink(c, 6); c.stroke()
        for k in range(3): c.move_to(sx * 200, -380 + k * 140); c.arc(sx * 200, -330 + k * 140, 30, math.pi, 0); c.line_to(sx * 200 + 30, -280 + k * 140); c.line_to(sx * 200 - 30, -280 + k * 140); c.close_path(); c.set_source_rgba(*hx('2D6CDF', .7)); c.fill_preserve(); ink(c, 4); c.stroke()
    c.rectangle(-130, -260, 260, 400); c.set_source_rgba(*hx('E8DCC4')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(0, -120, 90, 0, 6.29); c.set_source_rgba(*hx(RED, .7)); c.fill_preserve(); ink(c, 5); c.stroke()
    c.move_to(-60, 140); c.line_to(-60, 30); c.arc(0, 30, 60, math.pi, 0); c.line_to(60, 140); c.close_path(); c.set_source_rgba(*hx('5E3F28')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.restore()

def monk(c, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-110, 260); c.curve_to(-100, 40, -70, -60, 0, -70); c.curve_to(70, -60, 100, 40, 110, 260); c.close_path(); c.set_source_rgba(*hx('6B4A2E')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.move_to(-20, -40); c.line_to(-20, 200); c.set_source_rgba(*hx(GOLD if 'GOLD' in globals() else 'E3B341')); c.set_line_width(10); c.stroke()
    c.arc(0, -130, 62, 0, 6.29); c.set_source_rgba(*hx('F2C9A0')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(0, -165, 50, math.pi, 0); c.set_source_rgba(*hx('6B4A2E')); c.fill()
    for ex in (-20, 20): c.arc(ex, -128, 7, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.restore()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .16)
    lid = .6 * eout(clamp((T + .3) / 1.2))
    overlay(fr, L_(lambda c: (coffin(c, CX, 1170, 1.25, T, lid), skull(c, CX - 120, 1010, .8 * clamp((T - .4) / .3) if T > .4 else 0, T), bonehand(c, CX + 140, 1010, .9 * clamp((T - .7) / .3) if T > .7 else 0, T))))
    if T > wfind(0, 'stranger'): burst(fr, 'WHO?!', 860, 860, T - wfind(0, 'stranger'), r=110, col=YEL, size=50, rot=10)
    tape(fr, 'ROMAN COFFIN', CX, 470, T + .4, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'THE WRONG MAN', 600, T + .4, size=120, fill='FFFFFF', rot=-2); title(fr, 'INSIDE', 730, T + .3, size=140, fill=YEL, rot=-2)

def s_abbey(fr, T):
    fr[:] = essay_slide(T, [("LONDON'S", 'grey'), ('WESTMINSTER ABBEY.', 'hl')], [S[1], wfind(1, 'westminster')], size=104)
    overlay(fr, L_(lambda c: abbey(c, CX, 1300, .7 * back(clamp((T - S[1] - .1) / .35)))))

def s_roman(fr, T):
    lt = T - S[2]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'AROUND AD 300', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: coffin(c, CX, 1050, 1.25 * back(clamp(lt / .35)), T, 0, False)))
    if T > wfind(2, 'sons'): chip(fr, '2 ROMAN SONS', 300, 760, T - wfind(2, 'sons'), YEL, 40, -4)
    if T > wfind(2, 'dad'): title(fr, 'FOR THEIR DAD', 620, T - wfind(2, 'dad'), size=110, fill=YEL); chip(fr, 'VALERIUS AMANDINUS', CX, 1300, T - wfind(2, 'dad'), 'FFFFFF', 36, 2)

def s_cross(fr, T):
    lt = T - S[3]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'BUT THE LID...', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: coffin(c, CX, 1150, 1.4, T, 0, True)))
    if T > wfind(3, 'cross'): burst(fr, 'A CROSS', 820, 800, T - wfind(3, 'cross'), r=120, col=YEL, size=40, rot=8)
    if T > wfind(3, 'roman'): title(fr, 'NOT ROMAN', 620, T - wfind(3, 'roman'), size=120, fill=YEL)

def s_open(fr, T):
    lt = T - S[4]; bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, '2016', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    t1 = wfind(4, 'skeleton'); lid = .7 * eout(clamp((lt - .2) / 1))
    overlay(fr, L_(lambda c: (coffin(c, CX, 1170, 1.25, T, lid, True), skull(c, CX, 1000, .9 * back(clamp((T - t1) / .3)) if T > t1 else 0, T))))
    if T > t1: title(fr, 'A SKELETON', 620, T - t1, size=120, fill=YEL)
    if T > wfind(4, 'dad'): chip(fr, 'NOT THE DAD', 820, 1380 - 40, T - wfind(4, 'dad'), 'FFFFFF', 40, 4)

def s_date(fr, T):
    lt = T - S[5]; bg(fr, T, 'F7E3C8'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'RADIOCARBON DATE', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    u = eout(clamp(lt / 1.5))
    def dr(c):
        x0, x1, y = 140, 940, 1000
        c.move_to(x0, y); c.line_to(x1, y); ink(c, 10); c.stroke()
        c.arc(x0 + 60, y, 26, 0, 6.29); c.set_source_rgba(*hx(STONE)); c.fill_preserve(); ink(c, 5); c.stroke()
        xm = lerp(x0 + 60, x1 - 80, u); c.arc(xm, y, 30, 0, 6.29); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 5); c.stroke()
        skull(c, xm, y + 200, .7, T)
    overlay(fr, L_(dr))
    chip(fr, 'COFFIN: ~AD 300', 260, 900, lt - .2, 'FFFFFF', 30, -3)
    if T > wfind(5, 'thousand'): chip(fr, 'BODY: ~AD 1000', 790, 900, T - wfind(5, 'thousand'), YEL, 32, 3)
    if T > wfind(5, 'gout'): title(fr, 'MIDDLE-AGED, GOUT', 620, T - wfind(5, 'gout'), size=96, fill=YEL)

def s_who(fr, T):
    lt = T - S[6]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'WHO GETS THIS?', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (abbey(c, 300, 1250, .55), coffin(c, 760, 1180, .6, T, 0, True, False))))
    burst(fr, '?', 760, 860, lt - .3, r=110, col=YEL, size=90, rot=8)
    title(fr, 'A VIP BURIAL', 620, lt, size=120, fill=YEL)

def s_abbot(fr, T):
    lt = T - S[7]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tape(fr, 'BEST GUESS', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: monk(c, CX, 1060, 1.3 * back(clamp(lt / .35)), T)))
    if T > wfind(7, 'abbot'): title(fr, 'AN ABBOT', 620, T - wfind(7, 'abbot'), size=130, fill=YEL); chip(fr, 'LIKELY ABBOT AELFWIG', CX, 1360, T - wfind(7, 'abbot'), YEL, 34, 2)

def s_guess(fr, T):
    fr[:] = essay_slide(T, [('A GUESS,', 'grey'), ('NOT PROOF.', 'hl')], [S[8], wfind(8, 'proof')], size=128)
    lt = T - S[8]
    if T > wfind(8, 'roman'): chip(fr, 'ROMAN DAD: LOST (LOOTED 1800s)', CX, 1150, T - wfind(8, 'roman'), YEL, 32, -2)

def s_end(fr, T):
    lt = T - S[9]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .16)
    tape(fr, '2 MEN, 1 COFFIN', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (coffin(c, CX, 1170, 1.25, T, .5), skull(c, CX - 120, 1010, .8, T), bonehand(c, CX + 140, 1010, .9, T))))
    if T > wfind(9, 'hope'): title(fr, '700 YEARS APART', 620, T - wfind(9, 'hope'), size=110, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_abbey), (S[3], s_roman), (S[4], s_cross), (S[5], s_open), (S[6], s_date), (S[7], s_who), (S[8], s_abbot), (S[9], s_guess), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'stranger'), wfind(4, 'skeleton'), wfind(3, 'cross')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Study: W. Rodwell, J. British Archaeological Assoc. (2026)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
