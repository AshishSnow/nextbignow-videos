"""What if you fell into Jupiter? — episode 35 (Galileo probe, 7 Dec 1995; orbiter plunge, 21 Sep 2003)."""
import sys, os, math, re
import skia
from jupprops import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('JP_DIR', 'jupiter'))
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


def top_shade(c, a=0.45, col=(10, 6, 24)):
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


# ================================================================== hook
def sc_hook(c, t, S):
    u = t
    tn = ph('never hit'); tt = ph("there isn't")
    z = 1 + 0.08 * u
    c.save(); cam(c, z, 540, 1300)
    jupiter_space(c, t, cx=540, cy=2350, r=1500)
    c.restore()
    k = cl(u / 4.0)
    astro(c, 540 + 30 * math.sin(t), lerp(1000, 1250, eo(k)), 1.15, POSES['float'] if t < tn else POSES['shock'],
          Face('happy', 'grin') if t < tn else Face('wide', 'o', 'worried', look=(0, 1)), t, rot=8 * math.sin(t * 0.8))
    if t > tt - 0.1:
        # 'no ground' sign falling away
        kk = eback(pr(t, tt - 0.1, 0.35), 1.6)
        c.save(); c.translate(540, 1440); c.scale(kk, kk)
        c.drawRoundRect(R.MakeXYWH(-230, -60, 460, 120), 24, 24, paint((255, 255, 255))); c.drawRoundRect(R.MakeXYWH(-230, -60, 460, 120), 24, 24, stroke(INK, 7))
        f = font('ant', 70); s_ = 'NO GROUND'; c.drawString(s_, -f.measureText(s_) / 2, 26, f, paint(RED))
        c.restore()
    top_shade(c, 0.5)
    tier(c, t, 0.0, 'what if you fell into', 'JUPITER?', (255, 200, 120), size=270, t1=tn - 0.25)
    tier(c, t, tn - 0.15, 'spoiler:', "YOU'D NEVER LAND", WT_, size=190)


def sc_robot(c, t, S):
    u = t - S['t0']
    tw = ph('talked to us')
    jupiter_space(c, t, cx=540, cy=2500, r=1500)
    orbiter(c, 820, 620, 0.55, t, rot=-8)
    y = lerp(850, 1300, eo(pr(t, S['t0'], 5.0)))
    probe(c, 420, y, 0.9, t, rot=8, signal=1.0 if t > tw - 0.3 else 0.3)
    if t > tw - 0.3:
        for i in range(4):
            ph_ = (t * 1.4 + i / 4) % 1
            x = lerp(440, 800, ph_); yy = lerp(y - 120, 680, ph_)
            c.drawCircle(x, yy, 12, paint((120, 220, 255), 1 - ph_))
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'one brave robot', 'TRIED IT', WT_, t1=tw - 0.2)
    tier(c, t, tw - 0.1, 'and it talked to us', 'THE WHOLE WAY', YEL, size=220)


def sc_entry(c, t, S):
    u = t - S['t0']
    ts = ph('one hundred seventy')
    cloud_fall(c, t, speed=2.2)
    probe(c, 540 + 10 * math.sin(t * 30), 1150, 1.2, t, heat=cl((t - S['t0'] - 0.5) / 0.6), signal=0.0)
    calendar(c, 850, 960, 0.6, 'DEC 7', '1995')
    if t > ts - 0.1:
        pill(c, 540, 1440, '170,000 KM/H', pr(t, ts - 0.1, 0.35), col=RED, size=70)
    top_shade(c, 0.45)
    tier(c, t, ph('galileo probe') - 0.1, "NASA's", 'GALILEO PROBE', WT_, size=210, t1=ts - 0.2)
    tier(c, t, ts - 0.05, 'hit the sky at', '170,000 KM/H', YEL, size=200)


def sc_india(c, t, S):
    u = t - S['t0']
    set_bg(c, (20, 30, 80), (60, 80, 160), spot=True, t=t)
    k = eio(pr(t, S['t0'] + 0.4, 1.8))
    india_bar(c, 90, 1000, 900, t, k)
    stopwatch_count(c, 540, 1420, 0.55, int(64 * k), t)
    top_shade(c, 0.3)
    tier(c, t, S['t0'] + 0.1, 'cross India in', 'ABOUT 1 MINUTE', YEL, size=210)


