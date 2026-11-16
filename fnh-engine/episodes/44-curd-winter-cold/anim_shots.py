# ================= shots: FreshNestHub 44 — "Does eating curd in winter give you a cold?" (Chubby INK; 35-50 s rule; ONE takeaway) =================
# COLOUR SCRIPT: ICE BLUE (ACC) = winter, the cold, the question, frost. The virus = olive green (the only other strong colour, the culprit).
# Story = the WINTER LUNCH TABLE (the aunty stops the spoon), THE LINEUP ROOM (new place: curd is suspect #1, the silhouette at #2), the TV room
# (a sneeze on a packed sofa), the morning worktop (fridge-cold curd sits out), the bathroom sink (hands); every explanation = the white BOARD.
# METAPHOR: a police lineup: curd gets blamed every winter, Detective Chubby finds the real culprit (the cold virus) with a light.
# Visual upgrade (ep 44): DETECTIVE CHUBBY (fedora + magnifier + a hat tip), suspects with legs + placards, kin_word 'shiver' (COLD words tremble with
# snow caps + icicles). Craft skill (ep 44): THE SILHOUETTE REVEAL (anim_fx.silhouette_reveal): the culprit is a dark shape with a rim light for ~1 s,
# then the lamp clicks on exactly on 'viruses'.
END = round(LINES["c2"]["end"] + 1.33, 3)            # 35-50 s rule: 0.1 s air + 0.6 s logo + 0.63 s loop tail
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "really") - 0.12, "punch"),
    ("S1", T("i2", "Every") - 0.12, "whip"), ("S1b", T("i2", "But") - 0.1, "cut"),
    ("S2", T("a1", "Colds") - 0.12, "cut"), ("S2b", T("a1", "mostly") - 0.1, "erase"),
    ("S3", T("a2", "You") - 0.1, "erase"), ("S3b", T("a2", "hand") - 0.12, "cut"),
    ("S4", T("a3", "And") - 0.1, "erase"),
    ("S5", T("b1", "So") - 0.12, "erase"), ("S5b", T("b1", "friendly") - 0.12, "erase"),
    ("S6", T("b2", "If") - 0.1, "erase"),
    ("S7", T("c1", "So") - 0.12, "whip"),
    ("S8", T("c2", "Send") - 0.1, "punch"),
    ("S9", LINES["c2"]["end"] + 0.1, "punch"), ("S10", LINES["c2"]["end"] + 0.7, "cut"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
MORPH = {}
_write_on0 = write_on


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
    """phone-size hand lettering (ep 27: the kit default reads too small)."""
    _write_on0(f, text, x, y, t, t0, int(size * 1.3), col, cps, op)


def st_(sid): return SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, PAPER, 22), 540, y, op=clamp((t - t0) / 0.2))


def kw(f, text, x, y, t, t0, mode="pop", size=130, col=None, **k):
    kin_word(f, text, x, y, t, t0, mode, size, col or ACC_S, stroke=2, stroke_col=INKC, **k)


def el_at(f, el, x, y, s=1.0, t=None, t0=None, rot=0.0, op=1.0):
    k = 1.0 if t0 is None else (snap(t, t0, 4) if t >= t0 else 0.0)
    if k > 0.01: rot_comp(f, scale_el(el, s), x, y, rot, k, op, 0.0)


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None):
    s = s * 1.7
    chub_head_only(f, x, y, s, t, mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow or ("sus" if expr == "sus" else "up"), look=look, turn=clamp(look[0]) * 0.5)


def nolean(d): return {k: v for k, v in d.items() if k != "lean"}


def hook_band(f, y0=228, y1=700, a=0.66):
    """a soft paper band behind the hook words (feathered edges)."""
    m = np.zeros((H, 1), np.float32); m[y0:y1] = a
    m = cv2.GaussianBlur(np.repeat(m, 4, 1), (1, 61), 0)[:, :1, None]
    f[:] = f * (1 - m) + np.array(C(PAPER), np.float32) * m


