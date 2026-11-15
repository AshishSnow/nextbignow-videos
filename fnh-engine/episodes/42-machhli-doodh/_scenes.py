
# ---------------------------------------------------------------- fish + milk props
def shadowed(c, path, col, dx=14, dy=16, lw=8):
    c.save(); c.translate(dx, dy); path(); c.set_source_rgba(*hx('1C1614')); c.fill(); c.restore()
    path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, lw); c.stroke()

def arm(c, x, y, s, T, patches=0.0, skin='C68A5E', rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    def p():
        c.new_path(); c.move_to(-320, -70); c.curve_to(-100, -95, 120, -80, 230, -70); c.curve_to(300, -110, 360, -60, 350, 0)
        c.curve_to(360, 60, 300, 100, 230, 70); c.curve_to(120, 80, -100, 95, -320, 70); c.close_path()
    shadowed(c, p, skin)
    if patches > 0:
        c.save(); p(); c.clip()
        for k, (px, py, r) in enumerate(((-180, -10, 46), (-40, 25, 34), (90, -20, 40), (210, 20, 28))):
            sc = clamp(patches * 4 - k)
            if sc > 0:
                c.save(); c.translate(px, py); c.scale(1, .7); c.arc(0, 0, r * sc, 0, 2 * math.pi); c.restore()
                c.set_source_rgba(*hx('FFF1E6')); c.fill()
        c.restore()
    c.restore()

def cells(c, x, y, T, attacked=0.0):
    # skin layer with colour cells (melanocytes); immune blobs turn some white
    c.rectangle(x - 400 + 14, y - 190 + 16, 800, 380); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(x - 400, y - 190, 800, 380); c.set_source_rgba(*hx('F6D2B8')); c.fill_preserve(); ink(c, 9); c.stroke()
    c.rectangle(x - 400, y - 190, 800, 90); c.set_source_rgba(*hx('E8B48F')); c.fill_preserve(); ink(c, 6); c.stroke()
    rnd = np.random.default_rng(7)
    for k in range(10):
        cx = x - 340 + k * 76; cy = y + 20 + 30 * math.sin(k * 1.7)
        dead = attacked * 10 > k and k % 2 == 0
        col = 'FFFFFF' if dead else '7A4420'
        c.arc(cx, cy, 30, 0, 2 * math.pi); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 5); c.stroke()
        if not dead:
            for a in range(3):
                c.move_to(cx, cy); c.line_to(cx + 48 * math.cos(a * 2.1 + k), cy - 60 - 10 * a); c.set_source_rgba(*hx('7A4420')); c.set_line_width(7); c.stroke()
    for k in range(3):
        u = clamp(attacked * 1.4 - k * .2)
        if u <= 0: continue
        bx = x - 320 + k * 300 + 40 * math.sin(T * 3 + k); by = y + 140
        c.arc(bx, by, 40 * ent(u), 0, 2 * math.pi); c.set_source_rgba(*hx('2D6CDF')); c.fill_preserve(); ink(c, 5); c.stroke()
        for ex in (-12, 12): c.arc(bx + ex, by - 8, 6, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill()
        c.move_to(bx - 14, by + 14); c.line_to(bx + 14, by + 10); ink(c, 4); c.stroke()

def stamp(c, x, y, txt_w, sc, col='E63946', rot=-.18):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    c.rectangle(-txt_w / 2, -70, txt_w, 140); c.set_source_rgba(*hx(col, .15)); c.fill_preserve(); c.set_source_rgba(*hx(col)); c.set_line_width(12); c.stroke()
    c.rectangle(-txt_w / 2 + 16, -54, txt_w - 32, 108); c.set_line_width(4); c.stroke()
    c.restore()

def handshake(c, x, y, s, T):
    c.save(); c.translate(x, y + 6 * math.sin(T * 6)); c.scale(s, s)
    def left():
        c.new_path(); c.move_to(-420, -40); c.line_to(-60, -40); c.curve_to(10, -40, 40, 0, 20, 40); c.line_to(-420, 60); c.close_path()
    def right():
        c.new_path(); c.move_to(420, -50); c.line_to(40, -50); c.curve_to(-40, -50, -50, 10, -10, 50); c.line_to(420, 50); c.close_path()
    shadowed(c, left, 'C68A5E'); shadowed(c, right, 'E8B48F')
    c.save(); right(); c.clip()
    for k, (px, py) in enumerate(((150, -10), (290, 20))):
        c.save(); c.translate(px, py); c.scale(1, .6); c.arc(0, 0, 30, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('FFF4EC')); c.fill()
    c.restore()
    for k in range(4): c.move_to(-40 + k * 18, -40); c.line_to(-30 + k * 18, 30); ink(c, 4); c.stroke()
    c.restore()

def heart(c, x, y, r, col='E63946'):
    c.save(); c.translate(x, y); c.move_to(0, r * .9)
    c.curve_to(-r * 1.6, -r * .2, -r * .7, -r * 1.3, 0, -r * .45); c.curve_to(r * .7, -r * 1.3, r * 1.6, -r * .2, 0, r * .9); c.close_path()
    c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, r * .1); c.stroke(); c.restore()

