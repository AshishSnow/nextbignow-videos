# ================= shots: "Hoover's free flights" (type A — three mistakes, the last one the cruelest) =================
# Generic props only: no Hoover/Maytag/Candy logos or product designs; brand names appear only as plain caption text.
EXEC_H = {"base": "exec", "top": (44, 60, 96), "tie": (190, 40, 46)}                    # Hoover Europe boss (UK)
EXEC_M = {"base": "exec", "top": (70, 70, 76), "tie": (40, 90, 170), "hair": "white", "hair_col": (220, 220, 214)}   # US parent boss
AGENT = {"base": "lady", "top": (40, 96, 170), "trim": (250, 250, 250)}                  # travel-agency clerk
MUM = {"base": "lady", "top": (200, 90, 60)}
DAD = {"base": "friend", "top": (70, 140, 110)}

SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "everyone") - 0.15, "punch"),
    ("S1a", T("i2", "Hoover") - 0.12, "whip"), ("S1b", T("i2", "European") - 0.25, "whip"),
    ("S2", T("i3", "It") - 0.12, "focus"),
    ("S3", T("a1", "Mistake") - 0.2, "zoom"), ("S4", T("a2", "Britain") - 0.15, "whip"), ("S4b", T("a3", "Get") - 0.12, "punch"),
    ("S5", T("a4", "few") - 0.3, "whip"), ("S6", T("a5", "cheapest") - 0.35, "focus"), ("S7", T("a6", "Two") - 0.15, "whip"),
    ("S8", T("a7", "Hoover") - 0.15, "whip"),
    ("S9", T("b1", "Mistake") - 0.2, "zoom"), ("S10", T("b2", "People") - 0.15, "whip"), ("S11", T("b4", "December") - 0.3, "focus"),
    ("S12", T("b5", "Every") - 0.15, "whip"),
    ("S13", T("c1", "Mistake") - 0.2, "flash"), ("S14", T("c2", "travel") - 0.25, "whip"), ("S15", T("c3", "Airports") - 0.15, "punch"),
    ("S16", T("c4", "Customers") - 0.15, "whip"), ("S17", T("c5", "court") - 0.2, "focus"),
    ("S18", T("d1", "So") - 0.12, "zoom"), ("S19", T("d2", "Hoover's") - 0.15, "whip"), ("S20", T("d3", "thirty") - 0.45, "punch"),
    ("S21", T("d4", "end") - 0.25, "whip"), ("S22", T("d5", "trade") - 0.2, "focus"),
    ("S23", T("d6", "nineteen") - 0.25, "whip"), ("S23b", T("d6", "sold") - 0.15, "punch"), ("S24", T("d7", "loss") - 0.2, "whip"),
    ("S25", T("t1", "Here's") - 0.12, "flash"), ("S26", T("t2", "Free") - 0.15, "whip"),
    ("S27", T("e1", "Running") - 0.15, "focus"), ("S28", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}


def lt(t, sid): return t - SHOT[sid]["start"]


def st0(sid): return SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail="", x=W / 2, maxw=800):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow, maxw=maxw)
    ed_show(f, el, x, y, t, t0, 0.34, out)


def flipel(el): return el[0][:, ::-1].copy(), el[1][:, ::-1].copy()


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INK, WHITE, 24), 540, y, op=clamp((t - t0) / 0.3))


def tickets_burst(f, x, y, t, t0, n_=7, spread=1.0, s=0.42, seed=0):
    """tickets fly out of a point and flutter down"""
    for i in range(n_):
        q = t - t0 - i * 0.11
        if q <= 0: continue
        ang = -math.pi / 2 + (i - (n_ - 1) / 2) * 0.32 * spread
        vx, vy = 560 * math.cos(ang), 760 * math.sin(ang)
        xx = x + vx * q; yy = y + vy * q + 620 * q * q
        if yy > H + 200: continue
        rot_comp(f, scale_el(ticket_el(("NEW YORK", "ORLANDO", "PARIS", "ROME", "MADRID", "NEW YORK", "ORLANDO")[(i + seed) % 7]), s),
                 xx, yy, 25 * math.sin(q * 6 + i), 1.0, 1.0, 0.25)


def mistake_label(f, t, t0, n_, text, col=WHITE, acc=YEL_):
    if t < t0: return
    comp(f, chip(f"MISTAKE #{n_}", RED_, WHITE, 46), 540, 380, scale=pin(t, t0, 0.25))
    say(f, text, 520, 150, col=col, t=t, t0=t0 + 0.1)


# ---- S0: hook — a vacuum cleaner with wings, spraying plane tickets (frame 1 = the most surprising object) ----
def _hook_frame(f, t, u, cap=True):
    title3d(f, "HOOVER", 860, t, -1, size=280, face=(255, 214, 60), side=(150, 50, 20))
    winged_vacuum(f, 540 + 30 * math.sin(t * 1.3), 1150 + 22 * math.sin(t * 2.2), 1.0, t, 1.0, -6 + 3 * math.sin(t * 1.7))
    tickets_burst(f, 560, 1060, (u % 2.6), 0.0, 4, 1.3, 0.34)


