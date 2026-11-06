"""What if you couldn't stop sneezing? — episode 36 (Donna Griffiths 26 Jul 1981 - 16 Sep 1983; Dundee windpipe case, BMJ 2023)."""
import sys, os, math, re
import skia
from sneezeprops import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('SN_DIR', 'sneeze'))
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]


def ph(text, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z']+", text.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j] for j in range(len(q))):
            return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text)


END = WT[-1][2] + 0.45
DURATION = END + 2.3
TY = 650
WT_ = (255, 255, 255); SM = (255, 240, 220)


def top_shade(c, a=0.45, col=(20, 10, 40)):
    c.drawRect(R.MakeLTRB(0, 0, W, 860), paint(shader=lin(0, 250, 0, 860, [argb(col, a), argb(col, 0)])))


def tier(c, t, t0, small, big, col=WT_, t1=None, size=250, y=TY, small_col=SM):
    two_tier(c, t, t0, small, big, y=y, big_size=size, big_col=col, small_col=small_col, shadow=True, t1=t1)


def pill(c, x, y, txt, k, col=RED, size=54, txt_col=(255, 255, 255)):
    if k <= 0: return
    kk = eback(min(1, k), 1.6)
    f = font('ant', size); w = f.measureText(txt) + size * 0.9; h = size * 1.45
    c.save(); c.translate(x, y); c.scale(kk, kk)
    c.drawRoundRect(R.MakeXYWH(-w / 2 + 4, -h / 2 + 8, w, h), h / 2, h / 2, paint((0, 0, 0), 0.3, blur=6))
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2, paint(col)); c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2, stroke(INK, 6))
    c.drawString(txt, -f.measureText(txt) / 2, size * 0.36, f, paint(txt_col))
    c.restore()


def room(c, t, wall=(120, 90, 220), floor=(250, 200, 120), fy=1500):
    set_bg(c, wall, tuple(min(255, v + 50) for v in wall), spot=True, t=t)
    c.drawRect(R.MakeLTRB(0, fy, W, H), paint(floor)); c.drawLine(0, fy, W, fy, stroke(INK, 8))
    for i in range(5):
        c.drawLine(-100 + i * 300, fy, -300 + i * 420, H, stroke(tuple(int(v * 0.85) for v in floor), 6))


def strike(c, x, y, w, k):
    if k <= 0: return
    c.drawLine(x - w / 2, y + 30, x - w / 2 + w * eo(k), y + 30 - 120 * eo(k), stroke(RED, 22))


# ================================================================== intro
def sc_hook(c, t, S):
    tn = ph('not for a minute'); tw = ph('two and a half'); tg = ph('twelve year old')
    room(c, t, (255, 120, 90), (255, 220, 150))
    n_sn = 0
    for i in range(20):
        if t > 0.5 + i * 1.5 + 0.6: n_sn += 1
    tissue_pile(c, 760, 1530, min(18, 2 + n_sn * 2), seed=3)
    tissue_box(c, 250, 1520, 1.0, t)
    t0 = 0.5 + 1.5 * int(max(0, t - 0.5) / 1.5)
    sneezer(c, 520, 1500, 1.9, t, t0, who='mascot', word='ACHOO!' if (int(max(0, t - 0.5) / 1.5) % 2 == 0) else 'CHOO!')
    top_shade(c, 0.5, (120, 30, 20))
    tier(c, t, 0.0, "what if you couldn't", 'STOP SNEEZING?', YEL, size=230, t1=tn - 0.25)
    tier(c, t, tn - 0.15, 'not for a minute. for', '2.5 YEARS', WT_, size=270, t1=tg - 0.3)
    tier(c, t, tg - 0.2, 'it happened to a', '12-YEAR-OLD GIRL', YEL, size=190)


