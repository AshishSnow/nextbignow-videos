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
- **Even pacing (added 27 Oct):** Chatterbox sometimes rushes long sentences and end-of-video CTAs (4.3–4.6 words/s against a 2.8–3.0 median). make_vo4.py now re-stretches any chunk of 5+ words above 3.5 words/s to about 3.3 (max 18% extra stretch) and logs it. Re-run an existing voice with `--reuse` to apply it without regenerating.
- **Checks:** every word is checked with the forced aligner. New words go into the aligner's custom dictionary.
- **Background jobs:** a background shell is killed after at most 2 hours, along with any renders it started. Don't use one long-running queue. Start each render on its own with `render_one.sh <episode> <out.mp4>` (about 25 minutes per 2:30 video).
- **Memory:** the voice model takes about 4.8 GB of the 8 GB box. Don't run a second heavy job beside it (an ffmpeg filtergraph that reads the same input twice got the voice job OOM-killed). Splice patches by encoding segments separately and using the concat demuxer.
- **Research note:** modern neural voices teach as well as human voices, but an obviously synthetic voice lowers enjoyment and trust. Keep the voice as natural and warm as possible, and listen for wrong stresses.

## 5. Visual rules

- **Scene length:** about 4–7 s per scene in 2–3 minute videos. Slower camera moves give the viewer time to absorb each idea.
- **Explaining things:** use explanatory graphics with subtle 3D cards, such as size bars, comparison charts and icon grids, at the moments that need them.
- **Captions:** two-tier and centred, at key moments only. The big-word baseline sat at y = 650 in the stick-figure look; from episode 33, see 5b.
- **Look:** vibrant sets, foreground depth-of-field dust and fog, a sound effect for every moment, and screen shake on impacts.
- **Sound under speech:** broadband noise effects (flush, crowd, waves, crash) go in the gaps between lines, not under words. The mix-alignment check catches it: words near a loud effect drift by more than 0.3 s.
- **Loop:** the final scene flows back into the hook frame.
- **Small caption line:** 30 characters or fewer. Longer lines run past the frame edges; put the detail in the voice, not the caption.
- **Before rendering:**
  - Do a layout pass *before* the voice exists: make a fake `align.json` from `paras.txt` (about 0.37 s per word, +0.4 s per sentence, +1.3 s per `---`) and render guide stills against it. Layout bugs get fixed while the voice is generating, so the real-timing check is quick.
  - Check a guide sheet with the safe-zone overlays (again with the real timings).
  - Check that the mix still lines up: align `mix16.wav` against the script and compare with the voice-only timings (mean drift should be under 0.05 s).
  - Look at a contact sheet of the rendered video.
- **Format variety:** YouTube's July 2026 rule penalises mass-produced, templated videos. Rotate formats: survivor story (24–27), myth-buster explainer (28), and keep new sets, props and gags per episode.

## 5b. The v3 look (from episode 33, approved 28 Oct)

The user asked for richer colour, a more natural 3D feel and new clothes (reference: the "yourtrainerarc" reels). Episode 33 is the first one in this look, and it replaces the stick mascot from now on.

- **Mascot ("Nova", `hero.py`):** painted 3D-look boy with a big head, spiky brown locks, thick brows, blush, real hands with fingers, and the **varsity outfit** (user picked B on 28 Oct): navy body, cream sleeves with a soft sheen, red and cream ribbed collar, cuffs and hem, a chenille "N" patch, snaps, a black tee, blue jeans, red high-tops and a watch. The other outfits stay in `OUTFITS` (`explorer`, `puffer`) for special episodes. It uses the same pose tuples as `toon.POSES`, so old scene code ports over.
- **Lighting:** every part goes through `shade()` (soft form shadow multiplied by the scene's ambient tint, a key highlight, a rim light in the scene's colour, and a self-coloured outline) plus cast shadows and ground contact shadows. Each set has its own `Light` (`L_DUSK`, `L_NIGHT`, `L_LAVA`, `L_WATER`…) with an `amb` exposure multiplier, so the character sits *in* the scene, not on top of it.
- **Hands:** never point with one raised finger. From the front it can read as a rude gesture. Point with the sideways finger-gun (`'point'`, thumb out) or use open hands.
- **Accessories:** `acc='shades' | 'sleepmask' | 'snorkel'`, and `arm_over` draws an arm in front of the face.
- **Sets (`cine.py`, `mcprops.py`):**
  - Layered parallax landscapes (sky, glowing Moon, three tree rows with haze between them, a textured field with clumped grass, and near grass drawn *in front of* the feet).
  - Depth-of-field blur on far rows and close-up backgrounds, plus bokeh, fireflies, dust, light rays and drifting cloud streaks.
  - A realistic procedural Moon and Io.
  - Space with nebulae; lunar surface; observatory; coastal city with a rising sea; underwater room; moonlit bedroom; ground cross-section; volcano land; Roche-limit ring debris.