def sc_heat(c, t, S):
    u = t - S['t0']
    tb = ph('braked so hard'); ts = ph('imagine your seatbelt')
    if t < ts - 0.15:
        cloud_fall(c, t, speed=2.5)
        probe(c, 540 + 8 * math.sin(t * 40), 1150, 1.3, t, heat=1.0, signal=0.0)
        if t < tb:
            sun_icon(c, 860, 520, 70, t)
            f = font('ant', 90); s_ = 'X2'; c.drawString(s_, 860 - f.measureText(s_) / 2, 700, f, stroke(INK, 12)); c.drawString(s_, 860 - f.measureText(s_) / 2, 700, f, paint(YEL))
        top_shade(c, 0.45)
        tier(c, t, S['t0'] + 0.1, 'the air got', '2X HOTTER THAN THE SUN', (255, 220, 120), size=150, t1=tb - 0.2)
        tier(c, t, tb - 0.05, 'it braked at', '230 G', RED, size=280, t1=ts - 0.2)
    else:
        set_bg(c, (255, 190, 90), (255, 230, 160), circle=(255, 255, 255), cy=1050, r=430, spot=True, t=t, circ_k=pr(t, ts - 0.15, 0.4))
        car_seat(c, 540, 1350, 1.4, t, squash=eo(pr(t, ts + 0.4, 0.5)))
        speed_lines(c, t, a=0.6, n=14, y0=900, y1=1500, col=(255, 255, 255))
        top_shade(c, 0.1, col=(120, 60, 0))
        tier(c, t, ts - 0.05, 'imagine your', 'SEATBELT DOING THAT', INK, size=160, small_col=INK)


# ================================================================== chapter 1: your turn
def sc_turn(c, t, S):
    u = t - S['t0']
    cloud_fall(c, t, speed=1.0)
    astro(c, 540 + 20 * math.sin(t * 1.2), 1200, 1.3, POSES['float'], Face('open', 'smile'), t, rot=10 * math.sin(t * 0.9))
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, "now it's", 'YOUR TURN', YEL, size=270)


def sc_heavy(c, t, S):
    u = t - S['t0']
    tg = ph('two and a half'); tw = ph('one hundred and twenty'); tl = ph('leg day')
    set_bg(c, (230, 140, 80), (255, 200, 140), circle=(255, 240, 210), cy=1050, r=430, spot=True, t=t, circ_k=pr(t, S['t0'], 0.4))
    if t < tl - 0.1:
        val = int(lerp(50, 125, eo(pr(t, tw - 0.4, 0.6))))
        heavy = val > 60
        astro(c, 540, 1360, 1.3, POSES['crouch'] if heavy else POSES['stand'], Face('wide', 'chatter', 'worried') if heavy else Face('open', 'smile'), t, squash=1 - 0.12 * heavy)
        scale_box(c, 540, 1420, 1.5, val)
        if tg - 0.2 < t:
            pill(c, 540, 860, '2.5X GRAVITY', pr(t, tg - 0.2, 0.35), col=(120, 60, 200), size=70)
    else:
        sq = math.sin(t * 6)
        astro(c, 540, 1420, 1.3, lerp_pose(POSES['crouch'], (0, 0, 220, 30, 140, -30, 180, 0, 180, 0), 0.5 + 0.5 * sq), Face('wide', 'chatter', 'angry'), t,
              prop=lambda cc, hr, hl: dumbbell(cc, hr[0], hr[1], 0.5, rot=0))
        for i in range(3):
            c.drawCircle(700 + i * 20, 980 - i * 40 - (t * 60 % 40), 10 + i * 4, paint((120, 200, 255), 0.7))
    top_shade(c, 0.2, col=(120, 50, 0))
    tier(c, t, ph('if you weigh') - 0.1, 'you weigh 50 kg?', 'NOW: 125 KG', INK, size=220, small_col=INK, t1=tl - 0.2)
    tier(c, t, tl - 0.1, 'great place for', 'LEG DAY', RED, size=270, small_col=INK)


