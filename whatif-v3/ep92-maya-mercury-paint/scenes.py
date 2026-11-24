import sys, os, json, math
sys.path.insert(0, '/home/claude/maya')
from kit import *
D = '/home/claude/maya'
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







CIN = 'C8321E'

def pyramid(c, x, y, s, paint=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for k in range(5):
        w = 420 - k * 70; h = 70
        c.rectangle(-w / 2 + 12, -k * h - h + 14, w, h); c.set_source_rgba(0, 0, 0, .2); c.fill()
        c.rectangle(-w / 2, -k * h - h, w, h)
        col = hx(CIN) if (k + 1) / 5 <= paint + .001 else hx('D9C9A3')
        c.set_source_rgba(*col); c.fill_preserve(); ink(c, 7); c.stroke()
    c.rectangle(-60, -5 * 70 - 90, 120, 90); c.set_source_rgba(*(hx(CIN) if paint > .99 else hx('D9C9A3'))); c.fill_preserve(); ink(c, 7); c.stroke()
    c.rectangle(-22, -5 * 70 - 60, 44, 60); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-40, -350, 80, 350); c.set_source_rgba(1, 1, 1, .25); c.fill()
    c.restore()

def lake(c, x, y, w, h, T, tox=0.0):
    c.save(); c.translate(x, y); c.scale(1, h / w)
    c.arc(0, 0, w, 0, 6.29); c.restore()
    a = hx('5FB0E0'); b = hx('6E7B3A'); m = [a[i] * (1 - tox) + b[i] * tox for i in range(3)]
    c.set_source_rgba(*m); c.fill_preserve(); ink(c, 7); c.stroke()
    for k in range(3):
        xx = x - w * .5 + k * w * .45 + 20 * math.sin(T * 2 + k)
        c.move_to(xx, y - 10 + k * 15); c.line_to(xx + 70, y - 10 + k * 15); c.set_source_rgba(1, 1, 1, .5 * (1 - tox)); c.set_line_width(6); c.stroke()

def fish(c, x, y, s, al=1.0, flip=False):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    c.save(); c.scale(1.6, 1); c.arc(0, 0, 40, 0, 6.29); c.restore(); c.set_source_rgba(*hx('F2A541', al)); c.fill_preserve(); ink(c, 5, al); c.stroke()
    c.move_to(60, 0); c.line_to(100, -30); c.line_to(100, 30); c.close_path(); c.set_source_rgba(*hx('F2A541', al)); c.fill_preserve(); ink(c, 5, al); c.stroke()
    c.arc(-35, -8, 6, 0, 6.29); c.set_source_rgba(*hx('1C1614', al)); c.fill()
    c.restore()

