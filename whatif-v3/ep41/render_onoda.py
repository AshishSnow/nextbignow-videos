"""What if a war ended and nobody told you? — episode 41 (Hiroo Onoda, Lubang, Dec 1944 - 9 Mar 1974)."""
import sys, os, math, re
import skia
from onodaprops import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('ON_DIR', 'onoda'))
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


def top_shade(c, a=0.45, col=(10, 40, 20)):
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


def sc_hook(c, t, S):
    t29 = ph('twenty nine years'); tn = ph('hiroo onoda')
    jungle(c, t)
    yr = 1945 + int(29 * eio(pr(t, 0.3, max(1.0, tn - 0.6))))
    year_flip(c, 540, 1000, 0.8, yr, t)
    soldier(c, 540, 1520, 1.5, POSES['crouch'], Face('wide', 'flat', 'worried', look=(1, 0)), t, beard=cl((yr - 1945) / 29))
    top_shade(c, 0.5)
    tier(c, t, 0.0, 'what if a war ended...', 'AND NOBODY TOLD YOU?', YEL, size=190, t1=t29 - 0.3)
    tier(c, t, t29 - 0.2, 'hiding in a jungle for', '29 YEARS', WT_, size=290, t1=tn - 0.3)
    tier(c, t, tn - 0.2, 'Japanese soldier', 'HIROO ONODA', YEL, size=240)


def sc_sent(c, t, S):
    tn = ph('never surrender')
    jungle(c, t)
    calendar(c, 830, 1330, 0.55, 'DEC', '1944')
    soldier(c, 460, 1520, 1.8, POSES['stand'], Face('open', 'flat', 'angry'), t)
    if t > tn - 0.2: speech(c, 540, 930, 560, 150, 'NEVER SURRENDER', pr(t, tn - 0.2, 0.35), size=70, col=RED)
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'sent to Lubang island,', 'THE PHILIPPINES', WT_, size=230)


def sc_ended(c, t, S):
    tl = ph('dropped leaflets'); tf = ph('were fake')
    jungle(c, t)
    if t > tl - 0.4:
        k = pr(t, tl - 0.4, 2.5)
        jet(c, lerp(-200, 1300, k), 420, 0.9)
        leaflets(c, t, 1.0 * pr(t, tl, 0.4))
    soldier(c, 300, 1520, 1.4, POSES['shrug'] if t > tf else POSES['stand'], Face('open', 'frown', 'angry') if t > tf else Face('open', 'o', 'up'), t)
    if t > tf - 1.2: big_leaflet(c, 720, 1250, 0.9, pr(t, tf - 1.2, 0.4), fake=pr(t, tf, 0.3))
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'in 1945,', 'THE WAR ENDED', WT_, size=270, t1=tf - 0.4)
    tier(c, t, tf - 0.3, 'he thought the leaflets were', 'A TRICK', RED, size=290)


def sc_family(c, t, S):
    tl = ph('loudspeakers')
    jungle(c, t)
    soldier(c, 360, 1520, 1.6, POSES['hug'], Face('open', 'frown', 'angry'), t)
    for i in range(3):
        k = pr(t, S['t0'] + 0.3 + i * 0.4, 0.35)
        if k > 0:
            c.save(); c.translate(730 + (i - 1) * 90, 1150 + i * 60); c.rotate(-10 + i * 10); c.scale(eback(k, 1.6), eback(k, 1.6))
            c.drawRect(R.MakeXYWH(-80, -55, 160, 110), paint((255, 250, 230))); c.drawRect(R.MakeXYWH(-80, -55, 160, 110), stroke(INK, 5))
            c.drawLine(-80, -55, 0, 10, stroke(INK, 3)); c.drawLine(80, -55, 0, 10, stroke(INK, 3))
            c.restore()
    if t > tl - 0.2:
        c.save(); c.translate(780, 950)
        c.drawPath(poly([(-40, -30), (60, -80), (60, 80), (-40, 30)], True), paint((200, 200, 210))); c.drawPath(poly([(-40, -30), (60, -80), (60, 80), (-40, 30)], True), stroke(INK, 5))
        for i in range(3): c.drawArc(R.MakeXYWH(60 + i * 24, -50 - i * 14, 40 + i * 20, 100 + i * 28), -40, 80, False, stroke(YEL, 6, 0.5 + 0.5 * math.sin(t * 8 + i)))
        c.restore()
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'letters, photos, loudspeakers...', "HE DIDN'T BELIEVE IT", YEL, size=200)


