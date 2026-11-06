"""What if you were trapped at the bottom of the sea? — episode 38 (Harrison Okene, tug Jascon-4, off Nigeria, May 2013)."""
import sys, os, math, re
import skia
from bubbleprops import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('BB_DIR', 'bubble'))
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


def top_shade(c, a=0.45, col=(5, 15, 40)):
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


def head_in_bubble(c, x, y, s, t, face):
    """Harrison chest-deep in water, head up in the air pocket (draw before pocket_room water? no: after, then water overlay)."""
    harrison(c, x, y, s, POSES['hug'], face, t)


# ================================================================== intro
def sc_hook(c, t, S):
    tf = ph('flipped over'); tsk = ph('and sank'); tn = ph('no way out'); th = ph('harrison okene')
    if t < tn - 0.1:
        ocean(c, t, hy=1150, sky=((60, 80, 150), (150, 150, 210)), sun=False)
        k = eio(pr(t, tf - 0.1, 0.8)); ks = eio(pr(t, tsk, 1.5))
        tug(c, 540, 1130 + 500 * ks, 0.95, t, rot=180 * k)
        wave_front(c, t, 1180, 26, (30, 100, 180), 0.9)
        top_shade(c, 0.5)
        tier(c, t, 0.0, 'what if your ship', 'FLIPPED AND SANK', WT_, size=230, t1=tn - 0.3)
        return
    deep_bg(c, t, 0.85, bubbles=6)
    if t < th - 0.2:
        harrison(c, 540, 1520, 1.9, POSES['shock'], Face('wide', 'o', 'worried'), t)
        c.drawRect(R.MakeWH(W, H), paint((0, 0, 10), 0.55))
        top_shade(c, 0.3)
        tier(c, t, tn - 0.05, 'no way out.', 'PITCH BLACK', WT_, size=270)
        return
    harrison(c, 540, 1520, 1.9, POSES['stand'], Face('open', 'smile'), t)
    pill(c, 540, 1610, "SHIP'S COOK", pr(t, th, 0.35), col=ORANGE, size=56)
    top_shade(c, 0.3)
    tier(c, t, th - 0.15, 'it happened to', 'HARRISON OKENE', YEL, size=200)


def sc_wave(c, t, S):
    tw = ph('a huge wave'); tb = ph('in the bathroom')
    if t < tb - 0.2:
        ocean(c, t, hy=1150, sky=((20, 24, 70), (60, 60, 120)), sun=False, night=0.8)
        k = pr(t, tw, 1.4)
        if t > tw - 0.2: big_wave(c, t, k * (1 - 0.6 * cl((k - 0.5) / 0.5)))
        tug(c, 560, 1130, 0.95, t, rot=lerp(0, 180, eio(cl((k - 0.35) / 0.65))))
        wave_front(c, t, 1180, 26, (30, 100, 180), 0.9)
        calendar(c, 820, 900, 0.55, 'MAY', '2013')
        top_shade(c, 0.5)
        tier(c, t, S['t0'] + 0.1, 'off Nigeria, at', '4:30 AM', WT_, size=280, t1=tw - 0.3)
        tier(c, t, tw - 0.2, 'a huge wave', 'FLIPPED THE BOAT', YEL, size=210)
        return
    set_bg(c, (90, 150, 200), (160, 210, 240), spot=True, t=t)
    c.save(); c.translate(540, 1150); c.rotate(14 * math.sin(t * 3)); c.translate(-540, -1150)
    c.drawRoundRect(R.MakeXYWH(220, 830, 640, 720), 30, 30, stroke(INK, 10))
    harrison(c, 540, 1520, 1.8, POSES['shock'], Face('wide', 'o', 'worried'), t, rot=10 * math.sin(t * 4))
    c.restore()
    top_shade(c, 0.4)
    tier(c, t, tb - 0.15, 'he was in the bathroom, in', 'JUST HIS SHORTS', WT_, size=210)


