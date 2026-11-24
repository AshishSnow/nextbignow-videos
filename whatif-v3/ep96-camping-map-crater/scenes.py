import sys, os, json, math
sys.path.insert(0, '/home/claude/crater')
from kit import *
D = '/home/claude/crater'
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



def tent(c, x, y, s):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-200 + 12, 14); c.line_to(12, -260 + 14); c.line_to(200 + 12, 14); c.close_path(); c.set_source_rgba(0, 0, 0, .25); c.fill()
    c.move_to(-200, 0); c.line_to(0, -260); c.line_to(200, 0); c.close_path(); c.set_source_rgba(*hx('F28C28')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.move_to(-60, 0); c.line_to(0, -150); c.line_to(60, 0); c.close_path(); c.set_source_rgba(*hx('7A3A12')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def satmap(c, x, y, w, h, T, ring=0.0, zoom=1.0):
    c.save(); c.rectangle(x - w / 2, y - h / 2, w, h); c.clip()
    c.rectangle(x - w / 2, y - h / 2, w, h); c.set_source_rgba(*hx('3E7A3A')); c.fill()
    rng = np.random.default_rng(5)
    for k in range(60):
        c.arc(x + rng.uniform(-w / 2, w / 2), y + rng.uniform(-h / 2, h / 2), rng.uniform(10, 40) * zoom, 0, 6.29); c.set_source_rgba(*hx(['2F5E2C', '4E8C45', '5E9C52'][k % 3])); c.fill()
    for k in range(6):
        c.save(); c.translate(x + rng.uniform(-w / 2, w / 2), y + rng.uniform(-h / 2, h / 2)); c.scale(1.6, .8); c.arc(0, 0, rng.uniform(15, 40) * zoom, 0, 6.29); c.restore()
        c.set_source_rgba(*hx('3F7FC4')); c.fill()
    c.save(); c.translate(x + 40, y + 10); c.scale(1, 1); c.arc(0, 0, 150 * zoom, 0, 6.29); c.restore(); c.set_source_rgba(*hx('6B8F5A', .9)); c.set_line_width(26 * zoom); c.stroke()
    c.arc(x + 40, y + 10, 40 * zoom, 0, 6.29); c.set_source_rgba(*hx('8A8A7A')); c.fill()
    c.save(); c.translate(x - 120 * zoom, y + 60 * zoom); c.scale(2, .7); c.arc(0, 0, 40 * zoom, 0, 6.29); c.restore(); c.set_source_rgba(*hx('3F7FC4')); c.fill()
    if ring > 0:
        c.arc(x + 40, y + 10, 190 * zoom, 0, 6.29 * ring); c.set_source_rgba(*hx(RED)); c.set_line_width(12); c.stroke()
    c.reset_clip(); c.restore()
    c.rectangle(x - w / 2, y - h / 2, w, h); ink(c, 9); c.stroke()

def phone(c, x, y, s, T, ring):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-230 + 14, -400 + 16, 460, 800); c.set_source_rgba(0, 0, 0, .25); c.fill()
    c.rectangle(-230, -400, 460, 800); c.set_source_rgba(*hx('2B2B33')); c.fill_preserve(); ink(c, 8); c.stroke()
    satmap(c, 0, 0, 400, 700, T, ring, .9)
    c.restore()

def cone(c, x, y, s):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, -260); c.line_to(-200, 160); c.curve_to(-80, 200, 80, 200, 200, 160); c.close_path()
    c.set_source_rgba(*hx('A89B8C')); c.fill_preserve(); ink(c, 8); c.stroke()
    for k in range(9):
        a = -170 + k * 42
        c.move_to(0 + a * .05, -240); c.line_to(a, 170); c.set_source_rgba(*hx('5E5448', .6)); c.set_line_width(5); c.stroke()
    c.restore()

def volcano(c, x, y, s):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-260, 160); c.line_to(-60, -150); c.line_to(60, -150); c.line_to(260, 160); c.close_path(); c.set_source_rgba(*hx('8B6A4A')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.move_to(-60, -150); c.line_to(-30, -90); c.line_to(0, -130); c.line_to(30, -90); c.line_to(60, -150); c.close_path(); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 5); c.stroke()
    c.restore()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .14)
    t1 = wfind(0, 'crater')
    overlay(fr, L_(lambda c: (tent(c, 260, 1330, .9), phone(c, 650, 1020, .75 * back(clamp((T + .4) / .4)), T, clamp((T - t1) / .6) if T > t1 else 0))))
    if T > t1: burst(fr, 'WAIT...', 230, 860, T - t1, r=110, col=YEL, size=44, rot=-10)
    tape(fr, 'CAMPING TRIP', CX, 470, T + .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'FOUND A CRATER', 600, T + .3, size=110, fill=YEL, rot=-2)

def s_real(fr, T):
    fr[:] = essay_slide(T, [('THAT REALLY HAPPENED.', 'grey'), ('IN QUEBEC.', 'hl')], [S[1], wfind(1, 'quebec')], size=104)
    chip(fr, 'COTE-NORD, CANADA', CX, 1150, T - wfind(1, 'quebec'), YEL, 40, -2)