def hook_words(f, t, t0=-1.0, op=1.0):
    """the hook question as moving words (on screen at frame 0): COLD? shivers with snow caps + icicles."""
    kw(f, "DO YOU KNOW IF", 540, 300, t, t0, "pop", 70, col=INKC, op=op)
    kw(f, "CURD IN WINTER", 540, 430, t, t0, "pop", 116, col=INKC, op=op)
    kw(f, "= A COLD?", 540, 590, t, t0, "shiver", 150, col=ACC_S, op=op)


# ---- the WINTER LUNCH TABLE: snow outside the window, the window light turns cool ----
def set_winter(t, blur=4):
    f = set_lunch(t, blur)
    win = (slice(330, 970), slice(590, 970))
    f[win] = f[win] * 0.62 + np.array(C((214, 230, 246)), np.float32) * 0.38
    g = f.copy(); snow(g, t, 1.0, 40, 9, 330, 970); f[win] = g[win]
    return f


LX, LY, LS = 390, 1690, 1.62           # Chubby at the table (table top 1330)
AX, AY, AS = 860, 1700, 1.55           # the aunty (the curd police) at the right
AUNTY = (214, 96, 128)


def aunty(f, t, stop=1.0, expr="angry", look=(-1, 0), talking=False, pose=None):
    p = dict(pose or dict(la=(30 + 105 * stop, 20 + 140 * stop), ra=(24, 12), lean=-4 * stop))
    ln = p.pop("lean", 0.0)
    chub(f, AX, AY, AS, t=t, shirt=AUNTY, mouth=talk(t) if talking else (2 if stop > 0.5 else 0), expr=expr, brow="sus" if expr == "angry" else "up",
         look=look, turn=-0.5, lean=ln, **p)
    dress(f, AX, AY, AS, "aunty", ln)


def table_hook(f, t, frozen=True):
    """frame 0 composition: the spoon of curd is ALREADY at Chubby's mouth; the aunty's palm is up: STOP."""
    shake = 3 * math.sin(t * 31) if frozen else 0
    chub(f, LX, LY, LS, t=t, la=(24, 12), ra=(150, -128), mouth="o", expr="wow", brow="up", look=(0.9, 0), turn=0.45, lean=-3 + shake * 0.3,
         hand_r="grip", hold=scale_el(spoon_el(), 0.45), hold_off=(-10, -30), hold_front=True)
    aunty(f, t)
    cloth_front(f, 1330)
    el_at(f, curd_el("happy", (-0.5, 0)), 620, 1280, 1.0)


# ---- S0: HOOK at frame 0: winter lunch, the spoon of curd is at Chubby's lips, the aunty's palm says STOP; COLD? shivers ----
def shot_S0(t, n):
    f = set_winter(t)
    table_hook(f, t)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="cool")


# ---- S0b: '...really give you a cold?' close-up: Chubby's eyes slide to the aunty (double take), the curd on the spoon right under his nose ----
def shot_S0b(t, n):
    f = set_winter(t, 8); f = dof(f, 3); t0 = st_("S0b")
    lk, ln, ex, br = double_take(t, t0 + 0.15)
    chub_head_only(f, 470, 1130, 2.5, t, mouth="o", expr=ex or "wow", brow=br or "up", look=(-lk[0], lk[1]), turn=0.4)
    el_at(f, spoon_el(), 760, 1360, 1.0, rot=-30)
    cv2.ellipse(f, (700, 1330), (54, 30), -30, 0, 360, C(CURD), -1, cv2.LINE_AA); cv2.ellipse(f, (700, 1330), (54, 30), -30, 0, 360, C(INKC), 4, cv2.LINE_AA)
    grip_hand(f, 960, 1180, 1.8, kind="open")                                                   # the aunty's palm comes in from the right
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="cool")


