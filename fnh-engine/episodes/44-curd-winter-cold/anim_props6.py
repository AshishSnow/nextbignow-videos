# ================= anim_props6.py = lib44 (ep 44, 16 Nov): "Does eating curd in winter give you a cold?" — ACCENT = winter ICE BLUE (the cold, the
# question, frost, the chips). METAPHOR: a POLICE LINEUP. Curd (a steel katori of dahi with a nervous face) is the usual suspect every winter; Detective
# Chubby (fedora + magnifier) turns the lamp on a SILHOUETTE at the end of the line and finds the real culprit: the cold VIRUS (olive-green, knobbed).
# New place: set_lineup(t, dim) = the lineup room (slate wall with height lines, a strip light, a dark floor), lineup_front() = the floor edge + slot marks.
# New ink props: curd_el(mood, look, frost, empty), virus_el(mood, look, ph), card_el(n) (lineup placard), fedora(f, ...) (draws a hat on chub's head),
# soap_foam(f, ...) (hand-wash suds), sneeze_spray(f, ...) (droplets that carry mini viruses). =================
ACC = (92, 156, 214); ACC_S = (40, 92, 150); ACC_L = (196, 226, 248); ACC_XL = (232, 244, 252)      # ice blue = winter / the cold / the question
CURD = (252, 250, 240); CURD_S = (226, 220, 200)
STEEL = (206, 212, 218); STEEL_S = (150, 158, 168); STEEL_H = (244, 248, 252)
VIR = (150, 172, 72); VIR_S = (92, 118, 40); VIR_K = (214, 120, 80)                                # the virus: olive green + rust knobs
HAT = (124, 94, 66); HAT_S = (86, 62, 44)
WALL = (128, 140, 158)
SRC_VIR = "Source: CDC; Mayo Clinic; BBC Science Focus"
SRC_CURD = "Source: The Week fact check (2026); The South First"
SRC_WINTER = "Source: Mayo Clinic; BBC Science Focus"
SC3 = 3


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


# ---------------- props (ink language: one warm-ink wobbly outline, flat fill, shade + hatch on the shadow side) ----------------
def curd_el(mood="n", look=(0, 0), frost=0.0, empty=False, seed=441):
    """a steel KATORI of dahi: a white curd dome above the rim, a face on the steel bowl. frost 0..1 = fridge-cold (pale blue + frost specks)."""
    fk = round(clamp(frost) * 4) / 4
    def mk():
        w, h = 320, 260; im, d, S = _cv(w, h)
        body = _arcpts(160, 112, 132, 120, 0, 180, 30)                                   # bowl: a half-ellipse under the rim
        _ink_poly(d, body, STEEL, seed, INK_W, amp=1.2)
        _shade(im, lambda q, S_: q.polygon(_P(body), fill=255), lambda q, S_, c: q.ellipse(S_(170, 60, 340, 300), fill=c), STEEL_S, 120)
        _hatch_in(im, (190, 120, 300, 230), lambda q, S_: q.polygon(_P(body), fill=255), -40, 10, 30)
        d.arc(S(60, 60, 150, 220), 120, 200, fill=STEEL_H + (230,), width=7 * SC3)        # steel shine
        if not empty:
            dome = _arcpts(160, 112, 122, 46, 180, 360, 26)
            _ink_poly(d, dome, CURD, seed + 1, INK_W - 1, amp=1.0)
            d.arc(S(80, 74, 200, 130), 200, 260, fill=(255, 255, 255, 255), width=6 * SC3)
            d.ellipse(S(196, 84, 230, 100), fill=CURD_S + (200,))
        _ink_ell(d, 160, 112, 134, 18, None, seed + 2, INK_W - 1, amp=0.8)               # the rim
        _face(d, S, 160, 170, 1.45, mood, look)
        if fk > 0:
            ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); q = ImageDraw.Draw(ov)
            q.polygon(_P(body), fill=ACC_L + (int(110 * fk),))
            r = np.random.default_rng(seed)
            for j in range(int(26 * fk)):
                x, y = r.uniform(50, 270), r.uniform(118, 220)
                q.line(_P([(x - 5, y), (x + 5, y)]), fill=(255, 255, 255, 230), width=2 * SC3); q.line(_P([(x, y - 5), (x, y + 5)]), fill=(255, 255, 255, 230), width=2 * SC3)
            im.alpha_composite(ov)
        return _done(im, w, h)
    return gcache(("curd44", mood, look, fk, empty, seed), mk)


