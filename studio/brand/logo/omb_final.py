import sys, os
sys.path.insert(0, '/home/claude/studio/projects/pet-rock/comic'); os.chdir('/home/claude/studio/projects/pet-rock/comic')
import skia, numpy as np, cv2
from toon import R, paint, stroke
from comickit import dots, title, caption, KINK
OUT = '/home/claude/studio/projects/omb-logo/final'
NAVY, YEL, WHITE, CREAM = (24, 36, 92), (255, 200, 0), (255, 255, 255), (252, 241, 210)
def shade(c, k): return tuple(int(v * k) for v in c)
def badge(c, cx, cy, k=1.0, bc=NAVY, lc=YEL, xc=YEL, tc=YEL):
    c.save(); c.translate(cx, cy); c.scale(k, k)
    c.save(); c.rotate(-8)
    b = skia.RRect.MakeRectXY(R.MakeXYWH(-400, -260, 800, 520), 60, 60)
    c.save(); c.translate(18, 18); c.drawRRect(b, paint(KINK)); c.restore(); c.drawRRect(b, paint(bc))
    dots(c, (-400, -260, 800, 520), shade(bc, 1.45) if bc == NAVY else shade(bc, .78), cell=20, rmax=6, grad=(0.3, 1), a=0.55)
    c.drawRRect(b, stroke(KINK, 16)); c.restore()
    title(c, 'OMB', 0, 90, 300, lc, 1.0, 'c', shadow=14, rot=-8)
    title(c, '!', 330, -120, 200, xc, 1.0, 'c', shadow=8, rot=12)
    caption(c, 'OOPS MY BUSINESS', -282, 288, 1.0, col=tc, size=54, rot=-8)
    c.restore()
def save(s, name, alpha=True):
    a = np.ascontiguousarray(s.makeImageSnapshot().toarray()); cv2.imwrite(f'{OUT}/{name}', a if alpha else a[..., :3])
F = lambda n, z: skia.Font(skia.Typeface.MakeFromFile(f'/home/claude/studio/fonts/ttf/{n}'), z)
# 1 master badge, transparent
s = skia.Surface(1024, 1024); c = s.getCanvas(); c.clear(0); badge(c, 512, 500); save(s, 'omb_logo_badge.png')
# 2 profile picture (round-safe)
s = skia.Surface(1024, 1024); c = s.getCanvas(); c.clear(skia.Color(*YEL, 255)); badge(c, 512, 500, 0.92); save(s, 'omb_profile_picture.png', False)
# 3 horizontal lockup on white + on navy
for nm, bg, txt in (('omb_lockup_light.png', WHITE, NAVY), ('omb_lockup_dark.png', NAVY, WHITE)):
    s = skia.Surface(2000, 640); c = s.getCanvas(); c.clear(skia.Color(*bg, 255))
    badge(c, 330, 310, 0.62, bc=NAVY if bg == WHITE else YEL, lc=YEL if bg == WHITE else NAVY, xc=YEL if bg == WHITE else WHITE, tc=YEL if bg == WHITE else WHITE)
    f = F('Montserrat-Black.ttf', 128); x = 690
    c.drawString('Oops', x, 330, f, skia.Paint(Color=skia.Color(*(YEL if bg == WHITE else YEL)), AntiAlias=True))
    c.drawString('MyBusiness', x + f.measureText('Oops') + 6, 330, f, skia.Paint(Color=skia.Color(*txt), AntiAlias=True))
    c.drawString('BUSINESS STORIES  .  CASE STUDIES', x + 6, 410, F('Montserrat-SemiBold.ttf', 44), skia.Paint(Color=skia.Color(*(120, 126, 146) if bg == WHITE else (190, 196, 220)), AntiAlias=True))
    save(s, nm, False)
# board
b = np.full((1500, 2100, 3), (210, 241, 252), np.uint8)
def put(f, x, y, w, h):
    im = cv2.imread(f'{OUT}/{f}', cv2.IMREAD_UNCHANGED); im = cv2.resize(im, (w, h), interpolation=cv2.INTER_AREA)
    if im.shape[2] == 4:
        a = im[..., 3:4] / 255.; r = b[y:y+h, x:x+w]; r[:] = (r * (1 - a) + im[..., :3] * a).astype(np.uint8)
    else: b[y:y+h, x:x+w] = im[..., :3]
put('omb_logo_badge.png', 40, 40, 620, 620); put('omb_profile_picture.png', 720, 60, 580, 580)
cv2.circle(b, (2100 - 420, 350), 290, (210, 241, 252), -1)
pp = cv2.resize(cv2.imread(f'{OUT}/omb_profile_picture.png'), (560, 560)); m = np.zeros((560, 560), np.uint8); cv2.circle(m, (280, 280), 280, 255, -1)
r = b[70:630, 1400:1960]; r[m > 0] = pp[m > 0]
put('omb_lockup_light.png', 40, 720, 1000, 320); put('omb_lockup_dark.png', 1060, 720, 1000, 320)
put('omb_lockup_light.png', 40, 1080, 1000, 320)
cv2.imwrite(f'{OUT}/0_final_board.png', b[:1080]); print('ok')