def itch(c, x, y, T, n=9):
    rnd = np.random.default_rng(3)
    for k in range(n):
        dx, dy = rnd.uniform(-150, 150), rnd.uniform(-60, 60)
        r = 9 + 4 * abs(math.sin(T * 4 + k))
        c.arc(x + dx, y + dy, r, 0, 2 * math.pi); c.set_source_rgba(*hx('E63946')); c.fill()
    for k in range(3):
        a = T * 9 + k * 2
        c.move_to(x - 200 + k * 30, y - 120); c.line_to(x - 170 + k * 30 + 10 * math.sin(a), y - 160); ink(c, 6); c.stroke()

def plus_eq(c, x, y, sym, r=46):
    c.arc(x + 6, y + 8, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 6); c.stroke()
    if sym == '+': c.move_to(x - 22, y); c.line_to(x + 22, y); c.move_to(x, y - 22); c.line_to(x, y + 22)
    else: c.move_to(x - 22, y - 9); c.line_to(x + 22, y - 9); c.move_to(x - 22, y + 9); c.line_to(x + 22, y + 9)
    ink(c, 9); c.stroke()

# ---------------------------------------------------------------- scenes
SC = {l['id']: l for l in TL}

def sc_h1(fr, T, t, l):
    fr[:] = paper('4FC3F7')
    sticker(fr, FRY, 400, 1010, T, 0, .78, -6)
    if t > 1.0: sticker(fr, MILK, 790, 1000, T, 1, .82 * ent(t - 1.0, .35), 6)
    title(fr, 'मछली के बाद दूध?', 520, T + 1.0, 112, 'FFFFFF', -2.5)
    tape(fr, 'मछली खाई...', 380, 1330, T + 1.0, 'FFFFFF', 48, rot=-4)
    tape(fr, '...ऊपर से दूध!', 780, 1330, t - 1.4, 'FFC93C', 48, rot=4)

def sc_h2(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 1.3, .4, 20)
    fr[:] = paper('E63946')
    if t < .12: fr[:] = (fr * .3 + 255 * .7).astype(np.uint8)
    def dr(c):
        granny(c, 330 + dx, 1060 + dy, 1.05, T)
        if t > 1.1: c.save(); c.translate(720, 800); c.scale(ent(t - 1.1), ent(t - 1.1)); bubble(c, 0, 0, 440, 230, (-1, 1)); c.restore()
        arm(c, 690, 1200, .6 * ent(t - 1.3), T, patches=clamp((t - 1.5) / 1.2), rot=-.1)
    overlay(fr, cairo_layer(dr))
    put_rgba(fr, ttext('सफ़ेद दाग!', 66, HI_B, 'E63946', sw=6), 720, 790, ent(t - 1.2), 1.0, -3)
    title(fr, 'दादी बोलेंगी...', 500, t, 120, 'FFC93C', -3)

