# ================= shots: FreshNestHub 48 — "Does eating ice cream in winter give you a cold?" (Chubby INK; 35-50 s rule; ONE takeaway; Part 2 of ep 44) =================
# COLOUR SCRIPT: warm wedding gold/maroon (the party) vs cold night blue (the fog outside, the shiver) + ONE accent STRAWBERRY PINK (the ice cream, the question).
# The virus = olive green (the culprit, from lib44). Board shots = white paper + blue ink + the pink accent.
# Story = THE WINTER WEDDING (new place): Chubby in a shawl at the dessert counter, shivering, ice cream at his lips; the relatives say NO, the doctor says FINE;
# the board shows WHERE a cold comes from (a virus, from people) and why ice cream can even SOOTHE a sore throat (Mayo Clinic; the NHS lists ice lollies).
# Visual upgrade (ep 48): Chubby's SHIVER acting (lib48 shiver(): uneven 8-10 Hz tremor bursts, hunched shoulders, chattering teeth, breath fog puffs),
# the wedding shawl, the shared serving ladle, a profile throat on the board that cools from red to pink.
END = round(LINES["c2"]["end"] + 1.33, 3)            # 35-50 s rule: 0.1 s air + 0.6 s logo + 0.63 s loop tail
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "really") - 0.12, "punch"),
    ("S1", T("i2", "Ask") - 0.12, "whip"), ("S1b", T("i2", "Ask", 1) - 0.1, "cut"),
    ("S2", T("a1", "A") - 0.12, "erase"), ("S2b", T("a1", "there's") - 0.1, "erase"),
    ("S3", T("a2", "You") - 0.1, "whip"), ("S3b", T("a2", "or") - 0.12, "cut"),
    ("S4", T("a3", "And") - 0.1, "erase"),
    ("S5", T("b1", "But") - 0.12, "whip"),
    ("S6", T("b2", "Got") - 0.1, "erase"), ("S6b", T("b2", "cold") - 0.12, "cut"),
    ("S7", T("b3", "The") - 0.1, "erase"),
    ("S8", T("c1", "So") - 0.12, "whip"), ("S8b", T("c1", "wash") - 0.12, "cut"),
    ("S9", T("c2", "Send") - 0.1, "punch"),
    ("S10", LINES["c2"]["end"] + 0.1, "punch"), ("S11", LINES["c2"]["end"] + 0.7, "cut"),
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


def hook_band(f, y0=228, y1=700, a=0.72):
    """a soft paper band behind the hook words (feathered edges) - the tent stripes are busy."""
    m = np.zeros((H, 1), np.float32); m[y0:y1] = a
    m = cv2.GaussianBlur(np.repeat(m, 4, 1), (1, 61), 0)[:, :1, None]
    f[:] = f * (1 - m) + np.array(C(PAPER), np.float32) * m


def hook_words(f, t, t0=-1.0, op=1.0):
    """the hook question as moving words (on screen at frame 0): A COLD? shivers with snow caps + icicles."""
    kw(f, "DO YOU KNOW IF", 540, 300, t, t0, "pop", 70, col=INKC, op=op)
    kw(f, "ICE CREAM IN WINTER", 540, 425, t, t0, "pop", 74, col=ACC_S, op=op)
    kw(f, "= A COLD?", 540, 590, t, t0, "shiver", 150, col=(40, 92, 150), op=op)


LX, LY, LS = 380, 1690, 1.62           # Chubby at the dessert counter (counter top 1330)


def chubby_cold(f, t, amt=1.0, eat=False, x=LX, look=(0.9, 0.2), extra=None):
    """Chubby in the wedding shawl, SHIVERING, the spoon of ice cream at his lips (eat=True: he munches happily, no shiver)."""
    sv = shiver(t, amt if not eat else 0.0, LS, seed=1)
    kw_ = dict(la=(26, 14), ra=(150, -128), hand_r="grip")
    if extra: kw_.update(extra)
    chub(f, x + sv["dx"], LY, LS, t=t, mouth=(munch(t) if eat else ("o" if amt < 0.3 else sv["mouth"])), expr=("happy" if eat else sv["expr"]),
         brow=("up" if eat else sv["brow"]), look=look, turn=0.45, lean=-3 + sv["lean"], squash=sv["squash"], hair=sv["hair"], **kw_)
    stole(f, x, LY, LS, -3 + sv["lean"], sv["dx"])
    # pink scoop on the spoon tip (at the lips)
    mx, my = mouth_xy(x + sv["dx"], LY, LS, t, -3 + sv["lean"], sv["squash"])
    sx, sy = mx + 36, my + 6                                                       # spoon bowl at the lips, handle down-right to his fist
    cv2.line(f, (int(sx), int(sy)), (int(sx + 150), int(sy + 40)), C(INKC), 14, cv2.LINE_AA); cv2.line(f, (int(sx), int(sy)), (int(sx + 150), int(sy + 40)), C((214, 170, 110)), 8, cv2.LINE_AA)
    cv2.ellipse(f, (int(sx), int(sy)), (34, 22), 10, 0, 360, C(ACC), -1, cv2.LINE_AA); cv2.ellipse(f, (int(sx), int(sy)), (34, 22), 10, 0, 360, C(INKC), 4, cv2.LINE_AA)
    cv2.ellipse(f, (int(sx - 10), int(sy - 8)), (10, 5), 10, 0, 360, C((255, 230, 240)), -1, cv2.LINE_AA)
    if not eat:
        fog_puffs(f, mx - 20, my - 30, t, 1.6, -1, 0.55, t_start=0.35)
        tremble_marks(f, x + sv["dx"], LY, LS, t)
    return mx, my