def sc_donna(c, t, S):
    ts = ph('she sneezed'); ta = ph('then again'); tb = ph('and again')
    room(c, t, (90, 170, 250), (255, 230, 170))
    calendar(c, 820, 1080, 0.6, 'JULY', '1981')
    if t < ts:
        donna(c, 470, 1500, 1.9, POSES['wave'], Face('happy', 'grin'), t)
    else:
        tt = ts if t < ta else (ta if t < tb else tb)
        sneezer(c, 470, 1500, 1.9, t, tt - 0.45, who='donna')
    top_shade(c, 0.4, (20, 40, 90))
    tier(c, t, ph('her name was') - 0.1, 'her name was', 'DONNA GRIFFITHS', WT_, size=170)


def sc_million(c, t, S):
    u = t - S['t0']; tm = ph('a million')
    set_bg(c, (40, 20, 90), (110, 50, 190), circle=(160, 90, 240), cy=1150, r=440, spot=True, t=t)
    k = eio(pr(t, S['t0'] + 0.3, max(0.6, tm - S['t0'] + 0.3)))
    n = 1000000 * k
    counter(c, 540, 1120, 0.95, round(n, -3) if k < 1 else 1000000, t, col=YEL, label='SNEEZES')
    for i in range(10):
        ph_ = (t * 0.7 + i / 10) % 1
        tissue_pile(c, 120 + i * 95, 1450 + 300 * ph_, 1, seed=i)
    sneezer(c, 800, 1490, 0.9, t, S['t0'] + 0.1, who='donna', period=1.4)
    top_shade(c, 0.4)
    tier(c, t, S['t0'] + 0.1, 'in just the first year', 'ABOUT A MILLION', YEL, size=210)


def sc_perday(c, t, S):
    tsoup = ph('try eating soup'); thw = ph('try doing homework'); ths = ph('try hiding')
    if t < tsoup - 0.1:
        set_bg(c, (255, 180, 60), (255, 220, 140), circle=(255, 240, 200), cy=1150, r=420, spot=True, t=t)
        # clock with ticking hand and two sneeze marks per lap
        c.save(); c.translate(0, 120); c.translate(540, 1150); c.scale(0.9, 0.9); c.translate(-540, -1150)
        c.drawCircle(540, 1150, 300, paint((255, 255, 255))); c.drawCircle(540, 1150, 300, stroke(INK, 12))
        for i in range(12):
            a = i / 12 * 6.283
            c.drawLine(540 + math.sin(a) * 250, 1150 - math.cos(a) * 250, 540 + math.sin(a) * 280, 1150 - math.cos(a) * 280, stroke(INK, 8))
        a = (t - S['t0']) * 6.283 / 3.0
        c.drawLine(540, 1150, 540 + math.sin(a) * 240, 1150 - math.cos(a) * 240, stroke(RED, 12)); c.drawCircle(540, 1150, 20, paint(INK))
        for j, aa in enumerate((0.0, 3.14)):
            hit = ((a - aa) % 6.283) < 0.9
            c.save(); c.translate(540 + math.sin(aa) * 390, 1150 - math.cos(aa) * 390)
            s_ = 1.25 if hit else 1.0; c.scale(s_, s_)
            f = font('ant', 70); c.drawString('ACHOO', -f.measureText('ACHOO') / 2, 25, f, stroke(INK, 10)); c.drawString('ACHOO', -f.measureText('ACHOO') / 2, 25, f, paint(YEL if hit else (255, 255, 255)))
            c.restore()
        c.restore()
        top_shade(c, 0.25, (120, 50, 0))
        tier(c, t, S['t0'] + 0.1, 'day and night, about', '2 EVERY MINUTE', INK, size=200, small_col=INK)
        return
    if t < thw - 0.1:
        room(c, t, (60, 190, 160), (255, 220, 160), fy=1550)
        c.drawRect(R.MakeXYWH(150, 1330, 780, 40), paint((180, 110, 60))); c.drawRect(R.MakeXYWH(150, 1330, 780, 40), stroke(INK, 6))
        kb = sneezer(c, 330, 1550, 1.6, t, tsoup + 0.3, who='donna', base=POSES['hold'], word='')
        soup(c, 690, 1320, 0.9, t, splash=kb)
        top_shade(c, 0.3, (0, 60, 50))
        tier(c, t, tsoup - 0.05, 'now try eating', 'SOUP', WT_, size=280)
        return
    if t < ths - 0.1:
        room(c, t, (90, 130, 240), (255, 220, 160), fy=1550)
        c.drawRect(R.MakeXYWH(150, 1330, 780, 40), paint((180, 110, 60))); c.drawRect(R.MakeXYWH(150, 1330, 780, 40), stroke(INK, 6))
        kb = sneezer(c, 330, 1550, 1.6, t, thw + 0.25, who='donna', base=POSES['hold'], word='')
        homework(c, 690, 1230, 0.9, -6, k_fly=eo(kb))
        top_shade(c, 0.3, (0, 30, 90))
        tier(c, t, thw - 0.05, 'or doing', 'HOMEWORK', WT_, size=260)
        return
    room(c, t, (240, 110, 150), (255, 230, 170), fy=1560)
    kb = sneezer(c, 640, 1560, 1.25, t, ph('hide and seek') + 0.1, who='donna', base=POSES['crouch'], word='ACHOO!')
    sofa(c, 470, 1580, 1.2)
    draw_stick(c, 180, 1560, 1.25, POSES['shock'] if kb > 0 else POSES['stand'], Face('closed' if kb <= 0 else 'happy', 'grin' if kb > 0 else 'smile'), t=t, scarf=TEAL)
    if kb > 0:
        f = font('ant', 90); s_ = 'FOUND YOU!'
        c.drawString(s_, 300 - f.measureText(s_) / 2 + 60, 1050, f, stroke(INK, 12)); c.drawString(s_, 300 - f.measureText(s_) / 2 + 60, 1050, f, paint(MINT))
    top_shade(c, 0.3, (90, 0, 40))
    tier(c, t, ths - 0.05, 'or playing', 'HIDE AND SEEK', WT_, size=210)


