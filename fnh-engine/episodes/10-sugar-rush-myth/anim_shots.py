# ================= shots: FreshNestHub 10 — "Is the sugar rush real?" (refutation structure: myth -> busted -> how it works -> tests -> twist) =================
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "Candy") - 0.15, "punch"), ("S1b", T("i2", "Scientists") - 0.15, "whip"),
    ("S2", T("i3", "And") - 0.15, "focus"),
    ("S3", T("a1", "Here's") - 0.15, "whip"), ("S3b", T("a1", "boom,") - 0.1, "punch"), ("S4", T("a2", "But") - 0.15, "flash"),
    ("S5", T("b1", "Blood") - 0.15, "zoom"), ("S5b", T("b1", "It's") - 0.12, "whip"),
    ("S6", T("b2", "When") - 0.15, "whip"), ("S6b", T("b2", "It's") - 0.12, "zoom"),
    ("S7", T("b3", "It") - 0.15, "whip"), ("S7b", T("b3", "Think") - 0.12, "punch"),
    ("S8", T("b4", "It") - 0.15, "whip"), ("S8b", T("b4", "to") - 0.1, "zoom"),
    ("S9", T("b5", "So") - 0.15, "focus"), ("S9b", T("b5", "Like") - 0.12, "punch"),
    ("S10", T("c1", "But") - 0.15, "whip"), ("S11", T("c2", "Some") - 0.15, "whip"), ("S12", T("c3", "And") - 0.15, "zoom"),
    ("S13", T("c4", "In") - 0.15, "whip"), ("S14", T("c5", "The") - 0.15, "punch"),
    ("S15", T("d1", "So") - 0.15, "focus"), ("S16", T("d2", "Thirty-five") - 0.15, "whip"), ("S16b", T("d2", "Every") - 0.12, "zoom"),
    ("S17", T("d3", "But") - 0.15, "whip"), ("S18", T("d4", "Those") - 0.15, "focus"), ("S18b", T("d4", "They") - 0.12, "punch"),
    ("S19", T("d5", "Same") - 0.15, "flash"), ("S19b", T("d5", "The") - 0.1, "zoom"),
    ("S20", T("e1", "So") - 0.15, "whip"), ("S21", T("e2", "Parties.") - 0.1, "punch"), ("S21c", T("e2", "Friends,") - 0.1, "whip"),
    ("S21d", T("e2", "staying") - 0.1, "zoom"),
    ("S22", T("f1", "One") - 0.15, "focus"), ("S23", T("f2", "And") - 0.15, "whip"),
    ("S24", T("g1", "So") - 0.15, "focus"), ("S25", T("g2", "Send") - 0.15, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SWEET_C = (236, 100, 180); SUGAR_C = (255, 150, 60)


def lt(t, sid): return t - SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def uw(f, lead, big, t, t0, acc=YEL_, size=170, out=None, y=470):
    """white caption with shadow (dark sets)."""
    ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.5, lead_col=WHITE, out=out)


def rays(f, x, y, r, col, amt, t, nr=14):
    if amt <= 0.01: return
    ov = np.zeros((H, W), np.float32); a0 = t * 0.25
    for i in range(nr):
        a = a0 + i * 2 * math.pi / nr; da = math.pi / nr * 0.5
        pts = np.array([[x, y], [x + r * math.cos(a - da), y + r * math.sin(a - da)], [x + r * math.cos(a + da), y + r * math.sin(a + da)]], np.int32)
        cv2.fillPoly(ov, [pts], 1.0, cv2.LINE_AA)
    ov = cv2.GaussianBlur(ov, (0, 0), 6) * np.clip(1 - np.hypot(_xx - x, _yy - y) / r, 0, 1)
    f += ov[..., None] * np.array(C(col), np.float32) * amt


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / d))


def munch(t, rate=0.42):
    ph = (t / rate) % 1.0
    return (2 if ph < 0.5 else 0), int(t / rate)


def st_(sid): return SHOT[sid]["start"]


def tri(x): x = x % 1.0; return 2 * x if x < 0.5 else 2 - 2 * x


def hyper_lines(f, x, y, r, t, col=YEL_, n=8):
    """zig-zag 'hyper' energy marks around a point (what the myth says sugar does)."""
    for i in range(n):
        a = i * 2 * math.pi / n + t * 2.5; pts = []
        for j in range(4):
            rr = r + j * 26; aj = a + (0.12 if j % 2 else -0.12)
            pts.append((x + rr * math.cos(aj), y + rr * math.sin(aj)))
        P = np.array(pts, np.int32); cv2.polylines(f, [P], False, C(INK), 14, cv2.LINE_AA); cv2.polylines(f, [P], False, C(col), 7, cv2.LINE_AA)


def flying_candy(f, t, cx=540, cy=1000, R=360, n=7, sp=1.6, s=0.42, seed=0):
    for i in range(n):
        a = t * sp + i * 2 * math.pi / n + seed; r_ = R * (0.8 + 0.2 * math.sin(t * 2 + i))
        rot_comp(f, scale_el(candy_el(CANDY_COLS[(i + seed) % 5]), s), cx + r_ * math.cos(a), cy + r_ * 0.7 * math.sin(a), t * 200 + i * 40, 1.0, 1.0, 0.2)


def walls(f, col=(150, 90, 50)):
    for x0, x1 in ((40, 130), (950, 1040)):
        f[300:1520, x0:x1] = np.array(C(col), np.float32)
        for yy in range(320, 1520, 90): cv2.line(f, (x0, yy), (x1, yy), C(tuple(int(c * 0.7) for c in col)), 4, cv2.LINE_AA)
        cv2.rectangle(f, (x0, 300), (x1, 1520), C(INK), 6, cv2.LINE_AA)


# ---- S0: hook — Chubby mid sugar-rush, bouncing with candy flying... then the frame FREEZES (record scratch) ----
TFZ = T("i1", "myth?") - 0.12


def shot_S0(t, n):
    f = stage("night"); moon(f, 830, 760, 90)
    te = min(t, TFZ); frz = t >= TFZ
    comp(f, scale_el(bucket_el(), 0.62), 200, 1380)
    ph = (te * 1.9) % 1.0; up = math.sin(math.pi * ph)
    y = 1470 - 330 * up; x = 560 + 90 * math.sin(te * 3.0)
    sq = 0.6 if (ph < 0.08 or ph > 0.92) else -0.35 * up
    if not frz: speed_lines(f, t, 0.6, 700, 1300, 10)
    flying_candy(f, te, 560, 960, 380, 7, 1.8, 0.42)
    chub(f, x, y, 1.0, la=(160, 170), ra=(150 + 20 * math.sin(te * 9), 175), ll=6 + 30 * up, rl=6 - 20 * up, mouth=3 if not frz else "o",
         expr="happy" if not frz else "wow", brow="up", look=(0, 0) if not frz else (1, 0), squash=sq, shadow=False, lean=10 * math.sin(te * 6))
    contact(f, x, 1474, 260 * (1 - 0.5 * up), 0.3)
    if not frz: hyper_lines(f, x, y - 420, 150, te)
    if frz:
        k = clamp((t - TFZ) / 0.12)
        g = (f @ LUMA)[..., None]; f[:] = f * (1 - 0.55 * k) + g * 0.55 * k
        if t < TFZ + 0.16: f += 0.5 * (1 - (t - TFZ) / 0.16)
        comp(f, burst_el("?!", YEL_, INK, 80), 830, 1000, scale=pin(t, TFZ + 0.05, 0.22))
    uw(f, "do you know the", "[SUGAR RUSH]", t, 0.12, out=T("i1", "might") - 0.05, size=190)
    uw(f, "might be a", "[MYTH?]", t, T("i1", "might"), size=230)
    return finish(f, n)


