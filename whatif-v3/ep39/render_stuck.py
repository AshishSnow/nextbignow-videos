"""What if you got stuck in space for a year? — episode 39 (Frank Rubio: launch 21 Sep 2022, Soyuz MS-22 leak Dec 2022, landed 27 Sep 2023, 371 days)."""
import sys, os, math, re
import skia
from stuckprops import *
from fallprops import parachute
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('ST_DIR', 'stuck'))
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
WT_ = (255, 255, 255); SM = (255, 240, 220); SKY = (140, 210, 255)


def top_shade(c, a=0.45, col=(8, 10, 40)):
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


def bigtxt(c, x, y, s_, size, col):
    f = font('ant', size)
    c.drawString(s_, x - f.measureText(s_) / 2, y + size * 0.36, f, stroke(INK, size * 0.14)); c.drawString(s_, x - f.measureText(s_) / 2, y + size * 0.36, f, paint(col))


def sp(c, t, seed=4, glow=None):
    space_bg(c, t, SPACE[0], SPACE[1], seed=seed)


# ================================================================== intro
def sc_hook(c, t, S):
    tc = ph("can't come home"); tf = ph('frank rubio')
    sp(c, t)
    draw_planet(c, 'earth', 540, 2150, 900, rot=t * 0.02, glow=(120, 190, 255))
    iss(c, 540, 1000, 0.85, t, rot=-6)
    stuck = t > tc - 0.1
    astro(c, 540 + 20 * math.sin(t), 1450, 1.2, POSES['shock'] if stuck else POSES['wave'], Face('wide', 'o', 'worried') if stuck else Face('happy', 'grin'), t, rot=8 * math.sin(t * 0.7))
    if stuck: no_stamp(c, 820, 1250, 0.8, pr(t, tc - 0.1, 0.3))
    if t > tf - 0.1: pill(c, 540, 1610, 'NASA ASTRONAUT', pr(t, tf - 0.1, 0.35), col=(40, 80, 200), size=50)
    top_shade(c, 0.5)
    tier(c, t, 0.0, 'what if you went to space and', "COULDN'T COME HOME?", YEL, size=190, t1=tf - 0.3)
    tier(c, t, tf - 0.2, 'it happened to', 'FRANK RUBIO', WT_, size=260)


def sc_launch(c, t, S):
    tp = ph('the plan was simple')
    if t < tp - 0.1:
        set_bg(c, (40, 60, 150), (255, 150, 90), spot=False, t=t)
        k = eio(pr(t, S['t0'] + 0.6, 3.0))
        draw_rocket(c, 540, lerp(1560, 600, k), 0.9, flame=1.0, t=t)
        smoke(c, 540, 1560, t, S['t0'] + 0.6, n=16, spread=380)
        calendar(c, 830, 1000, 0.55, 'SEP', '2022')
        top_shade(c, 0.4)
        tier(c, t, S['t0'] + 0.1, 'he launched on a', 'SOYUZ ROCKET', WT_, size=250)
        return
    sp(c, t, seed=7)
    draw_planet(c, 'earth', 540, 2150, 900, rot=t * 0.02, glow=(120, 190, 255))
    iss(c, 540, 1050, 1.0, t)
    soyuz(c, 540, 1260, 0.55, t)
    top_shade(c, 0.45)
    tier(c, t, tp - 0.05, 'the plan:', '6 MONTHS', YEL, size=300, t1=ph('ride the same') - 0.3)
    tier(c, t, ph('ride the same') - 0.2, 'then ride the same', 'CAPSULE HOME', WT_, size=230)


def sc_hit(c, t, S):
    tr = ph('tiny space rock'); tl = ph('coolant started')
    sp(c, t, seed=11)
    iss(c, 540, 900, 0.8, t)
    hit = tr + 0.9
    soyuz(c, 540, 1250, 0.95, t, leak=pr(t, tl - 0.3, 0.6), hole=pr(t, hit, 0.15))
    if t < hit:
        k = pr(t, tr - 0.2, hit - tr + 0.2)
        rock(c, lerp(-100, 578, k), lerp(1050, 1326, k), 1.2, t)
    elif t < hit + 0.4:
        c.drawCircle(578, 1326, 160 * pr(t, hit, 0.4), paint((255, 230, 150), 1 - pr(t, hit, 0.4)))
    top_shade(c, 0.5)
    tier(c, t, tr - 0.2, 'a tiny space rock hit', 'HIS RIDE HOME', RED, size=230, t1=tl - 0.3)
    tier(c, t, tl - 0.2, 'coolant started', 'SPRAYING OUT', SKY, size=250)