# ================================================================== how a sneeze works
def sc_what(c, t, S):
    tt = ph('something tickles'); tn = ph('a nerve fires'); te = ph('everybody out')
    set_bg(c, (30, 160, 200), (120, 220, 240), circle=(200, 245, 255), cy=1200, r=470, spot=True, t=t)
    head_section(c, 470, 1250, 1.05, t, tickle=pr(t, tt, 0.8), signal=pr(t, tn - 0.1, 1.2), alarm=pr(t, te - 0.3, 0.3))
    speech(c, 560, 920, 620, 150, 'EVERYBODY OUT!', pr(t, te - 0.1, 0.35), size=86, col=RED)
    top_shade(c, 0.35, (0, 50, 80))
    tier(c, t, S['t0'] + 0.1, 'okay, so what is a', 'SNEEZE?', WT_, size=290, t1=te - 0.4)


def sc_body(c, t, S):
    te = ph('your eyes snap'); tb = ph('you suck in'); ts = ph('slam it out'); to = ph('once it starts')
    set_bg(c, (255, 110, 80), (255, 190, 120), circle=(255, 230, 190), cy=1150, r=440, spot=True, t=t)
    if t < tb:
        donna(c, 540, 1520, 2.0, POSES['stand'], Face('closed', 'flat', 'angry'), t)
        pill(c, 540, 1610, 'EYES SHUT', pr(t, te, 0.3), col=PURP, size=56)
    elif t < ts:
        k = eo(pr(t, tb, 0.8))
        donna(c, 540, 1520, 2.0, lerp_pose(POSES['stand'], P_PRE, k), Face('closed', 'o', 'up'), t, squash=1 + 0.06 * k)
        for i in range(5):
            ph_ = (t * 1.5 + i / 5) % 1
            c.drawLine(320 + ph_ * 160, 1010 + i * 20, 360 + ph_ * 160, 1010 + i * 20, stroke((255, 255, 255), 8, 1 - ph_))
        pill(c, 540, 1610, 'BIG BREATH IN', pr(t, tb, 0.3), col=BLUE, size=56)
    else:
        sneezer(c, 420, 1520, 2.0, t, ts - 0.55, who='donna', word='ACHOO!')
        pill(c, 540, 1610, 'BLAST!', pr(t, ts, 0.3), col=RED, size=56)
    top_shade(c, 0.3, (120, 30, 0))
    tier(c, t, to - 0.1, 'once it starts,', "YOU CAN'T STOP IT", WT_, size=200)