# ---- S1: 'Every winter, curd gets the blame.' THE LINEUP: curd is suspect #1, sweating; a mugshot FLASH on 'blame' ----
def shot_S1(t, n):
    f = set_lineup(t); t0 = st_("S1"); tb = T("i2", "blame") - 0.12
    lamp_pool(f, 330, 980, 230, 0.35)
    suspect(f, curd_el("ouch" if t > tb else "sad", (0.4, -0.3)), 330, 1.75, t, num=1, sweat=1.0 if t > tb else 0.4)
    if tb < t < tb + 0.12: f[:] = f + 0.7 * (1 - (t - tb) / 0.12)
    kw(f, "EVERY WINTER", 540, 400, t, t0 + 0.05, "shiver", 96, col=ACC_S)
    if t > tb: kw(f, "BLAMED", 540, 540, t, tb, "shake", 140, col=(176, 40, 44), amp=0.5)
    return finish(f, n, look="cool")


# ---- S1b: '...But it's the wrong suspect.' Detective Chubby with the magnifier on curd; WRONG SUSPECT stamp on 'wrong' ----
def detective(f, t, x, y, s, look=(-1, 0), mouth=None, expr="sus", tip=0.0, mag=True, lean=0.0, ra=(120, 150)):
    chub(f, x, y, s, t=t, la=(24, 12), ra=ra, mouth=talk(t) if mouth is None else mouth, expr=expr, brow="sus" if expr == "sus" else "up",
         look=look, turn=-0.5 if look[0] < 0 else 0.5, hand_r="grip", shirt=(212, 190, 150), lean=lean,
         hold=scale_el(magnifier_ink_el(), 0.55) if mag else None, hold_off=(0, -40), hold_front=True)
    fedora(f, x, y, s, lean, tip)


def shot_S1b(t, n):
    f = set_lineup(t); t0 = st_("S1b"); tw = T("i2", "wrong") - 0.1
    lamp_pool(f, 740, 980, 230, 0.35)
    suspect(f, curd_el("sad", (-0.6, -0.2)), 740, 1.6, t, num=1, sweat=0.6)
    detective(f, t, 290, 1720, 1.4, look=(1, 0.1), lean=6 + 2 * math.sin(t * 2), ra=(80, 40))
    if t > tw: el_at(f, vstamp_el("WRONG SUSPECT", (176, 40, 44), 64), 540, 470, 1.0, t, tw, rot=-8)
    return finish(f, n, look="cool")


# ---- S2: 'Colds are caused by viruses,' lights DOWN: a silhouette stands at #2 (rim light only) ... the lamp clicks on at 'viruses' = the VIRUS ----
VX = 750


def shot_S2(t, n):
    t0 = st_("S2"); tv = T("a1", "viruses") - 0.15
    k = clamp((t - tv) / 0.12)
    f = set_lineup(t, dim=0.75 * (1 - k))
    if k > 0:
        lamp_pool(f, VX, 960, 260, 0.6 * k)
        if t - tv < 0.14: f[:] = f + 0.5 * (1 - (t - tv) / 0.14)
    suspect(f, curd_el("sad", (1, 0)), 300, 1.6, t, num=1, op=0.55 + 0.45 * k)
    hip = LINE_FLOOR + 10 - 70 * 1.6
    if k > 0.5: legs(f, VX, hip, 1.6)
    silhouette_reveal(f, virus_el("sly", (-0.6, 0), int(t * 8) % 4), VX, hip - 122 * 1.6 + 3 * math.sin(t * 2), k, 1.6, rim=(255, 232, 180), rim_w=7)
    if k > 0.5: el_at(f, card_el(2), VX, hip - 40, 0.95)
    if t < tv: kw(f, "?", VX, 700, t, t0 + 0.2, "breathe", 260, col=(236, 240, 246))
    else: kw(f, "VIRUS", 540, 420, t, tv, "shake", 150, col=VIR_S, amp=0.5)
    return finish(f, n, look="cool")


# ---- S2b: '...mostly one called rhinovirus, not by cold food.' BOARD: the virus drawn big + label; then curd + a snowflake get a red X ----
def snowflake_on(f, x, y, r, k, col=ACC_S):
    for j in range(3):
        a = j * math.pi / 3
        draw_on(f, [(x - r * math.cos(a), y - r * math.sin(a)), (x + r * math.cos(a), y + r * math.sin(a))], clamp(k * 3 - j), col, 7, seed=60 + j, tip=False)


