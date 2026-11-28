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

## Learned from ghost-editor (MIT) + OpenMontage — 27 Nov 2026
- Caption News grammar fits our petrol style: captions slam in 2-3 chunks on the word onsets (scale 1.3 -> 1 in 0.13 s);
  ONE keyword per caption on a coloured block that wipes left->right in 0.12 s; first caption lands by frame 4 (0.13 s).
- Title sting -> channel bug: the title lands big once, then shrinks to a small corner bug for the rest of the reel.
- Evidence beat: when a source is named, show the real document tilted on a dark desk, a highlighter sweeps the words AS
  they are spoken, plus a 'SOURCE: ...' tag. No number on screen without its source.
- Colour has meaning: accent = the point, red = the bad thing, white = everything else, grey = labels.
- Sound only where something enters: hit on frame 4, a pop under every keyword wipe, paper/whoosh into cards, marker sound
  under each highlighter sweep, one soft boom under the verdict. CC0 kit copied to studio/sfxlib/ghost/.
- Short-form data (OpenMontage): visual change every 1-3 s; 16-30 s ~84 % completion vs 31-60 s ~68 %; 85 % watch muted ->
  every word must read without sound; universal safe zone 900x1400 centred; 1-2 font families max.
- Workflow: preview + approval sheet (frame at every beat) before the final render; log every owner correction as a taste rule.

