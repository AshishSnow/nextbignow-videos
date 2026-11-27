"""CASE STUDY N° 06 — Bubble Wrap was supposed to be wallpaper. PAPER look (paper_story)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
from paper_story import *

ASSETS = {'wrap': ('wrap.bin',), 'wrap2': ('wrap2.bin',), 'curtain': ('wallp.bin',), 'wall': ('wall.bin',), 'green': ('green.bin',),
          'ibm': ('ibm.bin', 'sepia'), 'box': ('box.bin',)}


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, photos=[('wrap', 540, 1070, 720, -4, 0.0)], cap=(560, 70, INK, 'was supposed'), arrow=(240, 650, 400, 880, 0.3)),
        dict(at='was supposed', bg=P, photos=[('wall', 540, 1120, 640, 4, None)], words=[('ON YOUR', 540, 560, 170, CREAM, 'your walls'), ('WALLS.', 540, 750, 210, H, 'walls')], shake='walls'),
        dict(at='in nineteen fifty', bg=D, props=[(D_text('1957', 240, INK, sub='NEW JERSEY'), 540, 1040, 640, 400, -3, None)], cap=(560, 62, CREAM, 'sealed')),
        dict(at='sealed two', bg=P, photos=[('curtain', 540, 1080, 620, -3, None)], cap=(560, 60, CREAM, 'textured'),
             labels=[('2 SHOWER CURTAINS', 540, 1440, 66, 3, 'shower', H)]),
        dict(at='textured wallpaper', bg=D, photos=[('wrap2', 540, 1120, 640, 4, None)], words=[('TEXTURED', 540, 560, 160, CREAM, None), ('WALLPAPER.', 540, 740, 170, H, 'wallpaper')]),
        dict(at='nobody wanted', bg=P, photos=[('wall', 540, 1150, 560, -5, None)], words=[('NOBODY', 540, 560, 190, CREAM, None), ('WANTED IT.', 540, 750, 170, H, 'wanted')]),
        dict(at='so they tried', bg=D, photos=[('green', 540, 1060, 720, 3, None)], cap=(560, 60, CREAM, 'that flopped'),
             words=[('FLOPPED TOO.', 540, 1440, 140, H, 'flopped')]),
        dict(at='then ibm', bg=P, photos=[('ibm', 540, 1080, 760, -3, None)], cap=(560, 60, CREAM, 'and needed'), labels=[('A NEW COMPUTER', 540, 1440, 72, 3, 'new computer', H)]),
        dict(at='and needed', bg=D, photos=[('box', 540, 1150, 600, 4, None)], words=[('SHIP IT', 540, 560, 170, CREAM, 'ship it'), ('WITHOUT BREAKING IT.', 540, 720, 90, H, 'without')]),
        dict(at='bubble wrap was the', bg=P, photos=[('wrap', 540, 1150, 680, -3, None)], words=[('THE ANSWER.', 540, 640, 150, H, 'answer')], shake='answer'),
        dict(at='the wallpaper flop', bg=D, photos=[('wall', 330, 900, 420, -6, None), ('box', 740, 1120, 420, 6, 'packaging')],
             labels=[('FLOP', 330, 1150, 70, -4, None), ('PACKAGING', 740, 1380, 70, 4, 'packaging', H)]),
        dict(at='and this april', bg=P, props=[(D_text('$10B', 260, INK, sub='SEALED AIR DEAL, APRIL'), 540, 1060, 700, 420, -3, 'ten billion')],
             cap=(560, 60, CREAM, None), shake='ten billion'),
        dict(at='the product was', bg=D, words=[('NEVER', 540, 760, 200, CREAM, 'never'), ('THE PROBLEM.', 540, 950, 160, CREAM, 'the problem'),
                                                ('THE CUSTOMER', 540, 1200, 150, H, 'the customer'), ('WAS.', 540, 1370, 170, H, 'was send')]),
        dict(at='send this', bg=PAPER_C, photos=[('wrap2', 540, 800, 560, -3, None)], cap=(1180, 64, (40, 20, 60), None)),
    ]


S = Story(HERE, 'CASE STUDY', 'N° 06', scenes, ASSETS, cover_at=lambda S: S.ph('wallpaper', after=S.ph('textured')) + 0.3)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
