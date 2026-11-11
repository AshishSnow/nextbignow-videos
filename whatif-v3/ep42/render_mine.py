"""What if you were trapped 700 m underground? — episode 42 (San José mine, Atacama, Chile: 5 Aug - 13 Oct 2010, 33 miners, 69 days)."""
import sys, os, math, re
import skia
from mineprops import *
from engine import Episode, load_words, HERE
from trenchprops import depth_meter

D = os.path.join(HERE, os.environ.get('MN_DIR', 'mine'))
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


def top_shade(c, a=0.45, col=(30, 15, 5)):
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


def crowd(c, cx, cy, n, s, t, t0=0.0, seed=1, shades=0.0, cheer=False):
    for i in range(n):
        col_ = i % 8; row = i // 8
        x = cx - 330 + col_ * 95 + (row % 2) * 45; y = cy - row * 70
        miner(c, x, y, s, POSES['arms_up'] if cheer and (int(t * 3) + i) % 2 else POSES['stand'], Face('happy', 'grin') if cheer else Face('open', 'flat', 'worried'), t, shades=shades, beard=0.3)


# ================================================================== intro
def sc_hook(c, t, S):
    t33 = ph('thirty three miners'); t69 = ph('sixty nine days')
    ground_section(c, t, surf=520)
    k = eo(pr(t, 0.2, 1.6))
    c.drawLine(540, 520, 540, lerp(520, 1350, k), stroke((70, 50, 40), 26, 0.6))
    c.drawOval(R.MakeXYWH(300, 1290, 480, 170), paint((40, 30, 26)))
    for i in range(5):
        miner(c, 380 + i * 80, 1440, 0.55, POSES['stand'], Face('open', 'flat', 'worried'), t)
    depth_meter(c, t, k, '%d M' % int(700 * k))
    top_shade(c, 0.4, (10, 30, 60))
    tier(c, t, 0.0, 'what if you were trapped', '700 M UNDERGROUND', YEL, size=200, t1=t33 - 0.3)
    tier(c, t, t33 - 0.2, 'it happened to', '33 MINERS', WT_, size=290, t1=t69 - 0.3)
    tier(c, t, t69 - 0.2, 'trapped for', '69 DAYS', YEL, size=300)


def sc_collapse(c, t, S):
    tc = ph('collapsed')
    ground_section(c, t, surf=760)
    calendar(c, 830, 950, 0.5, 'AUG 5', '2010')
    c.drawLine(200, 900, 880, 1450, stroke((50, 35, 28), 60))
    if t > tc - 0.1:
        k = eo(pr(t, tc - 0.1, 0.5))
        slab = poly([(420, 1060 + 400 * (k - 1)), (680, 1100 + 400 * (k - 1)), (700, 1290 + 400 * (k - 1)), (440, 1260 + 400 * (k - 1))], True)
        c.drawPath(slab, paint((120, 85, 60))); c.drawPath(slab, stroke(INK, 7))
        for i in range(14):
            ph_ = pr(t, tc, 1.2)
            c.drawCircle(560 + (hsh(i, 2) - 0.5) * 400 * ph_, 1200 - 100 * ph_ + 300 * ph_ * ph_ * hsh(i, 3), 12, paint(ROCK_L, 1 - ph_))
    miner(c, 760, 1430, 0.8, POSES['shock'] if t > tc else POSES['stand'], Face('wide', 'o', 'worried') if t > tc else Face('open', 'smile'), t)
    top_shade(c, 0.4, (10, 30, 60))
    tier(c, t, S['t0'] + 0.1, 'a copper and gold mine in', 'THE ATACAMA DESERT', WT_, size=190, t1=tc - 0.3)
    tier(c, t, tc - 0.2, 'then the mountain', 'COLLAPSED', RED, size=290)


def sc_shelter(c, t, S):
    tf = ph('food for maybe'); t33 = ph('there were thirty three')
    cave_room(c, t)
    if t > tf - 0.2:
        c.save(); c.translate(850, 1100); k = eback(pr(t, tf - 0.2, 0.35), 1.6); c.scale(k, k)
        c.drawRect(R.MakeXYWH(-90, -70, 180, 140), paint((180, 130, 80))); c.drawRect(R.MakeXYWH(-90, -70, 180, 140), stroke(INK, 6))
        c.drawLine(-90, 0, 90, 0, stroke(INK, 4)); f = font('ant', 40); c.drawString('FOOD', -f.measureText('FOOD') / 2, -15, f, paint(INK))
        c.restore()
    crowd(c, 470, 1520, 16 if t < t33 else 33, 0.55, t)
    top_shade(c, 0.45)
    tier(c, t, tf - 0.15, 'food for', '2-3 DAYS', YEL, size=300, t1=t33 - 0.3)
    tier(c, t, t33 - 0.2, 'and there were', '33 OF THEM', WT_, size=290)