# ---- S0: HOOK at frame 0: the winter wedding, Chubby in a shawl SHIVERING with ice cream at his lips, breath fog; A COLD? shivers ----
def shot_S0(t, n):
    f = set_wedding(t)
    chubby_cold(f, t)
    wedding_front(f, 1330)
    el_at(f, icecream_cup_el("happy", (-0.6, -0.2), melt=0.25), 700, 1240, 0.95)
    el_at(f, cone_el("happy", (-0.8, 0)), 920, 1220, 0.75, rot=6)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="warm")


# ---- S0b: '...really give you a cold?' close-up: teeth chatter, breath fog, the pink scoop right under his nose; his eyes go to the scoop and back ----
def shot_S0b(t, n):
    f = set_wedding(t, 9); f = dof(f, 3); t0 = st_("S0b")
    sv = shiver(t, 1.0, 2.5, seed=2)
    hx = 470 + sv["dx"] * 0.7
    chub_head_only(f, hx, 1120, 2.5, t, mouth=sv["mouth"], expr="ouch", brow="sad", look=(0.6, 0.7) if (t - t0) % 1.2 < 0.6 else (0.2, 0.0), turn=0.35, hair=sv["hair"])
    stole(f, hx, 1120 + 420 * 2.5 - 40, 2.5, 0, 0)
    el_at(f, spoon_el(), 800, 1400, 1.4, rot=-30)
    cv2.ellipse(f, (720, 1330), (70, 48), -30, 0, 360, C(ACC), -1, cv2.LINE_AA); cv2.ellipse(f, (720, 1330), (70, 48), -30, 0, 360, C(INKC), 5, cv2.LINE_AA)
    fog_puffs(f, hx + 120, 1240, t, 1.2, 1, 2.0, t_start=t0 + 0.1)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="cool")


# ---- S1: 'Ask anyone at home, and it's a big no.' the relatives at the counter: aunty + uncle, fingers wagging, heads shaking: BIG NO ----
def relative(f, x, y, s, t, kind, shirt, wag=1.0, look=(-1, 0), expr="angry", phase=0.0):
    shake = 6 * math.sin(t * 14 + phase) * wag
    chub(f, x, y, s, t=t, shirt=shirt, la=(30 + 110 * wag, 30 + 120 * wag) if kind == "aunty" else (24, 12), ra=(24, 12) if kind == "aunty" else (120, 140),
         mouth=talk(t) if wag > 0.5 else 0, expr=expr, brow="sus", look=look, turn=-0.5 * (1 if look[0] < 0 else -1), lean=shake * 0.4,
         hand_l="point" if kind == "aunty" else "open", hand_r="open" if kind == "aunty" else "point")
    dress(f, x, y, s, kind, shake * 0.4)


def shot_S1(t, n):
    f = set_wedding(t); t0 = st_("S1"); tn = T("i2", "no") - 0.1
    relative(f, 300, 1700, 1.45, t, "aunty", (214, 96, 128), 1.0, (1, 0), "angry", 0.0)
    relative(f, 760, 1700, 1.45, t, "boss", (96, 120, 160), 1.0, (-1, 0), "angry", 1.4)
    wedding_front(f, 1330)
    el_at(f, icecream_cup_el("sad" if t > tn else "n", (0, -0.4)), 540, 1250, 0.9)
    kw(f, "ASK ANYONE AT HOME", 540, 360, t, t0 + 0.05, "pop", 80, col=INKC)
    if t > tn: kw(f, "BIG NO!", 540, 520, t, tn, "shake", 160, col=(176, 40, 44), amp=0.6)
    return finish(f, n, look="warm")