def shot_S0(t, n):
    f = sky_bg(t); u = lt(t, "S0")
    _hook_frame(f, t, u)
    ui_word(f, "a vacuum company gives away", "FREE FLIGHTS?", 470, t, -0.5, col=WHITE, size=170, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S0b: ...and everyone says YES — a street full of people holding vacuum boxes up ----
def shot_S0b(t, n):
    u = lt(t, "S0b"); f = set_view("street", t, 1.04, 540, 1000)
    looks = ["friend", "hero", MUM, "oldman", DAD]
    for i, (x, who) in enumerate(zip((150, 330, 540, 750, 930), looks)):
        k = pin(t, st0("S0b") + 0.05 * i, 0.25)
        y = 1760 + (i % 2) * 40
        person(f, x, y, 0.72, who, la=(150, 200), ra=(18, 8) if i % 2 else (150, 200), mouth=2 if (int(t * 6) + i) % 3 else 0,
               expr="wow", brow="up", bob=-30 * k * abs(math.sin(t * 7 + i)))
        if i % 2 == 0: rot_comp(f, scale_el(carton_el(220), 0.6), x, y - 520 * 0.72 - 95 - 30 * k * abs(math.sin(t * 7 + i)), 6 * math.sin(t * 5 + i), 1.0, 1.0, 0.25)
    say(f, "EVERYONE SAID YES", 560, 140, t=t, t0=T("i1", "yes?") - 0.15)
    return finish(f, n)


# ---- S1a: Hoover found out — three bosses fired ----
def shot_S1a(t, n):
    u = lt(t, "S1a"); f = set_view("office", t, 1.18, 540, 1050, blur=2.0)
    tf = T("i2", "fired,") - 0.1
    for i, x in enumerate((230, 540, 850)):
        person(f, x, 1760, 0.78, EXEC_H, la=(18, 8), ra=(18, 8), mouth=0, expr="wow" if t >= tf + 0.1 * i else "n",
               brow="sad" if t >= tf + 0.1 * i else "n", sweat=t >= tf + 0.1 * i, look=(0, -1))
        if t >= tf + 0.12 * i:
            k = clamp((t - tf - 0.12 * i) / 0.16)
            rot_comp(f, stamp_el("FIRED", RED_, 64), x, 1240, -12, 1.5 - 0.5 * eo(k), clamp(k * 3), 0.0)
    ui_word(f, "hoover found out:", "3 BOSSES FIRED", 470, t, T("i2", "Three") - 0.12, col=WHITE, size=150, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S1b: ...and its European business sold ----
def shot_S1b(t, n):
    f = stage("purple", GOLD, 540, 1020, 430); u = lt(t, "S1b")
    comp(f, scale_el(bank_el("HOOVER EUROPE"), 1.0), 540, 1080, scale=pin(t, st0("S1b") + 0.02, 0.3))
    ts = T("i2", "sold.") - 0.1
    if t >= ts:
        k = clamp((t - ts) / 0.18)
        rot_comp(f, sign_el("SOLD", RED_, WHITE, 120, False), 540, 1110, -8, 1.6 - 0.6 * eo(k), clamp(k * 3), 0.3)
        if t < ts + 0.1: f = f + 0.2
    ui_word(f, "its whole", "EUROPEAN BUSINESS", 470, t, T("i2", "whole") - 0.1, col=YEL_, size=130, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S2: roadmap — three mistakes, the last one the cruelest ----
def shot_S2(t, n):
    f = stage("teal", (255, 255, 255), 540, 1050, 430); u = lt(t, "S2")
    tc = T("i3", "cruelest.") - 0.15
    for i in range(3):
        t0 = st0("S2") + 0.15 + 0.28 * i
        if t < t0: continue
        x = 220 + 320 * i; last = i == 2
        hot = last and t >= tc
        col = RED_ if hot else (255, 255, 255)
        el = gcache(("mcard", i, hot), lambda i=i, hot=hot: sign_el(f"#{i + 1}", RED_ if hot else (255, 255, 255), WHITE if hot else INK, 150, False))
        sh = 10 * math.sin((t - tc) * 30) * math.exp(-(t - tc) * 4) if hot else 0
        rot_comp(f, el, x + sh, 1080, (-6, 3, 8)[i], pin(t, t0, 0.25) * (1.25 if hot else 1.0), 1.0, 0.35)
    if t >= tc: comp(f, chip("THE CRUELEST", RED_, WHITE, 40), 860, 1290, scale=pin(t, tc, 0.25))
    ui_word(f, "it took", "3 MISTAKES", 470, t, T("i3", "three") - 0.12, col=WHITE, size=170, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S3: mistake 1 — the maths (scene: the marketing boss proud of his poster) ----
def shot_S3(t, n):
    u = lt(t, "S3"); f = set_view("office", t, 1.25, 540, 1100, blur=3.0)
    comp(f, scale_el(ad_poster_el("SPEND £100", "2 FREE", "FLIGHTS!"), 0.62), 330, 1090, scale=pin(t, st0("S3"), 0.3))
    person(f, 770, 1880, 1.15, EXEC_H, la=(18, 8), ra=(110, 150), mouth=talk(t), expr="smirk", brow="up", look=(-1, 0))
    mistake_label(f, t, st0("S3") + 0.05, 1, "THE MATHS")
    return finish(f, n)


# ---- S4: Britain, 1992 — the shop window offer ----
def shot_S4(t, n):
    u = lt(t, "S4"); f = set_view("store", t, 1.0, 540, 960)
    hud_clock(f, "BRITAIN", "1992", "AUGUST")
    comp(f, scale_el(ad_poster_el("SPEND", "£100+", "ON HOOVER PRODUCTS"), 0.66), 540, 860, scale=pin(t, T("a2", "Spend") - 0.1, 0.3) if t >= T("a2", "Spend") - 0.1 else 0.001)
    comp(f, scale_el(vacuum_el(300), 0.62), 260, 1430)
    person(f, 820, 1720, 0.82, "hero", la=(18, 8), ra=(60, 100), mouth=0, expr="wow" if t >= T("a2", "hundred") else "n", brow="up", look=(-1, -1))
    return finish(f, n)


# ---- S4b: ...get two free return flights to Europe ----
def shot_S4b(t, n):
    f = stage("orange", YEL_, 540, 1000, 440); u = lt(t, "S4b")
    comp(f, scale_el(ad_poster_el("GET", "2 FREE", "RETURN FLIGHTS"), 0.8), 540, 1060, scale=pin(t, st0("S4b"), 0.25))
    tickets_burst(f, 540, 1100, t, T("a3", "free") - 0.05, 7, 1.1, 0.4)
    te = T("a3", "Europe.") - 0.12
    if t >= te: comp(f, chip("TO EUROPE", NAVY_, WHITE, 46), 540, 1440, scale=pin(t, te, 0.25))
    return finish(f, n)


# ---- S5: a few months later — flights to America (map) ----
def shot_S5(t, n):
    f = stage("sky", (255, 255, 255), 540, 1050, 300); u = lt(t, "S5")
    ta = T("a4", "America.") - 0.3
    atlantic(f, clamp((t - T("a4", "bigger.") + 0.1) / 1.6), t)
    comp(f, scale_el(pin_el("BRITAIN"), 0.8), 870, 800, scale=pin(t, st0("S5") + 0.1, 0.25))
    if t >= ta:
        comp(f, scale_el(pin_el("NEW YORK"), 0.8), 250, 840, scale=pin(t, ta, 0.25))
        comp(f, scale_el(pin_el("ORLANDO"), 0.8), 260, 1220, scale=pin(t, ta + 0.15, 0.25))
    ui_word(f, "then they made it bigger:", "AMERICA", 470, t, T("a4", "bigger.") - 0.2, col=INK, size=190, shadow=0.15, lead_col=INK)
    return finish(f, n)


# ---- S6: the cheapest vacuum that counted — £119 tag ----
def shot_S6(t, n):
    u = lt(t, "S6"); f = set_view("store", t, 1.35, 540, 1150, blur=5.0)
    glow_disc(f, (255, 236, 170), 540, 1080, 360, 0.5)
    comp(f, scale_el(vacuum_el(300), 0.95), 540, 1180, scale=pin(t, st0("S6"), 0.3))
    tn = T("a5", "nineteen") - 0.2
    if t >= tn: swing_tag(f, hangtag_el("£119", "CHEAPEST"), 700, 820, t, 7, 70)
    ui_word(f, "the cheapest vacuum that counted", "£119", 470, t, T("a5", "cost") - 0.1, col=RED_, size=200, shadow=0.2, lead_col=INK)
    src(f, "The Hustle; UPI, Apr 1993 ($177)", t, tn + 0.4)
    return finish(f, n)


# ---- S7: two transatlantic tickets weigh far more than the vacuum ----
def shot_S7(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 420); u = lt(t, "S7")
    tt = T("a6", "several") - 0.2; k = eo(clamp((t - tt) / 0.6))
    tickets = gcache("tix2", lambda: el_from(_tix2()))
    balance(f, 540, 900, -16 * k, scale_el(vacuum_el(300), 0.55), tickets, t)
    if t >= tt + 0.4: comp(f, chip("2 TICKETS: ~£600", RED_, WHITE, 40), 760, 1470, scale=pin(t, tt + 0.4, 0.25))
    comp(f, chip("VACUUM: £119", INK, WHITE, 40), 320, 1470, scale=pin(t, st0("S7") + 0.1, 0.25))
    ui_word(f, "the flights were worth", "SEVERAL TIMES MORE", 470, t, T("a6", "worth") - 0.12, col=INK, size=120, shadow=0.1, lead_col=INK)
    src(f, "Ticket value ~£600: BBC News, 2004", t, tt + 0.8, 1540 - 80)
    return finish(f, n)


def _tix2():
    im = Image.new("RGBA", (360, 300), (0, 0, 0, 0))
    for i, d in enumerate(("NEW YORK", "NEW YORK")):
        el = scale_el(ticket_el(d), 0.72); a = (np.dstack([el[0], el[1][..., None]]) * 255).astype(np.uint8)
        pi = Image.fromarray(a, "RGBA").rotate((-8, 6)[i], expand=True, resample=Image.BICUBIC)
        im.alpha_composite(pi, (10 + i * 20, 20 + i * 70))
    return im


# ---- S8: it was buying people holidays (living room: the box opens into a holiday) ----
def shot_S8(t, n):
    u = lt(t, "S8"); f = set_view("parlor", t, 1.08, 540, 1050)
    th = T("a7", "holidays.") - 0.35; k = clamp((t - th) / 0.4)
    person(f, 230, 1740, 0.86, DAD, la=(18, 8), ra=(70, 120), mouth=talk(t) if k > 0 else 0, expr="wow" if k > 0 else "n", brow="up", look=(1, 0))
    person(f, 850, 1740, 0.86, MUM, la=(70, 120), ra=(18, 8), expr="wow" if k > 0 else "smirk", brow="up", look=(-1, 0))
    comp(f, scale_el(carton_el(300, "VACUUM"), 0.95), 540, 1450)
    if k > 0:
        light_rays(f, 540, 1250, (255, 236, 170), 0.6 * k)
        rot_comp(f, scale_el(suitcase_el(300), 0.8), 540, 1180 - 180 * eo(k), 6 * math.sin(t * 3), 1.0, k, 0.3)
        tickets_burst(f, 540, 1250, t, th + 0.1, 5, 0.9, 0.34, seed=2)
    if t < th: say(f, "NOT SELLING VACUUMS...", 520, 110, t=t, t0=T("a7", "selling") - 0.1)
    else: say(f, "BUYING HOLIDAYS", 520, 150, col=(255, 214, 60), t=t, t0=th)
    return finish(f, n)


# ---- S9: mistake 2 — customers can do maths too (close-up, the maths in his head) ----
def shot_S9(t, n):
    u = lt(t, "S9"); f = set_view("parlor", t, 1.5, 540, 1000, blur=6.5)
    person_head_at(f, 540, 1120, 2.2, DAD, mouth=0, expr="smirk" if u > 1.0 else "sus", brow="sus", look=(1, -1))
    mistake_label(f, t, st0("S9") + 0.05, 2, "CUSTOMERS DO MATHS")
    if u > 0.6:
        comp(f, chip("£119 VACUUM  <  £600 FLIGHTS", INK, YEL_, 44), 540, 690, scale=pin(t, st0("S9") + 0.6, 0.25))
    return finish(f, n)


# ---- S10: people bought vacuums they didn't need — a queue walking out with boxes ----
def shot_S10(t, n):
    u = lt(t, "S10"); f = set_view("street", t, 1.0, 540, 960)
    for i in range(5):
        x = 1240 - ((u * 120 + i * 260) % 1500)
        if not (100 < x < 980): continue
        who = ("hero", MUM, "oldman", "friend", "kid")[i]
        ws = math.sin((u + i) * 9)
        person(f, x, 1700, 0.74, who, la=(150, 190), ra=(150, 190), ll=7 + 14 * ws, rl=7 - 14 * ws, mouth=0, expr="smirk", brow="up", look=(-1, 0))
        comp(f, scale_el(carton_el(220), 0.55), x, 1700 - 520 * 0.74 - 90)
    tt = T("b2", "tickets.") - 0.25
    say(f, "JUST FOR THE TICKETS", 560, 130, t=t, t0=tt)
    return finish(f, n)


# ---- S11: an estimated 80,000 extra machines in two months ----
def shot_S11(t, n):
    f = stage("emerald", GOLD, 540, 1000, 420); u = lt(t, "S11")
    te = T("b4", "eighty") - 0.2; k = clamp((t - te) / 1.0)
    if t < te + 0.25:
        rot_comp(f, scale_el(calendar_el("THE RUSH", "JAN" if t >= T("b4", "January") - 0.1 else "DEC"), 0.62), 540, 800, -4 + 2 * math.sin(t * 2), pin(t, st0("S11") + 0.05, 0.3), clamp((te + 0.25 - t) / 0.25), 0.3)
    m = int(3 + 15 * k)
    for i in range(m):
        r_, c_ = divmod(i, 6); x = 210 + c_ * 132 + (r_ % 2) * 30; y = 1400 - r_ * 150
        comp(f, scale_el(carton_el(220), 0.5), x, y)
    if t >= te: odometer(f, 540, 760, "80,000", k, cell=(84, 130))
    ui_word(f, "experts' estimate, two months", "EXTRA MACHINES", 470, t, T("b4", "experts") - 0.1, col=WHITE, size=130, shadow=0.45, lead_col=WHITE)
    src(f, "UPI, Apr 1993: sales-promotion experts' estimate", t, te + 0.6)
    return finish(f, n)


# ---- S12: every buyer was owed two tickets — tickets rain on the boss ----
def shot_S12(t, n):
    u = lt(t, "S12"); f = set_view("office", t, 1.3, 540, 1100, blur=3.0)
    person(f, 540, 1900, 1.25, EXEC_H, la=(40, 60), ra=(40, 60), mouth=0, expr="wow", brow="sad", sweat=True, look=(0, -1),
           bob=4 * math.sin(t * 20))
    for i in range(16):
        ph = (u * 0.55 + i / 16) % 1
        x = 150 + (i * 151) % 780; y = 660 + ph * 1100
        rot_comp(f, scale_el(ticket_el(("NEW YORK", "ORLANDO", "PARIS")[i % 3]), 0.3), x, y, (i * 37) % 60 - 30 + 40 * ph, 1.0, 1.0, 0.2)
    ui_word(f, "every buyer was owed", "2 TICKETS", 470, t, T("b5", "owed") - 0.15, col=YEL_, size=170, shadow=0.45, lead_col=WHITE,
            out=T("b5", "what") - 0.1)
    ui_word(f, "so what would hoover", "DO?", 470, t, T("b5", "what") - 0.05, col=YEL_, size=200, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S13: mistake 3 — the cruelest (dark airport, spotlight) ----
def shot_S13(t, n):
    u = lt(t, "S13"); f = set_view("airport", t, 1.15, 540, 1050, blur=2.5)
    f *= 0.35
    _sglow(f, 540, 1350, 380, (255, 220, 170), 0.7)
    person(f, 540, 1760, 0.95, AGENT, la=(18, 8), ra=(18, 8), mouth=0, expr="smirk", brow="sus", look=(0, 0))
    mistake_label(f, t, st0("S13") + 0.05, 3, "THE CRUELEST", col=RED_, acc=WHITE)
    return finish(f, n)


# ---- S14: the travel agents made the flights hard to get (over-the-shoulder at the desk) ----
def shot_S14(t, n):
    u = lt(t, "S14"); f = set_view("airport", t, 1.12, 540, 1000, blur=1.5)
    th = T("c2", "hard") - 0.2
    person(f, 640, 1760, 0.9, AGENT, la=(18, 8), ra=(40, 60) if t >= th else (18, 8), mouth=talk(t), expr="smirk", brow="sus", look=(-1, 0))
    if t >= th: comp(f, sign_el("SORRY, FULL", RED_, WHITE, 64, False), 640, 1010, scale=pin(t, th, 0.25))
    person(f, 230, 2050, 2.0, "hero", back=True, shadow=False, la=(18, 8), ra=(18, 8))
    ui_word(f, "the agents made the flights", "HARD TO GET", 470, t, T("c2", "agents") - 0.1, col=WHITE, size=160, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S15: airports far from home, dates nobody wanted, expensive extras ----
def shot_S15(t, n):
    f = stage("red", YEL_, 540, 1000, 420); u = lt(t, "S15")
    t1, t2, t3 = T("c3", "Airports") - 0.12, T("c3", "Dates") - 0.12, T("c3", "Expensive") - 0.12
    items = ((t1, 1060 - 260, "FAR FROM HOME", lambda: scale_el(pin_el("THAT AIRPORT?"), 1.0)),
             (t2, 1060, "DATES NOBODY WANTED", lambda: scale_el(calendar_el("FREE DATE", "✗"), 0.42)),
             (t3, 1060 + 260, "EXPENSIVE EXTRAS", lambda: tag_el("+ £££", RED_, WHITE, 70)))
    for i, (tt, y, lab, mk) in enumerate(items):
        if t < tt: continue
        rot_comp(f, gcache(("s15", i), mk), 280, y, (-4, 4, -3)[i], pin(t, tt, 0.25), 1.0, 0.3)
        comp(f, ed_el("", lab, "", big_col=WHITE, big_size=60, maxw=520, shadow=0.4), 690, y, scale=pin(t, tt + 0.05, 0.25))
    return finish(f, n)


# ---- S16: customers furious — a pressure group of thousands ----
def shot_S16(t, n):
    u = lt(t, "S16"); f = set_view("dusk", t, 1.0, 540, 960)
    signs = ("WHERE'S MY FLIGHT?", "PAY UP!", "WE BOUGHT IT!")
    for i, x in enumerate((250, 540, 830)):
        who = ("friend", MUM, "oldman")[i]
        person(f, x, 1800 + 30 * (i % 2), 0.92, who, la=(150, 175), ra=(150, 175), mouth=2 if (int(t * 5) + i) % 2 else 0, expr="mad", brow="mad",
               bob=-12 * abs(math.sin(t * 5 + i)))
        rot_comp(f, sign_el(signs[i], (255, 255, 255), RED_, 34, True), x, 1800 + 30 * (i % 2) - 476 * 0.92 - 90 - 12 * abs(math.sin(t * 5 + i)), (-5, 3, 6)[i], 0.92, 1.0, 0.3)
    say(f, "THOUSANDS JOINED", 600, 140, t=t, t0=T("c4", "Thousands") - 0.12)
    return finish(f, n)


# ---- S17: court cases dragged on for years ----
def shot_S17(t, n):
    f = stage("purple", GOLD, 540, 1000, 420); u = lt(t, "S17")
    yrs = ["1993", "1994", "1995", "1996", "1997", "1998"]
    yi = min(len(yrs) - 1, int(max(0, u - 0.3) / 0.38))
    comp(f, scale_el(calendar_el("COURT", yrs[yi]), 0.62), 360, 1060)
    k = (u * 2.6) % 1.0; ang = -40 + 50 * (1 - abs(math.cos(k * math.pi)))
    rot_comp(f, scale_el(gavel_el(), 0.9), 770, 1020, ang, 1.0, 1.0, 0.3)
    ui_word(f, "the court cases dragged on", "FOR YEARS", 470, t, T("c5", "court") - 0.1, col=YEL_, size=180, shadow=0.45, lead_col=WHITE)
    src(f, "Litigation ran until 1998 (BBC News, 2004)", t, st0("S17") + 0.8)
    return finish(f, n)


# ---- S18: so who paid the bill? (close-up + a receipt unrolling) ----
def shot_S18(t, n):
    u = lt(t, "S18"); f = set_view("office", t, 1.5, 540, 950, blur=6.0)
    person_head_at(f, 360, 1150, 2.0, EXEC_H, mouth=0, expr="wow", brow="sad", sweat=True, look=(1, 0))
    k = clamp(u / 1.4)
    el = receipt_el([("FLIGHTS", "£££", False), ("COURT CASES", "£££", False), ("LAWYERS", "£££", False), ("TOTAL", "???", True)], 420, 460, title="THE BILL")
    comp(f, el, 790, 520 + 640 * eo(k))
    ui_word(f, "so who paid", "THE BILL?", 470, t, T("d1", "who") - 0.15, col=YEL_, size=200, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S19: Maytag (the American owner) fired three top executives ----
def shot_S19(t, n):
    u = lt(t, "S19"); f = set_view("office", t, 1.0, 540, 980)
    tf = T("d2", "fired") - 0.15
    person(f, 780, 1720, 0.95, EXEC_M, la=(18, 8), ra=(90, 95) if t >= tf else (18, 8), mouth=talk(t), expr="mad", brow="mad", look=(-1, 0))
    comp(f, chip("MAYTAG (US OWNER)", INK, WHITE, 34), 780, 1830 - 150)
    for i in range(3):
        x = 420 - i * 150 - (max(0, t - tf - 0.3) * 110 if t >= tf + 0.3 else 0)
        if x < 60: continue
        ws = math.sin((u + i) * 10) if t >= tf else 0
        person(f, x, 1720, 0.78, EXEC_H, la=(70, 110), ra=(70, 110), ll=7 + 12 * ws, rl=7 - 12 * ws, mouth=0, expr="sad", brow="sad", look=(-1, 0))
        comp(f, scale_el(carton_el(220, "MY STUFF"), 0.45), x + 20, 1510)
    say(f, "3 TOP EXECUTIVES FIRED", 560, 110, t=t, t0=tf + 0.1)
    return finish(f, n)


# ---- S20: $30 million set aside, after tax ----
def shot_S20(t, n):
    f = stage("emerald", GOLD, 540, 1020, 430); u = lt(t, "S20")
    rot_comp(f, scale_el(cheque_el("MAYTAG CORP.", "FREE FLIGHTS", "$30,000,000", "Thirty million dollars (after tax)", "the flights", year="1993"), 0.98),
             540, 1060, -4 + 1.5 * math.sin(t * 2), pin(t, st0("S20") + 0.05, 0.3), 1.0, 0.35)
    tt = T("d3", "thirty") - 0.15
    if t >= tt: light_rays(f, 540, 1060, (255, 236, 170), 0.35 * clamp((t - tt) / 0.3))
    ui_word(f, "set aside just to fly people", "$30 MILLION", 470, t, tt, col=YEL_, size=190, shadow=0.45, lead_col=WHITE)
    src(f, "Maytag Q1 1993: $30M after-tax charge (UPI; TIME)", t, tt + 0.6)
    return finish(f, n)


# ---- S21: about 220,000 people flew (departure hall, a jet takes off) ----
def shot_S21(t, n):
    u = lt(t, "S21"); f = set_view("airport", t, 1.0, 540, 960)
    q = clamp((u - 0.3) / 3.0)
    rot_comp(f, scale_el(plane_el(700), 0.55), 200 + 760 * q, 520 - 260 * q * q, -8 * q, 1.0, 1.0 - 0.6 * q, 0.0)
    for i in range(4):
        x = 160 + i * 250 + (u * 60) % 40
        person(f, x, 1740, 0.7, ("hero", MUM, "oldman", DAD)[i], la=(18, 8), ra=(40, 50), mouth=0, expr="smirk", brow="up", look=(0, -1),
               hold=scale_el(suitcase_el(200), 0.5), hold_off=(10, 30))
    tn = T("d4", "twenty") - 0.6
    if t >= tn: odometer(f, 540, 620, "220,000", clamp((t - tn) / 0.9), cell=(80, 124))
    if t >= tn + 0.9: say(f, "FLEW FOR FREE", 830, 130, t=t, t0=tn + 0.9)
    src(f, "~220,000 flew: Marketing Week; Chief Marketer", t, tn + 1.0, 420)
    return finish(f, n)


# ---- S22: total cost £48 million ----
def shot_S22(t, n):
    f = stage("orange", YEL_, 540, 1050, 430); u = lt(t, "S22")
    tf = T("d5", "forty") - 0.2
    cash_pile(f, 540, 1420, 21, clamp((u - 0.1) / 2.2), 1.05)
    ui_word(f, "the total cost", "£48 MILLION", 470, t, tf, col=WHITE, size=200, shadow=0.45, lead_col=WHITE)
    src(f, "Marketing Week, Jun 1995; Campaign", t, tf + 0.6, 1520 - 58)
    return finish(f, n)


# ---- S23: 1995 (split-flap year card) ----
def shot_S23(t, n):
    f = world("night", "purple", t); u = lt(t, "S23")
    flapboard(f, 540, 1000, "1995", t, st0("S23") + 0.05, cell=(150, 220))
    return finish(f, n)


# ---- S23b: Maytag sold Hoover's European business to an Italian rival ----
def shot_S23b(t, n):
    f = stage("sky", (255, 255, 255), 540, 1020, 430); u = lt(t, "S23b")
    comp(f, scale_el(bank_el("HOOVER EUROPE"), 0.9), 540, 1070)
    k = clamp((u - 0.05) / 0.2)
    rot_comp(f, sign_el("SOLD", RED_, WHITE, 120, False), 540, 1120, -8, 1.6 - 0.6 * eo(k), clamp(k * 3), 0.3)
    ti = T("d6", "Italian") - 0.15
    if t >= ti: comp(f, chip("BUYER: CANDY (ITALY)", GRN_, WHITE, 44), 540, 1460 - 40, scale=pin(t, ti, 0.25))
    ui_word(f, "maytag sold", "HOOVER EUROPE", 470, t, st0("S23b") + 0.05, col=INK, size=150, shadow=0.1, lead_col=INK)
    return finish(f, n)


# ---- S24: the loss on that sale: about $135 million ----
def shot_S24(t, n):
    f = stage("cream", None); u = lt(t, "S24")
    tl = T("d7", "thirty") - 0.5
    line_chart(f, 160, 820, 920, 1360, [(0, 0.85), (0.3, 0.7), (0.55, 0.62), (0.75, 0.3), (1.0, 0.05)], clamp(u / 1.6), col=RED_, th=14)
    ui_word(f, "the loss on that sale", "-$135M", 470, t, tl, col=RED_, size=220, shadow=0.1, lead_col=INK)
    src(f, "Maytag 1995 annual report (SEC): after-tax loss on sale", t, tl + 0.6, 1440)
    return finish(f, n)


# ---- S25: the twist — the offer worked: it sold vacuums, far too many ----
def shot_S25(t, n):
    u = lt(t, "S25"); f = set_view("store", t, 1.1, 540, 1000)
    tm = T("t1", "Far") - 0.15
    person(f, 540, 1760, 0.9, EXEC_H, la=(150, 190), ra=(150, 190), mouth=0, expr="wow", brow="sad", sweat=t >= tm, look=(0, -1))
    if t >= tm:
        for i in range(14):
            q = t - tm - i * 0.07
            if q <= 0: continue
            x = 160 + (i * 197) % 760; yy = min(1640 - (i // 5) * 170, -200 + 2600 * q * q)
            comp(f, scale_el(carton_el(220), 0.6), x, yy)
    tw = T("t1", "offer") - 0.1
    if t < tw: say(f, "THE TWIST", 520, 150, col=(255, 214, 60), t=t, t0=T("t1", "twist.") - 0.12)
    elif t < tm: say(f, "THE OFFER WORKED", 520, 130, col=(120, 236, 140), t=t, t0=tw)
    else: say(f, "FAR TOO MANY", 520, 150, col=(255, 90, 80), t=t, t0=tm)
    ts_ = T("t1", "sold") - 0.12
    if ts_ <= t < tm + 0.3: rot_comp(f, closed_sign_el("SOLD OUT", 400), 540, 900, 6 * math.sin(t * 3), pin(t, ts_, 0.25), 1.0, 0.3)
    return finish(f, n)


# ---- S26: takeaway — read the claim rules first (your hand, the small print) ----
def shot_S26(t, n):
    u = lt(t, "S26"); f = set_view("store", t, 1.4, 540, 1000, blur=6.5)
    rot_comp(f, scale_el(ticket_el("FREE FLIGHT", top="*SEE RULES"), 1.2), 470, 960, -6, pin(t, st0("S26"), 0.3), 1.0, 0.35)
    fg_hand(f, 470, 1560, 1.7, ang=-6)
    tc = T("t2", "claim") - 0.2
    if t >= tc:
        comp(f, form_el(360, "CLAIM RULES"), 790, 1230, scale=pin(t, tc, 0.25) * 0.8)
        rot_comp(f, magnifier_el(), 760, 1300, -20, 0.8 * pin(t, tc + 0.1, 0.25), 1.0, 0.3)
    say(f, "WORTH MORE THAN YOU PAY?", 420, 90, t=t, t0=T("t2", "Free") - 0.05)
    if t >= tc: say(f, "READ THE CLAIM RULES", 560, 120, col=(255, 214, 60), t=t, t0=tc)
    return finish(f, n)


# ---- S27: loop — back to frame 1: what happens when everyone says yes? ----
def shot_S27(t, n):
    f = sky_bg(t); u = lt(t, "S27")
    _hook_frame(f, t, u)
    ui_word(f, "running a giveaway? ask:", "WHAT IF EVERYONE SAYS YES?", 470, t, T("e1", "First") - 0.1, col=WHITE, size=110, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S28: send it + brand sting ----
def shot_S28(t, n):
    f = stage("emerald", (255, 214, 120), 540, 880, 420); u = lt(t, "S28")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("free flights w/ a vacuum?!", "read the small print lol", pr), 0.82), 600, 950, scale=pin(t, st0("S28")))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(ticket_el("NEW YORK"), 0.3), hold_off=(20, -40))
        ui_word(f, "send this to the friend who", "NEVER READS THE SMALL PRINT", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=86, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i2", "fired,") - 0.1, 0.3, 12), (T("i2", "sold.") - 0.1, 0.3, 14), (T("i3", "cruelest.") - 0.15, 0.3, 10),
           (T("a5", "nineteen") - 0.2, 0.25, 8), (T("a6", "several") - 0.2 + 0.5, 0.3, 10), (T("b4", "eighty") - 0.2, 0.25, 8),
           (T("c1", "Mistake") - 0.2, 0.3, 14), (T("d2", "fired") - 0.15, 0.3, 12), (T("d3", "thirty") - 0.15, 0.25, 10),
           (T("d6", "sold") - 0.1, 0.3, 14), (T("d7", "thirty") - 0.5, 0.3, 12), (T("t1", "Far") - 0.15, 0.4, 16)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0 + 0.035 * clamp((tt - s["start"]) / max(0.5, s["end"] - s["start"]))   # slow push-in on every shot
    for ti, d, a in IMPACTS:
        if s["start"] - 0.05 <= ti < s["end"] and ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83); z += 0.03 * k
    if dx or dy or abs(z - 1) > 1e-4: f = cam(f, z, W / 2, H / 2, dx, dy)
    return f


def _bl(x, s_):
    if s_ < 0.5: return x
    sm = cv2.resize(x, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    return cv2.resize(cv2.GaussianBlur(sm, (0, 0), s_ / 4), (W, H), interpolation=cv2.INTER_LINEAR)


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); k = sh["trans"]; dt = t - sh["start"]
    if i > 0:
        if k == "focus" and dt < 0.34:
            p = dt / 0.34; prv = rs(SHOTS[i - 1]["id"], t, n); m = eio(p)
            f = _bl(prv, 40 * m) * (1 - m) + _bl(f, 40 * (1 - m)) * m
        elif k == "whip" and dt < 0.22:
            p = 1 - dt / 0.22; M = np.float32([[1, 0, -360 * p * p], [0, 1, 0]])
            f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
        elif k == "zoom" and dt < 0.2:
            p = 1 - dt / 0.2; acc = np.zeros_like(f)
            for q in range(5): acc += cam(f, 1 + 0.06 * q * p)
            f = acc / 5
        elif k == "flash" and dt < 0.14: f = f + 0.8 * (1 - dt / 0.14) ** 1.5
        elif k == "punch" and dt < 0.16: f = cam(f, 1 + 0.08 * (1 - dt / 0.16)) + 0.12 * (1 - dt / 0.16)
    nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    if nx is not None and nx["trans"] == "whip" and sh["end"] - t < 0.14:
        p = 1 - (sh["end"] - t) / 0.14; M = np.float32([[1, 0, 360 * p * p], [0, 1, 0]])
        f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