def sc_ration(c, t, S):
    items = (('two spoonfuls', 'spoon'), ('sip of milk', 'milk'), ('a cracker', 'cracker'))
    set_bg(c, (40, 120, 220), (110, 180, 250), circle=(170, 215, 255), cy=1150, r=440, spot=True, t=t)
    for i, (p_, kind) in enumerate(items):
        k = pr(t, ph(p_) - 0.2, 0.35)
        if k <= 0: continue
        def dr(cc, kind=kind):
            if kind == 'spoon':
                tuna_can(cc, 0, 70, 0.7); spoon(cc, -30, -20, 0.8, rot=-20); spoon(cc, 30, -20, 0.8, rot=20)
            elif kind == 'milk': milk_cup(cc, 0, 10, 1.0)
            else: cracker(cc, 0, 10, 1.0)
        card3d(c, 260 + i * 280, 1180, 250, 320, 8 * math.sin(t + i), 0, dr, k=k)
    pill(c, 540, 1440, 'EVERY 2 DAYS', pr(t, ph("that's it") - 0.1, 0.35), col=RED, size=62)
    top_shade(c, 0.4, (0, 20, 60))
    tier(c, t, S['t0'] + 0.1, 'the rule: per man,', 'EVERY 2 DAYS', WT_, size=280)


def sc_heat(c, t, S):
    tk = ph('eight kilos')
    cave_room(c, t, warm=1.0)
    thermometer(c, 820, 1450, 0.8, 0.8)
    miner(c, 430, 1520, 1.8, POSES['shrug'], Face('open', 'frown', 'worried'), t, dirt=1.0, beard=0.3)
    for i in range(4):
        ph_ = (t * 0.8 + i / 4) % 1
        c.drawOval(R.MakeXYWH(380 + i * 30, 900 + ph_ * 200, 14, 22), paint((140, 200, 255), 1 - ph_))
    if t > tk - 0.2: pill(c, 430, 1610, '-8 KG EACH', pr(t, tk - 0.2, 0.35), col=RED, size=56)
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'hot, humid, and', '35°C', (255, 170, 120), size=300, t1=tk - 0.3)
    tier(c, t, tk - 0.2, 'each man lost about', '8 KILOS', YEL, size=290)


# ================================================================== contact
def sc_drill(c, t, S):
    ground_section(c, t, surf=900)
    for i, x in enumerate((220, 540, 860)):
        drill_rig(c, x, 900, 0.7, t)
        k = eo(pr(t, S['t0'] + 0.3 + i * 0.4, 3.0))
        c.drawLine(x, 900, x + (i - 1) * 60 * k, 900 + 560 * k, stroke((40, 30, 25), 6))
    c.drawOval(R.MakeXYWH(380, 1420, 320, 110), paint((40, 30, 26)))
    for i in range(3): miner(c, 470 + i * 70, 1510, 0.4, POSES['stand'], Face('open', 'flat', 'worried'), t)
    top_shade(c, 0.4, (10, 30, 60))
    tier(c, t, S['t0'] + 0.1, 'rescuers were', 'DRILLING BLIND', WT_, size=270)


def sc_note(c, t, S):
    tb = ph('broke through'); tn = ph('little note'); tu = ph('when the drill came back')
    if t < tu - 0.2:
        cave_room(c, t)
        k = eo(pr(t, tb - 0.4, 0.8))
        c.drawLine(540, 0, 540, lerp(0, 1050, k), stroke((150, 150, 160), 22))
        c.drawPath(poly([(520, lerp(0, 1050, k)), (560, lerp(0, 1050, k)), (540, lerp(0, 1050, k) + 50)], True), paint((200, 200, 210)))
        for i, x in enumerate((340, 740)):
            miner(c, x, 1520, 1.3, POSES['arms_up'] if (int(t * 4) + i) % 2 and t > tb else POSES['stand'], Face('wide', 'grin', 'up') if t > tb else Face('open', 'flat'), t, beard=0.3, flip=i == 1)
        if t > tn - 0.2: note_paper(c, 540, 1000, 0.35, pr(t, tn - 0.2, 0.35))
        top_shade(c, 0.45)
        tier(c, t, S['t0'] + 0.1, 'day 17:', 'A DRILL BROKE THROUGH', YEL, size=190, t1=tn - 0.3)
        tier(c, t, tn - 0.2, 'they taped on', 'A NOTE', WT_, size=300)
        return
    set_bg(c, (255, 150, 60), (255, 210, 130), circle=(255, 235, 190), cy=1150, r=450, spot=True, t=t)
    note_paper(c, 540, 1180, 1.2, pr(t, tu, 0.4))
    for i in range(16):
        ph_ = (t * 0.6 + i / 16) % 1
        c.drawRect(R.MakeXYWH(hsh(i, 2) * W, 280 + ph_ * 1200, 18, 30), paint([YEL, RED, MINT, (120, 200, 255)][i % 4]))
    top_shade(c, 0.3, (120, 50, 0))
    tier(c, t, tu - 0.05, '"we are fine in the shelter,', 'THE 33"', INK, size=290, small_col=INK)


