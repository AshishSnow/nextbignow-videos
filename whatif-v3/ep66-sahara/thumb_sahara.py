"""Painted thumbnail for ep66: big two-line title, one character (lone runner), one key prop (giant bat across the sun)."""
import os, sys, math
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sahara', 'full')]
import paint_sahara_full as S
import skia
W, H = 1080, 1920
ANTON = os.path.join(S.FX, 'Anton.ttf')


def big_text(c, s, y, size, fill, outline=(60, 18, 20), sh=0.55):
    f = S.F(ANTON, size); x = W / 2 - f.measureText(s) / 2
    b = S.P((0, 0, 0), sh); b.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14)); c.drawString(s, x + 8, y + 12, f, b)
    o = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=size * 0.09, StrokeJoin=skia.Paint.kRound_Join); o.setColor(S.col(outline))
    c.drawString(s, x, y, f, o); c.drawString(s, x, y, f, S.P(fill))


def big_bat(c, x, y, s, cc):
    """proper bat silhouette: ears, body, scalloped finger-wings."""
    c.save(); c.translate(x, y); c.scale(s, s)
    for sgn in (1, -1):
        p = skia.Path(); p.moveTo(0, -10)
        p.cubicTo(sgn * 40, -60, sgn * 120, -95, sgn * 210, -70)          # leading edge to wingtip
        p.lineTo(sgn * 200, -40)
        for (x1, x2, y2) in [(175, 150, 10), (125, 100, 25), (80, 55, 30)]:  # scalloped trailing edge
            p.quadTo(sgn * x1, -30 + y2 * .3, sgn * x2, y2)
            p.lineTo(sgn * (x2 - 5), y2 - 30)
        p.quadTo(sgn * 30, 20, 0, 30); p.close(); c.drawPath(p, S.P(cc))
        f = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3); f.setColor(S.col((70, 40, 60), .7))
        for (tx, ty) in [(200, -40), (150, 10), (100, 25), (55, 30)]: c.drawLine(sgn * 20, -20, sgn * tx, ty, f)
    c.drawOval(skia.Rect.MakeLTRB(-22, -45, 22, 45), S.P(cc))
    c.drawCircle(0, -52, 22, S.P(cc))
    for sgn in (1, -1):
        e = skia.Path(); e.moveTo(sgn * 8, -66); e.lineTo(sgn * 22, -96); e.lineTo(sgn * 20, -60); e.close(); c.drawPath(e, S.P(cc))
        c.drawCircle(sgn * 9, -54, 4, S.P((255, 200, 90)))
    c.restore()


def hiker(c, x, y, s, cc):
    """filled silhouette of a worn-out runner leaning forward, cap + backpack."""
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(8)
    pt = S.P(cc)
    st = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join); st.setColor(S.col(cc))
    st.setStrokeWidth(15); c.drawLine(0, -95, -18, -48, st); c.drawLine(-18, -48, -12, 0, st)    # back leg
    c.drawLine(0, -95, 20, -52, st); c.drawLine(20, -52, 26, 0, st)                                # front leg
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-16, -170, 18, -88), 14, 14), pt)          # torso
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-40, -168, -10, -110), 8, 8), pt)         # backpack
    st.setStrokeWidth(11); c.drawLine(10, -160, 24, -122, st); c.drawLine(24, -122, 30, -96, st)    # arm
    c.drawCircle(4, -190, 19, pt)                                                                    # head
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-14, -210, 34, -198), 5, 5), pt)          # cap brim
    c.drawLine(-8, -196, -26, -176, st)                                                              # neck flap
    c.restore()


def draw(c):
    S.vgrad(c, None, None, 0, H, [0, .35, .62, 1], [S.col((52, 30, 92)), S.col((180, 60, 90)), S.col((250, 140, 70)), S.col((255, 200, 120))])
    S.glow(c, W / 2, 1120, 900, (255, 190, 110), .55)
    c.drawCircle(W / 2, 1120, 300, S.P((255, 226, 160)))
    S.glow(c, W / 2, 1120, 420, (255, 245, 210), .5)
    S.fill_dune(c, S.dune(3, 1390, 160, 120), (205, 105, 70), (120, 50, 50), rim=(255, 200, 140), rim_a=.7)
    S.fill_dune(c, S.dune(7, 1640, 230, 520), (150, 62, 52), (60, 24, 32), rim=(255, 170, 110), rim_a=.8)
    big_bat(c, W / 2 + 10, 1040, 1.7, (28, 14, 26))              # key prop: giant bat across the sun
    for x, y, s, f in [(200, 900, 2.2, .3), (870, 880, 1.8, 2.0), (800, 950, 1.4, .9)]: S.bat(c, x, y, s, f, .9, (40, 18, 34))
    hiker(c, 270, 1388, 1.25, (30, 12, 18))                     # one character: lone runner on the crest
    sp = S.F(S.FD + 'Inter-Bold.otf', 46); s = 'HE ATE BATS TO SURVIVE'; x = W / 2 - 50 - sp.measureText(s) / 2
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - 30, 248, x + sp.measureText(s) + 30, 322), 37, 37), S.P((215, 38, 61)))
    c.drawString(s, x, 302, sp, S.P((255, 255, 255)))
    big_text(c, 'LOST IN THE', 540, 170, (255, 240, 210))
    big_text(c, 'SAHARA', 790, 270, (255, 214, 64))
    big_text(c, '9 DAYS', 1560, 150, (255, 240, 210), sh=.7)


surf = skia.Surface(W, H); c = surf.getCanvas(); draw(c); S.grain(c, .18); c.drawImage(S.WM, 0, 0)
out = os.path.join(S.D, 'thumb_sahara.png'); surf.makeImageSnapshot().save(out, skia.kPNG)
from PIL import Image
Image.open(out).convert('RGB').save(out.replace('.png', '.jpg'), quality=95); print(out)
