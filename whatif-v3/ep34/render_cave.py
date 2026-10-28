"""What if you lived in a cave for 500 days? — episode 34 (Beatriz Flamini 2021–23, Michel Siffre 1972)."""
import sys, os, math, re
import skia
from caveprops import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('CV_DIR', 'cave'))
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
WT_ = (255, 255, 255); SM = (240, 230, 255)
WALL = (250, 240, 220)


def top_shade(c, a=0.45, col=(10, 6, 24)):
    c.drawRect(R.MakeLTRB(0, 0, W, 860), paint(shader=lin(0, 250, 0, 860, [argb(col, a), argb(col, 0)])))


def tier(c, t, t0, small, big, col=WT_, t1=None, size=250, y=TY, t_big=None):
    two_tier(c, t, t0, small, big, y=y, big_size=size, big_col=col, small_col=SM, shadow=True, t1=t1, t_big=t_big)


# ================================================================== hook
def sc_hook(c, t, S):
    u = t
    t_no = ph('no sunlight')
    cave_bg(c, t, lamp=(540, 1200), lamp_a=0.55)
    camp(c, 700, 1420, 0.85, t)
    k = pr(t, 0.4, 1.6)
    bx = lerp(-120, 300, eo(k))
    pose = walk_pose(t * 1.5, 0.9) if k < 1 else POSES['stand']
    face = Face('open', 'smile', look=(1, 0)) if k < 1 else Face('open', 'o', look=(0, -1))
    beatriz(c, bx, 1420, 1.15, pose, face, t, lamp=1.0)
    # the four 'no' icons popping in one by one
    for i, (ph_, icon) in enumerate((('no sunlight', 'sun'), ('no clock', 'clock'), ('no phone', 'phone'), ('nobody', 'people'))):
        tt = ph(ph_)
        kk = eback(pr(t, tt, 0.3), 1.6)
        if kk <= 0: continue
        x = 220 + i * 213; y = 950
        c.save(); c.translate(x, y); c.scale(kk, kk)
        c.drawCircle(0, 0, 78, paint((255, 255, 255))); c.drawCircle(0, 0, 78, stroke(INK, 6))
        if icon == 'sun': sun_icon(c, 0, 0, 26, t)
        elif icon == 'clock': body_clock(c, 0, 0, 0.2, t, hours=12)
        elif icon == 'phone': phone(c, 0, 0, 0.26, t, 0)
        else:
            for sx in (-1, 1):
                c.drawCircle(sx * 22, -16, 14, paint(INK)); c.drawRoundRect(R.MakeXYWH(sx * 22 - 20, 2, 40, 36), 14, 14, paint(INK))
        c.drawLine(-62, -62, 62, 62, stroke(RED, 12)); c.drawCircle(0, 0, 78, stroke(RED, 10))
        c.restore()
    top_shade(c, 0.6)
    tier(c, t, 0.25, 'what if you lived alone in a', 'CAVE', WT_, size=270, t1=ph('for five') - 0.1)
    tier(c, t, ph('for five') - 0.05, 'for', '500 DAYS', YEL, size=270, t1=t_no - 0.2)


def sc_early(c, t, S):
    u = t - S['t0']
    cave_bg(c, t, lamp=(540, 1250), lamp_a=0.5, dark=0.25)
    camp(c, 760, 1420, 0.8, t)
    tw = ph('she thought')
    asleep = t < tw - 0.3
    pose = POSES['sit'] if asleep else POSES['shock']
    face = Face('closed', 'smile') if asleep else Face('wide', 'o', 'worried', look=(-1, 0))
    beatriz(c, 330, 1420, 1.15, pose, face, t, lamp=0.0)
    # rescuer arriving down the rope
    kk = eo(pr(t, S['t0'] + 0.2, 1.2))
    rope(c, 150, -20, 1300, sway=0.5, t=t)
    rescuer(c, 150, lerp(200, 1420, kk), 1.0, POSES['hold'] if kk < 1 else POSES['wave'], Face('happy', 'grin'), t)
    if t > tw:
        speech(c, 330, 1000, 420, 150, 'EARLY?', eback(pr(t, tw, 0.3), 1.6), size=90, col=RED, tail=1)
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'one woman', 'DID IT', WT_, t1=tw - 0.2)


def sc_descent(c, t, S):
    u = t - S['t0']
    k = eo(pr(t, S['t0'] + 0.3, 2.2))
    cave_mouth(c, t)
    if k < 1:
        beatriz(c, 540, lerp(1120, 1260, k), 1.0, POSES['hold'], Face('open', 'smile'), t, lamp=0.0, a=1 - k * 0.9)
    calendar(c, 860, 960, 0.8, 'NOV', '2021')
    top_shade(c, 0.3)
    tier(c, t, S['t0'] + 0.15, 'Beatriz Flamini,', 'GRANADA', WT_, size=230, t1=ph('seventy meters') - 0.2)
    tier(c, t, ph('seventy meters') - 0.1, 'seventy meters', 'UNDERGROUND', YEL, size=210)