def sc_nosafe(c, t, S):
    tn = ph('the answer was no')
    set_bg(c, (200, 50, 50), (255, 130, 90), circle=(255, 190, 150), cy=1150, r=440, spot=True, t=t)
    soyuz(c, 420, 1300, 1.0, t, rot=10 * math.sin(t))
    c.drawCircle(420, 1300, 200, paint((255, 120, 40), 0.35 + 0.15 * math.sin(t * 6), blur=30))
    thermometer(c, 820, 1450, 0.75, lerp(0.3, 0.95, eo(pr(t, S['t0'] + 0.3, 1.5))))
    if t > tn - 0.1: no_stamp(c, 420, 1300, 1.2, pr(t, tn - 0.1, 0.3))
    top_shade(c, 0.4, (90, 0, 0))
    tier(c, t, S['t0'] + 0.1, 'without coolant it could', 'OVERHEAT', YEL, size=290, t1=tn - 0.3)
    tier(c, t, tn - 0.2, 'not safe to fly', 'PEOPLE HOME', WT_, size=250)


def sc_wait(c, t, S):
    tsx = ph('six months turned')
    if t < tsx - 0.2:
        sp(c, t, seed=13)
        draw_planet(c, 'earth', 540, 2150, 900, rot=t * 0.02, glow=(120, 190, 255))
        k = eo(pr(t, S['t0'] + 0.2, 3.0))
        soyuz(c, lerp(980, 540, k), lerp(1500, 1150, k), 0.8, t, rot=lerp(-30, 0, k))
        pill(c, lerp(980, 540, k), lerp(1500, 1150, k) + 200, 'EMPTY', 1, col=(40, 80, 200), size=50)
        top_shade(c, 0.45)
        tier(c, t, S['t0'] + 0.1, 'a new capsule launched', 'EMPTY', WT_, size=300)
        return
    set_bg(c, (255, 150, 60), (255, 210, 130), circle=(255, 235, 190), cy=1150, r=440, spot=True, t=t)
    calendar(c, 330, 1180, 0.8, 'PLAN', '6 MO')
    calendar(c, 760, 1180, 0.8 * eback(pr(t, tsx + 0.6, 0.4), 1.6), 'REALITY', '1 YEAR', col=RED)
    top_shade(c, 0.3, (120, 50, 0))
    tier(c, t, tsx - 0.15, '6 months turned into', 'A WHOLE YEAR', INK, size=250, small_col=INK)


# ================================================================== a year up there
def sc_days(c, t, S):
    t90 = ph('every ninety'); t16 = ph('sixteen sunrises')
    sp(c, t, seed=17)
    if t < t16 - 0.2:
        earth_orbit(c, 540, 1200, 300, t)
        top_shade(c, 0.45)
        tier(c, t, S['t0'] + 0.1, 'a year in space? first,', 'NO REAL DAYS', WT_, size=250, t1=t90 - 0.3)
        tier(c, t, t90 - 0.2, 'one lap around Earth:', '90 MINUTES', YEL, size=270)
        return
    draw_planet(c, 'earth', 540, 2150, 900, rot=t * 0.02, glow=(120, 190, 255))
    n = int(16 * eo(pr(t, t16 - 0.2, 1.6)))
    sunrise_ticker(c, 540, 1060, 1.0, n, t)
    top_shade(c, 0.45)
    tier(c, t, t16 - 0.15, 'every single day:', '16 SUNRISES', YEL, size=280)


def sc_life(c, t, S):
    tw = ph('drinking water'); tp = ph('sweat and pee'); tc = ph("yesterday's coffee")
    module_bg(c, t)
    if t < tw - 0.2:
        sleep_bag(c, 540, 1150, 1.1, t)
        top_shade(c, 0.3, (40, 50, 90))
        tier(c, t, S['t0'] + 0.1, 'you sleep in a bag', 'STRAPPED TO A WALL', INK, size=190, small_col=INK)
        return
    water_loop(c, 540, 1180, 1.25, t)
    if t > tc - 0.2:
        pouch(c, 830, 1420, 0.8 * eback(pr(t, tc - 0.2, 0.35), 1.6))
    top_shade(c, 0.3, (40, 50, 90))
    tier(c, t, tw - 0.15, 'your drinking water is', 'RECYCLED', (40, 110, 220), size=280, small_col=INK, t1=tp - 0.4)
    tier(c, t, tp - 0.35, 'yes, including', 'SWEAT AND PEE', RED, size=240, small_col=INK)


