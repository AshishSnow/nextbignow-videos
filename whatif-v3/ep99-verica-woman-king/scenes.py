import sys, os, json, math
sys.path.insert(0, '/home/claude/verica')
from kit import *
D = '/home/claude/verica'
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



GOLD = 'E3B341'

def britain(c, x, y, s, hl=0.0):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    pts = [(-40, -330), (40, -300), (60, -220), (20, -160), (90, -60), (120, 40), (160, 120), (190, 200), (120, 230), (40, 250), (-60, 260), (-160, 290), (-120, 220), (-60, 180), (-90, 100), (-40, 20), (-90, -60), (-60, -140), (-100, -220), (-70, -290)]
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.close_path(); c.set_source_rgba(*hx('9CCB7A')); c.fill_preserve(); ink(c, 8); c.stroke()
    if hl > 0:
        c.save(); c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
        c.close_path(); c.clip()
        c.rectangle(-200, 170, 420, 140); c.set_source_rgba(*hx(RED, .75 * hl)); c.fill(); c.restore()
    c.restore()

def coin(c, x, y, s, T, kind='slender', label='REX'):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.arc(12, 14, 200, 0, 6.29); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.arc(0, 0, 200, 0, 6.29); c.set_source_rgba(*hx(GOLD)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(0, 0, 175, 0, 6.29); c.set_source_rgba(*hx('B8860B')); c.set_line_width(4); c.stroke()
    # horse
    c.save(); c.scale(1.6, 1); c.arc(0, 40, 45, 0, 6.29); c.restore(); c.set_source_rgba(*hx('B8860B')); c.fill()
    c.move_to(60, 20); c.line_to(110, -40); c.line_to(130, -20); c.line_to(90, 40); c.close_path(); c.fill()
    for lx in (-50, -20, 30, 60): c.move_to(lx, 70); c.line_to(lx, 130); c.set_line_width(10); c.stroke()
    # rider
    w = 10 if kind == 'slender' else 24
    c.move_to(0, 0); c.line_to(10, -70); c.set_line_width(w); c.stroke()
    c.arc(12, -95, 18 if kind == 'slender' else 24, 0, 6.29); c.fill()
    if kind != 'slender':
        c.move_to(-10, -60); c.line_to(-80, -130); c.set_line_width(8); c.stroke()
        c.save(); c.translate(40, -40); c.scale(1, 1.3); c.arc(0, 0, 30, 0, 6.29); c.restore(); c.fill()
    c.select_font_face('Luckiest Guy'); c.set_font_size(48); c.set_source_rgba(*hx('7A5A10')); e = c.text_extents(label); c.move_to(-e.width / 2, -130); c.show_text(label)
    c.restore()

def ship(c, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.rotate(.06 * math.sin(T * 2)); c.scale(s, s)
    c.move_to(-200, 0); c.line_to(200, 0); c.line_to(150, 80); c.line_to(-150, 80); c.close_path(); c.set_source_rgba(*hx('8B5A3C')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.move_to(0, 0); c.line_to(0, -260); ink(c, 8); c.stroke()
    c.rectangle(-110, -240, 220, 180); c.set_source_rgba(*hx('F7F1E3')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.rectangle(-110, -170, 220, 30); c.set_source_rgba(*hx(RED)); c.fill()
    for k in range(5): c.move_to(-120 + k * 60, 60); c.line_to(-150 + k * 60, 130); ink(c, 5); c.stroke()
    c.restore()

def column(c, x, y, s):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-110, -320, 220, 40); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 6); c.stroke()
    c.rectangle(-80, -280, 160, 400); c.set_source_rgba(*hx('F2EDE4')); c.fill_preserve(); ink(c, 6); c.stroke()
    for k in range(4): c.move_to(-50 + k * 33, -270); c.line_to(-50 + k * 33, 110); c.set_source_rgba(*hx('1C1614', .3)); c.set_line_width(4); c.stroke()
    c.rectangle(-120, 120, 240, 50); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def shield(c, x, y, s):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-70 + 8, -110 + 10, 140, 220); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.rectangle(-70, -110, 140, 220); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(0, 0, 26, 0, 6.29); c.set_source_rgba(*hx(GOLD)); c.fill_preserve(); ink(c, 5); c.stroke()
    for sx in (-1, 1): c.move_to(sx * 40, -80); c.line_to(sx * 40, 80); c.set_source_rgba(*hx(GOLD)); c.set_line_width(8); c.stroke()
    c.restore()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    overlay(fr, L_(lambda c: (britain(c, 330, 1040, 1.1 * back(clamp((T + .4) / .4)), clamp(T / 1.5)), coin(c, 790, 1100, .9 * back(clamp((T - .3) / .4)), T))))
    if T > wfind(0, 'woman'): burst(fr, 'A WOMAN?', 790, 830, T - wfind(0, 'woman'), r=130, col=YEL, size=40, rot=10)
    tape(fr, 'ROMAN BRITAIN', CX, 470, T + .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'THE KING WAS A WOMAN?', 600, T + .3, size=94, fill=YEL, rot=-2)

def s_name(fr, T):
    fr[:] = essay_slide(T, [('NOT BOUDICA.', 'grey'), ('VERICA.', 'hl')], [S[1], wfind(1, 'verica')], size=128)
    overlay(fr, L_(lambda c: coin(c, CX, 1180, .7 * back(clamp((T - wfind(1, 'verica')) / .35)) if T > wfind(1, 'verica') else 0, T)))

def s_ousted(fr, T):
    lt = T - S[2]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'AROUND AD 40', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: britain(c, CX, 1030, 1.25 * back(clamp(lt / .35)), clamp((T - wfind(2, 'southern')) / .6) if T > wfind(2, 'southern') else 0)))
    if T > wfind(2, 'forced'): title(fr, 'FORCED OUT', 620, T - wfind(2, 'forced'), size=120, fill=YEL)
    if T > wfind(2, 'southern'): chip(fr, 'SOUTHERN BRITAIN', 760, 1330, T - wfind(2, 'southern'), 'FFFFFF', 36, 3)