def sc_rule(c, t, S):
    u = t - S['t0']
    cave_bg(c, t, lamp=(540, 1200), lamp_a=0.5)
    camp(c, 740, 1420, 0.8, t)
    tb = ph('panic button'); tn = ph('she never')
    beatriz(c, 330, 1420, 1.15, POSES['stand'], Face('open', 'flat', look=(1, 0)), t, lamp=0.6)
    # the rule card
    def rulecard(cc):
        f = font('ant', 70); s_ = 'RULE'
        cc.drawString(s_, -f.measureText(s_) / 2, -60, f, paint(RED))
        f2 = font('mxb', 44)
        for i, line in enumerate(('NOBODY TALKS', 'TO HER.')):
            cc.drawString(line, -f2.measureText(line) / 2, 10 + i * 56, f2, paint(INK))
    card3d(c, 540, 1000, 560, 260, -8, 4, rulecard, fill=(255, 250, 235), k=pr(t, S['t0'] + 0.2, 0.4) * (1 - pr(t, tb - 0.4, 0.3)))
    if t > tb - 0.2:
        kk = eback(pr(t, tb - 0.2, 0.35), 1.6)
        c.save(); c.translate(540, 1000); c.scale(kk, kk)
        c.drawRoundRect(R.MakeXYWH(-140, 40, 280, 60), 20, 20, paint((120, 120, 130))); c.drawRoundRect(R.MakeXYWH(-140, 40, 280, 60), 20, 20, stroke(INK, 6))
        c.drawCircle(0, 0, 90, paint(RED)); c.drawCircle(0, 0, 90, stroke(INK, 7)); c.drawCircle(-25, -30, 26, paint((255, 255, 255), 0.35))
        f = font('ant', 44); s_ = 'PANIC'; c.drawString(s_, -f.measureText(s_) / 2, 16, f, paint((255, 255, 255)))
        c.restore()
        if t > tn:
            # cobweb on the button
            kw = pr(t, tn, 0.5)
            for i in range(6):
                a = math.radians(i * 30 + 200); c.drawLine(630, 920, 630 + math.cos(a) * 90 * kw, 920 + math.sin(a) * 90 * kw, stroke((220, 220, 230), 2, 0.8))
            for r_ in (30, 55, 80):
                c.drawArc(R.MakeXYWH(630 - r_, 920 - r_, 2 * r_, 2 * r_), 200, 150, False, stroke((220, 220, 230), 2, 0.8 * kw))
    top_shade(c, 0.4)
    tier(c, t, ph('not even if'), 'not even if', 'FAMILY DIES', WT_, size=210, t1=tb - 0.3)
    tier(c, t, tn - 0.05, 'she never', 'TOUCHED IT', YEL, size=220)


# ================================================================== chapter 1: clock
def sc_clock(c, t, S):
    u = t - S['t0']
    tb = ph('your clock breaks'); td = ph('just')
    set_bg(c, (40, 20, 80), (110, 60, 150), circle=(255, 200, 90), cy=900, r=430, spot=True, t=t, circ_k=pr(t, S['t0'], 0.5))
    drift = eo(pr(t, td, 0.8))
    head_with_clock(c, 540, 900, 1.0, t, drift=drift, hand_speed=1.0 + 2.0 * drift)
    if tb - 0.1 < t < ph('your brain has') + 0.2:
        kk = pr(t, tb, 0.3)
        c.drawCircle(540, 900, 300, stroke(RED, 14 * kk, 0.9 * kk))
    top_shade(c, 0.4)
    tier(c, t, ph('your clock breaks') - 0.1, 'first,', 'YOUR CLOCK BREAKS', WT_, size=190, t1=ph('twenty-four hours') - 0.2)
    tier(c, t, ph('twenty-four hours') - 0.1, 'your built-in clock runs on', '24 H 11 MIN', YEL, size=230, t1=ph('every morning') - 0.2)


def sc_reset(c, t, S):
    u = t - S['t0']
    ts = ph('sunlight resets'); tc = ph('in a cave'); td = ph('drifts')
    cave_k = eo(pr(t, tc, 0.5))
    # day sky -> cave
    set_bg(c, mix((120, 190, 255), (30, 20, 50), cave_k), mix((230, 245, 255), (60, 40, 90), cave_k), spot=False, floor=1420)
    if cave_k < 1:
        sun_icon(c, 540, 330, 80, t, a=1 - cave_k)
        kb = pr(t, ts, 0.4)
        for i in range(7):
            a = math.radians(60 + i * 10)
            x1 = 540 + math.cos(a) * 520 * kb; y1 = 330 + math.sin(a) * 520 * kb
            c.drawLine(540, 330, x1, y1, stroke(YEL, 6, 0.7 * (1 - cave_k)))
    else:
        stalactites(c, 0, n=10, seed=3)
    drift = eo(pr(t, td, 0.7))
    body_clock(c, 540, 1050, 1.0, t, k_drift=drift, hand_speed=1 + 3 * drift, glow=(ts < t < tc) and not cave_k)
    draw_stick(c, 300, 1420, 1.0, POSES['point_up'] if t < tc else POSES['shrug'], Face('open', 'smile' if t < tc else 'flat', look=(1, -1)), t=t)
    if drift > 0:
        f = font('ant', 60); s_ = '?'
        for i in range(3):
            c.drawString(s_, 820 + i * 40 - 20 * math.sin(t * 3 + i), 820 - i * 50 - 20 * drift, f, paint(YEL, drift))
    top_shade(c, 0.4 * cave_k + 0.1)
    tier(c, t, ts - 0.05, 'every morning', 'SUNLIGHT RESETS IT', YEL if cave_k < 0.5 else WT_, size=180, t1=tc - 0.2)
    tier(c, t, tc - 0.05, 'in a cave, there is', 'NO SUNLIGHT', WT_, size=230, t1=td - 0.3)
    tier(c, t, td - 0.1, 'so the clock just', 'DRIFTS', RED, size=270)


