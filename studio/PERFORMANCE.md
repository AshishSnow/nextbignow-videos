# OopsMyBusiness — what our videos actually did

Update every run (Metricool `getAnalyticsDataByMetrics`, brand 7643430, last 21 days):
- Instagram reels fields: `IGRE02` date, `IGRE03` caption, `IGRE23` views, `IGRE11` reach, `IGRE24` avg watch time (s),
  `IGRE28` 3-second view rate (%), `IGRE21` shares, `IGRE12` saves, `IGRE10` likes, `IGRE07` comments.
- YouTube fields: `YTVP02` date, `YTVP17` title, `YTVP06` views, `YTVP08` avg view duration, `YTVP09` likes, `YTVP12` shares.
  Numbers arrive since 27 Oct (views + avg view duration in s; likes/shares not checked yet). The "all videos" connector
  (`YTVV*`) returned nothing on 26 Oct. Pull `YTVP02,YTVP17,YTVP06,YTVP08` every run into the YouTube table below.
- Instagram numbers for posts published the same day are usually empty — read them the next run.
Add new rows, refresh rows younger than 7 days, then rewrite the **Insights** section from the data.

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
U. **Length vs hold:** the three videos over 115 s hold 15–23 % of their length; the 70–100 s ones 28–35 % (airline 28 %, Planet Fitness 35 %,
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
K. **A roadmap in the script ("Step one… Step two", "four secrets, the last one is genius") goes with ~10 points more of the video
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