def virus_el(mood="sly", look=(0, 0), ph=0, seed=442):
    """THE COLD VIRUS (a rhinovirus as a cartoon): a round olive body ringed with short stalks that end in rust knobs, a sly face. ph = knob wiggle frame."""
    ph = int(ph) % 4
    def mk():
        w, h = 300, 300; im, d, S = _cv(w, h); cx = cy = 150; R = 92
        for i in range(14):                                                               # stalks + knobs behind the body edge
            a = i / 14 * 2 * math.pi + 0.08 * math.sin(ph * 1.6 + i)
            x0, y0 = cx + (R - 10) * math.cos(a), cy + (R - 10) * math.sin(a); x1, y1 = cx + (R + 30) * math.cos(a), cy + (R + 30) * math.sin(a)
            d.line(S(x0, y0, x1, y1), fill=INKC + (255,), width=7 * SC3)
            _ink_ell(d, x1, y1, 13, 13, VIR_K, seed + i, 4, n=14, amp=0.6)
        _ink_ell(d, cx, cy, R, R, VIR, seed, INK_W, n=36, amp=1.6)
        _shade(im, lambda q, S_: q.ellipse(S_(cx - R, cy - R, cx + R, cy + R), fill=255), lambda q, S_, c: q.ellipse(S_(cx - 40, cy - 30, cx + 170, cy + 170), fill=c), VIR_S, 120)
        _hatch_in(im, (cx, cy, cx + R, cy + R), lambda q, S_: q.ellipse(S_(cx - R, cy - R, cx + R, cy + R), fill=255), -40, 10, 34)
        for (dx, dy, r) in ((-40, -46, 10), (30, -54, 7), (52, 20, 9), (-56, 30, 7)):    # facets (an icosahedral virus, simplified)
            d.ellipse(S(cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r), fill=VIR_S + (150,))
        d.ellipse(S(cx - 62, cy - 70, cx - 36, cy - 52), fill=(255, 255, 255, 150))
        _face(d, S, cx, cy + 10, 2.0, mood, look)
        return _done(im, w, h)
    return gcache(("virus44", mood, look, ph, seed), mk)


def card_el(n=1, seed=443):
    """a lineup placard: a white board with the suspect number."""
    def mk():
        w, h = 200, 150; im, d, S = _cv(w, h)
        _ink_poly(d, [(16, 20), (184, 16), (186, 132), (14, 136)], (250, 248, 240), seed, INK_W - 1)
        fnt = ImageFont.truetype(F_HAND, 92 * SC3); tx = str(n); tw = d.textlength(tx, font=fnt)
        d.text((100 * SC3 - tw / 2, 18 * SC3), tx, font=fnt, fill=INKC + (255,))
        return _done(im, w, h)
    return gcache(("card44", n, seed), mk)


def fedora(f, x, y, s, lean=0.0, tip=0.0):
    """Detective Chubby's FEDORA over chub(f, x, y, s, ...) (head centre ~ (x + lean*2*s, y - 420*s)); tip 0..1 = he tips it (lifts + tilts)."""
    hx, hy = x + lean * 2 * s, y - 420 * s - 70 * s - 26 * s * tip
    ang = math.radians(-14 * tip)
    def R(px, py): return (int(hx + px * s * math.cos(ang) - py * s * math.sin(ang)), int(hy + px * s * math.sin(ang) + py * s * math.cos(ang)))
    crown = np.array([R(-78, -8), R(-66, -96), R(-20, -110), R(0, -96), R(20, -110), R(66, -96), R(78, -8)], np.int32)
    brim = np.array([R(-150 + 8 * math.cos(a), 0 + 22 * math.sin(a)) if False else R(150 * math.cos(a), 22 * math.sin(a) - 4) for a in np.linspace(0, 2 * math.pi, 36)], np.int32)
    cv2.fillPoly(f, [brim], C(HAT_S), cv2.LINE_AA); cv2.polylines(f, [brim], True, C(INKC), max(2, int(5 * s)), cv2.LINE_AA)
    cv2.fillPoly(f, [crown], C(HAT), cv2.LINE_AA); cv2.polylines(f, [crown], True, C(INKC), max(2, int(5 * s)), cv2.LINE_AA)
    band = np.array([R(-76, -10), R(-74, -34), R(74, -34), R(76, -10)], np.int32)
    cv2.fillPoly(f, [band], C((60, 44, 34)), cv2.LINE_AA)


