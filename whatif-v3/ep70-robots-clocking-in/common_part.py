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
LOGO = None
def logo(fr):
    global LOGO
    if LOGO is None:
        p = '/home/claude/nextbignow-videos/NextBigNow_logo_transparent.png'
        im = Image.open(p).convert('RGBA'); im.thumbnail((150, 150)); LOGO = np.array(im)
    put_rgba(fr, LOGO, W - 200, 330, 1.0, .95, 0)

# ------------------------------------------------------------------ scenes
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

def s_cta(fr, T, plat):
    fr[:] = paper(None); rays(fr, T, RED, .14); lt = T - END
    if LOGO is None: logo(np.zeros_like(fr))
    big = Image.open('/home/claude/nextbignow-videos/NextBigNow_logo_transparent.png').convert('RGBA'); big.thumbnail((420, 420))
    put_rgba(fr, np.array(big), CX, 860, back(clamp(lt / .4)), 1.0, -4 * math.sin(T))
    if plat == 'ig':
        tape(fr, 'SEND THIS TO SOMEONE', CX, 1170, lt - .3, col=YEL, size=50, font=LUCKY, rot=-2)
        tape(fr, 'WHO HATES THEIR SHIFT', CX, 1260, lt - .5, col='FFFFFF', size=46, font=LUCKY, rot=2)
    else:
        tape(fr, 'SUBSCRIBE', CX, 1170, lt - .3, col=RED, size=70, font=LUCKY, rot=-2, tcol='FFFFFF')
        tape(fr, 'FOR WHAT HAPPENS NEXT', CX, 1270, lt - .5, col=YEL, size=44, font=LUCKY, rot=2)