- **Post (`engine3.Episode3`):** world, then camera and transitions (`punch`, `whip`, `flash`, `dip`), then grade + bloom + vignette + film grain (per-scene grade matrix), then a **crisp UI overlay** (captions and cards drawn after the grade), then the watermark.
- **Captions v3:** Anton condensed, white with a thick black stroke and a soft shadow, the key word in yellow, popping in. Rows: y 400/560 (top) or 1290/1450 (bottom). Info pills sit at y 345, under the watermark. Anton has no "×" or "≈", so write "X" and "~".
- **First frame:** no fade from black. The question text is on screen from frame 0 (YouTube decides "viewed vs swiped" on the first frame).
- **Anchors:** `ph()` returns the first match, so repeated phrases ("bring the Moon ten…") need `after=`. Print the scene table and check t0 < t1 for every scene.
- **File size:** film grain changes every frame, so a CRF 14 master comes out about 9 Mbps (186 MB for 2:50) and GitHub rejects anything over 100 MB. Deliver the master to the user, and host a 2-pass 4.2 Mbps copy for Metricool (94 MB, 47.9 dB PSNR against the master, so it looks identical). Next time try lighter grain (alpha about 0.03).
- **Cost:** about 1.3–2 s per frame per process. Render the two halves as **two separate background commands** (each has its own 2-hour limit); a 2:50 video takes about 70 minutes.

## 6. Posting

- **Instagram:** 4 a day at 05:30 (US evening), 10:00 (India peak), 14:30 and 19:00 IST while we had 1-minute reels. Since the switch to 2–3 minute videos (27 Oct), each new long video takes about 1.5 h to make, so new ones go out at 10:00 and 19:00 IST (2 a day) and quality comes first.
- **YouTube (since 27 Oct):** new 2–3 minute videos take the 19:30 IST Shorts slot; older 1-minute Shorts move to the 06:30 slots.
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

