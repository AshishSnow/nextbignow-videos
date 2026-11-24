import sys, os, json, math
sys.path.insert(0, '/home/claude/bees')
from kit import *
D = '/home/claude/bees'
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




def bee(c, x, y, s, T, kind='honey', flip=False, angry=False):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    wf = .3 * math.sin(T * 40)
    for side in (-1, 1):
        c.save(); c.translate(-10 * side, -45); c.rotate(side * (.5 + wf)); c.scale(1, 1.6); c.arc(0, -20, 28, 0, 6.29); c.restore()
        c.set_source_rgba(.85, .95, 1, .8); c.fill_preserve(); ink(c, 4); c.stroke()
    if kind == 'bumble':
        c.save(); c.scale(1.15, 1); c.arc(0, 0, 70, 0, 6.29); c.restore(); c.set_source_rgba(*hx('1C1614')); c.fill_preserve(); ink(c, 6); c.stroke()
        c.save(); c.scale(1.15, 1); c.arc(0, 0, 70, 0, 6.29); c.restore(); c.clip()
        c.rectangle(-30, -80, 30, 160); c.set_source_rgba(*hx(YEL)); c.fill()
        c.rectangle(40, -80, 50, 160); c.set_source_rgba(*hx('F7F1E3')); c.fill(); c.reset_clip()
    elif kind == 'hover':
        c.save(); c.scale(1.9, .75); c.arc(0, 0, 42, 0, 6.29); c.restore(); c.set_source_rgba(*hx('E8A33A')); c.fill_preserve(); ink(c, 5); c.stroke()
        for k in range(3): c.rectangle(-40 + k * 30, -28, 12, 56); c.set_source_rgba(*hx('1C1614')); c.fill()
    else:
        c.save(); c.scale(1.7, 1); c.arc(0, 0, 45, 0, 6.29); c.restore(); c.set_source_rgba(*hx('F2B233')); c.fill_preserve(); ink(c, 6); c.stroke()
        c.save(); c.scale(1.7, 1); c.arc(0, 0, 45, 0, 6.29); c.restore(); c.clip()
        for k in range(3): c.rectangle(-20 + k * 32, -50, 14, 100); c.set_source_rgba(*hx('3A2A20')); c.fill()
        c.reset_clip()
        c.move_to(76, 0); c.line_to(100, -6); c.line_to(76, 10); c.set_source_rgba(*hx('1C1614')); c.fill()
    hx0 = -90 if kind != 'hover' else -95
    c.arc(hx0, -5, 32, 0, 6.29); c.set_source_rgba(*hx('3A2A20')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.arc(hx0 - 10, -12, 9, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill()
    c.arc(hx0 - 12, -12, 4, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    if angry: c.move_to(hx0 - 24, -28); c.line_to(hx0 + 2, -20); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(5); c.stroke()
    if kind != 'hover':
        c.move_to(hx0 - 10, -30); c.curve_to(hx0 - 20, -60, hx0 - 40, -70, hx0 - 50, -62); ink(c, 4); c.stroke()
    c.restore()

def flower(c, x, y, s, col='F7D1DE', center=YEL):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, 40); c.curve_to(10, 140, -10, 220, 0, 320); c.set_source_rgba(*hx('3FAE5A')); c.set_line_width(14); c.stroke()
    for k in range(5):
        a = k * 1.2566; c.save(); c.rotate(a); c.translate(0, -70); c.scale(.8, 1.2); c.arc(0, 0, 50, 0, 6.29); c.restore()
        c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(0, 0, 40, 0, 6.29); c.set_source_rgba(*hx(center)); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def hive(c, x, y, s):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    for k in range(4):
        w = 260 - abs(k - 1.5) * 50
        c.save(); c.translate(0, -k * 80); c.scale(w / 100, 1); c.arc(0, 0, 100, math.pi, 0); c.restore()
        c.save(); c.translate(0, -k * 80 + 40); c.scale(w / 100, .4); c.arc(0, 0, 100, 0, 6.29); c.restore()
        c.set_source_rgba(*hx('E8B04A')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(0, -60, 30, 0, 6.29); c.set_source_rgba(*hx('3A2A20')); c.fill()
    c.restore()

def thermo(c, x, y, s, lvl):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-30, -300, 60, 300); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(0, 30, 60, 0, 6.29); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 7); c.stroke()
    h = 280 * lvl; c.rectangle(-16, -h, 32, h + 10); c.set_source_rgba(*hx(RED)); c.fill()
    c.restore()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .14)
    t1 = wfind(0, 'bully'); push = eout(clamp((T - t1) / .5)) if T > t1 else 0
    def dr(c):
        flower(c, CX, 1060, 1.3)
        bee(c, CX - 80 + 30 * math.sin(T * 3), 930, 1.0, T, 'honey', False, T > t1)
        bee(c, 780 + 200 * push, 1120 + 150 * push, .8, T, 'bumble', True)
    overlay(fr, L_(dr))
    if T > t1: burst(fr, 'SHOVE!', 860, 870, T - t1, r=110, col=YEL, size=46, rot=10)
    tape(fr, 'THE HONEYBEE', CX, 470, T + .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'FLOWER BULLY?', 600, T + .3, size=120, fill=YEL, rot=-2)

