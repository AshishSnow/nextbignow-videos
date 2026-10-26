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
- 30–45 s is the sweet spot.
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
- Reels over 90 s are not recommended to non-followers. Aim for under 60 s.
- Use 3–5 specific hashtags.
- Never ask for a specific comment word ("Comment YES or NO"). Instagram says that can limit reach. Ask an open question instead.

## 3. Script rules

- **Opening:** line 1 is the intro question ("What would happen if…?"), with visual action inside the first 1.5 s.
- **Length:** about 100–115 words (about 40–45 s). One story, 4–6 beats, each explained clearly. Don't rush.
- **Content:**
  - Lead with real stories and real numbers.
  - Check every fact against a source before voicing it.
  - Make it conversational: contractions, short sentences, "..." beats before reveals.
- **Format:** spell numbers out as words in the voice script.
- **Ending:** close on an open question that flows back into the first frame.

## 4. Voice (make_vo3.py, chosen 26 Oct: voice "C")

- **Model:** Chatterbox Turbo, cloning the channel's approved young male voice from the reference clip `ref_voice.wav`. Same voice as before, more natural rhythm and intonation.
- **Pacing:** one call per paragraph, and each '...' becomes its own beat with a controlled pause. Silence is trimmed and chunk loudness evened out.
- **Mastering:** EQ, de-ess and compression to −16 LUFS. Every word is checked with the forced aligner; a missing or repeated word means regenerate with a new seed.
- **Speed:** about 3 minutes per 40-second voiceover on this CPU.
- **Earlier versions:**
  - make_vo2.py: Kokoro with per-sentence pacing and PSOLA. Fallback only.
  - make_vo.py: the original. Retired.
- **Next to test:** emotion and laugh tags on punchlines, emphasis on key words, and a short A/B listening test each week.

## 5. Visual rules

- A new beat every 3–4 s: cuts, camera push-ins, and varied transitions (wipe, whip, zoom, flash).
- Captions only at key moments, two-tier and centred. The big-word baseline sits at y = 650 so it clears the watermark and the safe zones.
- Vibrant sets and subtle 3D cards (`card3d`).
- A sound effect for every moment, and screen shake on impacts.
- The final scene transitions back into the hook frame (loop).
- Before rendering, check a guide sheet with the safe-zone overlays.

## 6. Posting

- **Instagram:** 4 a day at 05:30 (US evening), 10:00 (India peak), 14:30 and 19:00 IST.
  - Caption starts with the keyword, max 5 hashtags.
  - Include alt text, a first-comment question and the AI label.
- **YouTube:** 2 Shorts a day at 06:30 (US evening) and 19:30 IST. Full videos at 21:30 IST.
  - Titles start with the keyword, with 8–10 long-tail tags. No #shorts.

## 7. Improvement log

| # | Video | What changed | Result (fill in after 48 h) |
|---|---|---|---|
| 24 | What if a whale swallowed you? | 42 s instead of 61–84 s. 13 scenes, about 3 s per beat. Real story (Michael Packard, 2021). Loop ending. Subtle 3D cards. No yes/no comment bait. Re-voiced with voice C before publishing. | pending |
| 25 | What if your elevator cable snapped? | Voice C from the start. Real story (Betty Lou Oliver, 1945). Depth-of-field foreground dust, drifting fog, speed lines. Camera follows the falling car. Warmer, more vibrant building palette. Physics moment (weightless float in the falling car). 3/4-view bomber. | pending |