def sc_speed(c, t, S):
    tn = ph('yeah no'); t16 = ph('about sixteen'); tj = ph("that's a jogger")
    if t < tj - 0.1:
        set_bg(c, (30, 40, 90), (70, 90, 180), circle=(110, 130, 230), cy=1250, r=440, spot=True, t=t)
        k = 0.95 if t < t16 else lerp(0.95, 0.12, eo(pr(t, t16, 0.8)))
        gauge(c, 540, 1350, 330, k, t)
        lbl = '160 KM/H?' if t < t16 else '16 KM/H'
        f = font('ant', 120); c.drawString(lbl, 540 - f.measureText(lbl) / 2, 1520, f, stroke(INK, 14)); c.drawString(lbl, 540 - f.measureText(lbl) / 2, 1520, f, paint(YEL if t < t16 else MINT))
        if t < t16: strike(c, 540, 1480, 520, pr(t, tn, 0.35))
        top_shade(c, 0.4)
        tier(c, t, S['t0'] + 0.1, 'a sneeze flies at', '160 KM/H?', WT_, size=250, t1=t16 - 0.3)
        tier(c, t, t16 - 0.2, 'real top speed: about', '16 KM/H', MINT, size=270)
        return
    set_bg(c, (120, 210, 255), (210, 240, 255), spot=False, t=t)
    c.drawRect(R.MakeLTRB(0, 1450, W, H), paint((90, 90, 100))); c.drawLine(0, 1450, W, 1450, stroke(INK, 8))
    for i in range(6):
        x = (i * 240 - t * 300) % 1300 - 100
        c.drawRect(R.MakeXYWH(x, 1560, 120, 18), paint((255, 255, 255)))
    jogger(c, 360, 1450, 1.6, t)
    pill(c, 360, 1620, 'SNEEZE', 1, col=BLUE, size=50)
    race_car(c, 800, 1440, 0.75, t)
    cross_icon(c, 800, 1300, 1.2 * eback(pr(t, ph('not a race car') - 0.1, 0.3), 1.6))
    top_shade(c, 0.25, (0, 60, 120))
    tier(c, t, tj - 0.05, "that's a", 'JOGGER', INK, size=290, small_col=INK)


