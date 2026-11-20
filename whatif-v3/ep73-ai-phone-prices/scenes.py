import sys, os, json, math
sys.path.insert(0, '/home/claude/ram')
from kit import *
D = '/home/claude/ram'
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

RAM = st('ram', w=640); RAMS = st('ram', w=220); PHONE = st('phone', h=760); LAPTOP = st('laptop', w=600); CHIP = st('chip', w=420)

def pricetag(c, x, y, s, rot, col=YEL):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.move_to(-60, -260); c.line_to(0, -150); ink(c, 6); c.stroke()
    for dx, dy, cc in ((14, 16, '1C1614'), (0, 0, col)):
        c.move_to(-170 + dx, -90 + dy); c.line_to(60 + dx, -150 + dy); c.line_to(170 + dx, -20 + dy); c.line_to(170 + dx, 150 + dy); c.line_to(-170 + dx, 150 + dy); c.close_path(); c.set_source_rgba(*hx(cc)); c.fill()
    c.move_to(-170, -90); c.line_to(60, -150); c.line_to(170, -20); c.line_to(170, 150); c.line_to(-170, 150); c.close_path(); ink(c, 8); c.stroke()
    c.arc(60, -100, 16, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 5); c.stroke(); c.restore()

def recycle(c, x, y, r, T):
    for k in range(3):
        a0 = T * 1.5 + k * 2 * math.pi / 3; c.arc(x, y, r, a0, a0 + 1.6); c.set_source_rgba(*hx(GREEN)); c.set_line_width(34); c.stroke()
        a1 = a0 + 1.6; hx_, hy_ = x + math.cos(a1) * r, y + math.sin(a1) * r
        c.move_to(hx_ + math.cos(a1) * 40, hy_ + math.sin(a1) * 40); c.line_to(hx_ - math.cos(a1) * 40, hy_ - math.sin(a1) * 40); c.line_to(hx_ - math.sin(a1) * 50, hy_ + math.cos(a1) * 50); c.close_path(); c.set_source_rgba(*hx(GREEN)); c.fill()

def rising(c, T, t0, x0=170, y0=1300, w=740, h=520, end_label=True):
    ink(c, 7); c.move_to(x0, y0 - h); c.line_to(x0, y0); c.line_to(x0 + w, y0); c.stroke()
    p = clamp((T - t0) / 1.8); n = int(60 * p); c.new_path()
    for j in range(n + 1):
        u = j / 60; v = .15 + .75 * (1 - math.exp(-u * 2.6)) + .03 * math.sin(u * 25)
        c.line_to(x0 + w * u, y0 - h * v)
    c.set_source_rgba(*hx(RED)); c.set_line_width(16); c.stroke()

def s_hook(fr, T):
    fr[:] = paper(RED, .76); rays(fr, T, 'FFFFFF', .14, cy=1080)
    sk(fr, PHONE, 420, 1060, T, 0, .95, -8)
    overlay(fr, cairo_layer(lambda c: pricetag(c, 780, 1000, 1.0, .15 * math.sin(T * 3))))
    price = int(lerp(799, 1099, eout(T / 2.2))); put_rgba(fr, ttext(f'${price:,}', 84, LUCKY, '1C1614', 'FFFFFF', shadow=False), 790, 1030, 1.0, 1.0, 8 * math.sin(T * 3))
    burst(fr, 'AI', 800, 760, T - .4, r=95, col=CYAN, size=70)
    tape(fr, 'AI IS MAKING YOUR PHONE', CX, 470, 1.0, col='FFFFFF', size=50, font=LUCKY, rot=-2)
    title(fr, 'MORE EXPENSIVE', 600, 1.0, size=110, fill=YEL, rot=-3)

def s_question(fr, T):
    lt = T - S[1]; fr[:] = paper(BLUE, .68); rays(fr, T, 'FFFFFF', .1)
    sk(fr, PHONE, 300, 1050, T, 1, .7, -6, lt); sk(fr, LAPTOP, 770, 1080, T, 2, .8, 4, lt - .3)
    burst(fr, '$$$', CX, 800, lt - .8, r=100, col=YEL, size=60)
    tape(fr, 'WHY WILL YOUR NEXT DEVICE', CX, 470, lt, col='FFFFFF', size=48, font=LUCKY, rot=-2)
    title(fr, 'COST WAY MORE?', 590, lt - .15, size=104, fill=YEL)

