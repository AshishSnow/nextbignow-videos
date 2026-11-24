import sys, os, json, math
sys.path.insert(0, '/home/claude/voyager')
from kit import *
D = '/home/claude/voyager'
L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + 0.3; TOTAL = END + 1.6
def wt(i, frac): return S[i] + L[i]['dur'] * frac
def wfind(i, word):
    tx = L[i]['text'].lower(); k = tx.find(word.lower()); return wt(i, k / max(1, len(tx)))
def st(name, **kw):
    return load_st(name, **kw) if os.path.exists(f'{D}/st/{name}.png') else None
PHOTO = {}
def photo(name, w, h, focus=(.5, .5)):
    k = (name, w, h, focus)
    if k not in PHOTO:
        p = f'{D}/ph/{name}.jpg'
        PHOTO[k] = panel_img(comic_photo(p, w, h, focus)) if os.path.exists(p) else None
    return PHOTO[k]
exec(open(D + '/common_part.py').read())
def chip(fr, txt, cx, cy, t, col=CYAN, size=40, rot=0): tape(fr, txt, cx, cy, t, col=col, size=size, font=INTER, rot=rot)
def sk(fr, im, x, y, T, k, sc, rot=0, t=1.0):
    if im is not None: sticker(fr, im, x, y, T, k, sc, rot, t)
def stat(fr, big, small, cx, cy, t, col=RED, rot=-3, size=130):
    if t <= 0: return
    title(fr, big, cy, t, size=size, fill='FFFFFF' if col == RED else YEL, rot=rot, cx=cx)
    tape(fr, small, cx, cy + size * .8, t - .1, col=col, size=40, font=LUCKY, rot=rot + 1, tcol='FFFFFF' if col == RED else '1C1614')

sys.path.insert(0, '/home/claude/samples')
import essay as ES

def bg(fr, T, tint='F3E3B3', m=.55): fr[:] = paper(tint, m)
def essay_slide(T, lines, t0s, size=128):
    fr = ES.base(True); ES.headline(fr, lines, T, t0s, y=400, dark=True, size=size); return fr


def stars(c, T, n=70, seed=3):
    rng = np.random.default_rng(seed)
    for k in range(n):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(2, 6)
        a = .5 + .5 * math.sin(T * 3 + k)
        c.arc(x, y, r, 0, 6.29); c.set_source_rgba(1, 1, .9, .35 + .5 * a); c.fill()