def sc_siffre(c, t, S):
    u = t - S['t0']
    cave_bg(c, t, lamp=(540, 1150), lamp_a=0.5, teal=0.3)
    texas_sign(c, 860, 1260, 1.0, k=pr(t, ph('texas') - 0.2, 0.4))
    siffre(c, 400, 1420, 1.15, POSES['stand'], Face('open', 'smile', look=(1, 0)), t)
    calendar(c, 230, 500, 0.8, 'DAYS', '205') if t > ph('two hundred') - 0.2 else None
    top_shade(c, 0.5)
    tier(c, t, ph('michel') - 0.1, 'French scientist', 'MICHEL SIFFRE', WT_, size=210, t1=ph('two hundred') - 0.3)
    tier(c, t, ph('two hundred') - 0.1, 'a cave in Texas,', '205 DAYS', YEL, size=260)


def sc_48(c, t, S):
    u = t - S['t0']
    t48 = ph('forty-eight'); tn = ph("didn't even")
    set_bg(c, (20, 40, 90), (60, 110, 180), circle=(255, 230, 120), cy=820, r=400, spot=True, t=t, circ_k=pr(t, S['t0'], 0.5))
    k = eo(pr(t, t48 - 0.3, 1.0))
    hrs = int(24 + 24 * k)
    body_clock(c, 540, 960, 1.0, t, hours=hrs if hrs in (24, 48) else 24, hand_speed=0.6, k_drift=0.0)
    big = '%d H' % hrs
    f = font('ant', 130); c.drawString(big, 540 - f.measureText(big) / 2, 1400, f, stroke(INK, 14)); c.drawString(big, 540 - f.measureText(big) / 2, 1400, f, paint(YEL))
    # sleep / awake band
    y = 1470
    c.drawRoundRect(R.MakeXYWH(140, y, 800, 70), 35, 35, paint((255, 255, 255), 0.2)); c.drawRoundRect(R.MakeXYWH(140, y, 800, 70), 35, 35, stroke(INK, 5))
    aw = 800 * lerp(0.67, 0.75, k)
    c.drawRoundRect(R.MakeXYWH(140, y, aw, 70), 35, 35, paint(YEL)); c.drawRoundRect(R.MakeXYWH(140, y, aw, 70), 35, 35, stroke(INK, 5))
    f2 = font('mxb', 34); c.drawString('AWAKE %d H' % int(36 * k + 16 * (1 - k)), 170, y + 47, f2, paint(INK)); c.drawString('SLEEP', 140 + aw + 20, y + 47, f2, paint((255, 255, 255)))
    siffre(c, 300, 1420, 0.0, POSES['stand'], Face(), t) if False else None
    top_shade(c, 0.3)
    tier(c, t, t48 - 0.1, 'sometimes his body ran a', '48-HOUR DAY', WT_, size=220, t1=tn - 0.2)
    tier(c, t, tn - 0.05, "and he didn't", 'EVEN NOTICE', YEL, size=230)