# ---- S1b: 'Ask a doctor, and it's... fine.' a doctor (white coat + stethoscope) shrugs, thumbs-up on 'fine'; FINE stamp; Chubby's shiver stops ----
def shot_S1b(t, n):
    f = set_wedding(t); t0 = st_("S1b"); tf = T("i2", "fine") - 0.1
    ok = t > tf
    chub(f, 720, 1700, 1.5, t=t, shirt=(246, 248, 250), la=(24, 12), ra=(150, 170) if ok else (40, 30), hand_r="point" if ok else "open",
         mouth=talk(t), expr="happy" if ok else "n", brow="up", look=(-1, 0), turn=-0.5, lean=-2)
    hx_ = 720 - 2 * 1.5; cy_ = 1700 - 320 * 1.5
    cv2.ellipse(f, (int(hx_), int(cy_ - 40)), (70, 60), 0, 0, 180, C((70, 76, 90)), 8, cv2.LINE_AA)                     # stethoscope
    cv2.circle(f, (int(hx_ + 40), int(cy_ + 40)), 16, C((180, 186, 196)), -1, cv2.LINE_AA); cv2.circle(f, (int(hx_ + 40), int(cy_ + 40)), 16, C(INKC), 4, cv2.LINE_AA)
    cv2.line(f, (int(hx_ - 70), int(cy_ - 40)), (int(hx_ + 40), int(cy_ + 24)), C((70, 76, 90)), 7, cv2.LINE_AA)
    cv2.rectangle(f, (int(hx_ - 80), int(cy_ + 30)), (int(hx_ - 40), int(cy_ + 70)), C((250, 250, 250)), -1); cv2.line(f, (int(hx_ - 60), int(cy_ + 36)), (int(hx_ - 60), int(cy_ + 64)), C((214, 50, 50)), 8); cv2.line(f, (int(hx_ - 74), int(cy_ + 50)), (int(hx_ - 46), int(cy_ + 50)), C((214, 50, 50)), 8)
    sv = shiver(t, 0.0 if ok else 0.8, 1.4, seed=3)
    chub(f, 290 + sv["dx"], 1700, 1.4, t=t, la=(24, 12), ra=(24, 12), mouth="o" if ok else sv["mouth"], expr="wow" if ok else sv["expr"], brow="up",
         look=(1, 0), turn=0.5, lean=sv["lean"], squash=sv["squash"])
    stole(f, 290, 1700, 1.4, sv["lean"], sv["dx"])
    wedding_front(f, 1330)
    kw(f, "ASK A DOCTOR", 540, 360, t, t0 + 0.05, "pop", 96, col=INKC)
    if ok: el_at(f, vstamp_el("FINE", (40, 130, 90), 110), 540, 540, 1.0, t, tf, rot=-6)
    return finish(f, n, look="warm")


# ---- S2: 'A cold comes from a virus,' BOARD: a sneezy head with a cold -> an arrow back to the VIRUS that draws itself; label ----
def shot_S2(t, n):
    f = board_bg(); t0 = st_("S2"); tv = T("a1", "virus") - 0.15
    draw_ell_on(f, 300, 720, 150, 150, ramp(t, t0, 0.4), BP_INK, 7, seed=480)
    chub_head_only(f, 300, 740, 0.95 * snap(t, t0 + 0.15, 4) + 0.01, t, mouth="o", expr="ouch", brow="sad", look=(0.5, 0), turn=0.3)
    write_on(f, "a cold", 300, 950, t, t0 + 0.2, 50, BP_INK)
    if t > tv:
        draw_arrow_on(f, (700, 720), (470, 720), ramp(t, tv, 0.3), ACC_S, 8, 30)
        draw_ell_on(f, 800, 720, 140, 140, ramp(t, tv, 0.35), BP_INK, 7, seed=481)
        el_at(f, virus_el("sly", (-0.6, 0), int(t * 8) % 4), 800, 720, 0.9, t, tv + 0.1)
        write_on(f, "a virus", 800, 950, t, tv + 0.2, 50, VIR_S)
        kw(f, "VIRUS", 540, 1200, t, tv + 0.1, "shake", 150, col=VIR_S, amp=0.4)
    peek(f, t, 880, 1350, 0.4, expr="sus", look=(-0.6, -0.3))
    return finish(f, n, look="fresh")


# ---- S2b: '...and there's no virus in your ice cream. It's just cold.' BOARD: a big cone under a magnifier: only snowflakes inside, the virus outline gets a red X;
#      on 'just cold' a blue thermometer draws on = JUST COLD ----
def snowflake_on(f, x, y, r, k, col=None):
    col = col or (92, 156, 214)
    for j in range(3):
        a = j * math.pi / 3
        draw_on(f, [(x - r * math.cos(a), y - r * math.sin(a)), (x + r * math.cos(a), y + r * math.sin(a))], clamp(k * 3 - j), col, 6, seed=60 + j, tip=False)


