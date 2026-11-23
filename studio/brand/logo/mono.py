import sys, os
sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_logos import *
OUT = os.path.dirname(os.path.abspath(__file__))
CRE = CREAM_T


def b_mono(dark=True):   # O + square full stop, monochrome
    s, c = surf(1080, 1080); grain(c, 1080, 1080, DARK if dark else CREAM, 3)
    fg = CRE if dark else INKE
    f = anton(640); c.drawString('O', 300, 820, f, P(fg)); ow = f.measureText('O')
    c.drawRect(skia.Rect.MakeXYWH(300 + ow + 30, 690, 130, 130), P(fg))
    return s


def a_mono():
    s, c = surf(1080, 1080); grain(c, 1080, 1080, CREAM)
    f = anton(400); t = 'OOPS'; c.drawString(t, 540 - f.measureText(t) / 2, 600, f, P(INKE))
    c.drawRect(skia.Rect.MakeXYWH(170, 650, 740, 170), P(DARK)); tracked(c, 'MY BUSINESS', 540, 765, 84, CRE, 10, 'Bold')
    return s


def wm_mono(dark=True):
    s, c = surf(2000, 600); grain(c, 2000, 600, DARK if dark else CREAM, 3)
    fg = CRE if dark else INKE
    f = anton(330); t = 'OOPS'; c.drawString(t, 130, 440, f, P(fg)); x = 130 + f.measureText(t) + 26
    c.drawRect(skia.Rect.MakeXYWH(x, 370, 74, 74), P(fg))
    tracked(c, 'MY BUSINESS', x + 120, 440, 64, fg, 14, 'Bold', center=False)
    tracked(c, 'BUSINESS, EXPLAINED.', x + 120, 360, 30, MUTE, 8, 'Medium', center=False)
    return s


def mock_reel(acc_, logo_img):
    """a mini reel cover in the essay look with the mono logo bug in the corner."""
    s, c = surf(540, 960); grain(c, 540, 960, CREAM)
    for x in (75, 209, 343, 465): c.drawLine(x, 0, x, 960, S(acc_, 1.2, 0.4))
    f = anton(64); c.drawString('ANY TOPIC', 60, 300, f, P(INKE))
    w = f.measureText('IN COLOUR'); c.drawRect(skia.Rect.MakeXYWH(54, 318, w + 16, 70), P(acc_)); c.drawString('IN COLOUR', 62, 378, f, P(CRE))
    c.drawRect(skia.Rect.MakeXYWH(0, 640, 540, 320), P(acc_))
    c.drawImageRect(circle_preview(logo_img, 110), skia.Rect.MakeXYWH(400, 30, 110, 110), skia.SamplingOptions())
    return s.makeImageSnapshot()


if __name__ == '__main__':
    b_mono(True).makeImageSnapshot().save(os.path.join(OUT, 'logo_final_avatar_dark.png'), skia.kPNG)
    b_mono(False).makeImageSnapshot().save(os.path.join(OUT, 'logo_final_avatar_light.png'), skia.kPNG)
    wm_mono(True).makeImageSnapshot().save(os.path.join(OUT, 'logo_final_wordmark_dark.png'), skia.kPNG)
    wm_mono(False).makeImageSnapshot().save(os.path.join(OUT, 'logo_final_wordmark_light.png'), skia.kPNG)
    a_mono().makeImageSnapshot().save(os.path.join(OUT, 'logo_A_mono_avatar.png'), skia.kPNG)
    SW, SH = 2400, 2500
    s, c = surf(SW, SH); grain(c, SW, SH, (226, 220, 208))
    c.drawString('ONE LOGO. EVERY COLOUR.', 120, 200, anton(110), P(INKE))
    tracked(c, 'BLACK + CREAM LOGO STAYS THE SAME. THE REEL ACCENT CHANGES.', 120, 270, 34, INKE, 6, 'Medium', center=False)
    av = b_mono(True).makeImageSnapshot()
    c.drawImage(circle_preview(av, 420), 120, 340); c.drawImage(circle_preview(b_mono(False).makeImageSnapshot(), 420), 600, 340)
    c.drawImageRect(wm_mono(True).makeImageSnapshot(), skia.Rect.MakeXYWH(1080, 360, 1200, 360), skia.SamplingOptions(skia.FilterMode.kLinear))
    c.drawImageRect(wm_mono(False).makeImageSnapshot(), skia.Rect.MakeXYWH(1080, 740, 1200, 360), skia.SamplingOptions(skia.FilterMode.kLinear))
    accs = [(138, 66, 214), (214, 52, 44), (34, 140, 92), (226, 80, 150), (36, 98, 214)]
    for i, ac in enumerate(accs):
        c.drawImageRect(mock_reel(ac, av), skia.Rect.MakeXYWH(120 + i * 440, 1260, 400, 711), skia.SamplingOptions(skia.FilterMode.kLinear))
    tracked(c, 'PURPLE   ·   RED   ·   GREEN   ·   PINK   ·   BLUE', SW / 2, 2080, 40, INKE, 8, 'SemiBold')
    s.makeImageSnapshot().save(os.path.join(OUT, 'logo_final_sheet.png'), skia.kPNG); print('ok')