def s_other(fr, T):
    fr[:] = essay_slide(T, [('NOT TO YOU.', 'grey'), ('TO OTHER BEES.', 'hl')], [S[1], wfind(1, 'other')], size=124)
    lt = T - S[1]
    overlay(fr, L_(lambda c: (bee(c, 330, 1130, .8 * back(clamp(lt / .3)), T, 'bumble'), bee(c, 640, 1160, .7 * back(clamp((lt - .1) / .3)), T, 'hover'), bee(c, 870, 1100, .6 * back(clamp((lt - .2) / .3)), T, 'bumble', True))))

def s_watch(fr, T):
    lt = T - S[2]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'CAMBRIDGE, ENGLAND', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    def dr(c):
        hive(c, 280, 1250, 1.1 * back(clamp(lt / .35)))
        flower(c, 650, 980, .8, 'F7D1DE'); flower(c, 880, 1060, .7, 'D7E9A8', 'A3C24A')
        for k in range(3): bee(c, 450 + 150 * math.sin(T * 1.5 + k * 2), 840 + 60 * math.cos(T * 2 + k), .45, T, 'honey', k % 2 == 0)
    overlay(fr, L_(dr))
    if T > wfind(2, 'ninety'): title(fr, '93 HOURS OF WATCHING', 600, T - wfind(2, 'ninety'), size=92, fill=YEL)
    if T > wfind(2, 'flowers'): chip(fr, 'BRAMBLE + IVY', 760, 1350, T - wfind(2, 'flowers'), CYAN, 36, 3)

def s_fight(fr, T):
    lt = T - S[3]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'FIGHT CLUB', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    t1 = wfind(3, 'shoved'); push = eout(clamp((T - t1) / .6)) if T > t1 else 0
    def dr(c):
        flower(c, CX, 1080, 1.1)
        bee(c, 380 + 120 * push, 900, .9, T, 'honey', False, True)
        bee(c, 720 + 250 * push, 960 - 200 * push, .75, T, 'bumble', True)
    overlay(fr, L_(dr))
    if T > wfind(3, 'most'): title(fr, 'THEY START IT', 600, T - wfind(3, 'most'), size=110, fill=YEL)
    if T > t1: burst(fr, 'CHASED!', 800, 760, T - t1, r=110, col=YEL, size=40, rot=8)

def s_back(fr, T):
    lt = T - S[4]; bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'BACKING OFF', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def dr(c):
        flower(c, 330, 1060, 1.0); bee(c, 330, 930, .7, T, 'honey')
        bee(c, 760 + 20 * math.sin(T * 3), 900, .6, T, 'bumble', True); bee(c, 800, 1170 + 20 * math.cos(T * 3), .6, T, 'hover', True)
    overlay(fr, L_(dr))
    if T > wfind(4, 'third'): title(fr, '~1 IN 3 TIMES', 600, T - wfind(4, 'third'), size=110, fill=YEL); chip(fr, '28-36% OF ENCOUNTERS', 700, 1340, T - wfind(4, 'third'), YEL, 34, 3)