def sc_tuesday(c, t, S):
    u = t - S['t0']
    set_bg(c, (255, 170, 90), (255, 220, 150), circle=(255, 240, 200), cy=900, r=420, spot=True, t=t, circ_k=pr(t, S['t0'], 0.4))
    # office desk gag: mascot with bags under eyes holding coffee
    c.drawRoundRect(R.MakeXYWH(240, 1300, 600, 40), 10, 10, paint((150, 100, 60))); c.drawRoundRect(R.MakeXYWH(240, 1300, 600, 40), 10, 10, stroke(INK, 6))
    for x in (280, 800): c.drawLine(x, 1340, x, 1500, stroke((120, 80, 50), 14)); c.drawLine(x, 1340, x, 1500, stroke(INK, 3, 0.4))
    draw_stick(c, 540, 1420, 1.15, POSES['hold'], Face('wide', 'flat', 'worried'), t=t, prop=lambda cc, hr, hl: (cc.drawRoundRect(R.MakeXYWH(hr[0] - 24, hr[1] - 30, 48, 56), 8, 8, paint((255, 255, 255))), cc.drawRoundRect(R.MakeXYWH(hr[0] - 24, hr[1] - 30, 48, 56), 8, 8, stroke(INK, 5)), cc.drawArc(R.MakeXYWH(hr[0] + 18, hr[1] - 18, 24, 28), -90, 180, False, stroke(INK, 5))))
    P = rig_points(POSES['hold']); hx, hy = P['head']
    for sx in (-1, 1):
        c.drawArc(R.MakeXYWH(540 + (hx + sx * 18) * 1.15 - 14, 1420 + hy * 1.15 - 2, 28, 16), 0, 180, False, stroke((120, 90, 160), 5))
    calendar(c, 840, 1040, 0.7, 'TUESDAY', '48 H')
    for i in range(3):
        y = 760 - i * 60 - (t * 50 % 60); c.drawCircle(300 + i * 12, y, 10 + i * 6, stroke(INK, 4))
    smoke(c, 575, 1180, t, S['t0'] - 1, n=5, spread=60, col=(240, 240, 240), a=0.6, rise=30)
    top_shade(c, 0.1, col=(120, 60, 0))
    tier(c, t, ph('imagine staying') - 0.05, 'awake for two days,', 'NORMAL TUESDAY', INK, size=190)


def sc_count(c, t, S):
    u = t - S['t0']
    t65 = ph('sixty-five'); tg = ph('gave up')
    cave_bg(c, t, lamp=(400, 1100), lamp_a=0.5)
    n = int(min(65, 65 * eo(pr(t, S['t0'] + 0.1, t65 - S['t0'] - 0.2 + 0.001))))
    tally_wall(c, 110, 760, 0.85, n, col=WALL)
    beatriz(c, 760, 1420, 1.1, POSES['point_up'] if t < tg else POSES['shrug'], Face('open', 'smile' if t < tg else 'flat', look=(-1, -1)), t, lamp=0.5)
    if t > t65 - 0.1:
        kk = eback(pr(t, t65 - 0.1, 0.35), 1.6)
        c.save(); c.translate(540, 1000); c.scale(kk, kk)
        c.drawRoundRect(R.MakeXYWH(-200, -110, 400, 220), 30, 30, paint((255, 255, 255))); c.drawRoundRect(R.MakeXYWH(-200, -110, 400, 220), 30, 30, stroke(INK, 7))
        f = font('ant', 150); s_ = '65'; c.drawString(s_, -f.measureText(s_) / 2, 55, f, paint(RED))
        c.restore()
    if t > tg:
        kk = pr(t, tg, 0.4)
        # chalk thrown away
        c.drawRoundRect(R.MakeXYWH(760 + 200 * kk, 1380 - 200 * math.sin(math.pi * kk) + 60, 40, 14), 6, 6, paint(WALL))
    top_shade(c, 0.5)
    tier(c, t, ph('she tried to count') - 0.05, 'she tried to', 'COUNT THE DAYS', WT_, size=190, t1=t65 - 0.3)
    tier(c, t, tg - 0.1, 'on day 65,', 'SHE GAVE UP', YEL, size=230)


# ================================================================== chapter 2: memory
def sc_memory(c, t, S):
    u = t - S['t0']
    tf = ph('the day before')
    set_bg(c, (60, 30, 100), (130, 80, 170), circle=(255, 190, 220), cy=880, r=420, spot=True, t=t, circ_k=pr(t, S['t0'], 0.4))
    brain(c, 540, 960, 1.0, t)
    # fog over the brain
    kf = eo(pr(t, S['t0'] + 0.5, 1.2))
    for i in range(9):
        x = 300 + hsh(i, 3) * 480 + math.sin(t * 0.8 + i) * 30; y = 860 + hsh(i, 4) * 260
        r = 60 + 70 * hsh(i, 5)
        c.drawCircle(x, y, r, paint((230, 230, 245), 0.75 * kf, blur=r * 0.4))
    f = font('ant', 110); s_ = '?'
    for i in range(3):
        c.drawString(s_, 420 + i * 110, 800 - 30 * math.sin(t * 2 + i), f, paint(WT_, kf))
    siffre(c, 300, 1420, 1.1, POSES['shrug'], Face('open', 'flat', 'worried'), t)
    calendar(c, 820, 1250, 0.6, 'YESTERDAY', '???')
    top_shade(c, 0.3)
    tier(c, t, S['t0'] + 0.1, 'then your memory', 'GOES WEIRD', WT_, size=230, t1=tf - 0.9)
    tier(c, t, tf - 0.8, "couldn't remember", 'YESTERDAY', YEL, size=240)


