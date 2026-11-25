import sys, os, json, math
sys.path.insert(0, '/home/claude/bike')
from kit import *
D = '/home/claude/bike'
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









def bike(c, x, y, s, T, pedal=1.0, rider=True, col=BLUE, tired=False):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-220, 220, 440, 40); c.set_source_rgba(*hx('3A3F55')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.move_to(-120, 220); c.line_to(-40, -20); c.line_to(120, -60); c.line_to(140, 220); c.set_source_rgba(*hx('E5E7EB')); c.set_line_width(26); c.set_line_cap(1); c.set_line_join(1); c.stroke()
    c.move_to(-120, 220); c.line_to(-40, -20); c.line_to(120, -60); c.line_to(140, 220); ink(c, 6); c.stroke()
    c.arc(-20, 140, 70, 0, 6.29); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 6); c.stroke()
    a = T * 8 * pedal
    for k in (0, math.pi):
        px, py = -20 + 60 * math.cos(a + k), 140 + 60 * math.sin(a + k)
        c.move_to(-20, 140); c.line_to(px, py); ink(c, 8); c.stroke()
        c.rectangle(px - 25, py - 6, 50, 12); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-90, -40, 110, 24); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.move_to(120, -60); c.line_to(170, -130); ink(c, 10); c.stroke()
    if rider:
        c.save(); c.translate(-30, -150)
        c.move_to(-50, 110); c.curve_to(-60, 0, -20, -60, 40, -60); c.curve_to(90, -50, 110, 30, 100, 110); c.close_path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()
        c.move_to(60, -30); c.line_to(190, 30); c.set_source_rgba(*hx('F2C9A0')); c.set_line_width(20); c.stroke()
        for k in (0, math.pi):
            px, py = 10 + 60 * math.cos(a + k), 290 + 60 * math.sin(a + k)
            c.move_to(0, 110); c.line_to(px, py); c.set_source_rgba(*hx('2B2B33')); c.set_line_width(26); c.stroke()
        c.arc(30, -120, 58, 0, 6.29); c.set_source_rgba(*hx('F2C9A0')); c.fill_preserve(); ink(c, 6); c.stroke()
        c.arc(30, -150, 58, 3.3, 6.1); c.set_source_rgba(*hx('3A2A20')); c.fill()
        for ex in (10, 50):
            if tired: c.move_to(ex - 10, -120); c.line_to(ex + 10, -120); ink(c, 5); c.stroke(); c.arc(ex, -105, 9, 0, 3.14); c.set_source_rgba(*hx('9B7EDE', .7)); c.set_line_width(4); c.stroke()
            else: c.arc(ex, -122, 7, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.restore()
    c.restore()

def bed(c, x, y, s, T, sleeper=True):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-260, 0, 520, 90); c.set_source_rgba(*hx('8B5A3C')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.rectangle(-260, -50, 520, 60); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 6); c.stroke()
    c.rectangle(-260, -160, 40, 250); c.set_source_rgba(*hx('8B5A3C')); c.fill_preserve(); ink(c, 6); c.stroke()
    if sleeper:
        c.arc(-150, -80, 50, 0, 6.29); c.set_source_rgba(*hx('F2C9A0')); c.fill_preserve(); ink(c, 6); c.stroke()
        c.move_to(-110, -70); c.curve_to(-40, -110, 150, -100, 240, -60); c.line_to(240, -20); c.line_to(-110, -20); c.close_path(); c.set_source_rgba(*hx(CYAN)); c.fill_preserve(); ink(c, 6); c.stroke()
        c.select_font_face('Luckiest Guy'); c.set_font_size(60)
        for k in range(3):
            u = (T * .6 + k / 3) % 1; c.move_to(-120 + 60 * u + k * 10, -160 - 160 * u); c.set_source_rgba(*hx('2D6CDF', 1 - u)); c.show_text('Z')
    c.restore()

def clock(c, x, y, r, T, hrs):
    c.arc(x + 10, y + 12, r, 0, 6.29); c.set_source_rgba(0, 0, 0, .25); c.fill()
    c.arc(x, y, r, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 9); c.stroke()
    a = hrs / 12 * 6.283 - math.pi / 2; c.move_to(x, y); c.line_to(x + r * .5 * math.cos(a), y + r * .5 * math.sin(a)); ink(c, 12); c.stroke()
    a2 = hrs * 6.283 - math.pi / 2; c.move_to(x, y); c.line_to(x + r * .8 * math.cos(a2), y + r * .8 * math.sin(a2)); c.set_source_rgba(*hx(RED)); c.set_line_width(8); c.stroke()

def photos(c, T, n):
    cols = [RED, CYAN, YEL, '3FAE5A', '9B7EDE', 'F28C28']
    for k in range(n):
        x, y = 170 + (k % 4) * 240, 900 + (k // 4) * 260
        c.save(); c.translate(x, y); c.rotate(math.radians(-6 + (k * 5) % 12))
        c.rectangle(-95, -110, 190, 220); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 6); c.stroke()
        c.rectangle(-80, -95, 160, 140); c.set_source_rgba(*hx(cols[k % 6])); c.fill()
        c.arc(-30, -40, 22, 0, 6.29); c.set_source_rgba(1, 1, 1, .7); c.fill()
        c.restore()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .16)
    overlay(fr, L_(lambda c: (bed(c, 280, 1250, .75 * back(clamp((T + .5) / .5)), T), bike(c, 780, 1100, .7 * back(clamp((T + .3) / .5)), T, 1.0, True, BLUE, True))))
    if T > wfind(0, 'nap'): chip(fr, 'NAP?', 280, 960, T - wfind(0, 'nap'), 'FFFFFF', 54, -4)
    if T > wfind(0, 'bike'): chip(fr, 'BIKE?', 780, 760, T - wfind(0, 'bike'), YEL, 54, 4)
    tape(fr, 'NO SLEEP LAST NIGHT?', CX, 470, T + .4, col=RED, size=56, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, '20 MINUTES VS', 600, T + .4, size=116, fill='FFFFFF', rot=-2); title(fr, 'A 90-MIN NAP', 730, T + .3, size=130, fill=YEL, rot=-2)