def sc_clouds(c, t, S):
    u = t - S['t0']
    ta = ph('ammonia'); tb = ph('bathroom floor')
    cloud_fall(c, t, speed=0.7, ammonia=0.7)
    pose = POSES['float'] if t < tb - 0.4 else (0, 0, 200, 10, 110, -140, 186, 0, 174, 0)
    astro(c, 420, 1250, 1.25, pose, Face('open', 'puff' if t > ta + 0.5 else 'o', 'worried'), t, rot=6 * math.sin(t))
    if t > ta - 0.1:
        spray_bottle(c, 820, 1150, 1.1 * eback(pr(t, ta - 0.1, 0.35), 1.6), t, spray=1.0)
    for i in range(5):
        ph_ = (t * 0.5 + i / 5) % 1
        x = 820 - ph_ * 300; y = 1000 - ph_ * 60
        c.drawPath(_wave(x, y), stroke((140, 200, 120), 6, (1 - ph_) * cl((t - ta) / 0.5)))
    top_shade(c, 0.45)
    tier(c, t, ta - 0.1, 'the top clouds are', 'AMMONIA', WT_, size=270, t1=tb - 0.4)
    tier(c, t, tb - 0.35, 'it smells like a', 'MOPPED FLOOR', YEL, size=220)


def _wave(x, y):
    p = skia.Path(); p.moveTo(x - 30, y + 10); p.quadTo(x - 15, y - 15, x, y + 5); p.quadTo(x + 15, y + 25, x + 30, y); return p


def sc_wind(c, t, S):
    u = t - S['t0']
    th = ph('strongest hurricane')
    cloud_fall(c, t, speed=0.6)
    speed_lines(c, t, a=1.0, n=34, y0=700, y1=1700, speed=3200, col=(255, 255, 255), w=8)
    shake = 12 * math.sin(t * 50)
    astro(c, 380 + shake, 1450, 1.0, (-22, -10, 250, 40, 290, -40, 210, 10, 200, 10), Face('wide', 'chatter', 'worried'), t, rot=-18)
    gauge(c, 540, 1040, 200, 0.95, t)
    if t > th - 0.2:
        kk = eback(pr(t, th - 0.2, 0.35), 1.6)
        c.save(); c.translate(780, 1380); c.scale(kk, kk)
        c.drawRoundRect(R.MakeXYWH(-150, -110, 300, 220), 30, 30, paint((255, 255, 255))); c.drawRoundRect(R.MakeXYWH(-150, -110, 300, 220), 30, 30, stroke(INK, 6))
        hurricane_icon(c, -60, 0, 0.7, t)
        f2 = font('ant', 50); c.drawString('SLOWER', 0, 18, f2, paint((60, 120, 200)))
        c.restore()
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'and the wind?', '540 KM/H', YEL, size=260, t1=th - 0.3)
    tier(c, t, th - 0.25, 'faster than any', 'HURRICANE', WT_, size=260)


# ================================================================== chapter 2: deeper
def sc_squeeze(c, t, S):
    u = t - S['t0']
    ts = ph('went silent'); tp = ph('twenty-three'); tb = ph('boiling water'); tf = ph('only the first hour')
    dark = cl(u / 8) * 0.55
    cloud_fall(c, t, speed=0.5, dark=dark)
    probe(c, 540, 1050, 1.0, t, chute=1.0, signal=0.0 if t > ts else 1.0)
    if t > ts - 0.1:
        kk = eback(pr(t, ts - 0.1, 0.3), 1.6)
        c.save(); c.translate(540, 1330); c.scale(kk, kk)
        c.drawRoundRect(R.MakeXYWH(-260, -60, 520, 120), 24, 24, paint((30, 30, 40))); c.drawRoundRect(R.MakeXYWH(-260, -60, 520, 120), 24, 24, stroke(INK, 6))
        f = font('ant', 70); s_ = 'SIGNAL LOST'; c.drawString(s_, -f.measureText(s_) / 2, 26, f, paint(RED if (t * 3) % 1 < 0.6 else (120, 30, 30)))
        c.restore()
    if t > tp - 0.2:
        pill(c, 300, 1460, '23X PRESSURE', pr(t, tp - 0.2, 0.35), col=(120, 60, 200), size=50)
    if t > tb - 0.2:
        pill(c, 790, 1460, '152°C', pr(t, tb - 0.2, 0.35), col=RED, size=50)
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'the deeper you go,', 'THE MORE IT SQUEEZES', WT_, size=160, t1=tf - 0.3)
    tier(c, t, tf - 0.25, 'and that was only', 'THE FIRST HOUR', YEL, size=210)