def sc_sink(c, t, S):
    u = t - S['t0']
    k = eo(pr(t, S['t0'], max(2.0, ph('upside down', after=S['t0']) - S['t0'] + 0.5)))
    deep_bg(c, t, 0.3 + 0.4 * k, bubbles=10)
    seafloor(c, lerp(2200, 1480, k), t)
    tug(c, 540, lerp(700, 1400, k), 0.9, t, rot=180 + 4 * math.sin(t), lights=False)
    depth_meter(c, t, k, '%d M' % int(30 * k))
    top_shade(c, 0.35)
    tier(c, t, S['t0'] + 0.1, 'it sank', '30 METERS DOWN', WT_, size=220)


# ================================================================== the bubble
def sc_pocket(c, t, S):
    tf = ph('found something'); tp = ph('a pocket of air'); tm = ph('just over a meter')
    found = t > tp - 0.2
    pocket_room(c, t, water_y=1150 if found else 900, air_top=760 if found else 760, dark=0.0 if found else 0.35)
    if found:
        c.drawRect(R.MakeLTRB(0, 760, W, 1150), paint((200, 240, 255), 0.18 * pr(t, tp - 0.2, 0.5)))
        harrison(c, 420, 1400, 1.5, POSES['hug'], Face('wide', 'o', 'up'), t)
        pocket_room_water = True
        wp = skia.Path(); wp.moveTo(-20, H + 20); wp.lineTo(-20, 1150)
        for i in range(0, W + 41, 30): wp.lineTo(i, 1150 + 10 * math.sin(i * 0.02 + t * 2))
        wp.lineTo(W + 20, H + 20); wp.close()
        c.drawPath(wp, paint((30, 90, 150), 0.82)); c.drawPath(wp, stroke((140, 200, 255), 4, 0.7))
        if t > tm - 0.2:
            k = eo(pr(t, tm - 0.2, 0.5))
            c.drawLine(800, 770, 800, 770 + 380 * k, stroke(YEL, 8))
            c.drawLine(770, 770, 830, 770, stroke(YEL, 8)); c.drawLine(770, 770 + 380 * k, 830, 770 + 380 * k, stroke(YEL, 8))
            pill(c, 800, 960, '~1.2 M', k, col=INK, size=50, txt_col=YEL)
    else:
        harrison(c, lerp(200, 520, cl((t - S['t0']) / 3)), 1300, 1.4, walk_pose(t * 1.2, 0.6), Face('open', 'frown', 'worried'), t)
        wp = skia.Path(); wp.moveTo(-20, H + 20); wp.lineTo(-20, 1050)
        for i in range(0, W + 41, 30): wp.lineTo(i, 1050 + 14 * math.sin(i * 0.02 + t * 3))
        wp.lineTo(W + 20, H + 20); wp.close()
        c.drawPath(wp, paint((30, 90, 150), 0.85))
        for i in range(8):
            ph_ = (t * 1.2 + i / 8) % 1
            c.drawLine(100 + i * 120, 760 + ph_ * 300, 100 + i * 120, 820 + ph_ * 300, stroke((150, 210, 255), 8, 1 - ph_))
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'water was', 'POURING IN', SKY, size=270, t1=tp - 0.3)
    tier(c, t, tp - 0.2, 'then he found', 'A POCKET OF AIR', YEL, size=220)


def sc_wait(c, t, S):
    tw = ph('and waited')
    pocket_room(c, t, water_y=1150, air_top=760)
    c.drawRect(R.MakeLTRB(0, 760, W, 1150), paint((200, 240, 255), 0.15))
    harrison(c, 540, 1400, 1.5, POSES['hug'], Face('open', 'flat', 'worried'), t)
    wp = skia.Path(); wp.moveTo(-20, H + 20); wp.lineTo(-20, 1150)
    for i in range(0, W + 41, 30): wp.lineTo(i, 1150 + 10 * math.sin(i * 0.02 + t * 2))
    wp.lineTo(W + 20, H + 20); wp.close()
    c.drawPath(wp, paint((30, 90, 150), 0.82)); c.drawPath(wp, stroke((140, 200, 255), 4, 0.7))
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'he stuck his head in the bubble', 'AND WAITED', WT_, size=250)