# ---- S1: candy makes kids bounce off the walls (ping-pong) ----
def shot_S1(t, n):
    f = stage("pink", (255, 236, 200), 540, 980, 360); u = lt(t, "S1"); walls(f)
    ph = tri(u * 0.85 + 0.25); x = 250 + 580 * ph; hitw = (u * 0.85 + 0.25) % 0.5
    sq = 0.7 * math.exp(-hitw * 30) if hitw < 0.15 else 0.0
    y = 1400 - 140 * abs(math.sin(u * 7))
    chub(f, x, y, 0.82, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up", squash=-sq, lean=(-12 if ph < 0.5 else 12),
         look=(1, -1) if t >= T("i2", "right?") - 0.1 else (0, 0), shadow=False)
    if sq > 0.1:
        wx = 150 if x < 540 else 930; dust_puff(f, wx, y - 200, t, t - hitw * 1.2, 7)
        comp(f, burst_el("BOING!", YEL_, INK, 40), wx + (90 if x < 540 else -90), y - 520, scale=0.8 + 0.2 * sq)
    flying_candy(f, u, x, 1000, 300, 5, 2.4, 0.32, 2)
    uw(f, "candy makes kids", "[BOUNCE] OFF THE WALLS", t, st_("S1") + 0.1, size=120)
    return finish(f, n)


# ---- S1b: scientists tested it ----
def shot_S1b(t, n):
    f = stage("teal", (255, 236, 160), 700, 1060, 330); u = lt(t, "S1b")
    cv2.rectangle(f, (540, 1290), (980, 1320), C(INK), -1, cv2.LINE_AA); cv2.rectangle(f, (550, 1296), (970, 1314), C((240, 240, 250)), -1, cv2.LINE_AA)
    rot_comp(f, scale_el(candy_el(CANDY_COLS[0]), 0.75), 760, 1230 + 6 * math.sin(t * 4), 8 * math.sin(t * 2), 1.0, 1.0, 0.3)
    mx = 700 + 60 * math.sin(u * 2.4)
    scientist(f, 340, 1470, 1.0, la=(20, 10), ra=(80, 40), mouth=talk(t), brow="sus", expr="sus", look=(1, 0.3),
              hold=scale_el(magnifier_el(), 0.5), hold_off=(50, -70), hold_front=True)
    comp(f, chip("TEST #1", INK, WHITE, 30), 760, 1120, op=clamp((u - 0.4) / 0.3))
    uw(f, "scientists", "[TESTED IT]", t, T("i2", "Scientists") - 0.05, size=200)
    return finish(f, n)


# ---- S2: open loop — the real reason is way weirder (curtain tease) ----
def curtain(f, gap, t, y0=640, y1=1500):
    for side in (-1, 1):
        x0, x1 = (60, 540 - gap / 2) if side < 0 else (540 + gap / 2, 1020)
        f[y0:y1, int(x0):int(x1)] = np.array(C((200, 20, 40)), np.float32)
        for xx in np.arange(x0 + 30, x1, 60): cv2.line(f, (int(xx), y0), (int(xx + 8 * math.sin(t * 2 + xx)), y1), C((140, 8, 24)), 16, cv2.LINE_AA)
        cv2.rectangle(f, (int(x0), y0), (int(x1), y1), C(INK), 6, cv2.LINE_AA)
    f[y0 - 30:y0 + 20, 40:1040] = np.array(C(GOLD), np.float32); cv2.rectangle(f, (40, y0 - 30), (1040, y0 + 20), C(INK), 6, cv2.LINE_AA)


def shot_S2(t, n):
    f = stage("purple"); u = lt(t, "S2")
    tw = T("i3", "weirder.") - 0.2
    gap = 40 + 220 * ramp(t, tw, 0.4)
    # behind the curtain: party silhouettes bouncing (the answer we tease)
    g = f.copy(); rays(g, 540, 1000, 700, (255, 220, 120), 0.6, t)
    for i, x in enumerate((430, 540, 650)):
        yy = 1150 - 60 * abs(math.sin(t * 6 + i)); cv2.circle(g, (x, int(yy)), 60, C(INK), -1, cv2.LINE_AA)
        cv2.fillPoly(g, [np.array([[x - 40, yy - 50], [x + 40, yy - 50], [x, yy - 150]], np.int32)], C(INK), cv2.LINE_AA)
    f[640:1500, 540 - int(gap / 2):540 + int(gap / 2)] = g[640:1500, 540 - int(gap / 2):540 + int(gap / 2)]
    curtain(f, gap, t)
    chub(f, 900, 1490, 0.7, la=(20, 10), ra=(-150, -150), mouth=talk(t), expr="sus", brow="sus", look=(-1, 0), lean=-8)
    for i, (x, y) in enumerate(((250, 820), (380, 760))):
        comp(f, ed_el("", "?", "", big_col=YEL_, big_size=110, shadow=0.5), x, y + 10 * math.sin(t * 4 + i), op=clamp((u - 0.2 - 0.2 * i) / 0.2))
    uw(f, "the real reason is", "[WAY WEIRDER]", t, T("i3", "real") - 0.1, size=170)
    return finish(f, n)


# ---- S3: the MYTH: sugar floods your blood ----
def shot_S3(t, n):
    f = stage("orange"); u = lt(t, "S3")
    myth_tag(f, 540, 700, t, T("a1", "myth.") - 0.15)
    ts = T("a1", "Sugar") - 0.1
    rot_comp(f, scale_el(candy_el(CANDY_COLS[1]), 0.8), 200, 1070, 10 * math.sin(t * 3), pin(t, st_("S3") + 0.05, 0.3), 1.0, 0.3)
    draw_arrow(f, 300, 1070, 380, 1070, ramp(t, ts, 0.25), WHITE, 12, 34)
    yc, r = 1080, 150
    blood(f, t, yc, r, 400, 960, 0, 160, 9)
    nfl = int(clamp((t - ts) / 1.2) * 18)
    rng = np.random.default_rng(5)
    for i in range(18):
        ox, oy = rng.uniform(0, 600), rng.uniform(-r * 0.7, r * 0.7)
        if i >= nfl: continue
        x = 420 + (ox + 260 * t) % 520
        comp(f, scale_el(sugar_el("happy" if i % 3 else "sly"), 0.4), x, yc + oy + 8 * math.sin(t * 5 + i))
    label_at(f, "BLOOD", 680, 1360, t, ts + 0.3, 680, yc + r + 30)
    uw(f, "sugar floods your", "[BLOOD]", t, ts, size=200) if t >= ts else uw(f, "here's the", "[MYTH]", t, st_("S3") + 0.1, acc=WHITE, size=200)
    return finish(f, n)


# ---- S3b: ...and BOOM, you're hyper (still the myth) ----
def shot_S3b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 440); u = lt(t, "S3b")
    rays(f, 540, 1000, 820, (255, 120, 40), 0.45, t)
    jx = 10 * math.sin(t * 61); jy = 8 * math.cos(t * 53)
    chub(f, 540 + jx, 1460 + jy, 1.1, la=(160, 175), ra=(160, 175), mouth=3, expr="wow", brow="up", look=(math.sin(t * 20), 0),
         squash=-0.3 * abs(math.sin(t * 12)), shadow=True)
    hyper_lines(f, 540 + jx, 1460 - 460, 200, t, RED_, 10)
    comp(f, burst_el("BOOM!", RED_, WHITE, 70), 820, 760, scale=pin(t, st_("S3b") + 0.02, 0.22))
    comp(f, tag_el("MYTH", RED_, WHITE, 40), 200, 1400)
    ui_word(f, "and boom, you're", "[HYPER]", 470, t, st_("S3b") + 0.05, col=INK, acc=RED_, size=230)
    return finish(f, n)