**Episode facts (27–32)**
- [Sylacauga meteorite (Wikipedia)](https://en.wikipedia.org/wiki/Sylacauga_(meteorite))
- [Encyclopedia of Alabama: Hodges meteorite strike](https://encyclopediaofalabama.org/article/hodges-meteorite-strike-sylacauga-aerolite/)
- [ScienceAlert: first recorded human meteorite strike](https://www.sciencealert.com/first-recorded-human-meteorite-strike-still-a-wild-tale-70-years-on)
- [Smithsonian Insider: meteorite landing speed and temperature](https://insider.si.edu/?p=24002)
- [Nature news 2005: quicksand can't swallow you](https://www.nature.com/news/2005/050926/full/news050926-9.html)
- [National Geographic: quicksand science](https://www.nationalgeographic.com/science/article/quicksand-science-why-it-traps-how-to-escape/)
- [Mental Floss: quicksand facts (1-in-35 films stat)](https://www.mentalfloss.com/science/geology/8-fascinating-facts-about-quicksand-01hh2se7qweb)
- [Smithsonian: Charles Osborne, who hiccuped for 68 years](https://www.smithsonianmag.com/history/the-curious-case-of-charles-osborne-who-hiccuped-for-68-years-straight-180980232/)
- [Howes 2012 (PMC): hiccups and the amphibian gill-ventilation hypothesis](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3504071/)
- [Guinness World Records: the 68-year hiccup attack](https://www.guinnessworldrecords.com/news/2023/7/extreme-measures-person-with-68-year-attack-of-hiccups-took-to-try-and-stop-them-754877)
- [Scientific American: does swallowed gum stay for seven years?](https://www.scientificamerican.com/article/fact-or-fiction-chewing-gum-takes-seven-years-to-digest/)
- [PubMed: chewing gum bezoars (Milov et al., Pediatrics 1998)](https://pubmed.ncbi.nlm.nih.gov/9685468/)
- [University of York: 5,700-year-old chewing gum DNA](https://www.york.ac.uk/news-and-events/news/2019/research/ancientchewinggumrevealsnewcluesaboutourancestors/)
- [Guinness World Records: longest hair (female), Xie Qiuping](https://www.guinnessworldrecords.com/world-records/longest-hair-female)
- [SYFY Wire: how long and strong can hair get (growth, 100 g per hair)](https://www.syfy.com/syfy-wire/rapunzel-hair-tangled-magical-science-possible)
- [José Salvador Alvarenga (Wikipedia)](https://en.wikipedia.org/wiki/Jos%C3%A9_Salvador_Alvarenga)
- [CNN via WTVR: real-life castaway survived 438 days lost at sea](https://www.wtvr.com/2016/01/08/real-life-castaway-survived-438-days-lost-at-sea)

### Episode facts (33)
- Moon recedes about 3.8 cm (1.5 in) a year, measured with the Apollo 11 retroreflector since 1969 (accuracy ~2 cm): [NASA JPL](https://www.jpl.nasa.gov/news/apollo-11-experiment-continues-to-return-valuable-data/)
- A day lasted just over 18 hours 1.4 billion years ago (Meyers & Malinverno, PNAS, 2018): [UW–Madison](https://news.wisc.edu/thank-the-moon-for-earths-lengthening-day)
- Earth–Moon Roche limit about 19,900 km; inside it a moon breaks up into a ring: [Sky at Night](https://www.skyatnightmagazine.com/space-science/roche-limit)
- Half the distance gives about 8x the tides (inverse cube), so 10x closer gives about 1000x the tidal pull; more quakes and volcanoes (Neil Comins, Jazmin Scarlett): [Space.com](https://www.space.com/what-if-moon-closer-to-earth)
- Phobos moves ~2 m closer to Mars per century and should break into a ring in ~20–40 million years (Mittal & Black, Nature Geoscience, 2015): [Space.com](https://www.space.com/31195-mars-may-get-rings-like-saturn.html)
- Solid ground rises and falls about 20 cm a day from Earth tides: [Old Farmer's Almanac](https://www.almanac.com/what-are-earth-tides-moons-surprising-pull-solid-earth)
- Supermoon up to 14% bigger and 30% brighter than at apogee (context): [Royal Museums Greenwich](https://www.rmg.co.uk/stories/space-astronomy/what-supermoon)

## 7b. Topic backlog (researched, not yet made)

- **What if you never stopped sneezing?** Donna Griffiths (UK) started sneezing on 13 Jan 1981 and had her first sneeze-free day on 16 Sep 1983, the 977th day. Guinness estimates about a million sneezes in the first year. Myth-busters: a measured sneeze peaks around 4.5 m/s (about 10 mph), not 100 mph (Tang et al. 2013). The photic sneeze reflex (the "ACHOO" syndrome) affects roughly 10–35% of people. Sources: [Guinness record](https://www.guinnessworldrecords.com/world-records/67595-longest-sneezing-fit), [PopSci on sneeze speed](https://www.popsci.com/science/article/2013-08/fyi-how-forceful-sneeze/), [PBS on the photic sneeze reflex](https://www.pbs.org/newshour/science/does-the-sun-make-you-sneeze). It is too close in format to the hiccups episode (29), so space it at least a week apart.
- **Space evergreen:** the Mars reel was our top Instagram reach. Rotate a space topic back in, for example a 2–3 minute "What if you fell into Jupiter?"

## 8. Improvement log

| # | Video | What changed | Result (fill in after 48 h) |
|---|---|---|---|
| 24 | What if a whale swallowed you? | 42 s instead of 61–84 s. 13 scenes, about 3 s per beat. Real story (Michael Packard, 2021). Loop ending. Subtle 3D cards. No yes/no comment bait. Re-voiced with voice C before publishing. | pending |
| 24 v2 | What if a whale swallowed you? (remake, 2:43) | Too fast (175 wpm), so rebuilt as a 2:43 version at 139 wpm. Humour beats (sandwich plan, "snack with a scuba tank", party story, snake twist). Three chapters with breaks. Size chart, 90-species grid, FAKE newspaper. Emotion tags in the voice. | pending |
| 25 | What if your elevator cable snapped? | Voice C from the start. Real story (Betty Lou Oliver, 1945). Depth-of-field foreground dust, drifting fog, speed lines. Camera follows the falling car. Warmer, more vibrant building palette. Physics moment (weightless float in the falling car). 3/4-view bomber. | pending |
| 25 v2 | What if your elevator cable snapped? (remake, 2:42) | 2–3 min format at 138 wpm, four chapters. Gags after each explanation ("steel spaghetti" mattress, jump-timing ceiling bonk, awkward silence callback). Elisha Otis 1854 demo with crowd. | pending |
| 26 | What if you fell out of a plane? | Juliane Koepcke (1971) + Vesna Vulović record. Terminal-velocity graph, starfish vs pencil cards, stopwatch. New layered rainforest set (light shafts, vines, ferns). "INSERT COIN" game-over gag. 141 wpm. | pending |
| 27 | What if a meteorite hit you? | Ann Hodges (1954). Crash animated in one continuous room set (roof → radio → hip) with camera push. Myth-buster beat (meteorites land cold) with a cross-section, then the frozen-mascot gag. Landlord/farmer twist ("space is not fair"). | pending |
| 28 | What if you stepped into quicksand? | First myth-buster format (no single survivor). Old-film sepia parody with film grain and sprocket holes, microscope grain view of liquefaction, density bars, stretched-arms gag, "really lazy" escape payoff. | pending |
| 29 | What if you never stopped hiccuping? | Charles Osborne (68 years). Weird-body science format. Synthesised "hic" sound effect synced to every on-screen jolt. Animated diaphragm and vocal-cord cutaway, odometer to 430 million, envelope avalanche, shotgun-scare and "I do" gags. First voice with even pacing. | pending |
| 30 | What if you swallowed your gum? | Journey format: follow one piece of gum (mouth → stomach → gut → exit) with a gum mascot that has a face. Myth-buster with a real 1998 case and a 5,700-year-old birch-tar "gum" twist. Close-up inset card for the gum-on-shoe gag. | pending |
| 31 | What if you never cut your hair? | Growth cycle shown on an animated follicle (grow, rest, fall, new). "100,000 tiny projects quitting" gag. Xie Qiuping record vs a giraffe. Strength twist: one hair holds an apple, a full head two elephants. Circus hair-hang and tower ending. | pending |
| 32 | What if you got lost at sea? | Salvador Alvarenga, 438 days adrift. Ocean set with bobbing skiff and a beard that grows across the episode. Map of the Pacific drift, seawater "debt" explainer with an IOU-stack gag, turtle-blood vs smoothie, quiet night scene for the sad beat (no gag), island arrival "HOLA!" gag. | pending |
| 33 | What if the Moon came 10x closer? | **First v3 look**: painted 3D varsity mascot, cinematic dusk/night sets, DOF, bloom, grade and grain, crisp overlay captions. Real anchor: the Apollo 11 mirror panel (1969) and lunar laser ranging (Moon recedes 3.8 cm a year). Explainers: 10x wider and 100x brighter (10x10 grid of moons), 1000x tides (10x10x10 card), ground tides 20 cm, Io, Roche limit (~20,000 km) with the Moon shattering into a ring, Phobos, 18-hour days 1.4 billion years ago. Gags: sunglasses at midnight, sleep mask, snorkel in the beach house, Earth as a stress ball, sneaky Moon, fingernail speed. 2:50, 144 wpm. Mix drift 0.010 s. Instagram Nov 2 19:00, YouTube Nov 7 19:30 IST. | pending |
