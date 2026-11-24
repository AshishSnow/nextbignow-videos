import sys; sys.argv = ['x']; exec(open('/home/claude/fart/scenes.py').read().split("if __name__")[0])
fr = radial_bg('E8F5B0', '4E7A1A', CX, 1300); rays(fr, 0.4, 'FFFFFF', .16, CX, 1300); vignette(fr, .4)
overlay(fr, cairo_layer(lambda c: (cloud(c, 560, 1380, 2.2, 0.3), wavy(c, 560, 1100, 1.6, 0.3, 4), egg(c, 230, 1700, 1.0, True), food(c, 'broc', 880, 1700, 1.4, 0))))
def face(c):
    for ex in (470, 650):
        c.arc(ex, 1350, 34, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 6); c.stroke()
        c.arc(ex + 8, 1356, 14, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.move_to(470, 1460); c.curve_to(520, 1420, 600, 1500, 650, 1450); ink(c, 10); c.stroke()
overlay(fr, cairo_layer(face))
burst(fr, 'SULFUR!', 850, 1150, 1.0, r=150, col=YEL, size=50, rot=10)
tape(fr, '~20 TIMES A DAY', 420, 330, 1.0, col=RED, size=54, font=LUCKY, rot=-3, tcol='FFFFFF')
big_word(fr, 'WHY FARTS', 520, 180, 'FFFFFF', -3)
big_word(fr, 'STINK?!', 730, 200, YEL, -3)
logo(fr); Image.fromarray(fr).save('/home/claude/fart/out/thumb_fart.jpg', quality=95)
