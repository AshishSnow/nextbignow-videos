import sys, os, json, math
sys.path.insert(0, '/home/claude/sailor')
from kit import *
D = '/home/claude/sailor'
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


def sea(c, T, y=1180, col='2D6CDF', amp=18):
    c.move_to(0, y)
    for x in range(0, W + 20, 20): c.line_to(x, y + amp * math.sin(x / 70 + T * 2.5))
    c.line_to(W, H); c.line_to(0, H); c.close_path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()
    for k in range(5):
        yy = y + 70 + k * 60; c.move_to(0, yy)
        for x in range(0, W + 20, 20): c.line_to(x, yy + 10 * math.sin(x / 50 + T * 3 + k))
        c.set_source_rgba(1, 1, 1, .25); c.set_line_width(5); c.stroke()

def boat(c, x, y, s, T, torn=0.0, rock=1.0):
    if s < .01: return
    c.save(); c.translate(x, y); c.rotate(.08 * rock * math.sin(T * 2)); c.scale(s, s)
    c.move_to(-220, 0); c.line_to(220, 0); c.line_to(160, 90); c.line_to(-160, 90); c.close_path(); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    c.rectangle(-220, 30, 440, 18); c.set_source_rgba(*hx(RED)); c.fill()
    c.move_to(0, 0); c.line_to(0, -420); ink(c, 10); c.stroke()
    if torn < .5:
        c.move_to(15, -400); c.line_to(190, -20); c.line_to(15, -20); c.close_path()
        c.set_source_rgba(*hx('F7F1E3')); c.fill_preserve(); ink(c, 7); c.stroke()
        c.move_to(-15, -330); c.line_to(-150, -20); c.line_to(-15, -20); c.close_path(); c.set_source_rgba(*hx('F7F1E3')); c.fill_preserve(); ink(c, 7); c.stroke()
    else:
        c.move_to(15, -400); c.line_to(120, -260); c.line_to(60, -230); c.line_to(140, -160); c.line_to(15, -200); c.close_path()
        c.set_source_rgba(*hx('E6DCC6')); c.fill_preserve(); ink(c, 7); c.stroke()
        c.move_to(-15, -330); c.line_to(-90, -220); c.line_to(-40, -200); c.line_to(-15, -150); c.close_path(); c.set_source_rgba(*hx('E6DCC6')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.restore()

def dog(c, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.scale(1.5, 1); c.arc(0, 0, 50, 0, 6.29); c.restore(); c.set_source_rgba(*hx('C98A4B')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(-80, -45, 42, 0, 6.29); c.set_source_rgba(*hx('C98A4B')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.move_to(-100, -80); c.curve_to(-130, -60, -125, -20, -105, -15); c.set_source_rgba(*hx('7A4E2A')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.arc(-118, -40, 9, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(-80, -55, 6, 0, 6.29); c.fill()
    c.move_to(70, -10); c.line_to(105, -40 + 10 * math.sin(T * 10)); ink(c, 8); c.stroke()
    for lx in (-40, 40): c.move_to(lx, 40); c.line_to(lx, 80); ink(c, 10); c.stroke()
    c.restore()

def beacon(c, x, y, s, T, on=0.0):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    if on > 0:
        for k in range(3):
            u = (T * .9 + k / 3) % 1; c.arc(0, -120, 60 + 260 * u, 0, 6.29); c.set_source_rgba(*hx(RED, (1 - u) * on)); c.set_line_width(10); c.stroke()
    c.rectangle(-60 + 10, -100 + 12, 120, 220); c.set_source_rgba(0, 0, 0, .25); c.fill()
    c.rectangle(-60, -100, 120, 220); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.move_to(0, -100); c.line_to(0, -200); ink(c, 10); c.stroke()
    c.arc(0, -210, 22, 0, 6.29); c.set_source_rgba(*hx(RED if on > 0 and (T * 3) % 1 < .5 else '777777')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.rectangle(-35, -60, 70, 50); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.restore()

def plane(c, x, y, s):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.scale(3, 1); c.arc(0, 0, 40, 0, 6.29); c.restore(); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 6); c.stroke()
    c.move_to(-20, 0); c.line_to(30, -110); c.line_to(60, -110); c.line_to(40, 0); c.close_path(); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 6); c.stroke()
    c.move_to(-110, -10); c.line_to(-140, -70); c.line_to(-115, -70); c.line_to(-90, -10); c.close_path(); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def ship(c, x, y, s):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-300, 0); c.line_to(300, 0); c.line_to(250, 110); c.line_to(-270, 110); c.close_path(); c.set_source_rgba(*hx('2B2B33')); c.fill_preserve(); ink(c, 7); c.stroke()
    for k, col in enumerate((RED, YEL, CYAN, RED, YEL)):
        c.rectangle(-220 + k * 80, -70, 74, 70); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 5); c.stroke()
    c.rectangle(180, -150, 90, 150); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def heli(c, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.scale(1.5, 1); c.arc(0, 0, 70, 0, 6.29); c.restore(); c.set_source_rgba(*hx('F28C28')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.move_to(100, -10); c.line_to(260, -20); ink(c, 14); c.stroke()
    w = 260 * abs(math.cos(T * 25)); c.move_to(-w, -90); c.line_to(w, -90); ink(c, 10); c.stroke()
    c.move_to(0, -70); c.line_to(0, -90); ink(c, 8); c.stroke()
    c.arc(-40, -10, 30, 0, 6.29); c.set_source_rgba(*hx(CYAN)); c.fill()
    c.restore()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .12)
    overlay(fr, L_(lambda c: (boat(c, CX, 1150, 1.0 * back(clamp((T + .4) / .4)), T, 1.0), sea(c, T))))
    tape(fr, '2 MONTHS SILENT', CX, 470, T + .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'LOST AT SEA', 600, T + .3, size=120, fill=YEL, rot=-2)
    if T > wfind(0, 'silent'): burst(fr, 'SILENT', 820, 780, T - wfind(0, 'silent'), r=110, col=YEL, size=44, rot=10)

def s_sailor(fr, T):
    lt = T - S[1]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tape(fr, 'TRUE STORY', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: (person(c, 380, 980, 1.1 * back(clamp(lt / .35)), T, 0, False, BLUE), dog(c, 740, 1190, 1.4 * back(clamp((T - wfind(1, 'dog')) / .35)) if T > wfind(1, 'dog') else 0, T))))
    if T > wfind(1, 'eighty'): title(fr, 'AGE 86', 600, T - wfind(1, 'eighty'), size=130, fill=YEL)
    if T > wfind(1, 'dog'): chip(fr, '+ HIS DOG', 760, 1000, T - wfind(1, 'dog'), 'FFFFFF', 44, 4)

def s_route(fr, T):
    lt = T - S[2]; bg(fr, T, 'D6EEF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THE TRIP', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    u = eout(clamp(lt / 4))
    def dr(c):
        c.rectangle(80, 640, 920, 760); c.set_source_rgba(*hx('6FB7E8')); c.fill_preserve(); ink(c, 8); c.stroke()
        c.move_to(760, 640); c.line_to(1000, 640); c.line_to(1000, 1000); c.curve_to(900, 960, 840, 900, 800, 820); c.close_path(); c.set_source_rgba(*hx('9CCB7A')); c.fill_preserve(); ink(c, 6); c.stroke()
        x0, y0, x1, y1 = 820, 760, 240, 1300
        c.move_to(x0, y0); c.curve_to(600, 900, 380, 1100, lerp(x0, x1, u), lerp(y0, y1, u)) if False else None
        pts = [(lerp(x0, x1, v) - 120 * math.sin(math.pi * v), lerp(y0, y1, v)) for v in np.linspace(0, u, 40)]
        c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
        c.set_source_rgba(*hx(RED)); c.set_line_width(10); c.set_dash([22, 14]); c.stroke(); c.set_dash([])
        c.arc(x0, y0, 16, 0, 6.29); c.set_source_rgba(*hx(RED)); c.fill()
        c.arc(x1, y1, 18, 0, 6.29); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 4); c.stroke()
    overlay(fr, L_(dr))
    chip(fr, 'OREGON', 820, 700, lt - .2, 'FFFFFF', 34, 3)
    if T > wfind(2, 'samoa'): chip(fr, 'AMERICAN SAMOA', 330, 1340, T - wfind(2, 'samoa'), YEL, 34, -3)
    if T > wfind(2, 'thousands'): title(fr, 'THOUSANDS OF MILES', 600, T - wfind(2, 'thousands'), size=92, fill=YEL)

def s_aug(fr, T):
    fr[:] = essay_slide(T, [('AUGUST 20:', 'grey'), ('RADIO SILENCE.', 'hl')], [S[3], wfind(3, 'radio')], size=124)
    lt = T - S[3]
    def dr(c):
        c.rectangle(CX - 110, 1050, 220, 160); c.set_source_rgba(*hx('C9CED6')); c.fill_preserve(); ink(c, 8); c.stroke()
        c.move_to(CX + 60, 1050); c.line_to(CX + 100, 930); ink(c, 8); c.stroke()
        c.arc(CX - 40, 1130, 40, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    overlay(fr, L_(dr))
    if T > wfind(3, 'stopped'): xstamp(fr, CX, 1130, T - wfind(3, 'stopped'), 1.0)

def s_oct(fr, T):
    lt = T - S[4]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'NO ALARM', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    def cal(c, x, y, lab, num, sc, rot):
        c.save(); c.translate(x, y); c.rotate(math.radians(rot)); c.scale(sc, sc)
        c.rectangle(-150 + 10, -150 + 12, 300, 300); c.set_source_rgba(0, 0, 0, .25); c.fill()
        c.rectangle(-150, -150, 300, 300); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
        c.rectangle(-150, -150, 300, 80); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 8); c.stroke()
        c.select_font_face('Luckiest Guy'); c.set_font_size(54); c.set_source_rgba(1, 1, 1, 1); e = c.text_extents(lab); c.move_to(-e.width / 2, -92); c.show_text(lab)
        c.set_font_size(130); c.set_source_rgba(*hx('1C1614')); e = c.text_extents(num); c.move_to(-e.width / 2, 110); c.show_text(num)
        c.restore()
    overlay(fr, L_(lambda c: (cal(c, 300, 1010, 'AUG', '20', back(clamp(lt / .3)), -6), cal(c, 780, 1060, 'OCT', '24', back(clamp((T - wfind(4, 'october')) / .3)) if T > wfind(4, 'october') else 0.001, 6))))
    if T > wfind(4, 'october'): title(fr, '2 MONTHS LATER', 600, T - wfind(4, 'october'), size=104, fill=YEL)

def s_drift(fr, T):
    lt = T - S[5]; bg(fr, T, 'B9C4CF'); rays(fr, T, 'FFFFFF', .08)
    tape(fr, 'DRIFTING', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: (boat(c, CX + 40 * math.sin(T * .7), 1160, 1.0, T, 1.0, 2.5), sea(c, T, 1180, '24508F', 30))))
    if T > wfind(5, 'torn'): chip(fr, 'SAILS TORN', 300, 720, T - wfind(5, 'torn'), YEL, 44, -4); title(fr, 'NO WAY HOME', 600, T - wfind(5, 'torn'), size=110, fill=YEL)

def s_save(fr, T):
    fr[:] = essay_slide(T, [('WHAT SAVED HIM?', 'grey'), ('HIS BEACON.', 'hl')], [S[6], wfind(6, 'beacon')], size=120)
    t1 = wfind(6, 'beacon')
    overlay(fr, L_(lambda c: beacon(c, CX, 1220, .9, T, clamp((T - t1) / .3) if T > t1 else 0)))
    if T > wfind(6, 'three'): chip(fr, '3 DAYS AFTER THE ALARM', CX, 830, T - wfind(6, 'three'), YEL, 34, -2)

def s_plane(fr, T):
    lt = T - S[7]; bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'SPOTTED', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    u = eout(clamp(lt / 2.5))
    overlay(fr, L_(lambda c: (boat(c, 760, 1180, .6, T, 1.0), sea(c, T, 1200), plane(c, lerp(-100, 380, u), 760, .9))))
    if T > wfind(7, 'four'): title(fr, '460 MILES OFF SAN DIEGO', 600, T - wfind(7, 'four'), size=84, fill=YEL)

def s_rescue(fr, T):
    lt = T - S[8]; bg(fr, T, 'F7E3C8'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'RESCUED', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    t1 = wfind(8, 'helicopter')
    def dr(c):
        ship(c, 560, 1170, 1.0 * back(clamp(lt / .35)))
        sea(c, T, 1260)
        if T > t1 - .3: heli(c, lerp(1200, 700, eout(clamp((T - t1 + .3) / 1.2))), 840, .8, T)
    overlay(fr, L_(dr))
    if T > wfind(8, 'dog'): chip(fr, 'MAN + DOG SAFE', 330, 760, T - wfind(8, 'dog'), YEL, 40, -3)

def s_end(fr, T):
    fr[:] = essay_slide(T, [('CARRY A BEACON.', 'main'), ('TELL SOMEONE YOUR PLAN.', 'hl')], [S[9], wfind(9, 'tell')], size=86)
    overlay(fr, L_(lambda c: beacon(c, CX, 1250, .7, T, 1.0)))

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_sailor), (S[3], s_route), (S[4], s_aug), (S[5], s_oct), (S[6], s_drift), (S[7], s_save), (S[8], s_plane), (S[9], s_rescue), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(3, 'stopped'), wfind(6, 'beacon'), wfind(8, 'helicopter')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Source: U.S. Coast Guard via news reports')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
