
# ---------------------------------------------------------------- tea / teeth props
def tooth(c, x, y, s, T, mood='happy', stains=0.0, sweat=0.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    def shape():
        c.new_path(); c.move_to(-150, -120); c.curve_to(-150, -230, -40, -220, 0, -175); c.curve_to(40, -220, 150, -230, 150, -120)
        c.curve_to(150, -20, 120, 40, 110, 120); c.curve_to(100, 230, 40, 240, 25, 140); c.curve_to(15, 90, -15, 90, -25, 140)
        c.curve_to(-40, 240, -100, 230, -110, 120); c.curve_to(-120, 40, -150, -20, -150, -120); c.close_path()
    c.save(); c.translate(14, 16); shape(); c.set_source_rgba(*hx('1C1614')); c.fill(); c.restore()
    shape(); c.set_source_rgba(*hx('FFFFFF')); c.fill_preserve(); ink(c, 9); c.stroke()
    c.save(); shape(); c.clip()
    c.arc(-70, -150, 40, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill()
    c.move_to(110, -150); c.curve_to(130, -60, 110, 20, 95, 100); c.set_source_rgba(*hx('DDE6EE')); c.set_line_width(34); c.stroke()
    if stains > 0:
        for k, (sx, sy, r) in enumerate(((-80, -40, 40), (50, -90, 34), (20, 30, 46), (-60, 70, 30), (90, 10, 26))):
            c.arc(sx, sy, r * stains, 0, 2 * math.pi); c.set_source_rgba(*hx('A0642A', .75)); c.fill()
    c.restore()
    for ex in (-50, 50):
        if mood == 'shock': c.arc(ex, -70, 18, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
        else: c.save(); c.translate(ex, -70); c.scale(1, 1.3); c.arc(0, 0, 12, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(-85, -30, 18, 0, 2 * math.pi); c.arc(85, -30, 18, 0, 2 * math.pi); c.set_source_rgba(*hx('FF7AA8', .5)); c.fill()
    if mood == 'happy': c.arc(0, -40, 34, .2, math.pi - .2); ink(c, 8); c.stroke()
    elif mood == 'shock': c.save(); c.translate(0, -20); c.scale(1, 1.3); c.arc(0, 0, 22, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('B33A3A')); c.fill_preserve(); ink(c, 6); c.stroke()
    else: c.move_to(-30, -15); c.curve_to(-10, -35, 10, -35, 30, -15); ink(c, 8); c.stroke()
    if sweat > 0:
        c.move_to(140, -170); c.curve_to(120, -130, 125, -110, 145, -110); c.curve_to(165, -110, 165, -130, 140, -170); c.set_source_rgba(*hx('9FD8FF')); c.fill_preserve(); ink(c, 4); c.stroke()
    c.restore()

def wglass(c, x, y, s, T, fill=.75, col='9FD8FF', ice=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-120 + 14, -180 + 16); c.line_to(120 + 14, -180 + 16); c.line_to(95 + 14, 180 + 16); c.line_to(-95 + 14, 180 + 16); c.close_path(); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.move_to(-120, -180); c.line_to(120, -180); c.line_to(95, 180); c.line_to(-95, 180); c.close_path(); c.set_source_rgba(*hx('EAF6FF', .9)); c.fill_preserve(); ink(c, 8); c.stroke()
    top = 180 - 360 * fill; wob = 8 * math.sin(T * 3)
    c.move_to(-120 + 25 * (1 - fill), top + wob); c.curve_to(-40, top - 10, 40, top + 10, 120 - 25 * (1 - fill), top - wob); c.line_to(95, 178); c.line_to(-95, 178); c.close_path()
    c.set_source_rgba(*hx(col)); c.fill()
    c.rectangle(-80, -150, 20, 290); c.set_source_rgba(1, 1, 1, .5); c.fill()
    if ice:
        for k, (ix, iy) in enumerate(((-40, top + 20), (35, top + 10), (0, top + 70))):
            c.save(); c.translate(ix, iy); c.rotate(.3 * k); c.rectangle(-36, -36, 72, 72); c.set_source_rgba(*hx('FFFFFF', .8)); c.fill_preserve(); ink(c, 4); c.stroke(); c.restore()
    c.restore()

def bubble(c, x, y, w, h, tail=(-1, 1)):
    c.save(); c.translate(x, y)
    def sh():
        c.new_path(); c.save(); c.scale(w / 2, h / 2); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.move_to(tail[0] * w * .15, h * .4); c.line_to(tail[0] * w * .38, h * .78); c.line_to(tail[0] * w * .02, h * .45)
    c.save(); c.translate(14, 16); sh(); c.set_source_rgba(*hx('1C1614')); c.fill(); c.restore()
    sh(); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    c.restore()

def granny(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-170, 240); c.curve_to(-170, 30, 170, 30, 170, 240); c.close_path(); c.set_source_rgba(*hx('E63946')); c.fill_preserve(); ink(c); c.stroke()
    c.arc(0, -80, 110, 0, 2 * math.pi); c.set_source_rgba(*hx('C9C9C9')); c.fill_preserve(); ink(c); c.stroke()
    c.arc(0, -60, 95, 0, 2 * math.pi); c.set_source_rgba(*hx('E8A87C')); c.fill_preserve(); ink(c); c.stroke()
    c.arc(0, -175, 45, 0, 2 * math.pi); c.set_source_rgba(*hx('C9C9C9')); c.fill_preserve(); ink(c, 6); c.stroke()
    for ex in (-35, 35):
        c.arc(ex, -70, 26, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, .6); c.fill_preserve(); ink(c, 5); c.stroke()
        c.arc(ex, -70, 7, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.move_to(-9, -70); c.line_to(9, -70); ink(c, 5); c.stroke()
    c.save(); c.translate(0, -15); c.scale(1, .7); c.arc(0, 0, 22, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('B33A3A')); c.fill()
    c.arc(0, -40, 6, 0, 2 * math.pi); c.set_source_rgba(*hx('E63946')); c.fill()   # bindi
    c.move_to(140, 120); c.line_to(220 + 10 * math.sin(T * 12), -60); ink(c, 20); c.stroke()   # wagging finger arm
    c.arc(225 + 10 * math.sin(T * 12), -70, 22, 0, 2 * math.pi); c.set_source_rgba(*hx('E8A87C')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def tooth_section(c, x, y, s, T, worn=0.0, zap=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-330 + 14, 160 + 16, 660, 260); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-330, 160, 660, 260); c.set_source_rgba(*hx('FF8A9A')); c.fill_preserve(); ink(c, 8); c.stroke()     # gum
    def outer():
        c.new_path(); c.move_to(-200, 380); c.curve_to(-230, 100, -240, -150, -150, -260); c.curve_to(-60, -330, 60, -330, 150, -260)
        c.curve_to(240, -150, 230, 100, 200, 380); c.close_path()
    outer(); c.set_source_rgba(*hx('FFFFFF')); c.fill_preserve(); ink(c, 9); c.stroke()            # enamel
    c.new_path(); c.move_to(-150, 380); c.curve_to(-180, 100, -185, -120, -110, -210); c.curve_to(-40, -260, 40, -260, 110, -210)
    c.curve_to(185, -120, 180, 100, 150, 380); c.close_path(); c.set_source_rgba(*hx('FFE7A8')); c.fill_preserve(); ink(c, 6); c.stroke()   # dentin
    c.new_path(); c.move_to(-60, 380); c.curve_to(-70, 150, -80, -40, 0, -90); c.curve_to(80, -40, 70, 150, 60, 380); c.close_path()
    c.set_source_rgba(*hx('FF6B6B')); c.fill_preserve(); ink(c, 6); c.stroke()   # pulp / nerve
    if worn > 0:   # worn gap in enamel on the top-right
        c.save(); outer(); c.clip(); c.arc(170, -230, 90 * worn, 0, 2 * math.pi); c.set_source_rgba(*hx('FFE7A8')); c.fill(); c.restore()
        for k in range(6):
            a = -.9 + k * .12; c.move_to(130 + math.cos(a) * 40, -200 + math.sin(a) * 40); c.line_to(30 + k * 6, -60 + k * 4)
            c.set_source_rgba(*hx('C9A15A', worn)); c.set_line_width(3); c.stroke()
    if zap > 0:
        pts = [(220, -330), (150, -230), (190, -210), (90, -120), (130, -110), (20, -20)]
        c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
        c.set_source_rgba(*hx('FFC93C', zap)); c.set_line_width(26); c.stroke_preserve(); c.set_source_rgba(*hx('1C1614', zap)); c.set_line_width(6); c.stroke()
    c.restore()

def brush(c, x, y, s, T, rot=-.4):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.rectangle(-260 + 12, -24 + 14, 420, 48); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-260, -24, 420, 48); c.set_source_rgba(*hx('3EC1D3')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.rectangle(80, -80, 140, 60); c.set_source_rgba(*hx('FFFFFF')); c.fill_preserve(); ink(c, 6); c.stroke()
    for k in range(7): c.move_to(90 + k * 20, -80); c.line_to(90 + k * 20, -20); c.set_source_rgba(*hx('9FD8FF')); c.set_line_width(5); c.stroke()
    c.restore()

def clock(c, x, y, r, T):
    c.save(); c.translate(x, y)
    c.arc(12, 14, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(0, 0, r, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 9); c.stroke()
    for k in range(12): a = k * math.pi / 6; c.move_to(math.cos(a) * r * .8, math.sin(a) * r * .8); c.line_to(math.cos(a) * r * .9, math.sin(a) * r * .9); ink(c, 5); c.stroke()
    a = T * 2.5 - math.pi / 2; c.move_to(0, 0); c.line_to(math.cos(a) * r * .7, math.sin(a) * r * .7); ink(c, 8); c.stroke()
    c.move_to(0, 0); c.line_to(0, -r * .45); ink(c, 10); c.stroke()
    c.restore()

def xmark(c, x, y, r, col='E63946'):
    c.move_to(x - r, y - r); c.line_to(x + r, y + r); c.move_to(x + r, y - r); c.line_to(x - r, y + r)
    c.set_source_rgba(*hx('1C1614')); c.set_line_width(40); c.stroke_preserve(); c.set_source_rgba(*hx(col)); c.set_line_width(24); c.stroke()

def tickmark(c, x, y, r, col='3FAE5A'):
    c.move_to(x - r, y); c.line_to(x - r * .3, y + r * .7); c.line_to(x + r, y - r * .8)
    c.set_source_rgba(*hx('1C1614')); c.set_line_width(40); c.stroke_preserve(); c.set_source_rgba(*hx(col)); c.set_line_width(24); c.stroke()

def steam(c, x, y, s, T):
    for k in range(3):
        c.move_to(x - 50 * s + k * 50 * s, y); c.curve_to(x - 80 * s + k * 50 * s, y - 60 * s, x - 20 * s + k * 50 * s, y - 90 * s, x - 50 * s + k * 50 * s, y - (150 + 15 * math.sin(T * 3 + k)) * s)
        c.set_source_rgba(1, 1, 1, .9); c.set_line_width(12 * s); c.stroke()

def ent(t, d=.3): return back(min(1, max(0, t) / d)) if t < d else 1.0