def sc_drops(c, t, S):
    tc = ph('little cloud'); tr = ph('right across'); tm = ph('your mom was right')
    room(c, t, (130, 100, 230), (255, 220, 160))
    if t < tm - 0.1:
        sneezer(c, 220, 1500, 1.4, t, S['t0'] + 0.1, who='mascot', word='')
        k = eo(pr(t, S['t0'] + 0.8, max(1.0, tr - S['t0'] + 0.6)))
        droplet_cloud(c, 380 + 300 * k, 1150, k, t, spread=1.0)
        draw_stick(c, 860, 1500, 1.3, POSES['shock'] if t > tr else POSES['stand'], Face('wide', 'o', 'worried') if t > tr else Face('open', 'smile'), t=t, scarf=ORANGE, flip=True)
        top_shade(c, 0.4)
        tier(c, t, tc - 0.4, 'droplets hang like a', 'LITTLE CLOUD', SNOT, size=220)
    else:
        set_bg(c, (60, 200, 120), (150, 240, 180), circle=(220, 255, 230), cy=1150, r=430, spot=True, t=t)
        u = t - (tm + 0.6)
        if u < 0:
            draw_stick(c, 540, 1500, 1.9, POSES['stand'], Face('open', 'smile'), t=t)
        else:
            pose = lerp_pose(POSES['stand'], P_ELBOW, eio(cl(u / 0.3)))
            draw_stick(c, 540, 1500, 1.9, pose, Face('closed', 'flat', 'angry') if u < 1.2 else Face('happy', 'smile'), t=t)
            if 0.3 < u < 1.3:
                f = font('ant', 80); s_ = 'choo!'
                c.drawString(s_, 720, 1000, f, stroke(INK, 10)); c.drawString(s_, 720, 1000, f, paint((255, 255, 255)))
            if u > 1.2:
                check_icon(c, 820, 1150, 1.0 * eback(pr(t, tm + 1.8, 0.3), 1.6))
        top_shade(c, 0.3, (0, 70, 30))
        tier(c, t, tm - 0.05, 'your mom was right:', 'COVER IT', WT_, size=280)


# ================================================================== don't hold it in
def sc_hold(c, t, S):
    td = ph('in two thousand'); tp = ph('pinched his nose')
    if t < td - 0.1:
        set_bg(c, (220, 40, 60), (255, 110, 110), circle=(255, 170, 170), cy=1150, r=430, spot=True, t=t)
        draw_stick(c, 540, 1520, 1.9, P_PINCH, Face('wide', 'puff', 'worried'), t=t, squash=1 + 0.03 * math.sin(t * 8))
        c.drawCircle(540, 1520 - 1.9 * 210 + 30, 0, paint(INK))
        top_shade(c, 0.4, (90, 0, 0))
        tier(c, t, S['t0'] + 0.1, 'whatever you do,', "DON'T HOLD IT IN", WT_, size=200)
        return
    set_bg(c, (120, 200, 255), (220, 240, 255), spot=False, t=t)
    for i in range(4):
        x = (i * 380 - t * 400) % 1500 - 200
        tree(c, x, 1420, 1.0, seed=i, col=(70, 180, 90))
    c.drawRect(R.MakeLTRB(0, 1420, W, H), paint((90, 90, 100)))
    pinch = t > tp - 0.1

    def inner(cc):
        draw_stick(cc, 40, -40, 1.0, P_SIT_PINCH if pinch else P_SIT_DRIVE,
                   Face('wide', 'puff', 'worried') if pinch else (Face('closed', 'o', 'up') if t > ph('a sneeze hit') - 0.2 else Face('open', 'smile')), t=t, scarf=ORANGE)
        cc.drawCircle(160, -190, 50, stroke(INK, 10))
    car_side(c, 520, 1520, 1.15, t, inner=inner)
    calendar(c, 840, 900, 0.5, 'SCOTLAND', '2023')
    top_shade(c, 0.25, (0, 60, 120))
    tier(c, t, td - 0.05, 'a man in Scotland was', 'DRIVING', INK, size=260, small_col=INK, t1=tp - 0.3)
    tier(c, t, tp - 0.2, 'he pinched his nose and', 'CLOSED HIS MOUTH', RED, size=180, small_col=INK)


def sc_tear(c, t, S):
    tt = ph('it tore'); ts = ph('neck swelled')
    set_bg(c, (40, 20, 70), (100, 40, 120), circle=(150, 70, 170), cy=1150, r=440, spot=True, t=t)
    windpipe(c, 540, 1180, 0.95, t, pressure=cl((t - S['t0']) / 0.6), tear=pr(t, tt, 0.5), swell=pr(t, ts, 0.6))
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'the pressure had', 'NOWHERE TO GO', WT_, size=210, t1=tt - 0.3)
    tier(c, t, tt - 0.2, 'it tore a hole in his', 'WINDPIPE', RED, size=280, t1=ph('all to stop') - 0.3)
    tier(c, t, ph('all to stop') - 0.2, 'all to stop', 'ONE SNEEZE', YEL, size=250)