def s_scan(fr, T):
    lt = T - S[2]; bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'SATELLITE MAPS', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    t1 = wfind(2, 'circle')
    def dr(c):
        satmap(c, CX, 1020, 860, 640, T, clamp((T - t1) / .6) if T > t1 else 0, 1.0 + .3 * clamp((T - t1) / 2) if T > t1 else 1.0)
        mx, my = lerp(250, CX + 40, eout(clamp(lt / 3))), lerp(800, 1030, eout(clamp(lt / 3)))
        c.arc(mx, my, 90, 0, 6.29); c.set_source_rgba(1, 1, 1, .25); c.fill_preserve(); ink(c, 12); c.stroke()
        c.move_to(mx + 64, my + 64); c.line_to(mx + 160, my + 160); c.set_line_width(26); c.set_line_cap(1); ink(c, 26); c.stroke()
    overlay(fr, L_(dr))
    chip(fr, 'AMATEUR ASTRONOMER', CX, 770, lt - .3, YEL, 36, -2)
    if T > t1: title(fr, 'A STRANGE CIRCLE', 600, T - t1, size=104, fill=YEL)

def s_volc(fr, T):
    fr[:] = essay_slide(T, [('EXPERTS SAID:', 'grey'), ('OLD VOLCANO.', 'hl')], [S[3], wfind(3, 'volcano')], size=124)
    overlay(fr, L_(lambda c: volcano(c, CX, 1200, .9 * back(clamp((T - S[3] - .1) / .35)))))

def s_check(fr, T):
    lt = T - S[4]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tape(fr, 'GO CHECK', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (person(c, 340, 1000, 1.0 * back(clamp(lt / .3)), T, 1.0, False, RED), person(c, 700, 1030, .9 * back(clamp((lt - .15) / .3)), T, 1.0, True, BLUE))))
    title(fr, 'GEOLOGISTS', 600, lt, size=120, fill=YEL)

def s_cones(fr, T):
    lt = T - S[5]; bg(fr, T, 'F7E3C8'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THE PROOF', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: cone(c, CX, 1040, 1.3 * back(clamp(lt / .35)))))
    title(fr, 'SHATTER CONES', 600, lt, size=110, fill=YEL)
    if T > wfind(5, 'impact'): burst(fr, 'IMPACT!', 830, 1250, T - wfind(5, 'impact'), r=120, col=YEL, size=44, rot=8)
    if T > wfind(5, 'cracks'): chip(fr, 'CONE-SHAPED CRACKS', 330, 1290, T - wfind(5, 'cracks'), 'FFFFFF', 34, -3)

def s_size(fr, T):
    lt = T - S[6]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'HOW BIG?', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        r = 380 * back(clamp(lt / .4))
        if r > 1:
            c.arc(CX, 1010, r, 0, 6.29); c.set_source_rgba(*hx('6B8F5A')); c.fill_preserve(); ink(c, 9); c.stroke()
            c.arc(CX, 1010, r * .65, 0, 6.29); c.set_source_rgba(*hx('3F7FC4', .8)); c.fill()
            c.arc(CX, 1010, r * .2, 0, 6.29); c.set_source_rgba(*hx('8A8A7A')); c.fill_preserve(); ink(c, 5); c.stroke()
        if T > wfind(6, 'manhattan'):
            u = eout(clamp((T - wfind(6, 'manhattan')) / .6)); L = 2 * 380 * 13.4 / 16
            c.rectangle(CX - L / 2, 1010 - 30, L * u, 60); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 6); c.stroke()
    overlay(fr, L_(dr))
    if T > wfind(6, 'sixteen'): title(fr, '~16 MILES WIDE', 600, T - wfind(6, 'sixteen'), size=110, fill=YEL)
    if T > wfind(6, 'manhattan'): chip(fr, 'MANHATTAN (~13 MI)', CX, 1080, T - wfind(6, 'manhattan'), 'FFFFFF', 32, 0)

def s_age(fr, T):
    lt = T - S[7]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'HOW OLD?', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def dr(c):
        x0, x1, y = 120, 960, 1050
        c.move_to(x0, y); c.line_to(x1, y); ink(c, 10); c.stroke()
        for v, lab, col in ((390, 'CRATER', RED), (230, 'FIRST DINOS', '3FAE5A'), (0, 'NOW', '1C1614')):
            x = x1 - (x1 - x0) * v / 400
            c.arc(x, y, 26, 0, 6.29); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 5); c.stroke()
    overlay(fr, L_(dr))
    chip(fr, '390 MILLION YRS AGO', 220, 1170, lt - .2, YEL, 30, -3)
    if T > wfind(7, 'dinosaurs'): chip(fr, 'DINOS: ~230M', 560, 900, T - wfind(7, 'dinosaurs'), 'FFFFFF', 32, 3); title(fr, 'OLDER THAN DINOS', 600, T - wfind(7, 'dinosaurs'), size=100, fill=YEL)
    if T > wfind(7, 'three'): title(fr, '390 MILLION YEARS', 600, T - wfind(7, 'three'), size=96, fill=YEL) if T < wfind(7, 'dinosaurs') else None

def s_stamp(fr, T):
    fr[:] = essay_slide(T, [('NOT OFFICIAL YET.', 'grey'), ('"ESSENTIALLY CONFIRMED."', 'hl')], [S[8], wfind(8, 'essentially')], size=92)
    lt = T - S[8]
    chip(fr, 'AWAITING OFFICIAL REVIEW', CX, 1150, lt - .3, YEL, 36, -3)

def s_end(fr, T):
    lt = T - S[9]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .14)
    tape(fr, 'NEXT TRIP', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (tent(c, 260, 1330, .9), phone(c, 650, 1020, .75, T, 1.0))))
    if T > wfind(9, 'look'): title(fr, 'LOOK CLOSER', 600, T - wfind(9, 'look'), size=120, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_real), (S[3], s_scan), (S[4], s_volc), (S[5], s_check), (S[6], s_cones), (S[7], s_size), (S[8], s_age), (S[9], s_stamp), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'crater'), wfind(5, 'impact'), wfind(6, 'sixteen')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Source: NASA Earth Observatory / Western Univ.')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