def shot_S2b(t, n):
    f = board_bg(); t0 = st_("S2b"); tn = T("a1", "virus", 1) - 0.12; tj = T("a1", "just") - 0.12
    el_at(f, cone_el("happy", (0.3, -0.2)), 360, 900, 1.5, t, t0)
    draw_ell_on(f, 700, 720, 200, 200, ramp(t, t0 + 0.15, 0.35), BP_INK, 8, seed=482)          # the magnifier lens
    draw_on(f, [(840, 860), (960, 990)], ramp(t, t0 + 0.4, 0.2), BP_INK, 16, seed=483, tip=False)
    for j, (dx, dy) in enumerate(((-80, -60), (40, -90), (90, 30), (-40, 70), (-110, 20))):
        snowflake_on(f, 700 + dx, 720 + dy, 26, ramp(t, t0 + 0.3 + 0.08 * j, 0.3))
    if t > tn:
        draw_ell_on(f, 700, 720, 60, 60, ramp(t, tn, 0.2), VIR_S, 5, seed=484)
        kx = ramp(t, tn + 0.25, 0.18)
        draw_on(f, [(620, 640), (780, 800)], kx, (196, 40, 44), 14, seed=485, tip=False)
        draw_on(f, [(780, 640), (620, 800)], kx, (196, 40, 44), 14, seed=486, tip=False)
        write_on(f, "no virus inside", 540, 300, t, tn + 0.2, 48, (176, 40, 44))
    if t > tj:
        TX_ = 850
        draw_on(f, [(TX_, 1300), (TX_, 1060)], ramp(t, tj, 0.25), BP_INK, 26, seed=487, tip=False)
        cv2.circle(f, (TX_, 1320), 40, C((92, 156, 214)), -1, cv2.LINE_AA); cv2.circle(f, (TX_, 1320), 40, C(BP_INK), 6, cv2.LINE_AA)
        cv2.line(f, (TX_, 1300), (TX_, int(1300 - 60 * ramp(t, tj + 0.1, 0.4))), C((92, 156, 214)), 14, cv2.LINE_AA)
        kw(f, "JUST COLD", 470, 1290, t, tj, "shiver", 100, col=(40, 92, 150))
    src(f, SRC_VIR48, t, t0 + 0.4, 1462)
    return finish(f, n, look="fresh")


# ---- S3: 'You catch that virus from other people, from a sneeze, a cough,' the wedding: a guest SNEEZES next to Chubby; droplets carry mini viruses ----
GX, GY = 760, 1700


def shot_S3(t, n):
    f = set_wedding(t); t0 = st_("S3"); ts = T("a2", "sneeze") - 0.05; tc = T("a2", "cough") - 0.05
    pre = clamp((t - (ts - 0.45)) / 0.45) if t < ts else 0.0
    after = t >= ts
    lean_c = (9 * pre) if not after else (-14 * math.exp(-(t - ts) * 4))
    chub(f, GX, GY, 1.45, t=t, shirt=(120, 160, 120), mouth=("o" if (not after and pre > 0.2) else (3 if after and t - ts < 0.3 else 0)),
         expr="ouch" if (after and t - ts < 0.4) else ("sus" if pre > 0.2 else "n"), brow="up", look=(-1, -0.3 * pre), turn=-0.4, lean=lean_c, la=(24, 12), ra=(40, 20))
    dress(f, GX, GY, 1.45, "cousin", lean_c)
    rec = jump_back(t, ts + 0.12, 30) if after else 0
    if isinstance(rec, tuple): rec = rec[0]
    sv = shiver(t, 0.5, 1.45, seed=4)
    chub(f, 300 - rec + sv["dx"], GY, 1.45, t=t, mouth=talk(t), expr="gross" if after else "n", brow="up", look=(1, 0), turn=0.4, lean=-6 - (8 if after else 0), la=(24, 12), ra=(24, 12))
    stole(f, 300 - rec, GY, 1.45, -6 - (8 if after else 0), sv["dx"])
    wedding_front(f, 1330)
    mx, my = mouth_xy(GX, GY, 1.45, t, lean_c, 0)
    sneeze_spray(f, mx - 10, my, t, ts, -1, 34, 900, seed=4)
    if t > tc:
        for j in range(3):
            u = clamp((t - tc - j * 0.08) / 0.5)
            if 0 < u < 1: cv2.ellipse(f, (int(mx - 30 - 160 * u), int(my + 10)), (int(20 + 40 * u), int(14 + 26 * u)), 0, 0, 360, C((236, 238, 244)), 5, cv2.LINE_AA)
    if t < ts: kw(f, "FROM PEOPLE", 540, 400, t, t0 + 0.05, "pop", 110, col=INKC)
    else: kw(f, "ACHOO!", 540, 400, t, ts, "shake", 150, col=VIR_S, amp=0.6)
    if t > tc: kw(f, "+ coughs", 540, 540, t, tc, "pop", 80, col=INKC)
    return finish(f, n, look="warm")