def shot_S2b(t, n):
    f = board_bg(); t0 = st_("S2b"); tr = T("a1", "rhinovirus") - 0.12; tn = T("a1", "not") - 0.1; tf = T("a1", "food") - 0.1
    up = 1 - 0.35 * ramp(t, tn, 0.4)
    vy = 640 * up + 120 * (1 - up)
    draw_ell_on(f, 540, vy, 230 * up, 230 * up, ramp(t, t0, 0.4), BP_INK, 7, seed=50)
    el_at(f, virus_el("sly", (0, 0), int(t * 8) % 4), 540, vy, 1.35 * up, t, t0 + 0.25)
    if t > tr: write_on(f, "rhinovirus", 540, vy + 290 * up, t, tr, 52, VIR_S)
    if t > tr + 0.4 and t < tn + 0.3: write_on(f, "the #1 cold germ", 540, vy + 380 * up, t, tr + 0.4, 40, BP_INK)
    if t > tn:
        el_at(f, curd_el("n", (0, 0)), 330, 1150, 0.85, t, tn)
        snowflake_on(f, 760, 1150, 90, ramp(t, tn + 0.15, 0.4))
        if t > tf:
            for x in (330, 760):
                kx = ramp(t, tf + (0 if x < 500 else 0.12), 0.18)
                draw_on(f, [(x - 120, 1030), (x + 120, 1270)], kx, (196, 40, 44), 14, seed=70 + x, tip=False)
                draw_on(f, [(x + 120, 1030), (x - 120, 1270)], kx, (196, 40, 44), 14, seed=71 + x, tip=False)
            write_on(f, "cold food? no", 540, 1360, t, tf + 0.2, 44, (176, 40, 44))
    src(f, SRC_VIR, t, t0 + 0.4, 1462)
    if t < tn: peek(f, t, 880, 400, 0.38, expr="sus", look=(-0.6, 0.3))
    return finish(f, n, look="fresh")


# ---- S3: 'You catch it from other people, from a sneeze, a cough,' the TV room: a packed sofa; the cousin SNEEZES toward Chubby ----
CXH, CYH = 360, 1470          # the cousin on the sofa (feet), Chubby at 720


def sofa_row(f, t, ts, tc, s=1.2):
    comp(f, sofa_el(), 540, 1340)
    pre = clamp((t - (ts - 0.45)) / 0.45) if t < ts else 0.0                              # anticipation: 'ah... ah...' (head tips back)
    after = t >= ts
    lean_c = (-9 * pre) if not after else (14 * math.exp(-(t - ts) * 4))
    chub(f, CXH, CYH, s, t=t, sit=True, shirt=(120, 160, 120), mouth=("o" if (not after and pre > 0.2) else (3 if after and t - ts < 0.3 else 0)),
         expr="ouch" if (after and t - ts < 0.4) else ("sus" if pre > 0.2 else "n"), brow="up", look=(1, -0.3 * pre), turn=0.4, lean=lean_c, la=(24, 12), ra=(40, 20))
    dress(f, CXH, CYH, s, "cousin", lean_c)
    rec = jump_back(t, ts + 0.12, 30) if after else 0
    if isinstance(rec, tuple): rec = rec[0]
    chub(f, 720 + rec, CYH, s, t=t, sit=True, mouth=talk(t), expr="gross" if after else "n", brow="up", look=(-1, 0), turn=-0.4, lean=6 + (8 if after else 0), la=(24, 12), ra=(24, 12))
    sofa_front(f, 1360)


def shot_S3(t, n):
    f = set_tvroom(t); t0 = st_("S3"); ts = T("a2", "sneeze") - 0.05; tc = T("a2", "cough") - 0.05
    sofa_row(f, t, ts, tc)
    mx, my = mouth_xy(CXH, CYH, 1.2, t, 0, 0)
    sneeze_spray(f, mx + 10, my, t, ts, 1, 34, 900, seed=4)
    if t > tc:
        for j in range(3):
            u = clamp((t - tc - j * 0.08) / 0.5)
            if 0 < u < 1: cv2.ellipse(f, (int(mx + 30 + 160 * u), int(my + 10)), (int(20 + 40 * u), int(14 + 26 * u)), 0, 0, 360, C((236, 238, 244)), 5, cv2.LINE_AA)
    if t < ts: kw(f, "FROM PEOPLE", 540, 400, t, t0 + 0.05, "pop", 110, col=INKC)
    else: kw(f, "ACHOO!", 540, 400, t, ts, "shake", 150, col=VIR_S, amp=0.6)
    if t > tc: kw(f, "+ coughs", 540, 540, t, tc, "pop", 80, col=INKC)
    return finish(f, n, look="night")