def sc_s1(fr, T, t, l):
    fr[:] = paper('9B7FE0')
    sticker(fr, RAW, 300, 900, T, 2, .42, -8, t)
    if t > .6: sticker(fr, MILK, 690, 900, T, 3, .36 * ent(t - .6), 4)
    def dr(c):
        if t > .4: plus_eq(c, 500, 900, '+')
        if t > 1.6: plus_eq(c, 860, 900, '=')
        arm(c, CX, 1190, .95 * ent(t - 2.6), T, patches=clamp((t - 3.4) / 1.6))
    overlay(fr, cairo_layer(dr))
    title(fr, 'बहुत लोग कहते हैं...', 500, t, 108, 'FFFFFF', -2)
    burst(fr, '?', 900, 760, t - 1.9, 70, 'E63946', LUCKY, 80)
    tape(fr, 'स्किन पर सफ़ेद धब्बे?', CX, 1360, t - 3.6, 'FFC93C', 50, rot=-2)

def sc_s2(fr, T, t, l):
    fr[:] = paper('1FB5A8')
    overlay(fr, cairo_layer(lambda c: cells(c, CX, 1010, T, clamp((t - 5.2) / 3.0))))
    title(fr, 'खाने से नहीं होता!', 500, t, 112, 'FFFFFF', -2)
    tape(fr, 'सफ़ेद दाग = विटिलिगो', CX, 700, t - 1.2, 'FFC93C', 52, rot=-2)
    tape(fr, 'रंग बनाने वाले सेल्स', 330, 1290, t - 3.0, 'FFFFFF', 42, rot=-3)
    tape(fr, 'इम्यून सिस्टम की गलती', 760, 1290, t - 5.4, '2D6CDF', 42, rot=3, tcol='FFFFFF')

def sc_s3(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 1.2, .35, 16)
    fr[:] = paper('FF8C1A')
    sticker(fr, CURRY, 380, 950, T, 4, .55, -4, t)
    sticker(fr, MILK, 790, 950, T, 5, .5, 5, t - .2)
    overlay(fr, cairo_layer(lambda c: (stamp(c, CX + dx, 1010 + dy, 700, ent(t - 1.2, .2)), doctor(c, 820, 1220, .55 * ent(t - 5.0), T))))
    if t > 1.2: put_rgba(fr, ttext('कोई सबूत नहीं!', 84, HI_B, 'E63946', sw=6), CX + dx, 1010 + dy, ent(t - 1.2, .2), 1.0, -10)
    title(fr, 'रिसर्च क्या कहती है?', 500, t, 108, 'FFFFFF', -2)
    tape(fr, 'स्किन डॉक्टर: मिथ!', 380, 1330, t - 5.2, 'FFFFFF', 50, rot=-3)