# ---- S3b: '...or a germy hand.' close-up of the buffet: the SHARED LADLE in the gulab jamun bowl; hand after hand grabs the handle; viruses hop on it ----
def shot_S3b(t, n):
    f = set_wedding(t, 10); f = dof(f, 3); t0 = st_("S3b")
    wedding_front(f, 1250)
    el_at(f, jamun_bowl_el("ouch", (0.5, -0.5)), 420, 1190, 1.5)
    gx, gy = ladle(f, 520, 1120, -32, 1.25)
    k = int((t - t0) / 0.42) % 3                                                           # hands take turns: grab - let go
    u = ((t - t0) / 0.42) % 1
    reach = math.sin(math.pi * u)
    sleeves = ((214, 96, 128), (96, 120, 160), (120, 160, 120))
    sx, sy = 1120, 700 + 160 * k
    hx, hy = sx + (gx - sx) * reach, sy + (gy - sy) * reach
    cv2.line(f, (int(sx), int(sy)), (int(hx + 40), int(hy)), C(INKC), 96, cv2.LINE_AA); cv2.line(f, (int(sx), int(sy)), (int(hx + 40), int(hy)), C(sleeves[k]), 84, cv2.LINE_AA)
    grip_hand(f, hx, hy, 2.6, kind="grip", rot=-40)
    for j in range(min(4, 1 + int((t - t0) / 0.3))):                                       # viruses pile up on the handle
        p = 0.3 + 0.17 * j
        vx = 520 + (gx - 520) * p; vy = 1120 + (gy - 1120) * p - 36
        el_at(f, virus_el("happy", (0.3, 0), int(t * 8 + j) % 4), vx, vy + 4 * math.sin(t * 9 + j), 0.34)
    kw(f, "GERMY HAND", 540, 400, t, t0 + 0.05, "shake", 120, col=VIR_S, amp=0.3)
    return finish(f, n, look="warm")


# ---- S4: 'And winter packs us all indoors, so it hops from person to person.' BOARD: a wedding TENT cut-away, the side flaps drop shut (cold outside),
#      heads pack in, then the virus hops head to head ----
HEADS = [(300, 1200), (430, 1170), (560, 1205), (690, 1170), (820, 1200), (365, 1030), (625, 1020), (495, 1035)]


def shot_S4(t, n):
    f = board_bg(); t0 = st_("S4"); ti = T("a3", "indoors") - 0.12; th = T("a3", "hops") - 0.12
    tent = [(150, 1310), (150, 820), (330, 640), (540, 560), (750, 640), (930, 820), (930, 1310)]
    draw_on(f, tent, ramp(t, t0, 0.5), BP_INK, 8, seed=490, tip=False)
    draw_on(f, [(540, 560), (540, 470)], ramp(t, t0 + 0.3, 0.2), BP_INK, 6, seed=491, tip=False)              # the pole + flag
    if t > t0 + 0.45: hatch_on(f, [(540, 470), (610, 490), (540, 510)], 1.0, ACC)
    for j, (sx_) in enumerate((80, 1000)):                                                                         # cold outside: snowflakes + fog lines
        snowflake_on(f, sx_, 760 + 140 * j, 34, ramp(t, t0 + 0.2, 0.4))
    write_on(f, "cold night", 540, 1420, t, t0 + 0.2, 40, (40, 92, 150))
    k_shut = ramp(t, ti - 0.3, 0.4)                                                                                # side flaps drop shut
    for sg in (-1, 1):
        x = 540 + sg * 390
        draw_on(f, [(x, 820), (x, 820 + 490 * k_shut)], 1.0, BP_INK, 6, seed=492 + sg, tip=False)
    for j, (x, y) in enumerate(HEADS):
        if t > ti + j * 0.07:
            k = snap(t, ti + j * 0.07, 3)
            chub_head_only(f, x, y, 0.62 * k + 0.01, t + j, mouth=talk(t) if j == 2 else 0, expr="n" if j != 4 else "ouch", look=((-1) ** j * 0.5, 0), turn=(-1) ** j * 0.3)
    if t < th: kw(f, "WINTER = INDOORS", 540, 340, t, t0 + 0.1, "pop", 90, col=INKC)
    else:
        order = [5, 2, 6, 3, 4]
        u = ((t - th) * 1.6) % 1; j0 = int((t - th) * 1.6) % (len(order) - 1)
        a, b = HEADS[order[j0]], HEADS[order[j0 + 1]]
        x = a[0] + (b[0] - a[0]) * u; y = a[1] - 70 - 120 * math.sin(math.pi * u)
        el_at(f, virus_el("sly", (1, 0), int(t * 8) % 4), x, y, 0.3)
        kw(f, "PERSON TO PERSON", 540, 340, t, th, "sneak", 86, col=VIR_S)
    src(f, SRC_WIN48, t, t0 + 0.6, 1462 + 30)
    return finish(f, n, look="fresh")


