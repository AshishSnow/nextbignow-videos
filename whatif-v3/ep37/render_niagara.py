"""What if you went over Niagara Falls in a barrel? — episode 37 (Annie Edson Taylor, 24 Oct 1901)."""
import sys, os, math, re
import skia
from niagaraprops import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('NG_DIR', 'niagara'))
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


def top_shade(c, a=0.45, col=(10, 20, 50)):
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


def bigtxt(c, x, y, s_, size, col, rot=0.0):
    f = font('ant', size)
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawString(s_, -f.measureText(s_) / 2, size * 0.36, f, stroke(INK, size * 0.14)); c.drawString(s_, -f.measureText(s_) / 2, size * 0.36, f, paint(col))
    c.restore()


# ================================================================== intro
def sc_hook(c, t, S):
    tb = ph('inside a barrel'); ts = ph('sixty three'); tbd = ph('on her birthday')
    if t > ts - 0.2:
        set_bg(c, (255, 120, 150), (255, 190, 210), circle=(255, 230, 240), cy=1150, r=440, spot=True, t=t)
        annie(c, 420, 1520, 1.8, POSES['wave'], Face('happy', 'grin'), t)
        if t > tbd - 0.2: cake(c, 790, 1500, 0.8 * eback(pr(t, tbd - 0.2, 0.35), 1.6), t)
        top_shade(c, 0.4, (100, 0, 40))
        tier(c, t, ts - 0.2, 'the first survivor was a', '63-YEAR-OLD TEACHER', YEL, size=170)
        return
    falls_bg(c, t, edge_y=1020)
    # barrel tips over the edge and drops, on a loop
    ph_ = (t % 3.0) / 3.0
    if ph_ < 0.35:
        x = lerp(200, 560, ph_ / 0.35); y = 940; rot = 20 * math.sin(t * 4)
    else:
        k = (ph_ - 0.35) / 0.65; x = 560 + 60 * k; y = 940 + 900 * k * k; rot = 200 * k
    barrel(c, x, y, 0.75, rot=rot)
    top_shade(c, 0.55)
    tier(c, t, 0.0, 'what if you went over', 'NIAGARA FALLS', WT_, size=230, t1=tb - 0.25)
    tier(c, t, tb - 0.15, 'inside a', 'BARREL?', YEL, size=290, t1=ts - 0.3)
    tier(c, t, ts - 0.2, 'the first survivor was a', '63-YEAR-OLD TEACHER', YEL, size=170)


def sc_annie(c, t, S):
    tb = ph('almost broke')
    set_bg(c, (90, 70, 170), (170, 140, 230), circle=(210, 190, 255), cy=1150, r=440, spot=True, t=t)
    calendar(c, 820, 1060, 0.6, 'YEAR', '1901')
    annie(c, 460, 1520, 1.9, POSES['stand'] if t < tb else POSES['shrug'], Face('open', 'smile') if t < tb else Face('open', 'frown', 'worried'), t)
    if t > tb:
        c.save(); c.translate(800, 1400)
        k = eback(pr(t, tb, 0.35), 1.6); c.scale(k, k)
        c.drawOval(R.MakeXYWH(-90, -60, 180, 120), paint((150, 100, 60))); c.drawOval(R.MakeXYWH(-90, -60, 180, 120), stroke(INK, 6))
        c.drawCircle(0, 70, 16, paint((230, 200, 80))); c.drawCircle(0, 70, 16, stroke(INK, 4))
        c.restore()
    top_shade(c, 0.4)
    tier(c, t, ph('her name was') - 0.1, 'her name was', 'ANNIE EDSON TAYLOR', WT_, size=160, t1=tb - 0.3)
    tier(c, t, tb - 0.2, 'it was 1901, and she was', 'ALMOST BROKE', YEL, size=230)