def sc_twenty(c, t, S):
    t20 = ph('more than twenty'); tg = ph('the good news'); t5 = ph('five weeks')
    if t < tg - 0.1:
        set_bg(c, (40, 20, 70), (100, 40, 120), circle=(150, 70, 170), cy=1300, r=440, spot=True, t=t)
        gauge(c, 540, 1380, 330, lerp(0.15, 1.0, eo(pr(t, t20 - 0.2, 0.8))), t)
        pill(c, 540, 1530, '20X A NORMAL SNEEZE', pr(t, t20, 0.35), col=RED, size=60)
        top_shade(c, 0.45)
        tier(c, t, t20 - 0.2, 'holding it in can build', '20X PRESSURE', YEL, size=230)
        return
    set_bg(c, (60, 200, 120), (150, 240, 180), circle=(220, 255, 230), cy=1150, r=430, spot=True, t=t)
    windpipe(c, 380, 1200, 0.75, t, tear=1.0, heal=eo(pr(t, t5 - 0.4, 0.8)))
    calendar(c, 800, 1180, 0.65, 'HEALED IN', '5 WKS')
    top_shade(c, 0.3, (0, 70, 30))
    tier(c, t, tg - 0.05, 'the good news?', 'IT HEALED ITSELF', WT_, size=200)


# ================================================================== weird facts
def sc_facts(c, t, S):
    tsun = ph('step into bright'); tph = ph('photic')
    if t < tsun - 0.1:
        set_bg(c, (255, 80, 160), (255, 160, 200), circle=(255, 220, 240), cy=1150, r=430, spot=True, t=t)
        for i in range(3):
            k = pr(t, S['t0'] + 0.2 + i * 0.25, 0.3)
            card3d(c, 270 + i * 270, 1200, 220, 300, 10 * math.sin(t + i), 0, lambda cc, i=i: cc.drawString('?', -40, 60, font('ant', 200), paint(PURP)), k=k)
        top_shade(c, 0.3, (100, 0, 50))
        tier(c, t, S['t0'] + 0.1, 'sneeze facts that sound fake', 'BUT ARE REAL', WT_, size=220)
        return
    kk = pr(t, tsun, 0.6)
    set_bg(c, (40, 40, 80), (80, 70, 120), spot=False, t=t)
    doorway(c, 640, 1560, 1.6, t, k_sun=0.4 + 0.6 * kk)
    c.drawRect(R.MakeLTRB(0, 1560, W, H), paint((70, 60, 90)))
    sun_icon(c, 640, 980, 90 * kk, t)
    sneezer(c, 420, 1560, 1.6, t, tsun + 0.5, who='mascot', word='ACHOO!')
    top_shade(c, 0.45)
    tier(c, t, tph - 0.2, 'sunlight sneezes are real:', 'PHOTIC SNEEZE', YEL, size=210)