# ---- S5: 'But wait, the cold part might even help you.' close-up: Chubby's TAKE (eyes pop, brows up), the scoop held up into the light; WAIT... -> HELP? ----
def shot_S5(t, n):
    f = set_wedding(t, 8); f = dof(f, 2); t0 = st_("S5"); tw = T("b1", "wait") - 0.08; th = T("b1", "help") - 0.12
    tk = take(t, tw) if t > tw else dict(dy=0, squash=0, lean=0, expr="n", brow="n", look=(0, 0))
    chub(f, 430, 1880 + tk.get("dy", 0), 2.0, t=t, la=(24, 12), ra=(150, 175), hand_r="grip", hold=scale_el(cone_el("wow", (-0.6, -0.4)), 0.7), hold_off=(0, -60),
         hold_front=True, mouth=("jaw" if tw < t < tw + 0.5 else talk(t)), expr="wow", brow="up", look=(0.6, -0.6), turn=0.3, lean=tk.get("lean", 0), squash=tk.get("squash", 0))
    stole(f, 430, 1880 + tk.get("dy", 0), 2.0, tk.get("lean", 0), 0)
    lamp_pool(f, 700, 700, 260, 0.35 * ramp(t, th, 0.3))
    if t < th: kw(f, "WAIT...", 540, 380, t, tw, "pop", 140, col=INKC)
    else: kw(f, "IT CAN HELP?", 540, 380, t, th, "pop", 120, col=ACC_S)
    return finish(f, n, look="golden")


# ---- S6 / S6b: 'Got a sore throat? Mayo Clinic doctors say cold ice cream can actually soothe it.' BOARD: a profile head; the throat glows RED with heat
#      lines (sore); on 'cold' a pink scoop slides down the throat, the red hatch cools to pink/blue: SOOTHED ----
PROF = [(300, 700), (318, 560), (380, 450), (480, 410), (580, 440), (640, 520), (660, 580), (700, 640), (650, 660), (668, 700), (648, 730), (662, 790),
        (600, 840), (600, 1300)]
PROF_B = [(300, 700), (318, 860), (370, 990), (400, 1300)]
THR = [(520, 820), (566, 820), (570, 1240), (526, 1240)]


def board_throat(f, t, t0, sore=1.0, cool=0.0, scoop_k=None):
    draw_on(f, PROF, ramp(t, t0, 0.5), BP_INK, 7, seed=500, tip=False)
    draw_on(f, PROF_B, ramp(t, t0, 0.5), BP_INK, 7, seed=501, tip=False)
    if t > t0 + 0.3:
        cv2.circle(f, (580, 540), 12, C(BP_INK), -1, cv2.LINE_AA)                                  # eye
        draw_ell_on(f, 400, 620, 30, 46, ramp(t, t0 + 0.3, 0.3), BP_INK, 6, seed=505)              # ear
    draw_on(f, [(640, 700), (560, 740), (520, 820), (526, 1240)], ramp(t, t0 + 0.3, 0.4), BP_INK, 5, seed=502, tip=False)
    draw_on(f, [(640, 720), (586, 770), (566, 820), (570, 1240)], ramp(t, t0 + 0.3, 0.4), BP_INK, 5, seed=503, tip=False)
    if sore > 0:
        red = _mix((214, 60, 54), (240, 150, 170), cool)
        hatch_on(f, [(520, 820), (566, 820), (570, 1010), (524, 1010)], sore, red, gap=10, w=5)
        if cool < 0.6:
            for j in range(3):                                                                         # heat zigzags
                y = 840 + 60 * j; x0 = 640 + 8 * math.sin(t * 9 + j)
                pts = [(x0 + 14 * (i % 2), y + 18 * i) for i in range(6)]
                draw_on(f, pts, sore * (1 - cool / 0.6), (214, 60, 54), 5, seed=510 + j, tip=False)
    if scoop_k is not None and 0 <= scoop_k <= 1:
        y = 760 + 360 * scoop_k; x = 600 - 50 * clamp(scoop_k * 3)
        cv2.circle(f, (int(x), int(y)), 26, C(ACC), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), 26, C(INKC), 4, cv2.LINE_AA)
    if cool > 0.3:
        for j in range(4):
            snowflake_on(f, 470 + 140 * (j % 2), 860 + 90 * j, 20, clamp((cool - 0.3) / 0.4))