def sc_count120(c, t, S):
    u = t - S['t0']
    t5 = ph('five minutes'); tf = ph('five real')
    set_bg(c, (20, 60, 90), (40, 140, 160), circle=(255, 240, 200), cy=860, r=400, spot=True, t=t, circ_k=pr(t, S['t0'], 0.4))
    num = int(min(120, 1 + u * 12))
    stopwatch_count(c, 540, 980, 0.82, num, t)
    siffre(c, 300, 1420, 1.1, POSES['point_up'], Face('open', 'chatter' if t < t5 else 'o', look=(1, -1)), t)
    if t > t5 - 0.1:
        kk = eback(pr(t, t5 - 0.1, 0.35), 1.6)
        def card(cc):
            f = font('ant', 72)
            for i, (s_, col) in enumerate((('FELT LIKE 2 MIN', (60, 120, 200)), ('REAL: 5 MIN', RED))):
                cc.drawString(s_, -f.measureText(s_) / 2, -20 + i * 90, f, paint(col))
        card3d(c, 540, 1330, 620, 230, -6, 4, card, fill=(255, 250, 235), k=kk)
    top_shade(c, 0.3)
    tier(c, t, ph('counted to one') - 0.1, 'he counted to 120,', '1 PER SECOND', WT_, size=210, t1=t5 - 0.3)
    tier(c, t, t5 - 0.1, 'it took him', '5 MINUTES', YEL, size=260, t1=tf + 0.3)


def sc_hobbies(c, t, S):
    u = t - S['t0']
    tb = ph('sixty books'); tk = ph('knitted'); te = ph('exercised'); tt = ph('talked to herself')
    cave_bg(c, t, lamp=(540, 1150), lamp_a=0.55)
    camp(c, 760, 1420, 0.75, t)
    items = [(tb, 'book'), (tk, 'hat'), (te, 'dumbbell'), (tt, 'talk')]
    cur = max([i for i, (tt_, _) in enumerate(items) if t >= tt_ - 0.2] + [-1])
    pose = POSES['hold']
    if cur == 2: pose = (0, 0, 200, 10, 95, -100, 186, 0, 174, 0)
    if cur == 3: pose = POSES['shrug']
    def prop(cc, hr, hl):
        if cur == 0: book(cc, hr[0], hr[1] - 10, 0.8, rot=-10, open_=True)
        elif cur == 1: knit_hat(cc, hr[0], hr[1] - 10, 0.7)
        elif cur == 2: dumbbell(cc, hr[0], hr[1], 0.55, rot=-20 + 20 * math.sin(t * 6))
    beatriz(c, 330, 1420, 1.15, pose, Face('happy' if cur >= 0 else 'open', 'smile', look=(0.5, 0)), t, lamp=0.0, prop=prop)
    if cur == 3:
        speech(c, 330, 950, 520, 150, 'GREAT CHAT', eback(pr(t, tt, 0.3), 1.6), size=80, col=INK, tail=-1)
    # pile of 60 books counting up
    if t > tb - 0.1:
        n = int(min(60, (t - tb + 0.1) * 30))
        for i in range(n):
            col = [(220, 70, 60), (60, 120, 200), (240, 190, 70), (80, 160, 100), (150, 90, 170)][i % 5]
            x = 640 + (i // 12) * 70; y = 1400 - (i % 12) * 22
            c.drawRoundRect(R.MakeXYWH(x - 30, y - 18, 60, 18), 4, 4, paint(col)); c.drawRoundRect(R.MakeXYWH(x - 30, y - 18, 60, 18), 4, 4, stroke(INK, 3))
        f = font('ant', 90); s_ = '%d' % n; c.drawString(s_, 840 - f.measureText(s_) / 2, 1120, f, paint(YEL))
    top_shade(c, 0.5)
    tier(c, t, tb - 0.05, 'she read', '60 BOOKS', YEL, size=250, t1=tk - 0.2)
    tier(c, t, tk - 0.05, 'knitted hats,', 'EXERCISED', WT_, size=230, t1=tt - 0.3)
    tier(c, t, tt - 0.05, 'and talked', 'TO HERSELF', YEL, size=230)


def sc_room_service(c, t, S):
    u = t - S['t0']
    tw = ph('pulled her waste'); tr = ph('best room'); tbt = ph('best room') + 1.2
    cave_bg(c, t, lamp=(540, 1250), lamp_a=0.5)
    kd = eo(pr(t, S['t0'] + 0.2, 1.4))
    ku = eo(pr(t, tw, 1.4))
    rope(c, 700, -20, lerp(300, 1180, kd) if t < tw else lerp(1180, 300, ku), sway=0.4, t=t)
    bucket(c, 700, lerp(300, 1180, kd) if t < tw else lerp(1180, 300, ku), 0.85, t, kind='food' if t < tw else 'waste')
    beatriz(c, 380, 1420, 1.15, POSES['arms_up'] if t < tw else POSES['hold'], Face('happy', 'grin') if t < tbt else Face('open', 'puff'), t, lamp=0.0)
    if t > tr - 0.1:
        kk = eback(pr(t, tr - 0.1, 0.35), 1.6)
        c.save(); c.translate(540, 1000); c.scale(kk, kk)
        c.drawRoundRect(R.MakeXYWH(-250, -70, 500, 140), 30, 30, paint(YEL)); c.drawRoundRect(R.MakeXYWH(-250, -70, 500, 140), 30, 30, stroke(INK, 7))
        f = font('ant', 64); s_ = '5-STAR SERVICE'; c.drawString(s_, -f.measureText(s_) / 2, 22, f, paint(INK))
        for i in range(5):
            x = -120 + i * 60
            c.drawPath(_star(x, -100, 22), paint(YEL)); c.drawPath(_star(x, -100, 22), stroke(INK, 4))
        c.restore()
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'her team lowered', 'FOOD', WT_, size=270, t1=tw - 0.2)
    tier(c, t, tw - 0.05, 'and pulled her', 'WASTE UP', WT_, size=250, t1=tr - 0.3)