def s_drop(fr, T):
    lt = T - S[5]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'BUMBLEBEES DROP', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    u = eout(clamp((T - wfind(5, 'bumblebees')) / 1.0)) if T > wfind(5, 'bumblebees') else 0
    def dr(c):
        for k, (x, h, col, lab) in enumerate(((300, 200 + 200 * eout(clamp(lt / 1.2)), 'F2B233', 'x2'), (720, 400 - 56 * u, '1C1614', ''))):
            c.rectangle(x - 110, 1250 - h, 220, h); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
        bee(c, 300, 1250 - (200 + 200 * eout(clamp(lt / 1.2))) - 60, .6, T, 'honey'); bee(c, 720, 1250 - (400 - 56 * u) - 70, .6, T, 'bumble')
    overlay(fr, L_(dr))
    chip(fr, 'HONEYBEES x2', 300, 1300, lt - .3, YEL, 34, -3)
    if u > 0: chip(fr, 'BUMBLEBEES -14%', 720, 1300, T - wfind(5, 'bumblebees'), 'FFFFFF', 34, 3)

def s_heat(fr, T):
    fr[:] = essay_slide(T, [('HEAT', 'hl'), ('MAKES IT WORSE.', 'main')], [S[6], wfind(6, 'worse')], size=128)
    lt = T - S[6]
    overlay(fr, L_(lambda c: thermo(c, CX, 1250, .9, .3 + .6 * clamp(lt / 3))))
    if T > wfind(6, 'fights'): chip(fr, 'MORE FIGHTS', 780, 1100, T - wfind(6, 'fights'), YEL, 40, 4)

def s_love(fr, T):
    lt = T - S[7]; bg(fr, T, 'F7D9C4'); rays(fr, T, 'FFFFFF', .14)
    tape(fr, 'WHO LIKES IT HOT?', CX, 470, lt, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        c.arc(CX, 700, 90, 0, 6.29); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 6); c.stroke()
        bee(c, 320, 1060, .85 * back(clamp(lt / .3)), T, 'honey')
        if T > wfind(7, 'bumblebees'): bee(c, 760, 1100 + 10 * math.sin(T * 2), .8, T * .3, 'bumble', True)
    overlay(fr, L_(dr))
    chip(fr, 'HONEYBEE: LOVES IT', 320, 1290, lt - .3, YEL, 34, -3)
    if T > wfind(7, "don't"): chip(fr, "BUMBLEBEE: NOPE", 760, 1290, T - wfind(7, "don't"), 'FFFFFF', 34, 3)

def s_keepers(fr, T):
    lt = T - S[8]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .12)
    tape(fr, 'MORE HIVES', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    u = eout(clamp((lt - .3) / 1.5))
    def dr(c):
        c.rectangle(220, 1250 - 220, 240, 220); c.set_source_rgba(*hx('E8B04A')); c.fill_preserve(); ink(c, 7); c.stroke()
        h = 220 + 330 * u; c.rectangle(620, 1250 - h, 240, h); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 7); c.stroke()
    overlay(fr, L_(dr))
    chip(fr, '2010: 19,000', 340, 1300, lt - .2, 'FFFFFF', 32, -3); chip(fr, 'NOW: 47,000', 740, 1300, lt - .6, YEL, 32, 3)
    if T > wfind(8, 'doubled'): title(fr, 'UK BEEKEEPERS x2', 600, T - wfind(8, 'doubled'), size=100, fill=YEL)

def s_end(fr, T):
    fr[:] = essay_slide(T, [('SAVE THE BEES?', 'grey'), ('HELP THE WILD ONES TOO.', 'hl')], [S[9], wfind(9, 'wild') - .6], size=96)
    lt = T - S[9]
    chip(fr, 'SMALL STUDY. KEEP BEEKEEPING.', CX, 860, lt - .3, YEL, 30, -2)
    overlay(fr, L_(lambda c: (flower(c, 330, 1130, .7), bee(c, 330, 1030, .5, T, 'bumble'), flower(c, 760, 1150, .7, 'D7E9A8', 'A3C24A'), bee(c, 760, 1050, .5, T, 'hover', True))))

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_other), (S[3], s_watch), (S[4], s_fight), (S[5], s_back), (S[6], s_drop), (S[7], s_heat), (S[8], s_love), (S[9], s_keepers), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'bully'), wfind(3, 'shoved'), wfind(6, 'worse')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Study: Buckle et al., Ecological Entomology (2026)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