def sc_plan(c, t, S):
    steps = [('survived', 'SURVIVE IT', (60, 190, 120)), ('get famous', 'GET FAMOUS', (240, 110, 160)), ('worry about money', 'MONEY FOREVER', (255, 190, 50))]
    set_bg(c, (255, 140, 70), (255, 200, 130), circle=(255, 230, 190), cy=1150, r=440, spot=True, t=t)
    for i, (p_, lbl, col) in enumerate(steps):
        k = pr(t, ph(p_) - 0.2, 0.35)
        if k <= 0: continue
        def dr(cc, lbl=lbl, col=col, i=i):
            f = font('ant', 70); cc.drawCircle(-220, 0, 50, paint(col)); cc.drawCircle(-220, 0, 50, stroke(INK, 5))
            fn = font('ant', 64); cc.drawString(str(i + 1), -220 - fn.measureText(str(i + 1)) / 2, 23, fn, paint((255, 255, 255)))
            cc.drawString(lbl, 40 - f.measureText(lbl) / 2, 25, f, paint(INK))
        card3d(c, 540, 980 + i * 200, 620, 170, 6 * math.sin(t + i), 0, dr, k=k)
    top_shade(c, 0.3, (120, 50, 0))
    tier(c, t, S['t0'] + 0.1, 'her plan?', 'GO OVER THE FALLS', INK, size=210, small_col=INK)


def sc_age(c, t, S):
    tt = ph('twenty years younger')
    set_bg(c, (40, 180, 200), (130, 225, 235), circle=(210, 250, 255), cy=1150, r=440, spot=True, t=t)
    annie(c, 380, 1520, 1.8, POSES['shrug'], Face('happy', 'grin'), t)
    speech(c, 720, 960, 330, 200, "I'M 43", pr(t, ph('forty three') - 0.2, 0.35), size=100, col=INK)
    if t > tt - 0.2:
        bigtxt(c, 760, 1300, 'REAL: 63', 100, YEL, rot=-6 * eback(pr(t, tt - 0.2, 0.4), 1.6))
    top_shade(c, 0.3, (0, 60, 80))
    tier(c, t, ph('she even told') - 0.1, 'she told reporters she was', '43', WT_, size=300, t1=ph('bold move') - 0.3)
    tier(c, t, ph('bold move') - 0.2, '', 'BOLD MOVE', YEL, size=280)


# ================================================================== the barrel
def sc_barrel(c, t, S):
    tm = ph('a mattress'); th = ph('leather harness'); ta = ph('heavy anvil')
    set_bg(c, (200, 110, 50), (255, 190, 110), circle=(255, 225, 170), cy=1180, r=450, spot=True, t=t)
    cut = pr(t, tm - 0.4, 0.5)
    barrel(c, 540, 1250, 1.45, cut=cut, mattress=pr(t, tm, 0.3), harness=pr(t, th, 0.3), anvil=pr(t, ta, 0.4))
    for lbl, tt_, x, y in (('MATTRESS', tm, 230, 1080), ('HARNESS', th, 850, 1130), ('ANVIL', ta, 830, 1420)):
        if t > tt_ - 0.1: pill(c, x, y, lbl, pr(t, tt_ - 0.1, 0.3), col=INK, size=46)
    top_shade(c, 0.35, (100, 40, 0))
    tier(c, t, S['t0'] + 0.1, 'so she built a', 'CUSTOM BARREL', WT_, size=230, t1=tm - 0.5)
    tier(c, t, tm - 0.4, 'inside:', 'PADDING + WEIGHT', YEL, size=200)


