# OopsMyBusiness — what our videos actually did

Update every run (Metricool `getAnalyticsDataByMetrics`, brand 7643430, last 21 days):
- Instagram reels fields: `IGRE02` date, `IGRE03` caption, `IGRE23` views, `IGRE11` reach, `IGRE24` avg watch time (s),
  `IGRE28` 3-second view rate (%), `IGRE21` shares, `IGRE12` saves, `IGRE10` likes, `IGRE07` comments.
- YouTube fields: `YTVP02` date, `YTVP17` title, `YTVP06` views, `YTVP08` avg view duration, `YTVP09` likes, `YTVP12` shares.
  Numbers arrive since 27 Oct (views + avg view duration in s; likes/shares not checked yet). The "all videos" connector
  (`YTVV*`) returned nothing on 26 Oct. Pull `YTVP02,YTVP17,YTVP06,YTVP08` every run into the YouTube table below.
- Instagram numbers for posts published the same day are usually empty — read them the next run.
Add new rows, refresh rows younger than 7 days, then rewrite the **Insights** section from the data.

## Snapshot 2026-11-12 ~03:05 IST (episode run: HOW IT WORKS EP 6, cash pays card rewards)
Delivery (getScheduledPosts 8–12 Nov): **every post PUBLISHED on both networks, no provider ERROR** — incl. the owner's live-session
chair-flip (11 Nov 21:56 IST, bright explainer look, not a studio episode). Instagram (IGRE, pulled 21:20 UTC 11 Nov):
| Post (IST) | Views | Reach | Avg watch s | 3-s % | Saves | Likes |
|---|---|---|---|---|---|---|
| 11 Nov 21:56 chair flip (owner, bright) | 6 | 5 | 3.9 | 20.0 | 0 | 2 |
| 11 Nov 05:00 Netflix BIG (board) | 5 | 4 | 2.7 | 25.0 | 0 | 0 |
| 10 Nov 05:00 Instacart HIW (board) | 154 | 134 | 16.3 | 63.2 | 0 | 1 |
| 9 Nov 19:35 Michelin anime BIG (owner) | 174 | 157 | 6.9 | 46.1 | 0 | 2 |
| 9 Nov 05:00 dropship HOW TO (board) | 132 | 116 | 12.2 | 46.3 | 1 | 1 |
| 8 Nov 05:00 Prime HIW (board) | 634 | 577 | 24.0 | 64.9 | 1 | 6 |
| 8 Nov 00:00 exporting HOW TO (board) | 1,733 | 1,550 | 35.0 | 78.7 | 5 | 16 |
YouTube (YTVP; Metricool rows still stop at 8 Nov): exporting 431 / 50 s avg, Southwest 352 / 30 s, Prime 62 / 26 s, dropship 63 / 18 s.
**Insights (AR):** (1) Netflix at 5 views after ~22 h and the chair flip at 6 after ~5 h look like Metricool's IG import lag
(PERFORMANCE note 6), not a verdict — re-read next run; if Netflix is still < 50, compare its first 2 s with Instacart's.
(2) The two HOW IT WORKS whiteboard posts (Prime 64.9 %, Instacart 63.2 %) open better than the last two HOW TOs except
exporting; HOW TO still owns saves (exporting 5). (3) Views per post are sliding since 8 Nov on both networks (IG 1,733 → 634 → 132–174;
YT 431 → ~62) — the opener fix (object on screen at frame 0) helped the 3-s rate, not reach. This run tests two owner-asked changes at once:
an **American narrator** (usa_narr) and a **more colourful board** (colour spots) — judge them on the 3-s rate and avg watch vs Instacart.

## Snapshot 2026-11-11 ~08:30 IST (R&D run: writers' room)
**Delivery (getScheduledPosts, 9–14 Nov IST):** dropshipping (9 Nov 05:00), the owner's Michelin anime (9 Nov 19:35), same cart (10 Nov 05:00) and **Netflix (11 Nov 05:00, 423740538)** all PUBLISHED on Instagram + YouTube; no provider ERROR. Nothing scheduled after Netflix.
**Analytics (IGRE 21 Oct → 11 Nov, YTVP):** every Instagram row equal to the 02:50 IST pull within ±2 (same cart 152 / 63.4 %, Michelin 173 / 46.4 %, dropship 132 / 46.3 %, Prime 634 / 64.9 %, exporting 1,730 / 78.7 %); Netflix has no row yet (3.5 h old). YouTube rows unchanged (latest 8 Nov: Prime 40 · 25 s).
**Insight AR (11 Nov):** no new numbers, so AP (object in the first second → 63.4 %) and AQ (BIGs do better on YouTube) stand. The test that matters next is Netflix: first BIG with a live counter (`tally`) carrying the middle — read its avg watch vs same cart's 16.6 s (14 %) once it is ≥ 24 h old. The two new queued scripts (7-Eleven BIG, print-on-demand HOW TO) both carry a counter or a growing bar (`tally` OWNED IN TOKYO, `costbar_m`) for the same reason. Media kit unchanged (last 10 IG reels avg 437 views, median 311, 3-s 61.1 %, avg watch 19.7 s).