# ---- S3b: '...a hand you just shook.' close-up handshake; tiny viruses hop from his hand to yours ----
def shot_S3b(t, n):
    f = set_tvroom(t, 10); f = dof(f, 3); t0 = st_("S3b")
    pump = 18 * math.sin((t - t0) * 12) * clamp((t - t0) / 0.2)
    for sg, col in ((-1, (120, 160, 120)), (1, INK_MINT)):                                      # sleeves
        x0 = 540 + sg * 640; x1 = 540 + sg * 150
        P = np.array([(x0, 900 + pump), (x1, 880 + pump), (x1, 1160 + pump), (x0, 1220 + pump)], np.int32)
        cv2.fillPoly(f, [P], C(col), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), 6, cv2.LINE_AA)
    grip_hand(f, 470, 1020 + pump, 3.8, kind="grip"); grip_hand(f, 610, 1020 + pump, 3.8, kind="grip", rot=180)
    for j in range(4):
        u = ((t - t0) * 1.1 + j / 4) % 1
        x = 380 + 320 * u; y = 860 + pump - 180 * math.sin(math.pi * u)
        el_at(f, virus_el("happy", (1, 0), int(t * 8) % 4), x, y, 0.36, op=clamp(min(u, 1 - u) * 6))
    kw(f, "HANDSHAKE", 540, 420, t, t0 + 0.05, "pop", 120, col=INKC)
    return finish(f, n, look="night")


# ---- S4: 'And in winter, we all pack indoors with the windows shut, sharing the same air.' BOARD: a house cut-away; heads pack in; windows shut; ----
#      the virus hops head to head through the same air
HEADS = [(300, 1180), (430, 1150), (560, 1185), (690, 1150), (820, 1180), (365, 1010), (625, 1000)]


def shot_S4(t, n):
    f = board_bg(); t0 = st_("S4"); ti = T("a3", "indoors") - 0.12; tw = T("a3", "windows") - 0.1; ts = T("a3", "same") - 0.12
    house = [(170, 1300), (170, 760), (540, 480), (910, 760), (910, 1300), (170, 1300)]
    draw_on(f, house, ramp(t, t0, 0.5), BP_INK, 8, seed=80, tip=False)
    snowflake_on(f, 110, 470, 40, ramp(t, t0 + 0.2, 0.5), ACC); snowflake_on(f, 980, 560, 34, ramp(t, t0 + 0.4, 0.5), ACC)
    if t < ts: write_on(f, "winter", 540, 330, t, t0 + 0.1, 48, ACC_S)
    for j, (wx, wy) in enumerate(((290, 850), (790, 850))):                                     # windows draw on, then SHUT (bars slam across)
        draw_on(f, [(wx - 70, wy - 60), (wx + 70, wy - 60), (wx + 70, wy + 60), (wx - 70, wy + 60), (wx - 70, wy - 60)], ramp(t, t0 + 0.3, 0.4), BP_INK, 6, seed=90 + j, tip=False)
        if t > tw:
            kk = snap(t, tw + j * 0.1, 3)
            cv2.line(f, (int(wx - 70 * kk), wy), (int(wx + 70 * kk), wy), C(BP_INK), 7, cv2.LINE_AA)
            cv2.line(f, (wx, int(wy - 60 * kk)), (wx, int(wy + 60 * kk)), C(BP_INK), 7, cv2.LINE_AA)
            hatch_on(f, [(wx - 70, wy - 60), (wx + 70, wy - 60), (wx + 70, wy + 60), (wx - 70, wy + 60)], ramp(t, tw + j * 0.1, 0.3), ACC_L)
    for j, (x, y) in enumerate(HEADS):
        if t > ti + j * 0.08:
            k = snap(t, ti + j * 0.08, 3)
            chub_head_only(f, x, y, 0.66 * k + 0.01, t + j, mouth=talk(t) if j == 2 else 0, expr="n" if j != 4 else "ouch", look=((-1) ** j * 0.5, 0), turn=(-1) ** j * 0.3)
    if t > tw: write_on(f, "windows shut", 540, 1400, t, tw, 44, BP_INK)
    if t > ts:
        for q in range(5):                                                                         # the same air swirls between them
            draw_on(f, [(260 + 140 * q + 18 * math.sin(v * 6 + t * 3), 960 + 50 * v) for v in np.linspace(0, 1, 8)], 1.0, ACC, 4, seed=100 + q, tip=False)
        u = ((t - ts) * 1.4) % 1; j0 = int((t - ts) * 1.4) % 4; a, b = HEADS[j0], HEADS[j0 + 1]
        x = a[0] + (b[0] - a[0]) * u; y = a[1] - 70 - 110 * math.sin(math.pi * u)
        el_at(f, virus_el("sly", (1, 0), int(t * 8) % 4), x, y, 0.3)
        kw(f, "SAME AIR", 540, 360, t, ts, "pop", 110, col=ACC_S)
    src(f, SRC_WINTER, t, t0 + 0.6, 1462 + 30)
    return finish(f, n, look="fresh")


