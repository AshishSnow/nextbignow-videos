
# ---------------------------------------------------------------- vital-sign props (16:9)
def heart(c, x, y, s, T, beat=True):
    k = 1 + (.08 * max(0, math.sin(T * 7.5)) ** 8 if beat else 0)
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    def sh():
        c.new_path(); c.move_to(0, 90); c.curve_to(-170, -10, -120, -150, 0, -70); c.curve_to(120, -150, 170, -10, 0, 90); c.close_path()
    c.save(); c.translate(12, 14); sh(); c.set_source_rgba(*hx('1C1614')); c.fill(); c.restore()
    sh(); c.set_source_rgba(*hx('E63946')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(-55, -55, 22, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, .6); c.fill()
    c.restore()

def artery(c, x0, y, x1, T, r=55, push=0.0):
    c.rectangle(x0 + 12, y - r + 14, x1 - x0, 2 * r); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(x0, y - r, x1 - x0, 2 * r); c.set_source_rgba(*hx('FFB0B0')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.rectangle(x0, y - r * .62, x1 - x0, r * 1.24); c.set_source_rgba(*hx('C1121F')); c.fill()
    n = 9
    for k in range(n):
        px = x0 + ((T * 260 + k * (x1 - x0) / n) % (x1 - x0))
        c.arc(px, y + 8 * math.sin(k * 2.1), 14, 0, 2 * math.pi); c.set_source_rgba(*hx('FF6B6B')); c.fill()
    if push > 0:
        for sx in range(int(x0 + 60), int(x1 - 40), 120):
            for sgn in (-1, 1):
                yy = y + sgn * (r + 12); c.move_to(sx, yy + sgn * 40 * push); c.line_to(sx, yy); ink(c, 6); c.stroke()
                c.move_to(sx - 12, yy + sgn * 14); c.line_to(sx, yy); c.line_to(sx + 12, yy + sgn * 14); ink(c, 6); c.stroke()

def wrist(c, x, y, s, T, fingers=True, thumb=False, beat=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-520 + 14, -110 + 16); c.line_to(120 + 14, -130 + 16); c.line_to(140 + 14, 130 + 16); c.line_to(-520 + 14, 110 + 16); c.close_path(); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.move_to(-520, -110); c.line_to(120, -130); c.curve_to(330, -170, 360, 150, 140, 130); c.line_to(-520, 110); c.close_path()
    c.set_source_rgba(*hx('E8A87C')); c.fill_preserve(); ink(c, 8); c.stroke()
    # radial pulse spot (thumb side = top edge)
    k = beat * max(0, math.sin(T * 7.5)) ** 6
    c.arc(-40, -70, 22 + 26 * k, 0, 2 * math.pi); c.set_source_rgba(*hx('E63946', .35 + .4 * k)); c.fill()
    if fingers:
        for i, fx in enumerate((-90, 10)):
            c.save(); c.translate(fx, -90); c.rotate(-.25)
            c.rectangle(-40 + 10, -250 + 12, 80, 270); c.set_source_rgba(*hx('1C1614')); c.fill()
            c.rectangle(-40, -250, 80, 270); c.set_source_rgba(*hx('F2C29C')); c.fill_preserve(); ink(c, 7); c.stroke()
            c.restore()
    if thumb:
        c.save(); c.translate(60, -60); c.rotate(.5)
        c.rectangle(-48, -230, 96, 230); c.set_source_rgba(*hx('F2C29C')); c.fill_preserve(); ink(c, 7); c.stroke(); c.restore()
    c.restore()

def neck(c, x, y, s, T, beat=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.arc(0, -220, 150, 0, 2 * math.pi); c.set_source_rgba(*hx('E8A87C')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.rectangle(-80, -100, 160, 240); c.set_source_rgba(*hx('E8A87C')); c.fill(); c.move_to(-80, -90); c.line_to(-80, 140); c.move_to(80, -90); c.line_to(80, 140); ink(c, 8); c.stroke()
    c.move_to(-260, 260); c.curve_to(-250, 140, 250, 140, 260, 260); c.set_source_rgba(*hx('3EC1D3')); c.fill_preserve(); ink(c, 8); c.stroke()
    k = beat * max(0, math.sin(T * 7.5)) ** 6
    c.arc(55, 0, 16 + 20 * k, 0, 2 * math.pi); c.set_source_rgba(*hx('E63946', .4 + .4 * k)); c.fill()
    for ex in (-50, 50): c.arc(ex, -230, 13, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(0, -180, 35, .2, math.pi - .2); ink(c, 7); c.stroke()
    c.restore()

def chest(c, x, y, s, T, rate=.3):
    br = .5 + .5 * math.sin(T * 2 * math.pi * rate)
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-300, 330); c.curve_to(-310, -160, 310, -160, 300, 330); c.close_path(); c.set_source_rgba(*hx('FFC93C')); c.fill_preserve(); ink(c, 8); c.stroke()
    for sx in (-1, 1):
        c.save(); c.translate(sx * 100, 60); c.scale(1 + .14 * br, 1 + .1 * br)
        c.new_path(); c.move_to(0, -170); c.curve_to(sx * 140, -150, sx * 150, 120, sx * 40, 170); c.curve_to(-sx * 20, 150, -sx * 10, -60, 0, -170); c.close_path()
        c.set_source_rgba(*hx('FF8FA3')); c.fill_preserve(); ink(c, 7); c.stroke(); c.restore()
    c.move_to(0, -150); c.line_to(0, -40); ink(c, 14); c.stroke()
    for k in range(3):
        a = ((T * rate + k / 3) % 1)
        c.move_to(-60 + k * 60, -230 - a * 120); c.curve_to(-90 + k * 60, -260 - a * 120, -30 + k * 60, -290 - a * 120, -60 + k * 60, -320 - a * 120)
        c.set_source_rgba(*hx('FFFFFF', 1 - a)); c.set_line_width(10); c.stroke()
    c.restore()

def sunmoon(c, x, y, r, T, moon=False):
    c.save(); c.translate(x, y)
    if not moon:
        for i in range(12):
            a = i * math.pi / 6 + T * .3; c.move_to(math.cos(a) * r * 1.25, math.sin(a) * r * 1.25); c.line_to(math.cos(a) * r * 1.6, math.sin(a) * r * 1.6)
            c.set_source_rgba(*hx('FF8C1A')); c.set_line_width(12); c.stroke()
        c.arc(0, 0, r, 0, 2 * math.pi); c.set_source_rgba(*hx('FFC93C')); c.fill_preserve(); ink(c, 7); c.stroke()
    else:
        c.arc(0, 0, r, 0, 2 * math.pi); c.set_source_rgba(*hx('FFF3B0')); c.fill_preserve(); ink(c, 7); c.stroke()
        c.arc(r * .45, -r * .2, r * .85, 0, 2 * math.pi); c.set_source_rgba(*hx('2D3A8C')); c.fill()
    c.restore()

def card(c, x, y, w, h, col, rot=0.0, top=None):
    c.save(); c.translate(x, y); c.rotate(rot)
    c.rectangle(-w / 2 + 14, -h / 2 + 16, w, h); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-w / 2, -h / 2, w, h); c.set_source_rgba(*hx('FFF8E7')); c.fill_preserve(); ink(c, 8); c.stroke()
    if top: c.rectangle(-w / 2, -h / 2, w, 60); c.set_source_rgba(*hx(top)); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def stat(fr, x, y, label, big, t, col='E63946', w=420, h=260, rot=-2, bigsize=96, font=LUCKY):
    if t <= 0: return
    sc = ent(t)
    lay = cairo_layer(lambda c: card(c, x, y, w, h, col, math.radians(rot), top=col))
    if sc < .999: lay = cv2.warpAffine(lay, cv2.getRotationMatrix2D((x, y), 0, sc), (W, H))
    overlay(fr, lay)
    put_rgba(fr, ttext(label, 34, HI_M, 'FFFFFF', sw=4, shadow=False), x, y - h / 2 + 30, sc, 1.0, -rot)
    put_rgba(fr, ttext(big, bigsize, font, 'FFC93C', sw=8), x, y + 30, sc, 1.0, -rot)

def chapter(fr, T, t, n, hi, en, col):
    fr[:] = paper(col)
    put_rgba(fr, burst_img(str(n), 170, 'FFC93C', LUCKY, 170), 520, 500, ent(t, .35), 1.0, -6 + 3 * math.sin(T * 3))
    put_rgba(fr, ttext(hi, 150, HI_B, 'FFFFFF', sw=12), 1150, 450, ent(t - .15), 1.0, -2)
    tape(fr, en, 1150, 640, t - .4, 'FFFFFF', 54, ELITE, 2)

def title16(fr, txt, t, col='FFC93C', size=96, y=170):
    title(fr, txt, y, t, size, col, -1.5)

def check_items(fr, items, t, x=1240, y0=300, dy=78, col='FFFFFF'):
    for i, (txt, at) in enumerate(items):
        tk = t - at
        if tk > 0:
            put_rgba(fr, tape_img(txt, 40, col, HI_M), x, y0 + i * dy, ent(tk, .25), 1.0, -1 + (i % 2) * 2)
            overlay(fr, cairo_layer(lambda c, i=i, tk=tk: tickmark(c, x - 330, y0 + i * dy, 22 * ent(tk, .25))))

# ---------------------------------------------------------------- scenes
SC = {l['id']: l for l in TL}
def at(id_, T): return T - SC[id_]['start']

def sc_i(fr, T, t, l):
    k = l['id']
    fr[:] = paper('FFC93C' if k == 'i1' else '3EC1D3' if k == 'i2' else None)
    if k == 'i1':
        sticker(fr, BPM, 470, 560, T, 0, .85, -6)
        sticker(fr, OXI, 1460, 470, T, 1, .85, 8)
        sticker(fr, THM, 1430, 760, T, 2, .8, -10)
        title16(fr, 'इन नंबरों का मतलब पता है?', T + 1.0, 'FFFFFF', 92)
        burst(fr, '?!', 980, 560, T + 1.0, 120, 'E63946', LUCKY, 90)
    elif k == 'i2':
        overlay(fr, cairo_layer(lambda c: doctor(c, 520, 600, 1.15 * ent(t), T)))
        title16(fr, 'डॉक्टर सबसे पहले ये चेक करते हैं', t, 'FFFFFF', 80)
        tape(fr, 'VITAL SIGNS', 1250, 480, t - 4.0, 'FFC93C', 72, ELITE, -3)
        tape(fr, 'शरीर के 5 ज़रूरी इशारे', 1250, 640, t - 6.0, 'FFFFFF', 54, rot=2)
    else:
        title16(fr, 'आज पाँचों आसान भाषा में', t - 4.5, 'E63946', 86)
        chips = (('नब्ज़', 'E63946', .2), ('साँस', '3EC1D3', .96), ('BP', '2D6CDF', 1.78), ('ऑक्सीजन', '3FAE5A', 2.74), ('तापमान', 'FF8C1A', 3.48))
        for i, (txt, col, a) in enumerate(chips):
            stat(fr, 230 + i * 365, 560, f'{i + 1}', txt, t - a, col, 320, 230, -3 + 1.5 * i, 70, HI_B)

def sc_p(fr, T, t, l):
    k = l['id']
    if k == 'p0': chapter(fr, T, t, 1, 'नब्ज़', 'PULSE', 'E63946'); return
    if k == 'p1':
        fr[:] = paper('FFB0C8')
        overlay(fr, cairo_layer(lambda c: (artery(c, 600, 560, 1700, T, push=clamp((t - 2.0) / .6)), heart(c, 420, 560, 1.3 * ent(t), T))))
        title16(fr, 'हर धड़कन = खून का धक्का', t, 'FFFFFF', 88)
        tape(fr, 'यही धक्का कलाई पर महसूस होता है', 1150, 800, t - 4.0, 'FFC93C', 50, rot=-2)
    elif k == 'p2':
        fr[:] = paper()
        thumb = t > 5.6
        overlay(fr, cairo_layer(lambda c: wrist(c, 980, 640, 1.15, T, fingers=not thumb, thumb=thumb, beat=1.0)))
        title16(fr, 'दो उंगलियाँ, अंगूठे वाली तरफ़', t, 'E63946', 86)
        if thumb:
            overlay(fr, cairo_layer(lambda c: xmark(c, 1060, 440, 90 * ent(t - 5.6))))
            tape(fr, 'अंगूठा नहीं! उसकी अपनी नब्ज़', 1400, 820, t - 5.9, 'FFC93C', 50, rot=2)
    elif k == 'p3':
        fr[:] = paper('3EC1D3')
        overlay(fr, cairo_layer(lambda c: neck(c, 760, 600, 1.1, T, beat=1.0)))
        title16(fr, 'गर्दन पर भी', t, 'FFFFFF', 96)
        tape(fr, 'बहुत हल्के हाथ से', 1350, 480, t - 2.2, 'FFC93C', 56, rot=-2)
        tape(fr, 'एक बार में एक तरफ़', 1350, 620, t - 4.3, 'FFFFFF', 56, rot=2)
    elif k == 'p4':
        fr[:] = paper('FFC93C')
        overlay(fr, cairo_layer(lambda c: clock(c, 520, 560, 210 * ent(t), T)))
        stat(fr, 1200, 470, 'गिनो', '30 सेकंड', t - 1.4, '2D6CDF', 460, 230, -2, 76, HI_B)
        stat(fr, 1200, 760, 'फिर', '× 2', t - 2.6, 'E63946', 360, 220, 2, 96)
        title16(fr, 'घड़ी देखो', t, 'FFFFFF', 96)
        if t > 4.6: burst(fr, 'DONE!', 1640, 360, t - 4.6, 100, '3FAE5A', LUCKY, 56)
    elif k == 'p5':
        fr[:] = paper('3FAE5A')
        overlay(fr, cairo_layer(lambda c: heart(c, 420, 560, 1.4, T)))
        stat(fr, 1080, 540, 'आराम में, एक मिनट', '60-100', t - .4, 'E63946', 560, 300, -2, 130)
        title16(fr, 'नॉर्मल पल्स', t, 'FFFFFF', 100)
        tape(fr, 'रोज़ दौड़ने/खेलने वालों की कम भी हो सकती है', 1080, 820, t - 5.8, 'FFC93C', 44, rot=1)
    elif k == 'p6':
        fr[:] = paper('FF8C1A')
        title16(fr, 'पल्स बढ़ जाती है जब...', t, 'FFFFFF', 90)
        for i, (txt, a) in enumerate((('दौड़ने के बाद', .2), ('डर में', 1.0), ('बुखार में', 2.2))):
            stat(fr, 340 + i * 420, 520, '', txt, t - a, ('2D6CDF', 'E63946', 'FF7AA8')[i], 380, 200, -3 + 3 * i, 64, HI_B)
        tape(fr, 'इसलिए 5 मिनट आराम से बैठकर चेक करो', CX, 800, t - 4.6, 'FFC93C', 52, rot=-1)
    elif k == 'p7':
        fr[:] = paper('8E5CD9')
        overlay(fr, cairo_layer(lambda c: doctor(c, 1500, 620, 1.05 * ent(t - 5.5), T)))
        title16(fr, 'डॉक्टर से कब मिलें?', t, 'FFC93C', 92)
        check_items(fr, (('आराम में भी बार-बार 100 से ऊपर', .3), ('या 60 से नीचे + चक्कर/बेहोशी', 3.3)), t, 700, 450, 150)

def sc_b(fr, T, t, l):
    k = l['id']
    if k == 'b0': chapter(fr, T, t, 2, 'साँस', 'BREATHING RATE', '3EC1D3'); return
    if k == 'b1':
        fr[:] = paper('B9F2C8')
        overlay(fr, cairo_layer(lambda c: chest(c, 520, 600, 1.0, T, .3)))
        stat(fr, 1250, 540, 'एक मिनट में', '12-20', t - 3.0, '3FAE5A', 560, 300, -2, 130)
        title16(fr, 'छाती कितनी बार ऊपर-नीचे?', t, '3FAE5A', 88)
    elif k == 'b2':
        fr[:] = paper('2D3A8C')
        overlay(fr, cairo_layer(lambda c: (wrist(c, 760, 760, .75, T, beat=1.0), chest(c, 1450, 600, .75, T, .3))))
        title16(fr, 'चालाकी!', t, 'FFC93C', 120)
        tape(fr, 'पता चला तो साँस बदल जाती है', CX, 330, t - 2.4, 'FFFFFF', 52, rot=-2)
        tape(fr, 'नब्ज़ के बहाने चुपचाप गिनो', CX, 860, t - 7.0, 'FFC93C', 56, rot=2)
        if t > 7.0: burst(fr, 'SHH!', 1700, 380, t - 7.0, 100, 'FF7AA8', LUCKY, 58)
    else:
        fr[:] = paper('FF7AA8')
        title16(fr, 'हल्के में मत लेना', t, 'FFFFFF', 100)
        check_items(fr, (('बुखार के साथ बहुत तेज़ साँस', .2), ('थोड़ा चलने पर भी साँस फूलना', 3.3)), t, 960, 460, 160, 'FFC93C')

def sc_c(fr, T, t, l):
    k = l['id']
    if k == 'c0': chapter(fr, T, t, 3, 'ब्लड प्रेशर', 'BLOOD PRESSURE', '2D6CDF'); return
    if k == 'c1':
        fr[:] = paper('FFB0C8')
        overlay(fr, cairo_layer(lambda c: (artery(c, 520, 600, 1750, T, r=80, push=1.0), heart(c, 330, 600, 1.2, T))))
        title16(fr, 'नसों की दीवार पर ज़ोर = BP', t, 'FFFFFF', 86)
    elif k == 'c2':
        fr[:] = paper()
        sticker(fr, BPM, 520, 580, T, 3, .95, -4, t)
        stat(fr, 1300, 430, 'ऊपर वाला: दिल धड़कता है', 'SYS', t - 1.8, 'E63946', 620, 240, -2, 96)
        stat(fr, 1300, 740, 'नीचे वाला: दिल आराम करता है', 'DIA', t - 5.3, '2D6CDF', 620, 240, 2, 96)
        title16(fr, 'दो नंबर', t, '2D6CDF', 110)
    elif k == 'c3':
        fr[:] = paper('FFF3B0')
        title16(fr, 'कितना सही?', t, 'E63946', 104)
        stat(fr, 600, 560, 'अच्छा', '<120/80', t - .2, '3FAE5A', 620, 320, -2, 110)
        stat(fr, 1330, 560, 'बार-बार = हाई BP', '140/90+', t - 3.5, 'E63946', 620, 320, 2, 110)
        if t > 3.5: burst(fr, 'HIGH!', 1700, 330, t - 3.5, 95, 'E63946', LUCKY, 54)
    elif k == 'c4':
        fr[:] = paper('3EC1D3')
        sticker(fr, BPM, 500, 600, T, 4, .8, 5, t)
        stat(fr, 1250, 560, 'घर की मशीन पर बार-बार', '135/85+', t - 3.2, 'FF8C1A', 640, 320, -2, 110)
        title16(fr, 'घर पर सीमा थोड़ी कम', t, 'FFFFFF', 92)
        tape(fr, 'तो भी डॉक्टर को दिखाओ', 1250, 830, t - 6.2, 'FFC93C', 50, rot=1)
    elif k == 'c5':
        fr[:] = paper('8E5CD9')
        overlay(fr, cairo_layer(lambda c: (doctor(c, 560, 640, 1.1, T), heart(c, 1300, 560, 1.0 + .25 * clamp((t - 3.2) / .5), T))))
        title16(fr, 'एक बार का नंबर? घबराओ मत!', t, 'FFC93C', 86)
        if t > 3.2: burst(fr, 'UP!', 1560, 380, t - 3.2, 90, 'E63946', LUCKY, 60)
    elif k == 'c6':
        fr[:] = paper('FFFFFF' if False else None)
        title16(fr, 'BP नापने का सही तरीका', t, '2D6CDF', 90)
        sticker(fr, BPM, 330, 600, T, 5, .7, -6, t)
        items = (('30 मिनट पहले चाय/कॉफ़ी/सिगरेट नहीं', 1.7), ('पहले टॉयलेट', 5.8), ('पीठ टिकाकर 5 मिनट बैठो', 7.2),
                 ('पैर ज़मीन पर, क्रॉस नहीं', 10.8), ('हाथ टेबल पर, दिल की ऊँचाई', 12.8), ('कफ़ नंगी बाँह पर', 15.5),
                 ('नापते वक्त बात नहीं', 18.3), ('1 मिनट गैप, 2 बार, लिख लो', 20.4))
        check_items(fr, items, t, 1180, 290, 76)

def sc_o(fr, T, t, l):
    k = l['id']
    if k == 'o0': chapter(fr, T, t, 4, 'ऑक्सीजन', 'SpO2 / OXYGEN', '3FAE5A'); return
    if k == 'o1':
        fr[:] = paper('2D3A8C')
        sticker(fr, OXI, 620, 560, T, 6, 1.05, -6, t)
        def dr(c):
            for i in range(5):
                a = clamp((t - 2.0) / 1.5); c.move_to(1000, 560); c.line_to(1000 + 600 * a, 420 + i * 70)
                c.set_source_rgba(*hx('FF3B3B', .7)); c.set_line_width(18); c.stroke()
        overlay(fr, cairo_layer(dr))
        title16(fr, 'उंगली के आर-पार लाल रोशनी', t, 'FFC93C', 86)
        tape(fr, 'खून में कितनी ऑक्सीजन?', 1400, 830, t - 4.5, 'FFFFFF', 54, rot=2)
    elif k == 'o2':
        fr[:] = paper('3FAE5A')
        sticker(fr, OXI, 520, 560, T, 7, .85, 4, t + 1)
        stat(fr, 1250, 540, 'ज़्यादातर लोगों में', '95-100%', t - .4, '3FAE5A', 640, 320, -2, 120)
        title16(fr, 'नॉर्मल ऑक्सीजन', t, 'FFFFFF', 100)
    elif k == 'o3':
        fr[:] = paper('FF8C1A')
        title16(fr, 'ये नंबर बिगाड़ते हैं!', t, 'FFFFFF', 100)
        for i, (txt, a, col) in enumerate((('ठंडी उंगलियाँ', 1.2, '3EC1D3'), ('गहरी नेल पॉलिश', 2.3, 'FF7AA8'), ('नकली नाखून', 3.5, '8E5CD9'), ('हाथ हिलाना', 4.7, 'E63946'))):
            stat(fr, 270 + i * 460, 560, '', txt, t - a, col, 400, 220, -3 + 2 * i, 58, HI_B)
    elif k == 'o4':
        fr[:] = paper('3EC1D3')
        sticker(fr, OXI, 400, 600, T, 8, .7, -4, t + 1)
        title16(fr, 'सही तरीका', t, 'FFFFFF', 104)
        check_items(fr, (('हाथ गरम करो', .1), ('नेल पॉलिश वाली उंगली छोड़ो', 1.5), ('आराम से बैठो', 3.3), ('नंबर रुकने तक इंतज़ार', 4.5)), t, 1180, 360, 120)
    elif k == 'o5':
        dx, dy = shake(T, l['start'] + 3.4, .4, 18)
        fr[:] = paper('E63946')
        title16(fr, 'कब ध्यान दें?', t, 'FFC93C', 104)
        stat(fr, 560 + dx, 520 + dy, 'डॉक्टर से बात करो', '≤ 92%', t - .2, 'FF8C1A', 600, 300, -2, 120)
        stat(fr, 1360 + dx, 520 + dy, 'तुरंत अस्पताल', '≤ 88%', t - 3.4, '1C1614', 600, 300, 2, 120)
        tape(fr, 'नीले होंठ, साँस फूलना, छाती में दर्द = तुरंत अस्पताल', CX, 830, t - 5.6, 'FFFFFF', 44, rot=-1)

def sc_t(fr, T, t, l):
    k = l['id']
    if k == 't0': chapter(fr, T, t, 5, 'तापमान', 'TEMPERATURE', 'FF8C1A'); return
    if k == 't1':
        fr[:] = paper('FFC93C')
        sticker(fr, THM, 560, 560, T, 9, 1.0, -8, t)
        stat(fr, 1360, 540, 'नॉर्मल', '97.8-99°F', t - .8, 'FF8C1A', 680, 320, -2, 104)
        title16(fr, 'शरीर का तापमान', t, 'FFFFFF', 100)
    elif k == 't2':
        fr[:] = paper('2D3A8C')
        overlay(fr, cairo_layer(lambda c: (sunmoon(c, 600, 560, 130 * ent(t), T), sunmoon(c, 1320, 560, 130 * ent(t - 1.2), T, moon=True))))
        tape(fr, 'सुबह थोड़ा कम', 600, 830, t - .3, 'FFC93C', 54, rot=-2)
        tape(fr, 'शाम को थोड़ा ज़्यादा', 1320, 830, t - 1.5, 'FFFFFF', 54, rot=2)
        title16(fr, 'बिल्कुल नॉर्मल!', t - 2.6, 'FFC93C', 100)
    elif k == 't3':
        fr[:] = paper('3EC1D3')
        sticker(fr, THM, 960, 520, T, 10, .9, 4, t)
        stat(fr, 480, 640, 'बगल', 'थोड़ा कम', t - .2, '2D6CDF', 460, 230, -3, 70, HI_B)
        stat(fr, 1440, 640, 'मुँह', 'थोड़ा ज़्यादा', t - 1.2, 'E63946', 460, 230, 3, 70, HI_B)
        tape(fr, 'हर बार एक ही जगह से नापो', CX, 860, t - 3.1, 'FFC93C', 56, rot=-1)
        title16(fr, 'कहाँ से नापा?', t, 'FFFFFF', 100)
    elif k == 't4':
        fr[:] = paper()
        sticker(fr, THM, 600, 560, T, 11, .9, -6, t)
        overlay(fr, cairo_layer(lambda c: clock(c, 1450, 520, 170 * ent(t - .5), T)))
        tape(fr, 'मुँह से? 15 मिनट पहले गरम/ठंडा नहीं', CX, 820, t - .8, 'FFC93C', 50, rot=-1)
        title16(fr, 'बीप तक रुको!', t - 4.9, 'E63946', 100)
        if t > 4.9: burst(fr, 'BEEP!', 1700, 330, t - 4.9, 95, '3FAE5A', LUCKY, 54)
    elif k == 't5':
        dx, dy = shake(T, l['start'] + .2, .4, 16)
        fr[:] = paper('FF7AA8')
        stat(fr, 560 + dx, 520 + dy, 'बुखार', '100.4°F+', t - .1, 'E63946', 640, 320, -2, 110)
        stat(fr, 1360, 520, 'डॉक्टर के पास', '103°F+', t - 3.6, '1C1614', 600, 320, 2, 110)
        tape(fr, 'या बुखार 3 दिन से ज़्यादा', 1360, 820, t - 6.0, 'FFC93C', 52, rot=2)
        title16(fr, 'कब बुखार?', t, 'FFFFFF', 100)

def sc_r(fr, T, t, l):
    k = l['id']
    if k == 'r1':
        fr[:] = paper('FFC93C')
        title16(fr, 'एक बार में याद कर लो', t, 'FFFFFF', 90)
        cards = (('पल्स', '60-100', 'E63946', 2.5), ('साँस', '12-20', '3EC1D3', 4.5), ('BP', '<120/80', '2D6CDF', 6.8), ('ऑक्सीजन', '95%+', '3FAE5A', 10.0), ('तापमान', '~99°F', 'FF8C1A', 12.3))
        for i, (lab, big, col, a) in enumerate(cards):
            stat(fr, 210 + i * 375, 560, lab, big, t - a, col, 340, 280, -3 + 1.5 * i, 66 if len(big) > 5 else 80)
    elif k == 'r2':
        fr[:] = paper('8E5CD9')
        overlay(fr, cairo_layer(lambda c: doctor(c, 1450, 620, 1.1, T)))
        title16(fr, 'ये नंबर इशारे हैं, इलाज नहीं', t, 'FFC93C', 88)
        tape(fr, 'कुछ अजीब लगे? खुद दवा नहीं, डॉक्टर से मिलो', 760, 600, t - 4.8, 'FFFFFF', 46, rot=-2)
    else:
        fr[:] = paper('FF7AA8')
        sticker(fr, BPM, 520, 580, T, 12, .75, -8, t)
        overlay(fr, cairo_layer(lambda c: phone_s(c, 1300, 600, .85, T)))
        title16(fr, 'सेव करो और भेजो!', t, 'FFFFFF', 100)
        tape(fr, 'जिसके पास BP मशीन है, पर नंबर कोई नहीं समझता', CX, 860, t - 1.6, 'FFC93C', 44, rot=-1)
        burst(fr, 'SAVE!', 1700, 360, t - .5, 95, '3FAE5A', LUCKY, 54)

def sc_brand(fr, T, t):
    fr[:] = paper('3FAE5A')
    overlay(fr, cairo_layer(lambda c: logo(c, CX, 440, 190 * ent(t, .4))))
    title(fr, 'FreshNestHub', 720, t - .3, 120, 'FFFFFF', -2, LUCKY)
    tape(fr, '@fnhtruths  |  @FreshnestHub', CX, 880, t - .7, 'FFC93C', 40, ELITE, -1)

SCENES = {}
for _l in TL:
    SCENES[_l['id']] = {'i': sc_i, 'p': sc_p, 'b': sc_b, 'c': sc_c, 'o': sc_o, 't': sc_t, 'r': sc_r}[_l['id'][0]]

