
# ---------------------------------------------------------------- almond props
def water_bowl(c, x, y, s, T, bubbles=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-300 + 14, -40 + 16); c.curve_to(-290 + 14, 220 + 16, 290 + 14, 220 + 16, 300 + 14, -40 + 16); c.close_path(); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.move_to(-300, -40); c.curve_to(-290, 220, 290, 220, 300, -40); c.close_path(); c.set_source_rgba(*hx('E3E7EE')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.save(); c.scale(1, .28); c.arc(0, -140, 300, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('9FD8FF', .9)); c.fill_preserve(); ink(c, 6); c.stroke()
    if bubbles:
        for k in range(6):
            ph = (T * .7 + k / 6) % 1; c.arc(-200 + k * 80, -40 - ph * 160, 10 + 6 * ph, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1 - ph); c.fill()
    c.restore()

def dustbin(c, x, y, s, T, skins=0.0, lid=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-170 + 14, -150 + 16); c.line_to(170 + 14, -150 + 16); c.line_to(130 + 14, 250 + 16); c.line_to(-130 + 14, 250 + 16); c.close_path(); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.move_to(-170, -150); c.line_to(170, -150); c.line_to(130, 250); c.line_to(-130, 250); c.close_path(); c.set_source_rgba(*hx('3FAE5A')); c.fill_preserve(); ink(c, 8); c.stroke()
    for k in range(3): c.move_to(-70 + k * 70, -100); c.line_to(-55 + k * 55, 210); ink(c, 6); c.stroke()
    c.save(); c.translate(-190, -160); c.rotate(-lid * .9)
    c.rectangle(0, -40, 380, 40); c.set_source_rgba(*hx('2E8B48')); c.fill_preserve(); ink(c, 7); c.stroke(); c.restore()
    for k in range(int(skins * 8)):
        c.save(); c.translate(-80 + (k * 47) % 170, -180 - (k % 3) * 30); c.rotate(k)
        c.new_path(); c.save(); c.scale(1, .45); c.arc(0, 0, 40, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('A0642A')); c.fill_preserve(); ink(c, 4); c.stroke(); c.restore()
    c.restore()

def magnifier(c, x, y, r, T):
    c.save(); c.translate(x + 6 * math.sin(T * 2), y)
    c.move_to(r * .7, r * .7); c.line_to(r * 1.7, r * 1.7); c.set_source_rgba(*hx('1C1614')); c.set_line_width(36); c.stroke()
    c.arc(0, 0, r, 0, 2 * math.pi); c.set_source_rgba(*hx('9FD8FF', .35)); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(20); c.stroke()
    c.restore()

def people(c, x0, y0, n, T, cols=10, step=62, show=1.0):
    k = int(n * show)
    for i in range(k):
        x = x0 + (i % cols) * step; y = y0 + (i // cols) * (step + 14)
        col = ('E63946', '2D6CDF', '3FAE5A', 'FF8C1A', '8E5CD9')[i % 5]
        c.arc(x, y - 18, 14, 0, 2 * math.pi); c.set_source_rgba(*hx(col)); c.fill()
        c.move_to(x - 20, y + 26); c.curve_to(x - 20, y - 4, x + 20, y - 4, x + 20, y + 26); c.close_path(); c.fill()

def split_bar(c, x, y, w, h, frac, T):
    c.rectangle(x - w / 2 + 14, y - h / 2 + 16, w, h); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(x - w / 2, y - h / 2, w, h); c.set_source_rgba(*hx('FFF3D6')); c.fill()
    c.rectangle(x - w / 2, y - h / 2, w * frac, h); c.set_source_rgba(*hx('A0642A')); c.fill()
    c.rectangle(x - w / 2, y - h / 2, w, h); ink(c, 9); c.stroke()

def belly(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, -150); c.curve_to(160, -170, 200, 60, 80, 150); c.curve_to(0, 200, -150, 160, -170, 40); c.curve_to(-190, -60, -110, -40, -60, -90); c.curve_to(-40, -130, -20, -150, 0, -150); c.close_path()
    c.set_source_rgba(*hx('FF8FA3')); c.fill_preserve(); ink(c, 8); c.stroke()
    for ex in (-30, 50): c.arc(ex, -20, 12, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(10, 20, 36, .2, math.pi - .2); ink(c, 8); c.stroke()
    c.restore()

def fiber(c, x, y, w, T):
    for k in range(7):
        y0 = y - 120 + k * 40
        c.move_to(x - w / 2, y0)
        for i in range(8): c.curve_to(x - w / 2 + i * w / 8 + 20, y0 - 25 + 10 * math.sin(T * 3 + k), x - w / 2 + i * w / 8 + 40, y0 + 25, x - w / 2 + (i + 1) * w / 8, y0)
        c.set_source_rgba(*hx(('3FAE5A', 'A0642A', 'FFC93C')[k % 3])); c.set_line_width(10); c.stroke()

# ---------------------------------------------------------------- scenes
SC = {l['id']: l for l in TL}

def sc_h1(fr, T, t, l):
    fr[:] = paper('FFC93C')
    overlay(fr, cairo_layer(lambda c: water_bowl(c, 330, 1180, .85, T)))
    sticker(fr, ONE, 330, 1060, T, 0, .5, -12)
    sticker(fr, PEEL, 790, 1080, T, 1, .55, 6)
    sticker(fr, ONE, CX, 760, T, 2, .95, -8)
    title(fr, 'बादाम का छिलका फेंकते हो?', 520, T + 1.0, 92, 'FFFFFF', -2.5)
    tape(fr, 'रात भर भिगोकर...', 330, 1320, T + 1.0, 'FFFFFF', 48, rot=-4)
    tape(fr, '...सुबह छीलकर', 790, 1320, t - 1.9, 'FFFFFF', 48, rot=4)

def sc_h2(fr, T, t, l):
    dx, dy = shake(T, l['start'] + .1, .4, 22)
    fr[:] = paper('E63946')
    if t < .12: fr[:] = (fr * .3 + 255 * .7).astype(np.uint8)
    overlay(fr, cairo_layer(lambda c: dustbin(c, CX + dx, 1080 + dy, 1.2, T, skins=clamp((t - 1.0) / 1.6), lid=clamp((t - .6) / .5))))
    title(fr, 'रुको!', 500, t, 170, 'FFC93C', -4)
    tape(fr, 'सबसे कीमती हिस्सा कचरे में!', CX, 1340, t - 1.6, 'FFFFFF', 52, rot=-2)

def sc_s1(fr, T, t, l):
    fr[:] = paper()
    sticker(fr, ONE, CX, 1000, T, 3, 1.05, -6, t)
    overlay(fr, cairo_layer(lambda c: magnifier(c, 680, 930, 150 * ent(t - .6), T)))
    title(fr, 'ये भूरा छिलका', 520, t, 120, 'FF8C1A', -2)
    tape(fr, 'एंटीऑक्सीडेंट', 330, 1290, t - 2.2, 'FFC93C', 54, rot=-4)
    tape(fr, 'FLAVONOIDS', 790, 1290, t - 4.0, '3FAE5A', 50, ELITE, 4)

def sc_s2(fr, T, t, l):
    fr[:] = paper('3EC1D3')
    f = .8 * clamp((t - .4) / 1.2)
    overlay(fr, cairo_layer(lambda c: split_bar(c, CX, 1000, 800, 170, f, T)))
    put_rgba(fr, ttext('छिलका', 52, HI_B, 'FFFFFF', sw=6), CX - 160, 1000, ent(t - 1.0), 1.0, 0)
    title(fr, 'कितना छिलके में?', 520, t, 112, 'FFFFFF', -2)
    burst(fr, '80%+', 820, 760, t - 1.6, 130, 'E63946', LUCKY, 70)
    sticker(fr, PILE, CX, 1280, T, 4, .55, 0, t - .2)

def sc_s3(fr, T, t, l):
    fr[:] = paper('3FAE5A')
    overlay(fr, cairo_layer(lambda c: (fiber(c, 330, 1000, 420, T), belly(c, 790, 1010, 1.15 * ent(t - 1.6), T))))
    title(fr, 'फ़ाइबर भी!', 520, t, 128, 'FFC93C', -2)
    tape(fr, 'पेट के लिए अच्छा', 790, 1290, t - 1.9, 'FFFFFF', 54, rot=3)

def sc_q1(fr, T, t, l):
    fr[:] = paper('8E5CD9')
    overlay(fr, cairo_layer(lambda c: water_bowl(c, CX, 1120, 1.25, T)))
    sticker(fr, ONE, CX - 80, 960, T, 5, .45, -10, t)
    sticker(fr, ONE, CX + 120, 990, T, 6, .4, 14, t - .2)
    title(fr, 'बड़ा सवाल', 500, t, 128, 'FFC93C', -3)
    tape(fr, 'भिगोने से फ़ायदा बढ़ता है?', CX, 700, t - 1.3, 'FFFFFF', 56, rot=-2)
    burst(fr, '?', 880, 900, t - 1.6, 95, 'E63946', LUCKY, 110)

def sc_q2(fr, T, t, l):
    fr[:] = paper()
    def dr(c):
        for i, (x, col) in enumerate(((290, '3EC1D3'), (790, 'FFC93C'))):
            tk = t - (2.1 if i == 0 else 3.0)
            if tk > 0:
                sc = ent(tk); c.save(); c.translate(x, 860); c.scale(sc, sc); c.rotate(-.03 + .06 * i)
                c.rectangle(-220 + 14, -230 + 16, 440, 460); c.set_source_rgba(*hx('1C1614')); c.fill()
                c.rectangle(-220, -230, 440, 460); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 9); c.stroke()
                if i == 0: water_bowl(c, 0, 60, .55, T)
                c.restore()
        people(c, 245, 1210, 70, T, cols=10, step=66, show=clamp(t / 2.2))
    overlay(fr, cairo_layer(dr))
    if t > 2.1: sticker(fr, ONE, 290, 860, T, 7, .38, -8, t - 2.1)
    if t > 3.0: sticker(fr, ONE, 790, 860, T, 8, .38, 10, t - 3.0)
    tape(fr, 'भीगे', 290, 1100, t - 2.3, 'FFFFFF', 54, rot=-4)
    tape(fr, 'सूखे', 790, 1100, t - 3.2, 'FFFFFF', 54, rot=4)
    title(fr, '70+ लोगों पर टेस्ट', 500, t, 110, 'E63946', -2)

def sc_q3(fr, T, t, l):
    dx, dy = shake(T, l['start'] + .1, .4, 20)
    fr[:] = paper('FF8C1A')
    title(fr, 'नतीजा?', 500, t, 140, 'FFFFFF', -3)
    def card2(y, lab, big, col, a):
        tk = t - a
        if tk <= 0: return
        sc = ent(tk)
        lay = cairo_layer(lambda c: (c.rectangle(CX - 400 + 14, y - 130 + 16, 800, 260), c.set_source_rgba(*hx('1C1614')), c.fill(),
                                      c.rectangle(CX - 400, y - 130, 800, 260), c.set_source_rgba(*hx('FFF8E7')), c.fill_preserve(), ink(c, 9), c.stroke(),
                                      c.rectangle(CX - 400, y - 130, 800, 64), c.set_source_rgba(*hx(col)), c.fill_preserve(), ink(c, 7), c.stroke()))
        if sc < .999: lay = cv2.warpAffine(lay, cv2.getRotationMatrix2D((CX, y), 0, sc), (W, H))
        overlay(fr, lay)
        put_rgba(fr, ttext(lab, 40, HI_M, 'FFFFFF', sw=4, shadow=False), CX, y - 98, sc, 1.0, 0)
        put_rgba(fr, ttext(big, 92, HI_B, 'E63946', sw=8), CX, y + 30, sc, 1.0, -2)
    card2(860 + dy, 'पेट पर असर', 'कोई खास फ़र्क नहीं', '3EC1D3', .3)
    card2(1200 + dy, 'जिसके लिए भिगोते हैं (फ़ाइटेट)', 'कम नहीं हुआ!', '8E5CD9', 3.0)

def sc_w1(fr, T, t, l):
    fr[:] = paper('3EC1D3')
    def dr(c):
        water_bowl(c, 330, 1000, .7, T)
        if t > 2.6: tickmark(c, 330, 1250, 70 * ent(t - 2.6))
        dustbin(c, 790, 1000, .75, T, skins=1.0, lid=1.0)
        if t > 4.9: xmark(c, 790, 980, 120 * ent(t - 4.9, .25))
    overlay(fr, cairo_layer(dr))
    sticker(fr, ONE, 330, 960, T, 9, .35, -10, t)
    title(fr, 'भिगोना? ठीक है!', 500, t, 112, 'FFFFFF', -2)
    tape(fr, 'चबाने में नरम', 330, 1330, t - 2.8, 'FFC93C', 50, rot=-4)
    tape(fr, 'छिलका मत फेंको!', 790, 1330, t - 5.0, 'FFFFFF', 50, rot=4)

def sc_e1(fr, T, t, l):
    fr[:] = paper('FFC93C')
    sticker(fr, PILE, CX, 980, T, 10, .95, -4, t)
    title(fr, 'छिलके समेत खाओ!', 500, t, 116, 'FFFFFF', -2)
    tape(fr, 'अच्छे से चबाकर', CX, 1320, t - 1.2, '3FAE5A', 58, rot=-2)
    burst(fr, 'YES!', 860, 740, t - .3, 100, '3FAE5A', LUCKY, 64)

def sc_e2(fr, T, t, l):
    fr[:] = paper('FF7AA8')
    overlay(fr, cairo_layer(lambda c: phone_s(c, CX - 150, 1000, 1.0, T)))
    sticker(fr, PONE, CX - 150, 1000, T, 11, .9, 0, t)
    sticker(fr, ONE, 800, 820, T, 12, .4, 20, t - .6)
    title(fr, 'भेजो उस दोस्त को', 500, t, 108, 'FFFFFF', -2)
    tape(fr, 'जो रोज़ बड़े प्यार से बादाम छीलता है', CX, 1320, t - 1.3, 'FFC93C', 44, rot=-2)

def sc_brand(fr, T, t):
    fr[:] = paper('3FAE5A')
    overlay(fr, cairo_layer(lambda c: logo(c, CX, 860, 200 * ent(t, .4))))
    title(fr, 'FreshNestHub', 1150, t - .3, 110, 'FFFFFF', -2, LUCKY)
    tape(fr, '@fnhtruths  |  @FreshnestHub', CX, 1300, t - .7, 'FFC93C', 40, ELITE, -1)

SCENES = dict(h1=sc_h1, h2=sc_h2, s1=sc_s1, s2=sc_s2, s3=sc_s3, q1=sc_q1, q2=sc_q2, q3=sc_q3, w1=sc_w1, e1=sc_e1, e2=sc_e2)