# ---- S5: 'So the curd's innocent. Doctors say it's safe in winter,' THE LINEUP lit: the virus in cuffs, curd walks free; INNOCENT; hat tip ----
def shot_S5(t, n):
    f = set_lineup(t); t0 = st_("S5"); ti = T("b1", "innocent") - 0.12; td = T("b1", "Doctors") - 0.1
    lamp_pool(f, 330, 980, 240, 0.45); lamp_pool(f, VX, 980, 240, 0.3)
    walk_out = ramp(t, td + 0.3, 1.2)
    suspect(f, curd_el("happy" if t > ti else "sad", (-0.5, -0.2)), 300 - 230 * walk_out, 1.5, t, num=None)
    by2 = suspect(f, virus_el("ouch", (0.5, 0), int(t * 8) % 4), VX, 1.4, t, num=None)
    el_at(f, cuff_el(354, 0.0), VX, by2 + 90, 0.9)
    detective(f, t, 190, 1990, 1.45, look=(1, -0.4), expr="happy", tip=snap(t, td + 0.2, 4) if t > td + 0.2 else 0.0, mag=False, ra=(26, 14))
    if t > ti: el_at(f, vstamp_el("INNOCENT", (40, 130, 90), 70), 540, 440, 1.0, t, ti, rot=-6)
    if t > td + 0.3: write_on(f, "safe in winter", 540, 590, t, td + 0.3, 44, INKC)
    return finish(f, n, look="warm")


# ---- S5b: '...and its friendly bacteria are good for your gut.' BOARD: a curd bowl, a magnified window of friendly bacteria, an arrow to the gut ----
def shot_S5b(t, n):
    f = board_bg(); t0 = st_("S5b"); tb = T("b1", "bacteria") - 0.12; tg = T("b1", "gut") - 0.12
    el_at(f, curd_el("happy", (0.5, 0)), 290, 700, 1.05, t, t0)
    draw_ell_on(f, 700, 620, 190, 190, ramp(t, t0 + 0.2, 0.4), BP_INK, 7, seed=110)
    draw_on(f, [(420, 660), (520, 640)], ramp(t, t0 + 0.3, 0.3), BP_INK, 6, seed=111, tip=False)
    if t > tb - 0.2:
        bug_crowd(f, 700, 620, t, 5, 0.85, "happy", 100, seed=3)
        write_on(f, "friendly bacteria", 680, 880, t, tb, 40, BP_INK)
    if t > tg - 0.3:
        el_at(f, stomach_ink_el("happy", (0, -0.4)), 540, 1170, 1.35, t, tg - 0.3)
        draw_arrow_on(f, (620, 930), (570, 1030), ramp(t, tg - 0.2, 0.3), ACC_S, 7, 26, bend=0.2)
        if t > tg: kw(f, "GOOD FOR YOUR GUT", 540, 1380, t, tg, "pop", 76, col=ACC_S)
    src(f, SRC_CURD, t, t0 + 0.3, 1462)
    return finish(f, n, look="fresh")