# ---- S4: BUSTED — your body won't let that happen ----
def shot_S4(t, n):
    f = stage("sky", (255, 255, 255), 540, 1100, 380); u = lt(t, "S4")
    tw = T("a2", "why.") - 0.2
    if t < tw: myth_tag(f, 540, 720, t, st_("S4") - 1.0, st_("S4") + 0.15)
    z = 1 + 0.5 * ramp(t, tw, 0.5)
    g = f.copy()
    chub(g, 540, 1480, 1.0, la=(35, -75), ra=(35, -75), mouth=talk(t), expr="smirk", brow="n", look=(0, 0))
    cv2.circle(g, (540, 1265), 30 + int(14 * math.sin(t * 6)), C(YEL_), 6, cv2.LINE_AA)
    g = cam(g, z, 540, 1265)
    m = np.zeros((H, W), np.float32); m[800:] = 1.0; m = cv2.GaussianBlur(m, (0, 0), 20)
    f[:] = f * (1 - m[..., None]) + g * m[..., None]
    uw(f, "your body", "[WON'T LET IT]", t, T("a2", "body") - 0.15, size=170) if t < tw else uw(f, "here's", "[WHY]", t, tw, size=230)
    return finish(f, n)


# ---- S5: blood sugar = sugar riding in your blood (pre-training: name the part on sight) ----
def blood(f, t, yc=1060, r=250, x0=60, x1=1020, sugar=8, flow=220, seed=4):
    cv2.rectangle(f, (x0, int(yc - r - 30)), (x1, int(yc + r + 30)), C((170, 20, 40)), -1, cv2.LINE_AA)
    g = np.linspace(0, 1, 2 * r)[:, None, None]
    f[int(yc - r):int(yc + r), x0:x1] = np.array(C((255, 214, 206)), np.float32) * (1 - g * 0.3) + np.array(C((240, 150, 150)), np.float32) * (g * 0.3)
    for yy in (yc - r - 30, yc - r, yc + r, yc + r + 30): cv2.line(f, (x0, int(yy)), (x1, int(yy)), C(INK), 6 if yy in (yc - r - 30, yc + r + 30) else 3, cv2.LINE_AA)
    rng = np.random.default_rng(seed); L = x1 - x0; pts = []
    for i in range(10):
        ox = rng.uniform(0, L); oy = rng.uniform(-r * 0.6, r * 0.6)
        x = x0 + (ox + flow * t) % L; y = yc + oy + 10 * math.sin(t * 3 + i)
        cv2.ellipse(f, (int(x), int(y)), (62, 44), 12 * math.sin(t + i), 0, 360, C(INK), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(x), int(y)), (56, 38), 12 * math.sin(t + i), 0, 360, C((214, 30, 44)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(x), int(y)), (28, 17), 12 * math.sin(t + i), 0, 360, C((160, 14, 28)), -1, cv2.LINE_AA)
        if i < sugar:
            comp(f, scale_el(sugar_el("happy"), 0.42), x, y - 58); pts.append((x, y - 58))
    return pts


def shot_S5(t, n):
    f = stage("red"); u = lt(t, "S5")
    pts = blood(f, t, yc=1080, r=240, x0=60, x1=1020, sugar=7)
    tr = T("b1", "riding") - 0.15
    if t >= tr:
        px, py = min(pts, key=lambda p: abs(p[0] - 560)); spotlight(f, px, py, 90, 0.45 * ramp(t, tr, 0.3))
        label_at(f, "SUGAR (GLUCOSE)", 540, 1420, t, tr, px, py + 40)
    cx_ = min(pts, key=lambda p: abs(p[0] - 300))[0] if pts else 300
    label_at(f, "RED BLOOD CELL", 330, 700, t, st_("S5") + 0.5, cx_, 860)
    uw(f, "blood sugar =", "[SUGAR IN YOUR BLOOD]", t, st_("S5") + 0.1, size=110)
    return finish(f, n)


# ---- S5b: it's fuel for your cells ----
def shot_S5b(t, n):
    f = stage("emerald"); u = lt(t, "S5b")
    nin = min(6, int(clamp(u / 1.6) * 7))
    comp(f, scale_el(cell_el(1.0, nin), 0.95), 470, 1060, scale=pin(t, st_("S5b") + 0.02, 0.3))
    k = u % 0.6 / 0.6
    if nin < 6: comp(f, scale_el(sugar_el("happy"), 0.42), 110 + 110 * eo(k), 1060 - 60 * math.sin(math.pi * k), op=1 - k * 0.3)
    gauge_tube(f, 880, 760, 1340, 0.15 + 0.7 * clamp(u / 1.8), 0.85, 70, (60, 220, 120), "FULL")
    comp(f, chip("ENERGY", INK, WHITE, 26), 880, 1400)
    if u > 1.2: sparkles(f, 470, 1000, t, st_("S5b") + 1.2, 10, 260)
    label_at(f, "BODY CELL", 300, 700, t, st_("S5b") + 0.3, 380, 820)
    uw(f, "it's", "[FUEL] FOR YOUR CELLS", t, st_("S5b") + 0.08, size=140)
    return finish(f, n)


# ---- S6: x-ray belly — when it rises, your pancreas wakes up ----
def shot_S6(t, n):
    f = stage("cream", (255, 214, 160), 540, 980, 420); u = lt(t, "S6")
    tp = T("b2", "pancreas") - 0.15; tw = T("b2", "wakes") - 0.1
    chub(f, 470, 1590, 1.42, la=(30, 20), ra=(30, 20), mouth=0, expr="n", brow="n", look=(0.6, -0.4), shadow=False)
    bx, by, br = 470 + 0, 1590 - 215 * 1.42 + 30, 168
    cv2.circle(f, (int(bx), int(by)), br + 10, C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(bx), int(by)), br, C((24, 36, 70)), -1, cv2.LINE_AA)
    comp(f, scale_el(pancreas_el(t >= tw), 0.5), bx + 30, by + 60)
    comp(f, scale_el(stomach_el(), 0.48), bx - 40, by - 30, op=0.95)
    if t >= tw: sparkles(f, bx + 120, by + 40, t, tw, 10, 140); comp(f, burst_el("!", YEL_, INK, 50), bx + 190, by - 120, scale=pin(t, tw, 0.22))
    v = 0.5 + 0.2 * ramp(t, T("b2", "rises,") - 0.25, 0.6)
    sugar_gauge(f, 790, 870, 130, v, label="SUGAR")
    if t >= tp: label_at(f, "PANCREAS", 300, 1060, t, tp, bx + 20, by + 70)
    if t < tp: ui_word(f, "when blood sugar", "[RISES]", 470, t, st_("S6") + 0.1, col=INK, acc=RED_, size=200, out=tp - 0.05)
    else: ui_word(f, "your", "[PANCREAS] WAKES UP", 470, t, tp, col=INK, acc=(220, 120, 20), size=140)
    return finish(f, n)


# ---- S6b: an organ behind your stomach (scale cue: where it is in the body) ----
def shot_S6b(t, n):
    f = stage("pink", (255, 236, 200), 470, 1060, 380); u = lt(t, "S6b")
    tb = T("b2", "behind") - 0.15
    k = ramp(t, tb, 0.5)
    comp(f, scale_el(pancreas_el(True), 0.95), 520, 1150)
    comp(f, scale_el(stomach_el(), 0.95), 420 - 60 * k, 1000 - 140 * k, op=1 - 0.55 * k)
    label_at(f, "STOMACH", 240, 700, t, st_("S6b") + 0.3, 330, 840)
    if t >= tb: label_at(f, "PANCREAS", 330, 1400, t, tb + 0.2, 470, 1220)
    chub(f, 850, 1460, 0.42, la=(20, 10), ra=(20, 10), mouth=0, expr="happy", brow="up")
    cv2.circle(f, (int(850 + 8), int(1460 - 215 * 0.42 + 14)), 13, C(RED_), -1, cv2.LINE_AA); ring(f, 858, 1460 - 76, 26 + 6 * math.sin(t * 8), RED_, 4)
    comp(f, chip("it's in here", INK, WHITE, 22), 850, 1240, op=clamp((u - 0.5) / 0.3))
    uw(f, "an organ", "[BEHIND] YOUR STOMACH", t, st_("S6b") + 0.08, size=130)
    return finish(f, n)