def _star(x, y, r):
    p = skia.Path()
    for i in range(10):
        a = math.radians(-90 + i * 36); rr = r if i % 2 == 0 else r * 0.45
        (p.moveTo if i == 0 else p.lineTo)(x + math.cos(a) * rr, y + math.sin(a) * rr)
    p.close(); return p


def sc_flies(c, t, S):
    u = t - S['t0']
    tf = ph('flies'); tc = ph('completely covered')
    cave_bg(c, t, lamp=(540, 1200), lamp_a=0.45, dark=0.3)
    camp(c, 760, 1420, 0.8, t)
    k = eo(pr(t, tf, 1.0))
    kc = eo(pr(t, tc - 0.3, 0.8))
    beatriz(c, 360, 1420, 1.15, POSES['shock'] if k > 0.3 else POSES['stand'], Face('wide', 'o', 'worried') if k > 0.3 else Face('open', 'flat'), t, lamp=0.0)
    flies(c, t, int(80 * k), 360, 1200, 260 + 200 * (1 - kc), k=1.0)
    flies(c, t, int(120 * kc), 360, 1150, 160, k=1.0, seed=17)
    top_shade(c, 0.55)
    tier(c, t, S['t0'] + 0.1, 'then came', 'THE WORST DAY', WT_, size=210, t1=tf - 0.2)
    tier(c, t, tf - 0.05, 'the cave got invaded by', 'FLIES', RED, size=290, t1=tc - 0.3)
    tier(c, t, tc - 0.05, 'completely', 'COVERED', RED, size=270)


# ================================================================== chapter 3: the exit
def sc_rescue(c, t, S):
    u = t - S['t0']
    tw = ph('when they woke'); ta = ph('already')
    cave_bg(c, t, lamp=(540, 1250), lamp_a=0.45, dark=0.35)
    camp(c, 760, 1420, 0.8, t, lamp_on=False)
    kk = eo(pr(t, S['t0'] + 0.2, 1.3))
    rope(c, 150, -20, 1300, sway=0.5, t=t)
    rescuer(c, 150, lerp(150, 1420, kk), 1.0, POSES['hold'] if kk < 1 else POSES['point'], Face('happy', 'grin'), t)
    awake = t > tw + 0.2
    beatriz(c, 380, 1420, 1.15, POSES['sit'] if not awake else POSES['shock'], Face('closed', 'smile') if not awake else Face('wide', 'o', 'worried', look=(-1, 0)), t, lamp=0.0)
    if not awake:
        f = font('ant', 60)
        for i in range(3):
            c.drawString('z', 420 + i * 30, 1050 - i * 50 - (t * 40 % 60), f, paint(WT_, 0.8 - i * 0.2))
    if t > ta - 0.05:
        speech(c, 380, 950, 560, 160, 'ALREADY? NO WAY', eback(pr(t, ta - 0.05, 0.3), 1.6), size=66, col=RED, tail=1)
    calendar(c, 860, 1000, 0.7, 'APR', '2023')
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'her team', 'CLIMBED DOWN', WT_, size=210, t1=tw - 0.3)


def sc_160(c, t, S):
    u = t - S['t0']
    t160 = ph('one hundred and sixty'); t500 = ph('five hundred', after=t160); ty = ph('almost a year')
    set_bg(c, (30, 20, 70), (90, 50, 140), spot=True, t=t)
    k1 = eo(pr(t, t160, 0.9)); k2 = eo(pr(t, t500 - 0.1, 1.0))
    f = font('mxb', 44)
    c.drawString('IN HER HEAD', 140, 800, f, paint(SM, pr(t, S['t0'] + 0.1, 0.3)))
    big_number_bar(c, 140, 890, 800, 0.32 * k1, '%d' % int(160 * k1), (80, 160, 255))
    if t > t500 - 0.3:
        c.drawString('REAL', 140, 1070, f, paint(SM, pr(t, t500 - 0.3, 0.3)))
        big_number_bar(c, 140, 1160, 800, max(0.01, k2), '%d' % int(500 * k2), RED, text_col=(255, 255, 255))
    if t > ty - 0.1:
        kk = eback(pr(t, ty - 0.1, 0.35), 1.6)
        c.save(); c.translate(540, 1400); c.scale(kk, kk)
        c.drawRoundRect(R.MakeXYWH(-300, -70, 600, 140), 30, 30, paint(YEL)); c.drawRoundRect(R.MakeXYWH(-300, -70, 600, 140), 30, 30, stroke(INK, 7))
        f2 = font('ant', 70); s_ = '340 DAYS MISSING'; c.drawString(s_, -f2.measureText(s_) / 2, 24, f2, paint(INK))
        c.restore()
    beatriz(c, 540, 1820, 1.0, POSES['shrug'], Face('wide', 'o', 'worried'), t, lamp=0.0) if False else None
    top_shade(c, 0.3)
    tier(c, t, S['t0'] + 0.05, 'in her head,', '160 DAYS', (80, 160, 255), size=240, t1=t500 - 0.2)
    tier(c, t, t500 - 0.1, 'the real number?', '500', RED, size=270, t1=ty - 0.2)
    tier(c, t, ty - 0.05, 'her brain lost', 'ALMOST A YEAR', YEL, size=200)


