# NextBigNow "What If" — improvement playbook

Run this loop before every new video. Every video has to beat the last one on voice, visuals or retention.
Last updated: 26 Oct 2026.

## 1. Check the data first (Metricool)

- **Instagram:** reach, views, average watch time, 3-second view rate, shares, saves.
- **YouTube:** views, average view duration, likes, comments, shares.
- Write down the top 3 and bottom 3 and what explains them: topic, hook, length, time posted.

**Snapshot, 26 Oct (Instagram, first 11 reels):**

| Reel | Reach | Avg watch | 3 s view rate |
|---|---|---|---|
| Mars | 3,247 | 13.7 s | 29% |
| Ice melted | 1,251 | 24.3 s | 64% |
| Asteroid | 1,127 | **30.7 s** | 67% |
| Megalodon | 1,110 | 26.5 s | **71%** |
| Earth spin | 1,095 | 28.9 s | 64% |
| Trench | 1,091 | 23.0 s | 66% |
| Moon | 318 | 21.8 s | 56% |
| Sun | 265 | 23.7 s | 57% |
| Volcano | 227 | 19.6 s | 54% |
| Gravity | 198 | 16.3 s | 51% |
| Internet | 150 | 14.5 s | 45% |

**What the snapshot says:**

- Physical danger and big-impact topics (sharks, asteroids, the deep sea, Earth's spin) reach about 5x more people than abstract or tech topics.
- People watched about 15–30 s of 61–84 s videos, so viewers were leaving halfway. New Shorts aim for about 40–50 s, with fewer points, each explained properly.
- Shares and saves were close to zero. Real stories and surprising twists are what get shared.

## 2. Algorithm rules (2026)

**YouTube Shorts**

- The hook has to land in the first 2 s.
- The main gate is viewed vs. swiped away, plus average % viewed. Aim for 50% or more on a 30–60 s Short.
- Shorts can now run up to 3 minutes, and 2–3 minutes is our format. To hold retention over that length, bring in a new beat, question or joke every 20–30 s.
- Change the visual every 3–4 s.
- End on a frame that loops back into the opening.
- Burn in the key captions.
- Write the title as the phrase people actually search.
- Post 1–2 Shorts a day at consistent times.
- Comments count heavily.

**YouTube monetization (16 July 2026 "inauthentic content" clarification)**

- Template-based, repetitive or mass-produced videos are not monetized.
- Every video needs a new set, a new opening and a new structure.
- Add a real research angle, such as a real story or real numbers.

**Instagram Reels**

- Ranking signals:
  - Watch time and replays come first.
  - Sends per reach (DM shares) drive reach to non-followers.
  - Likes per reach matter for followers.
- Keep content original, turn the AI label on, and never post with another app's watermark.
- Reels up to 3 minutes can now be recommended to non-followers (Instagram, Jan 2025). 2026 data shows 2–3 minute reels get about the same median views as 60–90 s ones. Stay under 3 minutes.
- Use 3–5 specific hashtags.
- Never ask for a specific comment word ("Comment YES or NO"). Instagram says that can limit reach. Ask an open question instead.

## 3. Script rules (updated 27 Oct, from the research rulebook; links at the end)

**Length and pace.** 2:00–2:55. Never go over 2:55: both YouTube Shorts and Instagram Reels top out at 3 minutes.
- Aim for about 140–160 words per minute, including pauses. Ashish found 175 wpm too fast.
- Word counts:
  - 2:00 ≈ 290–330 words
  - 2:30 ≈ 360–400 words
  - 2:45 ≈ 400–430 words

**Structure: 3–4 chapters.** Each chapter answers one sub-question.
- Leave a 1.5–2 s pause with only visuals at every chapter break. In the script this is a `---` line.
- Say the structure out loud ("Reason number one…") and back it up on screen with arrows, zooms and highlights.

**Beat template for 2:30:**

| Time | Beat |
|---|---|
| 0:00–0:03 | Visual shock + the "What if…?" question |
| 0:03–0:15 | Stakes + an open loop |
| 0:15–0:35 | Real named person, place and date |
| 0:35–1:10 | Chapter 1: but → therefore |
| 1:10–1:45 | Chapter 2: a new "but", a question, a short pause, a surprise answer |
| 1:45–2:15 | Pay off the opening loop |
| 2:15–2:30 | Callback joke + CTA |

**Story rules:**
- Join scenes with "but" or "therefore", never "and then".
- Close every open loop within about 45 s.
- Write to "you", in a conversational style.

**Humour rules:**
- Jokes must be about the topic.
- Explain the mechanism straight first, then add the joke.
- The mascot is the butt of the joke, never the viewer.
- About one gag every 20–30 s.
- No gag stays on screen next to a diagram.
- Use the rule of three with a true, absurd third item.
- Use deadpan understatement and silly-but-accurate scale comparisons.
- End on a callback.

**Facts:** every fact gets a source before it's voiced. Numbers are spelled out as words in the voice script.

**Captions:** key words only, at key moments, centred. Never a full transcript.

**Music:** only our own synthesised score. Any copyright claim on a Short over 1 minute blocks it worldwide.

## 4. Voice (make_vo4.py, voice "C" = Chatterbox Turbo cloning the approved young male voice)

- **Generation:** each sentence and each '...' beat is generated separately.
- **Emotion tags:** these go at the start of a sentence: `[dramatic]`, `[surprised]`, `[sarcastic]`, `[whispering]`, `[chuckle]`, `[happy]`, `[fear]`. Use them on punchlines and reveals. Overusing them makes the delivery sound fake.
- **Speed:** Rubber Band time-stretch at tempo 0.9 (pitch and formants preserved). Net speed is about 140 wpm.
- **Pauses:**
  - 0.4 s between sentences
  - 0.6 s on '...' beats
  - +0.25 s between paragraphs
  - +1.3 s at chapter breaks (`---`)
- **Checks:** every word is checked with the forced aligner. New words go into the aligner's custom dictionary.
- **Research note:** modern neural voices teach as well as human voices, but an obviously synthetic voice lowers enjoyment and trust. Keep the voice as natural and warm as possible, and listen for wrong stresses.

## 5. Visual rules

- **Scene length:** about 4–7 s per scene in 2–3 minute videos. Slower camera moves give the viewer time to absorb each idea.
- **Explaining things:** use explanatory graphics with subtle 3D cards, such as size bars, comparison charts and icon grids, at the moments that need them.
- **Captions:** two-tier and centred, at key moments only. The big-word baseline sits at y = 650.
- **Look:** vibrant sets, foreground depth-of-field dust and fog, a sound effect for every moment, and screen shake on impacts.
- **Loop:** the final scene flows back into the hook frame.
- **Before rendering:**
  - Check a guide sheet with the safe-zone overlays.
  - Look at a contact sheet of the rendered video.

## 6. Posting

- **Instagram:** 4 a day at 05:30 (US evening), 10:00 (India peak), 14:30 and 19:00 IST.
  - Caption starts with the keyword, max 5 hashtags.
  - Include alt text, a first-comment question and the AI label.
- **YouTube:** 2 Shorts a day at 06:30 (US evening) and 19:30 IST. Full videos at 21:30 IST.
  - Titles start with the keyword, with 8–10 long-tail tags. No #shorts.

## 7. Research sources (27 Oct 2026)

**Pace**
- [Guo et al. 2014: video engagement](https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf)
- [Murphy et al. 2022: lecture speed and comprehension](https://castel.psych.ucla.edu/wp-content/uploads/sites/111/2022/03/Applied-Cognitive-Psychology-2021-Murphy-Learning-in-double-time-The-effect-of-lecture-video-speed-on-immediate-and.pdf)

**Multimedia learning**
- [Mayer 2020: multimedia principles](https://ugc.futurelearn.com/uploads/files/7d/d6/7dd6188d-c343-4311-b064-ac98d2c95abc/Multimedia_Principles._R._E._Mayer__2020.pdf)
- [Rey et al. 2019: segmenting meta-analysis](https://is.tuebingen.mpg.de/publications/rey2018segmenting)
- [Sundararajan & Adesope 2020: seductive details](https://news.wsu.edu/press-release/2020/03/19/seductive-details-inhibit-learning)
- [Ginns et al. 2013: conversational style](https://researchers.westernsydney.edu.au/en/publications/designing-instructional-text-in-a-conversational-style-a-meta-ana/)
- [Siegle 2022: synthetic vs human voice](https://keep.lib.asu.edu/system/files/c7/Siegle_asu_0010N_22109.pdf)

**Humour**
- [Banas et al. 2011, via Faculty Focus: humour in teaching](https://www.facultyfocus.com/articles/effective-teaching-strategies/humor-in-the-classroom-40-years-of-research/)
- [Bolkan, Griffin & Goodboy 2018: humour and learning](https://natcom.org/node/2520)

**Curiosity and story**
- [Loewenstein 1994: psychology of curiosity](https://stafforini.com/works/loewenstein-1994-psychology-curiosity-review/)
- [Kang et al. 2009: curiosity and memory](https://www.cmu.edu/dietrich/sds/docs/loewenstein/WickCandleLearning.pdf)
- [Dahlstrom 2014: storytelling for science](https://uvm.edu/~mjk/195%20Winter%20Tracking%20Specialty/Using%20narratives%20and%20storytelling%20to%20communicate%20science%20with%20nonexpert%20audiences.pdf)

**Platforms**
- [YouTube: 3-minute Shorts](https://blog.youtube/news-and-events/tall-updates-coming-to-shorts/)
- [YouTube Help: music claims on longer Shorts](https://support.google.com/youtube/answer/15424877?hl=en)
- [Instagram: 3-minute Reels shown to non-followers](https://creators.instagram.com/blog/the-latest-with-instagram?)
- [Socialinsider: Reels length data 2026](https://socialinsider.io/blog/instagram-reels-length/)

## 8. Improvement log

| # | Video | What changed | Result (fill in after 48 h) |
|---|---|---|---|
| 24 | What if a whale swallowed you? | 42 s instead of 61–84 s. 13 scenes, about 3 s per beat. Real story (Michael Packard, 2021). Loop ending. Subtle 3D cards. No yes/no comment bait. Re-voiced with voice C before publishing. | pending |
| 24 v2 | What if a whale swallowed you? (remake, 2:43) | Too fast (175 wpm), so rebuilt as a 2:43 version at 139 wpm. Humour beats (sandwich plan, "snack with a scuba tank", party story, snake twist). Three chapters with breaks. Size chart, 90-species grid, FAKE newspaper. Emotion tags in the voice. | pending |
| 25 | What if your elevator cable snapped? | Voice C from the start. Real story (Betty Lou Oliver, 1945). Depth-of-field foreground dust, drifting fog, speed lines. Camera follows the falling car. Warmer, more vibrant building palette. Physics moment (weightless float in the falling car). 3/4-view bomber. | pending |
