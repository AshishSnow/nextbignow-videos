import sys
for d in sys.argv[1:]:
    h=open(d+'/_head.py').read()
    h=h.replace("""def title(fr, txt, cy, t, size=120, fill='FFC93C', rot=-2.0, font=HI_B, cx=CX):
    put_rgba(fr, ttext(txt, size, font, fill), cx, cy, back(t / .3), clamp(t / .1), rot)""",
"""SAFE_W = 840  # phones crop ~110px each side of 9:16 on 20:9 screens
def title(fr, txt, cy, t, size=120, fill='FFC93C', rot=-2.0, font=HI_B, cx=CX):
    im = ttext(txt, size, font, fill); k = min(1.0, SAFE_W / im.shape[1])
    put_rgba(fr, im, cx, cy, back(t / .3) * k, clamp(t / .1), rot)""")
    h=h.replace("""    put_rgba(fr, tape_img(txt, size, col, font, tcol), cx, cy, back(t / .3), clamp(t / .1), rot)""",
"""    im = tape_img(txt, size, col, font, tcol); k = min(1.0, SAFE_W / im.shape[1])
    lim = min(cx - 120, W - 120 - cx) * 2
    if lim > 0: k = min(k, lim / im.shape[1])
    put_rgba(fr, im, cx, cy, back(t / .3) * k, clamp(t / .1), rot)""")
    h=h.replace("LOGO = cairo_layer(lambda c: logo(c, 112, 316, 52))","LOGO = cairo_layer(lambda c: logo(c, 200, 316, 52))")
    open(d+'/_head.py','w').write(h)
    t=open(d+'/_tail.py').read()
    t=t.replace("put_rgba(fr, logo_word(), 112 + 200, 316, 1.0, 1.0, -2)","put_rgba(fr, logo_word(), 200 + 200, 316, 1.0, 1.0, -2)")
    t=t.replace("put_rgba(fr, credit_img(CREDIT), 30, 960, 1.0, 1.0, 0)","put_rgba(fr, credit_img(CREDIT), 128, 960, 1.0, 1.0, 0)")
    open(d+'/_tail.py','w').write(t)
    print(d, h.count('SAFE_W'), 'logo200' if '200, 316, 52' in h else 'NOLOGO', '128, 960' in t)