# ================================================================== science
def bubble_dome(c, t, k_co2=0.0, k_o2=0.0, squeeze=0.0, dissolve=0.0):
    set_bg(c, (20, 70, 140), (50, 130, 210), spot=True, t=t)
    cx, cy, r = 540, 1150, 330 * (1 - 0.18 * squeeze)
    c.drawCircle(cx, cy, r, paint((210, 240, 255), 0.85)); c.drawCircle(cx, cy, r, stroke((255, 255, 255), 8))
    c.drawCircle(cx - r * 0.4, cy - r * 0.45, r * 0.18, paint((255, 255, 255), 0.6))
    n = int(14 * k_co2)
    for i in range(n):
        a = hsh(i, 2) * 6.283; rr = r * 0.75 * math.sqrt(hsh(i, 3))
        y_off = 260 * dissolve * hsh(i, 5) if i % 2 == 0 else 0
        molecule(c, cx + math.cos(a) * rr + 6 * math.sin(t * 2 + i), cy + math.sin(a) * rr + y_off, 0.55, 'co2', 1 - (dissolve if i % 2 == 0 else 0))
    for i in range(int(12 * k_o2)):
        a = hsh(i, 7) * 6.283; rr = r * 0.7 * math.sqrt(hsh(i, 8))
        molecule(c, cx + math.cos(a) * rr + 6 * math.sin(t * 2.4 + i), cy + math.sin(a) * rr, 0.5, 'o2')
    if squeeze > 0:
        for i in range(8):
            a = i / 8 * 6.283; d = r + 70 + 15 * math.sin(t * 8)
            x0, y0 = cx + math.cos(a) * d, cy + math.sin(a) * d
            c.save(); c.translate(x0, y0); c.rotate(math.degrees(a) + 180)
            c.drawPath(poly([(0, -26), (60, 0), (0, 26)], True), paint(YEL, squeeze)); c.restore()
    if dissolve > 0:
        c.drawRect(R.MakeLTRB(0, cy + r * 0.6, W, H), paint((30, 90, 160), 0.6))


def sc_co2(c, t, S):
    tc = ph('carbon dioxide'); tk = ph('can kill you')
    bubble_dome(c, t, k_co2=pr(t, tc - 0.3, max(1.0, tk - tc + 0.5)))
    harrison(c, 540, 1420, 1.0, POSES['hug'], Face('open', 'flat', 'worried') if t < tk else Face('wide', 'o', 'worried'), t)
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'every breath adds', 'CARBON DIOXIDE', WT_, size=210, t1=tk - 0.3)
    tier(c, t, tk - 0.2, 'too much of it', 'CAN KILL YOU', RED, size=250)


def sc_lucky(c, t, S):
    tp = ph('water pressure'); ts = ph('splashing water')
    bubble_dome(c, t, k_co2=1.0, k_o2=pr(t, ph('more oxygen') - 0.3, 0.8), squeeze=pr(t, tp, 0.6) * (1 - pr(t, ts - 0.3, 0.4)),
                dissolve=pr(t, ts, 1.4))
    harrison(c, 540, 1420, 1.0, POSES['hug'], Face('open', 'smile'), t)
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'but he got', 'LUCKY', YEL, size=300, t1=tp - 0.3)
    tier(c, t, tp - 0.2, 'pressure packed in', 'MORE OXYGEN', SKY, size=250, t1=ts - 0.3)
    tier(c, t, ts - 0.2, 'and the water soaked up', 'SOME CO2', MINT, size=260)


def sc_cold(c, t, S):
    tm = ph('pulled a mattress')
    pocket_room(c, t, water_y=1250, air_top=760)
    if t < tm - 0.1:
        thermometer(c, 820, 1350, 0.9, 0.15, col=(80, 160, 250))
        harrison(c, 420, 1500, 1.5, POSES['hug'], Face('open', 'chatter', 'worried'), t, rot=3 * math.sin(t * 30))
    else:
        mattress_raft(c, 540, 1260, 1.3)
        harrison(c, 540, 1230, 1.5, POSES['sit'], Face('open', 'smile'), t)
    wp = skia.Path(); wp.moveTo(-20, H + 20); wp.lineTo(-20, 1250)
    for i in range(0, W + 41, 30): wp.lineTo(i, 1250 + 10 * math.sin(i * 0.02 + t * 2))
    wp.lineTo(W + 20, H + 20); wp.close()
    c.drawPath(wp, paint((30, 90, 150), 0.7 if t > tm else 0.82)); c.drawPath(wp, stroke((140, 200, 255), 4, 0.7))
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'then there was', 'THE COLD', SKY, size=290, t1=tm - 0.3)
    tier(c, t, tm - 0.2, 'so he built a', 'MATTRESS PLATFORM', YEL, size=200)