def sc_black(c, t, S):
    u = t - S['t0']
    tl = ph('acting like a liquid'); ts = ph('slowly sink'); tb = ph('biggest ocean')
    dark = 0.6 + 0.4 * cl(u / 2)
    cloud_fall(c, t, speed=0.25, dark=dark)
    sink = eo(pr(t, ts, 3.0))
    if t > tl - 0.2:
        # liquid-like hydrogen: wobbly translucent surface rising under the astronaut
        y0 = lerp(1900, 1250, eo(pr(t, tl - 0.2, 1.2)))
        p = skia.Path(); p.moveTo(-20, H + 20)
        for i in range(46):
            x = -20 + i * 26; p.lineTo(x, y0 + 14 * math.sin(x * 0.015 + t * 1.2))
        p.lineTo(W + 20, H + 20); p.close()
        c.drawPath(p, paint(shader=lin(0, y0, 0, H, [argb((60, 90, 170), 0.55), argb((20, 30, 70), 0.85)])))
        c.drawPath(p, stroke((120, 170, 255), 4, 0.6))
    astro(c, 540, 1300 + 260 * sink, 1.1, POSES['float'], Face('open', 'o', 'worried', look=(0, 1)), t, rot=5 * math.sin(t))
    if t > tl:
        for i in range(8):
            ph_ = (t * 0.6 + i / 8) % 1
            c.drawCircle(400 + hsh(i, 3) * 280, 1500 - ph_ * 400, 6 + 10 * hsh(i, 4), stroke((160, 200, 255), 3, 1 - ph_))
    top_shade(c, 0.4)
    tier(c, t, ph('the sky turns black') - 0.1, 'the sky turns', 'BLACK', WT_, size=280, t1=tl - 0.3)
    tier(c, t, tl - 0.25, 'gas starts acting', 'LIKE A LIQUID', (140, 190, 255), size=220, t1=ph('no splash') - 0.1)
    tier(c, t, ph('no splash') - 0.05, 'no edge.', 'NO SPLASH', WT_, size=260, t1=tb - 0.3)
    tier(c, t, tb - 0.25, 'the biggest ocean in the', 'SOLAR SYSTEM', (140, 190, 255), size=220)


def sc_metal(c, t, S):
    u = t - S['t0']
    tm = ph('shiny like mercury'); tf = ph('magnetic field')
    if t < tf - 0.3:
        metal_ocean(c, t, k=eo(pr(t, S['t0'] + 0.2, 0.8)), top=1050)
        astro(c, 540, 1150 + 20 * math.sin(t * 1.3), 1.1, POSES['shock'], Face('wide', 'o', 'up'), t)
        for i in range(10):
            a = (t * 0.7 + i * 0.63) % 6.28
            c.drawCircle(540 + math.cos(a) * 420, 700 + math.sin(a) * 120, 5, paint((255, 255, 255), 0.6))
        top_shade(c, 0.45)
        tier(c, t, S['t0'] + 0.1, 'hydrogen crushed into', 'METAL', (220, 228, 245), size=290, t1=tm - 0.2)
        tier(c, t, tm - 0.1, 'liquid, shiny like', 'MERCURY', (220, 228, 245), size=270)
    else:
        space_bg(c, t, (14, 16, 50), (30, 24, 60), seed=9)
        mag_field(c, 540, 1050, 260, t, a=eo(pr(t, tf - 0.3, 0.6)))
        draw_planet(c, 'jupiter', 540, 1050, 260, rot=t * 0.05, glow=(255, 210, 160), halo=(255, 190, 130))
        top_shade(c, 0.3)
        tier(c, t, tf - 0.25, "it powers Jupiter's", 'MAGNETIC FIELD', (120, 210, 255), size=200)