def ring(f, x, y, r, col, th=8, op=1.0):
    ov = f.copy(); cv2.circle(ov, (int(x), int(y)), int(r), C(col), th, cv2.LINE_AA); f[:] = f * (1 - op) + ov * op


# ---- S7: it sends out insulin ----
def shot_S7(t, n):
    f = stage("yellow", (255, 255, 255), 380, 1100, 300); u = lt(t, "S7")
    rot_comp(f, scale_el(pancreas_el(True), 0.85), 330, 1160, 4 * math.sin(t * 5), 1.0, 1.0, 0.3)
    ti = T("b3", "insulin.") - 0.3
    for j in range(5):
        q = (t - ti - j * 0.18) / 0.9
        if q < 0: continue
        q = clamp(q); x = 470 + 360 * eo(q) - 30 * j; y = 1100 - 300 * math.sin(math.pi * q * 0.8) + 90 * j - 40
        rot_comp(f, scale_el(ikey_el(), 0.5), x, y, -30 + 50 * q + 15 * j, 1.0, 1.0, 0.2)
    if t >= ti + 0.5: label_at(f, "INSULIN", 640, 1430, t, ti + 0.5, 780, 1250)
    if t >= ti - 0.2: uw(f, "it sends out", "[INSULIN]", t, ti - 0.2, acc=(220, 40, 120), size=210)
    return finish(f, n)


# ---- S7b: think of insulin as a key ----
def shot_S7b(t, n):
    f = stage("purple", (255, 214, 100), 540, 1050, 400); u = lt(t, "S7b")
    tk = T("b3", "key.") - 0.2
    rays(f, 540, 1050, 760, (255, 230, 140), 0.4 * ramp(t, tk, 0.3), t)
    rot_comp(f, scale_el(ikey_el(), 1.55), 540, 1060 + 10 * math.sin(t * 3), -12 + 6 * math.sin(t * 2), pin(t, st_("S7b") + 0.05, 0.35), 1.0, 0.35)
    comp(f, chip("INSULIN", INK, WHITE, 34), 300, 1330, op=clamp((u - 0.3) / 0.3))
    if t >= tk: comp(f, ed_el("", "=", "", big_col=WHITE, big_size=90, shadow=0.4), 540, 1330, scale=pin(t, tk, 0.25)); comp(f, chip("A KEY", YEL_, INK, 34), 760, 1330, scale=pin(t, tk + 0.1, 0.25))
    uw(f, "think of insulin as a", "[KEY]", t, st_("S7b") + 0.08, size=230)
    return finish(f, n)


# ---- S8: it unlocks your cells, so the sugar moves in ----
CX8, CY8, CS8 = 650, 1080, 1.1


def shot_S8(t, n):
    f = stage("teal"); u = lt(t, "S8")
    tu = T("b4", "cells,") - 0.1; tm = T("b4", "moves") - 0.25
    open_k = ramp(t, tu + 0.3, 0.35)
    nin = int(clamp((t - tm) / 1.0) * 6) if t >= tm else 0
    comp(f, scale_el(cell_el(open_k, nin), CS8), CX8, CY8)
    door_x = CX8 - 260 * CS8 + 20
    k = ramp(t, st_("S8") + 0.05, tu - st_("S8") - 0.05)
    if open_k < 0.9:
        rot_comp(f, scale_el(ikey_el(), 0.45), 120 + (door_x - 70 - 120) * k, CY8 - 30, -90 * ramp(t, tu, 0.25), 1.0, 1.0, 0.2)
    if t >= tu: comp(f, burst_el("CLICK!", YEL_, INK, 40), door_x - 40, CY8 - 260, scale=pin(t, tu, 0.22), op=clamp((tu + 0.9 - t) / 0.2))
    if t >= tm:
        for j in range(6 - nin):
            q = clamp((t - tm) * 1.4 - j * 0.25)
            comp(f, scale_el(sugar_el("happy"), 0.4), 80 + j * 70 + (door_x - 80 - j * 70) * eo(q), CY8 + 110 + 20 * math.sin(t * 9 + j) - 60 * q)
    label_at(f, "CELL DOOR", 260, 760, t, st_("S8") + 0.4, door_x - 10, CY8 - 90)
    uw(f, "it", "[UNLOCKS] YOUR CELLS", t, st_("S8") + 0.1, size=150)
    return finish(f, n)


