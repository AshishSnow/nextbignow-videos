"""What if you were left alone on an island? — episode 40 (Alexander Selkirk, Más a Tierra, 1704 - 2 Feb 1709)."""
import sys, os, math, re
import skia
from islandprops import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('IS_DIR', 'island'))
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


def top_shade(c, a=0.45, col=(10, 30, 60)):
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


# ================================================================== intro
def sc_hook(c, t, S):
    to = ph('your own idea'); tn = ph('alexander selkirk'); tb = ph('famous books')
    beach(c, t)
    k = pr(t, 0.3, 6.0)
    tall_ship(c, lerp(700, 1000, k), 1010, lerp(0.5, 0.3, k), t)
    selkirk(c, 480, 1520, 1.8, POSES['wave'] if t < to else POSES['shrug'], Face('open', 'smile') if t < to else Face('happy', 'grin'), t)
    if t > tb - 0.2: book_cover(c, 830, 1300, 0.55, pr(t, tb - 0.2, 0.4))
    top_shade(c, 0.5)
    tier(c, t, 0.0, 'what if you got', 'LEFT ON AN ISLAND', YEL, size=220, t1=to - 0.3)
    tier(c, t, to - 0.2, '...and it was', 'YOUR OWN IDEA?', WT_, size=230, t1=tn - 0.3)
    tier(c, t, tn - 0.2, 'Scottish sailor', 'ALEXANDER SELKIRK', YEL, size=170)


def sc_ship(c, t, S):
    td = ph('drop me off')
    ocean(c, t, hy=1150, sky=((90, 150, 230), (200, 225, 255)), sun=False)
    tall_ship(c, 560, 1250, 0.9, t, damaged=1.0)
    calendar(c, 230, 1420, 0.55, 'YEAR', '1704')
    if t > td - 0.3:
        speech(c, 400, 880, 480, 150, 'DROP ME OFF!', pr(t, td - 0.3, 0.35), size=76, col=RED)
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'he was sure the ship was', 'FALLING APART', WT_, size=230)


def sc_fine(c, t, S):
    tc = ph('off the coast')
    ocean(c, t, hy=1000, sky=((100, 170, 240), (220, 240, 255)), sun=False)
    island(c, 330, 1300, 1.3, t)
    k = pr(t, S['t0'] + 0.4, 5.0)
    tall_ship(c, lerp(760, 1150, k), 1120, 0.45, t)
    selkirk(c, 300, 1290, 0.7, POSES['shock'], Face('wide', 'o', 'worried'), t)
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'the captain said...', 'FINE', YEL, size=300, t1=tc - 0.3)
    tier(c, t, tc - 0.2, 'left on a tiny island off', 'CHILE', WT_, size=300)


def sc_items(c, t, S):
    tr = ph('regretted it'); tn = ph('the answer was no')
    if t < tr - 0.2:
        set_bg(c, (255, 150, 60), (255, 210, 130), circle=(255, 235, 190), cy=1150, r=440, spot=True, t=t)
        for i, (p_, kind) in enumerate((('a hatchet', 'hatchet'), ('a knife', 'knife'), ('cooking pot', 'pot'), ('a bible', 'book'))):
            k = pr(t, ph(p_) - 0.2, 0.35)
            if k <= 0: continue
            x = 330 + (i % 2) * 420; y = 1000 + (i // 2) * 360
            card3d(c, x, y, 300, 300, 8 * math.sin(t + i), 0, lambda cc, kind=kind: item_icon(cc, kind, 1.2), k=k)
        top_shade(c, 0.3, (120, 50, 0))
        tier(c, t, S['t0'] + 0.1, 'all he got:', 'A FEW TOOLS', INK, size=270, small_col=INK)
        return
    ocean(c, t, hy=1000, sky=((100, 170, 240), (220, 240, 255)), sun=False)
    tall_ship(c, 820, 1100, 0.5, t)
    selkirk(c, 380, 1420, 1.5, POSES['arms_up'], Face('wide', 'o', 'worried'), t)
    wave_front(c, t, 1350, 20, (40, 120, 200), 0.9)
    if t > tn - 0.1: no_stamp(c, 800, 1000, 0.9, pr(t, tn - 0.1, 0.3))
    top_shade(c, 0.45)
    tier(c, t, tr - 0.1, 'he begged to', 'COME BACK', WT_, size=290, t1=tn - 0.3)
    tier(c, t, tn - 0.2, 'the answer:', 'NO', RED, size=300)


def sc_twist(c, t, S):
    ts = ph('it sank')
    ocean(c, t, hy=1000, sky=((60, 70, 130), (140, 140, 200)), sun=False)
    tall_ship(c, 540, 1150, 0.9, t, damaged=1.0, sink=eio(pr(t, ts - 0.2, 2.5)))
    wave_front(c, t, 1180, 30, (30, 90, 170), 1.0)
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'the twist?', 'HE WAS RIGHT', YEL, size=290, t1=ts - 0.3)
    tier(c, t, ts - 0.2, 'not long after,', 'THE SHIP SANK', WT_, size=250)


