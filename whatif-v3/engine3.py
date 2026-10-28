"""v3 episode engine: world layer -> camera/transitions -> cinematic post (grade, bloom, grain, vignette)
-> crisp UI overlay (captions, cards) -> NextBigNow watermark. Scenes: dict(k, t0, fn, ov=None, tin, grade=None)."""
import math
import skia
from engine import Episode, load_words, HERE, FPS, watermark
from toon import *
from cine import Post, grade_matrix, FULLR
from gfx import PLUS


class Episode3(Episode):
    def __init__(self, D, scenes, duration, end, post=None):
        super().__init__(D, scenes, duration, end)
        self.post = post or Post()
        self.FINAL = skia.Surface(W, H)
        self._grades = {}

    def _grade(self, S):
        g = S.get('grade')
        key = tuple(g) if g else None
        if key not in self._grades:
            self._grades[key] = skia.ColorFilters.Matrix(g or grade_matrix())
        return self._grades[key]

    def render(self, t):
        SC = self.SCENES
        cur = [S for S in SC if S['t0'] <= t < S['t1']][0]
        idx = SC.index(cur)
        c = self.CONTENT.getCanvas(); c.clear(skia.ColorBLACK)
        c.save(); cur['fn'](c, t, cur); c.restore()
        img = self.CONTENT.makeImageSnapshot()
        o = self.OUT.getCanvas(); o.clear(skia.ColorBLACK)
        dx, dy, rot = self.shake_at(t)
        z = 1.0 + min(0.05, (abs(dx) + abs(dy)) / 500)
        tin = cur.get('tin'); u = t - cur['t0']
        p = skia.Paint()
        if tin in ('punch', 'zoom') and u < 0.32:
            z *= 1 + (0.09 if tin == 'punch' else 0.22) * (1 - eo(u / 0.32))
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
        # dip to black between chapters
        if tin == 'dip' and u < 0.3:
            o.drawRect(FULLR, paint((0, 0, 0), 1 - eo(u / 0.3)))
        if nxt and nxt.get('tin') == 'dip' and t > nxt['t0'] - 0.25:
            o.drawRect(FULLR, paint((0, 0, 0), eio((t - (nxt['t0'] - 0.25)) / 0.25)))
        if tin in ('flash', 'punch') and u < 0.18:
            o.drawRect(FULLR, paint((255, 244, 230), (0.75 if tin == 'flash' else 0.35) * (1 - u / 0.18), blend=PLUS))
        for (t0, a, d, rgb) in self.FL:
            if t0 <= t < t0 + d:
                o.drawRect(FULLR, paint(rgb, a * (1 - (t - t0) / d), blend=PLUS))
        self.post.GR = self._grade(cur)
        graded = self.post.apply(self.OUT.makeImageSnapshot(), t, bloom=cur.get('bloom'))
        f = self.FINAL.getCanvas(); f.drawImage(graded, 0, 0)
        if cur.get('ov'):
            f.save(); f.translate(dx * 0.35, dy * 0.35); cur['ov'](f, t, cur); f.restore()
        f.drawImage(watermark(), 0, 0)
        return self.FINAL.makeImageSnapshot()
