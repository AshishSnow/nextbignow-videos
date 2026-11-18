# Car dealer money (18 Nov 2026): NEON STORY look (first one)
Owner moved off black + yellow ("think out of the box", reference: detailed illustrated cartoon room, moody neon purple + warm lamp,
a character with a feeling, one story prop). Everything is drawn in code (neon.py kit): round-head characters (orange hero, blue salesman/
mechanic, green finance manager), sweat drops, blinking, neon signs that flicker; text lives IN the world (neon signs, screens, sticky notes).
render_neon.py: 10 scenes, whip transitions, camera push/drift, shake on reveals; one pass writes the IG and YT cuts (YT = frame x0.85 into the
safe box over a blurred copy, subs y 1320). Subtitles: small dark glass pill, active word neon pink. mix_sfx.py: Kenney CC0 + synth SFX, ducked, no music.
YT version: thumbnail (thumb.py) on the first 0.27 s (owner 18 Nov: Shorts has no custom thumbnail upload).
Final encode: 2-pass 9 Mb/s (raw CRF16 render is ~300 MB because of grain).
Voice: work/takes.sh (CBV=usa_narr make_vo x2) -> comp_takes n1 -> trim_gaps -> convert work/align.json to [[tok,start,end]] in comic/cd/align.json.

18 Nov 20:00: owner found the dark neon night look boring -> DAY COMIC grade (his reference: bright blue sky, turquoise, white highlights, sparkles, bold outlines, comic panel border). neon.py/render_neon.py are now the day look; *_night.py keep the old one. Saturation x1.25, contrast x1.06 on every frame, no grain, light vignette.
