# Pet Rock — OopsMyBusiness "vintage comic + current editorial" style (15 Nov 2026)
Owner's brief (copied from NextBigNow): cream newsprint + Ben-Day dots, sepia history / solid red question scenes, Luckiest Guy titles,
Special Elite tape captions, inked photo panels, bursts, mini stat cards, self-drawing charts, real Wikimedia Commons photos run through
comicfx.comicify (credits vertical on the left + in the description), small paper-strip subtitles (Inter, y≈1440, word highlight),
whip/zoom/wipe/flash transitions, shakes, NO music (light comic SFX), 1080x1920 30 fps, 1:30-2:00, cover = frame at 0.2 s.
Pipeline: studio voice (scripts/vo_lines.py -> make_vo usa_narr, 2 takes + comp) -> convert align to [[word,start,end]] (+ atempo 1.05)
-> pr/align.json, pr/script.txt, pr/vo.wav -> fetch.py (Commons API; use 1920px thumbs on upload.wikimedia.org, UA with contact URL,
slow pacing: API rate-limits hard) -> comicify -> render_pr.py still/guide checks -> audio_pr.py -> `render_pr.py range f0 f1 out` x2 -> concat + mux.
engine.py here has the NextBigNow watermark removed; audiokit.mixdown(music_lufs=None) = no music. Fonts: LuckiestGuy.ttf + SpecialElite.ttf in ../fonts.
