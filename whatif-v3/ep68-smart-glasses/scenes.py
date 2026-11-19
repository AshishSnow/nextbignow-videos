import sys, os, json, math
sys.path.insert(0, '/home/claude/glasses')
from kit import *
D = '/home/claude/glasses'
L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + 0.3; TOTAL = END + 2.6
def wt(i, frac): return S[i] + L[i]['dur'] * frac          # time inside line i at char fraction
def wfind(i, word):
    tx = L[i]['text'].lower(); k = tx.find(word.lower()); return wt(i, k / max(1, len(tx)))
def ex(name):
    return os.path.exists(f'{D}/st/{name}.png')
G = load_st('glasses', w=760); GG = load_st('gglass', w=620); SELF = load_st('selfie', h=900)
HP = load_st('handphone', w=820); CR = load_st('crack', w=520); LD = load_st('lookdown', h=760)
PHOTO = {}
def photo(name, w, h, focus=(.5, .5)):
    k = (name, w, h, focus)
    if k not in PHOTO:
        p = f'{D}/ph/{name}.jpg'
        PHOTO[k] = panel_img(comic_photo(p, w, h, focus)) if os.path.exists(p) else None
    return PHOTO[k]

def phone_draw(c, x, y, s, rot=0, glow=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.save(); c.translate(14, 16); c.rectangle(-130, -260, 260, 520); c.restore(); c.set_source_rgba(*hx('1C1614')); c.fill()
    def rr(x0, y0, w, h, r):
        c.new_path(); c.arc(x0 + w - r, y0 + r, r, -math.pi / 2, 0); c.arc(x0 + w - r, y0 + h - r, r, 0, math.pi / 2); c.arc(x0 + r, y0 + h - r, r, math.pi / 2, math.pi); c.arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi); c.close_path()
    rr(-130, -260, 260, 520, 36); c.set_source_rgba(*hx('2A2F3A')); c.fill_preserve(); ink(c, 9); c.stroke()
    rr(-112, -236, 224, 472, 22); c.set_source_rgba(*hx('6FC3FF', glow)); c.fill()
    for k in range(4):
        rr(-92, -200 + k * 105, 184, 80, 14); c.set_source_rgba(1, 1, 1, .75 * glow); c.fill()
    c.restore()