# ================================================================== surviving
def sc_lions(c, t, S):
    ti = ph('moved inland')
    if t < ti - 0.2:
        beach(c, t)
        for i, x in enumerate((640, 820)):
            sea_lion(c, x, 1480 + i * 40, 1.2, t, roar=cl((math.sin(t * 4 + i * 2) + 0.2)), flip=True)
        selkirk(c, 280, 1500, 1.5, POSES['hug'], Face('closed', 'frown', 'angry'), t)
        top_shade(c, 0.45)
        tier(c, t, S['t0'] + 0.1, 'the beach belonged to', 'SEA LIONS', WT_, size=290)
        return
    jungle(c, t)
    selkirk(c, lerp(200, 540, eo(pr(t, ti, 2.0))), 1500, 1.6, walk_pose(t * 1.4, 0.8), Face('open', 'smile'), t)
    top_shade(c, 0.4, (10, 50, 20))
    tier(c, t, ti - 0.1, 'so he', 'MOVED INLAND', WT_, size=280)


def sc_goats(c, t, S):
    tc = ph('chased them down'); to = ph('outrun them')
    jungle(c, t)
    if t < tc - 0.2:
        goat(c, 400, 1480, 1.1, t); goat(c, 760, 1500, 0.9, t, flip=True)
        top_shade(c, 0.4, (10, 50, 20))
        tier(c, t, S['t0'] + 0.1, 'the island had', 'WILD GOATS', WT_, size=280)
        return
    run = (t * 520) % 1500 - 300
    goat(c, run + 260, 1500, 1.0, t, run=1.0)
    selkirk(c, run, 1500, 1.4, walk_pose(t * 2.6, 1.2, run=True), Face('open', 'grin', 'angry'), t, beard=0.3)
    speed_lines(c, t, a=0.6, n=14, y0=1100, y1=1500, col=(255, 255, 255))
    top_shade(c, 0.4, (10, 50, 20))
    tier(c, t, tc - 0.1, 'out of gunpowder, he', 'CHASED THEM', YEL, size=290, t1=to - 0.5)
    tier(c, t, to - 0.4, 'he got so fast he could', 'OUTRUN GOATS', WT_, size=230)


def sc_rats(c, t, S):
    tc = ph('tamed the wild cats')
    set_bg(c, (20, 30, 70), (50, 60, 120), spot=False, t=t)
    for i in range(30):
        c.drawCircle(hsh(i, 2) * W, 300 + hsh(i, 3) * 500, 2 + 2 * hsh(i, 4), paint((255, 255, 255), 0.6))
    c.drawCircle(830, 1000, 70, paint((250, 245, 210)))
    c.drawRect(R.MakeLTRB(0, 1450, W, H), paint((60, 90, 60)))
    selkirk(c, 540, 1480, 1.3, POSES['sit'], Face('closed', 'flat') if t < tc else Face('happy', 'smile'), t, beard=0.4)
    if t < tc - 0.1:
        for i, x in enumerate((300, 780, 880)):
            rat(c, x + 20 * math.sin(t * 2 + i), 1490, 1.0, t, flip=i > 0)
    else:
        k = pr(t, tc - 0.1, 0.6)
        for i, (x, fl) in enumerate(((290, False), (800, True), (420, False), (690, True))):
            cat(c, x, 1500, 0.75 * eback(cl(k * 1.5 - i * 0.15), 1.5), t, face='happy', flip=fl)
    top_shade(c, 0.4)
    tier(c, t, S['t0'] + 0.1, 'then came the', 'RATS', (255, 170, 160), size=300, t1=tc - 0.3)
    tier(c, t, tc - 0.2, 'his fix: wild cats as', 'BODYGUARDS', YEL, size=270)


def sc_skins(c, t, S):
    set_bg(c, (190, 120, 60), (240, 190, 120), circle=(255, 225, 170), cy=1150, r=440, spot=True, t=t)
    k = eo(pr(t, S['t0'] + 0.5, 1.0))
    selkirk(c, 540, 1520, 2.0, POSES['wave'], Face('happy', 'grin'), t, goat=k, beard=0.6)
    top_shade(c, 0.35, (100, 40, 0))
    tier(c, t, S['t0'] + 0.1, 'new clothes, sewn with a nail:', 'GOAT SKINS', WT_, size=290)


def sc_spanish(c, t, S):
    tt = ph('climbed a tree')
    if t < tt - 0.2:
        ocean(c, t, hy=1150, sky=((100, 170, 240), (220, 240, 255)), sun=False)
        tall_ship(c, 560, 1250, 0.8, t, flag=(250, 200, 40))
        top_shade(c, 0.45)
        tier(c, t, S['t0'] + 0.1, 'ships came... but they were', 'SPANISH', YEL, size=290)
        return
    jungle(c, t)
    tree(c, 540, 1450, 3.2, seed=9, col=(40, 140, 70))
    selkirk(c, 560, 1050, 1.0, POSES['hug'], Face('wide', 'flat', 'worried'), t, goat=1.0, beard=0.6)
    for i, x in enumerate((180, 880)):
        draw_stick(c, x, 1520, 1.2, walk_pose(t * 1.2 + i, 0.7), Face('open', 'frown', 'angry'), t=t, scarf=(250, 200, 40), flip=i == 1)
    top_shade(c, 0.4, (10, 50, 20))
    tier(c, t, tt - 0.15, 'so he hid', 'UP A TREE', WT_, size=290)