def sc_stayed(c, t, S):
    td = ph('then decades')
    jungle(c, t)
    u = t - S['t0']
    yr = 1946 + int(25 * eio(pr(t, S['t0'] + 0.3, max(2.0, ph("it wasn't harmless") - S['t0'] - 0.6))))
    year_flip(c, 540, 1000, 0.7, yr, t)
    soldier(c, lerp(150, 900, (u * 0.12) % 1), 1520, 1.3, walk_pose(t * 1.2, 0.7), Face('open', 'flat', 'angry'), t, beard=cl((yr - 1945) / 29), worn=cl((yr - 1945) / 20))
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'so he stayed. years...', 'THEN DECADES', WT_, size=260, t1=None)


def sc_harm(c, t, S):
    ta = ph('he was alone')
    set_bg(c, (40, 50, 60), (80, 90, 100), circle=(110, 120, 130), cy=1150, r=440, spot=True, t=t)
    if t < ta - 0.3:
        for i, x in enumerate((340, 540, 740)):
            a = 1 - pr(t, S['t0'] + 3.0 + i * 1.5, 0.8) if i > 0 else 1.0
            soldier(c, x, 1520, 1.3, POSES['stand'], Face('open', 'flat', 'worried'), t, rot=0) if a > 0.05 else None
        top_shade(c, 0.45, (10, 10, 20))
        tier(c, t, S['t0'] + 0.1, "it wasn't harmless:", 'PEOPLE GOT HURT', (255, 170, 160), size=230)
        return
    soldier(c, 540, 1520, 1.8, POSES['hug'], Face('open', 'frown', 'worried'), t, beard=0.6, worn=1.0)
    top_shade(c, 0.45, (10, 10, 20))
    tier(c, t, ta - 0.2, 'in the end,', 'HE WAS ALONE', WT_, size=280)


def sc_suzuki(c, t, S):
    tp = ph('a panda'); ts = ph('abominable snowman')
    set_bg(c, (255, 150, 60), (255, 210, 130), circle=(255, 235, 190), cy=1150, r=440, spot=True, t=t)
    explorer(c, 300, 1520, 1.6, POSES['wave'], Face('happy', 'grin'), t)
    for i, (tt_, fn, lbl) in enumerate(((ph('lieutenant onoda'), lambda cc: soldier(cc, 0, 120, 0.7, POSES['stand'], Face('open', 'flat', 'angry'), t), 'ONODA'),
                                        (tp, lambda cc: panda(cc, 0, 130, 0.55, t), 'PANDA'),
                                        (ts, lambda cc: snow_beast(cc, 0, 130, 0.55, t), 'YETI'))):
        k = pr(t, tt_ - 0.2, 0.35)
        if k > 0:
            card3d(c, 760, 900 + i * 230, 280, 210, 6 * math.sin(t + i), 0, fn, k=k)
    top_shade(c, 0.3, (120, 50, 0))
    tier(c, t, S['t0'] + 0.1, '1974: explorer Norio Suzuki', 'GOES LOOKING', INK, size=250, small_col=INK, t1=ph('lieutenant onoda') - 0.3)
    tier(c, t, ph('lieutenant onoda') - 0.2, 'his checklist:', 'ONODA, PANDA, YETI', INK, size=190, small_col=INK)


def sc_found(c, t, S):
    tr = ph('refused to give up'); tc = ph('commanding officer')
    jungle(c, t)
    explorer(c, 300, 1520, 1.5, POSES['wave'], Face('happy', 'grin'), t)
    soldier(c, 780, 1520, 1.5, POSES['hug'] if t > tr else POSES['shock'], Face('open', 'frown', 'angry') if t > tr else Face('wide', 'o', 'up'), t, flip=True, beard=0.7, worn=1.0)
    if t > tc - 0.3: speech(c, 700, 950, 560, 150, 'ONLY IF MY BOSS SAYS', pr(t, tc - 0.3, 0.35), size=58, col=INK)
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'and he found him in', '4 DAYS', YEL, size=290, t1=tr - 0.3)
    tier(c, t, tr - 0.2, 'but Onoda still', 'REFUSED', RED, size=290)


def sc_cmdr(c, t, S):
    tb = ph('bookshop')
    set_bg(c, (90, 60, 150), (170, 120, 220), circle=(210, 170, 250), cy=1150, r=440, spot=True, t=t)
    bookshelf(c, 700, 1520, 0.9)
    commander(c, 380, 1520, 1.7, POSES['hold'], Face('open', 'smile'), t)
    top_shade(c, 0.4)
    tier(c, t, S['t0'] + 0.1, 'Suzuki found his old commander', 'SELLING BOOKS', YEL, size=250)