def sc_taller(c, t, S):
    ts = ph('spine stretches'); tg = ph('a few centimeters')
    module_bg(c, t, tint=(220, 240, 255))
    k = eo(pr(t, ts, 2.0))
    ruler(c, 760, 1520, 680)
    draw_stick(c, 500, 1520, 2.0, POSES['float'] if k > 0.5 else POSES['stand'], Face('wide', 'grin', 'up') if k > 0.5 else Face('open', 'smile'), t=t, squash=1 + 0.06 * k)
    if t > tg - 0.2: pill(c, 760, 760 + 60, '+ A FEW CM', pr(t, tg - 0.2, 0.35), col=MINT, size=50, txt_col=INK)
    top_shade(c, 0.3, (40, 50, 90))
    tier(c, t, S['t0'] + 0.1, 'your spine stretches, so', 'YOU GET TALLER', (40, 110, 220), size=230, small_col=INK)


def sc_bones(c, t, S):
    te = ph('exercise about two')
    if t < te - 0.2:
        set_bg(c, (90, 40, 120), (170, 90, 200), circle=(210, 150, 240), cy=1150, r=440, spot=True, t=t)
        bone(c, 380, 1180, 1.0, frac=1.0)
        bone(c, 720, 1180, 1.0, frac=1 - 0.8 * eo(pr(t, S['t0'] + 0.6, 3.0)))
        pill(c, 380, 1460, 'EARTH', 1, col=MINT, size=46, txt_col=INK); pill(c, 720, 1460, 'SPACE', 1, col=RED, size=46)
        top_shade(c, 0.4)
        tier(c, t, S['t0'] + 0.1, 'bones and muscles', 'GET WEAKER', YEL, size=280)
        return
    module_bg(c, t)
    treadmill(c, 540, 1500, 1.0, t)
    draw_stick(c, 540, 1480, 1.6, walk_pose(t * 2.2, 1.0, run=True), Face('open', 'chatter', 'angry'), t=t)
    bungee(c, 470, 1180, 300, 1500); bungee(c, 610, 1180, 780, 1500)
    top_shade(c, 0.3, (40, 50, 90))
    tier(c, t, te - 0.15, 'so they exercise', '2 HOURS A DAY', RED, size=270, small_col=INK)


# ================================================================== home
def sc_home(c, t, S):
    t371 = ph('three hundred seventy one'); tl = ph('the longest')
    if t < t371 - 0.3:
        set_bg(c, (120, 190, 255), (255, 220, 160), spot=False, t=t)
        c.drawRect(R.MakeLTRB(0, 1500, W, H), paint((220, 180, 120)))
        k = eo(pr(t, S['t0'], 3.5))
        y = lerp(500, 1440, k)
        parachute(c, 540, y - 330, 1.1, t)
        c.drawLine(470, y - 240, 520, y - 60, stroke(INK, 3)); c.drawLine(610, y - 240, 560, y - 60, stroke(INK, 3))
        c.save(); c.translate(540, y); bell = skia.Path(); bell.moveTo(-50, -70); bell.lineTo(50, -70); bell.lineTo(90, 50); bell.lineTo(-90, 50); bell.close()
        c.drawPath(bell, paint((140, 110, 80))); c.drawPath(bell, stroke(INK, 6)); c.restore()
        calendar(c, 840, 1330, 0.55, 'SEP', '2023')
        top_shade(c, 0.3, (20, 60, 120))
        tier(c, t, S['t0'] + 0.1, 'finally, Frank', 'CAME HOME', WT_, size=290)
        return
    set_bg(c, (40, 60, 170), (110, 130, 240), circle=(160, 180, 255), cy=1150, r=440, spot=True, t=t)
    bigtxt(c, 540, 1100, str(int(371 * eo(pr(t, t371 - 0.3, 1.0)))), 260, YEL)
    pill(c, 540, 1290, 'DAYS IN SPACE', 1, col=INK, size=56)
    if t > tl - 0.1: pill(c, 540, 1440, 'U.S. RECORD', pr(t, tl - 0.1, 0.35), col=RED, size=60)
    top_shade(c, 0.4)
    tier(c, t, tl - 0.1, 'the longest spaceflight', 'BY AN AMERICAN', WT_, size=250)