# ---- S8b: to be used... or stored ----
def shot_S8b(t, n):
    f = stage("emerald"); u = lt(t, "S8b")
    tu = T("b4", "used") - 0.15; ts = T("b4", "stored.") - 0.15
    def L(g):
        if t < tu: return
        w_ = walk(t, 1.4); chub(g, 300, 1400, 0.62, mouth=2, expr="happy", brow="up", **w_)
        bolt = np.array([[420, 760], [370, 900], [410, 900], [360, 1040], [470, 860], [430, 860], [470, 760]], np.int32)
        cv2.fillPoly(g, [bolt], C(YEL_), cv2.LINE_AA); cv2.polylines(g, [bolt], True, C(INK), 5, cv2.LINE_AA)
        speed_lines(g, t, 0.5, 1150, 1380, 6)
    def R(g):
        cv2.rectangle(g, (650, 1000), (910, 1400), C(INK), -1, cv2.LINE_AA); cv2.rectangle(g, (660, 1010), (900, 1390), C((200, 150, 90)), -1, cv2.LINE_AA)
        nn = int(clamp((t - ts) / 0.9) * 9)
        for j in range(nn): comp(g, scale_el(sugar_el(None), 0.32), 700 + (j % 3) * 80, 1350 - (j // 3) * 70)
        comp(g, chip("STORAGE", INK, WHITE, 26), 780, 960)
    split_contrast(f, t, tu, L, R, "USED NOW", "STORED", (255, 190, 30), (120, 90, 200), t_r=ts)
    ui_word(f, "to be", "[USED] OR [STORED]", 470, t, st_("S8b") + 0.05, col=WHITE, acc=YEL_, size=150, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S9: healthy body: blood sugar stays in a tight range ----
def shot_S9(t, n):
    f = stage("sky"); u = lt(t, "S9")
    tt = T("b5", "tight") - 0.15
    kick = math.exp(-max(0, u - 0.8) * 2.2) * (u > 0.8) * 0.14 + math.exp(-max(0, u - 2.2) * 2.2) * (u > 2.2) * 0.12
    v = 0.5 + 0.03 * math.sin(t * 4) + kick
    sugar_gauge(f, 540, 1240, 340, v, label="BLOOD SUGAR")
    for j, tc in enumerate((0.6, 2.0)):
        if tc - 0.3 < u < tc + 0.3:
            q = clamp((u - tc + 0.3) / 0.6); rot_comp(f, scale_el(candy_el(CANDY_COLS[j]), 0.45), 140 + 300 * q, 820 + 200 * q, 200 * q, 1.0, 1.0 - q * 0.6, 0.2)
        if tc + 0.3 < u < tc + 1.1:
            q = clamp((u - tc - 0.3) / 0.8); rot_comp(f, scale_el(ikey_el(), 0.32), 940 - 220 * q, 860 + 40 * q, 20, 1.0, 1.0 - q * 0.5, 0.2)
    if t >= tt: label_at(f, "TIGHT RANGE", 540, 760, t, tt, 540, 1240 - 300)
    uw(f, "blood sugar stays in a", "[TIGHT RANGE]", t, tt - 0.4, size=160) if t >= tt - 0.4 else uw(f, "in a", "[HEALTHY BODY]", t, st_("S9") + 0.1, size=160)
    return finish(f, n)


# ---- S9b: like a thermostat ----
def shot_S9b(t, n):
    f = stage("orange", (255, 220, 140), 640, 1040, 360); u = lt(t, "S9b")
    rot_comp(f, scale_el(thermostat_el("21"), 1.15), 640, 1040, 0, pin(t, st_("S9b") + 0.05, 0.3), 1.0, 0.35)
    chub(f, 230, 1470, 0.8, la=(20, 10), ra=(70, 40), mouth=talk(t), expr="happy", brow="up", look=(1, -0.5))
    comp(f, chip("keeps it steady", INK, WHITE, 30), 640, 1330, op=clamp((u - 0.5) / 0.3))
    uw(f, "like a", "[THERMOSTAT]", t, st_("S9b") + 0.08, size=200)
    return finish(f, n)


# ---- S10: re-hook / PART 2 — they ran blind tests ----
def shot_S10(t, n):
    f = stage("purple", (255, 214, 100), 540, 1000, 360); u = lt(t, "S10")
    tb = T("c1", "blind") - 0.15; tt = T("c1", "trust") - 0.1
    rot_comp(f, sign_el("SUGAR = HYPER?", YEL_, INK, 52, False), 640, 800 + 6 * math.sin(t * 3), 6, pin(t, st_("S10") + 0.05, 0.3), 1.0, 0.3)
    if t >= tt: comp(f, check_el(46, False), 860, 730, scale=pin(t, tt, 0.25))
    shake = 1 if tt <= t < tt + 0.6 else 0
    scientist(f, 330, 1470, 1.0, la=(20, 10), ra=(20, 10) if t < tb else (150, 170), mouth=talk(t), expr="sus" if t < tb else "wow",
              brow="sus" if t < tb else "up", look=(math.sin(t * 18) * shake, 0) if shake else (1, -0.5))
    if t >= tb:
        for j, x in enumerate((640, 860)):
            comp(f, scale_el(cup2_el("?", (255, 140, 60)), 0.62), x, 1300, scale=pin(t, tb + 0.1 * j, 0.25))
        slam(f, stamp_el("BLIND TEST", RED_, 56), 700, 1060, -6, t, tb + 0.15)
    chapter_card(f, t, st_("S10") + 0.1, 2, "THE BLIND TESTS", y=1430)
    uw(f, "they ran", "[BLIND TESTS]", t, tb - 0.2, size=180) if t >= tb - 0.2 else uw(f, "scientists didn't just", "[TRUST IT]", t, st_("S10") + 0.1, size=170)
    return finish(f, n)


# ---- S11: some kids got sugar, others a sweetener that tastes the same ----
def shot_S11(t, n):
    f = stage("cream"); u = lt(t, "S11")
    tsg = T("c2", "sugar.") - 0.2; tsw = T("c2", "sweetener") - 0.15; tsa = T("c2", "same.") - 0.15
    def L(g):
        chub(g, 260, 1460, 0.62, la=(20, 10), ra=(60, 30), mouth=talk(t, False), expr="happy", brow="up", look=(1, 0))
        comp(g, scale_el(cup2_el("A", SUGAR_C), 0.62), 420, 1200)
        q = clamp((t - tsg) / 0.4); comp(g, scale_el(sugar_el("happy"), 0.45), 420, 820 + 300 * q * q, op=1 - clamp((t - tsg - 0.45) / 0.15))
    def R(g):
        chub(g, 820, 1460, 0.62, la=(60, 30), ra=(20, 10), mouth=0, expr="happy", brow="up", look=(-1, 0))
        comp(g, scale_el(cup2_el("B", SUGAR_C), 0.62), 660, 1200)
        q = clamp((t - tsw) / 0.5); rot_comp(g, scale_el(packet_el(), 0.5), 700, 850 + 200 * eo(q), -40 * q, 1.0, 1.0 - 0.8 * clamp((t - tsw - 0.7) / 0.2), 0.2)
        for j in range(8):
            if q > 0.6 and t < tsw + 1.2: cv2.circle(g, (int(670 + 6 * math.sin(j)), int(950 + ((t - tsw) * 400 + j * 30) % 200)), 5, C((255, 255, 255)), -1, cv2.LINE_AA)
    split_contrast(f, t, st_("S11") + 0.05, L, R, "SUGAR", "SWEETENER", SUGAR_C, SWEET_C, t_r=tsw - 0.2)
    if t >= tsa:
        cv2.circle(f, (540, 1200), 62, C(INK), -1, cv2.LINE_AA); cv2.circle(f, (540, 1200), 54, C(WHITE), -1, cv2.LINE_AA)
        comp(f, ed_el("", "=", "", big_col=INK, big_size=90), 540, 1202, scale=pin(t, tsa, 0.25))
    ui_word(f, "tastes the", "[SAME]", 470, t, tsa - 0.1, col=INK, acc=RED_, size=220) if t >= tsa - 0.1 else ui_word(f, "", "[SUGAR] VS [SWEETENER]", 470, t, st_("S11") + 0.1, col=INK, acc=(230, 90, 20), size=120)
    return finish(f, n)


# ---- S12: nobody knew who got what. not even the scientists ----
def shot_S12(t, n):
    f = stage("yellow"); u = lt(t, "S12")
    tn = T("c3", "nobody") - 0.15; tsc = T("c3", "scientists.") - 0.15
    for j, x in enumerate((420, 660)): comp(f, scale_el(cup2_el("?", SUGAR_C), 0.5), x, 1370)
    chub(f, 200, 1440, 0.58, la=(20, 10), ra=(20, 10), mouth=0, expr="happy", brow="up")
    if t >= tn: blindfold(f, 200, 1440, 0.58)
    mom(f, 470, 1440, 0.66, la=(20, 10), ra=(20, 10), mouth=0, expr="n", brow="n")
    if t >= tn + 0.25: blindfold(f, 470, 1440, 0.66)
    flail = t >= tsc and t < tsc + 0.8
    scientist(f, 790, 1440, 0.72, la=(150, 170) if flail else (20, 10), ra=(150, 170) if flail else (70, 40), mouth="o" if flail else 0,
              expr="wow" if flail else "sus", brow="up", bob=-12 * abs(math.sin(t * 16)) if flail else 0)
    if t >= tsc: blindfold(f, 790, 1440, 0.72, bob=-12 * abs(math.sin(t * 16)) if flail else 0); comp(f, burst_el("?!", YEL_, INK, 44), 900, 900, scale=pin(t, tsc, 0.22))
    ui_word(f, "not even the", "[SCIENTISTS]", 470, t, T("c3", "Not") - 0.1, col=INK, acc=RED_, size=170) if t >= T("c3", "Not") - 0.1 else ui_word(f, "", "[NOBODY] KNEW", 470, t, tn, col=INK, acc=RED_, size=200)
    return finish(f, n)


# ---- S13: 1995: researchers pooled 23 tests (count-up pile) ----
def shot_S13(t, n):
    f = stage("cream"); u = lt(t, "S13")
    ty = T("c4", "nineteen") - 0.15; tp = T("c4", "pooled") - 0.25; te = T("c4", "tests.") + 0.1
    if t >= ty: rot_comp(f, scale_el(calendar_el("YEAR", "1995"), 0.6), 250, 860, -6, pin(t, ty, 0.3), 1.0, 0.3)
    nn = count_up(t, tp, 23, max(0.4, te - tp)) if t >= tp else 0
    for i in range(nn):
        rng = np.random.default_rng(i); x = 700 + rng.uniform(-110, 110); y = 1380 - i * 22
        rot_comp(f, scale_el(test_card_el(), 0.55), x, y, rng.uniform(-25, 25), 1.0, 1.0, 0.15 if i % 4 == 0 else 0.0)
    if nn and nn < 23:
        q = (t - tp) * 23 / max(0.4, te - tp) % 1.0; comp(f, scale_el(test_card_el(), 0.55), 1000 - 300 * q, 700 + 500 * q)
    chip_k = clamp((t - tp - 0.3) / 0.3)
    comp(f, chip("Source: Wolraich et al., JAMA 1995", INK, WHITE, 22), 540, 1462, op=chip_k)
    ui_word(f, "researchers pooled", f"[{nn}] TESTS", 470, t, tp, col=INK, acc=(40, 120, 230), size=200) if t >= tp else ui_word(f, "in", "[1995]", 470, t, ty, col=INK, acc=RED_, size=220)
    return finish(f, n)


# ---- S14: the result: no change in behaviour or thinking ----
def bars_pair(f, x, base, k, lab, t):
    for j, (dx, col, nm) in enumerate(((-75, SUGAR_C, "SUGAR"), (75, SWEET_C, "NO SUGAR"))):
        hh = int(320 * k * (1 + 0.01 * math.sin(t * 5 + j)))
        if hh > 2:
            f[base - hh:base, int(x + dx - 60):int(x + dx + 60)] = np.array(C(col), np.float32)
            cv2.rectangle(f, (int(x + dx - 60), base - hh), (int(x + dx + 60), base), C(INK), 6, cv2.LINE_AA)
        comp(f, chip(nm, INK, WHITE, 20), x + dx, base + 30)
    comp(f, chip(lab, YEL_, INK, 30), x, base + 90)


def shot_S14(t, n):
    f = stage("emerald"); u = lt(t, "S14")
    tb = T("c5", "behaved...") - 0.3; tth = T("c5", "thought.") - 0.3; td = T("c5", "didn't") - 0.1
    cv2.rectangle(f, (120, 760), (960, 1420), C((250, 248, 240)), -1, cv2.LINE_AA); cv2.rectangle(f, (120, 760), (960, 1420), C(INK), 6, cv2.LINE_AA)
    bars_pair(f, 330, 1290, ramp(t, st_("S14") + 0.2, 0.6), "BEHAVIOUR", t)
    t2 = T("c5", "or") - 0.2
    if t >= t2: bars_pair(f, 750, 1290, ramp(t, t2, 0.6), "THINKING", t)
    if t >= td: slam(f, stamp_el("NO CHANGE", RED_, 60), 540, 860, -6, t, td)
    uw(f, "the", "[RESULT?]", t, st_("S14") + 0.05, size=200, out=td - 0.05)
    if t >= td: uw(f, "sugar", "[DIDN'T CHANGE IT]", t, td, size=150)
    return finish(f, n)


# ---- S15: PART 3 — so why do parents swear they see it? ----
def shot_S15(t, n):
    f = stage("red", (255, 200, 120), 400, 1000, 360); u = lt(t, "S15")
    tw = T("d1", "wild.") - 0.15
    mom(f, 360, 1470, 1.0, la=(35, -75), ra=(110, 60), mouth=talk(t), expr="sus", brow="sus", look=(1, 0))
    comp(f, bubble_el("IT'S THE SUGAR!", 40), 560, 760, scale=pin(t, st_("S15") + 0.3, 0.3))
    chub(f, 820, 1460, 0.58, la=(20, 10), ra=(60, 30), mouth=0, expr="happy", brow="n", look=(-1, 0), hold=scale_el(candy_el(CANDY_COLS[2]), 0.3), hold_front=True)
    if t >= tw: comp(f, burst_el("WILD!", YEL_, INK, 56), 820, 1000, scale=pin(t, tw, 0.22))
    chapter_card(f, t, T("d1", "This") - 0.1, 3, "THE PARENT TEST", y=1430, dur=1.4)
    uw(f, "why do parents", "[SWEAR] THEY SEE IT?", t, st_("S15") + 0.1, size=120)
    return finish(f, n)


# ---- S16: 35 boys got a sweet drink ----
def shot_S16(t, n):
    f = stage("sky"); u = lt(t, "S16")
    t0 = st_("S16") + 0.05; nn = count_up(t, t0, 35, 1.0)
    hd = scale_el(chub_head_el(0, False, "n", 0, 0, "happy"), 0.3); cup = scale_el(cup2_el("", SUGAR_C), 0.16)
    for i in range(nn):
        r_, c_ = divmod(i, 7)
        x = 210 + c_ * 110; y = 760 + r_ * 125 + 4 * math.sin(t * 6 + i)
        comp(f, hd, x, y); comp(f, cup, x + 32, y + 40)
    uw(f, "", f"[{nn}] BOYS", t, t0, size=220)
    comp(f, chip("ages 5 to 7 · Hoover & Milich, 1994", INK, WHITE, 24), 540, 1430, op=clamp((u - 0.8) / 0.3))
    return finish(f, n)


# ---- S16b: every single one was sugar-free ----
def shot_S16b(t, n):
    f = stage("lime", (255, 255, 230), 540, 1060, 380); u = lt(t, "S16b")
    tf_ = T("d2", "sugar-free.") - 0.15
    rot_comp(f, scale_el(cup2_el("", SUGAR_C), 1.25), 540, 1080, 3 * math.sin(t * 2), pin(t, st_("S16b") + 0.03, 0.3), 1.0, 0.35)
    comp(f, scale_el(sugar_el("sly"), 0.55), 220, 1180); comp(f, check_el(44, False), 220, 1180, scale=pin(t, tf_, 0.25))
    if t >= tf_: slam(f, stamp_el("SUGAR-FREE", (20, 140, 80), 64), 560, 1360, -6, t, tf_)
    uw(f, "every single one", "[SUGAR-FREE]", t, st_("S16b") + 0.08, size=170, acc=(255, 255, 255))
    return finish(f, n)


# ---- S17: half the moms were told... a big dose of sugar (split) ----
def mom_pair(g, x, t, lvl=None, told=None, mood="n"):
    mom(g, x - 80, 1450, 0.62, la=(20, 10), ra=(70, 40), mouth=0, expr=mood, brow="sus" if mood == "sus" else "n", look=(1, 0))
    chub(g, x + 110, 1450, 0.44, la=(20, 10), ra=(20, 10), mouth=0, expr="happy", brow="n", look=(-1, 0), hold=scale_el(cup2_el("", SUGAR_C), 0.22), hold_front=True)


def shot_S17(t, n):
    f = stage("teal"); u = lt(t, "S17")
    tt = T("d3", "told...") - 0.15; ts = T("d3", "big") - 0.15
    def L(g):
        mom_pair(g, 330, t)
        if t >= tt: comp(g, bubble_el("no sugar", 34), 300, 860, scale=pin(t, tt, 0.25))
    def R(g):
        mom_pair(g, 750, t, mood="sus" if t >= ts else "n")
        if t >= tt: comp(g, bubble_el("SUGAR!", 40), 720, 860, scale=pin(t, tt + 0.15, 0.25))
        if t >= ts: comp(g, scale_el(sugar_el("sly"), 0.42), 860, 1010, scale=pin(t, ts, 0.25))
    split_contrast(f, t, st_("S17") + 0.05, L, R, "TOLD: NO SUGAR", "TOLD: SUGAR!", (60, 160, 220), SUGAR_C)
    uw(f, "half the moms were", "[TOLD: SUGAR]", t, tt - 0.1, size=150)
    return finish(f, n)


# ---- S18: those moms rated their boys as more hyper ----
def shot_S18(t, n):
    f = stage("teal"); u = lt(t, "S18")
    th = T("d4", "hyper.") - 0.3
    def L(g):
        chub(g, 330, 1460, 0.42, la=(20, 10), ra=(20, 10), mouth=0, expr="happy", brow="n")
        rating_board(g, 330, 990, 0.82, 0.4 * ramp(t, st_("S18") + 0.2, 0.6))
    def R(g):
        chub(g, 750, 1460, 0.42, la=(20, 10), ra=(20, 10), mouth=0, expr="happy", brow="n")
        rating_board(g, 750, 990, 0.82, 0.4 * ramp(t, st_("S18") + 0.2, 0.6) + 0.6 * ramp(t, th, 0.5))
        if t >= th + 0.3: slam(g, stamp_el("MORE HYPER!", RED_, 34), 750, 1222, -6, t, th + 0.3)
    split_contrast(f, t, st_("S18"), L, R, "TOLD: NO SUGAR", "TOLD: SUGAR!", (60, 160, 220), SUGAR_C, wipe=0.01)
    if u > 0.4: comp(f, chip("same calm kids", INK, WHITE, 24), 540, 1462, op=clamp((u - 0.4) / 0.3))
    uw(f, "they rated their boys", "[MORE HYPER]", t, st_("S18") + 0.1, size=150)
    return finish(f, n)


# ---- S18b: they stayed closer, and controlled them more ----
def shot_S18b(t, n):
    f = stage("pink", (255, 236, 200), 540, 1000, 360); u = lt(t, "S18b")
    tcl = T("d4", "closer,") - 0.2; tco = T("d4", "controlled") - 0.15
    k = ramp(t, st_("S18b") + 0.1, tcl - st_("S18b"))
    mx = 260 + 230 * k
    mom(f, mx, 1470, 0.95, la=(20, 10), ra=(95, 30) if t >= tco else (30, 10), mouth=talk(t) if t >= tco else 0, expr="sus", brow="sus", look=(1, 0.3), lean=10 * k)
    chub(f, 800, 1470, 0.6, la=(20, 10), ra=(20, 10), mouth=0, expr="n", brow="sad", look=(-1, -0.5))
    label_at(f, "STAYED CLOSER", 600, 760, t, tcl)
    if t >= tco: comp(f, bubble_el("SIT STILL!", 40), 760, 930, scale=pin(t, tco, 0.25))
    uw(f, "they stayed", "[CLOSER]", t, st_("S18b") + 0.08, size=210, out=tco - 0.05)
    if t >= tco: uw(f, "and", "[CONTROLLED] THEM MORE", t, tco, size=130)
    return finish(f, n)


# ---- S19: same drink. different belief. ----
def shot_S19(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 380); u = lt(t, "S19")
    td = T("d5", "Different") - 0.15
    for j, x in enumerate((330, 750)): rot_comp(f, scale_el(cup2_el("", SUGAR_C), 0.9), x, 1080, 0, pin(t, st_("S19") + 0.05 + 0.1 * j, 0.25), 1.0, 0.3)
    cv2.circle(f, (540, 1080), 62, C(INK), -1, cv2.LINE_AA); cv2.circle(f, (540, 1080), 54, C(WHITE), -1, cv2.LINE_AA)
    comp(f, ed_el("", "=", "", big_col=INK, big_size=90), 540, 1082)
    if t >= td:
        comp(f, bubble_el("no sugar", 34), 300, 790, scale=pin(t, td, 0.25)); comp(f, bubble_el("SUGAR!", 40), 760, 790, scale=pin(t, td + 0.12, 0.25))
        comp(f, ed_el("", "≠", "", big_col=RED_, big_size=110), 540, 800, scale=pin(t, td + 0.2, 0.25))
    ui_word(f, "same", "[DRINK]", 470, t, st_("S19") + 0.05, col=INK, acc=(20, 140, 80), size=210, out=td - 0.05)
    if t >= td: ui_word(f, "different", "[BELIEF]", 470, t, td, col=INK, acc=RED_, size=210)
    return finish(f, n)


# ---- S19b: the rush was in the grown-ups' heads (what moms saw vs what was really there) ----
def shot_S19b(t, n):
    f = stage("purple"); u = lt(t, "S19b")
    th = T("d5", "heads!") - 0.2
    def L(g):
        cv2.ellipse(g, (340, 1000), (190, 170), 0, 0, 360, C(WHITE), -1, cv2.LINE_AA)
        for (dx, dy, r_) in ((-130, 160, 40), (-170, 235, 24)): cv2.circle(g, (340 + dx, 1000 + dy), r_, C(WHITE), -1, cv2.LINE_AA)
        chub(g, 340 + 12 * math.sin(t * 40), 1120, 0.42, la=(160, 175), ra=(160, 175), mouth=3, expr="wow", brow="up", shadow=False)
        hyper_lines(g, 340, 1120 - 180, 90, t, RED_, 8)
        mom_head(g, 200, 1350, 0.75, t)
    def R(g):
        chub(g, 750, 1420, 0.62, la=(20, 10), ra=(60, 30), mouth=0, expr="happy", brow="n", hold=scale_el(cup2_el("", SUGAR_C), 0.26), hold_front=True)
        comp(g, chip("calm kid, no sugar", INK, WHITE, 26), 750, 840)
    split_contrast(f, t, st_("S19b") + 0.05, L, R, "WHAT MOMS SAW", "WHAT WAS REALLY THERE", (236, 72, 140), (20, 160, 110), t_r=st_("S19b") + 0.5)
    uw(f, "the rush was in the", "[GROWN-UPS' HEADS]", t, st_("S19b") + 0.1, size=130)
    if t >= th: comp(f, burst_el("!", YEL_, INK, 50), 220, 1170, scale=pin(t, th, 0.22))
    return finish(f, n)


def mom_head(f, x, y, s, t):
    cv2.ellipse(f, (int(x), int(y + 40 * s)), (int(112 * s), int(122 * s)), 0, 0, 360, C(INK), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y + 40 * s)), (int(104 * s), int(114 * s)), 0, 0, 360, C(MOM_HAIR), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y - 94 * s)), int(42 * s), C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y - 94 * s)), int(35 * s), C(MOM_HAIR), -1, cv2.LINE_AA)
    comp(f, scale_el(chub_head_el(0, False, "sus", 0.6, -0.6, "sus"), s), x, y + 10 * s)