# ---- S6: 'If fridge-cold curd bothers your throat, just let it sit out for a bit.' the worktop: a frosty bowl; Chubby touches his throat; ----
#      on 'sit' a timer runs and the frost melts away
WX, WY, WS = 400, 1720, 1.45


def shot_S6(t, n):
    f = set_worktop(t); t0 = st_("S6"); tt = T("b2", "throat") - 0.15; ts = T("b2", "sit") - 0.12
    melt = ramp(t, ts, 1.2)
    sore = tt < t < ts + 0.2
    chub(f, WX, WY, WS, t=t, la=(24, 12), ra=(150, -150) if sore else (40, 30), mouth=talk(t), expr="ouch" if sore else "happy",
         brow="sad" if sore else "up", look=(0.7, 0.3), turn=0.4, lean=2)
    worktop_front(f, 1330)
    el_at(f, curd_el("ouch" if melt < 0.5 else "happy", (-0.4, 0), frost=1 - melt), 800, 1250, 1.0)
    if melt < 0.9:
        for j in range(3):                                                                           # cold mist off the bowl
            u = ((t * 0.7 + j / 3) % 1); cv2.ellipse(f, (int(760 + 40 * j), int(1130 - 120 * u)), (int(26 + 20 * u), int(14 + 10 * u)), 0, 0, 360, C(ACC_L), 4, cv2.LINE_AA)
    if t < ts: kw(f, "FRIDGE-COLD?", 540, 400, t, t0 + 0.05, "shiver", 104, col=ACC_S)
    else:
        comp(f, timer_el(clamp((t - ts) / 1.6), "A BIT"), 800, 860)
        kw(f, "LET IT SIT", 540, 400, t, ts, "pop", 130, col=INKC)
    return finish(f, n, look="warm")


# ---- S7: 'So keep eating your curd, and just wash your hands more often.' the bathroom sink: suds, the viruses rinse away down the drain ----
def shot_S7(t, n):
    f = set_bathroom(t); t0 = st_("S7"); tw = T("c1", "wash") - 0.12
    chub_head_only(f, 540, 700, 1.7, t, mouth=talk(t), expr="happy", brow="up", look=(0, 0.7), op=0.85)       # his reflection in the round mirror
    el_at(f, curd_el("happy", (-0.6, 0)), 830, 990, 0.55)                                                     # the curd waits on the shelf
    on = ramp(t, t0 + 0.2, 0.3)
    if on > 0:                                                                                                # the tap runs
        cv2.line(f, (540, 1300), (540, int(1300 + 140 * on)), C((200, 228, 248)), 22, cv2.LINE_AA)
        cv2.line(f, (530, 1300), (530, int(1300 + 140 * on)), C((255, 255, 255)), 4, cv2.LINE_AA)
    rub = math.sin(t * 14) * 26 * (t > tw)
    for sg, col in ((-1, INK_MINT), (1, INK_MINT)):                                                         # sleeves from the bottom
        P = np.array([(540 + sg * 120 + rub * sg * 0.3, 1440), (540 + sg * 420, 1920), (540 + sg * 260, 1920), (540 + sg * 40 + rub * sg * 0.3, 1470)], np.int32)
        cv2.fillPoly(f, [P], C(col), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), 6, cv2.LINE_AA)
    grip_hand(f, 480 + rub, 1420, 3.0, kind="open", rot=20); grip_hand(f, 600 - rub, 1420, 3.0, kind="open", rot=-20)
    if t > tw:
        soap_foam(f, 540, 1410, t, 22, 150, ramp(t, tw, 0.4))
        for j in range(4):
            u = ((t - tw) * 0.9 + j / 4) % 1
            el_at(f, virus_el("ouch", (0, 1), int(t * 8) % 4), 540 + 160 * math.cos(u * 8 + j) * (1 - u), 1380 + 140 * u, 0.3 * (1 - 0.6 * u), op=1 - u)
    if t < tw: kw(f, "KEEP THE CURD", 540, 330, t, t0 + 0.05, "pop", 98, col=INKC)
    else: ui_word(f, "and just", "[WASH YOUR HANDS]", 340, t, tw, col=INKC, acc=ACC_S, size=96, lead_col=INKC)
    return finish(f, n, look="fresh")