def sc_more(c, t, S):
    tb = ph('stomach gets too full'); ts = ph('almost never'); tw = ph('wake up first')
    if t < tb - 0.5:
        set_bg(c, (255, 170, 60), (255, 220, 140), circle=(255, 240, 200), cy=1150, r=430, spot=True, t=t)
        donna(c, 470, 1520, 1.9, POSES['stand'], Face('closed', 'flat', 'worried'), t)
        tweezers(c, 640, 980, 1.0, t, pluck=pr(t, S['t0'] + 1.0, 0.4))
        kb = sneezer(c, 0, 0, 0.001, t, 99999)
        if t > ph('eyebrows') + 0.2:
            achoo(c, 560, 1050, 1.0, pr(t, ph('eyebrows') + 0.2, 1.0), t, word='ACHOO!')
        top_shade(c, 0.3, (120, 50, 0))
        tier(c, t, S['t0'] + 0.1, 'some people sneeze when they', 'PLUCK EYEBROWS', INK, size=200, small_col=INK)
        return
    if t < ts - 0.1:
        set_bg(c, (60, 190, 160), (150, 230, 200), circle=(220, 255, 240), cy=1150, r=430, spot=True, t=t)
        plate_big(c, 760, 1380, 1.0, k=1.0)
        draw_stick(c, 400, 1520, 1.9, POSES['stand'], Face('happy', 'grin'), t=t, squash=1.0)
        c.drawOval(R.MakeXYWH(400 - 80, 1520 - 1.9 * 170, 160, 150), paint((255, 255, 255))); c.drawOval(R.MakeXYWH(400 - 80, 1520 - 1.9 * 170, 160, 150), stroke(INK, 7))
        if t > tb + 0.6:
            achoo(c, 430, 1040, 1.0, pr(t, tb + 0.6, 1.0), t, word='ACHOO!')
        top_shade(c, 0.3, (0, 60, 50))
        tier(c, t, tb - 0.45, 'or when their', 'STOMACH IS FULL', WT_, size=210)
        return
    set_bg(c, (20, 24, 70), (50, 50, 120), spot=False, t=t)
    for i in range(30):
        c.drawCircle(hsh(i, 2) * W, 260 + hsh(i, 3) * 600, 2 + 3 * hsh(i, 4), paint((255, 255, 255), 0.5 + 0.5 * math.sin(t * 2 + i)))
    bed(c, 540, 1500, w=700)
    awake = t > tw - 0.2
    c.save(); c.translate(270, 1330)
    c.drawCircle(0, 0, 60, paint((255, 255, 255))); c.drawCircle(0, 0, 60, stroke(INK, 6))
    c.save(); c.scale(1.2, 1.2); draw_face(c, Face('wide', 'o', 'up') if awake else Face('closed', 'flat'), 46, False, t); c.restore()
    c.restore()
    blanket(c, 540, 1500, w=640)
    if not awake: zzz(c, 360, 1220, t)
    else:
        f = font('ant', 90); s_ = '?!'; c.drawString(s_, 340, 1220, f, stroke(INK, 10)); c.drawString(s_, 340, 1220, f, paint(YEL))
    top_shade(c, 0.4)
    tier(c, t, ts - 0.05, 'you almost never sneeze', 'IN YOUR SLEEP', SKY, size=230, t1=tw - 0.3)
    tier(c, t, tw - 0.2, 'your body makes you', 'WAKE UP FIRST', YEL, size=220)


# ================================================================== ending
def sc_stop(c, t, S):
    tsep = ph('september sixteenth'); t976 = ph('nine hundred seventy six'); tw = ph('a whole day'); tr = ph('she still holds')
    if t < tr - 0.1:
        set_bg(c, (90, 170, 250), (180, 220, 255), circle=(230, 245, 255), cy=1150, r=440, spot=True, t=t)
        if t < tw - 0.1:
            calendar(c, 300, 1150, 0.75, 'SEP 16', '1983')
            k = eio(pr(t, t976 - 0.6, 1.4))
            counter(c, 700, 1180, 0.55, int(976 * k), t, col=YEL, label='DAYS')
        else:
            donna(c, 540, 1520, 2.0, POSES['arms_up'], Face('happy', 'grin'), t)
            for i in range(14):
                ph_ = (t * 0.6 + i / 14) % 1
                c.drawRect(R.MakeXYWH(hsh(i, 2) * W, 280 + ph_ * 1200, 18, 30), paint([YEL, PINK, MINT, SKY][i % 4]))
            pill(c, 540, 1620, 'ZERO SNEEZES', pr(t, tw, 0.35), col=MINT, size=60, txt_col=INK)
        top_shade(c, 0.35, (20, 40, 90))
        tier(c, t, S['t0'] + 0.1, 'did Donna ever stop?', 'YES!', MINT, size=290, t1=tsep - 0.3)
        tier(c, t, tsep - 0.2, 'after 976 days, in 1983:', 'A SNEEZE-FREE DAY', WT_, size=170)
        return
    set_bg(c, (90, 40, 180), (170, 90, 240), circle=(210, 160, 255), cy=1150, r=440, spot=True, t=t)
    trophy(c, 540, 1380, 1.4, pr(t, tr - 0.1, 0.5), label='976 DAYS')
    top_shade(c, 0.4)
    tier(c, t, tr - 0.05, 'still the world record:', 'LONGEST SNEEZING FIT', YEL, size=160)


