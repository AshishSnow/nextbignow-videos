import sys, os, json, math
sys.path.insert(0, '/home/claude/altar')
from kit import *
D = '/home/claude/altar'
L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + 0.3; TOTAL = END + 2.6
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


def bg(fr, T, tint='D9C9A8', m=.55): fr[:] = paper(tint, m)

def pin(c, x, y, col, lab_=None):
    c.arc(x + 4, y + 5, 22, 0, 2 * math.pi); c.set_source_rgba(0, 0, 0, .4); c.fill()
    c.arc(x, y, 22, 0, 2 * math.pi); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 5); c.stroke()

def route(fr, T, u, x0=CX - 120, y0=1330, x1=CX + 160, y1=760):
    def dr(c):
        c.set_dash([26, 18]); c.move_to(x0, y0); c.curve_to(x0 - 180, y0 - 250, x1 + 200, y1 + 250, x1, y1)
        c.set_source_rgba(*hx('1C1614', .8)); c.set_line_width(9); c.stroke(); c.set_dash([])
        pin(c, x0, y0, RED); pin(c, x1, y1, CYAN)
    overlay(fr, cairo_layer(dr))
    return x0, y0, x1, y1

def bez(u, x0, y0, x1, y1):
    p = [(x0, y0), (x0 - 180, y0 - 250), (x1 + 200, y1 + 250), (x1, y1)]
    a = (1 - u) ** 3; b = 3 * u * (1 - u) ** 2; c_ = 3 * u * u * (1 - u); d = u ** 3
    return a * p[0][0] + b * p[1][0] + c_ * p[2][0] + d * p[3][0], a * p[0][1] + b * p[1][1] + c_ * p[2][1] + d * p[3][1]

def grid70(fr, T, t0, fail=None):
    def dr(c):
        for k in range(70):
            r_, q = divmod(k, 10); x = 150 + q * 87; y = 800 + r_ * 82
            on = clamp((T - t0 - k * .025) / .12)
            if on <= 0: continue
            c.save(); c.translate(x, y); c.scale(on, on)
            c.rectangle(-26, -30, 52, 60); c.set_source_rgba(*hx('F4EBD7')); c.fill_preserve(); ink(c, 4); c.stroke()
            c.rectangle(-26, -30, 52, 14); c.set_source_rgba(*hx('A0522D')); c.fill()
            if fail is not None:
                f = clamp((T - fail - k * .02) / .1)
                if f > 0:
                    c.set_source_rgba(*hx(RED)); c.set_line_width(9 * f)
                    c.move_to(-20, -20); c.line_to(20, 20); c.move_to(20, -20); c.line_to(-20, 20); c.stroke()
            c.restore()
    overlay(fr, cairo_layer(dr))

def fingerprint(c, x, y, T, s=1.0):
    for k in range(9):
        r = (30 + k * 26) * s; a0 = -math.pi * .95 + .2 * math.sin(k); a1 = math.pi * .2 + .3 * math.cos(k * 1.7)
        c.save(); c.translate(x, y); c.scale(.78, 1); c.arc(0, 0, r, a0, a1); c.restore()
        c.set_source_rgba(*hx('6B3E26', .85)); c.set_line_width(10 * s); c.stroke()
    sy = y - 260 * s + ((T * .5) % 1) * 520 * s
    c.rectangle(x - 260 * s, sy - 4, 520 * s, 8); c.set_source_rgba(*hx(CYAN, .8)); c.fill()

