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

## Instagram reels (snapshot 31 Oct 2026 10:50 IST — every CHUBBY post is now >= 48 h old; eps 14-16 rows arrived)
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
| 10-31 (sched. 11:45) | 17 does sugar rot your teeth | 166 | — | — | — | — | — | — | — | — | FIRST Chubby INK episode (hand-drawn ink + paper), first 'person talking' script, Halloween-day candy + teeth, swing score |
## What the numbers say so far (update every run, keep it to the 5 most useful lines)
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