def sc_orders(c, t, S):
    tr = ph('handed over')
    jungle(c, t)
    calendar(c, 830, 950, 0.5, 'MAR 9', '1974')
    commander(c, 300, 1520, 1.5, POSES['hold'], Face('open', 'flat'), t)
    c.save(); c.translate(300 + 90, 1520 - 210); c.drawRect(R.MakeXYWH(-50, -60, 100, 120), paint((255, 252, 235))); c.drawRect(R.MakeXYWH(-50, -60, 100, 120), stroke(INK, 4)); c.restore()
    soldier(c, 760, 1520, 1.5, POSES['hold'] if t > tr else POSES['stand'], Face('open', 'flat', 'worried') if t < tr else Face('closed', 'smile'), t, flip=True, beard=0.7, worn=1.0)
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'new orders:', 'STOP FIGHTING', YEL, size=290, t1=tr - 0.3)
    tier(c, t, tr - 0.2, 'after 29 years, he', 'GAVE UP HIS RIFLE', WT_, size=200)


def sc_missed(c, t, S):
    set_bg(c, (40, 180, 200), (130, 225, 235), circle=(210, 250, 255), cy=1150, r=440, spot=True, t=t)
    for i, (p_, kind) in enumerate((('moon landing', 'moon'), ('color tv', 'tv'), ('the beatles', 'record'))):
        k = pr(t, ph(p_) - 0.2, 0.35)
        if k > 0:
            card3d(c, 260 + i * 280, 1180, 250, 290, 8 * math.sin(t + i), 0, lambda cc, kind=kind: missed_icon(cc, kind, 1.1, t), k=k)
    top_shade(c, 0.3, (0, 60, 80))
    tier(c, t, S['t0'] + 0.1, 'a whole world changed:', 'HE MISSED IT ALL', INK, size=240, small_col=INK)


def sc_later(c, t, S):
    ts = ph('nature school'); t91 = ph('ninety one')
    set_bg(c, (60, 200, 120), (150, 240, 180), circle=(220, 255, 230), cy=1150, r=440, spot=True, t=t)
    if t < ts - 0.2:
        cow(c, 720, 1500, 1.2, t)
        draw_stick(c, 330, 1520, 1.7, POSES['wave'], Face('happy', 'grin'), t=t, scarf=None)
        top_shade(c, 0.3, (0, 70, 30))
        tier(c, t, S['t0'] + 0.1, 'later, he raised cattle in', 'BRAZIL', WT_, size=300)
        return
    draw_stick(c, 540, 1520, 1.7, POSES['arms_up'], Face('happy', 'grin'), t=t, scarf=None)
    for i, x in enumerate((220, 360, 720, 860)):
        draw_stick(c, x, 1520, 0.9, POSES['arms_up'] if (int(t * 2) + i) % 2 else POSES['wave'], Face('happy', 'grin'), t=t, scarf=[YEL, RED, TEAL, ORANGE][i])
    top_shade(c, 0.3, (0, 70, 30))
    tier(c, t, ts - 0.1, 'then he started a', 'NATURE SCHOOL', WT_, size=270, t1=t91 - 0.4)
    tier(c, t, t91 - 0.3, 'he lived to', '91', YEL, size=300)


def sc_ask(c, t, S):
    jungle(c, t)
    soldier(c, 400, 1520, 1.5, POSES['shrug'], Face('happy', 'smile'), t, beard=0.6)
    comment_bubble(c, 780, 1100, 0.75, pr(t, ph('comments') - 0.2, 0.35))
    top_shade(c, 0.45)
    tier(c, t, S['t0'] + 0.1, 'what would it take to convince', 'YOU?', YEL, size=300)
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint((10, 40, 20)))


SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='sent', t0=ph('in december') - 0.2, fn=sc_sent, tin='whip'),
    dict(k='ended', t0=ph('just a few months') - 0.2, fn=sc_ended, tin='flash'),
    dict(k='family', t0=ph('his family sent') - 0.2, fn=sc_family, tin='zoom'),
    dict(k='stayed', t0=ph('so he stayed') - 0.2, fn=sc_stayed, tin='wipe', col=(120, 170, 80)),
    dict(k='harm', t0=ph("it wasn't harmless") - 0.2, fn=sc_harm, tin='wipe', col=(60, 70, 80)),
    dict(k='suzuki', t0=ph('then in nineteen seventy') - 0.2, fn=sc_suzuki, tin='flash'),
    dict(k='found', t0=ph('and he actually found') - 0.2, fn=sc_found, tin='whip'),
    dict(k='cmdr', t0=ph('so suzuki went back') - 0.2, fn=sc_cmdr, tin='wipe', col=(170, 120, 220)),
    dict(k='orders', t0=ph('on march ninth') - 0.2, fn=sc_orders, tin='zoom'),
    dict(k='missed', t0=ph("he'd missed") - 0.2, fn=sc_missed, tin='whip'),
    dict(k='later', t0=ph('later he moved') - 0.2, fn=sc_later, tin='wipe', col=(150, 240, 180)),
    dict(k='ask', t0=ph('so what would it take') - 0.2, fn=sc_ask, tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('were fake'), 8, 0.25)

if __name__ == '__main__':
    EP.main(sys.argv)
