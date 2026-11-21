import sys, os, json, math
sys.path.insert(0, '/home/claude/bubble')
from kit import *
D = '/home/claude/bubble'
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

CASH = st('cash', w=560)

def balloon(c, x, y, r, T, label=True, pin=0.0):
    wob = 1 + .02 * math.sin(T * 5)
    c.save(); c.translate(x, y)
    c.move_to(0, r * 1.05); c.curve_to(30, r * 1.4, -30, r * 1.7, 10, r * 2.1); ink(c, 5); c.stroke()
    for dx, dy, col in ((14, 16, '1C1614'), (0, 0, RED)):
        c.save(); c.translate(dx, dy); c.scale(wob, 1.12 / wob); c.arc(0, 0, r, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx(col)); c.fill()
    c.save(); c.scale(wob, 1.12 / wob); c.arc(0, 0, r, 0, 2 * math.pi); c.restore(); ink(c, 9); c.stroke()
    c.save(); c.scale(wob, 1.12 / wob); c.arc(-r * .35, -r * .4, r * .22, 0, 2 * math.pi); c.restore(); c.set_source_rgba(1, 1, 1, .5); c.fill()
    c.move_to(-22, r * 1.12); c.line_to(22, r * 1.12); c.line_to(0, r * 1.02); c.close_path(); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 5); c.stroke()
    if pin > 0:
        px = r * 1.6 - pin * r * .5; c.move_to(px, -r * .6); c.line_to(px + 220, -r * .6 - 120); ink(c, 10); c.stroke()
        c.arc(px + 220, -r * .6 - 120, 26, 0, 2 * math.pi); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def bars(c, T, items, base=1260, x0=330, gap=420, hmax=560, vmax=None):
    vmax = vmax or max(v for v, _, _ in items)
    ink(c, 8); c.move_to(160, base); c.line_to(920, base); c.stroke()
    for j, (v, tg, col) in enumerate(items):
        p = eout((T - tg + .1) / .7); h = hmax * v / vmax * p; x = x0 + j * gap
        c.rectangle(x - 110 + 12, base - h + 14, 220, h); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.rectangle(x - 110, base - h, 220, h); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()

def circle_flow(c, T, a=1.0):
    cx, cy, r = CX, 1030, 250
    for k in range(2):
        a0 = T * 1.2 + k * math.pi; c.arc(cx, cy, r, a0, a0 + 2.4); c.set_source_rgba(*hx(GREEN, a)); c.set_line_width(26); c.stroke()
        a1 = a0 + 2.4; hx_, hy_ = cx + math.cos(a1) * r, cy + math.sin(a1) * r
        c.move_to(hx_ + math.cos(a1) * 40, hy_ + math.sin(a1) * 40); c.line_to(hx_ - math.cos(a1) * 40, hy_ - math.sin(a1) * 40); c.line_to(hx_ - math.sin(a1) * 55, hy_ + math.cos(a1) * 55); c.close_path(); c.set_source_rgba(*hx(GREEN, a)); c.fill()
        u = ((T * .6 + k * .5) % 1) * 2 * math.pi; c.arc(cx + math.cos(u) * r, cy + math.sin(u) * r, 22, 0, 2 * math.pi); c.set_source_rgba(*hx(YEL, a)); c.fill_preserve(); ink(c, 4, a); c.stroke()