# ---- S20: so what really makes kids wild? look where the candy shows up (pull-back reveal) ----
def shot_S20(t, n):
    f = stage("night"); u = lt(t, "S20")
    tw = T("e1", "where") - 0.2
    moon(f, 860, 760, 80)
    g = f.copy()
    for j, (x, y, c) in enumerate(((200, 900, 0), (880, 1000, 1), (320, 800, 2))): rot_comp(g, scale_el(balloon_el(CANDY_COLS[c]), 0.7), x, y + 14 * math.sin(t * 2 + j), 6 * math.sin(t + j), 1.0, 1.0, 0.2)
    comp(g, scale_el(ghost_el(), 0.55), 860, 1300 + 10 * math.sin(t * 3))
    comp(g, scale_el(party_hat_el(CANDY_COLS[4]), 0.8), 230, 1360)
    comp(g, scale_el(bucket_el(), 0.75), 540, 1150)
    z = 2.3 - 1.3 * ramp(t, tw - 0.4, 1.0)
    f[:] = cam(g, z, 540, 1150)
    if t >= tw + 0.5:
        for j, (x, y) in enumerate(((200, 880), (880, 980), (860, 1300), (230, 1360))):
            if t >= tw + 0.5 + 0.15 * j: ring(f, x, y, 70 + 10 * math.sin(t * 6 + j), YEL_, 8, 0.9)
    uw(f, "what really makes kids", "[WILD?]", t, st_("S20") + 0.08, size=200, out=tw - 0.05)
    if t >= tw: uw(f, "look at", "[WHERE] IT SHOWS UP", t, tw, size=140)
    return finish(f, n)