def probe(c, x, y, s=1.0, rot=0, col='D9A43A', panels=True):
    c.save(); c.translate(x, y); c.rotate(math.radians(rot)); c.scale(s, s)
    if panels:
        for sx in (-1, 1):
            c.rectangle(sx * 70 - (150 if sx < 0 else 0), -28, 150, 56); c.set_source_rgba(*hx('2B4C8C')); c.fill_preserve(); ink(c, 6); c.stroke()
            for k in range(1, 5):
                xx = sx * 70 - (150 if sx < 0 else 0) + k * 30; c.move_to(xx, -28); c.line_to(xx, 28); c.set_source_rgba(1, 1, 1, .35); c.set_line_width(2); c.stroke()
    c.rectangle(-70, -60, 140, 120); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    c.move_to(-40, -60); c.line_to(-20, -95); c.line_to(20, -95); c.line_to(40, -60); c.set_source_rgba(*hx('BBBBBB')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.restore()

def earth(c, x, y, r):
    c.arc(x + 10, y + 12, r, 0, 6.29); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.arc(x, y, r, 0, 6.29); c.set_source_rgba(*hx('2D6CDF')); c.fill()
    for dx, dy, rr in ((-.3, -.2, .38), (.35, .25, .3), (.1, -.45, .2)):
        c.arc(x + dx * r, y + dy * r, rr * r, 0, 6.29); c.set_source_rgba(*hx('3FAE5A')); c.fill()
    c.arc(x, y, r, 0, 6.29); ink(c, 8); c.stroke()

def rock(fr, T, x, y, w, t=1.0, rot=0, bob=6):
    s_ = st('rock', w=w)
    if s_ is not None and t > 0: put_rgba(fr, s_, x, y + bob * math.sin(T * 1.7), back(clamp(t / .35)), 1.0, rot + 4 * math.sin(T * .6))

def space(fr, T, tint='1E2450', m=.88):
    bg(fr, T, tint, m); overlay(fr, cairo_layer(lambda c: stars(c, T)))


def voyager(c, x, y, s, T, rot=-12):
    if s < .01: return
    c.save(); c.translate(x, y); c.rotate(math.radians(rot)); c.scale(s, s)
    c.move_to(40, 20); c.line_to(330, 80); ink(c, 8); c.stroke()
    c.move_to(-40, 30); c.line_to(-260, 160); ink(c, 8); c.stroke()
    c.rectangle(-290, 150, 60, 40); c.set_source_rgba(*hx('C9CED6')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.move_to(-20, -30); c.line_to(-60, -260); ink(c, 5); c.stroke()
    c.rectangle(-70, 20, 140, 90); c.set_source_rgba(*hx('D9A43A')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(0, 75, 26, 0, 6.29); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 4); c.stroke()
    c.save(); c.scale(1, .32); c.arc(0, -60 / .32, 190, 0, 6.29); c.restore(); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    c.save(); c.scale(1, .32); c.arc(0, -60 / .32, 120, 0, 6.29); c.restore(); c.set_source_rgba(*hx('E6E9EE')); c.fill()
    c.move_to(0, -60); c.line_to(0, -130); ink(c, 6); c.stroke()
    c.restore()

def phone_msg(c, x, y, s, T, txt='HELLO?', sent=0.0):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-170 + 12, -300 + 14, 340, 600); c.set_source_rgba(0, 0, 0, .25); c.fill()
    c.rectangle(-170, -300, 340, 600); c.set_source_rgba(*hx('2B2B33')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.rectangle(-145, -260, 290, 520); c.set_source_rgba(*hx('F7F1E3')); c.fill()
    c.rectangle(-20, 60, 150, 70); c.set_source_rgba(*hx(CYAN)); c.fill_preserve(); ink(c, 4); c.stroke()
    c.select_font_face('Luckiest Guy'); c.set_font_size(36); c.set_source_rgba(*hx('1C1614')); e = c.text_extents(txt); c.move_to(55 - e.width / 2, 110); c.show_text(txt)
    c.select_font_face('Inter'); c.set_font_size(26); t2 = 'Arrives: tomorrow' if sent > 0 else 'Sending...'; e = c.text_extents(t2); c.move_to(130 - e.width, 170); c.show_text(t2)
    c.restore()

def beam(c, x0, y0, x1, y1, u, col=YEL):
    c.move_to(x0, y0); c.line_to(lerp(x0, x1, u), lerp(y0, y1, u)); c.set_source_rgba(*hx(col)); c.set_line_width(14); c.set_line_cap(1); c.stroke()
    c.arc(lerp(x0, x1, u), lerp(y0, y1, u), 24, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 5); c.stroke()

def record(c, x, y, s, T):
    if s < .01: return
    c.save(); c.translate(x, y); c.rotate(T * .8); c.scale(s, s)
    c.arc(12, 14, 220, 0, 6.29); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.arc(0, 0, 220, 0, 6.29); c.set_source_rgba(*hx('E3B341')); c.fill_preserve(); ink(c, 8); c.stroke()
    for r in range(60, 210, 22): c.arc(0, 0, r, 0, 6.29); c.set_source_rgba(*hx('B8860B', .6)); c.set_line_width(3); c.stroke()
    c.arc(0, 0, 50, 0, 6.29); c.set_source_rgba(*hx('F7E3A0')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.arc(0, 0, 10, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.restore()

def batt(c, x, y, s, lvl):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-190, -90, 380, 180); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 9); c.stroke()
    c.rectangle(190, -40, 40, 80); c.set_source_rgba(*hx('BBBBBB')); c.fill_preserve(); ink(c, 6); c.stroke()
    w = 350 * lvl; c.rectangle(-175, -75, w, 150); c.set_source_rgba(*hx(RED if lvl < .35 else GREEN)); c.fill()
    c.restore()

def waves(c, x, y, T, strength=1.0, n=4):
    for k in range(n):
        u = (T * .8 + k / n) % 1; r = 60 + 260 * u
        c.arc(x, y, r, -2.4, -.8); c.set_source_rgba(*hx(CYAN, (1 - u) * strength)); c.set_line_width(10); c.stroke()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    space(fr, T)
    t1 = wfind(0, 'tomorrow')
    def dr(c):
        phone_msg(c, 300, 1080, .85 * back(clamp((T + .4) / .4)), T, 'HI!', 1 if T > t1 else 0)
        voyager(c, 820, 820, .7, T)
        u = clamp((T - .6) / 3)
        c.move_to(420, 900); c.line_to(lerp(420, 760, u), lerp(900, 840, u)); c.set_source_rgba(*hx(YEL, .8)); c.set_line_width(8); c.set_dash([18, 14]); c.stroke(); c.set_dash([])
    overlay(fr, L_(dr))
    if T > t1: burst(fr, '24 HOURS', 800, 1250, T - t1, r=130, col=YEL, size=40, rot=8)
    tape(fr, 'VOYAGER 1', CX, 470, T + .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'ONE LIGHT-DAY AWAY', 600, T + .3, size=100, fill=YEL, rot=-2)

def s_lday(fr, T):
    fr[:] = essay_slide(T, [('A FULL', 'grey'), ('LIGHT-DAY AWAY.', 'hl')], [S[1], wfind(1, 'light')], size=124)
    overlay(fr, L_(lambda c: (earth(c, 200, 1180, 80), voyager(c, 880, 1120, .35, T), beam(c, 280, 1170, 820, 1130, clamp((T - S[1]) / 2.3)))))
    chip(fr, 'NOV 18, 2026', CX, 1350, T - S[1] - .3, YEL, 36, -2)

def s_launch(fr, T):
    lt = T - S[2]; bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    tape(fr, 'BORN 1977', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    def dr(c):
        u = eout(clamp(lt / 3)); x = lerp(250, 760, u); y = lerp(1300, 820, u)
        c.move_to(250, 1300); c.line_to(x, y); c.set_source_rgba(*hx(RED)); c.set_line_width(10); c.set_dash([24, 14]); c.stroke(); c.set_dash([])
        earth(c, 230, 1320, 110)
        voyager(c, x, y, .6, T, -20)
    overlay(fr, L_(dr))
    if T > wfind(2, 'never'): title(fr, 'NEVER STOPPED', 600, T - wfind(2, 'never'), size=110, fill=YEL)

def s_speed(fr, T):
    lt = T - S[3]; space(fr, T)
    tape(fr, 'FAST AND FAR', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def dr(c):
        for k in range(8):
            u = (T * 1.5 + k / 8) % 1; y = 800 + k * 70
            c.move_to(1100 - 1300 * u, y); c.line_to(1180 - 1300 * u, y); c.set_source_rgba(1, 1, 1, .5); c.set_line_width(5); c.stroke()
        voyager(c, CX + 20 * math.sin(T * 2), 1050, .9 * back(clamp(lt / .35)), T)
    overlay(fr, L_(dr))
    title(fr, '38,000 MPH', 640, lt - .2, size=120, fill=YEL)
    if T > wfind(3, 'sixteen'): chip(fr, '16.1 BILLION MILES', CX, 1330, T - wfind(3, 'sixteen'), YEL, 40, 2)

def s_light(fr, T):
    lt = T - S[4]; space(fr, T, '2A1E50')
    tape(fr, 'EVEN LIGHT', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    u = clamp(lt / 4.5)
    def dr(c):
        earth(c, 170, 1220, 100); voyager(c, 900, 820, .45, T)
        beam(c, 250, 1170, 840, 860, u)
        c.select_font_face('Luckiest Guy'); c.set_font_size(110); h = int(24 * u)
        txt = f'{h} HRS'; e = c.text_extents(txt); c.set_source_rgba(1, 1, 1, 1); c.move_to(CX - e.width / 2, 1150); c.show_text(txt)
    overlay(fr, L_(dr))
    if T > wfind(4, 'twenty'): title(fr, '24 HOURS', 620, T - wfind(4, 'twenty'), size=120, fill=YEL)

def s_ask(fr, T):
    fr[:] = essay_slide(T, [('ASK A QUESTION,', 'grey'), ('WAIT 2 DAYS.', 'hl')], [S[5], wfind(5, 'two')], size=124)
    overlay(fr, L_(lambda c: (phone_msg(c, 330, 1150, .55, T, '?', 0), voyager(c, 800, 1100, .4, T))))

def s_batt(fr, T):
    lt = T - S[6]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'RUNNING LOW', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: batt(c, CX, 1020, 1.4 * back(clamp(lt / .35)) + .01, .55 - .3 * clamp(lt / 3.5))))
    if T > wfind(6, 'nuclear'): chip(fr, 'NUCLEAR POWER SOURCE', CX, 760, T - wfind(6, 'nuclear'), 'FFFFFF', 36, -2)
    if T > wfind(6, 'watts'): title(fr, '-4 WATTS A YEAR', 620, T - wfind(6, 'watts'), size=100, fill=YEL)

def s_signal(fr, T):
    lt = T - S[7]; space(fr, T)
    tape(fr, 'SINCE NOV 14', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    overlay(fr, L_(lambda c: (voyager(c, CX, 1080, .85, T), waves(c, CX, 1000, T, .5))))
    if T > wfind(7, 'basic'): chip(fr, 'BASIC CARRIER SIGNAL', CX, 750, T - wfind(7, 'basic'), CYAN, 36, -2)
    if T > wfind(7, 'no data'): title(fr, 'NO DATA', 620, T - wfind(7, 'no data'), size=130, fill=YEL); xstamp(fr, 820, 1260, T - wfind(7, 'no data'), .7)

def s_silent(fr, T):
    fr[:] = essay_slide(T, [('ONE DAY', 'grey'), ('IT GOES SILENT.', 'hl')], [S[8], wfind(8, 'silent')], size=124)
    lt = T - S[8]
    overlay(fr, L_(lambda c: (voyager(c, CX, 1180, .6, T), waves(c, CX, 1110, T, max(0, 1 - lt / 5)))))
    chip(fr, 'NASA LISTENS DAILY', CX, 900, lt - .3, YEL, 34, -2)

def s_end(fr, T):
    lt = T - S[9]; space(fr, T)
    tape(fr, 'THE GOLDEN RECORD', CX, 470, lt, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (record(c, CX, 1000, 1.2 * back(clamp(lt / .35)), T), voyager(c, 830, 1300, .4, T))))
    if T > wfind(9, 'tomorrow') - .4: title(fr, 'ARRIVES TOMORROW', 620, T - wfind(9, 'tomorrow') + .4, size=100, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_lday), (S[3], s_launch), (S[4], s_speed), (S[5], s_light), (S[6], s_ask), (S[7], s_batt), (S[8], s_signal), (S[9], s_silent), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'tomorrow'), wfind(4, 'twenty'), wfind(7, 'no data')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Source: NASA/JPL (Nov 2026)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