def crystal(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx, h, r in ((-60, 160, -.25), (0, 220, 0), (60, 150, .25)):
        c.save(); c.translate(dx, 60); c.rotate(r)
        c.move_to(-30, 0); c.line_to(-30, -h + 40); c.line_to(0, -h); c.line_to(30, -h + 40); c.line_to(30, 0); c.close_path()
        c.set_source_rgba(*hx(CIN)); c.fill_preserve(); ink(c, 7); c.stroke()
        c.move_to(-10, -20); c.line_to(-10, -h + 50); c.set_source_rgba(1, 1, 1, .5); c.set_line_width(6); c.stroke()
        c.restore()
    c.restore()

def core(c, x, y, T, prog, spikes):
    c.rectangle(x - 70 + 10, y - 400 + 12, 140, 800); c.set_source_rgba(0, 0, 0, .25); c.fill()
    for k in range(20):
        yy = y + 400 - (k + 1) * 40
        sp = spikes(k)
        col = [hx('8B6A4A'), hx('6E5236')][k % 2]
        if sp > 0: col = [col[i] * (1 - sp) + hx(CIN)[i] * sp for i in range(3)]
        if (k + 1) / 20 <= prog + .001:
            c.rectangle(x - 70, yy, 140, 40); c.set_source_rgba(*col); c.fill()
    c.rectangle(x - 70, y - 400, 140, 800); c.set_source_rgba(1, 1, 1, .15); c.fill_preserve(); ink(c, 8); c.stroke()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tox = clamp((T - wfind(0, 'poisoning')) / 1.2) if T > wfind(0, 'poisoning') else 0
    def dr(c):
        lake(c, CX, 1260, 430, 110, T, tox)
        pyramid(c, CX, 1150, 1.15 * back(clamp((T + .4) / .4)), clamp(T / 1.6))
        if tox > 0:
            for k in range(4):
                u = (T * .8 + k / 4) % 1; c.arc(CX - 150 + k * 100, 1150 + 120 * u, 14, 0, 6.29); c.set_source_rgba(*hx(CIN, 1 - u)); c.fill()
    overlay(fr, L_(dr))
    if T > wfind(0, 'poisoning'): burst(fr, 'TOXIC!', 860, 1200, T - wfind(0, 'poisoning'), r=110, col=YEL, size=48, rot=10)
    tape(fr, 'ANCIENT MAYA', CX, 470, T + .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'THE POISON PAINT', 600, T + .3, size=110, fill=YEL, rot=-2)

def s_maya(fr, T):
    fr[:] = essay_slide(T, [('THAT MAY HAVE HAPPENED', 'grey'), ('TO THE ANCIENT MAYA.', 'hl')], [S[1], wfind(1, 'ancient')], size=96)
    lt = T - S[1]
    overlay(fr, L_(lambda c: pyramid(c, CX, 1330, .9 * back(clamp((lt - .1) / .35)), 1.0)))

def s_red(fr, T):
    lt = T - S[2]; bg(fr, T, 'F7E3C8'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'CINNABAR', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: crystal(c, CX, 1050, 1.5 * back(clamp(lt / .35)))))
    for k, (w, lab, x, y, col) in enumerate((('murals', 'MURALS', 250, 760, 'FFFFFF'), ('temples', 'TEMPLES', 830, 860, YEL), ('burials', 'BURIALS', 280, 1300, CYAN))):
        if T > wfind(2, w): chip(fr, lab, x, y, T - wfind(2, w), col, 48, -4 + 4 * k)
    if T > wfind(2, 'pigment'): title(fr, 'BRIGHT RED PIGMENT', 600, T - wfind(2, 'pigment'), size=96, fill=YEL)

def s_hg(fr, T):
    fr[:] = essay_slide(T, [('BUT CINNABAR', 'grey'), ('IS MERCURY.', 'hl')], [S[3], wfind(3, 'mercury')], size=128)
    lt = T - S[3]
    overlay(fr, L_(lambda c: crystal(c, CX, 1160, .9 * back(clamp(lt / .35)))))
    if T > wfind(3, 'mercury'): burst(fr, 'Hg', 800, 1060, T - wfind(3, 'mercury'), r=100, col=YEL, size=70, rot=8)

def s_dig(fr, T):
    lt = T - S[4]; bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'MUD CORES', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def dr(c):
        lake(c, 360, 1240, 260, 70, T, 0); pyramid(c, 360, 1150, .55)
        core(c, 820, 1020, T, eout(clamp(lt / 3)), lambda k: 0)
    overlay(fr, L_(dr))
    if T > wfind(4, 'two'): chip(fr, '2 MAYA CITIES', 360, 760, T - wfind(4, 'two'), YEL, 42, -3)
    if T > wfind(4, 'mexico'): chip(fr, 'YUCATAN, MEXICO', 360, 860, T - wfind(4, 'mexico'), 'FFFFFF', 36, 3)

def s_spike(fr, T):
    lt = T - S[5]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'LAYER BY LAYER', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    t1 = wfind(5, 'spiked')
    def sp(k): return clamp((T - t1) / 1) * (1.0 if 9 <= k <= 15 else (.4 if k == 4 else 0)) if T > t1 else 0
    def dr(c):
        core(c, 260, 1040, T, 1.0, sp)
        x0, y0, w, h = 420, 1360, 560, 620
        c.move_to(x0, y0 - h); c.line_to(x0, y0); c.line_to(x0 + w, y0); ink(c, 6); c.stroke()
        lim = y0 - h * .45
        c.move_to(x0, lim); c.line_to(x0 + w, lim); c.set_source_rgba(*hx(RED)); c.set_line_width(6); c.set_dash([18, 12]); c.stroke(); c.set_dash([])
        u = clamp((T - S[5]) / 3.5)
        pts = [0.03, .03, .04, .25, .05, .04, .9, .95, .85, 1.0, .8, .3, .06, .04]
        c.move_to(x0, y0 - h * pts[0])
        n = int(1 + u * (len(pts) - 1))
        for i in range(1, n + 1): c.line_to(x0 + w * i / (len(pts) - 1), y0 - h * pts[min(i, len(pts) - 1)])
        c.set_source_rgba(*hx(CIN)); c.set_line_width(12); c.set_line_join(1); c.stroke()
    overlay(fr, L_(dr))
    chip(fr, "TODAY'S DANGER LIMIT", 700, 1060, T - wfind(5, 'danger'), 'FFFFFF', 30, -2)
    if T > wfind(5, 'centuries'): title(fr, 'FOR CENTURIES', 600, T - wfind(5, 'centuries'), size=110, fill=YEL)

