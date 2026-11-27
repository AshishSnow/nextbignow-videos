"""BUSINESS IDEA N° 05 — the Pet Rock: over a million plain rocks sold in 1975. PAPER look (paper_story)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
from paper_story import *
ST = S   # stroke paint helper (S is reused for the Story below)

ASSETS = {'rock': ('rocks.bin', 'warm', (0.40, 0.30, 0.62, 0.62)), 'rocks': ('rocks.bin',), 'beach': ('beach.bin',), 'bar': ('bar.bin', 'sepia'), 'dog': ('dogpet.bin', 'warm', (0.18, 0.25, 0.82, 0.70))}


def D_box(c):
    """pet carrier box: cardboard with air holes, straw, a rock peeking out"""
    c.drawRRect(rr(-220, -120, 440, 260, 14), P((196, 150, 96))); c.drawRRect(rr(-220, -120, 440, 260, 14), ST(INK, 5))
    c.drawLine(-220, -40, 220, -40, ST(INK, 3, 0.6))
    for i in range(5): c.drawCircle(-140 + i * 70, 40, 16, P(INK))
    for i in range(14): c.drawLine(-200 + i * 30, -120, -190 + i * 30 + (i % 3) * 8, -165 - (i % 4) * 8, ST((230, 200, 110), 5))
    c.drawOval(skia.Rect.MakeXYWH(-90, -200, 180, 120), P((140, 136, 130))); c.drawOval(skia.Rect.MakeXYWH(-90, -200, 180, 120), ST(INK, 4))


def D_manual(c):
    c.drawRect(skia.Rect.MakeXYWH(-180, -230, 360, 460), P((250, 246, 230))); c.drawRect(skia.Rect.MakeXYWH(-180, -230, 360, 460), ST(INK, 5))
    f = cond(50); g = serif(40)
    for i, s in enumerate(('CARE &', 'TRAINING')): c.drawString(s, -f.measureText(s) / 2, -120 + i * 56, f, P(INK))
    for i, s in enumerate(('sit.', 'stay.', 'play dead.')): c.drawString(s, -g.measureText(s) / 2, 40 + i * 56, g, P((120, 60, 40)))


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, photos=[('rock', 540, 1080, 660, -4, 0.0)], cap=(560, 66, INK, 'over a million'), arrow=(240, 660, 400, 880, 0.4)),
        dict(at='over a million', bg=P, photos=[('rocks', 540, 1140, 760, 4, None)], words=[('1,000,000+', 540, 600, 190, H, None), ('ROCKS.', 540, 790, 170, CREAM, 'rocks')], shake='rocks'),
        dict(at='regular rocks', bg=D, photos=[('rock', 450, 1000, 520, -3, None)], words=[('REGULAR', 540, 560, 160, CREAM, None)],
             props=[(D_text('$4', 200, INK, sub='EACH'), 760, 1360, 340, 260, 6, 'four dollars')]),
        dict(at='gary dahl', bg=P, photos=[('bar', 540, 1130, 540, -3, None)], labels=[('GARY DAHL, AD MAN', 540, 1440, 64, 3, None, H)], cap=(560, 62, CREAM, 'so he joked')),
        dict(at='so he joked', bg=D, photos=[('dog', 330, 900, 420, -6, None), ('rock', 740, 1090, 400, 6, 'is a rock')],
             words=[('THE PERFECT PET', 540, 560, 120, CREAM, 'the perfect'), ('IS A ROCK.', 540, 1450, 150, H, 'is a rock')]),
        dict(at='then he actually', bg=P, words=[('THEN HE', 540, 820, 170, CREAM, None), ('DID IT.', 540, 1010, 190, H, 'did it')], shake='did it'),
        dict(at='rocks from', bg=D, photos=[('beach', 540, 1100, 800, -3, None)], cap=(560, 62, CREAM, None),
             labels=[('< 1¢ EACH', 540, 1440, 80, 3, 'less than', H)]),
        dict(at='a little box', bg=P, props=[(D_box, 540, 1100, 620, 520, -3, None)], cap=(560, 62, CREAM, 'and a manual'),
             labels=[('AIR HOLES', 300, 1460, 56, -5, 'air holes'), ('STRAW', 780, 1480, 56, 5, 'straw', H)]),
        dict(at='and a manual', bg=D, props=[(D_manual, 540, 1080, 460, 560, 3, None)], cap=(560, 62, CREAM, None)),
        dict(at='the most popular', bg=P, photos=[('rock', 540, 1150, 560, -8, None)], cap=(560, 64, CREAM, 'play dead'),
             words=[('PLAY DEAD.', 540, 760, 200, H, 'play dead')], shake='dead'),
        dict(at='he made', bg=D, props=[(D_text('95¢', 260, INK, sub='PROFIT PER ROCK'), 540, 1000, 700, 420, -3, 'ninety five')],
             cap=(560, 62, CREAM, 'and became'), words=[('MILLIONAIRE', 540, 1440, 150, H, 'millionaire')]),
        dict(at="he didn't", bg=P, photos=[('rock', 540, 1160, 520, 4, None)], words=[("HE DIDN'T SELL", 540, 560, 120, CREAM, None), ('A ROCK.', 540, 720, 150, CREAM, 'a rock')],
             labels=[('HE SOLD A JOKE.', 540, 1440, 84, -3, 'he sold', H)]),
        dict(at='send this', bg=PAPER_C, photos=[('rocks', 540, 800, 560, -3, None)], cap=(1180, 64, (40, 20, 60), None)),
    ]


S = Story(HERE, 'BUSINESS IDEA', 'N° 05', scenes, ASSETS, cover_at=lambda S: S.ph('rocks') + 0.6)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
