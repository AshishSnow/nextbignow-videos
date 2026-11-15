import cv2, numpy as np, skia
OUT = '/home/claude/studio/projects/omb-logo/final_slip'
SRC = '/home/claude/studio/projects/omb-logo/slip/omb_slip_B_black_yellow.png'
BLK, YEL, WHITE = (24, 24, 30), (255, 214, 0), (255, 255, 255)
badge = cv2.imread(SRC, cv2.IMREAD_UNCHANGED)          # BGRA? skia toarray = BGRA on this box; written directly
cv2.imwrite(f'{OUT}/omb_logo.png', badge)
def comp(bg, im, x, y, w):
    h = int(im.shape[0] * w / im.shape[1]); im = cv2.resize(im, (w, h), interpolation=cv2.INTER_AREA); a = im[..., 3:4] / 255.
    r = bg[y:y + h, x:x + w]; r[:] = (r * (1 - a) + im[..., :3] * a).astype(np.uint8)
bgr = lambda c: (c[2], c[1], c[0])
# profile picture: yellow square, badge centred (round-crop safe)
pp = np.full((1024, 1024, 3), bgr(YEL), np.uint8); comp(pp, badge, 92, 80, 840); cv2.imwrite(f'{OUT}/omb_profile_picture.png', pp)
# profile on black too
pk = np.full((1024, 1024, 3), bgr(BLK), np.uint8); comp(pk, badge, 92, 80, 840); cv2.imwrite(f'{OUT}/omb_profile_picture_black.png', pk)
# lockups via skia text
F = lambda n, z: skia.Font(skia.Typeface.MakeFromFile(f'/home/claude/studio/fonts/ttf/{n}'), z)
for nm, bgc, word, tag in (('omb_lockup_light', WHITE, BLK, (110, 110, 120)), ('omb_lockup_dark', (48, 48, 58), WHITE, (190, 190, 200))):
    s = skia.Surface(2000, 640); c = s.getCanvas(); c.clear(skia.Color(*bgc, 255))
    f = F('Montserrat-Black.ttf', 130); x = 700
    c.drawString('Oops', x, 330, f, skia.Paint(Color=skia.Color(*((230, 180, 0) if bgc == WHITE else YEL)), AntiAlias=True))
    c.drawString('MyBusiness', x + f.measureText('Oops') + 6, 330, f, skia.Paint(Color=skia.Color(*word), AntiAlias=True))
    c.drawString('BUSINESS STORIES  .  CASE STUDIES', x + 6, 410, F('Montserrat-SemiBold.ttf', 44), skia.Paint(Color=skia.Color(*tag), AntiAlias=True))
    im = np.ascontiguousarray(s.makeImageSnapshot().toarray()[..., :3]).copy()
    comp(im, badge, 20, 0, 640); cv2.imwrite(f'{OUT}/{nm}.png', im)
# favicon / small icon (512)
fi = cv2.resize(pp, (512, 512), interpolation=cv2.INTER_AREA); cv2.imwrite(f'{OUT}/omb_icon_512.png', fi)
# board
B = np.full((1300, 2100, 3), (210, 241, 252), np.uint8)
comp(B, badge, 40, 20, 620)
B[40:620, 720:1300] = cv2.resize(pp, (580, 580))
m = np.zeros((580, 580), np.uint8); cv2.circle(m, (290, 290), 290, 255, -1); r = B[40:620, 1440:2020]; pk2 = cv2.resize(pp, (580, 580)); r[m > 0] = pk2[m > 0]
B[680:980, 40:1040] = cv2.resize(cv2.imread(f'{OUT}/omb_lockup_light.png'), (1000, 300))
B[680:980, 1060:2060] = cv2.resize(cv2.imread(f'{OUT}/omb_lockup_dark.png'), (1000, 300))
cv2.imwrite(f'{OUT}/0_final_board.png', B[:1000]); print('ok')