def s_crash(fr, T):
    lt = T - S[6]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'LAKE LIFE CRASHED', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    t1 = wfind(6, 'vanished'); al = 1 - clamp((T - t1) / .8) if T > t1 else 1
    def dr(c):
        lake(c, CX, 1050, 460, 300, T, 1 - al)
        for k in range(4): fish(c, 330 + k * 140, 980 + (k % 2) * 120 + 15 * math.sin(T * 3 + k), .9, al, k % 2 == 0)
    overlay(fr, L_(dr))
    for k, (w, lab, x, y) in enumerate((('algae', 'ALGAE', 250, 720), ('snails', 'SNAILS', CX, 690), ('insects', 'TINY INSECTS', 830, 760))):
        if T > wfind(6, w): chip(fr, lab, x, y, T - wfind(6, w), YEL, 38, -4 + 4 * k)
    if T > t1: xstamp(fr, CX, 1050, T - t1, 1.4); title(fr, 'GONE', 600, T - t1, size=130, fill=YEL)

def s_caveat(fr, T):
    fr[:] = essay_slide(T, [('NO TESTS ON PEOPLE.', 'grey'), ('NOT THE ONLY CAUSE.', 'hl')], [S[7], wfind(7, 'alone')], size=100)
    lt = T - S[7]
    overlay(fr, L_(lambda c: pyramid(c, CX, 1330, .8 * back(clamp((lt - .1) / .35)), 1.0)))
    chip(fr, 'NO HUMAN DATA', 300, 860, T - wfind(7, 'people'), YEL, 38, -4)
    if T > wfind(7, 'alone'): burst(fr, '1 OF MANY', 800, 1000, T - wfind(7, 'alone'), r=110, col=YEL, size=32, rot=8)

def s_drought(fr, T):
    lt = T - S[8]; bg(fr, T, 'F3D29A'); rays(fr, T, 'FFFFFF', .16)
    tape(fr, 'MANY STRESSES', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        c.arc(800, 820, 110, 0, 6.29); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 7); c.stroke()
        for k in range(6):
            x = 140 + k * 140; c.move_to(x, 1150); c.line_to(x + 40, 1230); c.line_to(x + 10, 1300); ink(c, 6); c.stroke()
        pyramid(c, 360, 1120, .6, 1.0)
    overlay(fr, L_(dr))
    if T > wfind(8, 'drought'): chip(fr, 'DROUGHT', 300, 760, T - wfind(8, 'drought'), YEL, 50, -4)
    if T > wfind(8, 'war'): chip(fr, 'WAR', 800, 1050, T - wfind(8, 'war'), 'FFFFFF', 54, 4)

def s_end(fr, T):
    lt = T - S[9]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tape(fr, 'ONE MORE STRESSOR', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: (lake(c, CX, 1260, 430, 110, T, .3), pyramid(c, CX, 1150, 1.1 * back(clamp(lt / .35)), 1.0))))
    if T > wfind(9, 'ask') - .2: title(fr, "WHAT'S IN THE PAINT?", 600, T - wfind(9, 'ask') + .2, size=96, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_maya), (S[3], s_red), (S[4], s_hg), (S[5], s_dig), (S[6], s_spike), (S[7], s_crash), (S[8], s_caveat), (S[9], s_drought), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'poisoning'), wfind(3, 'mercury'), wfind(6, 'vanished')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Study: Waters et al., Science Advances (2026)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
