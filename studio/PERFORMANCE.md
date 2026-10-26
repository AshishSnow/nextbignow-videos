# OopsMyBusiness — what our videos actually did

Update every run (Metricool `getAnalyticsDataByMetrics`, brand 7643430, last 21 days):
- Instagram reels fields: `IGRE02` date, `IGRE03` caption, `IGRE23` views, `IGRE11` reach, `IGRE24` avg watch time (s),
  `IGRE28` 3-second view rate (%), `IGRE21` shares, `IGRE12` saves, `IGRE10` likes, `IGRE07` comments.
- YouTube fields: `YTVP02` date, `YTVP17` title, `YTVP06` views, `YTVP08` avg view duration, `YTVP09` likes, `YTVP12` shares.
  As of 26 Oct these return titles but **null numbers**, and the "all videos" connector (`YTVV*`) returns nothing — Metricool
  isn't getting YouTube analytics for this channel. Try once per run; until numbers appear, Instagram is the signal.
- Instagram numbers for posts published the same day are usually empty — read them the next run.
Add new rows, refresh rows younger than 7 days, then rewrite the **Insights** section from the data.

## Instagram (snapshot 2026-10-26 21:50 IST)
| Date | Video | Style | Len | Views | Reach | Avg watch | 3-s view rate | Likes | Shares | Saves |
|---|---|---|---|---|---|---|---|---|---|---|
| 10-25 | Starbucks is secretly a bank (2nd time!) | animated, energetic voice | 55 s | 241 | 199 | 15.4 s | 52.9% | 5 | 0 | 0 |
| 10-25 | Costco $1.50 hot dog | animated, energetic voice | 68 s | 494 | 443 | 20.9 s | 58.9% | 21 | 0 | 1 |
| 10-25 | 4 restaurant tricks | animated, calm voice | 75 s | 1,436 | 1,245 | 25.2 s | 67.6% | 29 | 4 | 5 |
| 10-25 | McDonald's is a real-estate company | cut-out collage | ~60 s | 1,241 | 1,029 | 20.5 s | 65.6% | 26 | 1 | 3 |
| 10-24 | Couple beat the lottery | AI footage | – | 37 | 21 | 11.0 s | 25.0% | 2 | 0 | 0 |
| 10-24 | 7 online shopping traps | AI footage | – | 187 | 165 | 23.5 s | 61.7% | 5 | 0 | 1 |
| 10-23 | 7 supermarket traps | AI footage | – | 2,814 | 2,623 | 2.8 s | 12.0% | 6 | 2 | 0 |
| 10-23 | 5 shipping traps | AI footage | – | 3,964 | 3,583 | 12.2 s | 26.0% | 35 | 2 | 3 |
| 10-22 | Whey protein boom | AI footage | – | 62 | 51 | 26.0 s | 11.5% | 3 | 0 | 1 |
| 10-22 | Compaq clean-room copy | AI footage | – | 129 | 111 | 15.0 s | 40.2% | 4 | 1 | 1 |
| 10-21 | Dubai chocolate boom | AI footage | – | 267 | 225 | 16.4 s | 39.8% | 4 | 0 | 1 |
| 10-21 | $2 in China → $19.99 on Amazon | AI footage | – | 4,634 | 4,315 | 2.9 s | 13.1% | 6 | 1 | 4 |
| 10-20 | Starbucks is secretly a bank (1st) | AI footage | – | 185 | 149 | 9.3 s | 33.8% | 5 | 0 | 0 |
| 10-20 | Is AI killing Salesforce? | AI footage | – | 90 | 55 | 8.0 s | 20.3% | 3 | 0 | 1 |
| 10-20 | Google stopped sending you customers | AI footage | – | 3,154 | 2,976 | 1.3 s | 4.4% | 6 | 1 | 0 |
(Autopilot posts from 26 Oct onward: Amazon/AWS, Chick-fil-A, printer ink, Planet Fitness, cinema popcorn, Visa — add when their data arrives.)

## Insights (rewrite each run)
1. Our **animated explainers hold attention far better** (3-s view rate 53–68%, avg watch 15–25 s) than the older AI-footage reels (4–40%). Keep the animated format.
2. **Reach** has been highest for broad money hooks with a personal number ("$2 in China, $19.99 on Amazon", "I shipped a $10,000 box") — but those lost people in 3 s. Goal: broad, personal money hook **+** animated clarity.
3. Avg watch is only ~25–35% of the length → the middle loses people. Add a re-hook every ~10 s (open loop: "and the third one is the craziest"), change the picture every 2–3 s, keep sentences short, pay off at the very end.
4. **Shares and saves are near zero** → end with a useful takeaway the viewer can act on, and a CTA naming a very specific friend.
5. The calm, slower restaurant voice held best so far (25 s avg). Don't rush: slower, clearer delivery with real highs and lows (owner's request) — test it, don't assume.
6. Repeating a topic (Starbucks twice) wastes a slot → always check the post history before choosing.