def sc_cat(c, t, S):
    to = ph('on her cat'); tw = ph('the cat went over'); ta = ph('came back alive')
    if t < tw - 0.1:
        set_bg(c, (255, 120, 150), (255, 190, 210), circle=(255, 230, 240), cy=1150, r=440, spot=True, t=t)
        barrel(c, 380, 1430, 1.0)
        cat(c, 740, 1500, 1.4 * eback(pr(t, S['t0'] + 0.3, 0.4), 1.5), t, face='open', flip=True)
        top_shade(c, 0.35, (100, 0, 40))
        tier(c, t, S['t0'] + 0.1, 'first, she tested it on', 'HER CAT', WT_, size=290)
        return
    if t < ta - 0.1:
        falls_bg(c, t, edge_y=1000)
        k = pr(t, tw, ta - tw)
        barrel(c, 520 + 40 * k, 900 + 900 * k * k, 0.6, rot=300 * k)
        top_shade(c, 0.5)
        tier(c, t, tw - 0.05, 'the cat went', 'OVER THE FALLS', WT_, size=220)
        return
    set_bg(c, (60, 200, 120), (150, 240, 180), circle=(220, 255, 230), cy=1150, r=440, spot=True, t=t)
    barrel(c, 540, 1520, 1.0, rot=0)
    cat(c, 560, 1360, 1.3, t, face='happy', bandage=pr(t, ph('with a cut') - 0.1, 0.3))
    top_shade(c, 0.3, (0, 70, 30))
    tier(c, t, ta - 0.05, 'and it came back', 'ALIVE', WT_, size=300)


# ================================================================== the ride
def sc_ride(c, t, S):
    tp = ph('bicycle pump'); tr = ph('into the river')
    set_bg(c, (120, 200, 255), (220, 240, 255), spot=False, t=t)
    river(c, t, 1350)
    c.drawRect(R.MakeLTRB(0, 1280, 520, 1360), paint((120, 90, 60))); c.drawLine(0, 1280, 520, 1280, stroke(INK, 6))
    calendar(c, 820, 1000, 0.6, 'OCT 24', '1901')
    push = eo(pr(t, tr, 1.2))
    barrel(c, lerp(380, 700, push), lerp(1180, 1330, push), 0.9, rot=lerp(0, 25, push) + (6 * math.sin(t * 3) if push > 0.8 else 0))
    if t < tr:
        pump(c, 200, 1280, 0.9, t)
        draw_stick(c, 140, 1280, 1.2, POSES['press'], Face('open', 'smile'), t=t, scarf=(60, 120, 230))
    else:
        draw_stick(c, 200, 1280, 1.2, POSES['wave'], Face('open', 'o', 'worried'), t=t, scarf=(60, 120, 230))
    top_shade(c, 0.4)
    tier(c, t, S['t0'] + 0.1, 'October 24, her friends', 'SEALED HER IN', WT_, size=220, t1=tp - 0.3)
    tier(c, t, tp - 0.2, 'extra air with a', 'BICYCLE PUMP', YEL, size=230)


def sc_float(c, t, S):
    to = ph('then she went over'); t17 = ph('seventeen story')
    if t < to - 0.1:
        set_bg(c, (110, 190, 250), (200, 235, 255), spot=False, t=t)
        river(c, t, 1100)
        c.drawRect(R.MakeLTRB(800, 1100, W, H), paint((255, 255, 255), 0.7))
        u = t - S['t0']
        barrel(c, lerp(200, 700, cl(u / max(1, to - S['t0']))), 1200 + 15 * math.sin(t * 2), 0.8, rot=u * 70)
        top_shade(c, 0.4)
        tier(c, t, S['t0'] + 0.1, 'she floated for about', '20 MINUTES', WT_, size=260)
        return
    if t < t17 - 0.2:
        falls_bg(c, t, edge_y=950)
        k = pr(t, to + 0.2, 1.6)
        barrel(c, 520 + 40 * k, 870 + 1000 * k * k, 0.7, rot=280 * k)
        top_shade(c, 0.5)
        tier(c, t, to - 0.05, 'then she dropped', '51 METERS', YEL, size=280)
        return
    set_bg(c, (40, 60, 140), (110, 130, 220), circle=(150, 170, 250), cy=1150, r=440, spot=True, t=t)
    tower(c, 400, 1520, 1.0, 17, k=eo(pr(t, t17 - 0.2, 0.9)))
    k = pr(t, t17 + 0.6, 1.0)
    barrel(c, 650, lerp(840, 1450, k * k), 0.35, rot=200 * k)
    top_shade(c, 0.4)
    tier(c, t, t17 - 0.15, 'like falling off a', '17-STORY BUILDING', WT_, size=180)


