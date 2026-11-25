import sys, os, json, math
sys.path.insert(0, '/home/claude/mushroom')
from kit import *
D = '/home/claude/mushroom'
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







def shroom(c, x, y, s, T, blue=0.0, wob=1.0):
    if s < .01: return
    c.save(); c.translate(x, y); c.rotate(.04 * wob * math.sin(T * 2)); c.scale(s, s)
    c.move_to(-60, 0); c.curve_to(-80, 120, -70, 220, -40, 260); c.line_to(40, 260); c.curve_to(70, 220, 80, 120, 60, 0); c.close_path()
    c.set_source_rgba(*hx('F2C94C')); c.fill_preserve(); ink(c, 8); c.stroke()
    if blue > 0:
        c.save(); c.move_to(-60, 0); c.curve_to(-80, 120, -70, 220, -40, 260); c.line_to(40, 260); c.curve_to(70, 220, 80, 120, 60, 0); c.close_path(); c.clip()
        c.arc(20, 150, 90 * blue, 0, 6.29); c.set_source_rgba(*hx('2D6CDF', .85)); c.fill(); c.restore()
    c.move_to(-230, 10); c.curve_to(-230, -190, 230, -190, 230, 10); c.curve_to(120, 40, -120, 40, -230, 10)
    c.set_source_rgba(*hx('A0522D')); c.fill_preserve(); ink(c, 9); c.stroke()
    c.move_to(-160, -80); c.curve_to(-120, -130, -60, -150, -10, -150); c.set_source_rgba(1, 1, 1, .45); c.set_line_width(14); c.set_line_cap(1); c.stroke()
    c.restore()

def tiny(c, x, y, s, T, col, k=0):
    person(c, x + 30 * math.sin(T * 1.5 + k), y, s, T + k * .3, 1.0, k % 2 == 0, col, k % 3 == 0)

def table(c, y=1180):
    c.rectangle(0, y, W, 420); c.set_source_rgba(*hx('B5733A')); c.fill()
    c.move_to(0, y); c.line_to(W, y); ink(c, 8); c.stroke()
    for k in range(4): c.move_to(0, y + 60 + k * 70); c.line_to(W, y + 60 + k * 70); c.set_source_rgba(*hx('8A5228', .5)); c.set_line_width(4); c.stroke()

def crowd(c, T, n, y0=1150, s=.22, spread=900):
    cols = [RED, BLUE, '3FAE5A', 'F2A541', '9B7EDE', CYAN]
    for k in range(n):
        x = 90 + (k * 137) % spread + ((T * 40 + k * 23) % 60)
        y = y0 + (k % 3) * 28
        tiny(c, x, y - 80 * s / .22, s * (.8 + .4 * ((k * 7) % 5) / 5), T, cols[k % 6], k)

def plate(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s * .35)
    c.arc(0, 0, 260, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(0, 0, 190, 0, 6.29); c.set_source_rgba(*hx('E6E9EE')); c.fill(); c.restore()

def flask(c, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-40, -200); c.line_to(-40, -60); c.line_to(-150, 140); c.line_to(150, 140); c.line_to(40, -60); c.line_to(40, -200); c.close_path()
    c.set_source_rgba(1, 1, 1, .85); c.fill_preserve(); ink(c, 8); c.stroke()
    c.move_to(-110, 70); c.line_to(110, 70); c.line_to(150, 140); c.line_to(-150, 140); c.close_path(); c.set_source_rgba(*hx('9B7EDE')); c.fill()
    for k in range(4):
        u = (T * .8 + k / 4) % 1; c.arc(-40 + k * 25, 100 - 220 * u, 10, 0, 6.29); c.set_source_rgba(*hx('9B7EDE', 1 - u)); c.fill()
    c.restore()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .16)
    n = 2 + int(clamp((T - .3) / 3) * 7)
    overlay(fr, L_(lambda c: (table(c), plate(c, CX, 1170, 1.0), shroom(c, CX, 960, .95 * back(clamp((T + .5) / .5)), T), crowd(c, T, n, 1230, .32))))
    tape(fr, 'UNDERCOOKED MUSHROOM', CX, 470, T + .4, col=RED, size=56, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'HUNDREDS OF', 600, T + .4, size=120, fill='FFFFFF', rot=-2); title(fr, 'TINY PEOPLE', 730, T + .3, size=140, fill=YEL, rot=-2)

def s_hundreds(fr, T):
    fr[:] = essay_slide(T, [('SOMETIMES', 'grey'), ('HUNDREDS.', 'hl')], [S[1], wfind(1, 'hundreds')], size=128)
    lt = T - S[1]
    overlay(fr, L_(lambda c: crowd(c, T, int(4 + clamp(lt / 2) * 12), 1260, .26)))
    if T > wfind(1, 'finger'): chip(fr, '~3 TO 30 CM TALL', CX, 1000, T - wfind(1, 'finger'), YEL, 38, -2)