def sc_dist(c, t, S):
    tm = ph('to the moon and back')
    sp(c, t, seed=21)
    if t < tm - 0.2:
        earth_orbit(c, 540, 1200, 280, t * 3)
        bigtxt(c, 540, 1600 - 120, '~6,000 ORBITS', 90, YEL)
        top_shade(c, 0.45)
        tier(c, t, S['t0'] + 0.1, 'he traveled more than', '250 MILLION KM', WT_, size=210)
        return
    draw_planet(c, 'earth', 220, 1250, 120, rot=t * 0.1, glow=(120, 190, 255))
    draw_planet(c, 'moon', 860, 1250, 70, rot=0)
    k = (t * 2.0) % 1
    x = lerp(340, 790, k if int(t * 2) % 2 == 0 else 1 - k)
    c.drawCircle(x, 1250 - 120 * math.sin(math.pi * k), 12, paint(YEL))
    c.drawLine(340, 1250, 790, 1250, stroke((255, 255, 255), 3, 0.3))
    top_shade(c, 0.45)
    tier(c, t, tm - 0.15, 'like going to the Moon and back', '300+ TIMES', YEL, size=270)


def sc_no(c, t, S):
    tn = ph('would have said no')
    set_bg(c, (40, 180, 200), (130, 225, 235), circle=(210, 250, 255), cy=1150, r=440, spot=True, t=t)
    draw_stick(c, 400, 1520, 1.9, POSES['shrug'], Face('happy', 'grin'), t=t)
    speech(c, 760, 960, 360, 190, 'NO THANKS', pr(t, tn - 0.3, 0.35), size=80, col=INK)
    top_shade(c, 0.3, (0, 60, 80))
    tier(c, t, S['t0'] + 0.1, 'if asked for a full year,', "HE'D SAY NO", INK, size=270, small_col=INK)


def sc_ask(c, t, S):
    sp(c, t, seed=25)
    draw_planet(c, 'earth', 540, 2150, 900, rot=t * 0.02, glow=(120, 190, 255))
    iss(c, 540, 1050, 0.75, t)
    astro(c, 380, 1450, 1.0, POSES['wave'], Face('happy', 'grin'), t, rot=6 * math.sin(t))
    comment_bubble(c, 780, 1280, 0.75, pr(t, ph('comments') - 0.2, 0.35))
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'would you take the deal?', '1 YEAR IN SPACE', YEL, size=230)
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint((8, 10, 40)))


from meteorprops import speech, medal

SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='launch', t0=ph('he launched') - 0.2, fn=sc_launch, tin='flash'),
    dict(k='hit', t0=ph('but in december') - 0.2, fn=sc_hit, tin='whip'),
    dict(k='nosafe', t0=ph('without that coolant') - 0.2, fn=sc_nosafe, tin='wipe', col=(255, 130, 100)),
    dict(k='wait', t0=ph('a new capsule') - 0.2, fn=sc_wait, tin='zoom'),
    dict(k='days', t0=ph("so what's a year") - 0.2, fn=sc_days, tin='wipe', col=(40, 30, 90)),
    dict(k='life', t0=ph("you don't sleep") - 0.2, fn=sc_life, tin='whip'),
    dict(k='taller', t0=ph('and your body starts') - 0.2, fn=sc_taller, tin='zoom'),
    dict(k='bones', t0=ph("but it's not all fun") - 0.2, fn=sc_bones, tin='wipe', col=(170, 90, 200)),
    dict(k='home', t0=ph('finally in september') - 0.2, fn=sc_home, tin='flash'),
    dict(k='dist', t0=ph("he'd gone around") - 0.2, fn=sc_dist, tin='whip'),
    dict(k='no', t0=ph('and the funny part') - 0.2, fn=sc_no, tin='wipe', col=(130, 225, 235)),
    dict(k='ask', t0=ph('so would you take') - 0.2, fn=sc_ask, tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('tiny space rock') + 0.9, 16, 0.4); EP.flash(ph('tiny space rock') + 0.9, 0.3, 0.12, (255, 230, 160))
EP.shk(ph('the answer was no'), 10, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
