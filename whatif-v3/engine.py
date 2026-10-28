"""Shared What-If episode engine: word timings, transitions, shakes, NextBigNow watermark, render/guide/encode CLI."""
import sys, os, math, json, re, subprocess, time
import skia
from toon import *

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
FULL = R.MakeWH(W, H)

def load_words(D):
    al = [x for x in json.load(open(os.path.join(D, 'align.json'))) if x[0] not in ('<s>', '</s>', '<sil>')]
    return [(re.sub(r'\(\d\)', '', w), a, b) for w, a, b in al]

def finder(WT):
    """wk('word', n) -> start time of the n-th (1-based) occurrence of a spoken word."""
    def wk(word, n=1, end=False):
        word = word.lower(); k = 0
        for w, a, b in WT:
            if w.lower().strip("'") == word or w.lower() == word:
                k += 1
                if k == n: return b if end else a
        raise KeyError('%s #%d not in script' % (word, n))
    return wk

_WM = None
def watermark():
    global _WM
    if _WM is None:
        _WM = skia.Image.open(os.path.join(HERE, 'brand_wm_land.png' if LAND else 'brand_wm.png'))
    return _WM

class Episode:
    def __init__(self, D, scenes, duration, end):
        self.D, self.SCENES, self.DURATION, self.END = D, scenes, duration, end
        for i, S in enumerate(scenes):
            S['t1'] = scenes[i + 1]['t0'] if i + 1 < len(scenes) else duration + 1
        self.SH = []
        self.FL = []
        self.CONTENT = skia.Surface(W, H); self.OUT = skia.Surface(W, H)
        self.VIGN = paint(shader=rad(W / 2, H / 2, max(W, H) * 0.68, [argb((0, 0, 0), 0), argb((0, 0, 0), 0), argb((0, 0, 0), 0.2)], [0, 0.6, 1]))

    def shk(self, t0, amp, dec=0.25, fq=15):
        self.SH.append((t0, amp, dec, fq))

    def flash(self, t0, a=0.6, d=0.18, rgb=(255, 255, 255)):
        self.FL.append((t0, a, d, rgb))

    def shake_at(self, t):
        dx = dy = rot = 0.0
        for (t0, amp, dec, fq) in self.SH:
            u = t - t0
            if 0 <= u < dec * 4:
                e = amp * math.exp(-u / dec)
                dx += e * math.sin(u * fq * 6.283 + t0 * 3.1); dy += e * 0.8 * math.sin(u * fq * 7.1 + t0)
                rot += e * 0.03 * math.sin(u * fq * 5 + t0)
        return dx, dy, rot

    def render(self, t):
        SC = self.SCENES
        cur = [S for S in SC if S['t0'] <= t < S['t1']][0]
        idx = SC.index(cur)
        c = self.CONTENT.getCanvas(); c.clear(skia.ColorWHITE)
        c.save(); cur['fn'](c, t, cur); c.restore()
        img = self.CONTENT.makeImageSnapshot()
        o = self.OUT.getCanvas(); o.clear(skia.ColorBLACK)
        dx, dy, rot = self.shake_at(t)
        z = 1.0 + min(0.05, (abs(dx) + abs(dy)) / 500)
        tin = cur.get('tin'); u = t - cur['t0']
        p = skia.Paint()
        TR = 0.32
        if tin == 'zoom' and u < TR:
            z *= 1 + 0.25 * (1 - eo(u / TR))
        if tin == 'whip' and u < 0.16:
            k = 1 - u / 0.16
            dx += 500 * k * k
            p.setImageFilter(skia.ImageFilters.Blur(60 * k, 2, skia.TileMode.kClamp, None))
        nxt = SC[idx + 1] if idx + 1 < len(SC) else None
        if nxt and nxt.get('tin') == 'whip' and t > nxt['t0'] - 0.1:
            k = (t - (nxt['t0'] - 0.1)) / 0.1
            dx -= 500 * k * k
            p.setImageFilter(skia.ImageFilters.Blur(60 * k, 2, skia.TileMode.kClamp, None))
        p.setShader(img.makeShader(skia.TileMode.kMirror, skia.TileMode.kMirror, LINS))
        o.save(); o.translate(W / 2 + dx, H / 2 + dy); o.rotate(rot); o.scale(z, z); o.translate(-W / 2, -H / 2)
        o.drawRect(R.MakeXYWH(-400, -400, W + 800, H + 800), p)
        o.restore()
        if nxt and nxt.get('tin') == 'wipe' and t > nxt['t0'] - TR:
            k = eio((t - (nxt['t0'] - TR)) / TR)
            o.drawCircle(W / 2, H * 0.47, max(W, H) * 0.66 * k, paint(nxt['col']))
        if tin == 'flash' and u < 0.2:
            o.drawRect(FULL, paint((255, 255, 255), 0.8 * (1 - u / 0.2), blend=skia.BlendMode.kPlus))
        for (t0, a, d, rgb) in self.FL:
            if t0 <= t < t0 + d:
                o.drawRect(FULL, paint(rgb, a * (1 - (t - t0) / d), blend=skia.BlendMode.kPlus))
        o.drawRect(FULL, self.VIGN)
        o.drawImage(watermark(), 0, 0)
        return self.OUT.makeImageSnapshot()

    def guide_overlay(self, img):
        s = skia.Surface(W, H); c = s.getCanvas(); c.drawImage(img, 0, 0)
        red = paint((255, 0, 0), 0.28)
        if LAND:
            c.drawRect(R.MakeXYWH(0, 0, W, 54), red); c.drawRect(R.MakeXYWH(0, H - 120, W, 120), red)
            c.drawRect(R.MakeXYWH(0, 54, 96, H - 174), red); c.drawRect(R.MakeXYWH(W - 96, 54, 96, H - 174), red)
            return s.makeImageSnapshot()
        c.drawRect(R.MakeXYWH(0, 0, W, 250), red); c.drawRect(R.MakeXYWH(0, H - 420, W, 420), red)
        c.drawRect(R.MakeXYWH(W - 120, 250, 120, H - 670), red); c.drawRect(R.MakeXYWH(0, 250, 60, H - 670), red)
        cw = 1920 * 9 / 20
        c.drawLine((W - cw) / 2, 0, (W - cw) / 2, H, stroke((255, 0, 255), 3)); c.drawLine((W + cw) / 2, 0, (W + cw) / 2, H, stroke((255, 0, 255), 3))
        return s.makeImageSnapshot()

    def main(self, argv):
        mode = argv[1]
        if mode in ('still', 'guide'):
            od = os.path.join(self.D, 'stills'); os.makedirs(od, exist_ok=True)
            for v in argv[2:]:
                img = self.render(float(v))
                if mode == 'guide': img = self.guide_overlay(img)
                img.save(os.path.join(od, ('g_' if mode == 'guide' else 'f_') + '%06.2f.png' % float(v)), skia.kPNG)
            return
        if mode == 'nframes':
            print(int(round(self.DURATION * FPS))); return
        f0, f1, out = int(argv[2]), int(argv[3]), argv[4]
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', '%dx%d' % (W, H), '-r', str(FPS),
               '-i', '-', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14',
               '-profile:v', 'high', '-level', '4.2', '-x264-params', 'keyint=60:min-keyint=30', '-threads', '2',
               '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', out]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        st = time.time()
        for f in range(f0, f1):
            p.stdin.write(self.render(f / FPS).toarray().tobytes())
            if (f - f0) % 150 == 0: print('frame %d/%d %.1fs' % (f - f0, f1 - f0, time.time() - st), flush=True)
        p.stdin.close(); p.wait()
        print('done', out, time.time() - st)