def shot_S6(t, n):
    f = board_bg(); t0 = st_("S6"); ts = T("b2", "sore") - 0.1
    board_throat(f, t, t0, sore=ramp(t, ts, 0.4))
    if t > ts:
        draw_arrow_on(f, (820, 900), (660, 900), ramp(t, ts + 0.1, 0.3), (196, 40, 44), 7, 26)
        write_on(f, "sore throat", 830, 1010, t, ts + 0.15, 46, (176, 40, 44))
    kw(f, "SORE THROAT?", 540, 300, t, ts, "shake", 110, col=(176, 40, 44), amp=0.3)
    peek(f, t, 860, 1330, 0.42, expr="ouch", look=(-0.6, -0.3), brow="sad")
    return finish(f, n, look="fresh")


def shot_S6b(t, n):
    f = board_bg(); t0 = st_("S6b"); tc = T("b2", "cold") - 0.12; ts = T("b2", "soothe") - 0.12
    f = f.copy()
    sk = (t - tc) / 1.2
    board_throat(f, t, t0 - 3, sore=1.0, cool=ramp(t, ts, 0.6), scoop_k=sk if sk <= 1 else None)
    el_at(f, icecream_cup_el("happy", (-0.8, -0.2)), 840, 700, 0.95, t, tc)
    f = crash_zoom(f, t, ts, 1.12, 560, 950) if t > ts else f
    if t > ts: kw(f, "SOOTHE", 540, 330, t, ts, "breathe", 140, col=ACC_S)
    src(f, SRC_THROAT, t, t0 + 0.3, 1462)
    return finish(f, n, look="fresh")


# ---- S7: 'The NHS even lists ice lollies for a sore throat.' BOARD: a self-care CARD writes itself (SORE THROAT? what helps), the last row = ICE LOLLIES with a tick,
#      the lolly pops in; Chubby peeks and does a double take ----
def shot_S7(t, n):
    f = board_bg(); t0 = st_("S7"); tl = T("b3", "lollies") - 0.12
    card = [(190, 560), (890, 560), (890, 1290), (190, 1290), (190, 560)]
    draw_on(f, card, ramp(t, t0, 0.35), BP_INK, 7, seed=520, tip=False)
    write_on(f, "SORE THROAT?", 540, 640, t, t0 + 0.15, 48, (176, 40, 44))
    write_on(f, "what helps:", 540, 730, t, t0 + 0.5, 38, BP_INK)
    rows = ["rest + drinks", "lozenges", "ice lollies"]
    for j, r in enumerate(rows):
        y = 860 + 130 * j; tj = t0 + 0.7 + 0.35 * j if j < 2 else tl
        if t > tj:
            if j == 2: hatch_on(f, [(210, y - 50), (870, y - 50), (870, y + 50), (210, y + 50)], ramp(t, tl, 0.3), ACC_L)
            write_on(f, r, 500, y, t, tj, 52, ACC_S if j == 2 else BP_INK)
            draw_on(f, [(250, y), (275, y + 25), (320, y - 25)], ramp(t, tj + 0.15, 0.2), (40, 130, 90), 8, seed=530 + j, tip=False)
    if t > tl:
        el_at(f, lolly_el("happy", (-0.6, 0)), 800, 1170, 0.75, t, tl, rot=8)
    src(f, SRC_NHS, t, t0 + 0.3, 1462)
    lk, ln, ex, br = double_take(t, tl + 0.1) if t > tl + 0.1 else ((-0.5, -0.4), 0, None, None)
    peek(f, t, 880, 400, 0.4, expr=ex or "sus", look=(-abs(lk[0]), lk[1]), brow=br or "sus")
    return finish(f, n, look="fresh")


# ---- S8: 'So enjoy the scoop,' back at the counter: no more shiver, Chubby happily munches; the relatives behind gasp ----
def shot_S8(t, n):
    f = set_wedding(t); t0 = st_("S8")
    relative(f, 860, 1560, 1.0, t, "aunty", (214, 96, 128), 0.0, (-1, 0), "wow", 0.0)
    chubby_cold(f, t, 0.0, eat=True, x=LX)
    wedding_front(f, 1330)
    el_at(f, icecream_cup_el("love", (-0.6, -0.2)), 700, 1240, 0.95)
    kw(f, "ENJOY THE SCOOP", 540, 360, t, t0 + 0.05, "pop", 82, col=ACC_S)
    return finish(f, n, look="golden")