def s_flee(fr, T):
    lt = T - S[3]; bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'TO ROME', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    u = eout(clamp(lt / 3))
    def dr(c):
        column(c, 860, 1080, .9)
        ship(c, lerp(200, 560, u), 1150, .75, T)
        c.rectangle(0, 1250, W, 200); c.set_source_rgba(*hx('5FB0E0')); c.fill()
    overlay(fr, L_(dr))
    if T > wfind(3, 'help'): chip(fr, 'ASKED THE EMPEROR FOR HELP', CX, 760, T - wfind(3, 'help'), YEL, 36, -2)

def s_invade(fr, T):
    fr[:] = essay_slide(T, [('3 YEARS LATER:', 'grey'), ('ROME INVADED.', 'hl')], [S[4], wfind(4, 'legions')], size=118)
    lt = T - S[4]
    overlay(fr, L_(lambda c: [shield(c, 260 + k * 190, 1180, .7 * back(clamp((lt - k * .12) / .3))) for k in range(4)]))
    chip(fr, 'AD 43', CX, 1400 - 40, lt - .3, YEL, 40, -2)

def s_king(fr, T):
    lt = T - S[5]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THE OLD STORY', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        c.rectangle(240, 760, 600, 500); c.set_source_rgba(*hx('F7F1E3')); c.fill_preserve(); ink(c, 8); c.stroke()
        for k in range(8): c.move_to(290, 830 + k * 50); c.line_to(790 - (k % 3) * 80, 830 + k * 50); c.set_source_rgba(*hx('1C1614', .3)); c.set_line_width(6); c.stroke()
    overlay(fr, L_(dr))
    if T > wfind(5, 'king'): chip(fr, '"KING VERICA"', CX, 920, T - wfind(5, 'king'), 'FFFFFF', 54, -3)
    if T > wfind(5, 'man'): title(fr, 'A MAN?', 620, T - wfind(5, 'man'), size=130, fill=YEL)

def s_letter(fr, T):
    lt = T - S[6]; bg(fr, T, 'F7E3C8'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'LOOK AGAIN', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    t1 = wfind(6, 'ends')
    def dr(c):
        c.select_font_face('Luckiest Guy'); c.set_font_size(190)
        txt = 'VERIC'; e = c.text_extents(txt + 'A'); x0 = CX - e.width / 2
        c.move_to(x0 + 8, 1110 + 10); c.set_source_rgba(0, 0, 0, .3); c.show_text(txt + 'A')
        c.move_to(x0, 1110); c.set_source_rgba(*hx('1C1614')); c.show_text(txt)
        xa = x0 + c.text_extents(txt).x_advance
        if T > t1:
            k = back(clamp((T - t1) / .3)); c.save(); c.translate(xa + 60, 1040); c.scale(1 + .3 * k, 1 + .3 * k); c.move_to(-60, 70); c.set_source_rgba(*hx(RED)); c.show_text('A'); c.restore()
        else: c.move_to(xa, 1110); c.show_text('A')
    overlay(fr, L_(dr))
    chip(fr, '1 ARCHAEOLOGIST, BOURNEMOUTH UNIV.', CX, 770, lt - .2, CYAN, 30, -2)
    if T > wfind(6, 'women'): chip(fr, 'COMMON IN WOMEN\'S NAMES', CX, 1290, T - wfind(6, 'women'), YEL, 36, 2)

def s_coins(fr, T):
    lt = T - S[7]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tape(fr, 'THE COINS', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    t2 = wfind(7, 'warrior')
    overlay(fr, L_(lambda c: (coin(c, 300, 1030, .95 * back(clamp(lt / .35)), T, 'slender', 'VERICA'), coin(c, 790, 1030, .95 * back(clamp((T - t2 + .3) / .35)) if T > t2 - .3 else 0, T, 'warrior', 'OTHERS'))))
    if T > wfind(7, 'slender'): chip(fr, 'SLENDER RIDER', 300, 1290, T - wfind(7, 'slender'), YEL, 36, -3)
    if T > t2: chip(fr, 'MALE WARRIOR', 790, 1290, T - t2, 'FFFFFF', 36, 3)

def s_rex(fr, T):
    lt = T - S[8]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'EVEN THE TITLE', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: coin(c, CX, 1040, 1.3 * back(clamp(lt / .35)), T, 'slender', 'REX')))
    if T > wfind(8, 'rex'): title(fr, 'REX = RULER', 620, T - wfind(8, 'rex'), size=120, fill=YEL)
    if T > wfind(8, 'female'): chip(fr, 'ANY GENDER? (HIS ARGUMENT)', CX, 1340, T - wfind(8, 'female'), YEL, 34, -2)

def s_end(fr, T):
    fr[:] = essay_slide(T, [('ONE EXPERT. NOT PROOF.', 'grey'), ('BUT IF TRUE...', 'hl')], [S[9], wfind(9, 'right')], size=100)
    lt = T - S[9]
    overlay(fr, L_(lambda c: (britain(c, 330, 1160, .55, 1.0), coin(c, 770, 1160, .6, T))))
    chip(fr, 'NEW BOOK, 2027', CX, 870, lt - .4, YEL, 34, -2)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_name), (S[3], s_ousted), (S[4], s_flee), (S[5], s_invade), (S[6], s_king), (S[7], s_letter), (S[8], s_coins), (S[9], s_rex), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'woman'), wfind(4, 'legions'), wfind(6, 'ends')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Source: M. Russell, Bournemouth University')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
