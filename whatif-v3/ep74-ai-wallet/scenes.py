import sys, os, json, math
sys.path.insert(0, '/home/claude/wallet')
from kit import *
D = '/home/claude/wallet'
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

WAL = st('wallet', w=560); CART = st('cart', w=520); CARD = st('card', w=480); PARCEL = st('parcel', w=300); FOOD = st('food', h=520)

def rhand(c, x, y, s, grip=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx, dy, col in ((12, 14, '1C1614'), (0, 0, 'C9D1DA')):
        c.rectangle(-60 + dx, 40 + dy, 120, 260); c.set_source_rgba(*hx(col)); c.fill()
        c.rectangle(-90 + dx, -60 + dy, 180, 110); c.fill()
        for k in range(4):
            fx = -75 + k * 50; c.rectangle(fx + dx, -160 + 30 * grip + dy, 34, 110); c.fill()
    c.rectangle(-60, 40, 120, 260); c.set_source_rgba(*hx('C9D1DA')); ink(c, 7); c.stroke()
    c.rectangle(-90, -60, 180, 110); ink(c, 7); c.stroke()
    for k in range(4): c.rectangle(-75 + k * 50, -160 + 30 * grip, 34, 110); ink(c, 6); c.stroke()
    c.arc(0, 0, 18, 0, 2 * math.pi); c.set_source_rgba(*hx(CYAN)); c.fill(); c.restore()

def bubble(fr, txt, x, y, t, me=True, size=40):
    if t <= 0: return
    f = ImageFont.truetype(INTER, size); f.set_variation_by_name('Bold'); bb = f.getbbox(txt); w, h = bb[2] + 60, bb[3] + 44
    im = Image.new('RGBA', (w + 20, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    col = rgb(BLUE) if me else (255, 255, 255)
    d.rounded_rectangle((8, 10, w + 8, h + 10), 28, fill=INK + (255,)); d.rounded_rectangle((0, 0, w, h), 28, fill=col, outline=INK, width=4)
    d.polygon([(w - 50, h - 2), (w - 10, h + 26), (w - 80, h - 2)] if me else [(50, h - 2), (10, h + 26), (80, h - 2)], fill=col)
    d.text((30, 22 - bb[1]), txt, font=f, fill=(255, 255, 255) if me else INK)
    put_rgba(fr, np.array(im), x, y, back(clamp(t / .3)), 1.0, 0)

def phone_ui(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-210 + 14, -400 + 16, 420, 800); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-210, -400, 420, 800); c.set_source_rgba(*hx('2A2F3A')); c.fill_preserve(); ink(c, 9); c.stroke()
    c.rectangle(-185, -370, 370, 740); c.set_source_rgba(*hx('F4F6FA')); c.fill(); c.restore()

def stamp(fr, txt, x, y, t, col=RED, rot=-12, size=58):
    if t <= 0: return
    f = ImageFont.truetype(LUCKY, size); bb = f.getbbox(txt); w, h = bb[2] + 50, bb[3] + 36
    im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((4, 4, w, h), outline=rgb(col), width=8); d.text((25, 18 - bb[1]), txt, font=f, fill=rgb(col))
    put_rgba(fr, np.array(im), x, y, lerp(2.2, 1.0, eout(clamp(t / .25))), clamp(t / .1), rot)

def s_hook(fr, T):
    fr[:] = paper(GREEN, .62); rays(fr, T, 'FFFFFF', .14, cy=1080)
    sk(fr, WAL, 380, 1080, T, 0, 1.0, -8)
    sk(fr, CARD, 560 + 160 * eout(T / 1.2), 980 - 80 * eout(T / 1.2), T, 1, .55, 20)
    overlay(fr, cairo_layer(lambda c: rhand(c, 820 - 60 * eout(T / 1.2), 1050, 1.0, eout(T / 1.0))))
    tape(fr, 'YOUR AI CAN NOW', CX, 470, 1.0, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    title(fr, 'SPEND YOUR MONEY', 600, 1.0, size=104, fill=YEL, rot=-3)

def s_question(fr, T):
    lt = T - S[1]; fr[:] = paper(BLUE, .68); rays(fr, T, 'FFFFFF', .1)
    overlay(fr, cairo_layer(lambda c: phone_ui(c, CX, 1060, .95)))
    bubble(fr, 'buy me new sneakers', 610, 880, lt - .3, True)
    bubble(fr, 'Done. $89, arrives Friday', 480, 1060, lt - 1.3, False, 36)
    tape(fr, 'WHAT IF CHATGPT', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    title(fr, 'GOT YOUR WALLET?', 590, lt - .15, size=104, fill=YEL)

def s_launch(fr, T):
    lt = T - S[2]; fr[:] = paper(None); rays(fr, T, YEL, .16)
    sk(fr, WAL, CX, 1040, T, 2, 1.1, -4, lt)
    tape(fr, 'OPENAI JUST LAUNCHED', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    title(fr, 'CHATGPT WALLET', 600, lt - wfind(2, 'wallet') + S[2], size=110, fill=RED)
    chip(fr, 'U.S.  |  PRO USERS  |  18+', CX, 1330, T - wfind(2, 'u.s'), 'FFFFFF', 40, -2)

def s_buys(fr, T):
    lt = T - S[3]; fr[:] = paper(PINK, .55); rays(fr, T, 'FFFFFF', .12)
    bubble(fr, 'I need running shoes', CX + 120, 720, lt, True)
    tb = wfind(3, 'buys')
    sk(fr, CART, CX, 1130, T, 3, .9, -3, lt - .4)
    if T > tb - .3:
        y = lerp(700, 1040, eout((T - tb + .3) / .6)); sk(fr, PARCEL, CX + 20, y, T, 4, .8, 10)
    if T > tb + .3: burst(fr, 'BOUGHT!', 830, 900, T - tb - .3, r=120, col=YEL, size=46)
    tape(fr, 'YOU ASK. IT BUYS.', CX, 470, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)

def s_token(fr, T):
    lt = T - S[4]; fr[:] = paper('1B2A6B', .82); rays(fr, T, CYAN, .12)
    sk(fr, CARD, 330, 1000, T, 5, .9, -8, lt)
    tt = wfind(4, 'token')
    def lockd(c):
        c.save(); c.translate(790, 1030); c.scale(1.0, 1.0)
        c.arc(0, -120, 80, math.pi, 0); c.line_to(80, -60); c.move_to(-80, -120); c.line_to(-80, -60); ink(c, 30); c.stroke()
        c.rectangle(-130 + 12, -70 + 14, 260, 210); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.rectangle(-130, -70, 260, 210); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 8); c.stroke(); c.restore()
    if T > tt - .3: overlay(fr, cairo_layer(lockd))
    tape(fr, 'NEVER SEES YOUR CARD NUMBER', CX, 470, lt, col='FFFFFF', size=46, font=LUCKY, rot=-2)
    if T > tt: chip(fr, 'SECRET TOKEN: A7#9-K2X', CX, 1330, T - tt, YEL, 42, -2)

def s_bio(fr, T):
    lt = T - S[5]; fr[:] = paper(CYAN, .55); rays(fr, T, 'FFFFFF', .14)
    def fp(c):
        for k in range(9):
            r = 30 + k * 26; c.arc(CX, 1040, r, math.pi * (1.1 + .05 * k), math.pi * (1.9 + .1 * math.sin(k)))
            c.set_source_rgba(*hx('1C1614', clamp((lt - k * .08) / .2))); c.set_line_width(14); c.stroke()
        scan = 1040 - 260 + (lt * 300 % 520); c.rectangle(CX - 280, scan, 560, 10); c.set_source_rgba(*hx(GREEN, .8)); c.fill()
    overlay(fr, cairo_layer(fp))
    tape(fr, 'EVERY SINGLE PURCHASE', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    title(fr, 'FACE OR FINGERPRINT', 600, T - wfind(5, 'face'), size=86, fill=RED)

def s_twist(fr, T):
    lt = T - S[6]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, "BUT HERE'S", 860, lt, size=170, fill='FFFFFF'); title(fr, 'THE TWIST', 1060, lt - .12, size=170, fill=YEL)

def s_block(fr, T):
    lt = T - S[7]; fr[:] = paper(YEL, .55); rays(fr, T, 'FFFFFF', .12)
    tu = wfind(7, 'united'); ta = wfind(7, 'amazon'); te = wfind(7, 'ebay')
    if T > tu - .1:
        p = back(clamp((T - tu + .1) / .3))
        def pl(c):
            c.save(); c.translate(300, 820); c.scale(p, p); c.rotate(-.15)
            for dx, dy, col in ((10, 12, '1C1614'), (0, 0, 'FFFFFF')):
                c.save(); c.translate(dx, dy); c.scale(1, .28); c.arc(0, 0, 200, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx(col)); c.fill()
                c.move_to(-40 + dx, dy); c.line_to(60 + dx, 150 + dy); c.line_to(100 + dx, 150 + dy); c.line_to(60 + dx, dy); c.close_path(); c.fill()
                c.move_to(-40 + dx, dy); c.line_to(60 + dx, -150 + dy); c.line_to(100 + dx, -150 + dy); c.line_to(60 + dx, dy); c.close_path(); c.fill()
                c.move_to(-180 + dx, dy); c.line_to(-210 + dx, -100 + dy); c.line_to(-160 + dx, -100 + dy); c.line_to(-130 + dx, dy); c.close_path(); c.fill()
            c.save(); c.scale(1, .28); c.arc(0, 0, 200, 0, 2 * math.pi); c.restore(); ink(c, 6); c.stroke()
            for k in range(6): c.arc(-90 + k * 40, -8, 9, 0, 2 * math.pi); c.set_source_rgba(*hx(BLUE)); c.fill()
            c.restore()
        overlay(fr, cairo_layer(pl))
    sk(fr, PARCEL, 790, 860, T, 6, .9, 6, T - ta + .1)
    sk(fr, CART, CX, 1190, T, 7, .55, -3, T - te + .1)
    tb = wfind(7, 'blocking')
    stamp(fr, 'BLOCKED', 300, 820, T - tb, RED, -12, 50); stamp(fr, 'BLOCKED', 790, 860, T - tb - .15, RED, 10, 50); stamp(fr, 'BLOCKED', CX, 1190, T - tb - .3, RED, -6, 50)
    chip(fr, 'AIRLINE', 300, 1010, T - tu, 'FFFFFF', 34, -3); chip(fr, 'SHOPPING SITES', 790, 1040, T - ta, 'FFFFFF', 34, 3)
    tape(fr, 'BIG NAMES SAY NO', CX, 470, lt, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')

def s_tiny(fr, T):
    lt = T - S[8]; fr[:] = paper(PINK, .5); rays(fr, T, 'FFFFFF', .1)
    sk(fr, FOOD, CX, 1050, T, 8, .85 * (1 - .5 * eout((T - wfind(8, 'tiny')) / .5)), -4, lt)
    t5 = wfind(8, 'five hundred')
    if T > t5: stat(fr, '~500', 'AI FOOD ORDERS IN A WEEK', CX, 560, T - t5, YEL, -3, 140)
    if T > wfind(8, 'tiny'): burst(fr, 'TINY!', 830, 1250, T - wfind(8, 'tiny'), r=110, col=RED, size=56)

def s_next(fr, T):
    lt = T - S[9]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHAT', 860, lt, size=170, fill='FFFFFF'); title(fr, 'HAPPENS NEXT?', 1060, lt - .15, size=130, fill=YEL)

def store(c, x, y, s, open_=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-200 + 12, -180 + 14, 400, 380); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-200, -180, 400, 380); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    for k in range(5):
        c.rectangle(-200 + k * 80, -240, 80, 70); c.set_source_rgba(*hx(RED if k % 2 else 'FFFFFF')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.rectangle(-70, 20, 140, 180); c.set_source_rgba(*hx(GREEN if open_ else '6B7280')); c.fill_preserve(); ink(c, 7); c.stroke(); c.restore()

def s_choose(fr, T):
    lt = T - S[10]; fr[:] = paper(BLUE, .62); rays(fr, T, 'FFFFFF', .1)
    overlay(fr, cairo_layer(lambda c: (store(c, 300, 1040, .95, True), store(c, 790, 1040, .95, False))))
    tl = wfind(10, 'let'); to = wfind(10, 'lose')
    chip(fr, 'AI WELCOME', 300, 760, T - tl, GREEN, 40, -3); stamp(fr, 'NO AI', 790, 1080, T - to, RED, 10, 56)
    if CART is not None and T > tl: put_rgba(fr, CART, lerp(-100, 300, eout((T - tl) / 1.2)), 1290, .38, 1.0, 0)
    tape(fr, 'STORES WILL HAVE TO CHOOSE', CX, 470, lt, col='FFFFFF', size=48, font=LUCKY, rot=-2)

def s_war(fr, T):
    lt = T - S[11]; fr[:] = paper('FF8C1A', .7); rays(fr, T, 'FFFFFF', .14)
    overlay(fr, cairo_layer(lambda c: (store(c, 230, 1060, .7, True), store(c, 850, 1060, .7, True), rhand(c, CX, 1080 + 20 * math.sin(T * 5), .8, .5))))
    def rope(c):
        c.move_to(330, 1060); c.curve_to(420, 1000 + 30 * math.sin(T * 6), 640, 1120, 750, 1060); c.set_source_rgba(*hx('C8A27A')); c.set_line_width(16); c.stroke()
    overlay(fr, cairo_layer(rope))
    tape(fr, 'THE NEXT SHOPPING WAR', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    tw = wfind(11, 'your ai')
    if T > tw: title(fr, 'IS FOR YOUR AI', 600, T - tw, size=110, fill=YEL)

def s_end(fr, T):
    lt = T - S[12]; fr[:] = paper(GREEN, .62); rays(fr, T, 'FFFFFF', .12)
    sk(fr, WAL, CX, 1050, T, 9, 1.0, -4)
    title(fr, 'LET AI SHOP FOR YOU?', 560, lt, size=92, fill=YEL)
    if T > S[13]:
        burst(fr, 'YES', 250, 1250, T - S[13], r=110, col=BLUE, size=56, rot=-8)
        burst(fr, 'NO', 830, 1250, T - S[13] - .15, r=110, col=RED, size=56, rot=8)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_question), (S[3], s_launch), (S[4], s_buys), (S[5], s_token), (S[6], s_bio), (S[7], s_twist), (S[8], s_block),
           (S[9], s_tiny), (S[10], s_next), (S[11], s_choose), (S[12], s_war), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(3, 'buys') + .3, wfind(7, 'blocking'), wfind(8, 'tiny'), wfind(11, 'your ai')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Photos: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