def eyes(c, T, n=9):
    rng = np.random.default_rng(3)
    for k in range(n):
        x, y = rng.uniform(170, 910), rng.uniform(780, 1320); s = rng.uniform(.6, 1.1)
        if abs(x - CX) < 260 and abs(y - 1040) < 260: x = CX + (300 if x > CX else -300)
        blink = 1.0 if (T * 1.3 + k * .37) % 3 > .12 else .1
        for sx in (-1, 1):
            c.save(); c.translate(x + sx * 34 * s, y); c.scale(1, blink); c.arc(0, 0, 30 * s, 0, 2 * math.pi); c.restore(); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 5); c.stroke()
            if blink > .5: c.arc(x + sx * 34 * s + 8 * math.sin(T + k), y + 4, 12 * s, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()

def s_hook(fr, T):
    fr[:] = paper('1B2A6B', .82); rays(fr, T, RED, .12, cy=1060)
    overlay(fr, cairo_layer(lambda c: balloon(c, 800, 900, 120 + 60 * eout(T / 3), T)))
    put_rgba(fr, ttext('AI', 80, LUCKY, 'FFFFFF', shadow=False), 800, 900, 1.0 + .5 * eout(T / 3), 1.0, 0)
    ph = photo('fed', 600, 420, (.5, .5))
    if ph is not None: put_rgba(fr, ph, 380, 1150, 1.0, 1.0, -3)
    stamp(fr, 'RISK #1', 380, 1150, T - 1.2, RED, -10, 70)
    tape(fr, "THE FED'S NUMBER ONE RISK", CX, 470, 1.0, col='FFFFFF', size=50, font=LUCKY, rot=-2)
    title(fr, 'IS AI', 600, 1.0, size=140, fill=YEL, rot=-3)

def stamp(fr, txt, x, y, t, col=RED, rot=-12, size=58):
    if t <= 0: return
    f = ImageFont.truetype(LUCKY, size); bb = f.getbbox(txt); w, h = bb[2] + 50, bb[3] + 36
    im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((4, 4, w, h), fill=(255, 255, 255, 200), outline=rgb(col), width=8); d.text((25, 18 - bb[1]), txt, font=f, fill=rgb(col))
    put_rgba(fr, np.array(im), x, y, lerp(2.2, 1.0, eout(clamp(t / .25))), clamp(t / .1), rot)

def s_question(fr, T):
    lt = T - S[1]; fr[:] = paper(BLUE, .68); rays(fr, T, 'FFFFFF', .1)
    overlay(fr, cairo_layer(lambda c: balloon(c, CX - 60, 1000, 230 + 30 * eout(lt / 2), T, pin=eout(lt / 2.5))))
    put_rgba(fr, ttext('AI', 120, LUCKY, 'FFFFFF', shadow=False), CX - 60, 1000, 1.0, 1.0, 0)
    tape(fr, 'WHAT IF THE AI BOOM', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    title(fr, 'GOES BUST?', 590, lt - .15, size=130, fill=YEL)

def s_survey(fr, T):
    lt = T - S[2]; fr[:] = paper(None); rays(fr, T, YEL, .16)
    ph = photo('nyfed', 720, 480, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 960, back(clamp(lt / .35)), 1.0, -2)
    for k, (txt, x, col) in enumerate((('BANKS', 250, YEL), ('FUNDS', CX, 'FFFFFF'), ('BROKERS', 830, CYAN))):
        chip(fr, txt, x, 1300 - 40, lt - .6 - k * .25, col, 40, (-3, 2, -2)[k])
    tape(fr, 'THE NEW YORK FED ASKED', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    title(fr, 'WHAT SCARES YOU MOST?', 600, T - wfind(2, 'scares'), size=84, fill=RED)

def s_pct(fr, T):
    lt = T - S[3]; fr[:] = paper(RED, .76); rays(fr, T, 'FFFFFF', .1)
    t87 = S[3]; t50 = wfind(4, 'fifty')
    overlay(fr, cairo_layer(lambda c: bars(c, T, [(50, t50, 'FFFFFF'), (87, t87, YEL)], vmax=100)))
    if T > t50 - .1: title(fr, '50%', 1260 - 560 * .5 - 70, T - t50 + .1, size=90, fill='FFFFFF', rot=0, cx=330)
    title(fr, '87%', 1260 - 560 * .87 - 70, lt + .1, size=100, fill=YEL, rot=0, cx=750)
    tape(fr, 'SPRING', 330, 1320, T - t50, col='FFFFFF', size=34, font=ELITE, rot=-2); tape(fr, 'NOW', 750, 1320, lt, col=YEL, size=34, font=ELITE, rot=2)
    tape(fr, 'SAID AI', CX, 470, lt, col='FFFFFF', size=64, font=LUCKY, rot=-2)

def s_debt(fr, T):
    lt = T - S[5]; fr[:] = paper(CYAN, .55); rays(fr, T, 'FFFFFF', .12)
    t680 = wfind(5, 'six hundred'); t130 = wfind(6, 'one hundred')
    if T < S[6]:
        ph = photo('dc', 760, 520, (.5, .5))
        if ph is not None: put_rgba(fr, ph, CX, 1000, back(clamp(lt / .35)), 1.0, -2)
        if T > t680: stat(fr, '$680B+', 'BORROWED FOR AI DATA CENTERS', CX, 600, T - t680, RED, -3, 120)
        tape(fr, "HERE'S WHY", CX, 440, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    else:
        overlay(fr, cairo_layer(lambda c: bars(c, T, [(130, t130, 'FFFFFF'), (680, S[6] - .2, RED)])))
        title(fr, '$130B', 1260 - 560 * 130 / 680 - 70, T - t130 + .1, size=80, fill='FFFFFF', rot=0, cx=330)
        title(fr, '$680B', 1260 - 560 - 70, 1.0, size=90, fill=YEL, rot=0, cx=750)
        tape(fr, '2023', 330, 1320, 1.0, col='FFFFFF', size=34, font=ELITE, rot=-2); tape(fr, 'NOW', 750, 1320, 1.0, col=YEL, size=34, font=ELITE, rot=2)
        tape(fr, 'AI DEBT EXPLODED', CX, 470, T - S[6], col='FFFFFF', size=60, font=LUCKY, rot=-2)

def s_2t(fr, T):
    lt = T - S[7]; fr[:] = paper(GREEN, .55); rays(fr, T, 'FFFFFF', .14)
    n = int(clamp(lt / 2.5) * 9)
    def stacks(c):
        for k in range(n):
            for col_ in range(3):
                x = 280 + col_ * 260 + (k % 2) * 12; y = 1300 - k * 52
                c.rectangle(x - 110 + 8, y - 22 + 10, 220, 44); c.set_source_rgba(*hx('1C1614')); c.fill()
                c.rectangle(x - 110, y - 22, 220, 44); c.set_source_rgba(*hx('7BC67E')); c.fill_preserve(); ink(c, 5); c.stroke()
                c.rectangle(x - 22, y - 22, 44, 44); c.set_source_rgba(*hx('E9F5E1')); c.fill_preserve(); ink(c, 3); c.stroke()
    overlay(fr, cairo_layer(stacks))
    tape(fr, 'ADD LEASES + PROMISES', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    t2 = wfind(7, 'two')
    if T > t2: stat(fr, '$2 TRILLION+', 'ON THE LINE', CX, 610, T - t2, RED, -3, 110)

def s_circle(fr, T):
    lt = T - S[8]; fr[:] = paper(YEL, .5); rays(fr, T, 'FFFFFF', .12)
    overlay(fr, cairo_layer(lambda c: circle_flow(c, T, clamp(lt / .5))))
    tape(fr, 'MONEY GOING IN CIRCLES', CX, 470, lt, col=RED, size=56, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > S[9]:
        chip(fr, 'BIG TECH', CX, 760, T - wfind(9, 'big tech'), 'FFFFFF', 46, -2)
        chip(fr, 'SMALL AI COMPANIES', CX, 1300, T - wfind(9, 'smaller'), CYAN, 42, 2)
        if T > wfind(9, 'right back'): burst(fr, 'AND BACK!', 860, 1030, T - wfind(9, 'right back'), r=120, col=RED, size=40)

def s_next(fr, T):
    lt = T - S[10]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHAT', 860, lt, size=170, fill='FFFFFF'); title(fr, 'HAPPENS NEXT?', 1060, lt - .15, size=130, fill=YEL)

def s_fine(fr, T):
    lt = T - S[11]; fr[:] = paper(GREEN, .58); rays(fr, T, 'FFFFFF', .14)
    overlay(fr, cairo_layer(lambda c: balloon(c, CX, 980, 230, T)))
    put_rgba(fr, ttext('AI', 120, LUCKY, 'FFFFFF', shadow=False), CX, 980, 1.0, 1.0, 0)
    tape(fr, 'IF AI KEEPS MAKING MONEY', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    if T > wfind(11, 'nothing'): title(fr, 'NOTHING BREAKS', 600, T - wfind(11, 'nothing'), size=104, fill=YEL)

def s_drop(fr, T):
    lt = T - S[12]; fr[:] = paper('2A2F5A', .82); rays(fr, T, RED, .08)
    def ch(c):
        x0, y0, w, h = 170, 1260, 740, 520; ink(c, 7); c.move_to(x0, y0 - h); c.line_to(x0, y0); c.line_to(x0 + w, y0); c.stroke()
        p = clamp((T - wfind(12, 'drop') + .3) / 1.2); n = int(60 * clamp(lt / 1.0) + 0); c.new_path()
        for j in range(61):
            u = j / 60; v = .3 + .55 * u + .03 * math.sin(u * 30)
            if u > .7: v -= (u - .7) / .3 * .55 * p
            if j > max(n, 42 + int(18 * p)): break
            c.line_to(x0 + w * u, y0 - h * v)
        c.set_source_rgba(*hx(RED)); c.set_line_width(16); c.stroke()
    overlay(fr, cairo_layer(ch))
    tape(fr, 'IF PROFITS DISAPPOINT', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    tb = wfind(12, 'banks')
    if T > tb: stat(fr, '~$1T', 'BIG BANKS EXPOSED', CX, 600, T - tb, YEL, -3, 120)

def s_watch(fr, T):
    lt = T - S[13]; fr[:] = paper(PINK, .55); rays(fr, T, 'FFFFFF', .12)
    overlay(fr, cairo_layer(lambda c: (balloon(c, CX, 1040, 180, T), eyes(c, T))))
    put_rgba(fr, ttext('AI', 90, LUCKY, 'FFFFFF', shadow=False), CX, 1040, 1.0, 1.0, 0)
    tape(fr, "THE FED ISN'T SAYING IT'LL POP", CX, 470, lt, col='FFFFFF', size=46, font=LUCKY, rot=-2)
    tw = wfind(13, 'watching')
    if T > tw - .5: title(fr, "EVERYONE'S WATCHING", 600, T - tw + .5, size=88, fill=RED)

def s_end(fr, T):
    lt = T - S[14]; fr[:] = paper('1B2A6B', .82); rays(fr, T, YEL, .12)
    overlay(fr, cairo_layer(lambda c: balloon(c, CX, 1000, 200, T)))
    put_rgba(fr, ttext('AI', 100, LUCKY, 'FFFFFF', shadow=False), CX, 1000, 1.0, 1.0, 0)
    title(fr, 'BOOM OR BUBBLE?', 560, lt, size=110, fill=YEL)
    if T > S[15]:
        burst(fr, 'BOOM', 230, 1270, T - S[15], r=110, col=GREEN, size=48, rot=-8)
        burst(fr, 'BUBBLE', 850, 1270, T - S[15] - .15, r=120, col=RED, size=40, rot=8)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_question), (S[3], s_survey), (S[5], s_pct), (S[7], s_debt), (S[8], s_2t), (S[10], s_circle), (S[11], s_next),
           (S[12], s_fine), (S[13], s_drop), (S[14], s_watch), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (S[3], wfind(5, 'six hundred'), wfind(7, 'two'), wfind(12, 'drop')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Photos: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