# ---- S21: parties... Halloween ----
def shot_S21(t, n):
    th = T("e2", "Halloween.") - 0.12; hal = t >= th
    f = stage("night" if hal else "pink", None if hal else (255, 236, 200), 540, 1000, 380); u = lt(t, "S21")
    if hal:
        moon(f, 820, 780, 100); comp(f, scale_el(bucket_el(), 0.6), 250, 1360)
        chub(f, 560, 1460 - 120 * abs(math.sin(t * 7)), 0.95, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up", shadow=False)
        hx, hy = head_pos(560, 1460 - 120 * abs(math.sin(t * 7)), 0.95); comp(f, scale_el(witch_hat_el(), 0.85), hx, hy - 120)
    else:
        confetti(f, t, st_("S21"), 50)
        for j, (x, c) in enumerate(((180, 0), (900, 1))): rot_comp(f, scale_el(balloon_el(CANDY_COLS[c]), 0.75), x, 980 + 12 * math.sin(t * 2 + j), 0, 1.0, 1.0, 0.2)
        y = 1460 - 120 * abs(math.sin(t * 7))
        chub(f, 540, y, 0.95, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up", shadow=False)
        hx, hy = head_pos(540, y, 0.95); comp(f, scale_el(party_hat_el(CANDY_COLS[3]), 0.75), hx + 10, hy - 140)
    uw(f, "", "[HALLOWEEN]" if hal else "[PARTIES]", t, th if hal else st_("S21") + 0.03, size=210)
    return finish(f, n)


# ---- S21c: friends, costumes ----
def shot_S21c(t, n):
    f = stage("purple", (255, 214, 100), 540, 1050, 380); u = lt(t, "S21c")
    for j, x in enumerate((240, 540, 840)):
        y = 1460 - 90 * abs(math.sin(t * 7 + j)); s = 0.66
        chub(f, x, y, s, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up", shadow=False, shirt=[(16, 190, 130), (255, 140, 40), (60, 140, 240)][j])
        hx, hy = head_pos(x, y, s)
        if j == 0: comp(f, scale_el(witch_hat_el(), 0.6), hx, hy - 90)
        elif j == 1: comp(f, scale_el(ghost_el(), 0.62), hx, hy + 30)
        else: comp(f, scale_el(party_hat_el(CANDY_COLS[0]), 0.55), hx, hy - 100)
    ui_word(f, "", "[FRIENDS] + [COSTUMES]", 470, t, st_("S21c") + 0.03, col=WHITE, acc=YEL_, size=130, shadow=0.5)
    return finish(f, n)


# ---- S21d: staying up late. that's the real rush! ----
def shot_S21d(t, n):
    f = stage("night"); u = lt(t, "S21d")
    tr = T("e2", "real") - 0.15
    moon(f, 200, 760, 80)
    rot_comp(f, scale_el(clock_el(11, 30), 0.85), 820, 860, 4 * math.sin(t * 8), 1.0, 1.0, 0.3)
    if t >= tr: rays(f, 540, 1100, 800, (255, 200, 80), 0.5, t); confetti(f, t, tr, 40)
    chub(f, 480, 1460 - 140 * abs(math.sin(t * 8)), 0.9, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up", shadow=False)
    if t >= tr: slam(f, stamp_el("THE REAL RUSH", YEL_, 64), 540, 1250, -6, t, tr)
    uw(f, "staying up", "[LATE]", t, st_("S21d") + 0.05, size=220)
    return finish(f, n)


# ---- S22: one honest catch: a small effect in some kids can't be ruled out ----
def shot_S22(t, n):
    f = stage("cream"); u = lt(t, "S22")
    ts = T("f1", "small") - 0.15
    hd = scale_el(chub_head_el(0, False, "n", 0, 0, "happy"), 0.36)
    for i in range(20):
        r_, c_ = divmod(i, 5); x = 220 + c_ * 160; y = 780 + r_ * 150
        comp(f, hd, x, y + 3 * math.sin(t * 5 + i))
        if i in (6, 13) and t >= ts: comp(f, ed_el("", "?", "", big_col=RED_, big_size=60), x + 50, y - 50, scale=pin(t, ts + 0.1 * (i == 13), 0.25))
    mx = 540 + 260 * math.sin(u * 1.4); my = 1000 + 120 * math.cos(u * 1.1)
    comp(f, scale_el(magnifier_el(), 0.7), mx + 40, my + 70)
    comp(f, chip("can't rule out a small effect in some kids", INK, WHITE, 26), 540, 1430, op=clamp((t - ts) / 0.3))
    ui_word(f, "one honest", "[CATCH]", 470, t, st_("S22") + 0.1, col=INK, acc=RED_, size=220)
    return finish(f, n)


# ---- S23: sugar is still rough on your teeth ----
def shot_S23(t, n):
    f = stage("sky"); u = lt(t, "S23")
    tt = T("f2", "teeth.") - 0.2
    tooth(f, 540, 1120, 1.25, t, "sad", 0.4 + 0.6 * ramp(t, st_("S23") + 0.3, 1.6))
    for j in range(5):
        a = t * 1.2 + j * 1.25; comp(f, scale_el(sugar_el("sly"), 0.3), 540 + 330 * math.cos(a), 1080 + 250 * math.sin(a))
    if t >= tt: comp(f, burst_el("OUCH", YEL_, INK, 44), 820, 820, scale=pin(t, tt, 0.22))
    uw(f, "still rough on your", "[TEETH]", t, st_("S23") + 0.08, size=220)
    return finish(f, n)


# ---- S24: visual recap (1 -> 2 -> 3) ----
def shot_S24(t, n):
    f = stage("cream"); u = lt(t, "S24")
    t1 = T("g1", "insulin") - 0.15; t2 = T("g1", "blind") - 0.15; t3 = T("g1", "party") - 0.15
    items = [(scale_el(ikey_el(), 0.62), "STEADY SUGAR"), (scale_el(cup2_el("?", SUGAR_C), 0.8), "NO RUSH"), (scale_el(party_hat_el(CANDY_COLS[0]), 1.05), "THE PARTY")]
    recap_steps(f, items, 960, t, [t1, t2, t3], 300)
    myth_tag(f, 540, 1330, t, T("g1", "rest.") - 0.4, T("g1", "rest.") - 0.1, 50, "SUGAR RUSH")
    ui_word(f, "so", "[REMEMBER]", 470, t, st_("S24") + 0.05, col=INK, acc=RED_, size=200)
    return finish(f, n)


# ---- S25: send it + FreshNestHub sting ----
def shot_S25(t, n):
    f = stage("yellow", (255, 255, 255), 540, 880, 420); u = lt(t, "S25")
    vend = LINES["g2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("g2", "Send") + 0.3
        comp(f, scale_el(phone2_el("trick or treat tonight?", "brb sugar rush incoming", pr), 0.82), 640, 950, scale=pin(t, st_("S25")))
        if pr and t < T("g2", "Send") + 0.75:
            rr = (t - T("g2", "Send") - 0.3) / 0.45
            cv2.circle(f, (640, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, 250, 1480, 0.8, la=(20, 10), ra=(148, -130), mouth=talk(t), expr="smirk", brow="up", look=(1, 0),
             hold=scale_el(bucket_el(), 0.32), hold_off=(-20, 30), hold_front=True)
        ui_word(f, "send to the friend who blames", "[CANDY]", 420, t, T("g2", "friend") - 0.1, col=INK, acc=RED_, size=200, tail="for everything")
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INK, lead_size=42), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1480, 0.7, la=(20, 10), ra=(148, -130), mouth=2, expr="happy", brow="up", hold=scale_el(lollipop_el(CANDY_COLS[0]), 0.4), hold_off=(-20, -30), hold_front=True)
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TFZ, 0.4, 20), (st_("S1") + 0.02, 0.3, 12), (T("i2", "tested") - 0.1, 0.25, 10), (T("i3", "weirder.") - 0.2, 0.3, 12),
           (T("a1", "myth.") - 0.15, 0.3, 14), (st_("S3b") + 0.02, 0.5, 24), (st_("S4") + 0.15, 0.4, 20),
           (T("b2", "wakes") - 0.1, 0.3, 12), (T("b3", "key.") - 0.2, 0.3, 12), (T("b4", "unlocks") - 0.05, 0.3, 14),
           (T("c1", "blind") - 0.0, 0.35, 16), (T("c3", "scientists.") - 0.15, 0.3, 12), (T("c5", "didn't") - 0.1, 0.4, 18),
           (T("d1", "wild.") - 0.15, 0.3, 14), (T("d2", "sugar-free.") - 0.15, 0.35, 16), (T("d4", "hyper.") - 0.3, 0.3, 12),
           (T("d5", "heads!") - 0.2, 0.35, 16), (st_("S21") + 0.02, 0.3, 12), (T("e2", "Halloween.") - 0.12, 0.3, 12),
           (T("e2", "real") - 0.15, 0.45, 20), (T("f2", "teeth.") - 0.2, 0.3, 12), (T("g1", "rest.") - 0.1, 0.35, 16)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0
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