def sc_s4(fr, T, t, l):
    fr[:] = paper('FF7AA8')
    def dr(c):
        for i, (x, col, sk) in enumerate(((340, '2D6CDF', 'C68A5E'), (740, '8E5CD9', 'E8B48F'))):
            sc = ent(t - .3 - .3 * i)
            c.save(); c.translate(x, 1080); c.scale(sc, sc)
            c.move_to(-150, 200); c.curve_to(-150, -20, 150, -20, 150, 200); c.close_path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 8); c.stroke()
            c.arc(0, -120, 95, 0, 2 * math.pi); c.set_source_rgba(*hx(sk)); c.fill_preserve(); ink(c, 8); c.stroke()
            if i == 1:
                for px, py, r in ((-40, -160, 26), (35, -95, 20), (-20, -60, 14)):
                    c.save(); c.translate(px, py); c.scale(1, .75); c.arc(0, 0, r, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('FFF4EC')); c.fill()
            for ex in (-32, 32): c.arc(ex, -125, 10, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
            c.arc(0, -95, 32, .2, math.pi - .2); ink(c, 7); c.stroke()
            c.restore()
        if t > 1.0:
            a = ent(t - 1.0); c.move_to(470, 1150); c.curve_to(520, 1110 - 20 * a, 560, 1110 - 20 * a, 610, 1150); ink(c, 34); c.stroke()
            c.move_to(470, 1150); c.curve_to(520, 1110 - 20 * a, 560, 1110 - 20 * a, 610, 1150); c.set_source_rgba(*hx('E8B48F')); c.set_line_width(20); c.stroke()
        heart(c, CX, 820, 70 * ent(t - 3.2))
    overlay(fr, cairo_layer(dr))
    title(fr, 'छूने से नहीं फैलता', 500, t, 112, 'FFFFFF', -2)
    tape(fr, 'दूरी मत बनाओ', CX, 1360, t - 3.4, 'FFC93C', 58, rot=-2)

def sc_s5(fr, T, t, l):
    fr[:] = paper('9BDB6A')
    sticker(fr, RAW, 340, 880, T, 6, .36, -6, t)
    sticker(fr, MILK, 790, 880, T, 7, .32, 6, t - .2)
    overlay(fr, cairo_layer(lambda c: (arm(c, CX, 1150, .85, T, rot=.04), itch(c, CX, 1150, T) if t > 2.6 else None)))
    title(fr, 'एलर्जी है तो?', 500, t, 120, 'FFFFFF', -2)
    tape(fr, 'खुजली या दाने', CX, 1330, t - 3.0, 'FFFFFF', 52, rot=-2)
    burst(fr, 'अलग चीज़!', 820, 720, t - 5.2, 120, '8E5CD9', HI_B, 44)

def sc_w1(fr, T, t, l):
    fr[:] = paper('3EC1D3')
    def dr(c):
        arm(c, 420, 880, .55, T, patches=.3, rot=-.12)
        doctor(c, 760, 1110, .95 * ent(t - 3.8), T)
        if t > 3.0: tickmark(c, 330, 1170, 80 * ent(t - 3.0))
    overlay(fr, cairo_layer(dr))
    title(fr, 'नया सफ़ेद धब्बा दिखे?', 500, t, 104, 'FFFFFF', -2)
    tape(fr, 'डरो मत!', 330, 1320, t - 2.8, 'FFF8E7', 56, rot=-4)
    tape(fr, 'जल्दी स्किन डॉक्टर', 760, 1390, t - 4.2, 'FFC93C', 50, rot=3)

def sc_e1(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 1.9, .35, 16)
    fr[:] = paper('7FD8B0')
    sticker(fr, CURRY, 360, 980 + dy, T, 8, .55, -6, t)
    if t > .9: sticker(fr, KHEER, 780, 1000 + dy, T, 9, .55 * ent(t - .9), 4)
    overlay(fr, cairo_layer(lambda c: plus_eq(c, 580, 990, '+') if t > .6 else None))
    title(fr, 'फिश करी के बाद खीर?', 500, t, 104, 'FFFFFF', -2)
    burst(fr, 'चलेगी!', CX, 1240, t - 1.9, 115, 'E63946', HI_B, 54)

def sc_e2(fr, T, t, l):
    fr[:] = paper('FF6B5B')
    def dr(c):
        person_q(c, 300, 1110, 1.05, T)
        if t > 3.3: c.save(); c.translate(720, 800); c.scale(ent(t - 3.3), ent(t - 3.3)); bubble(c, 0, 0, 450, 230, (-1, 1)); c.restore()
        phone_s(c, 800, 1200, .55, T)
    overlay(fr, cairo_layer(dr))
    sticker(fr, MILK, 520, 1170, T, 10, .26, 8, t - .3)
    put_rgba(fr, ttext('अरे! मछली खाई है!', 46, HI_B, 'E63946', sw=5), 720, 790, ent(t - 3.4), 1.0, -2)
    title(fr, 'भेजो उस दोस्त को', 490, t, 108, 'FFFFFF', -2)

def sc_brand(fr, T, t):
    fr[:] = paper('3FAE5A')
    overlay(fr, cairo_layer(lambda c: logo(c, CX, 860, 200 * ent(t, .4))))
    title(fr, 'FreshNestHub', 1150, t - .3, 110, 'FFFFFF', -2, LUCKY)
    tape(fr, '@fnhtruths  |  @FreshnestHub', CX, 1300, t - .7, 'FFC93C', 40, ELITE, -1)

SCENES = dict(h1=sc_h1, h2=sc_h2, s1=sc_s1, s2=sc_s2, s3=sc_s3, s4=sc_s4, s5=sc_s5, w1=sc_w1, e1=sc_e1, e2=sc_e2)