# ---- S8b: '...and wash your hands instead.' the wedding hand-wash: a steel jug pours over his hands, suds, the viruses rinse off and fall ----
def shot_S8b(t, n):
    f = set_wedding(t, 10); f = dof(f, 3); t0 = st_("S8b")
    lota(f, 790, 820, 1.3, -35)
    k = ramp(t, t0 + 0.05, 0.2)
    if k > 0:
        cv2.line(f, (700, 900), (560, int(900 + 420 * k)), C((200, 228, 248)), 22, cv2.LINE_AA)
        cv2.line(f, (692, 900), (552, int(900 + 420 * k)), C((255, 255, 255)), 4, cv2.LINE_AA)
    rub = math.sin(t * 14) * 26
    for sg in (-1, 1):
        P = np.array([(540 + sg * 120 + rub * sg * 0.3, 1440), (540 + sg * 420, 1920), (540 + sg * 260, 1920), (540 + sg * 40 + rub * sg * 0.3, 1470)], np.int32)
        cv2.fillPoly(f, [P], C(INK_MINT), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), 6, cv2.LINE_AA)
    grip_hand(f, 470 + rub, 1370, 3.8, kind="open", rot=20); grip_hand(f, 610 - rub, 1370, 3.8, kind="open", rot=-20)
    soap_foam(f, 540, 1370, t, 22, 150, ramp(t, t0, 0.3))
    for j in range(4):
        u = ((t - t0) * 0.9 + j / 4) % 1
        el_at(f, virus_el("ouch", (0, 1), int(t * 8) % 4), 540 + 160 * math.cos(u * 8 + j) * (1 - u), 1340 + 160 * u, 0.3 * (1 - 0.6 * u), op=1 - u)
    ui_word(f, "and just", "[WASH YOUR HANDS]", 380, t, t0, col=INKC, acc=ACC_S, size=96, lead_col=INKC)
    return finish(f, n, look="warm")


# ---- S9: 'Send this to whoever says no ice cream at every winter wedding.' the aunty, arms crossed, says no ... then sneaks a spoon of Chubby's ice cream ----
def shot_S9(t, n):
    f = set_wedding(t); tw = T("c2", "winter") - 0.1
    sneak = ramp(t, tw, 0.5)
    chub(f, 330, 1690, 1.55, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="smirk", brow="up", look=(1, 0), turn=0.5)
    stole(f, 330, 1690, 1.55, 0, 0)
    chub(f, 790, 1700, 1.5, t=t, shirt=(214, 96, 128), la=(120 - 60 * sneak, 150 - 140 * sneak), ra=(24, 12), hand_l="grip" if sneak > 0.5 else "open",
         hold_l=scale_el(spoon_el(), 0.4) if sneak > 0.5 else None, mouth=("o" if sneak > 0.5 else 2), expr=("happy" if sneak > 0.7 else "angry"),
         brow="sus", look=(-1, 0.3 * sneak), turn=-0.5, lean=-4 * sneak)
    dress(f, 790, 1700, 1.5, "aunty", -4 * sneak)
    wedding_front(f, 1330)
    el_at(f, icecream_cup_el("wow" if sneak > 0.3 else "happy", (0.7, -0.3)), 560, 1250, 0.9)
    ui_word(f, "send this to whoever says", "[NO ICE CREAM!]", 420, t, T("c2", "Send") - 0.05, col=INKC, acc=ACC_S, size=110, lead_col=INKC)
    return finish(f, n, look="warm")


# ---- S10: the logo beat (0.6 s) ----
def shot_S10(t, n):
    t0 = st_("S10"); f = set_wedding(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.25) * 0.95)
    comp(f, ed_el("follow for more food facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.12) / 0.2))
    return finish(f, n, look="warm")


# ---- S11: the LOOP TAIL: back at the counter exactly like frame 0 (no caption); loop_seam blends into frame 0 ----
def shot_S11(t, n):
    f = set_wedding(t)
    chubby_cold(f, t)
    wedding_front(f, 1330)
    el_at(f, icecream_cup_el("happy", (-0.6, -0.2), melt=0.25), 700, 1240, 0.95)
    el_at(f, cone_el("happy", (-0.8, 0)), 920, 1220, 0.75, rot=6)
    hook_band(f)
    return finish(f, n, look="warm")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i2", "no") - 0.1, 0.35, 14), (T("i2", "fine") - 0.1, 0.35, 12), (T("a1", "virus") - 0.15, 0.4, 14),
           (T("a1", "virus", 1) - 0.12 + 0.25, 0.3, 10), (T("a2", "sneeze") - 0.05, 0.4, 16), (T("a3", "hops") - 0.12, 0.25, 8),
           (T("b1", "wait") - 0.08, 0.35, 12), (T("b2", "soothe") - 0.12, 0.3, 10), (T("b3", "lollies") - 0.12, 0.3, 10), (T("c2", "winter") - 0.1, 0.25, 8)]


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