def sc_core(c, t, S):
    u = t - S['t0']
    td = ph('twenty-five thousand'); tp = ph('twelve million'); tc = ph('crushed cooked')
    space_bg(c, t, (14, 16, 50), (30, 24, 60), seed=12)
    marker = lerp(0.05, 0.98, eio(pr(t, S['t0'] + 0.3, 3.5)))
    cutaway(c, 360, 1080, 290, t, k=eback(pr(t, S['t0'], 0.5), 1.4), marker=marker)
    if t > td - 0.1: pill(c, 300, 1450, '25,000°C', pr(t, td - 0.1, 0.35), col=RED, size=56)
    if t > tp - 0.1: pill(c, 760, 1450, '12 MILLION X', pr(t, tp - 0.1, 0.35), col=(120, 60, 200), size=56)
    if t > tc - 0.1:
        for i, w_ in enumerate(('CRUSHED', 'COOKED', 'MELTED')):
            tt = ph(w_.lower()) if w_ != 'CRUSHED' else tc
            pill(c, 540, 1300, w_, pr(t, tt - 0.05, 0.25) * (1 - pr(t, tt + 0.55, 0.15)) if i < 2 else pr(t, tt - 0.05, 0.25), col=INK, size=60)
    top_shade(c, 0.4)
    tier(c, t, S['t0'] + 0.1, 'at the very center', 'A FUZZY CORE', (255, 190, 100), size=230)


# ================================================================== chapter 3: the orbiter
def sc_orbiter(c, t, S):
    u = t - S['t0']
    tp = ph('on purpose')
    jupiter_space(c, t, cx=540, cy=2400, r=1500)
    k = eo(pr(t, ph('crashed it') - 0.2, 2.5))
    orbiter(c, lerp(760, 540, k), lerp(650, 1500, k), lerp(0.7, 0.35, k), t, rot=lerp(-10, 40, k), fire=cl((k - 0.5) * 2))
    calendar(c, 230, 1200, 0.6, 'SEP 21', '2003')
    if t > tp - 0.1:
        pill(c, 540, 1450, 'ON PURPOSE', pr(t, tp - 0.1, 0.35), col=RED, size=70)
    top_shade(c, 0.5)
    tier(c, t, ph('nasa crashed') - 0.1, 'in 2003, NASA', 'CRASHED IT', RED, size=260)


def sc_europa(c, t, S):
    u = t - S['t0']
    to = ph('might hide'); tl = ph('maybe life'); tg = ph('single earth germ')
    space_bg(c, t, (10, 14, 50), (30, 30, 70), seed=21)
    draw_planet(c, 'jupiter', 1010, 1750, 420, rot=t * 0.03, glow=(255, 210, 160))
    europa(c, 540, 1080, 300, t, cut=eo(pr(t, to - 0.2, 0.8)), life=pr(t, tl - 0.1, 0.4))
    if t > tg - 0.2:
        kk = pr(t, tg - 0.2, 0.4)
        x = lerp(1100, 760, eo(kk))
        microbe(c, x, 1340, 0.8, t, col=(200, 120, 220), angry=True)
        f = font('ant', 42); c.drawString('EARTH GERM', x - f.measureText('EARTH GERM') / 2, 1470, f, paint((255, 255, 255)))
        no_stamp(c, x, 1340, 0.8, pr(t, tg + 0.6, 0.3))
    top_shade(c, 0.45)
    tier(c, t, ph('to protect') - 0.1, 'to protect', 'EUROPA', (200, 230, 255), size=290, t1=tl - 0.2)
    tier(c, t, tl - 0.15, 'a hidden ocean, and', 'MAYBE LIFE', (140, 230, 140), size=250)