def sc_items(c, t, S):
    td = ph('total darkness')
    items = [('bottle of', soda_bottle, 260), ('life jacket', life_vest, 540), ('tiny flashlights', flashlight, 820)]
    set_bg(c, (40, 30, 80), (90, 70, 150), circle=(130, 110, 200), cy=1150, r=440, spot=True, t=t)
    for i, (p_, fn, x) in enumerate(items):
        k = pr(t, ph(p_) - 0.2, 0.35)
        if k <= 0: continue
        def dr(cc, fn=fn):
            if fn is soda_bottle: soda_bottle(cc, 0, 30, 0.75)
            elif fn is life_vest: life_vest(cc, 0, 20, 0.7)
            else: flashlight(cc, -20, 0, 0.9, rot=-30, on=0.0)
        card3d(c, x, 1180, 240, 320, 8 * math.sin(t + i), 0, dr, k=k)
    if t > td - 0.2:
        c.drawRect(R.MakeWH(W, H), paint((0, 0, 8), 0.85 * pr(t, td - 0.2, 0.8)))
        flashlight(c, 300, 1200, 1.0, rot=-15, on=0.5 + 0.5 * (math.sin(t * 9) > -0.6))
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'all he had:', 'COLA, A VEST, 2 LIGHTS', WT_, size=170, t1=td - 0.3)
    tier(c, t, td - 0.2, 'and', 'TOTAL DARKNESS', WT_, size=250)


# ================================================================== rescue
def sc_divers(c, t, S):
    tb = ph("weren't looking")
    deep_bg(c, t, 0.7, bubbles=16)
    k = eo(pr(t, S['t0'], 3.0))
    for i, (x, dl) in enumerate(((400, 0.0), (700, 0.4))):
        diver(c, x, lerp(400, 1000, k) + 80 * i, 1.1, POSES['float'], Face('open', 'flat'), t, rot=150, light=1.0)
    seafloor(c, 1520, t)
    tug(c, 540, 1500, 0.8, t, rot=180, lights=False)
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'almost 3 days later,', 'DIVERS CAME DOWN', WT_, size=220, t1=tb - 0.3)
    tier(c, t, tb - 0.2, 'not to rescue, but to', 'RECOVER BODIES', (255, 170, 160), size=220)


def sc_hand(c, t, S):
    tg = ph('a hand grabbed'); ta = ph('harrison was alive')
    pocket_room(c, t, water_y=600, air_top=500, dark=0.55)
    k = eo(pr(t, S['t0'], 2.0))
    diver(c, lerp(-100, 430, k), 1350, 1.4, (0, 0, 120, 0, 90, -10, 190, 10, 170, 10), Face('open', 'flat'), t, rot=-80, light=1.0)
    if t > tg - 0.2:
        kk = eback(pr(t, tg - 0.2, 0.3), 1.8)
        hand(c, 700, 1150, 1.4 * kk, rot=-100)
        c.drawCircle(700, 1150, 140, paint((255, 245, 190), 0.25 * kk, blur=30))
    if t > ta - 0.1:
        for i in range(14):
            ph_ = (t * 0.6 + i / 14) % 1
            c.drawCircle(hsh(i, 2) * W, 1500 - ph_ * 900, 6 + 8 * hsh(i, 3), stroke((255, 255, 255), 3, 1 - ph_))
    top_shade(c, 0.5)
    tier(c, t, tg - 0.15, 'then', 'A HAND GRABBED HIS', YEL, size=200, t1=ta - 0.3)
    tier(c, t, ta - 0.2, 'Harrison was', 'ALIVE!', MINT, size=300)