def sc_bottom(c, t, S):
    tp = ph('more than an olympic')
    if t < tp - 0.6:
        set_bg(c, (20, 60, 140), (60, 120, 220), circle=(100, 170, 250), cy=1250, r=440, spot=True, t=t)
        gauge(c, 540, 1350, 330, lerp(0.1, 0.85, eo(pr(t, S['t0'] + 0.4, 1.2))), t)
        bigtxt(c, 540, 1500, '110 KM/H', 120, YEL)
        top_shade(c, 0.4)
        tier(c, t, S['t0'] + 0.1, 'you hit the water at', '110 KM/H', WT_, size=270)
        return
    falls_bg(c, t, edge_y=930, mist=1.0)
    k = ((t - tp) % 1.0)
    pool_icon(c, 540, 1280, 1.3, fill=eo(cl(k * 1.3)), t=t)
    pill(c, 540, 1480, 'EVERY SECOND', 1, col=RED, size=60)
    splash(c, 540, 1230, k, 1.0)
    top_shade(c, 0.55)
    tier(c, t, tp - 0.55, 'more than an', 'OLYMPIC POOL', WT_, size=240)


# ================================================================== she lived
def sc_out(c, t, S):
    ta = ph('but alive'); tf = ph('the first person ever')
    set_bg(c, (60, 200, 120), (150, 240, 180), circle=(220, 255, 230), cy=1150, r=440, spot=True, t=t)
    barrel(c, 300, 1520, 0.9, lid=0.0)
    k = eo(pr(t, S['t0'] + 0.5, 1.4))
    alive = t > ta - 0.1
    annie(c, lerp(330, 600, k), 1520 - 120 * math.sin(math.pi * k), 1.8, POSES['arms_up'] if alive else POSES['crouch'],
          Face('happy', 'grin') if alive else Face('open', 'frown', 'worried'), t)
    if alive:
        for i in range(14):
            ph_ = (t * 0.6 + i / 14) % 1
            c.drawRect(R.MakeXYWH(hsh(i, 2) * W, 280 + ph_ * 1200, 18, 30), paint([YEL, PINK, MINT, (120, 200, 255)][i % 4]))
    if t > tf - 0.1: medal(c, 800, 1150, 0.9, pr(t, tf - 0.1, 0.4), label='1ST')
    top_shade(c, 0.3, (0, 70, 30))
    tier(c, t, S['t0'] + 0.1, 'bruised, shaking...', 'BUT ALIVE', WT_, size=290, t1=tf - 0.3)
    tier(c, t, tf - 0.2, 'the first person to', 'SURVIVE IT', YEL, size=290)


def sc_words(c, t, S):
    tc = ph('walk up to a cannon')
    set_bg(c, (220, 50, 60), (255, 120, 110), circle=(255, 180, 170), cy=1150, r=440, spot=True, t=t)
    annie(c, 360, 1520, 1.8, POSES['shrug'] if t < tc else POSES['shock'], Face('open', 'frown', 'angry'), t)
    if t > tc - 0.2:
        cannon(c, 760, 1440, 1.0 * eback(pr(t, tc - 0.2, 0.4), 1.5), t)
    top_shade(c, 0.4, (90, 0, 0))
    tier(c, t, S['t0'] + 0.1, 'her advice:', 'NEVER DO THIS', WT_, size=270, t1=tc - 0.3)
    tier(c, t, tc - 0.2, "she'd rather face a", 'CANNON', YEL, size=300)