def sc_become(c, t, S):
    u = t - S['t0']
    ta = ph('few atoms')
    z = 1 + 0.06 * u
    c.save(); cam(c, z, 540, 1050)
    space_bg(c, t, (14, 16, 50), (30, 24, 60), seed=31)
    draw_planet(c, 'jupiter', 540, 1050, 430, rot=t * 0.05, glow=(255, 210, 160), halo=(255, 190, 130))
    if t > ta - 0.3:
        for i in range(12):
            a = hsh(i, 3) * 6.28; r = 120 * hsh(i, 4)
            k = 0.5 + 0.5 * math.sin(t * 5 + i)
            c.drawCircle(600 + math.cos(a) * r, 1000 + math.sin(a) * r * 0.6, 5 + 4 * k, paint((255, 250, 220), k))
        c.drawCircle(600, 1000, 120, paint((255, 240, 180), 0.3, blur=40))
    c.restore()
    astro(c, 220, 1650, 0.8, POSES['wave'], Face('happy', 'smile'), t, rot=-8)
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, "it's not a place you land on,", 'YOU BECOME PART OF IT', YEL, size=150, t1=ta - 0.5)
    tier(c, t, ta - 0.45, 'Galileo is still in there,', 'AS ATOMS', WT_, size=260)


def sc_ask(c, t, S):
    u = t - S['t0']
    cloud_fall(c, t, speed=0.8)
    probe(c, 540, 1300, 1.2, t, heat=0.3, signal=1.0)
    astro(c, 540, 1160, 0.8, POSES['arms_up'], Face('happy', 'grin', 'up'), t)
    comment_bubble(c, 840, 900, 0.8, pr(t, ph('comments') - 0.2, 0.35))
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'would you ride it down for', 'ONE HOUR?', YEL, size=250)
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint((40, 24, 60)))


SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='robot', t0=ph('but one brave') - 0.2, fn=sc_robot, tin='whip'),
    dict(k='entry', t0=ph('on december') - 0.2, fn=sc_entry, tin='flash'),
    dict(k='india', t0=ph("that's fast enough") - 0.2, fn=sc_india, tin='wipe', col=(40, 60, 140)),
    dict(k='heat', t0=ph('the air in front') - 0.2, fn=sc_heat, tin='whip'),
    dict(k='turn', t0=ph("now it's your turn") - 0.2, fn=sc_turn, tin='wipe', col=(255, 214, 160)),
    dict(k='heavy', t0=ph('first you get heavy') - 0.2, fn=sc_heavy, tin='zoom'),
    dict(k='clouds', t0=ph('then come the clouds') - 0.2, fn=sc_clouds, tin='wipe', col=(250, 236, 210)),
    dict(k='wind', t0=ph('and the wind') - 0.2, fn=sc_wind, tin='whip'),
    dict(k='squeeze', t0=ph('the deeper you fall') - 0.2, fn=sc_squeeze, tin='wipe', col=(60, 40, 50)),
    dict(k='black', t0=ph('keep falling') - 0.2, fn=sc_black, tin='zoom'),
    dict(k='metal', t0=ph('thousands of kilometers') - 0.2, fn=sc_metal, tin='flash'),
    dict(k='core', t0=ph('at the very center') - 0.2, fn=sc_core, tin='wipe', col=(30, 24, 60)),
    dict(k='orbiter', t0=ph('so what happened') - 0.2, fn=sc_orbiter, tin='wipe', col=(255, 190, 130)),
    dict(k='europa', t0=ph('why to protect') - 0.2, fn=sc_europa, tin='whip'),
    dict(k='become', t0=ph("so jupiter isn't") - 0.2, fn=sc_become, tin='wipe', col=(255, 214, 160)),
    dict(k='ask', t0=ph('would you ride') - 0.2, fn=sc_ask, tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('one hundred seventy') + 0.1, 12, 0.35)
EP.shk(ph('braked so hard'), 18, 0.4); EP.flash(ph('braked so hard'), 0.4, 0.15, (255, 180, 90))
EP.shk(ph('imagine your seatbelt') + 0.5, 10, 0.25)
EP.shk(ph('went silent'), 8, 0.25)
EP.shk(ph('crushed cooked'), 14, 0.35)
EP.shk(ph('crashed it'), 10, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
