# OopsMyBusiness — what our videos actually did

Update every run (Metricool `getAnalyticsDataByMetrics`, brand 7643430, last 21 days):
- Instagram reels fields: `IGRE02` date, `IGRE03` caption, `IGRE23` views, `IGRE11` reach, `IGRE24` avg watch time (s),
  `IGRE28` 3-second view rate (%), `IGRE21` shares, `IGRE12` saves, `IGRE10` likes, `IGRE07` comments.
- YouTube fields: `YTVP02` date, `YTVP17` title, `YTVP06` views, `YTVP08` avg view duration, `YTVP09` likes, `YTVP12` shares.
  As of 26 Oct these return titles but **null numbers**, and the "all videos" connector (`YTVV*`) returns nothing — Metricool
  isn't getting YouTube analytics for this channel. Try once per run; until numbers appear, Instagram is the signal.
- Instagram numbers for posts published the same day are usually empty — read them the next run.
Add new rows, refresh rows younger than 7 days, then rewrite the **Insights** section from the data.

## Instagram (snapshot 2026-10-27 09:15 IST)
| Date | Video | Style | Len | Views | Reach | Avg watch | 3-s view rate | Likes | Shares | Saves |
|---|---|---|---|---|---|---|---|---|---|---|
| 10-27 | Movie theaters make money on popcorn (autopilot) | animated, calm voice | ~75 s | 5 | 0 | – | – | 1 | 0 | 0 |
| 10-26 | Printer ink costs more than champagne (autopilot) | animated, calm voice | ~75 s | 1,366 | 1,187 | 21.5 s | **74.0%** | 20 | 0 | 0 |
| 10-26 | Planet Fitness $15/month (autopilot) | animated, calm voice | ~75 s | 209 | 166 | 22.2 s | 64.0% | 4 | 0 | 0 |
| 10-26 | Chick-fil-A closed Sundays (autopilot) | animated, calm voice | ~75 s | 176 | 143 | 18.3 s | 54.2% | 4 | 0 | 0 |
| 10-26 | Amazon's money machine is AWS (autopilot) | animated, calm voice | ~70 s | 225 | 193 | 13.1 s | 50.0% | 6 | 0 | 1 |
| 10-25 | Starbucks is secretly a bank (2nd time!) | animated, energetic voice | 55 s | 412 | 342 | 17.3 s | 61.6% | 14 | 2 | 0 |
| 10-25 | Costco $1.50 hot dog | animated, energetic voice | 68 s | 1,225 | 1,066 | 23.0 s | 64.1% | 39 | 0 | 4 |
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
(27 Oct 09:15 IST, R&D run: every 10-26 row is unchanged since 05:45 IST, and popcorn is still 5 views / reach 0 / no watch data
about 9 h after posting — slower than any earlier autopilot post at this age (printer ink had >1k). Either Metricool's reel stats
lag or the reel got almost no test distribution; check it in the next run before reading anything into it. Visa (10-27 05:00 IST)
and Duolingo (10-27 10:00 IST, scheduled) are not in the data yet. YouTube `YTVP*` still not pulled — numbers were null on 26/27 Oct.)

## Insights (rewrite each run — 27 Oct 09:15 IST, R&D run: no new numbers since 05:45, insights stand)
1. **Everyday-object hooks win.** Printer ink vs champagne (a thing you buy, an absurd comparison) got the best 3-s view rate we have ever had (74%) and 1.4k views. The corporate-structure topics (AWS, Chick-fil-A franchise deal, Planet Fitness 10-K) held 50–64% and stayed under 250 views. → Pick topics about something in the viewer's hand/phone/receipt, framed as a "that can't be right" comparison or question.
2. Animated explainers keep 50–74% past 3 s vs 4–40% for the old AI-footage reels; keep the format. Avg watch is stuck at ~13–23 s on 60–75 s videos → the middle still leaks. Re-hook card mid-video + a visual change every 2–3 s.
3. **Shares and saves are still ~0** on every autopilot post. The only posts with real shares/saves (restaurant tricks, makhana) gave the viewer something to *use* → end with a concrete takeaway the viewer can apply to their own life, not just a fun fact.
4. The calm voice did not lower retention (printer ink 21.5 s avg on the calm voice) → keep calm and natural.
5. Repeating a topic wastes a slot → always check post history (incl. the owner's manual uploads).
6. 10-26 numbers did not move between 02:10 and 05:45 IST: Metricool refreshes reel stats slowly, so judge a post after ~24 h, not same-day. Printer ink (an object everyone has bought + a price comparison) is still the clear winner → this run picks the gas pump (everyone has filled up) with a per-gallon cents reveal.
7. Comments are 0 on every autopilot post. Ending lines that ask the viewer to *do* something with their own wallet (pay at the pump) are cheap to test for comments/saves.
8. (R&D 27 Oct) If popcorn is still ~0 reach after 24 h, compare it with printer ink frame-by-frame (first frame, caption,
   first 2 s of VO) — a near-zero test distribution usually means the reel was held back (originality/quality signal), not that the hook failed.