def sc_ask(c, t, S):
    tl = ph('let it out'); tq = ph("what's the most")
    room(c, t, (255, 120, 90), (255, 220, 150))
    if t < tq - 0.2:
        t0 = S['t0'] + 0.3 + 1.1 * int(max(0, t - S['t0'] - 0.3) / 1.1) if t < tl - 0.5 else tl - 0.3
        sneezer(c, 420, 1500, 1.9, t, min(t0, S['t0'] + 0.3 + 2.2) if t < tl - 0.5 else tl - 0.3, who='mascot', base=POSES['stand'],
                word=('ACHOO!' if t < tl - 0.5 else 'LET IT OUT!'))
    else:
        draw_stick(c, 420, 1500, 1.9, POSES['wave'], Face('happy', 'grin'), t=t)
        comment_bubble(c, 780, 980, 0.8, pr(t, ph('comments') - 0.2, 0.35))
    top_shade(c, 0.45, (120, 30, 20))
    tier(c, t, tq - 0.1, "what's your record?", 'SNEEZES IN A ROW', YEL, size=190)
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint((40, 24, 60)))


SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='donna', t0=ph('her name was') - 0.2, fn=sc_donna, tin='whip'),
    dict(k='million', t0=ph("by guinness's") - 0.2, fn=sc_million, tin='flash'),
    dict(k='perday', t0=ph("that's around two") - 0.2, fn=sc_perday, tin='wipe', col=(255, 200, 100)),
    dict(k='what', t0=ph('okay so what') - 0.2, fn=sc_what, tin='wipe', col=(120, 220, 240)),
    dict(k='body', t0=ph('your eyes snap') - 0.2, fn=sc_body, tin='zoom'),
    dict(k='speed', t0=ph("you've probably heard") - 0.2, fn=sc_speed, tin='whip'),
    dict(k='drops', t0=ph('the tiny droplets') - 0.2, fn=sc_drops, tin='wipe', col=(160, 130, 240)),
    dict(k='hold', t0=ph('and whatever you do') - 0.2, fn=sc_hold, tin='flash'),
    dict(k='tear', t0=ph('that trapped pressure') - 0.2, fn=sc_tear, tin='zoom'),
    dict(k='twenty', t0=ph('his doctors said') - 0.2, fn=sc_twenty, tin='whip'),
    dict(k='facts', t0=ph("here's some sneeze") - 0.2, fn=sc_facts, tin='wipe', col=(255, 140, 190)),
    dict(k='more', t0=ph('some people sneeze when they pluck') - 0.2, fn=sc_more, tin='whip'),
    dict(k='stop', t0=ph('so did donna') - 0.2, fn=sc_stop, tin='wipe', col=(150, 200, 255)),
    dict(k='ask', t0=ph('so next time') - 0.2, fn=sc_ask, tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('a million') + 0.1, 12, 0.35)
EP.shk(ph('slam it out'), 14, 0.3)
EP.shk(ph('it tore'), 16, 0.35); EP.flash(ph('it tore'), 0.3, 0.12, (255, 120, 120))
EP.shk(ph('more than twenty'), 10, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