def s_hook(fr, T):
    bg(fr, T); rays(fr, T, 'FFFFFF', .12)
    ph = photo('stonehenge', 820, 560, (.5, .55))
    if ph is not None: put_rgba(fr, ph, CX, 1000, back(clamp(T / .35)), 1.0, -2)
    sk(fr, st('stone', w=520), 720, 1260, T, 0, 1.0, -6, T - .4)
    tape(fr, "STONEHENGE'S 6-TON STONE", CX, 470, T, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    title(fr, 'LOST ITS HOME', 600, T - .15, size=124, fill=YEL, rot=-3)
    if T > wfind(0, 'again'): burst(fr, 'AGAIN!', 250, 1290, T - wfind(0, 'again'), r=105, col=RED, size=48, rot=-10)

def s_question(fr, T):
    lt = T - S[1]; bg(fr, T, 'B9D3C2')
    ph = photo('scot', 800, 560, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1010, back(clamp(lt / .35)), 1.0, 2)
    tape(fr, 'SCIENTISTS WERE SURE', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    title(fr, 'SCOTLAND?', 600, lt - .15, size=130, fill=YEL)
    if T > wfind(1, 'no.'): xstamp(fr, CX, 1010, T - wfind(1, 'no.'), 1.3)

def s_altar(fr, T):
    lt = T - S[2]; bg(fr, T)
    ph = photo('altar', 820, 560, (.5, .6))
    if ph is not None: put_rgba(fr, ph, CX, 1030, back(clamp(lt / .35)), 1.0, -1)
    tape(fr, 'THE ALTAR STONE', CX, 470, lt, col=RED, size=66, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > wfind(2, 'six'): stat(fr, '6 TONS', 'SANDSTONE SLAB', 300, 640, T - wfind(2, 'six'), YEL, -4, 110)
    if T > wfind(2, 'sixteen'): stat(fr, '16 FT', 'LONG', 790, 640, T - wfind(2, 'sixteen'), RED, 3, 110)
    if T > wfind(2, 'center'): chip(fr, 'DEAD CENTER OF THE CIRCLE', CX, 1360, T - wfind(2, 'center'), 'FFFFFF', 40, -2)

def s_2024(fr, T):
    lt = T - S[3]; bg(fr, T, 'C9DDF0')
    x0, y0, x1, y1 = route(fr, T, 1)
    tape(fr, 'STONEHENGE', x0 - 40, y0 + 70, lt, col='FFFFFF', size=40, font=LUCKY, rot=2)
    tape(fr, 'NE SCOTLAND', x1, y1 - 70, lt - .6, col=CYAN, size=40, font=LUCKY, rot=-2)
    tape(fr, '2024 STUDY SAID...', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    tm = wfind(3, 'over')
    if T > tm:
        n = int(460 * eout(clamp((T - tm) / 1.0))); title(fr, f'{n}+ MILES', 600, T - tm, size=120, fill=YEL)

def s_drag(fr, T):
    lt = T - S[4]; bg(fr, T, 'C9DDF0')
    x0, y0, x1, y1 = route(fr, T, 1)
    u = ease(clamp(lt / max(1, L[4]['dur'])))
    x, y = bez(u, x0, y0, x1, y1)
    def rope(c):
        c.move_to(x, y); c.line_to(x + 150, y - 120); c.set_source_rgba(*hx('8B5A2B')); c.set_line_width(8); c.stroke()
    overlay(fr, cairo_layer(rope))
    s_ = st('stone', w=300)
    if s_ is not None: sticker(fr, s_, x, y, T, 0, 1.0, -8 + 4 * math.sin(T * 6), 1.0, 4)
    tape(fr, 'DRAG 6 TONS...', CX, 470, lt, col=RED, size=64, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > wfind(4, 'across'): title(fr, 'ACROSS HALF OF BRITAIN', 600, T - wfind(4, 'across'), size=92, fill=YEL)

def s_twist(fr, T):
    lt = T - S[5]; bg(fr, T, 'E8C9A0'); rays(fr, T, 'FFFFFF', .1)
    ph = photo('orkney', 820, 420, (.5, .5))
    if ph is not None and lt < 2.2: put_rgba(fr, ph, CX, 1000, back(clamp(lt / .3)), 1.0, -2)
    tape(fr, "BUT HERE'S THE TWIST", CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    ts = wfind(5, 'seventy')
    if T > ts:
        stat(fr, '70 SAMPLES', 'FROM THAT EXACT AREA', CX, 600, T - ts, YEL, -3, 110)
        if lt >= 2.2: grid70(fr, T, ts + .2)

def s_print(fr, T):
    lt = T - S[6]; bg(fr, T, 'EADFC8')
    ph = photo('lab', 820, 500, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1140, 1.0, .35, 0)
    overlay(fr, cairo_layer(lambda c: fingerprint(c, CX, 1040, T, 1.0)))
    tape(fr, 'A GEOLOGICAL FINGERPRINT', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    for k, (w_, lab_, col) in enumerate((('grains', 'GRAINS', YEL), ('minerals', 'MINERALS', CYAN), ('chemistry', 'CHEMISTRY', 'FFFFFF'))):
        tk = wfind(6, w_)
        if T > tk: chip(fr, lab_ + '  OK', [230, CX, 850][k], 640 + (k % 2) * 70, T - tk, col, 36, [-4, 2, -2][k])

def s_zero(fr, T):
    lt = T - S[7]; bg(fr, T, 'F2C4B8')
    grid70(fr, T, S[7] - 5, fail=S[7] + .1)
    title(fr, '0 MATCHES', 560, lt, size=150, fill='FFFFFF', rot=-3)
    if T > wfind(7, 'not one'): burst(fr, 'NOT ONE', 820, 1440 - 180, T - wfind(7, 'not one'), r=120, col=RED, size=44, rot=8)

def s_home(fr, T):
    lt = T - S[8]; bg(fr, T)
    sk(fr, st('henge', w=420), 800, 960, T, 1, .8, 6, lt - .2)
    s = st('stone', w=600)
    if s is not None: put_rgba(fr, glow_outline(s, 14, (255, 255, 255)), CX, 1050, back(clamp(lt / .35)), 1.0, -4 + 2 * math.sin(T * 2))
    tape(fr, 'MOST FAMOUS ROCK IN BRITAIN', CX, 470, lt, col='FFFFFF', size=50, font=LUCKY, rot=-2)
    if T > wfind(8, 'no home'): title(fr, 'NO HOME AGAIN', 600, T - wfind(8, 'no home'), size=118, fill=YEL)
    if T > wfind(8, 'no home'): burst(fr, '?', 830, 1300 - 80, T - wfind(8, 'no home') - .2, r=90, col=RED, size=90)

def s_next(fr, T):
    lt = T - S[9]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHAT', 860, lt, size=170, fill='FFFFFF'); title(fr, 'HAPPENS NEXT?', 1060, lt - .15, size=130, fill=YEL)

def s_hunt(fr, T):
    lt = T - S[10]; bg(fr, T, 'B9D3C2')
    tape(fr, 'THE NEW HUNT', CX, 470, lt, col=RED, size=66, font=LUCKY, rot=-2, tcol='FFFFFF')
    for k, (w_, nm, lab_, x, y, r) in enumerate((('england', 'england', 'NORTHERN ENGLAND', 330, 760, -4), ('scotland', 'scot2', 'OTHER PARTS OF SCOTLAND', 760, 1000, 3), ('ireland', 'ireland', 'IRELAND?', 330, 1260, -2))):
        tk = wfind(10, w_) - .2
        if T > tk:
            ph = photo(nm, 470, 300, (.5, .5))
            if ph is not None: put_rgba(fr, ph, x, y, back(clamp((T - tk) / .3)), 1.0, r)
            chip(fr, lab_, x, y + 175, T - tk - .1, [YEL, CYAN, 'FFFFFF'][k], 36, r)

def s_quarry(fr, T):
    lt = T - S[11]; bg(fr, T, 'E8C9A0'); rays(fr, T, 'FFFFFF', .1)
    ph = photo('trilithon', 820, 560, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1030, 1.0 + .04 * lt, 1.0, 2)
    tape(fr, 'FIND THE QUARRY', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    if T > wfind(11, 'who'): title(fr, 'WHO MOVED IT?', 600, T - wfind(11, 'who'), size=112, fill=YEL)
    if T > wfind(11, 'how'): burst(fr, 'HOW?', 820, 1320, T - wfind(11, 'how'), r=110, col=RED, size=56)

def s_end(fr, T):
    lt = T - S[12]; bg(fr, T, 'C9DDF0')
    sk(fr, st('henge', w=380), CX + 160, 930, T, 1, 1.0, 4)
    sk(fr, st('stone', w=460), CX - 120, 1130, T, 0, 1.0, -5)
    title(fr, "WILL THEY EVER FIND IT?", 560, lt, size=90, fill=YEL)
    if T > S[13]:
        burst(fr, 'YES', 230, 1280, T - S[13], r=100, col=GREEN, size=54, rot=-8)
        burst(fr, 'NO', 850, 1280, T - S[13] - .15, r=100, col=RED, size=54, rot=8)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_question), (S[3], s_altar), (S[4], s_2024), (S[5], s_drag), (S[6], s_twist), (S[7], s_print), (S[8], s_zero),
           (S[9], s_home), (S[10], s_next), (S[11], s_hunt), (S[12], s_quarry), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(1, 'no.'), S[7] + .1, wfind(5, 'twist')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Images: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