# ---- S8: 'Send this to whoever keeps taking the curd off your plate every winter.' the table: the aunty slides the curd away; Chubby points ----
def shot_S8(t, n):
    f = set_winter(t); tc = T("c2", "curd") - 0.15
    chub(f, LX - 60, LY, LS, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="smirk", brow="up", look=(1, 0), turn=0.5)
    aunty(f, t, 0.0, expr="sus", look=(-0.6, 0.2), pose=dict(la=(70, 60), ra=(24, 12), lean=-3))
    cloth_front(f, 1330)
    slide = ramp(t, tc, 0.8)
    el_at(f, curd_el("sad" if slide > 0.3 else "n", (1, 0)), 520 + 200 * slide, 1290, 0.85)
    ui_word(f, "send this to the", "[CURD POLICE]", 420, t, T("c2", "Send") - 0.05, col=INKC, acc=ACC_S, size=120, lead_col=INKC)
    return finish(f, n, look="cool")


# ---- S9: the logo beat (0.6 s) ----
def shot_S9(t, n):
    t0 = st_("S9"); f = set_winter(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.25) * 0.95)
    comp(f, ed_el("follow for more food facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.12) / 0.2))
    return finish(f, n, look="cool")


# ---- S10: the LOOP TAIL: back at the table exactly like frame 0 (no caption); loop_seam blends into frame 0 ----
def shot_S10(t, n):
    f = set_winter(t)
    table_hook(f, t)
    hook_band(f)
    return finish(f, n, look="cool")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i2", "blame") - 0.12, 0.35, 14), (T("i2", "wrong") - 0.1, 0.35, 12), (T("a1", "viruses") - 0.15, 0.45, 18),
           (T("a1", "food") - 0.1, 0.3, 10), (T("a2", "sneeze") - 0.05, 0.4, 16), (T("a3", "windows") - 0.1, 0.25, 8),
           (T("b1", "innocent") - 0.12, 0.35, 14), (T("b2", "sit") - 0.12, 0.2, 6), (T("c1", "wash") - 0.12, 0.25, 8), (T("c2", "curd") - 0.15, 0.25, 8)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0
    for ti, d, a in IMPACTS:
        if s["start"] - 0.05 <= ti < s["end"] and ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83); z += 0.03 * k
    if dx or dy or abs(z - 1) > 1e-4: f = cam(f, z, W / 2, H / 2, dx, dy)
    return f


_FIRST = {}


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); k = sh["trans"]; dt = t - sh["start"]
    if i > 0:
        if k == "erase" and dt < 0.42:
            f = erase_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42)
        elif k == "morph" and dt < 0.42:
            a, b = MORPH[sh["id"]]; f = morph_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42, a, b)
        elif k == "whip" and dt < 0.22:
            p = 1 - dt / 0.22; M = np.float32([[1, 0, -360 * p * p], [0, 1, 0]])
            f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
        elif k == "flash" and dt < 0.14: f = f + 0.8 * (1 - dt / 0.14) ** 1.5
        elif k == "punch" and dt < 0.16: f = cam(f, 1 + 0.08 * (1 - dt / 0.16)) + 0.12 * (1 - dt / 0.16)
    nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    if nx is not None and nx["trans"] == "whip" and sh["end"] - t < 0.14:
        p = 1 - (sh["end"] - t) / 0.14; M = np.float32([[1, 0, 360 * p * p], [0, 1, 0]])
        f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
    if i == len(SHOTS) - 1:                                                     # the LOOP SEAM: the tail melts into frame 0
        if "f0" not in _FIRST: _FIRST["f0"] = rs(SHOTS[0]["id"], 0.0, 0)
        f = loop_seam(f, _FIRST["f0"], t, END, 0.33)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