def s_pick(fr, T):
    fr[:] = essay_slide(T, [('MOST PICK THE NAP.', 'grey'), ('SCIENCE SAYS: PEDAL.', 'hl')], [S[1], wfind(1, 'study')], size=100)
    overlay(fr, L_(lambda c: bike(c, CX, 1150, .6, T, 1.0, True, RED)))

def s_awake(fr, T):
    lt = T - S[2]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THE EXPERIMENT', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: clock(c, CX, 1060, 260, T, 30 * eout(clamp(lt / 3)))))
    if T > wfind(2, 'fifty'): chip(fr, '54 YOUNG ADULTS', 300, 1380 - 40, T - wfind(2, 'fifty'), YEL, 38, -3)
    if T > wfind(2, 'thirty'): title(fr, '30 HOURS AWAKE', 620, T - wfind(2, 'thirty'), size=110, fill=YEL)

def s_groups(fr, T):
    lt = T - S[3]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, '3 GROUPS', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    t1, t2, t3 = wfind(3, 'napped'), wfind(3, 'rode'), wfind(3, 'sat')
    def dr(c):
        if T > t1 - .2: bed(c, 270, 880, .55 * back(clamp((T - t1 + .2) / .3)), T)
        if T > t2 - .2: bike(c, 560, 1140, .55 * back(clamp((T - t2 + .2) / .3)), T, 1.0, True, BLUE)
        if T > t3 - .2: bike(c, 850, 860, .5 * back(clamp((T - t3 + .2) / .3)), T, 0.0, True, '888888', True)
    overlay(fr, L_(dr))
    if T > t1: chip(fr, 'NAP 90 MIN', 230, 1020, T - t1, 'FFFFFF', 32, -3)
    if T > t2: chip(fr, 'BIKE 20 MIN', 560, 1360 - 40, T - t2, YEL, 32, 2)
    if T > t3: chip(fr, 'JUST SIT', 860, 1110, T - t3, 'FFFFFF', 32, 3)

def s_photos(fr, T):
    lt = T - S[4]; bg(fr, T, 'F7E3C8'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'STUDY THESE', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: photos(c, T, int(clamp(lt / 1.8) * 8))))

def s_test(fr, T):
    lt = T - S[5]; bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, '3 DAYS LATER', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'MEMORY TEST', 620, lt, size=130, fill=YEL)
    overlay(fr, L_(lambda c: photos(c, T, 4)))

def s_result(fr, T):
    lt = T - S[6]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THE RESULT', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    u = eout(clamp(lt / 1.2))
    def dr(c):
        for k, (h, col) in enumerate(((380, CYAN), (370, YEL), (200, 'AAAAAA'))):
            x = 180 + k * 290; hh = h * u
            c.rectangle(x + 10, 1300 - hh + 12, 200, hh); c.set_source_rgba(0, 0, 0, .25); c.fill()
            c.rectangle(x, 1300 - hh, 200, hh); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    overlay(fr, L_(dr))
    for k, (lab, col) in enumerate((('NAP', 'FFFFFF'), ('BIKE', YEL), ('SIT', 'FFFFFF'))): chip(fr, lab, 280 + k * 290, 1350, lt - .2 - k * .1, col, 38, 0)
    chip(fr, 'ILLUSTRATIVE', 900, 800, lt - .5, 'FFFFFF', 24, 4)
    if T > wfind(6, 'way'): title(fr, 'REMEMBERED MORE', 640, T - wfind(6, 'way'), size=104, fill=YEL)

def s_same(fr, T):
    lt = T - S[7]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .16)
    tape(fr, 'SO...', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (bike(c, 330, 1100, .7, T, 1.4, True, BLUE), bed(c, 790, 1200, .5, T))))
    chip(fr, '=', CX, 1050, lt - .2, YEL, 90, 0)
    if T > wfind(7, 'twenty'): title(fr, '20 MIN = BIG HELP', 640, T - wfind(7, 'twenty'), size=104, fill=YEL)

def s_caveat(fr, T):
    fr[:] = essay_slide(T, [('ONE SMALL STUDY.', 'grey'), ('SLEEP STILL WINS.', 'hl')], [S[8], wfind(8, 'sleep')], size=110)
    overlay(fr, L_(lambda c: bed(c, CX, 1250, .7, T)))

def s_end(fr, T):
    lt = T - S[9]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .16)
    tape(fr, 'WRECKED + SHORT ON TIME?', CX, 470, lt, col='FFFFFF', size=52, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: bike(c, CX, 1100, .85, T, 1.6, True, RED)))
    if T > wfind(9, 'hop'): title(fr, 'HOP ON THE BIKE', 640, T - wfind(9, 'hop'), size=110, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_pick), (S[3], s_awake), (S[4], s_groups), (S[5], s_photos), (S[6], s_test), (S[7], s_result), (S[8], s_same), (S[9], s_caveat), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(1, 'pedal'), wfind(6, 'way'), wfind(9, 'hop')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Study: McGill University, PNAS (2026)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