def sc_rescue(c, t, S):
    tw = ph('looked wilder'); t4 = ph('four years and four')
    beach(c, t)
    k = eo(pr(t, S['t0'], 3.0))
    tall_ship(c, lerp(1150, 760, k), 1010, 0.45, t, flag=(40, 80, 200))
    calendar(c, 300, 920, 0.5, 'FEB', '1709')
    selkirk(c, 480, 1520, 1.9, POSES['arms_up'], Face('happy', 'grin'), t, goat=1.0, beard=1.0)
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'in 1709 a British ship', 'FINALLY CAME', WT_, size=250, t1=tw - 0.4)
    tier(c, t, tw - 0.3, 'he looked wilder than', 'THE GOATS', YEL, size=290, t1=t4 - 0.3)
    tier(c, t, t4 - 0.2, 'alone for', '4 YEARS, 4 MONTHS', WT_, size=200)


def sc_book(c, t, S):
    set_bg(c, (90, 50, 140), (170, 100, 220), circle=(210, 160, 250), cy=1150, r=440, spot=True, t=t)
    book_cover(c, 540, 1200, 1.15, pr(t, ph('robinson crusoe') - 0.3, 0.5))
    top_shade(c, 0.4)
    tier(c, t, S['t0'] + 0.1, 'ten years later, Defoe wrote', 'ROBINSON CRUSOE', YEL, size=210)


def sc_ask(c, t, S):
    tq = ph('could you last')
    ocean(c, t, hy=1100, sky=((255, 170, 110), (255, 220, 170)), sun=False)
    island(c, 540, 1350, 1.6, t)
    if t < tq - 0.2:
        c.save(); c.translate(540, 1150)
        c.drawLine(0, 0, 0, 160, stroke((120, 80, 40), 14))
        c.drawRoundRect(R.MakeXYWH(-230, -70, 460, 110), 14, 14, paint((200, 150, 90))); c.drawRoundRect(R.MakeXYWH(-230, -70, 460, 110), 14, 14, stroke(INK, 6))
        f = font('ant', 50); s_ = 'ROBINSON CRUSOE ISLAND'; c.drawString(s_, -f.measureText(s_) / 2, 0, f, paint(INK))
        c.restore()
        top_shade(c, 0.4, (120, 40, 0))
        tier(c, t, S['t0'] + 0.1, 'today the island is called', 'ROBINSON CRUSOE', WT_, size=200)
    else:
        selkirk(c, 450, 1340, 0.9, POSES['wave'], Face('happy', 'grin'), t, goat=1.0, beard=0.8)
        comment_bubble(c, 780, 1050, 0.75, pr(t, ph('comments') - 0.2, 0.35))
        top_shade(c, 0.4, (120, 40, 0))
        tier(c, t, tq - 0.1, 'could you last', '4 YEARS ALONE?', YEL, size=250)
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint((10, 30, 60)))


from spinprops import speed_lines

SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='ship', t0=ph('it was seventeen') - 0.2, fn=sc_ship, tin='whip'),
    dict(k='fine', t0=ph('the captain said') - 0.2, fn=sc_fine, tin='zoom'),
    dict(k='items', t0=ph('he got a musket') - 0.2, fn=sc_items, tin='wipe', col=(255, 190, 110)),
    dict(k='twist', t0=ph("but here's the twist") - 0.2, fn=sc_twist, tin='flash'),
    dict(k='lions', t0=ph("so now he's alone") - 0.2, fn=sc_lions, tin='wipe', col=(245, 220, 160)),
    dict(k='goats', t0=ph('the island had wild') - 0.2, fn=sc_goats, tin='whip'),
    dict(k='rats', t0=ph('then the rats') - 0.2, fn=sc_rats, tin='zoom'),
    dict(k='skins', t0=ph('when his clothes') - 0.2, fn=sc_skins, tin='wipe', col=(240, 190, 120)),
    dict(k='spanish', t0=ph('twice ships') - 0.2, fn=sc_spanish, tin='whip'),
    dict(k='rescue', t0=ph('finally in february') - 0.2, fn=sc_rescue, tin='flash'),
    dict(k='book', t0=ph('ten years later') - 0.2, fn=sc_book, tin='wipe', col=(170, 100, 220)),
    dict(k='ask', t0=ph('today that island') - 0.2, fn=sc_ask, tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('the answer was no'), 10, 0.3)
EP.shk(ph('it sank'), 12, 0.35)

if __name__ == '__main__':
    EP.main(sys.argv)