def sc_months(c, t, S):
    tm = ph('take months')
    ground_section(c, t, surf=900, mood=0.0)
    c.drawLine(540, 900, 540, 1450, stroke((40, 30, 25), 8))
    calendar(c, 540, 1180, 0.8 * eback(pr(t, tm - 0.3, 0.4), 1.6), 'RESCUE', 'MONTHS', col=RED) if t > tm - 0.3 else None
    top_shade(c, 0.4, (10, 30, 60))
    tier(c, t, S['t0'] + 0.1, 'finding them was one thing.', 'GETTING THEM OUT?', YEL, size=210)


def sc_doves(c, t, S):
    td = ph('the doves')
    cave_room(c, t)
    k = (t * 0.35) % 1
    dove_tube(c, 540, lerp(500, 1150, eo(cl(k * 1.4))), 0.8, t)
    items = ((ph('food water'), lambda cc: tuna_can(cc, 0, 0, 0.8)), (ph('water'), lambda cc: water_bottle(cc, 0, 0, 0.8)),
             (ph('medicine'), lambda cc: pills(cc, 0, 0, 0.9)), (ph('letters from home'), lambda cc: letter(cc, 0, 0, 0.9)),
             (ph('tiny projector'), lambda cc: projector(cc, 0, 0, 0.9)))
    for i, (tt_, fn) in enumerate(items):
        kk = pr(t, tt_ - 0.1, 0.35)
        if kk <= 0: continue
        x = 200 + (i % 3) * 340 if i < 3 else 370 + (i - 3) * 340; y = 1320 if i < 3 else 1480
        c.save(); c.translate(x if x != 540 else 700, y); s_ = eback(kk, 1.6); c.scale(s_, s_); fn(c); c.restore()
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'everything came down', 'A TINY HOLE', WT_, size=290, t1=td - 0.4)
    tier(c, t, td - 0.3, 'the delivery tubes:', '"THE DOVES"', (140, 200, 255), size=260)


# ================================================================== rescue
def sc_capsule(c, t, S):
    tp = ph('the phoenix'); tw = ph("person's shoulders")
    set_bg(c, (40, 60, 150), (110, 130, 230), circle=(160, 180, 255), cy=1150, r=450, spot=True, t=t)
    capsule(c, 540, 1180, 1.05 * eback(pr(t, tp - 0.4, 0.5), 1.4), t)
    if t > tw - 0.3:
        k = eo(pr(t, tw - 0.3, 0.5))
        c.drawLine(470, 1500, 470 + 140 * k, 1500, stroke(YEL, 8)); pill(c, 540, 1560, '~54 CM WIDE', k, col=INK, size=50, txt_col=YEL)
    top_shade(c, 0.4)
    tier(c, t, S['t0'] + 0.1, 'October 12: a rescue capsule', 'THE PHOENIX', YEL, size=280, t1=tw - 0.4)
    tier(c, t, tw - 0.3, 'barely wider than', 'YOUR SHOULDERS', WT_, size=230)


def sc_ride(c, t, S):
    u = t - S['t0']
    ground_section(c, t, surf=600)
    c.drawRect(R.MakeXYWH(500, 600, 80, H), paint((40, 30, 25)))
    k = (u * 0.18) % 1
    capsule(c, 540, lerp(1750, 950, k), 0.45, t)
    mins = 9 + int(9 * (0.5 + 0.5 * math.sin(u)))
    pill(c, 820, 1150, '%d MIN' % mins, 1, col=INK, size=56, txt_col=YEL)
    top_shade(c, 0.35, (10, 30, 60))
    tier(c, t, S['t0'] + 0.1, 'one by one, each ride took', '9-18 MINUTES', WT_, size=220)