def sc_rich(c, t, S):
    tn = ph('nope'); tm = ph('manager ran off'); tph = ph('posing for photos'); tb = ph('died broke')
    set_bg(c, (90, 70, 170), (170, 140, 230), circle=(210, 190, 255), cy=1150, r=440, spot=True, t=t)
    if t < tph - 0.2:
        if t > tm - 0.2:
            k = pr(t, tm, 2.0)
            x = lerp(500, 1250, k)
            barrel(c, x + 120, 1430, 0.8, rot=8 * math.sin(t * 10))
            draw_stick(c, x, 1520, 1.4, walk_pose(t * 2.4, 1.0, run=True), Face('happy', 'grin'), t=t, scarf=(40, 40, 40))
            annie(c, 260, 1520, 1.6, POSES['shock'], Face('wide', 'o', 'worried'), t)
        else:
            annie(c, 540, 1520, 1.8, POSES['shrug'], Face('open', 'frown', 'worried'), t)
            if t > tn - 0.1: cross_icon(c, 800, 1150, 1.2 * eback(pr(t, tn - 0.1, 0.3), 1.6))
        top_shade(c, 0.4)
        tier(c, t, S['t0'] + 0.1, 'so did she get rich?', 'NOPE', RED, size=300, t1=tm - 0.3)
        tier(c, t, tm - 0.2, 'her manager ran off', 'WITH THE BARREL', YEL, size=220)
        return
    annie(c, 380, 1520, 1.7, POSES['wave'], Face('happy', 'smile'), t)
    camera_flash(c, 800, 1150, 1.0, t, k=(t * 0.8) % 1)
    booklet(c, 760, 1420, 0.8, rot=8)
    top_shade(c, 0.4)
    tier(c, t, tph - 0.15, 'photos with tourists,', '10-CENT BOOKLETS', WT_, size=190, t1=tb - 0.3)
    tier(c, t, tb - 0.2, 'she died at 82,', 'BROKE', YEL, size=300)


def sc_ask(c, t, S):
    ti = ph('illegal'); ts = ph('would you have gone second')
    if t < ts - 0.2:
        falls_bg(c, t, edge_y=1000, mist=1.0)
        no_stamp(c, 540, 1300, 1.6, pr(t, ti - 0.1, 0.35))
        top_shade(c, 0.5)
        tier(c, t, S['t0'] + 0.1, 'today, going over is', 'ILLEGAL', RED, size=300)
        return
    set_bg(c, (255, 140, 70), (255, 200, 130), circle=(255, 230, 190), cy=1150, r=440, spot=True, t=t)
    barrel(c, 300, 1500, 0.9)
    cat(c, 540, 1500, 1.2, t, face='happy', bandage=1.0)
    comment_bubble(c, 820, 1050, 0.75, pr(t, ph('comments') - 0.2, 0.35))
    top_shade(c, 0.3, (120, 50, 0))
    tier(c, t, ts - 0.1, 'would you go second,', 'AFTER THE CAT?', INK, size=210, small_col=INK)
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint((20, 30, 60)))


SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='annie', t0=ph('her name was') - 0.2, fn=sc_annie, tin='whip'),
    dict(k='plan', t0=ph('her plan') - 0.2, fn=sc_plan, tin='wipe', col=(255, 190, 120)),
    dict(k='age', t0=ph('she even told') - 0.2, fn=sc_age, tin='zoom'),
    dict(k='barrel', t0=ph('so she built') - 0.2, fn=sc_barrel, tin='wipe', col=(255, 170, 90)),
    dict(k='cat', t0=ph('two days before') - 0.2, fn=sc_cat, tin='whip'),
    dict(k='ride', t0=ph('on october') - 0.2, fn=sc_ride, tin='flash'),
    dict(k='float', t0=ph('she floated') - 0.2, fn=sc_float, tin='wipe', col=(150, 210, 255)),
    dict(k='bottom', t0=ph("at the bottom you're") - 0.2, fn=sc_bottom, tin='zoom'),
    dict(k='out', t0=ph('when they finally') - 0.2, fn=sc_out, tin='wipe', col=(150, 240, 180)),
    dict(k='words', t0=ph('and her first words') - 0.2, fn=sc_words, tin='whip'),
    dict(k='rich', t0=ph('so did she get rich') - 0.2, fn=sc_rich, tin='wipe', col=(190, 160, 240)),
    dict(k='ask', t0=ph('today going over') - 0.2, fn=sc_ask, tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('then she went over') + 1.2, 16, 0.4); EP.flash(ph('then she went over') + 1.2, 0.3, 0.12, (255, 255, 255))
EP.shk(ph("at the bottom you're") + 0.4, 10, 0.3)
EP.shk(ph('walk up to a cannon') + 0.3, 12, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
