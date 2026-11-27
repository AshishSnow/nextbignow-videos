"""BUSINESS TRICKS · EP 01 (YouTube 16:9) — Why McDonald's really wants you on the app. PAPER wide look."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
os.environ.setdefault('OMB_WIDE', '1')
from wide_props import *

ASSETS = {'fries': ('fries.bin',), 'burger': ('burger2.bin',), 'coffee': ('coffee.bin',), 'rider': ('rider.bin',)}
RED = (232, 70, 60); GOLD = (255, 196, 60); GRN = (80, 160, 110)
L, R_, CX = 600, 1340, 960     # left column, right column, centre


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        # COLD OPEN
        dict(at=0.0, bg=PAPER_C, photos=[('fries', R_, 560, 640, -4, 0.0)], props=[(D_phone('deal', accent=RED), 640, 560, 330, 640, 4, 'download')],
             cap=(930, 52, INK, 'sounds like'), words=[('$1', 1650, 330, 170, RED, 'one dollar')]),
        dict(at='sounds like', bg=P, photos=[('fries', CX, 560, 560, 3, None)], words=[('BAIT.', CX, 300, 200, H, 'bait')], cap=(930, 50, CREAM, None), shake='bait'),
        dict(at='here are the', bg=D, chapter=('BUSINESS TRICKS · EP 01', 'Why they want you on the app'), cap=(930, 50, CREAM, None)),
        # TRICK 1
        dict(at='trick number one', bg=P, chapter=('TRICK 1', 'The bait')),
        dict(at="download the mcdonald's", bg=PAPER_C, props=[(D_phone('points', accent=RED), L, 560, 330, 640, -3, None)],
             labels=[('FREE LARGE FRIES', R_, 420, 72, -3, 'free large'), ('+1,500 POINTS', R_, 560, 72, 3, 'fifteen hundred', RED, (255, 250, 240)),
                     ('BURGER KING: CROWNS', R_, 700, 54, -2, 'crowns'), ('STARBUCKS: STARS', R_, 800, 54, 2, 'stars')]),
        dict(at="the gift isn't", bg=D, props=[(D_phone('icons', accent=RED), L, 560, 330, 640, 4, None)], cap=(930, 50, CREAM, None),
             words=[('THE REAL PRIZE:', R_, 440, 90, CREAM, 'the point is'), ('YOUR HOME SCREEN', R_, 560, 90, H, 'home screen')]),
        # TRICK 2
        dict(at='trick number two', bg=P, chapter=('TRICK 2', 'The frequency machine')),
        dict(at='mcdonald\'s says', bg=PAPER_C, props=[(D_chart([10.5, 26], ['BEFORE THE APP', 'AFTER JOINING'], [(200, 190, 210), RED], title='VISITS PER YEAR (US AVERAGE)',
                                                                source='McDonald\'s Q4 2025 earnings call'), CX, 560, 900, 640, 0, 'ten times')],
             words=[('2.5x', 1650, 300, 150, RED, 'twenty six')]),
        dict(at='same person', bg=D, photos=[('burger', L, 560, 560, -4, None)], cap=(930, 46, CREAM, 'that\'s why'),
             words=[('SAME BURGERS.', R_, 420, 90, CREAM, 'same burgers'), ('2.5x THE VISITS', R_, 560, 90, H, 'two and a half')]),
        dict(at="that's why mcdonald's", bg=P, props=[(D_text('210M', 220, INK, sub='ACTIVE APP USERS (90 DAYS)'), L, 520, 640, 380, -3, 'two hundred and ten'),
                                                    (D_text('250M', 220, RED, sub='TARGET BY END OF 2027'), R_, 560, 640, 380, 3, 'two hundred and fifty')],
             cap=(950, 46, CREAM, 'it already')),
        # DECISION
        dict(at='and that\'s why the old', bg=D, photos=[('fries', L, 560, 520, -4, None)], cap=(930, 48, CREAM, 'mcdonald\'s ceo'),
             labels=[('NATIONAL DEAL = DISCOUNT FOR EVERYONE', R_, 520, 50, 3, 'national deal', H)]),
        dict(at='mcdonald\'s ceo', bg=PAPER_C, props=[(D_quote(['"There\'s a lot', 'of waste in that."'], 'MCDONALD\'S CEO, ON NATIONAL DEALS', size=96), CX, 520, 1200, 520, 0, None)]),
        dict(at='so the deals moved', bg=P, props=[(D_phone('deal', accent=RED), L, 560, 330, 640, -4, None)], cap=(930, 48, CREAM, "when domino's"),
             words=[('YOU GET A DEAL.', R_, 440, 90, CREAM, 'who gets'), ('THEY DON\'T.', R_, 560, 90, H, "who doesn't")],
             labels=[('$7.99 CARRYOUT = DIGITAL ONLY', R_, 720, 52, -3, 'digital only', RED, (255, 250, 240))]),
        # TRICK 3
        dict(at='trick number three', bg=D, chapter=('TRICK 3', 'Points that shrink')),
        dict(at='your points are', bg=P, photos=[('coffee', R_, 560, 520, 4, None)], words=[('THEY SET THE', L, 470, 100, CREAM, 'controls'), ('EXCHANGE RATE.', L, 600, 100, H, 'exchange rate')]),
        dict(at='in february', bg=PAPER_C, props=[(D_beforeafter([('Cheapest reward', '50', '100'), ('Free drink', '150', '200'), ('Next tier', '200', '300')], head=('BEFORE (STARS)', 'FEB 2023')),
                                                   CX, 540, 1000, 480, 0, 'the cheapest')], cap=(960, 44, INK, None)),
        dict(at='and it works', bg=D, photos=[('coffee', L, 560, 460, -4, None)], props=[(D_text('~60%', 200, INK, sub='OF US COMPANY-OPERATED REVENUE'), R_, 480, 640, 360, 3, 'sixty percent')],
             labels=[('"4+ VISITS A WEEK"', R_, 760, 60, -3, 'four times', H)]),
        # TRICK 4
        dict(at='trick number four', bg=P, chapter=('TRICK 4', 'The billboard in your pocket')),
        dict(at='it knows what', bg=PAPER_C, props=[(D_phone('icons', accent=RED), L, 560, 330, 640, -3, None)],
             labels=[('WHAT YOU ORDER', R_, 400, 60, -3, 'what you order'), ('WHAT TIME', R_, 540, 60, 3, 'what time'), ('WHICH DEALS WORK ON YOU', R_, 680, 60, -2, 'which deals', RED, (255, 250, 240))]),
        dict(at='one app analyst', bg=D, props=[(D_notif('LUNCH IS CALLING', 'Your deal ends today', accent=RED), R_, 560, 620, 150, 2, 'push notification')],
             words=[('"THE BILLBOARD AD', L, 460, 80, CREAM, 'billboard ad'), ('THAT KEEPS GIVING"', L, 570, 80, H, 'keeps giving')], cap=(930, 46, CREAM, None)),
        # TRICK 5
        dict(at='trick number five', bg=P, chapter=('TRICK 5', 'Prices that move')),
        dict(at='in twenty twenty four', bg=PAPER_C, props=[(D_text('$20M', 200, INK, sub='DIGITAL MENU BOARDS (WENDY\'S, 2024)'), L, 520, 700, 380, -3, 'twenty million')],
             labels=[('"DYNAMIC PRICING"', R_, 440, 66, 3, 'dynamic'), ('INTERNET: "SURGE PRICING?!"', R_, 580, 56, -3, 'the internet', RED, (255, 250, 240)),
                     ('"WILL NOT IMPLEMENT SURGE PRICING"', R_, 740, 46, 2, 'would not')]),
        dict(at='but the idea', bg=D, cap=(930, 44, CREAM, None), labels=[('FTC, AUG 2026: PERSONALIZED PRICING POLICY', CX, 250, 56, -2, 'federal trade', H)],
             props=[(D_chart([100, 107], ['SHOPPER A', 'SHOPPER B'], [(200, 190, 210), RED], title='SAME GROCERY BASKET (INSTACART TEST, AVG)', unit='', source='Consumer Reports + partners, Dec 2025'),
                     CX, 600, 760, 480, 0, 'same basket')]),
        # TRICK 6
        dict(at='trick number six', bg=P, chapter=('TRICK 6', 'The convenience tax')),
        dict(at='a lendingtree', bg=PAPER_C, photos=[('rider', L, 560, 520, -4, None)],
             props=[(D_chart([100, 180], ['PICKUP', 'DELIVERED'], [(200, 190, 210), RED], title='SAME MEAL, PRICE INDEX', source='LendingTree study'), R_, 560, 640, 560, 2, 'eighty percent')]),
        # WHAT TO DO
        dict(at='so, should you', bg=D, photos=[('fries', CX, 600, 520, 3, 'take the free')], words=[('DELETE THE APP?', CX, 300, 120, CREAM, None), ('NOT REALLY.', CX, 430, 110, H, 'not really')]),
        dict(at='just play it', bg=PAPER_C, labels=[('1. TURN OFF NOTIFICATIONS', CX, 330, 64, -2, 'turn off'), ('2. USE POINTS BEFORE THE RULES CHANGE', CX, 470, 56, 2, 'use your points'),
                                                  ('3. PICKUP, NOT DELIVERY', CX, 610, 64, -2, 'order pickup', RED, (255, 250, 240)), ('4. CHECK THE COUNTER PRICE', CX, 750, 64, 2, 'check the price')]),
        dict(at='because the app', bg=P, photos=[('fries', L, 560, 520, -4, None)], words=[('TAKE THE FRIES.', R_, 460, 100, CREAM, 'take the fries'), ('KNOW WHAT YOU\'RE', R_, 600, 80, H, 'just know'),
                                                                                   ('PAYING WITH.', R_, 700, 80, H, 'paying with')]),
        dict(at='we break down', bg=PAPER_C, cap=(930, 46, (40, 20, 60), None)),
    ]


S = WideStory(HERE, 'BUSINESS TRICKS', 'EP 01', scenes, ASSETS, cover_at=lambda S: S.ph('bait') + 0.5)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
