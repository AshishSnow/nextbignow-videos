# FreshNestHub performance log (updated by every run — step 1 of PLAYBOOK)

How to refresh (Metricool, brand 7643474, last 21 days):
- Instagram reels: `getAnalyticsDataByMetrics` with metrics
  `IGRE02 date, IGRE03 caption, IGRE06 url, IGRE11 reach, IGRE23 views, IGRE24 avg watch time (s), IGRE28 3-second view rate %,
  IGRE27 retention %, IGRE10 likes, IGRE21 shares, IGRE12 saves, IGRE07 comments`.
- YouTube: `YTVP02, YTVP17, YTVP05, YTVP06 views, YTVP08 avg view duration, YTVP09, YTVP11, YTVP12` (connector
  "videos published in range"). On 26 Oct these came back EMPTY (null) — YouTube analytics are not flowing through
  Metricool; keep trying each run and note "YT n/a" if still empty. Judge with Instagram data meanwhile.
- Only judge posts that are >= 48 h old (numbers keep growing for 2–3 days). Overwrite each row with fresh numbers.
- Derived: hold = IGRE28 (share of viewers past 3 s); watch% = avg watch / video length; shares and saves per 1k reach.

## Instagram reels (snapshot 6 Nov 2026 15:55 IST; eps 17-22 final; ep 23 ~46 h; ep 24 ~23 h)
| posted (IST) | reel | len s | reach | views | avg watch s | 3-s hold % | likes | shares | saves | comments | style |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10-20 07:03 | fake honey (10 of 13 brands) | ~45 | 5567 | 6164 | 3.8 | 16.3 | 21 | 9 | 5 | 0 | old static |
| 10-20 15:01 | blue-light glasses | ~45 | 3063 | 3119 | 1.6 | 5.2 | 3 | 1 | 0 | 0 | old static |
| 10-21 06:20 | stress hair loss | ~45 | 116 | 128 | 2.3 | 7.6 | 4 | 0 | 0 | 0 | old static |
| 10-21 15:04 | fat is breathed out | ~45 | 642 | 741 | 9.3 | 38.7 | 11 | 1 | 8 | 0 | old |
| 10-22 02:03 | Botox history | ~50 | 1242 | 1385 | 18.5 | 44.0 | 17 | 7 | 5 | 0 | old |
| 10-22 16:02 | radium face cream | ~50 | 24 | 36 | 8.8 | 33.3 | 3 | 0 | 0 | 0 | old |
| 10-23 03:12 | water by age | ~40 | 4744 | 5213 | 8.0 | 30.4 | 17 | 4 | 2 | 8 | split-screen |
| 10-23 16:38 | ambergris whale ($1.5M) | ~55 | 1112 | 1250 | 37.9 | 60.2 | 34 | 1 | 3 | 0 | realistic clips + MrBeast edit |
| 10-24 15:36 | Kim K salmon-sperm facial | ~50 | 1139 | 1242 | 19.4 | 70.6 | 4 | 1 | 0 | 0 | realistic clips |
| 10-25 12:05 | 01 face mites | ~55 | 123 | 167 | 14.5 | 58.5 | 2 | 0 | 0 | 0 | Nessa (rejected) |
| 10-25 15:47 | 02 carmine lipstick | 35 | 117 | 132 | 8.0 | 55.7 | 2 | 0 | 0 | 0 | Nessa (rejected) |
| 10-26 02:24 | 03 dandruff | 50 | 1294 | 1554 | 15.6 | 67.8 | 23 | 10 | 4 | 0 | Nessa (rejected) |
| 10-26 06:22 | 04 tattoo ink | 51 | 1048 | 1262 | 18.0 | 72.8 | 27 | 1 | 1 | 0 | Nessa (rejected) |
| 10-26 18:00 | 07 carrots orange skin | 57 | 137 | 159 | 10.2 | 58.5 | 3 | 0 | 0 | 0 | CHUBBY v4 (approved) — FINAL (5 days) |
| 10-26 22:30 | 08 pineapple eats you | 56 | 113 | 131 | 17.3 | 60.7 | 3 | 0 | 0 | 0 | CHUBBY v4 — FINAL |
| 10-27 03:25 | 09 spicy food burn | 96 | 123 | 135 | 16.3 | 61.8 | 6 | 0 | 0 | 1 | CHUBBY v4 + Mayer kit — FINAL |
| 10-27 07:55 | 10 sugar rush myth | 118 | 1108 | 1294 | 38.7 | 67.7 | 26 | 4 | 0 | 3 | CHUBBY v4 + refutation kit, Halloween myth — BREAKOUT (final) |
| 10-27 12:25 | 11 mint feels cold | 125 | 1211 | 1401 | 27.6 | 68.8 | 34 | 1 | 0 | 1 | CHUBBY v4 + scale cues, everyday habit — BREAKOUT (final) |
| 10-27 17:25 | 12 silver leaf on sweets | 124 | 120 | 129 | 18.8 | 62.8 | 4 | 0 | 0 | 1 | CHUBBY v4 + cast card, Indian food purity — FINAL |
| 10-27 22:30 | 13 onions make you cry | 122 | 1178 | 1370 | 30.6 | 65.4 | 40 | 13 | 6 | 1 | CHUBBY v4 + chain map, universal kitchen moment + 2 practical fixes — BREAKOUT (final; most shares + saves ever) |
| 10-28 03:20 | 14 coffee doesn't give energy | ~137 | 126 | 141 | 15.2 | 56.3 | 5 | 0 | 0 | 1 | CHUBBY v4 + day graphs, daily habit + belief flip — did NOT break out |
| 10-28 07:52 | 15 chocolate melts in your mouth | 145 | 1280 | 1484 | 38.7 | 74.9 | 35 | 5 | 3 | 1 | FIRST v5 LOOK + M2 voice, Halloween everyday food — BREAKOUT, best 3-s hold ever (74.9 %) |
| 10-28 12:35 | 16 swallowed gum (7-year myth) | 169 | 121 | 136 | 21.8 | 61.3 | 5 | 0 | 0 | 1 | v5 look + INSIDE-THE-GUT world, myth flip, longest video — did NOT break out |
| 10-31 12:15 | 17 does sugar rot your teeth | 166 | 1053 | 1242 | 25.0 | 64.9 | 18 | 2 | 2 | 1 | FIRST Chubby INK episode, 'person talking' script, Halloween-day candy + teeth, swing score — BREAKOUT (FINAL) |
| 10-31 17:15 | 18 why does milk boil over | 171 | 1219 | 1371 | 30.2 | 74.7 | 24 | 0 | 0 | 1 | Chubby INK ep 2: stove place, hand poses, follow-through; daily chai moment + tested fixes — BREAKOUT (FINAL), joint best hold |
| 10-31 22:35 | 19 why do cut apples turn brown | 171 | 1030 | 1142 | 16.9 | 65.5 | 38 | 3 | 4 | 1 | Chubby INK ep 3: timing & spacing kit, ink titles, lunch table; tan hook + guess beat — BREAKOUT (FINAL), MOST LIKES of the ink eps (38), best saves (4) |
| 11-01 17:20 | 20 is leftover rice safe | 172 | 1051 | 1159 | 22.1 | 72.0 | 19 | 1 | 3 | 1 | Chubby INK ep 4: camera-language kit (CCTV opener, crash zooms, dutch, rack focus), night stove; belief-flip hook + rule-of-four mnemonic; tango score — BREAKOUT (FINAL) |
| 11-02 17:10 | 21 does the fridge make bread go stale faster | 163 | 1048 | 1196 | 23.7 | 67.5 | 19 | 3 | 1 | 3 | Chubby INK ep 5: visemes, morning worktop + inside-the-slice, the staling race; sequel to rice; ragtime score — BREAKOUT (~48 h), most comments of the ink eps |
| 11-03 17:12 | 22 why does namkeen go soft | 167 | 1006 | 1111 | 39.5 | 69.9 | 6 | 0 | 3 | 1 | Chubby INK ep 6: walk cycle + parallax Diwali lane, thirst-meter plank, Indo-disco with a crunch backbeat — BREAKOUT at ~46 h, best avg watch ever (39.5 s) |
| 11-04 17:20 | 23 which Diwali sweet goes bad first | 174 | 1171 | 1312 | 26.6 | 71.2 | 18 | 25 | 5 | 1 | Chubby INK ep 7: fuse metaphor + fuse chart, growing mould, corridor re-gift on arcs, screenshot card, STEPPS script, spaghetti-western score — ~46 h, RECORD SHARES (25) |
| 11-05 16:53 | 24 does the iodine test catch fake paneer | 173 | 1161 | 1293 | 34.5 | 80.0 | 24 | 0 | 3 | 1 | Chubby INK ep 8: speed-ramp opener, guard metaphor, starch spring, diner, 70s crime funk — ~23 h, RECORD 3-S HOLD (80.0 %), 0 shares; judge 7 Nov |
| 11-06 17:34 | 25 can you test ghee at home | 173 | — | — | — | — | — | — | — | — | Chubby INK ep 9: palm-tree hook, court + Judge Chubby, translucent ghee, verdict board card, qawwali score — judge 8 Nov |
## What the numbers say so far (update every run, keep it to the 5 most useful lines)
- 6 Nov 15:55: paneer holds 80.0 % past 3 s at ~23 h, the best ever by 5 points, and 34.5 s avg watch: a slow-motion drop that makes you wait for the landing beats every gag so far. But 0 shares, with a card and a send line, while sweets kept 25 on a list. So the card + send line alone are not the send design; a LIST people want to keep, about something in the house this week, may be. One pair of videos, could be timing. Ep 25 tests a list + a gag hook. YouTube: 0-3 views per Short, rows to 3 Nov.
- 5 Nov 15:55: ep 23 has 25 shares in ~22 h, against 0-3 on every other ink ep and 13 on onions, our old record. The send design (list + screenshot card + a line aimed at one person) looks like the first thing to move sends; one data point, could also be the timing. Namkeen recovered: 1006 reach, 39.5 s avg watch, so yesterday's 'late row or first miss' was late. YouTube rows still end 31 Oct.
- 4 Nov 15:50: rice 1051, bread 1048 at ~48 h: five finished ink eps in the 1029-1219 band. Namkeen is 288 at ~17 h (bread was 1043 at 23 h): late row or first miss, judge 5 Nov. YouTube rows reach only 31 Oct (milk 3 views, apples 0): still no distribution, judge monthly. Shares still 0-3; ep 23 is the first script designed for sends.
- 3 Nov 15:50: FIVE of five ink episodes sit in one narrow band: 1028-1219 reach (candy 1051, milk 1219, apples 1028, rice 1049, bread 1043 in 23 h). A band that tight looks like a ceiling of the first distribution batch, not a verdict on each video; what would break it is SENDS (still 0-3 per reel; onions' 13 is the record). Hold: milk 74.7, rice 71.9, bread 67.4, apples 65.5, candy 64.9: the hammer gag held worse than the CCTV gag, so a clear ACCIDENT to the food beats a joke with an object. Shorter did not raise watch seconds (2:43 = 23.8 s vs 2:52 = 22.2 s). Ep 22 tests a walking hook where the food itself fails in his hand, and a Diwali-week send line.
- 2 Nov 15:50: ALL FOUR ink episodes passed 1k reach (candy 1049, apples 1024, rice 1034 in only 22 h, milk 1217) -> 8 of the last 10 Chubby posts broke 1k, the ink look is now the safest thing we do. Avg watch swings with the topic (milk 30 s, candy 25 s, rice 22 s, apples 17 s), 3-s hold with the first second (milk boil-over 74.7 %, CCTV rice 72.1 % vs apples / candy 65 %): a physical accident or a surveillance gag at frame 0 beats a slow change. Shares stay low (0-3) and the mnemonic on rice did not move them yet (1 share at 22 h). Ep 21 shortens the video to 2:43 and tests a comic physical gag at frame 0 (hammering a nail with bread).
- 1 Nov 15:50: fresh rows at last. The ink look holds as well as the 3D look or better: milk 75.0 % 3-s hold (best ever) / 1204 reach / 30.2 s
  avg watch; candy+teeth 65.2 % / 1043 / 25.3 s; apples 68.5 % (17 h, still growing). 6 of the last 8 Chubby posts passed 1k reach, all of them a
  food in people's hands that week. Shares stay low on the ink eps (0-2) -> ep 20 adds a repeatable one-line rule to SEND (rule-of-four mnemonic).
- 31 Oct 21:40: reel rows STILL identical to 10:50 (third identical snapshot today; eps 17 + 18 have no rows at 9.5 h / 4.5 h) -> the reel
  rows refresh at most once or twice a day now; no new verdict. Ep 19 keeps the in-your-hand rule (a browning apple) + a belief flip (brown =
  bad? no) + a cheap tested fix; judge eps 17-19 at 48 h (2 Nov).
- 31 Oct 16:00: every reel row IDENTICAL to 10:50 (Metricool refreshes the reel rows a few times a day; ep 17 posted 12:15 has no row yet) ->
  no new verdict this run. Ep 18 keeps the two rules the data supports: a food-in-your-hand-this-week moment (milk boiling over) + a practical,
  tested fix ranking (shares/saves). Judge ep 17 (first ink look: 3-s hold vs chocolate 74.9 %) and ep 18 at 48 h (2 Nov).
- 31 Oct 10:50 (first fresh snapshot since 28 Oct; all posts >= 48 h): FOUR breakouts now — sugar rush 1108, mint 1211, onions 1178 (13 shares,
  6 saves = our best share/save numbers ever), chocolate 1280 (74.9 % hold = best ever, 38.7 s avg watch on 2:25). Coffee (126), gum (121),
  silver (120), spicy (123) stayed at the ~120 floor. The 'belief flip' alone does NOT predict reach (coffee + gum were belief flips and
  stalled); what the 4 winners share is a FOOD-IN-YOUR-HAND moment everyone has had THIS WEEK (candy, gum + ice water, cutting onions,
  chocolate) and a short, concrete title question. Shares/saves follow a PRACTICAL fix (onions: sharp knife + slow cuts). Hold is 56-75 % on
  all of them, so the hook works; the v5 look + M2 voice (chocolate) got the best hold.
- 31 Oct: YouTube rows now flow (up to 28 Oct) but every Short has 0-3 views (silver 3, 27 s avg) — the YT channel has no distribution yet;
  keep posting (originality + SEO titles) and judge YT monthly, not per video.
- 28 Oct 10:50: reel rows IDENTICAL to 02:00 and 05:50 (3rd identical snapshot); coffee + chocolate still missing -> Metricool's Instagram
  sync is stalled ~9 h; YouTube rows still end 25 Oct. No new verdicts possible; judge eps 14-16 once rows refresh (48 h rule).
- 28 Oct 05:50: all rows identical to the 02:00 snapshot; coffee (03:20) not in analytics yet -> refresh on daytime runs; ep 15 is the
  first v5-look + M2-voice reel: compare its 3-s hold / avg watch with eps 09-14 at 48 h (30 Oct 07:50).
- 28 Oct 02:00: two CHUBBY videos BROKE OUT: sugar rush (1102 reach, 38.9 s avg watch = 33 % of 1:58, 4 shares, 3 comments) and
  mint (1206 reach, 27.6 s, 34 likes). Both = an everyday experience everyone has had + a "you were wrong" twist (myth / brain trick).
  Spicy/silver/onions (~120 reach) were niche or explained a mechanism without a belief to flip. Hold is 62-69 % for ALL of them,
  so the hook works; the TOPIC decides who gets shown it. Longer videos still earn more absolute watch seconds (Mosseri's signal).
- Best 3-second hold: realistic-looking openings (Kim K 70.6 %, ambergris 60.2 %); animated Nessa reels held 56–58 %;
  static/talky openings 5–16 %. => The first frame must show strong motion + a clear question instantly.
- Longest watch: ambergris (37.9 s avg) — money stakes + story + MrBeast pacing keeps people watching.
- Biggest reach came from broad, useful, "is your X fake / how much water" topics, even with weak hold — topic pull
  matters. Prefer topics everyone has (food in their kitchen, daily habits) over niche science.
- Shares/saves are rare (max 9 shares) — make every video "send-worthy": a surprising fact + a practical takeaway.
- YouTube numbers via Metricool: still only rows up to 25 Oct at 02:00 on 28 Oct (ambergris 2 views); no rows for any CHUBBY video yet. Keep checking.
- 27 Oct 21:00: eps 09-12 published on IG but still missing from reel analytics (09 is 17.5 h old) -> lag > 17 h; judge at 48 h only.
- 27 Oct 11:00: carrots/pineapple numbers identical to 06:00 — reach fully stopped at 12–17 h. Ep 11 tests a sequel/series hook.
- 27 Oct: CHUBBY pineapple held 72.2 % past 3 s in its first hours (best with tattoo 72.8 %) — an absurd action in
  frame 0-1 s works. Judge reach/watch at 48 h (28 Oct 22:30 IST).
- 27 Oct 06:00: CHUBBY reach stalls at ~90–130 within 8–12 h despite 58–72 % 3-s hold; Nessa-era dandruff/tattoo reached
  1.0–1.3k. Distribution, not the hook, is the bottleneck -> test broad timely topics (ep 10 Halloween) and judge at 48 h.