def sc_chamber(c, t, S):
    td = ph('decompression chamber')
    if t < td - 0.6:
        deep_bg(c, t, 0.55, bubbles=20)
        harrison(c, 540, 1500, 1.6, POSES['arms_up'], Face('happy', 'grin'), t)
        top_shade(c, 0.45)
        tier(c, t, S['t0'] + 0.1, 'after about', '60 HOURS UNDERWATER', WT_, size=180, t1=td - 0.7)
        return
    set_bg(c, (40, 160, 200), (130, 220, 240), circle=(210, 250, 255), cy=1150, r=450, spot=True, t=t)
    chamber(c, 540, 1180, 1.05, t, inside=lambda cc: (cc.drawCircle(0, 0, 200, paint((150, 210, 250))),
                                                      harrison(cc, 0, 190, 0.9, POSES['wave'], Face('happy', 'smile'), t)))
    top_shade(c, 0.35, (0, 60, 80))
    tier(c, t, td - 0.55, 'first, a slow return in a', 'DECOMPRESSION CHAMBER', WT_, size=150)


def sc_ask(c, t, S):
    t3 = ph('almost three', after=S['t0']); tq = ph('if you were stuck')
    if t < tq - 0.2:
        set_bg(c, (255, 150, 60), (255, 210, 130), circle=(255, 235, 190), cy=1150, r=440, spot=True, t=t)
        calendar(c, 330, 1150, 0.75, 'HE GUESSED', '1 DAY')
        if t > t3 - 0.2:
            calendar(c, 750, 1150, 0.75 * eback(pr(t, t3 - 0.2, 0.35), 1.6), 'REALITY', '3 DAYS', col=RED)
        top_shade(c, 0.3, (120, 50, 0))
        tier(c, t, S['t0'] + 0.1, 'he thought he was down there', 'ONE DAY', INK, size=260, small_col=INK)
        return
    deep_bg(c, t, 0.6, bubbles=18)
    c.drawCircle(540, 1150, 280, paint((210, 240, 255), 0.85)); c.drawCircle(540, 1150, 280, stroke((255, 255, 255), 8))
    harrison(c, 460, 1400, 1.1, POSES['wave'], Face('happy', 'grin'), t)
    comment_bubble(c, 780, 1000, 0.75, pr(t, ph('comments') - 0.2, 0.35))
    top_shade(c, 0.5)
    tier(c, t, tq - 0.1, 'stuck in the bubble,', 'WHAT DO YOU DO FIRST?', YEL, size=170)
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint((5, 15, 40)))


SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='wave', t0=ph('it was may') - 0.2, fn=sc_wave, tin='whip'),
    dict(k='sink', t0=ph('the boat sank') - 0.2, fn=sc_sink, tin='zoom'),
    dict(k='pocket', t0=ph('water was pouring') - 0.2, fn=sc_pocket, tin='wipe', col=(50, 44, 60)),
    dict(k='wait', t0=ph('so he did the only') - 0.2, fn=sc_wait, tin='zoom'),
    dict(k='co2', t0=ph("now here's the scary") - 0.2, fn=sc_co2, tin='wipe', col=(40, 100, 180)),
    dict(k='lucky', t0=ph('but harrison got lucky') - 0.2, fn=sc_lucky, tin='flash'),
    dict(k='cold', t0=ph('then there was the cold') - 0.2, fn=sc_cold, tin='whip'),
    dict(k='items', t0=ph('all he had') - 0.2, fn=sc_items, tin='wipe', col=(80, 60, 140)),
    dict(k='divers', t0=ph('almost three days later') - 0.2, fn=sc_divers, tin='zoom'),
    dict(k='hand', t0=ph('one diver swam') - 0.2, fn=sc_hand, tin='whip'),
    dict(k='chamber', t0=ph('after about sixty') - 0.2, fn=sc_chamber, tin='flash'),
    dict(k='ask', t0=ph("he thought he'd") - 0.2, fn=sc_ask, tin='wipe', col=(255, 190, 110)),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('a huge wave') + 0.6, 16, 0.5)
EP.shk(ph('a hand grabbed'), 14, 0.35); EP.flash(ph('a hand grabbed'), 0.3, 0.12, (255, 255, 230))
EP.shk(ph('can kill you'), 8, 0.25)

if __name__ == '__main__':
    EP.main(sys.argv)
