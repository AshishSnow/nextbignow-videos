# FreshNestHub (FNH) posting strategy — owner decision 25 Nov 2026

## Instagram (@fnhtruths) — via Metricool
- Every reel goes out as a **TRIAL REEL** first (instagramData.type = "TRIAL_REEL"): shown to non-followers only, so a weak reel never hurts the main grid.
- Time: **09:50 IST** daily (Metricool best-time data: audience peaks at 10:00, second peak 18:00). One reel per day, never two in the same day.
- After 24 h, check in Metricool: views, skip rate (IGRE30), avg watch (IGRE24).
  - Winner = skip rate < 45% AND avg watch > 12 s (or views > 2x the trial average) -> owner taps "Share to profile" in the IG app.
  - Loser stays a trial; change ONE brick (title / first frame / hook line) for the next topic.
- Caption: Hinglish hook line, 3–4 short Hindi lines, source line, share line. Max 5 hashtags. First comment = yes/no question.
- isAiGenerated = true. Custom cover (videoThumbnailUrl) always.

## YouTube (@FreshnestHub) — OWNER POSTS MANUALLY. Do NOT schedule YouTube in Metricool.
- For each reel, deliver: the MP4 + a copy-paste kit (Hindi-first title, Hindi/Hinglish description, tags, pinned comment).
- Title format: `<Hindi title> | <Hinglish words> #shorts` — no English-only titles (Hindi voice + English title = wrong test audience; Shorts got 0–14 views in Oct–Nov).
- Upload from the YouTube app; Language + Audio language = Hindi; Made for kids = No; one Short per day, evening (~18:00) after the IG trial.
- One-time channel settings: default language Hindi; check Studio for any reused/limited-content notice.

## Content rules
- Topic = desi family rule / everyday habit + surprising twist + real proof (the chai and fish winners). Check the FULL topics_done.md before suggesting.
- 30–35 s target; colour theme by topic type; black frames between ideas; everything in motion; owner's real images.
- One improvement test per reel, written in topics_done.md ("TEST: ...").

## Script system v3 (26 Nov 2026, learned from 2 viral doc-style reels: 73–78 s, ~150 wpm)
Write the LAST line first (an ironic payoff or callback), then build backwards.
1. Pointing hook (0–3 s): "ये है ___" + a surprising identity or familiar comparison, spoken over the title frame. The main answer goes in this first line.
2. Paradox (3–7 s): "जिस चीज़ को हमने ___ समझा, वही ___" opens a loop the viewer needs closed.
3. Story proof with time markers: "2012 में…", "रात भर…", "सुबह…". Time words drive the story, not "और फिर".
4. One vivid concrete detail people can picture (they deliberately added cholera germs; a real number, a real place). Never generic.
5. Contrast turn: "पर…", "वहीं…". Show the side-by-side result as two short fragments.
6. Why, compared to something familiar; one line, 5th-grade words.
7. Honesty line: what it does NOT do. This builds trust and lowers "fake" comments.
8. Payoff: irony or callback to the hook ("same call, same man"). End the moment it lands, with no CTA, no doctor line, no "share".
Rhythm: fragments of 3–7 words, rule of three, a "basically" or "असल में" tone, no list-reading. Every line must map to one visual technique (anchor word, flip year, cork board, HUD, window, ribbon).
Score before recording (each item 0–2): hook clear in 3 s / paradox / vivid detail / turn / payoff irony / every line visual. Record only at 10/12 or more.