def hand(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-150, 420); c.curve_to(-170, 200, -140, 80, -60, 40); c.line_to(120, 60); c.curve_to(170, 120, 170, 300, 150, 420); c.close_path()
    c.set_source_rgba(*hx('F2B48C')); c.fill_preserve(); ink(c, 8); c.stroke()
    for k in range(3):
        c.move_to(150, -80 + k * 70); c.curve_to(210, -80 + k * 70, 210, -30 + k * 70, 150, -20 + k * 70); c.set_source_rgba(*hx('F2B48C')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.move_to(-150, -20); c.curve_to(-210, 40, -190, 120, -130, 120); c.set_source_rgba(*hx('F2B48C')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.restore()

def lens_mask_draw(c, cx, cy, w, h, col='1C1614', lw=34):
    """big glasses frame (two lenses) drawn as thick ink frame."""
    for sx in (-1, 1):
        x = cx + sx * (w * .26); c.save(); c.translate(x, cy); c.scale(w * .24, h * .5)
        c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx(col)); c.set_line_width(lw); c.stroke()
    c.move_to(cx - w * .04, cy - h * .14); c.curve_to(cx - w * .01, cy - h * .24, cx + w * .01, cy - h * .24, cx + w * .04, cy - h * .14); c.set_line_width(lw * .8); c.stroke()

def chip(fr, txt, cx, cy, t, col=CYAN, size=40, rot=0):
    tape(fr, txt, cx, cy, t, col=col, size=size, font=INTER, rot=rot)

def subs(fr, T):
    """small paper-strip subtitle, 2-4 words, current word highlighted."""
    for i, l in enumerate(L):
        if S[i] - .05 <= T < E[i] + .12:
            words = l['text'].split(); n = len(words); tx = l['text']
            pos = []; p = 0
            for w_ in words: k = tx.find(w_, p); pos.append(k / len(tx)); p = k + len(w_)
            cur = max([j for j in range(n) if wt(i, pos[j]) <= T] or [0])
            g0 = (cur // 3) * 3; grp = words[g0:g0 + 3]
            f = ImageFont.truetype(INTER, 34); f.set_variation_by_name('Bold')
            txt = ' '.join(grp).upper(); bb = f.getbbox(txt); w = bb[2] - bb[0] + 70; h = 64
            im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.rectangle((8, 8, w + 8, h + 8), fill=INK + (160,)); d.rectangle((0, 0, w, h), fill=CREAM + (250,), outline=INK + (255,), width=3)
            d.ellipse((14, h / 2 - 8, 30, h / 2 + 8), fill=rgb(RED))
            x = 44
            for j, w_ in enumerate(grp):
                ww = f.getbbox(w_.upper() + ' ')[2]
                if g0 + j == cur: d.rectangle((x - 4, 12, x + f.getbbox(w_.upper())[2] + 4, h - 12), fill=rgb(YEL))
                d.text((x, h / 2), w_.upper(), font=f, fill=INK, anchor='lm'); x += ww
            put_rgba(fr, np.array(im), CX, 1440, 1.0, 1.0, -1.2)
            return

def credit(fr, txt):
    f = ImageFont.truetype(INTER, 18); bb = f.getbbox(txt); im = Image.new('RGBA', (bb[2] + 10, bb[3] + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4, 2), txt, font=f, fill=INK + (170,)); put_rgba(fr, np.array(im), 74, 980, 1.0, 1.0, 90)

LOGO = None
def logo(fr):
    global LOGO
    if LOGO is None:
        p = '/home/claude/nextbignow-videos/NextBigNow_logo_transparent.png'
        im = Image.open(p).convert('RGBA'); im.thumbnail((150, 150)); LOGO = np.array(im)
    put_rgba(fr, LOGO, W - 200, 330, 1.0, .95, 0)

# ------------------------------------------------------------------ scenes
def s_hook(fr, T):
    fr[:] = paper(RED, .78); rays(fr, T, 'FFFFFF', .10, cy=1000)
    tg = S[1] + .1; k = clamp((T - tg) / .35)
    dx = -1000 * eout(k)
    sticker(fr, HP, CX + 40 + dx, 1060 - 260 * math.sin(k * math.pi), T, 0, 1.0, -8 - 40 * eout(k))
    if T > tg - .2:
        y = lerp(-400, 930, back(clamp((T - tg + .2) / .35)))
        sticker(fr, G, CX, y, T, 0, 1.0, -6)
    if T > tg + .25: burst(fr, 'BYE!', 260, 1180, T - tg - .25, r=120, col=YEL, size=70, rot=-10)
    tape(fr, 'YOUR PHONE IS ABOUT TO', CX, 470, 1.0, col='FFFFFF', size=50, font=LUCKY, rot=-2)
    title(fr, 'GET REPLACED?!', 600, 1.0, size=130, fill=YEL, rot=-3)

def s_pov(fr, T, t0, mode):
    fr[:] = paper(BLUE, .7)
    ph = photo('street', 1000, 700, (.5, .45))
    lt = T - t0
    if ph is not None: put_rgba(fr, ph, CX, 1010, 1.0 + .03 * lt, 1.0, 0)
    def dr(c):
        lens_mask_draw(c, CX, 1010, 1060, 520)
        if mode == 'dir':
            p = eout((lt - .3) / .6)
            c.save(); c.translate(CX + 40, 1130); c.scale(1, .45)
            c.move_to(-60, 120); c.line_to(-60, -40 * p); c.line_to(-140, -40 * p); c.line_to(0, -220 * p); c.line_to(140, -40 * p); c.line_to(60, -40 * p); c.line_to(60, 120); c.close_path()
            c.set_source_rgba(*hx(CYAN, .9)); c.fill_preserve(); ink(c, 8); c.stroke(); c.restore()
    overlay(fr, cairo_layer(dr))
    if mode == 'intro':
        chip(fr, 'MSG: running late', 330, 820, lt - .6, YEL, 34, -2)
        chip(fr, '72°F  SUNNY', 760, 800, lt - 1.0, 'FFFFFF', 34, 2)
        chip(fr, 'TURN RIGHT  >', 740, 1110, lt - 1.4, CYAN, 36, -1)
        tape(fr, 'WHAT IF YOUR SCREEN', CX, 470, lt, col='FFFFFF', size=48, font=LUCKY, rot=-2)
        title(fr, 'WAS HERE?', 590, lt - .15, size=120, fill=YEL)
    if mode == 'dir':
        chip(fr, 'TURN RIGHT  300 FT', CX, 800, lt - .7, CYAN, 40, -2)
        tape(fr, 'DIRECTIONS', CX, 500, lt, col=YEL, size=56, font=LUCKY, rot=-2)
        title(fr, 'ON THE STREET', 620, lt - .15, size=100, fill='FFFFFF')
    credit(fr, 'Photo: Wikimedia Commons (see description)')

def s_chart(fr, T):
    fr[:] = paper(None); rays(fr, T, YEL, .18, cy=1150)
    bars = [('LAST YEAR', 6, wfind(4, 'six'), GREY if False else '9AA5B1'), ('THIS YEAR', 20, wfind(5, 'twenty'), BLUE), ('2030', 75, wfind(7, 'seventy'), RED)]
    base = 1250; x0 = 230
    def dr(c):
        ink(c, 8); c.move_to(120, base); c.line_to(980, base); c.stroke()
        for j, (lab, v, tg, col) in enumerate(bars):
            p = eout((T - tg + .1) / .7); h = 560 * v / 75 * p; x = x0 + j * 300
            c.rectangle(x - 90 + 12, base - h + 14, 180, h); c.set_source_rgba(*hx('1C1614')); c.fill()
            c.rectangle(x - 90, base - h, 180, h); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    overlay(fr, cairo_layer(dr))
    for j, (lab, v, tg, col) in enumerate(bars):
        p = eout((T - tg + .1) / .7); x = x0 + j * 300; h = 560 * v / 75 * p
        if T > tg - .1:
            title(fr, f'{v}M', base - h - (60 if j < 2 or T < wfind(7, 'seventy') + .5 else 60), T - tg + .1, size=86, fill='FFFFFF', rot=0, cx=x)
            tape(fr, lab, x, base + 60, T - tg + .1, col=YEL if j < 2 else RED, size=34, font=ELITE, rot=-2, tcol='1C1614' if j < 2 else 'FFFFFF')
    t75 = wfind(7, 'seventy')
    if T > t75 + .5: sticker(fr, GG, 600, 700, T, 1, .36, -8, T - t75 - .5)
    if T > S[3]: tape(fr, 'SMART GLASSES SOLD', CX, 470, T - S[3], col='FFFFFF', size=46, font=LUCKY, rot=-2)
    if T > wfind(7, 'seventy') + .4: burst(fr, 'BOOM!', 300, 720, T - wfind(7, 'seventy') - .4, r=110, col=RED, size=58)

def s_specs(fr, T):
    fr[:] = paper(CYAN, .55); rays(fr, T, 'FFFFFF', .14, cy=960)
    tg = S[8]; sticker(fr, G, CX, 1000, T, 2, .95, -4, T - tg)
    cam = wfind(8, 'camera'); ai = wfind(8, 'google'); bat = wfind(8, 'nine')
    def dr(c):
        for (tt, x0, y0, x1, y1) in ((cam, 420, 960, 300, 800), (ai, 640, 930, 780, 800), (bat, 820, 1040, 800, 1220)):
            p = eout((T - tt) / .3)
            if p > 0: ink(c, 7); c.move_to(x0, y0); c.line_to(lerp(x0, x1, p), lerp(y0, y1, p)); c.stroke()
    overlay(fr, cairo_layer(dr))
    chip(fr, 'CAMERA', 300, 770, T - cam - .2, YEL, 44, -3)
    chip(fr, "GOOGLE'S AI BUILT IN", 700, 770, T - ai - .2, 'FFFFFF', 40, 2)
    chip(fr, 'UP TO 9 HRS BATTERY', 700, 1260, T - bat - .2, GREEN, 40, -2)
    tape(fr, "SAMSUNG'S PAIR", CX, 470, T - tg, col=RED, size=56, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'IS ABOUT TO DROP', 580, T - tg - .15, size=88, fill=YEL)
    if T > S[9]:
        def dr2(c):
            p = back(clamp((T - S[9]) / .35))
            c.save(); c.translate(CX, 1160); c.scale(p, p); c.rotate(-.05)
            c.rectangle(-300 + 12, -60 + 14, 600, 120); c.set_source_rgba(*hx('1C1614')); c.fill()
            c.rectangle(-300, -60, 600, 120); c.set_source_rgba(*hx('FFFFFF')); c.fill_preserve(); ink(c, 7); c.stroke(); c.restore()
        overlay(fr, cairo_layer(dr2))
        put_rgba(fr, ttext("APPLE'S PAIR: NEXT", 56, LUCKY, RED, shadow=False), CX, 1160, back(clamp((T - S[9]) / .35)), 1.0, -3)

def s_translate(fr, T):
    fr[:] = paper(PINK, .6)
    ph = photo('people', 1000, 700, (.5, .4)); lt = T - S[12]
    if ph is not None: put_rgba(fr, ph, CX, 1010, 1.0 + .03 * lt, 1.0, 0)
    overlay(fr, cairo_layer(lambda c: lens_mask_draw(c, CX, 1010, 1060, 520)))
    tape(fr, '¿DÓNDE ESTÁ LA ESTACIÓN?', CX, 560, lt, col='FFFFFF', size=46, font=INTER, rot=-2)
    tg = S[13]
    if T > tg:
        chip(fr, "WHERE'S THE STATION?", CX, 1100, T - tg, YEL, 46, -1)
        burst(fr, 'LIVE', 870, 1250, T - tg - .3, r=90, col=RED, size=48)
    tape(fr, 'LIVE TRANSLATION', CX, 440, lt, col=RED, size=52, font=LUCKY, rot=-2, tcol='FFFFFF')

def s_texts(fr, T):
    fr[:] = paper(GREEN, .55); lt = T - S[14]
    ph = photo('street', 1000, 700, (.3, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1010, 1.04 + .02 * lt, 1.0, 0)
    overlay(fr, cairo_layer(lambda c: lens_mask_draw(c, CX, 1010, 1060, 520)))
    for k, (txt, col) in enumerate((('MOM: dinner at 7?', 'FFFFFF'), ('JAKE: u up?', YEL), ('ORDER ARRIVING', CYAN))):
        chip(fr, txt, 330, 790 + k * 80, lt - .2 - k * .35, col, 32, -1)
    tg = S[15]
    if T > tg:
        sticker(fr, LD, 800, 1130, T, 6, .55, 4, T - tg); xstamp(fr, 800, 1080, T - tg - .4, .8)
        title(fr, 'NO PHONE.', 470, T - tg, size=100, fill='FFFFFF')
        title(fr, 'NO LOOKING DOWN.', 590, T - wfind(15, 'no looking'), size=88, fill=YEL)

def xstamp(fr, cx, cy, t, s=1.0):
    if t <= 0: return
    p = back(clamp(t / .25))
    def dr(c):
        c.save(); c.translate(cx, cy); c.scale(p * s, p * s)
        for a in (1, -1):
            c.move_to(-120, -120 * a); c.line_to(120, 120 * a); c.set_source_rgba(*hx('1C1614')); c.set_line_width(46); c.stroke()
            c.move_to(-120, -120 * a); c.line_to(120, 120 * a); c.set_source_rgba(*hx(RED)); c.set_line_width(30); c.stroke()
        c.restore()
    overlay(fr, cairo_layer(dr))

def s_losers(fr, T):
    fr[:] = paper(YEL, .6); rays(fr, T, 'FFFFFF', .12)
    tc = wfind(17, 'phone cases'); tr = wfind(17, 'screen'); ts = wfind(18, 'selfie')
    a = photo('cases', 430, 520); b = None
    if a is not None and T > tc - .1: put_rgba(fr, a, 300, 860, back(clamp((T - tc + .1) / .3)), 1.0, -4)
    if b is not None and T > tr - .1: put_rgba(fr, b, 780, 900, back(clamp((T - tr + .1) / .3)), 1.0, 3)
    if T > tr - .1: sticker(fr, CR, 780, 900, T, 5, .9, 8, T - tr + .1)
    tape(fr, 'PHONE CASES', 300, 1150, T - tc, col='FFFFFF', size=40, font=LUCKY, rot=-3)
    tape(fr, 'REPAIR SHOPS', 780, 1190, T - tr, col='FFFFFF', size=40, font=LUCKY, rot=2)
    xstamp(fr, 300, 860, T - tc - .5); xstamp(fr, 780, 900, T - tr - .5)
    if T > ts - .1:
        sticker(fr, SELF, CX, 1000, T, 3, .9, 12, T - ts + .1); xstamp(fr, CX, 900, T - ts - .7, 1.2)
    tape(fr, 'WHO LOSES?', CX, 470, T - S[16], col=RED, size=70, font=LUCKY, rot=-2, tcol='FFFFFF')

def s_proof(fr, T):
    fr[:] = paper(None); rays(fr, T, RED, .10)
    lt = T - S[19]; ph = photo('wearer', 760, 760, (.5, .35))
    if ph is not None and T > S[20] - .1: put_rgba(fr, ph, CX, 1010, back(clamp((T - S[20] + .1) / .35)), 1.0, -3)
    tape(fr, "STILL THINK IT'S HYPE?", CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    tm = wfind(20, 'millions')
    if T > tm: burst(fr, 'MILLIONS SOLD', 780, 700, T - tm, r=170, col=RED, size=46, rot=6)
    tn = wfind(20, 'normal')
    if T > tn: chip(fr, 'LOOKS LIKE NORMAL SUNGLASSES', CX, 1440 - 140, T - tn, YEL, 34, -1)

def s_end(fr, T):
    fr[:] = paper(RED, .78); rays(fr, T, 'FFFFFF', .1)
    lt = T - S[21]
    sticker(fr, HP, 300, 1000, T, 7, .6, -6)
    sticker(fr, G, 790, 1000, T, 4, .55, 6)
    burst(fr, 'VS', CX, 1000, lt - .2, r=100, col=YEL, size=70)
    tape(fr, 'WOULD YOU TRADE', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    title(fr, 'YOUR PHONE?', 590, lt - .15, size=110, fill=YEL)
    if T > S[22]: chip(fr, 'COMMENT  YES  OR  NO', CX, 1250, T - S[22], 'FFFFFF', 46, -2)

def s_cta(fr, T, plat):
    fr[:] = paper(None); rays(fr, T, RED, .14); lt = T - END
    if LOGO is None: logo(np.zeros_like(fr))
    big = Image.open('/home/claude/nextbignow-videos/NextBigNow_logo_transparent.png').convert('RGBA'); big.thumbnail((420, 420))
    put_rgba(fr, np.array(big), CX, 860, back(clamp(lt / .4)), 1.0, -4 * math.sin(T))
    if plat == 'ig':
        tape(fr, 'SEND THIS TO SOMEONE', CX, 1170, lt - .3, col=YEL, size=50, font=LUCKY, rot=-2)
        tape(fr, 'GLUED TO THEIR PHONE', CX, 1260, lt - .5, col='FFFFFF', size=46, font=LUCKY, rot=2)
    else:
        tape(fr, 'SUBSCRIBE', CX, 1170, lt - .3, col=RED, size=70, font=LUCKY, rot=-2, tcol='FFFFFF')
        tape(fr, 'FOR WHAT HAPPENS NEXT', CX, 1270, lt - .5, col=YEL, size=44, font=LUCKY, rot=2)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    if T < S[2]: s_hook(fr, T)
    elif T < S[3]: s_pov(fr, T, S[2], 'intro')
    elif T < S[8]: s_chart(fr, T)
    elif T < S[10]: s_specs(fr, T)
    elif T < S[12]:
        if T < S[11]:
            s_pov(fr, T, S[10], 'intro')
        else: s_pov(fr, T, S[11], 'dir')
    elif T < S[14]: s_translate(fr, T)
    elif T < S[16]: s_texts(fr, T)
    elif T < S[19]: s_losers(fr, T)
    elif T < S[21]: s_proof(fr, T)
    elif T < END: s_end(fr, T)
    else: s_cta(fr, T, plat); return fr
    dx, dy = 0, 0
    for at in (S[1] + .35, wfind(7, 'seventy') + .4, wfind(17, 'phone cases') + .5, wfind(18, 'selfie') + .7):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for a in sys.argv[2:]:
            t = float(a); Image.fromarray(frame(t)).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
