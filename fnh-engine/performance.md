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

## Instagram reels (snapshot 28 Oct 2026 02:00 IST — first rows for eps 09-13)
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
| 10-26 18:00 | 07 carrots orange skin | 57 | 137 | 159 | 10.2 | 58.5 | 3 | 0 | 0 | 0 | CHUBBY v4 (approved), 2 days old |
| 10-26 22:30 | 08 pineapple eats you | 56 | 113 | 131 | 17.3 | 60.7 | 3 | 0 | 0 | 0 | CHUBBY v4, 2 days old |
| 10-27 03:25 | 09 spicy food burn | 96 | 121 | 133 | 16.5 | 62.0 | 6 | 0 | 0 | 1 | CHUBBY v4 + Mayer kit, 23 h old |
| 10-27 07:55 | 10 sugar rush myth | 118 | 1102 | 1279 | 38.9 | 67.8 | 26 | 4 | 0 | 3 | CHUBBY v4 + refutation kit, Halloween myth, 18.5 h old - BREAKOUT |
| 10-27 12:25 | 11 mint feels cold | 125 | 1206 | 1394 | 27.6 | 68.9 | 34 | 1 | 0 | 1 | CHUBBY v4 + scale cues, everyday habit (gum + water), 14 h old - BREAKOUT |
| 10-27 17:25 | 12 silver leaf on sweets | 124 | 119 | 129 | 18.8 | 62.8 | 4 | 0 | 0 | 1 | CHUBBY v4 + cast card, Indian food purity, 9 h old |
| 10-27 22:30 | 13 onions make you cry | 122 | 126 | 143 | 15.5 | 63.1 | 1 | 0 | 0 | 1 | CHUBBY v4 + chain map, 4 h old |
| 10-28 03:20 | 14 coffee doesn't give energy | ~137 | — | — | — | — | — | — | — | — | CHUBBY v4 + day graphs (charts on video), everyday habit + myth-flip |
| 10-28 (sched. 07:50) | 15 chocolate melts in your mouth | 145 | — | — | — | — | — | — | — | — | FIRST v5 LOOK (Chubby v2 3D, lit places, materials) + M2 mature voice, Halloween everyday food + belief flip (bloom isn't mould) |
## What the numbers say so far (update every run, keep it to the 5 most useful lines)
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