## The 5-second hold system (26 Nov 2026 research: Kallaway, Jenny Hoyos, Paddy Galloway, retention-curve data)
Data: 30-50% of viewers leave in seconds 0-3, another 15-25% in seconds 3-10 if the hook does not start paying off. Viewed-vs-swiped under 60% = dead; 70-90% = winners. Hoyos: "you have one second". Kallaway: speed-to-value is about 4 s in short form.
Second-by-second:
- 0.0-1.0 s FIRST FRAME = THUMBNAIL: subject already on screen, already moving (mid-action, never an establishing shot or logo), 3-5 word text that names the topic. Sound starts on frame 1.
- 0-2 s CONTEXT: the topic in the first 2-3 spoken words, something every viewer has personally seen ("रसोई गैस की ये बदबू").
- 2-3.5 s LEAN: a shock that flips what they believe ("असली नहीं है").
- 3.5-6 s SNAPBACK WITH STAKES: the "why should I care", a concrete, heavy consequence, not a vague tease ("एक बार ये बदबू नहीं थी… और पूरा स्कूल उड़ गया").
- Two "dopamine hits" before second 6: each spoken turn gets a visual event (freeze, colour drop, hard flash).
Rules: the same message in voice + text + picture; staccato lines first (3-7 words); 5th-grade words; never repeat a fact in the hook; a visual change every 1.5-2 s; no intro/logo.
Body: but/therefore, never "and then"; the tip must call back to a detail of the story (the switch); loop ending that flows back into line 1.

## Editing language (26 Nov 2026, from owner's reference reels)
- Apple-style ad: calm voice, half the runtime is silence while pictures speak; one fixed word over a 0.5 s chronological montage; black cards with small centred text; ending mirrors the opening.
- Editorial creator reel: two-font system (heavy grotesk caps + elegant serif for the key word and captions); design-tool selection handles around a key word; big numerals on a blurred background, then focus pulls back; one signature colour set; physical props/hands instead of flat graphics.
- Founder reel: B&W with chromatic edges + fine screen texture; small red labels ending in "//".
- Our engine (tools/cine.py): AI depth map per photo -> 3D camera move + rack focus, bloom, haze shimmer, archive film, dust bokeh, split-tone grade.

## Script logic shared by every reference (26 Nov 2026)
1. First line = a promise (what you will get / what you believe is wrong).
2. Open a loop early, close it at the very end (the ending mirrors the opening).
3. Hard specifics: numbers, names, dates, exact times.
4. The narrator has a point of view: one honest human line (an opinion or a feeling) right after the hardest fact. This is what makes people connect.
5. A turn just before the payoff ("But…", "Until now.").
6. End on the closed loop; any action goes in the caption, not the voice.

## Voice (measured 26 Nov 2026)
- Doc-reel references: one continuous, conversational storyteller at ~3.1-3.3 words/s with almost no pauses (0-5 pauses over 0.4 s, none over 0.8 s) and a music bed under everything. The emotion comes from the words, the music and the cuts, not from voice acting.
- Our tag-directed takes ([whispers]/[sad]/[long pause]) had ~30% dead air and theatrical swings = sounds like an AI actor. Rule: no emotion tags in story shorts; write the emotion into the words and punctuation; let the music carry silence.
- Voice: a documentary narrator voice (Aditya 2.0, KgnO7XaC644NBfmLZmwn) instead of an ad voice. Most human option: owner records the script on his phone, ElevenLabs Voice Changer converts it (keeps his real timing and emotion).
- Apple-style pauses only for brand-film formats, never for story shorts.

## Script system v4 — owner notes 27 Nov 2026 (Copy Posse 'Quips/Tips/Clips' + owner's 6-step framework)
- Step 0 PACKAGING before any script: pick the idea by human psychology, write the TITLE and the COVER/THUMBNAIL line first; the hook = the cover text.
- Step 1 ASSURITY: the intro must pay a REWARD in 3-6 s (the shocking fact itself, not a tease), then open a curiosity gap with a question or a fear.
- Step 2 RESEARCH: watch ~10 videos on ONE topic (not 10 topics) before writing; note how big creators open, turn and close it.
- Step 3 MASTER SCRIPT: build our own pattern from those creators; body told as a short story.
- Step 5 CTA: one fixed signature line every time (brand repetition): "ऐसे ही रोज़ के सच के लिए FreshNestHub को फ़ॉलो करो।"
- Length discipline: ~75 words = 30 s, 150 words = 60 s; cut every word that isn't needed; too much content = split into two reels.
- Funnel mix: QUIPS (myth/stat, broad, for shares/follows) + TIPS (practical how-to, for saves) + CLIPS (personal/behind-the-scenes, for comments). We only made quips so far.
- Natural Hinglish over shuddh Hindi; short punchy sentences.