def s_ram(fr, T):
    lt = T - S[2]; fr[:] = paper(None); rays(fr, T, YEL, .16)
    sk(fr, RAM, CX, 1000, T, 3, 1.0, -6, lt)
    tape(fr, 'EVERY DEVICE NEEDS', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    tr = wfind(2, 'ram')
    if T > tr - .4: title(fr, 'MEMORY CHIPS (RAM)', 600, T - tr + .4, size=88, fill=RED)

def s_ai(fr, T):
    lt = T - S[3]; fr[:] = paper('1B2A6B', .82); rays(fr, T, CYAN, .12)
    ph = photo('server', 620, 700, (.5, .5))
    if ph is not None: put_rgba(fr, ph, 700, 1010, back(clamp(lt / .35)), 1.0, 3)
    if RAMS is not None:
        for k in range(6):
            u = ((lt * .5 + k / 6) % 1); put_rgba(fr, RAMS, lerp(80, 620, u), 820 + k * 80, .9, 1.0 - u * .3, -20 + 40 * u)
    tape(fr, 'AI DATA CENTERS BUY FIRST', CX, 470, lt, col='FFFFFF', size=50, font=LUCKY, rot=-2)
    tw = wfind(3, 'paying')
    if T > tw: burst(fr, 'PAYING MORE!', 300, 1300 - 60, T - tw, r=140, col=YEL, size=38)

def s_fab(fr, T):
    lt = T - S[4]; fr[:] = paper(CYAN, .55); rays(fr, T, 'FFFFFF', .12)
    ph = photo('fab', 760, 560, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 960, back(clamp(lt / .35)), 1.0, -2)
    tape(fr, 'CHIPMAKERS SWITCH FACTORIES', CX, 470, lt, col='FFFFFF', size=46, font=LUCKY, rot=-2)
    chip(fr, 'PHONES  >>>  AI', CX, 1310, lt - .8, RED, 52, -2)

def s_double(fr, T):
    lt = T - S[5]; fr[:] = paper(RED, .74); rays(fr, T, 'FFFFFF', .1)
    td = wfind(5, 'doubled'); base = 1260
    def dr(c):
        ink(c, 8); c.move_to(220, base); c.line_to(860, base); c.stroke()
        for j, (v, col) in enumerate(((1, 'FFFFFF'), (2, YEL))):
            p = 1.0 if j == 0 else eout((T - td + .1) / .6); h = 260 * v * p if j else 260 * eout(lt / .5); x = 390 + j * 300
            c.rectangle(x - 100 + 12, base - h + 14, 200, h); c.set_source_rgba(*hx('1C1614')); c.fill()
            c.rectangle(x - 100, base - h, 200, h); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    overlay(fr, cairo_layer(dr))
    tape(fr, 'BEFORE', 390, base + 60, lt, col='FFFFFF', size=34, font=ELITE, rot=-2); tape(fr, 'NOW', 690, base + 60, T - td, col=YEL, size=34, font=ELITE, rot=2)
    tape(fr, 'MEMORY PRICES', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    if T > td: title(fr, 'ROUGHLY DOUBLED', 600, T - td, size=100, fill=YEL)

def s_phone(fr, T):
    lt = T - S[6]; fr[:] = paper(PINK, .55); rays(fr, T, 'FFFFFF', .14)
    sk(fr, PHONE, 360, 1060, T, 4, .8, -5, lt)
    overlay(fr, cairo_layer(lambda c: pricetag(c, 790, 1040, .9, .12 * math.sin(T * 3), RED)))
    put_rgba(fr, ttext('+25-30%', 62, LUCKY, 'FFFFFF', shadow=False), 800, 1070, back(clamp((T - wfind(6, 'twenty')) / .3)), 1.0, 7 * math.sin(T * 3))
    tape(fr, 'PHONE PRICES', CX, 470, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    chip(fr, 'IN JUST ONE YEAR', CX, 600, T - wfind(6, 'year'), YEL, 44, 2)

def s_laptop(fr, T):
    lt = T - S[7]; fr[:] = paper(GREEN, .55); rays(fr, T, 'FFFFFF', .14)
    sk(fr, LAPTOP, CX, 1060, T, 5, 1.0, -3, lt)
    tape(fr, 'LAPTOP MAKERS', CX, 470, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    stat(fr, '+20%', 'UP TO', CX, 640, T - wfind(7, 'twenty'), RED, -3, 150)

def s_shelf(fr, T):
    lt = T - S[8]; fr[:] = paper(YEL, .55); rays(fr, T, 'FFFFFF', .12)
    ph = photo('store', 760, 560, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1000, 1.0, 1.0 - .55 * eout((T - wfind(8, 'disappearing')) / 1.2), -2)
    tape(fr, 'PHONES UNDER $200?', CX, 470, lt, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')
    tw = wfind(8, 'disappearing')
    if T > tw: title(fr, 'DISAPPEARING', 600, T - tw, size=110, fill='FFFFFF'); xstamp(fr, CX, 1000, T - tw - .4, 1.1)

def s_recycle(fr, T):
    lt = T - S[9]; fr[:] = paper(GREEN, .5); rays(fr, T, 'FFFFFF', .12)
    overlay(fr, cairo_layer(lambda c: recycle(c, CX, 1030, 300, T)))
    sk(fr, CHIP, CX, 1030, T, 6, .9, -6, lt)
    tape(fr, 'SOME BRANDS PLAN', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    tw = wfind(9, 'used')
    if T > tw: title(fr, 'USED MEMORY CHIPS', 600, T - tw, size=92, fill=YEL)

def s_next(fr, T):
    lt = T - S[10]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHAT', 860, lt, size=170, fill='FFFFFF'); title(fr, 'HAPPENS NEXT?', 1060, lt - .15, size=130, fill=YEL)

def s_tight(fr, T):
    lt = T - S[11]; fr[:] = paper('2A2F5A', .82); rays(fr, T, 'FFFFFF', .08)
    sq = eout((T - wfind(11, 'tighter')) / .6)
    def vise(c):
        gap = lerp(360, 180, sq)
        for sx in (-1, 1):
            c.rectangle(CX + sx * gap - 60 + 12, 860 + 14, 120, 380); c.set_source_rgba(*hx('1C1614')); c.fill()
            c.rectangle(CX + sx * gap - 60, 860, 120, 380); c.set_source_rgba(*hx('A0AEC0')); c.fill_preserve(); ink(c, 8); c.stroke()
    overlay(fr, cairo_layer(vise))
    sk(fr, RAM, CX, 1050, T, 7, .55 - .1 * sq, 90 - 6)
    tape(fr, 'A TOP CHIPMAKER SAYS', CX, 470, lt, col=YEL, size=54, font=LUCKY, rot=-2)
    if T > wfind(11, 'tighter'): title(fr, 'EVEN TIGHTER', 600, T - wfind(11, 'tighter'), size=112, fill='FFFFFF')

def s_2028(fr, T):
    lt = T - S[12]; fr[:] = paper(None); rays(fr, T, RED, .1)
    overlay(fr, cairo_layer(lambda c: rising(c, T, S[12] + .1)))
    tape(fr, 'PRICES COULD KEEP CLIMBING', CX, 470, lt, col='FFFFFF', size=48, font=LUCKY, rot=-2)
    if lt > 1.4: chip(fr, 'UNTIL MID-2028', 760, 760, lt - 1.4, RED, 44, -3)

def s_wait(fr, T):
    lt = T - S[13]; fr[:] = paper(BLUE, .65); rays(fr, T, 'FFFFFF', .12)
    sk(fr, PHONE, 330, 1060, T, 8, .7, -6); sk(fr, LAPTOP, 780, 1100, T, 9, .7, 4)
    tape(fr, 'NEED A NEW ONE?', CX, 470, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    tw = wfind(13, 'waiting')
    if T > tw: title(fr, 'WAITING MIGHT COST MORE', 600, T - tw, size=76, fill=YEL)

def s_end(fr, T):
    lt = T - S[14]; fr[:] = paper(RED, .76); rays(fr, T, 'FFFFFF', .12)
    sk(fr, PHONE, CX, 1050, T, 10, .8, -4)
    title(fr, 'BUY NOW OR WAIT?', 560, lt, size=100, fill=YEL)
    if T > S[15]:
        burst(fr, 'NOW', 250, 1250, T - S[15], r=110, col=GREEN, size=54, rot=-8)
        burst(fr, 'WAIT', 830, 1250, T - S[15] - .15, r=110, col=CYAN, size=50, rot=8)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_question), (S[3], s_ram), (S[4], s_ai), (S[5], s_fab), (S[6], s_double), (S[7], s_phone), (S[8], s_laptop),
           (S[9], s_shelf), (S[10], s_recycle), (S[11], s_next), (S[12], s_tight), (S[13], s_2028), (S[14], s_wait), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(5, 'doubled'), wfind(7, 'twenty'), wfind(8, 'disappearing') + .4, wfind(11, 'tighter')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Photos: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