def soap_foam(f, cx, cy, t, n=16, rad=110, k=1.0, seed=7):
    """hand-wash suds: white bubbles that jiggle around (cx, cy); k 0..1 = how much foam."""
    r = np.random.default_rng(seed)
    for j in range(int(n * k)):
        a = r.uniform(0, 2 * math.pi); d_ = r.uniform(0.2, 1) * rad
        x = cx + d_ * math.cos(a) + 6 * math.sin(t * 7 + j); y = cy + d_ * 0.6 * math.sin(a) + 5 * math.cos(t * 6 + j * 1.3)
        rr = int(r.uniform(10, 26))
        cv2.circle(f, (int(x), int(y)), rr, C((252, 252, 255)), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), rr, C((150, 180, 210)), 3, cv2.LINE_AA)
        cv2.circle(f, (int(x - rr * 0.35), int(y - rr * 0.35)), max(2, rr // 4), C((255, 255, 255)), -1, cv2.LINE_AA)


def sneeze_spray(f, x, y, t, t0, dirx=1, n=26, spd=760, seed=3, mini=True):
    """a SNEEZE: a cone of droplets from (x, y) that slow down and fall; every 4th droplet carries a tiny virus."""
    if t < t0: return
    u = t - t0
    r = np.random.default_rng(seed)
    for j in range(n):
        a = r.uniform(-0.45, 0.35); v = spd * r.uniform(0.5, 1.0); dl = r.uniform(0, 0.12)
        if u < dl: continue
        uu = u - dl; dist = v * (1 - math.exp(-2.6 * uu)) / 2.6
        px = x + dirx * dist * math.cos(a); py = y + dist * math.sin(a) + 260 * uu * uu
        op = clamp(1.6 - uu / 1.2)
        if op <= 0: continue
        if mini and j % 4 == 0:
            el_at_ = scale_el(virus_el("sly", (dirx, 0), int(t * 8) % 4), 0.28)
            rot_comp(f, el_at_, px, py, 20 * math.sin(t * 5 + j), 1.0, op, 0.0)
        else:
            rr = int(r.uniform(5, 11))
            cv2.circle(f, (int(px), int(py)), rr, C((214, 234, 248)), -1, cv2.LINE_AA); cv2.circle(f, (int(px), int(py)), rr, C(ACC_S), 2, cv2.LINE_AA)


# ---------------- the LINEUP ROOM (new place) ----------------
LINE_FLOOR = 1480


def set_lineup(t=0.0, dim=0.0, blur=3):
    """THE LINEUP ROOM: a slate-blue wall with white height lines + numbers, a strip light across the top (its glow pools on the wall), a dark
    floor from LINE_FLOOR. dim 0..1 = lights down (for the silhouette beat); paper-softened (ink look)."""
    def mk():
        f = _vgrad((150, 162, 180), WALL, 0, LINE_FLOOR)
        for i, yy in enumerate(range(620, LINE_FLOOR, 60)):
            th = 5 if i % 2 == 0 else 2
            cv2.line(f, (60, yy), (1020, yy), C((236, 240, 246)), th, cv2.LINE_AA)
        tl = np.zeros((H, W), np.uint8)
        for i, yy in enumerate(range(620, LINE_FLOOR, 120)):
            v = 210 - i * 10
            cv2.putText(tl, str(v), (78, yy - 12), cv2.FONT_HERSHEY_SIMPLEX, 1.3, 255, 3, cv2.LINE_AA)
            cv2.putText(tl, str(v), (930, yy - 12), cv2.FONT_HERSHEY_SIMPLEX, 1.3, 255, 3, cv2.LINE_AA)
        m = (tl.astype(np.float32) / 255)[..., None]
        f = f * (1 - m) + np.array(C((236, 240, 246)), np.float32) * m
        cv2.rectangle(f, (0, LINE_FLOOR), (W, H), C((70, 74, 88)), -1)
        cv2.line(f, (0, LINE_FLOOR), (W, LINE_FLOOR), C((48, 50, 62)), 8, cv2.LINE_AA)
        for x in (330, 750):                                                              # slot marks on the floor
            cv2.ellipse(f, (x, LINE_FLOOR + 40), (150, 26), 0, 0, 360, C((96, 100, 116)), 5, cv2.LINE_AA)
        cv2.rectangle(f, (40, 250), (1040, 286), C((60, 62, 74)), -1, cv2.LINE_AA)        # the strip light housing
        cv2.rectangle(f, (60, 276), (1020, 296), C((252, 248, 230)), -1, cv2.LINE_AA)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("set_lineup44", blur), mk).copy()
    glow(f, 540, 330, 520, (255, 246, 220), 0.32 * (1 - dim))
    if dim > 0:
        f *= (1 - 0.72 * dim)
    f = inkify(f)
    return f


def lamp_pool(f, x, y, r=260, amt=0.55, col=(255, 240, 200)):
    """a downlight pool on the lineup wall (a cone of light from the top)."""
    g = np.zeros((H, W), np.float32)
    cv2.ellipse(g, (int(x), int(y)), (int(r), int(r * 1.9)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
    g = cv2.GaussianBlur(g, (0, 0), r * 0.35)[..., None]
    f[:] = f + g * amt * (np.array(C(col), np.float32) - f * 0.6)


def suspect(f, el, x, s, t, num=None, bob=True, legs_=True, sweat=0.0, op=1.0):
    """a suspect standing in the lineup: ink legs + the body element + an optional placard held at the front."""
    y = LINE_FLOOR + 10
    if legs_: legs(f, x, y - 70 * s, s)
    by = y - 70 * s - 118 * s + (3 * math.sin(t * 2.3) if bob else 0)
    rot_comp(f, scale_el(el, s), x, by, 2 * math.sin(t * 1.7), 1.0, op, 0.0)
    if num is not None: el_at(f, card_el(num), x, by + 90 * s, 0.62 * s)
    if sweat > 0:
        for j in range(2):
            u = ((t * 0.9 + j * 0.5) % 1)
            cv2.ellipse(f, (int(x + (70 + 20 * j) * s), int(by - 60 * s + 80 * u)), (int(7 * s), int(11 * s)), 0, 0, 360, C((200, 228, 250)), -1, cv2.LINE_AA)
            cv2.ellipse(f, (int(x + (70 + 20 * j) * s), int(by - 60 * s + 80 * u)), (int(7 * s), int(11 * s)), 0, 0, 360, C(ACC_S), 2, cv2.LINE_AA)
    return by
