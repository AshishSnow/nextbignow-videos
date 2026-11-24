"""Shared helpers for ESSAY-look reels: shape/hatch/stamp/tag primitives + frame loop + CLI (still/nframes/cover/range)."""
import sys, os, math, subprocess
from essay_lib import *


def shape(c, sh, fill, ow=4, a=1.0):
    if isinstance(sh, skia.Rect): c.drawRect(sh, P(fill, a)); c.drawRect(sh, S(INKE, ow, a))
    elif isinstance(sh, skia.RRect): c.drawRRect(sh, P(fill, a)); c.drawRRect(sh, S(INKE, ow, a))
    else: c.drawPath(sh, P(fill, a)); c.drawPath(sh, S(INKE, ow, a))


def hatch(c, clip, a=0.35, step=9, ang=1):
    c.save(); c.clipPath(clip, doAntiAlias=True); b = clip.getBounds()
    for i in range(int(b.left()) - 500, int(b.right()) + 500, step): c.drawLine(i, b.bottom(), i + 250 * ang, b.top(), S(INKE, 1.3, a))
    c.restore()


def stamp(c, x, y, txt, k, rot=-8, size=70, fill=None, col=None, border=None):
    """pop-in label box"""
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(eback(k), eback(k))
    f = anton(size); w = f.measureText(txt); h = size * 1.5
    r = rr(-w / 2 - 26, -h / 2, w + 52, h, 14)
    c.drawRRect(r, P(fill if fill is not None else CREAM)); c.drawRRect(r, S(border or ACC[0], 7))
    c.drawString(txt, -w / 2, size * 0.36, f, P(col or ACC[0])); c.restore()


def bigquote(c, lines, k, cite, dark=True, y=720, size=76):
    c.drawRect(skia.Rect.MakeXYWH(150, y - 200, 70, 70), P(ACC[0], k)); c.drawRect(skia.Rect.MakeXYWH(240, y - 200, 70, 70), P(ACC[0], k))
    f = font(size, 'Bold', False)
    for i, s_ in enumerate(lines):
        kk = eo(cl(k * 1.5 - i * 0.18)); c.drawString(s_, 150, y + i * int(size * 1.3), f, P(CREAM_T if dark else INKE, kk))
    yy = y + len(lines) * int(size * 1.3) + 20
    c.drawLine(150, yy, 200, yy, S(ACC[0], 4)); body(c, cite, 220, yy + 12, 28, MUTE, 'SemiBold', a=k)


def final_fill(c, label, num, prog, lines, k, size=124, y=580, cta='FOLLOW FOR DAILY BUSINESS BREAKDOWNS'):
    page(c, False, label=label, num=num, prog=prog, fill=ACC[0])
    f = anton(size)
    for i, s_ in enumerate(lines):
        kk = eo(cl(k * 1.6 - i * 0.2)); c.save(); c.translate(0, 40 * (1 - kk))
        c.drawString(s_, 150, y + i * int(size * 1.1), f, P(CREAM_T if i < len(lines) - 1 else INKE, kk)); c.restore()
    if cta and k > 0.6:
        g = font(30, 'Bold', False); a = cl((k - 0.6) / 0.4)
        yy = y + (len(lines) - 1) * int(size * 1.1) + 70; c.drawRect(skia.Rect.MakeXYWH(150, yy - 12, 40, 6), P(INKE, a)); c.drawString(cta, 206, yy, g, P(INKE, a))


def build(T, SCENES, DARK_S, SHAKES, fill_t, TR=0.3):
    END = T.END

    def frame(t):
        s = skia.Surface(W, H); c = s.getCanvas(); sx = sy = 0.0
        for (ts, a, d) in SHAKES:
            if ts <= t < ts + d: k = 1 - (t - ts) / d; sx += a * k * math.sin(t * 90); sy += a * k * math.cos(t * 77)
        c.save(); c.translate(sx, sy)
        i = max(j for j, (t0, _) in enumerate(SCENES) if t >= t0)
        SCENES[i][1](c, t)
        if i > 0 and t < SCENES[i][0] + TR:
            k = eio((t - SCENES[i][0]) / TR); c.save(); c.translate(-W * k, 0); SCENES[i - 1][1](c, t); c.restore()
        c.restore()
        dark = i in DARK_S or (i == len(SCENES) - 1 and t >= fill_t)
        if 0.2 < t < END + 0.1: esubs(c, T, t, dark, 1440)
        return s
    return frame


def to_np(img): return img.toarray(colorType=skia.kRGBA_8888_ColorType)[:, :, :3]


def main(HERE, frame, cover, DUR):
    out = os.path.join(HERE, 'out'); os.makedirs(out, exist_ok=True)
    if sys.argv[1] == 'still':
        for v in sys.argv[2:]: frame(float(v)).makeImageSnapshot().save(os.path.join(out, 'ig_%06.2f.png' % float(v)), skia.kPNG)
    elif sys.argv[1] == 'nframes': print(int(DUR * FPS))
    elif sys.argv[1] == 'cover':
        s = skia.Surface(W, H); cover(s.getCanvas()); s.makeImageSnapshot().save(sys.argv[2], skia.kPNG)
    elif sys.argv[1] == 'range':
        f0, f1 = int(sys.argv[2]), int(sys.argv[3])
        enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
                                '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', os.path.join(out, 'ig_%05d.mp4' % f0)], stdin=subprocess.PIPE)
        for fi in range(f0, f1): enc.stdin.write(np.ascontiguousarray(to_np(frame(fi / FPS).makeImageSnapshot())).tobytes())
        enc.stdin.close(); enc.wait()