def sc_shades(c, t, S):
    set_bg(c, (255, 200, 80), (255, 235, 160), circle=(255, 250, 220), cy=1150, r=450, spot=True, t=t)
    for i in range(9):
        a = i / 9 * 6.283 + t * 0.2
        c.drawLine(540 + math.cos(a) * 480, 1150 + math.sin(a) * 480, 540 + math.cos(a) * 620, 1150 + math.sin(a) * 620, stroke((255, 255, 255), 10, 0.6))
    miner(c, 540, 1520, 2.0, POSES['arms_up'], Face('happy', 'grin'), t, shades=1.0, beard=0.6)
    top_shade(c, 0.3, (120, 60, 0))
    tier(c, t, S['t0'] + 0.1, 'they came out wearing', 'SUNGLASSES', INK, size=290, small_col=INK)


def sc_out(c, t, S):
    tl = ph('the last man up')
    set_bg(c, (60, 200, 120), (150, 240, 180), circle=(220, 255, 230), cy=1150, r=450, spot=True, t=t)
    if t < tl - 0.2:
        n = int(33 * eo(pr(t, S['t0'] + 0.3, 2.5)))
        bigtxt(c, 540, 1080, '%d/33' % n, 220, YEL)
        crowd(c, 470, 1520, 16, 0.55, t, cheer=True, shades=1.0)
        for i in range(16):
            ph_ = (t * 0.6 + i / 16) % 1
            c.drawRect(R.MakeXYWH(hsh(i, 2) * W, 280 + ph_ * 1200, 18, 30), paint([YEL, RED, MINT, (120, 200, 255)][i % 4]))
        top_shade(c, 0.3, (0, 70, 30))
        tier(c, t, S['t0'] + 0.1, '22 hours later:', 'ALL 33 SAVED', WT_, size=290)
        return
    miner(c, 540, 1520, 2.0, POSES['wave'], Face('happy', 'smile'), t, shades=1.0, beard=0.8)
    pill(c, 540, 1610, 'SHIFT BOSS', 1, col=RED, size=56)
    top_shade(c, 0.3, (0, 70, 30))
    tier(c, t, tl - 0.1, 'last one up:', 'LUIS URZUA', YEL, size=290)


def sc_ask(c, t, S):
    cave_room(c, t)
    tuna_can(c, 760, 1350, 1.3); spoon(c, 690, 1230, 1.0, rot=-20); spoon(c, 830, 1230, 1.0, rot=20)
    miner(c, 330, 1520, 1.5, POSES['shrug'], Face('happy', 'grin'), t, beard=0.5)
    comment_bubble(c, 760, 1000, 0.7, pr(t, ph('comments') - 0.2, 0.35))
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'could you survive on', '2 SPOONS OF TUNA?', YEL, size=200)
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint((30, 15, 5)))


SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='collapse', t0=ph('it was august') - 0.2, fn=sc_collapse, tin='whip'),
    dict(k='shelter', t0=ph('the men made it') - 0.2, fn=sc_shelter, tin='wipe', col=(60, 45, 35)),
    dict(k='ration', t0=ph('so they made a rule') - 0.2, fn=sc_ration, tin='zoom'),
    dict(k='heat', t0=ph('it was hot') - 0.2, fn=sc_heat, tin='whip'),
    dict(k='drill', t0=ph('up on the surface') - 0.2, fn=sc_drill, tin='wipe', col=(240, 180, 110)),
    dict(k='note', t0=ph('on day seventeen') - 0.2, fn=sc_note, tin='flash'),
    dict(k='months', t0=ph("but here's the thing") - 0.2, fn=sc_months, tin='whip'),
    dict(k='doves', t0=ph('so while they waited') - 0.2, fn=sc_doves, tin='zoom'),
    dict(k='capsule', t0=ph('then on october') - 0.2, fn=sc_capsule, tin='flash'),
    dict(k='ride', t0=ph('one by one') - 0.2, fn=sc_ride, tin='wipe', col=(240, 180, 110)),
    dict(k='shades', t0=ph('they came out wearing') - 0.2, fn=sc_shades, tin='zoom'),
    dict(k='out', t0=ph('twenty two hours later') - 0.2, fn=sc_out, tin='flash'),
    dict(k='ask', t0=ph('so could you survive') - 0.2, fn=sc_ask, tin='wipe', col=(60, 45, 35)),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('collapsed'), 18, 0.6); EP.flash(ph('collapsed'), 0.3, 0.1, (255, 230, 200))
EP.shk(ph('broke through'), 10, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