## Snapshot 2026-11-11 ~02:50 IST (episode run: HOW THEY GOT SO BIG EP 4, Netflix 2011)
**Delivery (getScheduledPosts, 7–14 Nov IST):** Southwest, currency button, Coca-Cola, exporting, Prime, dropshipping, the owner's Michelin anime and **same cart (10 Nov 05:00)** all PUBLISHED on Instagram + YouTube; no provider ERROR in the window (only the old reselling IG error of 6 Nov remains). Nothing scheduled after same cart.
**Analytics (IGRE + YTVP, 20 Oct → 11 Nov)** — new / refreshed rows:
| Date (IST) | Video | Kind · look | Views | Reach | Avg watch | 3-s rate | Shares | Saves | Likes | Comments |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 Nov 05:00 | Same cart (Instacart) | HOW IT WORKS · whiteboard | 152 | 132 | 16.6 s | **63.4 %** | 0 | 0 | 1 | 1 |
| 9 Nov 19:35 | Michelin (owner's anime) | BIG · anime | 173 | 156 | 7.0 s | 46.4 % | 0 | 0 | 2 | 0 |
| 9 Nov 05:00 | Dropshipping 30-day rule | HOW TO · whiteboard | 132 | 116 | 12.3 s | 46.3 % | 0 | 1 | 1 | 1 |
| 8 Nov 05:00 | Prime 'Iliad' | HOW IT WORKS · whiteboard | 634 | 577 | 24.0 s | 64.9 % | 0 | 1 | 6 | 1 |
| 8 Nov 00:00 | Exporting | HOW TO · whiteboard | 1,730 | 1,550 | 35.0 s | 78.7 % | 1 | 5 | 16 | 1 |
**YouTube (YTVP) is unstuck — rows now reach 8 Nov** (views · avg view duration s): exporting 312 · 55, **Southwest 292 · 30**, credit score 183 · 38, currency 169 · 13, Coca-Cola 109 · 20, importing 98 · 23, Prime 40 · 25 (young), reselling 179 · 24, Spotify 142 · 74.
**Insight AP (11 Nov): the 'object in the first second' fix worked once.** Same cart opened on a carton with five price tags landing by 0.7 s and got **63.4 % past 3 s** (21 h old), vs 46.3 % (dropship) and 46.4 % (Michelin) the two posts before it — back at the whiteboard average. Watch time is still low (16.6 s of 118 s = 14 %): the opening now works, the middle loses people. One post, so a hint, not proof. → This run's Netflix board opens on a finished picture (red envelope, big −800,000) and adds a **re-hook every ~20 s drawn as a running counter** (members leaving) so the middle has a number that keeps moving.
**Insight AQ (11 Nov): BIG stories do better on YouTube than their IG numbers suggest.** Southwest is the #2 YouTube Short of the whiteboard era (292 views, 30 s avg) while it was mid-table on IG (349, 60.5 %). Across the three kinds on YouTube: HOW TO avg 205 views (exporting, importing, reselling), BIG 201 (Southwest, Coca-Cola), HOW IT WORKS 134 (credit, currency, Prime, Spotify). On IG the HOW TOs still lead (exporting, food truck, drone). Keep the rotation; BIGs earn their place on YouTube.
Media kit (last 10 IG reels, incl. Michelin): avg **437 views** (median 311), 3-s rate 61.1 %, avg watch 19.7 s, 5.9 sends + saves + comments per 1,000 reach. YouTube last 10 with rows: avg 177 views.

## Snapshot 2026-11-10 ~08:30 IST (R&D run: Voice)
**Delivery (getScheduledPosts, 8–17 Nov IST):** exporting, Prime, dropshipping, the owner's Michelin anime and **same cart (422463083, 05:00 IST today)** all PUBLISHED on Instagram + YouTube; no provider ERROR. Nothing scheduled after same cart. The Michelin post went out with Instagram's AI label off (`isAiGenerated: false`); every studio post sets it on.
**Analytics (IGRE 20 Oct → 10 Nov, YTVP):** every Instagram row identical to the 03:35 IST pull (Michelin 166 / 46.6 %, dropship 129 / 47.5 %, Prime 632 / 65.1 %, exporting 1,727 / 78.8 %); same cart has no row yet (3.5 h old). YouTube (YTVP) still ends at Christmas lights (3 Nov) — Metricool's YouTube import has now been stuck 7 days; read view counts in YouTube Studio if a decision needs them.
**Insight AO (10 Nov):** no new numbers, so insight AN stands untested — the same-cart row (opened on five price tags by 0.7 s) is the test of 'concrete object in the first second' vs dropship's 47.5 %. Read it next run (≥ 24 h old). Media kit unchanged.

## Snapshot 2026-11-10 ~03:35 IST (episode run: HOW IT WORKS EP 5, same cart / Instacart price tests)
**Delivery (getScheduledPosts, 6–14 Nov IST):** everything from credit score (6 Nov) to **dropshipping (9 Nov 05:00)** and the owner's **Michelin anime pilot (9 Nov 19:35, 421658174)** PUBLISHED on Instagram + YouTube. Only the old reselling Instagram ERROR (418324142, 6 Nov, "Media container not created") remains — owner's call, not re-posted. Nothing scheduled after Michelin.
**Analytics (IGRE, 19 Oct → 10 Nov)** — new / refreshed rows:
| Date (IST) | Video | Kind · look | Views | Reach | Avg watch | 3-s rate | Shares | Saves | Likes | Comments |
|---|---|---|---|---|---|---|---|---|---|---|
| 9 Nov 19:35 | Michelin (owner's anime pilot) | BIG · anime | 166 | 148 | 7.2 s | 46.6 % | 0 | 0 | 2 | 0 |
| 9 Nov 05:00 | Dropshipping 30-day rule | HOW TO · whiteboard | 129 | 114 | 12.6 s | 47.5 % | 0 | 1 | 1 | 1 |
| 8 Nov 05:00 | Prime 'Iliad' | HOW IT WORKS · whiteboard | 632 | 576 | 24.1 s | 65.1 % | 0 | 1 | 6 | 1 |
| 8 Nov 00:00 | Exporting | HOW TO · whiteboard | 1,727 | 1,545 | 35.0 s | 78.8 % | 1 | 5 | 16 | 1 |
YouTube (YTVP): still no rows after 3 Nov (Metricool import stuck; the Shorts are live).
**Insight AN (10 Nov): the last two posts both opened under 50 % — the first time two in a row did.** Dropshipping (whiteboard HOW TO, 22 h old) 47.5 % / 12.6 s and Michelin (anime BIG, 8 h old) 46.6 % / 7.2 s, vs 60–79 % for the 7 whiteboard posts before them. Both are young rows (they may climb), but two different looks failing the same way points at the **first second, not the look**: dropship opened on a calendar + parcel with "do you know your shop has a DEADLINE?" (abstract), Michelin on a character. The posts that opened ≥ 65 % opened on a **concrete surprising number or object** (exporting: a tax gate crossed out; Prime: ILIAD; Spotify: 999 plays = $0). → This run opens on the surprise itself: five real price tags on one egg carton, all five visible by 0.7 s. Test: same-cart 3-s rate vs dropship 47.5 % / Prime 65.1 %. HOW IT WORKS on the board: Prime 632 / 65.1 % beat currency 345 / 62.1 % and credit 137 / 54.3 % — the consumer-vs-company story with a regulator ending is the strongest HOW IT WORKS shape so far, which is the shape of this episode.
Media kit (last 10 IG reels, incl. Michelin): avg **574 views** (median 347), 3-s rate 63.4 %, avg watch 23.4 s, 5.1 sends + saves + comments per 1,000 reach — down from 696 / 67.6 % on 9 Nov because the two newest rows are young and weak.

## Snapshot 2026-11-09 ~08:30 IST (R&D run: writers' room)
**Delivery (getScheduledPosts, 8–16 Nov IST):** exporting (419444583), Prime 'Iliad' (420282985) and **dropshipping (421118761, 05:00 IST today)** all PUBLISHED on Instagram + YouTube; no provider ERROR. Nothing scheduled after dropshipping.
**Analytics (IGRE + YTVP, 19 Oct → 9 Nov):** every Instagram row is identical to the 02:45 IST pull (exporting 1,712 / 78.9 %, Prime 611 / 65.0 %); dropshipping has no row yet (posted 3.5 h before the pull). YouTube (YTVP) still ends at Christmas lights (3 Nov) — 6 days, 11 Shorts missing; the Shorts are live, Metricool's YouTube import is the problem.
**Insight AM (9 Nov):** no new numbers → insight AL stands (HOW TO START wins on the whiteboard; BIGs hold least, 0–1 saves). The room acted on it: the next BIG in the queue (Netflix 2011) ends on a rule the viewer can copy ("say why before they pay", from Netflix's own letter) and the queue now holds a BIG, two HOW IT WORKS and a HOW TO. Test when it posts: Netflix saves / 1,000 reach vs Southwest 0 and Coca-Cola 1 (≈ 4 / 1,000). Media-kit numbers in BRAND.md unchanged (no new data).

## Snapshot 2026-11-09 ~02:45 IST (episode run: HOW TO START EP 8, dropshipping 30-day rule)
**Delivery (getScheduledPosts, 5–16 Nov IST):** every post from Spotify to **Prime 'Iliad' (8 Nov 05:00 IST)** PUBLISHED on Instagram + YouTube; only the old reselling Instagram ERROR (418324142, 6 Nov) remains — owner's call, not re-posted. Nothing scheduled after Prime; the owner's Michelin anime pilot (live session 8 Nov) isn't scheduled yet.
**Instagram finally refreshed (IGRE, 18 Oct → 9 Nov)** — whiteboard rows:
| Date (IST) | Video | Kind | Views | Reach | Avg watch | 3-s rate | Shares | Saves | Likes | Comments |
|---|---|---|---|---|---|---|---|---|---|---|
| 8 Nov 05:00 | Prime 'Iliad' | HOW IT WORKS | 611 | 555 | 24.1 s | 65.0 % | 0 | 1 | 6 | 1 |
| 8 Nov 00:00 | Exporting | HOW TO START | **1,712** | 1,537 | **35.3 s** | **78.9 %** | 1 | **5** | 16 | 1 |
| 7 Nov 19:35 | Coca-Cola $1 | BIG | 274 | 237 | 20.8 s | 68.8 % | 0 | 1 | 1 | 1 |
| 7 Nov 14:35 | Currency button | HOW IT WORKS | 343 | 320 | 16.0 s | 62.5 % | 0 | 0 | 2 | 1 |
| 7 Nov 09:35 | Southwest | BIG | 349 | 309 | 23.0 s | 60.5 % | 0 | 0 | 3 | 1 |
| 6 Nov 23:35 | Importing | HOW TO START | 443 | 391 | 25.8 s | 65.8 % | 0 | **5** | 7 | 1 |
| 6 Nov 20:35 | Credit score | HOW IT WORKS | 137 | 117 | 16.7 s | 54.3 % | 0 | 0 | 1 | 1 |
YouTube (YTVP): still no rows after Christmas lights (3 Nov) — 10 Shorts missing for 6 days; Metricool's YouTube import looks stuck (the Shorts themselves are PUBLISHED with public URLs).
**Insight AL (9 Nov): on the whiteboard, HOW TO START wins on every number.** Exporting is the best whiteboard post so far (78.9 % 3-s, 35.3 s avg watch = a third of the video, 1,712 views) and the two HOW TO posts hold **10 of the 12 whiteboard saves** (exporting 3.3 / 1,000 reach, importing 12.8 / 1,000). HOW IT WORKS sits mid (62–65 %, 16–24 s; Prime 611 views), and the two HOW THEY GOT SO BIG stories are the weakest on watch time (21–23 s on ~80–98 s videos, 0–1 saves). Whiteboard vs night look: whiteboard 3-s average 65.1 % (7 posts) vs the night/stick look 72.7 % (drone, vending, food truck, lights, Spotify) — the gap from Insight AI narrowed from ~10 to ~7.6 points now that exporting landed. → Keep HOW TO START in every rotation; BIG stories need a stronger "useful" ending to earn saves (the founder's move as a rule the viewer can copy), and they're the right slot to try the owner's new anime look on. This run builds a HOW TO (dropship) — it tests whether a third whiteboard HOW TO repeats the saves.

## Snapshot 2026-11-08 ~08:35 IST (R&D run: writers' room)
**Delivery (getScheduledPosts, 7–10 Nov IST):** Southwest, currency button, Coca-Cola, exporting **and Prime 'Iliad' (05:00 IST today, 420282985)** all PUBLISHED on Instagram + YouTube. No provider ERROR on any of them (reselling's old IG error unchanged). Nothing scheduled after Prime.
**Analytics (IGRE + YTVP, 18 Oct → 8 Nov):** every Instagram row is **identical** to the 02:50 IST pull (exporting still 4 views, Coca-Cola 157 / 69.9 %), and Prime has no row yet — Metricool's IG import hasn't refreshed in ~6 h; read again next run. **YouTube (YTVP): still no rows after Christmas lights (3 Nov)** — 5 days and 9 Shorts missing (Spotify → Prime). The video run should check whether the YouTube connector stopped importing (all 9 show PUBLISHED with public URLs) rather than read it as zero views.
**Insight AK (8 Nov):** no new numbers, so no new verdict on whiteboard vs night (Insight AI stands). The queue now leads with a HOW TO (dropship) — the kind Insight AJ found steadiest on the board and the only one with saves — to test whether HOW TO keeps its saves edge on a second whiteboard post. Media-kit numbers in BRAND.md unchanged (no new data).

## Snapshot 2026-11-08 ~02:50 IST (episode run: HOW IT WORKS EP 4, Prime 'Iliad')
**Delivery (getScheduledPosts, 5–12 Nov IST):** Spotify, credit score, importing, Southwest, currency button, Coca-Cola and **exporting (00:00 IST today)** all PUBLISHED on Instagram + YouTube. **Reselling (418324142) still instagram ERROR** (unchanged since 6 Nov, owner's call, not re-posted). No new provider errors.
Instagram (IGRE, 17 Oct → 8 Nov) — new + changed rows:
| Date | Video | Kind | Look | Views | Reach | Avg watch | 3-s rate | Likes | Shares | Saves | Comments |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 11-08 00:00 | HOW TO START EP 7 — exporting (~3 h) | HOW TO | whiteboard | 4 | 0 | — | — | 0 | 0 | 0 | 1 (ours) |
| 11-07 19:35 | BIG EP 2 — Coca-Cola $1 (~7 h) | BIG | whiteboard | 157 | 134 | 17.1 s | **69.9 %** | 0 | 0 | 1 | 1 (ours) |
| 11-07 14:35 | HOW IT WORKS EP 3 — currency button (~12 h) | HIW | whiteboard | 276 | 253 | 15.6 s | 64.4 % | 1 | 0 | 0 | 1 (ours) |
| 11-07 09:35 | BIG EP 1 — Southwest (~17 h) | BIG | whiteboard | 338 | 301 | 22.6 s | 60.5 % | 3 | 0 | 0 | 1 (ours) |
| 11-06 23:35 | HOW TO START EP 6 — importing (~27 h) | HOW TO | whiteboard | 439 | 387 | 25.7 s | 65.6 % | 7 | 0 | **5** | 1 (ours) |
| 11-06 20:35 | HOW IT WORKS EP 2 — credit score (~30 h) | HIW | whiteboard | 137 | 117 | 16.7 s | 54.3 % | 1 | 0 | 0 | 1 (ours) |
| 11-05 05:00 | HOW IT WORKS EP 1 — Spotify | HIW | night | 1,538 | 1,345 | 52.7 s | 84.0 % | 31 | 0 | 3 | 1 |
YouTube (YTVP): still no rows after Christmas lights (158 views / 31 s avg); food truck 311 / 54 s, vending 314 / 30 s, drone 366 / 29 s.
**Media-kit numbers (8 Nov, last 10 IG reels with ≥ 7 h, exporting excluded):** avg **633 views** (median 389), avg 3-s rate 67.9 %, avg watch 26.7 s, **9.5 sends + saves + comments per 1,000 reach** (30.6 incl. likes; our own first comments included); YouTube last 10 with rows avg 363 views (unchanged, rows stalled).
**Insight AI (8 Nov) — whiteboard vs night: on the first 5 whiteboard posts the board opens lower and gets watched less.** Whiteboard 3-s rate avg **62.9 %** (54–70) and avg watch 19.5 s on 80–116 s videos, vs the last 5 night/old-cast posts 72.9 % (68–84) and 34 s. Views are not comparable yet (night rows are 3–7 days old, whiteboard 7–30 h), but 3-s rate barely moves after day 1, so the gap is real on what we have: **~10 points fewer people past the first 3 s.** It's not topic alone: the kinds overlap (HIW: credit 54 / currency 64 on board vs Spotify 84 night; HOW TO: importing 66 board vs 68–76 night). The look is the owner's order, so the fix is inside the look: the first frame has to read as a finished picture with motion before the first word (Coca-Cola, whose frame 1 was pre-drawn, opened best at 70 %). Owner should see this number (he also asked on 7 Nov for a new style after rejecting the notebook).
**Insight AJ (8 Nov) — which kind holds:** BIG opens best on the board (Coca-Cola 70 %, Southwest 61 %, avg 65 %), HOW TO steadiest and the only one with saves on the board (importing 5 saves = 12.9 / 1,000 reach), HOW IT WORKS weakest on the board (54 %, 64 %). → this run's HOW IT WORKS (Prime 'Iliad') opens on a finished picture (scroll + helmet + the question) already in motion at frame 0, and carries a two-door map through the video so a viewer always knows where they are. Judge: 3-s ≥ 65 %, avg watch ≥ 25 s, saves ≥ 5 / 1,000 reach.

## Snapshot 2026-11-07 ~08:25 IST (R&D run: writers' room)
**Delivery (getScheduledPosts, 6–9 Nov IST):** credit score + importing PUBLISHED on both; **reselling (418324142) still instagram ERROR** (unchanged, owner's call). Southwest 09:35, currency button 14:35, Coca-Cola 19:35 (7 Nov) and exporting 00:00 (8 Nov) PENDING. No new provider errors.
Instagram and YouTube rows identical to the 02:50 IST pull (importing 95 views / 18 reach / 91.0 %; credit score 132 / 114 / 16.9 s / 54.9 %, 1 like, 0 saves, 0 shares; YouTube still no rows after Christmas lights). Media-kit numbers unchanged: IG last 10 avg 567 views, median 201.
**Insight AH (7 Nov) — nothing new to read yet; what the next pull must answer:** three whiteboard posts land today (Southwest 09:35, currency 14:35, Coca-Cola 19:35 IST) next to two whiteboard rows still under 24 h. Read whiteboard-vs-night at ≥ 24 h for ≥ 4 whiteboard posts before changing the look. The two HOW IT WORKS scripts queued today were picked by the owner's order, not by data; judge them on 3-s ≥ 65 % and saves ≥ 5 / 1,000 reach (insight Z).

## Snapshot 2026-11-07 ~02:50 IST (episode run: HOW TO START EP 7, exporting)
**Delivery (getScheduledPosts, 5–10 Nov):** Spotify, credit score and importing PUBLISHED on both networks. **Reselling (418324142) still shows instagram ERROR** ("Media container not created by unknown cause"), YouTube published; already reported on 6 Nov, not re-posted (owner decides). Southwest (09:35), currency button (14:35) and Coca-Cola (19:35) are PENDING for 7 Nov. No new errors.
Instagram (IGRE, 16 Oct → 7 Nov) — new + changed rows:
| Date | Video | Look | Len | Views | Reach | Avg watch | 3-s rate | Likes | Shares | Saves | Comments |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 11-06 23:35 | HOW TO START EP 6 — importing (~3 h) | whiteboard | 109 s | 95 | 18 | 13.9 s | **91.0 %** | 1 | 0 | 0 | 1 (ours) |
| 11-06 20:35 | HOW IT WORKS EP 2 — credit score (~6 h) | whiteboard | 116 s | 132 | 114 | 16.9 s | 54.9 % | 1 | 0 | 0 | 1 (ours) |
| 11-05 | HOW IT WORKS EP 1 — Spotify (~46 h) | NBN night | 136 s | 1,537 | 1,345 | 52.7 s | 84.0 % | 31 | 0 | 3 | 1 (ours) |
| 11-04 | HOW TO START EP 4 — Christmas lights | old cast | 155 s | 240 | 214 | 21.7 s | 68.8 % | 5 | 0 | 1 | 1 |
YouTube (YTVP): still no rows after Christmas lights (158 views / 31 s); food truck 311 / 54 s is now the best average view duration on YouTube; drone 366 / 29 s; vending 314 / 30 s.
**Media-kit numbers (7 Nov):** IG last 10 reels avg **567 views** (median 201), avg 3-s rate 65.3 %, avg watch 25.5 s, **9.2 reactions per 1,000 reach** (our own first comments included); YouTube last 10 with rows avg 363 views.
**Insight AF (7 Nov) — whiteboard vs night look: too early to call, and the two whiteboard rows disagree.** Importing opened at 91 % past 3 s (channel best, but on ~18 reach) and credit score at 55 %, both under 6 h old; Spotify on the night look holds the records with a full day of data (84 %, 52.7 s). Same look, opposite openings → the topic is still doing the work, not the board. Read again at ≥ 24 h before changing anything.
**Insight AG (7 Nov) — which kind holds: how-tos open steadiest (68–76 % on all five), HOW IT WORKS swings (Spotify 84 %, credit 55 %), HOW THEY GOT SO BIG has no row yet (Southwest posts 09:35 IST today).** Saves still come from how-tos (drone 14, vending 6, food truck 3). → this run builds a how-to (exporting) whose hook is a surprise anyone can repeat (the Constitution bans export taxes) and whose steps end on something to do (search the buyer's name, agree who pays at the door). Judge: 3-s ≥ 68 %, saves ≥ 5 / 1,000 reach.

## Snapshot 2026-11-06 ~08:30 IST (R&D run: writers' room)
Instagram rows identical to the 02:45 IST pull (Spotify 1,534 / 52.8 s / 84.1 %, drone 1,324, food truck 1,305, vending 571, lights 240). YouTube rows still stop at vending (205 / 30 s) and drone (348 / 29 s): no row for food truck, lights, Spotify or reselling. Media-kit numbers unchanged: IG last 10 avg 579 views, median 214, 9.8 reactions / 1,000 reach; YT last 10 with rows avg 419.
**⚠ Reselling (HOW TO START EP 5, Metricool 418324142) did NOT reach Instagram.** Planner status at 08:15 IST: instagram `ERROR`, "Media container not created by unknown cause"; youtube `PUBLISHED` (shorts/KChsuhTLJDs). So there will be no IG row for it, and insight AC's read ("first how-to on the new stack") can only be done on YouTube, whose rows run days late. Spotify went through with the same stack and a longer file, so length isn't the obvious cause. This run is read-only on Metricool: **owner decides whether to re-post it to Instagram.** Rule added in PLAYBOOK §6: after a post's time, read its provider status.
**Insight AE (6 Nov) — what the writers' room changed because of this data:** the hook of the new how-to is a law people can feel (jail for a muffin), the choice is one a stranger can answer without owning a kitchen, and the pricing step ends on a sum anyone can check (160 hours). Same test as AC/AB: 3-s, watch, saves ≥ 10 / 1,000, stranger comments. Nothing proven yet.

## Snapshot 2026-11-06 ~02:45 IST (episode run: HOW TO START EP 5, reselling)
Instagram (IGRE, 15 Oct → 6 Nov) — new + changed rows:
| Date | Video | Len | Views | Reach | Avg watch | 3-s rate | Likes | Shares | Saves | Comments |
|---|---|---|---|---|---|---|---|---|---|---|
| 11-05 | **HOW IT WORKS EP 1 — Spotify 999 plays** (~21.7 h) | 136 s | **1,534** | 1,341 | **52.8 s** | **84.1 %** | 31 | 0 | 3 | 1 (ours) |
| 11-04 | HOW TO START EP 4 — Christmas lights (~45.7 h) | 155 s | 240 | 214 | 21.7 s | 68.8 % | 5 | 0 | 1 | 1 (ours) |
| 11-03 | HOW TO START EP 3 — food truck | 101 s | 1,305 | 1,127 | 31.8 s | 68.2 % | 23 | 0 | 3 | 1 |
| 11-02 | HOW TO START EP 2 — vending | 99 s | 571 | 504 | 35.6 s | 68.0 % | 11 | 1 | 6 | 2 |
| 11-01 | HOW TO START EP 1 — drone | 115 s | 1,324 | 1,193 | 27.5 s | 75.9 % | 35 | 6 | 14 | 1 |
YouTube (YTVP): no rows yet for food truck, Christmas lights, Spotify; drone 348 / 29 s, vending 205 / 30 s unchanged.
**Media-kit numbers (6 Nov):** IG last 10 reels avg **579 views** (median 214), avg 3-s rate 61.5 %, avg watch 27.3 s, 9.8 reactions per 1,000 reach (shares + saves + comments, our own first comments included; 43 over 4,382 reach); YouTube last 10 with rows avg 419 views.
**Insight AC (6 Nov) — Spotify is the best opening and the best watch this channel has ever measured: 84.1 % past 3 s (old best 75.9 %), 52.8 s average (old best 35.6 s), 39 % of a 136 s video.** It beat its targets for 3-s (≥ 65 %) and watch (≥ 27 s), and missed saves: 2.2 per 1,000 reach against ≥ 5, 0 shares, no stranger comment. Views are not its record (makhana 4,725, importing 4,644), and those two also held only 13–17 % at 3 s, so views and hold are different questions. One row under 24 h. Three things changed at once: the real NBN kit, Chatterbox, and a new series with a money-number hook, so this cannot say which one did it. **What it does say: the owner's 4 Nov complaint was right and the rebuild did not hurt; stay on nbnkit + Chatterbox.** Reselling is the first how-to on this stack: same kit and voice with a different format, so it separates a little. Read: if 3-s and watch stay well above the old how-tos (68 %, 27–36 s), the stack is doing it; if saves return to ~10 / 1,000 while watch holds, how-to + stack is the best of both.
**Insight AD (6 Nov) — Christmas lights did not recover: 240 views at ~46 h, lowest watch of the how-tos.** The old cast's last episode, the longest one, and a narrower audience; can't separate them, no action beyond keeping how-tos broad.

## Snapshot 2026-11-05 ~08:30 IST (R&D run: writers' room)
Instagram rows unchanged from the 02:40 IST pull within ±0 views on the last 10 (Christmas lights still 228 / 21.3 s / 68.0 %, 1 save); Spotify EP 1 (published 05:00 IST on both, per the planner) has no row yet. YouTube rows still stop at vending (205 / 30 s) and drone (348 / 29 s): no row for food truck, Christmas lights or Spotify. Media-kit numbers unchanged: IG last 10 avg 483 views, median 208, 8.6 reactions / 1,000 reach; YT last 10 with rows avg 419. Whole-account check for repeats: no reselling, tax or Shorts-pay topic in any IG caption since the first post (19 Oct) or in the scheduled list.
**Insight AB (5 Nov) — the one thing all our saved videos share is that the viewer could act on them, and the two that got sent were dreams or tricks, not warnings.** Saves on the 4 how-tos: drone 14, vending 6, food truck 3, lights 1. Shares: drone 6, vending 1, the rest 0. The older posts with the most of both are makhana (10 saves, 11 shares) and the restaurant tricks (6 saves, 4 shares), both about money a viewer can picture; everything else has 0–4 of each. n is small and rows are mixed in age, so a lead. → EP 5 reselling is built as something to do (one list) plus a thing to send (a friend with a full closet). If it saves but isn't sent, that's the warning pattern again; if neither, the tax angle cost us.

## Snapshot 2026-11-05 ~02:40 IST (episode run: HOW IT WORKS EP 1, Spotify 999 plays)
Instagram (IGRE, 14 Oct → 4 Nov) — new + changed rows:
| Date | Video | Len | Views | Reach | Avg watch | 3-s rate | Likes | Shares | Saves | Comments |
|---|---|---|---|---|---|---|---|---|---|---|
| 11-04 | **HOW TO START EP 4 — Christmas lights** (~21.6 h) | 155 s | **228** | 202 | **21.3 s** | 68.0 % | 4 | 0 | 1 | 1 (ours) |
| 11-03 | HOW TO START EP 3 — food truck (~45 h) | 101 s | 1,302 | 1,127 | 31.8 s | 68.3 % | 23 | 0 | 3 | 1 (ours) |
| 11-02 | HOW TO START EP 2 — vending (~69 h) | 99 s | 571 | 503 | 35.6 s | 68.0 % | 11 | 1 | 6 | 2 (1 ours) |
| 11-01 | HOW TO START EP 1 — drone (~93 h) | 115 s | 1,324 | 1,193 | 27.5 s | 75.9 % | 35 | 6 | 14 | 1 (ours) |
YouTube (YTVP): drone 348 / 29 s, vending 205 / 30 s, glasses 81 / 25 s, all unchanged; food truck and Christmas lights still have no row.
**Media-kit numbers (5 Nov):** IG last 10 reels avg **483 views** (median 208), avg 3-s rate 59.5 %, avg watch 24.8 s, reactions (shares + saves + comments excl. our own) **8.6 per 1,000 reach** (35 on 4,065 reach); YT last 10 with rows avg 419 views (unchanged; last rows are older than the last two episodes).
**Insight AA (5 Nov) — the first three how-tos at ~21 h had 500–1,300 views, Christmas lights has 228, on the same 68 % 3-s rate.** Same opening hold, so it isn't the first three seconds. What differs: its 155 s length (our longest how-to), the lowest avg watch of the series (21.3 s against 27–36 s), and a seasonal subject. It is one row at under a day, and insight X found seconds watched don't fall with length across 18 reels, so this is a lead, not a verdict. The save target (≥ 10 / 1,000 reach) missed: 1 save = 5 / 1,000. It is also the episode the owner called "too cartoon" and "not like it triggers more views". Re-read it at 72 h before believing any of this. → This run: keep the new episode at ~135 s or less, and change the look completely. **Judge EP 1 (HOW IT WORKS): 3-s ≥ 65 %, saves ≥ 5 / 1,000 reach, any stranger comments on YES/NO, avg watch ≥ 27 s.**

## Snapshot 2026-11-04 ~08:30 IST (R&D run: writers' room)
Instagram + YouTube rows unchanged from the 02:40 IST pull within ±1 view (food truck 1,299, vending 570, drone 1,323); Christmas lights (posted 05:00 IST, published on both per the planner) has no row yet; food truck still no YouTube row. Media-kit numbers unchanged: IG last 10 avg 611 views, YT last 10 with rows avg 419.
**Insight Z (4 Nov) — a benchmark for HOW IT WORKS before it exists, three groups on the same IG rows (mixed dates, post-hoc tags, so a lead):** how-tos (n = 3) 1,064 views, 3-s 70.7 %, watch 31.6 s, shares 2.5 + saves 8.2 per 1,000 reach; old "how X makes money" explainers (n = 9, gas, printer, gym, Costco, AWS, Duolingo, Chick-fil-A, Visa, popcorn) 690 views, 56.4 %, 18.2 s, shares 0.6 + saves 1.0; stories (n = 6, glasses, banana, Hoover, Monopoly, De Beers, airline miles) 233 views, 52.7 %, 22.1 s, shares 0.8 + saves 1.6. Explainers about things in your hand reached people but were not kept (gas 1,523 views, 0 saves; printer 1,376, 0 saves). So HOW IT WORKS has one job the old ones failed: be worth saving. → Both new episodes end on something to do (read your deal; check your report free). **Judge EP 1 + EP 2: 3-s ≥ 65 %, saves ≥ 5 / 1,000 reach, any stranger comments on the YES/NO.** If they hold like the old explainers with ~1 save, the format needs more how-to in it, not better pictures.

## Snapshot 2026-11-04 ~02:40 IST (episode run: HOW TO START EP 4, Christmas lights)
Instagram (IGRE, 13 Oct → 4 Nov) — new + changed rows:
| Date | Video | Len | Views | Reach | Avg watch | 3-s rate | Likes | Shares | Saves | Comments |
|---|---|---|---|---|---|---|---|---|---|---|
| 11-03 | **HOW TO START EP 3 — food truck NYC** (~21 h) | 101 s | **1,299** | 1,126 | **31.9 s** | 68.3 % | 23 | **0** | **3** | 1 (ours) |
| 11-02 | HOW TO START EP 2 — vending (~45 h) | 99 s | 570 | 503 | 35.5 s | 67.9 % | 11 | 1 | 6 | 2 (1 ours) |
| 11-01 | HOW TO START EP 1 — drone (~69 h) | 115 s | 1,323 | 1,191 | 27.5 s | 75.9 % | 35 | 6 | 14 | 1 (ours) |
YouTube (YTVP) **rows are back after 28 Oct** (sync returned): drone 348 / 29 s avg / 5 likes / 2 shares · vending 205 / 30 s / 0 / 0 · glasses 81 / 25 s / 5 / 0. Food truck: no row yet. Same-age comparison is not fair yet, but the how-tos sit below the 2-min stories on YouTube (banana 678, Monopoly 487, De Beers 346) with about the same seconds watched.
**Media-kit numbers (4 Nov):** IG last 10 reels avg **611 views** (median 379), avg 3-s rate 59.5 %, avg watch 25.0 s, reactions (shares + saves + comments excl. our own) **6.7 per 1,000 reach** (35 on 5,242 reach); YT last 10 with rows avg 419 views.
**Insight Y (4 Nov) — three how-tos, three different results on one number: saves depend on who can use it.** All three open at 68–76 % and hold 27–36 s, so the format's opening and hold are steady. Saves per 1,000 reach: drone 11.8, vending 11.9, **food truck 2.7** (0 shares). The food truck had the reach (1,126) and 32 s of watch, but it was NYC-only, so most viewers could not use it. This corrects insight W's "way in" guess: EP 3 ended on a way in and still got 0 sends. → This run: a broad topic (any US homeowner, with a friend to send it to), no city lock, and a one-word question anyone can answer (PAY or DIY). Judge EP 4 on saves ≥ 10 / 1,000 reach and any comments from strangers. n = 3, a lead.

## Snapshot 2026-11-03 ~08:30 IST (R&D run: Story audit)
Instagram rows ≈ unchanged since 02:40 IST (±2–3 views on old reels); food truck (posted 05:00 IST) has no row yet. Media-kit numbers unchanged: last 10 reels avg 490 views, median 177, 7.2 reactions / 1,000 reach. Followers 58 (1 Nov).
**YouTube is blind, not weak:** no `YTVP` rows after 28 Oct and account-level `YTEV02` views stop on 30 Oct, for 3 published episodes. Subscribers 32 (25 Oct) → 41 (28 Oct), flat since (last row 2 Nov). Looks like the Metricool ↔ YouTube sync; don't read these Shorts as flops. Check the channel directly.
**Insight X (3 Nov, n = 18 animated reels, `lab/story/hook_length_audit.py`) — three of our rules were weaker than we said.**
(1) Length: seconds watched do not fall with length (rho +0.32); bands <80 s 18.2 s · 80–105 s 25.0 s · 105–125 s 22.4 s · 125 s+ 21.9 s. **This corrects insight U:** "hold % of length" falls partly by arithmetic, so it can't justify a cut on its own. (2) Hook wording: no signal (words −0.24, you/your −0.10, ellipsis −0.17). (3) Roadmap: +1.8 s / +6.7 points of 3-s (n = 11 vs 7), down from the "+10 points of length" in insight K (n = 6).
What does separate: **3-s rate vs views rho +0.80**, and by subject: things the viewer pays for or could do themselves (drone, vending, gas, printer, Costco, gym) 3-s 64–76 %, mean 69.8 %; all 12 others 24–64 %, mean 51.0 %. Four of the six tags were set after seeing those rows (insights L/O), the two how-tos were out-of-sample, and banana (type B, predicted to win) came in at 56 %. Treat as a lead, confounded by date.
→ Expect Pepsi P1 (type A) to open below the how-tos on IG: the earlier A/C/D stories opened at 43–61 %. Judge it on comments and on YouTube once sync returns, not on 3-s alone. A blind AI viewer panel failed to predict any of this (rho 0.00), so human numbers only.

## Snapshot 2026-11-03 ~02:40 IST (episode run: HOW TO START EP 3, food truck NYC)
Instagram (IGRE, 12 Oct → 3 Nov) — new + changed rows:
| Date | Video | Len | Views | Reach | Avg watch | 3-s rate | Likes | Shares | Saves | Comments |
|---|---|---|---|---|---|---|---|---|---|---|
| 11-02 | **HOW TO START EP 2 — vending machines** (~21 h) | 99 s | 501 | 441 | **36.5 s (37 % of length; animated-era best in seconds)** | 68.2 % | 10 | 0 | **5** | 2 (1 ours = **first real comment**) |
| 11-01 | HOW TO START EP 1 — drone business (~45 h) | 115 s | 1,319 | 1,187 | 27.5 s | 75.9 % | 34 | 6 | 14 | 1 (ours) |
| 10-31 | Glasses: one company | 145 s | 149 | 122 | 18.3 s | 43.4 % | 2 | 0 | 1 | 1 (ours) |
YouTube (YTVP): **still no rows after 28 Oct** — glasses, drone and vending are all published on YouTube per the planner, but Metricool's table has not returned them for 5 days. Treat YT as unknown for these three, not as zero.
**Media-kit numbers (3 Nov):** IG last 10 reels avg **490 views** (median 177), avg 3-s rate 55 %, avg watch 23.1 s, reactions (shares + saves + comments, excl. our own first comment) **7.2 per 1,000 reach** (30 on 4,195 reach); YT last 10 with rows avg 439 views (unchanged).
**Insight W (3 Nov) — saves repeat, sends don't yet.** Two how-tos in a row save at the same rate (drone 11.8, vending 11.3 saves per 1,000 reach; everything else on the channel ≈ 0–5), and vending held the longest watch of the animated era. But vending got 0 shares and 37 % of the drone's reach: a broad, dream-y topic (drones) gets sent, a cautionary one (scam history) gets kept. n = 2, so a lead, not a rule. → This run: give the viewer a *way in* at the end (work a truck; private-property permit with no waiting list) rather than only a warning, and judge EP 3 on shares per reach, not just saves. Judge: saves ≥ 10 / 1,000 reach (holds), any shares (new).

## Snapshot 2026-11-02 ~08:30 IST (R&D run: writers' room HOW TO START EP 3 + props kit 5)
Instagram + YouTube pulls (IGRE / YTVP, 12 Oct → 2 Nov 03:00 UTC): **no change** since the 02:40 IST pull — no row yet for HOW TO START EP 2 (vending, posted
1 Nov 23:30 UTC) and still no YouTube row for glasses (31 Oct) or the drone episode (1 Nov). Media-kit numbers unchanged (IG last 10 avg 445 views, 6.3 reactions
/ 1,000 reach). Insight V still the driver of this run: the only series with sends + saves (HOW TO START) had **0** queued scripts → EP 3 written and queued.

## Snapshot 2026-11-02 ~02:40 IST (episode run: HOW TO START EP 2, vending machines)
Instagram (IGRE, 11 Oct → 2 Nov) — new + changed rows:
| Date | Video | Len | Views | Reach | Avg watch | 3-s rate | Likes | Shares | Saves | Comments |
|---|---|---|---|---|---|---|---|---|---|---|
| 11-01 | **HOW TO START EP 1 — drone business** (~22 h) | 115 s | **1,313** | 1,180 | **27.6 s** | **75.9 %** (channel best) | 34 | **6** | **14** | 1 (ours) |
| 10-31 | Glasses: one company | 145 s | 141 (+98) | 117 | 18.9 s | 45.2 % | 2 | 0 | 1 | 1 (ours) |
| 10-28 | Banana / Hoover / Monopoly | — | 144 / 153 / 188 | — | 23.9 / 15.3 / 30.8 s | 56.8 / 45.5 / 60.7 % | — | 0 | 0 | 0 |
YouTube (YTVP): banana 677 / 33 s · Hoover 321 / 38 s · Monopoly 485 / 39 s · De Beers 345 / 35 s — **no rows yet for glasses (31 Oct) or the drone episode (1 Nov)**.
**Media-kit numbers (2 Nov):** IG last 10 reels avg **445 views** (median 165), avg 3-s rate 54 %, reactions (shares + saves + comments, excl. our own
first comment) **6.3 per 1,000 reach** (was 1.1 on 1 Nov — the drone episode alone: 20 reactions on 1,180 reach = 17 / 1,000); YT last 10 avg 439 views.
**Insight V (2 Nov) — HOW TO START is the first format that gets *used*, not just watched.** The drone how-to beat every animated reel on the 3-s
rate (75.9 % vs previous best 73.7 % printer ink), held 27.6 s (24 % of 115 s) and got the channel's first real saves (14) and shares (6) since the
autopilot began — saves are what sponsors in tools/insurance/courses look at. Insight U2's bar (≥ 50 % / ≥ 20 s) is passed on day 1. The China → Amazon
list how-to (13 % 3-s) proves it's the *story hook in frame 1* (money landing, a question) that makes a how-to work, not the list. → Owner's priority
confirmed by data: build HOW TO START EP 2 now (vending machines, hook = "do you know what a singer is?"); keep a save-worthy step list + a debatable
end question; judge EP 2 on saves per reach (drone: 12 / 1,000) and 3-s rate ≥ 60 %.

## Snapshot 2026-11-01 ~08:45 IST (R&D run: Topics / HOW TO START shelf + writers' room EP 2)
Instagram + YouTube pulls (IGRE / YTVP, 11 Oct → 1 Nov 03:30 UTC): **no change** since the 02:45 IST pull — glasses still 43 views / 13.1 s /
35.3 % (IG rows look frozen for ~18 h); YouTube still has no glasses row; the drone episode (HOW TO START EP 1) published 05:00 IST on both
(IG reel DfLV4fzRy5w, YT LfZrnTtzKWY) — rows next run. Media-kit numbers unchanged (IG last-10 avg 317 views, 1.1 reactions / 1,000 reach;
YT last-10 avg 440). No vending / food-truck / bakery / POD / pressure-washing topic in the 21-day IG captions or the scheduled list.
**Insight U2 (series planning):** the channel's only earlier *step-by-step* how-to (China → Amazon "in 5 steps", 21 Oct) has our biggest IG reach
(4,640 views) but a 2.9 s avg watch / 13 % 3-s rate — reach came, the opening didn't hold. HOW TO START must hook with a story/question in
frame 1 (the drone episode: money landing; EP 2: "do you know what a singer is?"), not with a list. Judge EP 1 vs that row next run:
3-s rate ≥ 50 % and avg watch ≥ 20 s = the format holds.

## Snapshot 2026-11-01 ~02:45 IST (episode run: HOW TO START ep 1, drone business)
Instagram (IGRE, last 21 days) — new row + changes since 31 Oct 14:30:
| Date | Video | Len | Views | Reach | Avg watch | 3-s rate | Likes | Shares | Saves | Comments |
|---|---|---|---|---|---|---|---|---|---|---|
| 10-31 | Glasses: one company (first WHO-REALLY-OWNS-IT-style episode, ~7 h old) | 145 s | 43 | 33 | 13.1 s | **35.3 %** | 2 | 0 | 0 | 1 (= our own first comment) |
| 10-28 | Banana clones | 132 s | 138 (+6) | 119 | 24.4 s | 59.7 % | 3 | 0 | 0 | 0 |
| 10-28 | Hoover free flights | ~136 s | 150 (+7) | 129 | 15.6 s | 45.8 % | 2 | 0 | 0 | 0 |
| 10-28 | Monopoly's real inventor | 135 s | 187 | 162 | 31.0 s | 61.1 % | 3 | 0 | 0 | 0 |
YouTube (YTVP, views / avg view duration s / likes / shares): banana **674** / 33 / 9 / 0 · Hoover 321 / 38 / 8 / 0 · Monopoly 491 / **40** / 10 / 3 ·
De Beers 346 / 35 / 6 / 3 · airline miles 563 / 33 · gas 550 / 13 · Duolingo 612 / 7 · Planet Fitness 687 / 16 · printer ink 738 / 16 · glasses: no row yet.
**Media-kit numbers (1 Nov):** IG last 10 reels avg **317 views** (median 157), avg 3-s rate 51 %, avg watch 19.2 s, reactions (shares + saves +
comments, excl. our own first comment) **1.1 per 1,000 reach**; YT last 10 Shorts avg **440 views** (median 521). Followers: no new IGEV pull this run.
**Insights (1 Nov):**
S. **YouTube now carries the long story episodes, Instagram doesn't.** The four 130–145 s story videos sit at 321–674 YT views with 33–40 s average
   view duration (our best on YouTube), but 138–187 IG views. On IG, reach per reel has settled at ~120–160 (no follower base to seed it).
   → Keep the stories ≤ ~2 min, keep the first 2 s strong for IG; judge episodes on both platforms (YT is the healthier signal right now).
T. The first new-format episode (glasses, 145 s) opened at a 35 % 3-s rate on IG — second-worst ever (Duolingo 24 %), after 7 h. Its frame 1 was a
   "tree of glasses" with a long question. Too early to judge (posts move for ~24 h), but it supports insight Q: the hook line + a readable
   object in frame 1 decide. → This episode: frame 1 = a drone already flying over a house for sale, 5-word caption on screen from frame 0,
   wh-question hook in 2.3 s; length cut to ~113 s.
U. Saves/shares are still ~0 on every reel. HOW TO START is the first format built to be *saved* (a checklist with real costs) — watch saves on it.

(31 Oct ~18:50 IST, R&D Visuals run 10: IG + YT pulls identical to 14:30 IST, number for number — nothing posted since 28 Oct; the glasses reel
(post 412018960) is still PENDING for 19:30 IST. No new signal; the first story-format episode (Pepsi jet P1) is built by the 16:05 UTC run.)
(31 Oct 14:15 IST, R&D Tooling run 9: IG + YT pulls identical to the 14:30 IST pull below, number for number — nothing posted since 28 Oct, the
glasses video is still unposted. First **account-level** pull (IGEV connector): followers 53 (24 Oct) → 54 (25) → **57** (26–29 Oct);
account reach per day 3,076 (25 Oct, 106 accounts engaged) → 2,788 (26) → 1,895 (27) → 436 (28) → 10 (29) → 8 (30) — reach lives
~1 day after a post and the account has no baseline audience of its own; `IGEV43/44` followers gained/lost = 0 rows; IG country
demographics (IGDP01/02) return nothing — Instagram only reports them from ~100 followers, so the media kit's audience-country line
waits for that. Pull IGEV01 + IGEV06 every run from now on (follower growth per week is a media-kit number).)
## Instagram (snapshot 2026-10-31 ~14:30 IST, R&D writers' room run — first pull with rows for De Beers, Monopoly, Hoover, banana; comments column = IGRE07, 0 everywhere)
| Date | Video | Style | Len | Views | Reach | Avg watch | 3-s view rate | Likes | Shares | Saves |
|---|---|---|---|---|---|---|---|---|---|---|
| 10-28 | Banana clones (autopilot, B, map timeline) | animated, calm voice | 132 s | 132 | 116 | 24.4 s (18 %) | 60.9% | 3 | 0 | 0 |
| 10-28 | Hoover free flights (autopilot, A, "three mistakes") | animated, calm voice | ~100 s | 143 | 125 | 16.3 s | 48.0% | 2 | 0 | 0 |
| 10-28 | Monopoly's real inventor (autopilot, D) | animated, calm voice | 135 s | 186 | 161 | **31.2 s** (23 %) | 61.5% | 3 | 0 | 0 |
| 10-28 | De Beers: 2 months' salary (autopilot, B/E, roadmap "three moves") | animated, calm voice | 118 s | 162 | 146 | 17.5 s (15 %) | 48.6% | 2 | 1 | 0 |
| 10-27 | Airline miles: Amex paid Delta $8.2B (autopilot, F) | animated, calm voice | 101 s | 587 | 537 | 28.4 s (28 %) | 63.9% | 15 | 0 | 1 |
| 10-27 | Gas stations barely make money on gas (autopilot, B) | animated, calm voice | 81 s | **1,522** | 1,185 | 22.3 s | 66.7% | 28 | 1 | 0 |
| 10-27 | Duolingo $1B from your streak (autopilot, F) | animated, calm voice | 93 s | 164 | 146 | 13.1 s | **23.8%** | 3 | 0 | 0 |
| 10-27 | Visa never lends you a dollar (autopilot, F) | animated, calm voice | ~70 s | 65 | 57 | 14.6 s | 53.3% | 4 | 0 | 0 |
| 10-27 | Movie theaters make money on popcorn (autopilot, F) | animated, calm voice | ~75 s | 145 | 122 | 12.7 s | 53.7% | 4 | 0 | 0 |
| 10-26 | Printer ink costs more than champagne (autopilot, B) | animated, calm voice | ~75 s | 1,376 | 1,195 | 21.4 s | **73.7%** | 20 | 0 | 0 |
| 10-26 | Planet Fitness $15/month (autopilot, F) | animated, calm voice | ~75 s | 1,279 | 1,085 | 26.2 s | 69.5% | 26 | 2 | 1 |
| 10-26 | Chick-fil-A closed Sundays (autopilot, F) | animated, calm voice | ~75 s | 181 | 148 | 18.3 s | 54.4% | 4 | 0 | 0 |
| 10-26 | Amazon's money machine is AWS (autopilot, F) | animated, calm voice | ~70 s | 231 | 200 | 12.8 s | 50.5% | 6 | 0 | 1 |
| 10-25 | Starbucks is secretly a bank (2nd time!) | animated, energetic voice | 55 s | 412 | 342 | 17.3 s | 61.6% | 14 | 2 | 0 |
| 10-25 | Costco $1.50 hot dog | animated, energetic voice | 68 s | 1,227 | 1,069 | 23.0 s | 64.1% | 39 | 0 | 4 |
| 10-25 | 4 restaurant tricks | animated, calm voice | 75 s | 1,466 | 1,264 | 25.1 s | 67.0% | 30 | 4 | 6 |
| 10-25 | McDonald's is a real-estate company | cut-out collage | ~60 s | 1,281 | 1,069 | 20.3 s | 65.5% | 28 | 1 | 3 |
| 10-24 | Couple beat the lottery | AI footage | – | 39 | 23 | 10.3 s | 23.1% | 2 | 0 | 0 |
| 10-24 | 7 online shopping traps | AI footage | – | 190 | 167 | 23.1 s | 60.6% | 5 | 0 | 1 |
| 10-23 | 7 supermarket traps | AI footage | – | 2,816 | 2,630 | 2.8 s | 12.1% | 6 | 2 | 0 |
| 10-23 | 5 shipping traps | AI footage | – | 3,966 | 3,589 | 12.2 s | 26.0% | 35 | 2 | 3 |
| 10-22 | Whey protein boom | AI footage | – | 64 | 53 | 25.2 s | 11.1% | 3 | 0 | 1 |
| 10-22 | Compaq clean-room copy | AI footage | – | 130 | 112 | 14.9 s | 39.8% | 4 | 1 | 1 |
| 10-21 | Dubai chocolate boom | AI footage | – | 270 | 227 | 16.2 s | 39.5% | 4 | 0 | 1 |
| 10-21 | $2 in China → $19.99 on Amazon | AI footage | – | 4,636 | 4,315 | 2.9 s | 13.1% | 6 | 1 | 4 |
| 10-20 | Starbucks is secretly a bank (1st) | AI footage | – | 186 | 150 | 9.3 s | 33.6% | 5 | 0 | 0 |
| 10-20 | Is AI killing Salesforce? | AI footage | – | 92 | 55 | 7.9 s | 21.3% | 3 | 0 | 1 |
| 10-20 | Google stopped sending you customers | AI footage | – | 3,154 | 2,976 | 1.3 s | 4.4% | 6 | 1 | 0 |
| 10-19 | Makhana: farmers $5, US $160 | AI footage | – | 4,716 | 4,425 | 3.5 s | 17.3% | 24 | 11 | 10 |
(28 Oct 08:35 IST, R&D Visuals run 7: IG pull identical to 06:00 IST (gas 1,503, printer 1,376, restaurant 1,468, McDonald's 1,284; De Beers 0;
still no rows for Monopoly, Hoover, banana); YouTube rows identical to 27 Oct → nothing new; table left as is.)
(28 Oct 06:00 IST, banana run: IG pull ≈ identical again (restaurant 1,468, McDonald's 1,284, Compaq 132, shopping 193; De Beers still 0 —
posted 00:00 IST; Monopoly 05:00 IST not in the data yet); YouTube rows identical to 27 Oct (no rows after Chick-fil-A) → no new signal.
getScheduledPosts: De Beers + Monopoly PUBLISHED, Hoover pending 10:00 IST. Type log: De Beers B/E, Monopoly D, Hoover A, banana B.)
(28 Oct 04:40 IST, R&D Sound run 6: Instagram pull ≈ identical to 01:45 IST — restaurant 1,466 → 1,468, McDonald's 1,281 → 1,284, Compaq 130 → 132,
shopping 190 → 193, others ±1; De Beers still 0 (posted 00:00 IST, same-day rows are normally empty). YouTube rows identical to 27 Oct (still no rows after
Chick-fil-A) → nothing new to conclude; table above left as is.)
(28 Oct 01:45 IST, Hoover run: Instagram rows moved for the first time since 26 Oct — Planet Fitness jumped 209 → 1,279 views, gas station 1,503 on day 1; YouTube rows still identical to 27 Oct (no rows after Chick-fil-A).)
(27 Oct 23:30 IST, R&D Story run: **9th identical pull** on both platforms, every row number-for-number the same; still no rows for
Visa, Duolingo, gas, airline, De Beers, Monopoly. Sync stalled ~33 h.)
(27 Oct 21:00 IST, Monopoly run: **8th identical pull** on both platforms (IG + YT rows number-for-number the same as 15:40 IST; popcorn 5 views /
reach 0; no rows for Visa, Duolingo, gas, airline). getScheduledPosts: Visa, Duolingo, gas, airline PUBLISHED with live URLs, De Beers pending 28 Oct 00:00.
Metricool analytics sync stalled ~30 h → no new signal; the run leaned on insight I (types) and picked type D (Monopoly origin) to start the per-type test.)
(27 Oct 18:45 IST, R&D Topics run: **7th identical pull** on both platforms — popcorn still 5 views / reach 0, no rows for Visa,
Duolingo, gas station, airline miles; YouTube rows identical too. Metricool analytics sync has now been stalled ~24 h; nothing new to learn.)
(27 Oct 15:40 IST, De Beers run: **6th identical pull**, both platforms. getScheduledPosts shows Visa, Duolingo and gas station as
PUBLISHED on Instagram + YouTube with live URLs, yet none of them has an analytics row → the Metricool analytics sync is stalled, not the posts.)
(27 Oct 13:20 IST, R&D run 3: **5th identical pull**, still no rows for Visa, Duolingo or airline miles; popcorn still 5 views /
reach 0 → the Instagram side of the Metricool sync is stuck, not our reels. YouTube *does* move: Google 56 → 127, makhana appears (1,230).)
(27 Oct 10:10 IST, R&D run 2: **identical to the 05:45 and 09:15 IST pulls, number for number**, and no row at all yet for
Visa (posted 27 Oct 05:00 IST) or the 27 Oct posts → Metricool's Instagram reel sync looks stalled since ~26 Oct evening IST;
popcorn's "5 views / reach 0" is most likely a stale first snapshot, not a suppressed reel. Don't act on it until rows move.)
(27 Oct 09:15 IST, R&D run: every 10-26 row is unchanged since 05:45 IST, and popcorn is still 5 views / reach 0 / no watch data
about 9 h after posting — slower than any earlier autopilot post at this age (printer ink had >1k). Either Metricool's reel stats
lag or the reel got almost no test distribution; check it in the next run before reading anything into it. Visa (10-27 05:00 IST)
and Duolingo (10-27 10:00 IST, scheduled) are not in the data yet. YouTube `YTVP*` still not pulled — numbers were null on 26/27 Oct.)

## YouTube Shorts (snapshot 2026-10-31 ~14:30 IST; `YTVP06` views, `YTVP08` avg view duration s, likes `YTVP09`; rows now exist for every post through 28 Oct)
| Date | Video | Views | Avg view (s) | IG views same video |
|---|---|---|---|---|
| 10-28 | Hoover free flights | 98 | 21 | 143 |
| 10-28 | Monopoly's real inventor | 255 | 32 | 186 |
| 10-28 | De Beers 2 months' salary | 196 | 32 | 162 |
| 10-27 | Airline miles | 394 | 30 | 587 |
| 10-27 | Gas stations | 527 | 13 | 1,522 |
| 10-27 | Duolingo streak | **609** | **6** | 164 |
| 10-27 | Visa | 1 | 0 | 65 |
| 10-27 | Popcorn | 153 | 14 | 145 |
| 10-26 | Planet Fitness | 678 | 17 | 1,280 |
| 10-26 | Printer ink | 728 | 16 | 1,376 |
| 10-26 | Chick-fil-A closed Sundays | 1,001 (was 44 on 27 Oct) | 22 | 181 |
| 10-25/26 | Amazon AWS | 724 (was 326) | 17 | 231 |
| 10-25 | Starbucks is secretly a bank (2nd) | 135 | 17 | 412 |
| 10-25 | Costco $1.50 hot dog | 1,081 | 14 | 1,229 |
| 10-25 | 4 restaurant tricks | 1,059 | 22 | 1,468 |
| 10-25 | McDonald's real estate | 1,415 | 17 | 1,292 |
| 10-24 | Couple beat the lottery | 16 | 20 | 39 |
| 10-24 | 7 online shopping traps | 776 | 19 | 190 |
| 10-23 | 7 supermarket traps | 1,304 | 27 | 2,816 |
| 10-23 | 5 shipping traps | 1,289 | 30 | 3,966 |
| 10-22 | Whey protein | 940 | 22 | 64 |
| 10-22 | Copying the app (Compaq) | 1,332 | 30 | 130 |
| 10-21 | Dubai chocolate | 737 | 19 | 270 |
| 10-21 | $2 China → $19.99 Amazon | 210 | 36 | 4,636 |
| 10-20 | Salesforce SaaSpocalypse | 255 | 47 | 92 |
| 10-20 | Starbucks bank (1st) | 16 | 13 | 186 |
| 10-20 | Google stopped sending customers | 127 | 13 | 3,154 |
| 10-19 | Makhana: farmers $5, America $160 | 1,230 | 14 | 4,716 |
(YouTube rows keep growing for days — Chick-fil-A 44 → 1,001, AWS 326 → 724 in four days — so judge a Short after ≥ 72 h, not on day 1.)

## Insights (31 Oct ~14:30 IST, R&D writers' room run — first rows for the four story-type videos; media-kit numbers for BRAND.md)
S. **The story types did not fix reach, and nothing fixes reactions yet.** Instagram day-3 rows: Monopoly (D) 186 views / 31.2 s avg (channel
   best in seconds, but 23 % of its 135 s), Hoover (A) 143 / 16.3 s / 48 % 3-s, De Beers (B/E) 162 / 17.5 s / 48.6 %, banana (B) 132 / 24.4 s
   / 60.9 %. Every post since 27 Oct 15:00 IST sits at 65–190 views except airline (587) and gas (1,522) → the fall is account-wide and
   by *time*, not by type: 5 posts a day on 26–27 Oct split the non-follower test audience, and the long (118–135 s) story videos hold only
   15–23 % of their length. Shares + saves + comments across the last 10 reels: 4 + 2 + 0 on 3,681 reach = **1.6 reactions per 1,000 reach**;
   comments = 0 on all 29 posts ever. → This is the baseline the YOUR MOVE / SPOT THE TRICK format must beat (BRAND.md §5): the
   choice CTA + firstCommentText is the first thing we have ever built for comments.
T. **Media-kit numbers (BRAND.md §5), 31 Oct:** avg views of the last 10 Instagram reels **439** (median 164); avg 3-s rate 57 %; avg watch
   21.5 s; reactions 1.6 / 1,000 reach; YouTube last 10 Shorts avg **302** views (median 196; Duolingo 609 views but a 6-s average view =
   the title drew clicks the video lost in the first seconds — a title/hook mismatch to avoid). Follower growth: not in these pulls (add
   `IGFO*`/brandSummary next run). Audience countries: not pulled yet (demographic connector) — needed for the media kit.
U. *(Corrected by insight X, 3 Nov: the hold % gap is largely arithmetic.)* **Length vs hold:** the three videos over 115 s hold 15–23 % of their length; the 70–100 s ones 28–35 % (airline 28 %, Planet Fitness 35 %,
   Costco 34 %). Avg watch in *seconds* is flat (16–31 s) whatever the length → the first ~25 s decide, and a 2-minute script is paid
   for in completion rate. The two new episodes are written at ~120–125 s with a re-hook every ≤ 20 s and the roadmap labels; if their hold
   stays < 25 %, cut SPOT THE TRICK to 3 tricks / ≤ 95 s and YOUR MOVE singles to ≤ 100 s.
V. **YouTube numbers arrive late and keep rising:** Chick-fil-A 44 → 1,001 and AWS 326 → 724 between 27 and 31 Oct, Monopoly and De Beers
   32-s average views (their best metric on either platform) → the story videos *do* hold on YouTube; judge every Short at ≥ 72 h.

## Insights (28 Oct 10:40 IST, glasses run — type C)
R. 10th near-identical pull: IG rows unchanged since 01:45 IST (gas 1,503, printer 1,376, restaurant 1,468, McDonald's 1,284; De Beers
   still 0 views 10 h after posting — same-day/next-morning rows stay empty); still no rows for Monopoly (D), Hoover (A), banana (B);
   YouTube rows identical to 27 Oct (nothing after Chick-fil-A). → No new signal; the run follows insights L/O (viewer's own life) with the
   first **type C** (hidden giant) — "your glasses, the shop and your insurance", a topic on the viewer's face. Type log: De Beers B/E,
   Monopoly D, Hoover A, banana B, glasses C. Next run: check De Beers (118 s) and Monopoly (135 s) avg-watch % of length when rows land.

## Insights (28 Oct 08:35 IST, R&D Visuals run 7 — first 3 s of the *posted* MP4s vs 3-s rate; `lab/visuals/`)
Q. **Nothing we can measure in the first 3 seconds explains the 3-s rate (n = 9 animated reels with data).** Measured on the actual
   posted files (hosting branches): frame-0 detail, caption on frame 0, time to first caption, motion in 1 s / 3 s, cuts, colourfulness,
   brightness. Spearman vs IG 3-s rate: all |rho| ≤ 0.27 with Duolingo, ≤ 0.58 without (none p < 0.1). Five reels opened on an
   **empty glow disc** at frame 0 (AWS, Planet Fitness, Visa, Chick-fil-A, popcorn: 3-s 50–70 %, mean 56.5 %); four opened on the
   object + caption (printer 73.7, gas 66.9, airline 64.8 — and **Duolingo 24.8**). Duolingo's first 3 s look like the gas station's
   (caption at frame 0, object, similar motion) → its collapse was not the picture; most likely the topic/hook line (insight M revised).
   → The 3-s rate is driven by the topic and the hook *line* (insights I/L/O), not frame polish. Keep frame 1 alive (cheap, platform
   advice), but don't expect retention from visual tweaks alone. Every reel holds its first shot ≥ 3 s (0 cuts in 3 s, all 14 files).

## Insights (28 Oct 06:00 IST, banana run)
P. No new rows since 01:45 IST (same-day posts are always empty) → decisions still rest on insights L/O: the banana video is a type-B
   everyday object with a "that can't be right" hook, after two story types (D, A). First test of a **map timeline** (spread year by
   year) and a 1950s sepia flashback inside a B video — compare its avg-watch % of length (130 s) with gas (28 %) and printer ink (29 %).

## Insights (28 Oct 04:40 IST, R&D Sound run 6)
O. **By type, current Instagram rows (animated era):** B (gas, printer ink, Costco) mean 1,369 views / 68.2 % 3-s / 22.3 s avg watch;
   E (restaurant tricks) 1,468 / 67.0 % / 25.2 s; F (8 posts) mean 331 / 54.2 % / 17.6 s, median ~184 views — and the only F above 450 views
   is Planet Fitness ("your own gym habit", 1,279). A (Hoover) and D (Monopoly) have no rows yet. → Insight L stands: topics about the
   viewer's own life (B/E or F framed that way) hold ~14 points more past 3 s and ~4.7 s more watch. Sound changed in this run (word
   guard) — from the next video on, note "guard" in the run log so a retention change can be checked against it at n ≥ 5.

## Insights (28 Oct 01:45 IST, Hoover run — first fresh Instagram data in ~33 h)
L. **Everyday-object (B) topics keep winning on day 1:** gas station 1,503 views / 66.9 % 3-s / 22.4 s, printer ink 1,376 / 73.7 %,
   Costco 1,227 / 64.1 % → B ≈ 1,370 views. Pure F business-model posts from 26–27 Oct: Visa 59, popcorn 145, Duolingo 158, airline
   186, Chick-fil-A 181, AWS 231 views. **Exception:** Planet Fitness (F) grew late, 209 → 1,279 views, 69.5 % 3-s, 26.2 s (35 % of
   length — our best hold) — an F topic about *your own* gym habit behaves like B/E. → Insight I still stands, refined: what wins is
   "something in the viewer's own life", not the type letter.
M. **Duolingo's 3-second rate collapsed to 24.8 %** (every other animated reel 50–74 %) with a normal topic → the first frame /
   first line lost people, not the topic. Its hook was a slow statement over a phone prop. → Frame 1 must already be the surprising
   object in motion with the question on screen (PLAYBOOK §6); this run's frame 1 = a vacuum cleaner with wings spraying plane tickets.
N. **Roadmap prediction (insight K) — partly confirmed:** no-roadmap Duolingo 15 % of length, airline 24 %, Visa ~21 % (all < 25 %,
   as predicted), but gas station 28 % without one and roadmap popcorn only ~17 % → roadmap helps but is not sufficient; hook and
   topic matter more. Keep R8 (cheap) and judge again at n ≥ 10. De Beers (roadmap) and Monopoly have no data yet.
   Avg watch as % of length so far: Planet Fitness 35 %, Costco 34 %, restaurant 33 %, printer 29 %, gas 28 %, airline 24 %,
   AWS 18 %, popcorn 17 %, Duolingo 15 %.

## Insights (27 Oct 23:30 IST, R&D Story run — script structure vs retention; `tools/story_check.py`, `lab/story/`)
K. *(Weakened by insight X, 3 Nov, n = 18.)* **A roadmap in the script ("Step one… Step two", "four secrets, the last one is genius") goes with ~10 points more of the video
   watched.** Avg watch as % of length, Instagram: with roadmap Costco 34 %, Starbucks #2 31 %, Planet Fitness 30 %, printer ink 29 %
   (+ restaurant tricks 33 %) vs without Amazon 19 %, Chick-fil-A 24 %. Holds inside type F (Starbucks, Planet Fitness), so it is not
   only insight I. Item labels rho +0.93 with avg-watch % (n = 6 — direction, not proof; labels also track the 3-s rate, so part is
   "better videos overall"). Keyword "turns"/"but" counts ran the other way (rho −0.60/−0.72) → not used as rules.
   **Prediction to check when rows return:** the five newest videos without a roadmap (Visa, Duolingo, gas station, airline miles,
   Monopoly) hold < 25 % of their length; roadmap ones (De Beers, popcorn, and new videos following PLAYBOOK §4 R8) ≥ 28 %.
   Track a `roadmap` yes/no column for every new post; re-run `python3 lab/story/corr.py` at n ≥ 10.

## Insights (27 Oct 21:00 IST, Monopoly run)
J. Still no data after 26 Oct (8 identical pulls) → nothing new to conclude. Type log for the per-type test (fill when rows return):
   Visa F, Duolingo F/E, gas station B, airline miles F, De Beers B/E, Monopoly D (first non-F/B/E type). Compare 3-s rate and avg-watch % of length
   (Monopoly 133 s, De Beers 118 s vs 75–100 s) once ≥ 3 posts per type have rows.

## Insights (27 Oct 18:45 IST, R&D Topics run — by topic TYPE, PLAYBOOK §2; animated posts 25–26 Oct only, small n)
I. **Types B (everyday object) and E (trick you can spot) hold attention best; F (corporate model) holds least.**
   Instagram, animated era: B printer ink 74.0 % 3-s / 21.5 s / 1,366 views, B/F Costco hot dog 64.1 % / 23.0 s / 1,225;
   E restaurant tricks 67.0 % / 25.1 s / 1,466 → B+E mean ≈ 68 % / 23 s / ~1,350 views.
   F AWS 50.0 % / 13.1 s / 225, Chick-fil-A 54.2 % / 18.3 s / 176, Planet Fitness 64.0 % / 22.2 s / 209, Starbucks (repeat) 61.6 % / 17.3 s / 412
   → F mean ≈ 57 % / 17.7 s / ~255 views (the one F winner, McDonald's real estate 65.5 % / 1,281, had a story: Kroc + Sonneborn).
   YouTube agrees: E restaurant 1,007, B Costco 984 vs F AWS 326, Chick-fil-A 44, Starbucks 41. The best YT avg views are stories
   with people and a turn (Compaq clean-room 30 s, A/D-like). → R&D stocked topic_bank.md with 11 verified non-F topics (B×3, E×2,
   A×2, C×1, D×3). Next videos: B/E first, then A/C/D; F at most 1 in 3. Re-test this split once ≥ 3 posts per type have data.

## Insights (27 Oct 15:40 IST, De Beers run; earlier insights below still stand)
F. Now YouTube has frozen too (every row identical to 13:20 IST) → no new performance signal this run; decisions rest on insights 1, 3 and C.
G. YouTube likes (`YTVP09`, first pull): the pre-autopilot Shorts with the most views also have the most likes (McDonald's 28, Compaq 35,
   makhana 34, supermarket 30) and shares stay ≤ 1 everywhere → shares are the weakest signal on both platforms; keep testing a usable takeaway
   plus a send-to-a-specific-friend CTA.
H. Longer is not punished by itself: the best YouTube average view durations are on the longest explainers (Salesforce 47 s, China-Amazon 36 s,
   shipping traps 30 s) → this run tries a 117 s video with re-hooks every ~20 s; compare its avg view % with the 75–100 s ones.

## Insights (27 Oct 13:20 IST, R&D run 3)
E. YouTube keeps updating while Metricool's Instagram reel stats stay frozen (5 identical pulls over ~8 h) → for posts after 26 Oct,
   judge on YouTube numbers until Instagram rows move again. Makhana is the first topic that won on **both** platforms (IG 4,716 /
   YT 1,230): money gap in the title ("Farmers Get $5. America Pays $160.") — supports insight C.

## Insights (27 Oct 11:30 IST, airline-miles run; A/B from R&D run 2 still stand)
A. **New: YouTube is a second, independent signal.** Its winners differ from Instagram's: Compaq 1,332 vs 130 on IG, whey 940 vs 64,
   shopping traps 776 vs 190 — while the IG giants (makhana-style broad hooks, $2 China 4,636) did ~200 on YouTube. YouTube's
   avg view (13–47 s) is in seconds of a ~60–90 s Short; the animated autopilot videos sit at 14–22 s, same as on IG.
   → Judge a topic on both platforms; a "flop" on one is not a flop. Track YT views for every new post.
B. Metricool's Instagram numbers were frozen for > 12 h (see note under the table) → never conclude "suppressed" from one pull.
C. **YouTube finally reports numbers, and it disagrees with Instagram.** On YouTube most pre-autopilot Shorts got 740–1,360 views,
   while the three autopilot Shorts with data got 41–326. The YouTube winners have a **concrete number + tension in the title**
   ("I Went In for $1 Milk… and Paid $47", "Farmers Get $5. America Pays $160.") — our autopilot titles are flat statements
   ("Chick-fil-A Closed Sundays Yet Still Wins"). → From this run: YouTube title = the most surprising number + an open loop, still ≤ 50 chars keyword-first.
D. Metricool Instagram reel stats were still frozen at 11:00 IST (popcorn 5 views / reach 0; Visa and Duolingo absent) → re-check next run.
1. **Everyday-object hooks win.** Printer ink vs champagne (a thing you buy, an absurd comparison) got the best 3-s view rate we have ever had (74%) and 1.4k views. The corporate-structure topics (AWS, Chick-fil-A franchise deal, Planet Fitness 10-K) held 50–64% and stayed under 250 views. → Pick topics about something in the viewer's hand/phone/receipt, framed as a "that can't be right" comparison or question.
2. Animated explainers keep 50–74% past 3 s vs 4–40% for the old AI-footage reels; keep the format. Avg watch is stuck at ~13–23 s on 60–75 s videos → the middle still leaks. Re-hook card mid-video + a visual change every 2–3 s.
3. **Shares and saves are still ~0** on every autopilot post. The only posts with real shares/saves (restaurant tricks, makhana) gave the viewer something to *use* → end with a concrete takeaway the viewer can apply to their own life, not just a fun fact.
4. The calm voice did not lower retention (printer ink 21.5 s avg on the calm voice) → keep calm and natural.
5. Repeating a topic wastes a slot → always check post history (incl. the owner's manual uploads).
6. 10-26 numbers did not move between 02:10 and 05:45 IST: Metricool refreshes reel stats slowly, so judge a post after ~24 h, not same-day. Printer ink (an object everyone has bought + a price comparison) is still the clear winner → this run picks the gas pump (everyone has filled up) with a per-gallon cents reveal.
7. Comments are 0 on every autopilot post. Ending lines that ask the viewer to *do* something with their own wallet (pay at the pump) are cheap to test for comments/saves.
8. (R&D 27 Oct) If popcorn is still ~0 reach after 24 h, compare it with printer ink frame-by-frame (first frame, caption,
   first 2 s of VO) — a near-zero test distribution usually means the reel was held back (originality/quality signal), not that the hook failed.