def sc_book(c, t, S):
    u = t - S['t0']
    tw = ph("didn't want to"); tb = ph("hadn't finished")
    cave_bg(c, t, lamp=(540, 1200), lamp_a=0.55)
    camp(c, 760, 1420, 0.8, t)
    rope(c, 150, -20, 1300, sway=0.3, t=t)
    rescuer(c, 150, 1420, 1.0, POSES['point'], Face('open', 'o', 'worried'), t)
    beatriz(c, 420, 1420, 1.15, POSES['hold'], Face('happy', 'smile', look=(0.5, 0.5)), t, lamp=0.0, prop=lambda cc, hr, hl: book(cc, hr[0], hr[1] - 10, 0.8, rot=-10, open_=True))
    if t > tb - 0.1:
        speech(c, 420, 950, 560, 160, "NOT FINISHED!", eback(pr(t, tb - 0.1, 0.3), 1.6), size=70, col=INK, tail=-1)
    top_shade(c, 0.5)
    tier(c, t, tw - 0.1, 'leaving?', "DIDN'T WANT TO", WT_, size=200, t1=tb - 0.3)
    tier(c, t, tb - 0.05, "she hadn't finished", 'HER BOOK', YEL, size=250)


def sc_why(c, t, S):
    u = t - S['t0']
    ta = ph('astronauts'); ts = ph('long missions') + 0.3
    k = eo(pr(t, ta - 0.2, 0.6))
    if k < 1:
        set_bg(c, (40, 30, 90), (120, 80, 170), circle=(255, 200, 110), cy=860, r=420, spot=True, t=t, circ_k=pr(t, S['t0'], 0.4))
        c.saveLayerAlpha(None, int(255 * (1 - k)))
        # three cards: sleep, memory, time
        for i, (lab, col) in enumerate((('SLEEP', (80, 160, 255)), ('MEMORY', (255, 150, 200)), ('TIME', YEL))):
            kk = eback(pr(t, S['t0'] + 0.3 + i * 0.25, 0.35), 1.6)
            if kk <= 0: continue
            x = 540 + (i - 1) * 300
            c.save(); c.translate(x, 900); c.scale(kk, kk)
            c.drawRoundRect(R.MakeXYWH(-130, -130, 260, 260), 36, 36, paint(col)); c.drawRoundRect(R.MakeXYWH(-130, -130, 260, 260), 36, 36, stroke(INK, 7))
            if i == 0:
                for j in range(3): c.drawString('z', -40 + j * 26, 20 - j * 26, font('ant', 60), paint(INK))
            elif i == 1: brain(c, 0, 10, 0.4, t)
            else: body_clock(c, 0, 0, 0.42, t, hours=12)
            f = font('ant', 50); c.drawString(lab, -f.measureText(lab) / 2, 190, f, paint(WT_))
            c.restore()
        c.restore()
    if k > 0:
        c.saveLayerAlpha(None, int(255 * k))
        space_bg(c, t, top=(10, 14, 50), bot=(30, 20, 70))
        astronaut_window(c, 540, 1000, 0.95, t)
        draw_stick(c, 540, 1560 + 20 * math.sin(t * 1.5), 1.1, POSES['float'], Face('happy', 'smile'), t=t, helmet=1.0)
        c.restore()
    if t > ts - 0.1:
        kk = eback(pr(t, ts - 0.1, 0.35), 1.6)
        c.save(); c.translate(540, 1700); c.scale(kk, kk)
        c.drawRoundRect(R.MakeXYWH(-330, -60, 660, 120), 30, 30, paint((255, 255, 255))); c.drawRoundRect(R.MakeXYWH(-330, -60, 660, 120), 30, 30, stroke(INK, 7))
        f = font('ant', 56); s_ = 'LONG SPACE MISSIONS'; c.drawString(s_, -f.measureText(s_) / 2, 20, f, paint(INK))
        c.restore()
    top_shade(c, 0.3)
    tier(c, t, S['t0'] + 0.1, 'so why do this?', 'FOR SCIENCE', WT_, size=230, t1=ta - 0.3)
    tier(c, t, ta - 0.1, 'that matters for', 'ASTRONAUTS', YEL, size=240)