def s_market(fr, T):
    lt = T - S[2]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'A REAL MUSHROOM', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def dr(c):
        c.rectangle(110, 1080, 860, 260); c.set_source_rgba(*hx('8B5A3C')); c.fill_preserve(); ink(c, 8); c.stroke()
        for k in range(5): shroom(c, 220 + k * 160, 1010, .4 * back(clamp((lt - k * .1) / .3)), T + k)
    overlay(fr, L_(dr))
    if T > wfind(2, 'china'): title(fr, 'YUNNAN, CHINA', 620, T - wfind(2, 'china'), size=110, fill=YEL)
    chip(fr, 'LANMAOA ASIATICA', CX, 1360, lt - .5, 'FFFFFF', 34, 2)

def s_sick(fr, T):
    lt = T - S[3]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'UNDERCOOKED = SICK', CX, 470, lt, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        person(c, 330, 1060, 1.1, T, 0, False, BLUE)
        for k in range(3):
            a = T * 4 + k * 2.1; c.arc(330 + 70 * math.cos(a), 870 + 20 * math.sin(a), 12, 0, 6.29); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 3); c.stroke()
        if T > wfind(3, 'same'): crowd(c, T, 5, 1150, .2, 380 + 0)
    overlay(fr, L_(dr))
    if T > wfind(3, 'same'):
        overlay(fr, L_(lambda c: [tiny(c, 650 + k * 80, 1120, .22, T, [RED, '3FAE5A', 'F2A541', '9B7EDE'][k], k) for k in range(4)]))
        chip(fr, 'SAME TINY FIGURES', 760, 820, T - wfind(3, 'same'), YEL, 36, 3)

def s_phil(fr, T):
    lt = T - S[4]; bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'ANOTHER COUNTRY', CX, 470, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    def dr(c):
        for (x, y, lab) in ((330, 950, 'CHINA'), (760, 1180, 'PHILIPPINES')):
            c.arc(x, y, 130, 0, 6.29); c.set_source_rgba(*hx('9CCB7A')); c.fill_preserve(); ink(c, 7); c.stroke()
        u = clamp(lt / 1.5); c.move_to(400, 1020); c.line_to(lerp(400, 690, u), lerp(1020, 1120, u)); c.set_source_rgba(*hx(RED)); c.set_line_width(10); c.set_dash([22, 14]); c.stroke(); c.set_dash([])
        tiny(c, 330, 940, .2, T, RED, 1); tiny(c, 760, 1170, .2, T, BLUE, 2)
    overlay(fr, L_(dr))
    chip(fr, 'CHINA', 330, 1130, lt - .2, 'FFFFFF', 36, -3); chip(fr, 'PHILIPPINES', 760, 1360, lt - .5, YEL, 36, 3)
    if T > wfind(4, 'same'): title(fr, 'SAME VISIONS', 620, T - wfind(4, 'same'), size=120, fill=YEL)

def s_dna(fr, T):
    lt = T - S[5]; bg(fr, T, 'F7E3C8'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'DNA CHECK', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (shroom(c, 280, 1000, .55, T), shroom(c, 800, 1000, .55, T + 1))))
    if T > wfind(5, 'same'): burst(fr, 'MATCH!', CX, 1240, T - wfind(5, 'same'), r=130, col=YEL, size=50, rot=8); title(fr, 'SAME SPECIES', 620, T - wfind(5, 'same'), size=120, fill=YEL)

def s_zero(fr, T):
    fr[:] = essay_slide(T, [('ZERO PSILOCYBIN.', 'grey'), ('NO KNOWN TRIP CHEMICAL.', 'hl')], [S[6], wfind(6, 'none')], size=92)
    overlay(fr, L_(lambda c: shroom(c, CX, 1160, .5, T)))

def s_new(fr, T):
    lt = T - S[7]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'MYSTERY INSIDE', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: flask(c, CX, 1060, 1.3 * back(clamp(lt / .35)), T)))
    burst(fr, '?', 830, 860, lt - .3, r=110, col=YEL, size=90, rot=8)
    if T > wfind(7, 'brand'): title(fr, 'A BRAND-NEW CHEMICAL?', 620, T - wfind(7, 'brand'), size=92, fill=YEL)

def s_brain(fr, T):
    lt = T - S[8]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'WHY IT MATTERS', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (person(c, 300, 1040, 1.0, T, 0, True, '9B7EDE'), [tiny(c, 640 + k * 90, 1150, .2, T, [RED, '3FAE5A', 'F2A541'][k], k) for k in range(3)])))
    if T > wfind(8, 'dementia'): chip(fr, 'SEEN IN DEMENTIA TOO', 700, 820, T - wfind(8, 'dementia'), YEL, 36, 3)

def s_end(fr, T):
    lt = T - S[9]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .16)
    overlay(fr, L_(lambda c: (table(c), plate(c, CX, 1170, 1.0), shroom(c, CX, 960, .95, T), crowd(c, T, 9, 1230, .32))))
    tape(fr, 'COOK IT PROPERLY', CX, 470, lt, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > wfind(9, 'until'): title(fr, 'OR THEY SHOW UP', 620, T - wfind(9, 'until'), size=110, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_hundreds), (S[3], s_market), (S[4], s_sick), (S[5], s_phil), (S[6], s_dna), (S[7], s_zero), (S[8], s_new), (S[9], s_brain), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(1, 'hundreds'), wfind(5, 'same'), wfind(6, 'zero')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Study: Domnauer & Dentinger, Mycologia (2026)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