## Human-sounding scripts and captions (from humanizer, MIT) + voice tooling (Handy) — 27 Nov 2026
Before sending any script, caption or description, strip AI tells:
- "Not X but Y" contrasts: keep one ONLY when X is a belief people really hold (the myth we bust: "आग फ़ोन से नहीं…
  कपड़ों से"). Never invent a fake X just for drama.
- No one-line closers that repeat the point, no staged candour ("सच कहूँ…", "Honestly?", "Here's the thing"), no
  run-ups ("चलो जानते हैं", "आज हम बात करेंगे"): start with the fact.
- No forced threes, no dashes (— –) in captions/descriptions: use comma, full stop or colon. Vary line openings.
- No inflated words (crucial, game-changer, shocking truth, "बहुत बड़ा राज़") or borrowed authority without a named source.
- Every line must add a new fact; if it only restates, cut it.
- Match the owner's own writing when he gives a sample.
Voice/timing tools: Handy = offline dictation (Whisper / Parakeet) with Silero VAD. Use Silero VAD to trim dead air
between voice lines (cap gaps ~0.45 s); keep Whisper for Hindi word timings (Parakeet is English/European only).
The owner can dictate his own read with Handy-style tools and we run it through the ElevenLabs Voice Changer for the
most human take.

## Topic + script system v5 (27 Nov 2026, everything the owner shared, combined)
TOPIC SCORE (0-2 each, publish only >= 11/14):
 1 In every Indian home / daily habit  2 Real surprise (most people believe the opposite)  3 Stakes/fear for family
 4 Action the viewer can take today  5 Share trigger ("send to the person who...")  6 Timely (season/news)
 7 Proof: a named study/hospital/regulator + one real case
HOOK SCORE (write 3 variants, 0-20 each, keep the best, >= 70/100): Clarity in 2 s, Emotion, Disruption (opening frame
 looks different from the feed), Stakes, Promise of a payoff. Reels favour a relatable pain point; Shorts favour a
 curiosity gap or bold claim. Pass the SILENT TEST: frame 0-3 s must work with sound off.
SCRIPT: hook -> reward (the shocking fact) by 3-6 s -> stacked open loops (close one, open the next: "aur ye toh
 aadha sach hai...") -> pattern interrupt every 2-3 s (visual change / one-word line) -> proof as a mini story ->
 tip -> last line points back to the hook (loop) -> fixed short CTA. Every line advances or raises a question.
 Payoff spread across the reel (a viewer leaving at 50 % still learned something). 75-90 words.
Then the humanizer pass (no fake contrasts, no staged candour, no dashes, no hype words, no repeat closers).

## Motion system v6 (73-microwave, 2026-11-27)
- Hook = a visual reveal, not just a headline: start inside the object (extreme close-up), pull back to show it, then reveal the invisible danger (heat-vision scan line over the microwave window).
- Camera on every scene: slow 5% push-in; screen shake + zoom punch + 1-frame chromatic split on every impact word.
- No hard cuts: alternate whip-pan (motion blur) and zoom punch-through transitions, 0.15 s each side; a white flash into the brand card.
- Show, don't tell: particles fly TOWARD the camera (3D depth), dive into the plastic wall before the 1 cm square, microscope eyepiece for lab results with cells shrinking and dying (not X marks).
- Particles and props draw UNDER headlines; never cover the key words.
- Code: episodes/73-microwave-plastic/_mw2.py (camera(), transition(), frame() override after the tail, before __main__).
- v7 real-image rule: Pexels/Pixabay/Unsplash are blocked here; Wikimedia Commons works (wmget.py, 20 s spacing on 429). Use a real photo plate for the hook (full-bleed blurred copy + purple grade behind a framed sharp copy), rembg cutouts of real objects, real microscope images for lab results (HEK 293 = kidney cells). Glass cuts out badly with rembg, so use it as a framed photo card.

## Script lessons from reference reel 1000216625 (dandruff, 60 s, 28 Nov 2026)
Script map: 0-4 s "अभी सिर में खुजली करो, नाखूनों में फँसा सफ़ेद डैंड्रफ देखो" (do-it-now hook) -> 4-6 s disgust threat ("अगली बार सौ बार सोचना")
-> 6-12 s myth flip ("सूखी चमड़ी नहीं, करोड़ों फंगस का कचरा") -> 12-16 s open loop ("महँगे शैम्पू के बाद भी जाता क्यों नहीं?")
-> 16-18 s blame twist ("क्योंकि तुम खुद इन्हें दावत दे रहे हो") -> 18-45 s named villain with a personality (Malassezia: "आज तो फ्री पार्टी")
explained as a cause chain (oil -> fungus eats -> acid -> irritation -> skin made too fast -> flakes) -> 45-50 s callback punchline
("तेल लगाकर भगा नहीं रहे, दावत दे रहे हो") -> 50-60 s part-2 cliffhanger follow + identity share ("उस दोस्त को भेजो जो सिर को तेल की टंकी बना लेता है") + comment question.
Rules taken:
1. Participation hook: make the viewer DO something with their body or the object in hand right now (check, touch, look).
2. Myth flip within 12 s; then blame the viewer's own everyday habit (the cultural one: champi, tiffin, chai).
3. Give the villain a name and a voice; one funny line from it. Explain HOW as a 4-6 step cause chain, one visual per link.
4. One sticky word introduced early and paid back in the punchline (दावत).
5. CTA = withhold the fix for part 2 ("सॉल्यूशन अगली वीडियो में") + identity-tagged share + yes/no comment question.
6. Tone: तुम, slang (दबा के, बेटा), short lines; zero report language (no university names in the first 15 s).
Visual: one recurring character in a home set, cute personified villains in a "micro world" set, metaphor machines (body = factory).

## FNH Paper look v1 (adapted from the OopsMyBusiness paper system, 28 Nov 2026)
- Backgrounds: cream paper #F0E8D8 (fibres + soft vignette) alternating with deep series-colour paper (purple #5C2696 for interesting topics). Replaces gradients, sunbursts and black slides.
- Headlines: flat, no 3D, centred, Teko 700 (condensed Devanagari, the Hindi stand-in for Archivo Condensed Black). Cream: ink #1E102C + key word red #E8463C; colour paper: cream text + key word yellow #FFD65C; red block only for the shock word.
- Subtitles: small Tiro Devanagari, sheared to italic, ink/cream with the current word in red/yellow, no pill. Strip ? and , (Tiro has no Latin glyphs).
- Cut-outs get a white die-cut sticker edge + soft shadow; photos as tilted white-border cards. Notes turn red on cream.
- Header: brand pill "FRESHNESTHUB" (Archivo 900, white on series colour) top-left at y~316 + round black logo badge top-right (x 900). Film grain on every frame.
- Code: episodes/74-tiffin-plastic/_paper.py (append last before __main__).
- Paper look v2 (28 Nov, from OopsMyBusiness "FAKE SHOPPERS" frames): headlines in Noto Sans Devanagari 900 with roughened "shady" edges that re-draw 8x/s (line boil) + stepped stop-motion jiggle and a pop-in; key words on tilted yellow/white sticker cards; dark offset shadow only on colour paper (none on cream);
  design-tool dashed selection box with corner handles around the punchline; vintage film cards (thick white border + black film edge + warm grade); every card/cut-out wobbles in 8 fps steps; series pill "रोज़ का सच N° xx" with a progress underline that fills across the video. Code: _paper2.py (append after _paper.py).
- 28 Nov: owner rejected the rough/boiling Noto font and the "रोज़ का सच" pill. Owner picked **Modak** (d_modak.ttf) for FNH headlines: clean (no roughening), hard offset shadow (dark on colour paper, light beige on cream, none inside sticker cards), key words on yellow sticker cards, stepped jiggle + pop kept. Header = only the round logo badge (no pill, no progress bar).
- 28 Nov (v4): first frame on colour paper (purple), never cream. Modak needs only a THIN ink outline (3 px; thick outlines close the counters and the owner could not read it) + hard dark shadow; on cream fill with the series colour, not ink. Intro 0-2 s = photo burst: 5 real photo prints slam in ~0.37 s apart, each with a shutter click (click2 + click4) and a 1-frame flash, then the hero cut-out slams on top. Code: _paper3.py.