def sc_phone(c, t, S):
    u = t - S['t0']
    tr = ph('relax'); tsun = ph('see the sun')
    set_bg(c, (120, 190, 255), (230, 245, 255), spot=False, floor=1420)
    sun_icon(c, 860, 330, 70, t)
    draw_stick(c, 420, 1420, 1.15, POSES['hold'], Face('wide', 'flat', look=(0.3, 1)) if t < tsun else Face('happy', 'smile', 'up', look=(1, -1)), t=t,
               prop=lambda cc, hr, hl: phone(cc, hr[0] + 10, hr[1] - 40, 0.42, t, 1.0 if t < tsun else 0.0))
    for i in range(3):
        y = 760 - i * 60 - (t * 50 % 60); c.drawCircle(300 + i * 12, y, 10 + i * 6, stroke(INK, 4, 0.5 if t < tsun else 0))
    top_shade(c, 0.1, col=(20, 60, 120))
    tier(c, t, S['t0'] + 0.1, 'lose track of time', 'ON YOUR PHONE?', INK, size=190, t1=tr - 0.2)
    tier(c, t, tr - 0.05, 'relax, at least you', 'CAN SEE THE SUN', INK, size=180)


def sc_ask(c, t, S):
    u = t - S['t0']
    cave_bg(c, t, lamp=(540, 1200), lamp_a=0.55)
    camp(c, 760, 1420, 0.8, t)
    beatriz(c, 380, 1420, 1.15, POSES['wave'], Face('happy', 'grin'), t, lamp=0.5)
    comment_bubble(c, 820, 980, 0.8, pr(t, ph('comments') - 0.2, 0.35))
    top_shade(c, 0.5)
    tier(c, t, S['t0'] + 0.1, 'could you last even', 'ONE WEEK?', WT_, size=250)
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint((40, 32, 70)))


SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='early', t0=ph('one woman') - 0.2, fn=sc_early, tin='whip'),
    dict(k='descent', t0=ph('in november') - 0.2, fn=sc_descent, tin='wipe', col=(10, 14, 48)),
    dict(k='rule', t0=ph('the rule was') - 0.2, fn=sc_rule, tin='whip'),
    dict(k='clock', t0=ph('so what happens') - 0.2, fn=sc_clock, tin='wipe', col=(255, 200, 90)),
    dict(k='reset', t0=ph('every morning') - 0.2, fn=sc_reset, tin='zoom'),
    dict(k='siffre', t0=ph('a french scientist') - 0.2, fn=sc_siffre, tin='wipe', col=(40, 190, 180)),
    dict(k='48', t0=ph('sometimes his body') - 0.2, fn=sc_48, tin='whip'),
    dict(k='tuesday', t0=ph('imagine staying') - 0.2, fn=sc_tuesday, tin='wipe', col=(255, 170, 90)),
    dict(k='count', t0=ph('and beatriz') - 0.2, fn=sc_count, tin='whip'),
    dict(k='memory', t0=ph('then your memory') - 0.2, fn=sc_memory, tin='wipe', col=(255, 190, 220)),
    dict(k='count120', t0=ph('and when he counted') - 0.2, fn=sc_count120, tin='zoom'),
    dict(k='hobbies', t0=ph('beatriz filled') - 0.2, fn=sc_hobbies, tin='wipe', col=(90, 70, 120)),
    dict(k='service', t0=ph('her team lowered') - 0.2, fn=sc_room_service, tin='whip'),
    dict(k='flies', t0=ph('then came the worst') - 0.2, fn=sc_flies, tin='zoom'),
    dict(k='rescue', t0=ph('finally in april') - 0.2, fn=sc_rescue, tin='wipe', col=(10, 6, 24)),
    dict(k='160', t0=ph('in her head') - 0.2, fn=sc_160, tin='whip'),
    dict(k='book', t0=ph('and her first words') - 0.2, fn=sc_book, tin='wipe', col=(90, 70, 120)),
    dict(k='why', t0=ph('so why do this') - 0.2, fn=sc_why, tin='wipe', col=(255, 200, 110)),
    dict(k='phone', t0=ph('so next time') - 0.2, fn=sc_phone, tin='whip'),
    dict(k='ask', t0=ph('could you last') - 0.2, fn=sc_ask, tin='wipe', col=(40, 32, 70)),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('your clock breaks') + 0.1, 10, 0.3)
EP.shk(ph('drifts'), 8, 0.3)
EP.shk(ph('flies') + 0.2, 12, 0.5)
EP.shk(ph('five hundred', after=ph('one hundred and sixty')) + 0.1, 14, 0.35); EP.flash(ph('five hundred', after=ph('one hundred and sixty')) + 0.1, 0.5, 0.15)
EP.shk(ph('already'), 8, 0.25)

if __name__ == '__main__':
    EP.main(sys.argv)
