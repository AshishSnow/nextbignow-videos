import sys, os, json, math
sys.path.insert(0, '/home/claude/seapig')
from kit import *
D = '/home/claude/seapig'
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






def microbe(c, x, y, s, T, col='5BC0BE', chomp=1.0, ph=0.0, happy=False, ang=0.0):
    if s < .01: return
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    w = math.sin(T * 6 + ph)
    c.move_to(-60, 0)
    for k in range(9): c.line_to(-60 - 14 * k, 14 * math.sin(T * 14 + k + ph))
    ink(c, 6); c.stroke()
    c.save(); c.scale(1.25 + .06 * w, 1 - .06 * w); c.arc(0, 0, 60, 0, 6.29); c.restore()
    c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    for ex in (8, 38): c.arc(ex, -18, 12, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 3); c.stroke(); c.arc(ex + 3, -18, 5, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    o = .5 + .5 * math.sin(T * 16 + ph) if chomp > 0 else 0
    if happy: c.arc(28, 14, 20, .2, 2.9); ink(c, 6); c.stroke()
    else:
        c.move_to(10, 18); c.line_to(60, 8 - 18 * o); c.line_to(60, 22 + 18 * o); c.close_path(); c.set_source_rgba(*hx('7A1C2C')); c.fill_preserve(); ink(c, 5); c.stroke()
        for tx in (30, 45): c.move_to(tx, 13 - 8 * o); c.line_to(tx + 5, 20 - 8 * o); c.line_to(tx + 10, 13 - 8 * o); c.set_source_rgba(1, 1, 1, 1); c.fill()
    c.restore()

def phone(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    def rr(x0, y0, w, h, r):
        c.new_sub_path(); c.arc(x0 + w - r, y0 + r, r, -1.57, 0); c.arc(x0 + w - r, y0 + h - r, r, 0, 1.57); c.arc(x0 + r, y0 + h - r, r, 1.57, 3.14); c.arc(x0 + r, y0 + r, r, 3.14, 4.71); c.close_path()
    rr(-190 + 12, -330 + 16, 380, 660, 50); c.set_source_rgba(0, 0, 0, .25); c.fill()
    rr(-190, -330, 380, 660, 50); c.set_source_rgba(*hx('1C1614')); c.fill()
    rr(-165, -290, 330, 580, 24); c.set_source_rgba(1, 1, 1, 1); c.fill()
    c.restore()

PIGC = 'F4A7B9'; PIGD = 'D9708F'

def seapig(c, x, y, s, T, cut=0.0, glow=0.0, eyes=True):
    """translucent pink sea pig: plump body, top 'antennae' papillae, tube legs that waddle."""
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    for k in range(6):
        lx = -170 + k * 68; sw = 14 * math.sin(T * 7 + k * 1.3)
        c.move_to(lx, 60); c.curve_to(lx + sw, 110, lx + sw, 140, lx + sw * 1.4, 160); c.set_source_rgba(*hx(PIGD)); c.set_line_width(30); c.set_line_cap(1); c.stroke()
    for k, (ax, al) in enumerate(((-40, 140), (10, 170), (60, 150))):
        sw = 18 * math.sin(T * 3 + k)
        c.move_to(ax, -80); c.curve_to(ax + sw, -80 - al * .5, ax + sw * 2, -80 - al * .8, ax + sw * 2.5, -80 - al); c.set_source_rgba(*hx(PIGC)); c.set_line_width(26); c.stroke()
        c.arc(ax + sw * 2.5, -80 - al, 16, 0, 6.29); c.set_source_rgba(*hx(PIGD)); c.fill()
    c.save(); c.scale(1.6, 1); c.arc(0, 0, 130, 0, 6.29); c.restore(); c.set_source_rgba(*hx(PIGC, .92)); c.fill_preserve(); ink(c, 9); c.stroke()
    c.save(); c.scale(1.4, .7); c.arc(-10, -30, 90, 0, 6.29); c.restore(); c.set_source_rgba(1, 1, 1, .25); c.fill()
    if eyes:
        for ex in (150, 185): c.arc(ex, -20, 9, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.arc(175, 20, 14, 0, 3.14); ink(c, 5); c.stroke()
    if cut > 0:                                                   # cut-away window into the skin
        c.save(); c.scale(1.6, 1); c.arc(-20, 10, 80 * cut, 0, 6.29); c.restore(); c.set_source_rgba(*hx('FFF1C9')); c.fill_preserve(); ink(c, 6); c.stroke()
    if glow > 0:
        for r in (250, 300): c.save(); c.scale(1.4, 1); c.arc(0, 0, r, 0, 6.29); c.restore(); c.set_source_rgba(*hx(YEL, .12 * glow)); c.fill()
    c.restore()

def deep_bg(fr, T, top='0B2545', bot='04101F'):
    a = np.array(hx(top)[:3]) * 255; b = np.array(hx(bot)[:3]) * 255; yy = np.linspace(0, 1, H)[:, None, None]
    fr[:] = (a * (1 - yy) + b * yy).astype(np.uint8)
    def snow(c):
        for k in range(70):
            x = (k * 137.5) % W; y = ((k * 251) + T * (30 + k % 5 * 12)) % H; c.arc(x, y, 2 + k % 3, 0, 6.29); c.set_source_rgba(1, 1, 1, .35); c.fill()
    overlay(fr, cairo_layer(snow))

def depth_gauge(c, x, y, s, u):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-30, -300, 60, 600); c.set_source_rgba(1, 1, 1, .15); c.fill_preserve(); c.set_source_rgba(1, 1, 1, .8); c.set_line_width(4); c.stroke()
    c.rectangle(-30, -300, 60, 600 * u); c.set_source_rgba(*hx(CYAN, .85)); c.fill()
    for k in range(7): c.move_to(30, -300 + k * 100); c.line_to(55, -300 + k * 100); c.set_source_rgba(1, 1, 1, .8); c.stroke()
    c.restore()

def magnifier(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-.5)
    c.rectangle(-22, 150, 44, 200); c.set_source_rgba(*hx('6B4226')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(0, 0, 160, 0, 6.29); c.set_source_rgba(.85, .95, 1, .25); c.fill_preserve(); c.set_source_rgba(*hx('B8B8C4')); c.set_line_width(26); c.stroke()
    c.arc(0, 0, 160, 0, 6.29); ink(c, 6); c.stroke(); c.restore()

def protein(c, x0, y, length, T, col=RED):
    c.move_to(x0, y)
    for k in range(int(length / 12)):
        c.line_to(x0 + k * 12, y + 22 * math.sin(k * .7 + T * 4))
    c.set_source_rgba(*hx(col)); c.set_line_width(14); c.set_line_cap(1); c.stroke()

def L_(fn): return cairo_layer(fn)
def pop(T, t0, d=.35): return back(clamp((T - t0) / d))

def s_hook(fr, T):
    deep_bg(fr, T)
    overlay(fr, L_(lambda c: (seapig(c, CX - 60 + 40 * math.sin(T * .8), 1150, 1.05 * pop(T, -.4), T), depth_gauge(c, 890, 1080, .7, eout(clamp(T / 3))))))
    tape(fr, 'THIS IS A PIG?', CX, 440, T + .4, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'IT HAS A SECRET', 570, T + .4, size=112, fill='FFFFFF', rot=-2); title(fr, 'ROOMMATE', 705, T + .3, size=140, fill=YEL, rot=-2)
    t = wfind(0, 'six')
    if T > t: chip(fr, '~6 MILES DOWN', 760, 1340, T - t, CYAN, 34, 4)

def s_intro(fr, T):
    lt = T - S[1]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .14, CX, 1100)
    overlay(fr, L_(lambda c: seapig(c, CX + 60 * math.sin(lt * 2), 1120, 1.0 * pop(T, S[1]), T * 1.5)))
    tape(fr, 'MEET THE SEA PIG', CX, 450, lt, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    t = wfind(1, 'squishy')
    if T > t: chip(fr, 'A SEA CUCUMBER', 300, 820, T - t, 'FFFFFF', 36, -4)
    t = wfind(1, 'waddles')
    if T > t: burst(fr, 'WADDLE!', 830, 1380 - 60, T - t, r=120, col=YEL, size=44, rot=8)

def s_look(fr, T):
    lt = T - S[2]; deep_bg(fr, T, '13315C', '081A33')
    overlay(fr, L_(lambda c: (seapig(c, CX, 1150, 1.0, T, eout(clamp((lt - .6) / .5))), magnifier(c, CX - 30 + 60 * math.sin(lt), 1120, .9 * pop(T, S[2] + .2), T))))
    tape(fr, 'JAPAN', CX, 450, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    t = wfind(2, 'skin')
    if T > t: title(fr, 'UNDER THE SKIN', 620, T - t, size=118, fill=YEL)

def s_found(fr, T):
    lt = T - S[3]; bg(fr, T, 'FFF1C9'); rays(fr, T, 'FFFFFF', .16, CX, 1100)
    def dr(c):
        for k in range(9):
            a = k * .7 + T * .3; r = 120 + 140 * (k % 3)
            microbe(c, CX + r * math.cos(a), 1120 + r * math.sin(a) * .8, .55 * pop(T, S[3] + k * .06), T, '5BC0BE', 0, k, True, 0)
    overlay(fr, L_(dr))
    t = wfind(3, 'nobody')
    if T > t: title(fr, 'NEVER NAMED', 620, T - t, size=124, fill=RED.join(['', '']) if False else YEL)
    t = wfind(3, 'named')
    if T > t: chip(fr, 'NEW SPECIES?', CX, 1430 - 60, T - t, CYAN, 38, -3)

def s_99(fr, T):
    lt = T - S[4]; bg(fr, T, 'DCE8F2'); rays(fr, T, 'FFFFFF', .12)
    u = eout(clamp((T - wfind(4, 'ninety')) / 1.2))
    def dr(c):
        for k in range(100):
            x = 190 + (k % 10) * 78; y = 820 + (k // 10) * 66; on = k < int(99 * u) + (1 if u > .99 else 0) and k != 99
            c.arc(x, y, 24, 0, 6.29); c.set_source_rgba(*hx('5BC0BE' if on else 'D0D0D0')); c.fill_preserve(); ink(c, 3); c.stroke()
    overlay(fr, L_(dr))
    tape(fr, 'UNDER ITS SKIN...', CX, 450, lt, col=RED, size=56, font=LUCKY, rot=-2, tcol='FFFFFF')
    t = wfind(4, 'ninety')
    if T > t: title(fr, 'UP TO 99%', 640, T - t, size=140, fill=YEL)
    t = wfind(4, 'this one')
    if T > t: chip(fr, 'ONE BACTERIUM', CX, 1500 - 60, T - t, 'FFFFFF', 38, 2)

def s_share(fr, T):
    lt = T - S[5]; bg(fr, T, 'FFE08A', .6); rays(fr, T, 'FFFFFF', .2, CX, 1080)
    tape(fr, 'SEND THIS TO...', CX, 450, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (phone(c, CX, 1080, .85 * pop(T, S[5] - .1)), seapig(c, CX, 1120, .5 * pop(T, S[5] + .2), T * 2))))
    chip(fr, '@WADDLES_A_LOT', CX, 900, lt - .2, CYAN, 36, 0)
    t = wfind(5, 'waddles')
    if T > t: burst(fr, 'WADDLE', 830, 700, T - t, r=130, col=YEL, size=44, rot=10)

def s_protein(fr, T):
    tw = wfind(6, 'it makes')
    if T < tw:
        fr[:] = essay_slide(T, [("HERE'S THE", 'grey'), ('WEIRD PART.', 'hl')], [S[6], wfind(6, 'weird') - .2], size=120); return
    lt = T - tw; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .12)
    def dr(c):
        protein(c, 120, 1000, 60, T, BLUE)
        protein(c, 120, 1250, 840 * eout(clamp((T - wfind(6, 'eighteen')) / 1.2)) + 30, T, RED)
    overlay(fr, L_(dr))
    chip(fr, 'NORMAL', 260, 900, lt, 'FFFFFF', 34, -3)
    t = wfind(6, 'eighteen')
    if T > t: chip(fr, 'THIS ONE', 280, 1150, T - t, YEL, 34, 3); title(fr, '~18X LONGER', 640, T - t, size=130, fill=YEL)

def s_unknown(fr, T):
    fr[:] = essay_slide(T, [('WHAT IS IT DOING?', 'main'), ('NOBODY KNOWS. YET.', 'hl')], [S[7], wfind(7, 'nobody') - .1], size=100)

def s_end(fr, T):
    lt = T - S[8]; deep_bg(fr, T)
    def dr(c):
        seapig(c, CX - 40, 1150, 1.0, T)
        microbe(c, CX + 130, 1080, .45 * pop(T, wfind(8, 'roommate')), T, '5BC0BE', 0, 1, True, 0)
    overlay(fr, L_(dr))
    t = wfind(8, 'roommate')
    if T > t: title(fr, 'SECRET ROOMMATE', 600, T - t, size=110, fill=YEL)
    t = wfind(8, "won't")
    if T > t: tape(fr, "...AND IT WON'T TALK", CX, 450, T - t, col=RED, size=54, font=LUCKY, rot=2, tcol='FFFFFF')

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_intro), (S[3], s_look), (S[4], s_found), (S[5], s_99), (S[6], s_share), (S[7], s_protein), (S[8], s_unknown), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'six'), wfind(4, 'ninety'), wfind(8, 'roommate')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Research: Yoshida et al., Univ. of Tokyo, ISME Host Microbe (2026).')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
