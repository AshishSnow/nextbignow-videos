# What-If v3 engine (NextBigNow, from episode 33)

Source for the v3 look: painted 3D mascot (`hero.py`, varsity outfit), cinematic sets and post (`cine.py`),
the episode engine with grade/bloom/grain and a crisp caption overlay (`engine3.py`), and episode 33's props,
render and audio scripts as a worked example. Rules and lessons: see `../PLAYBOOK.md`, section 5b.

Layout expected at run time (as in the scratch workspace): these files in `whatif/`, `gfx.py` in `qday/`,
`ed.py` in `mammoth/`, `align2.py` one level up, fonts (Anton, Montserrat, LilitaOne…) in `fonts/`, and the
Chatterbox Turbo voice in `tts2/`.

Pipeline: `paras.txt` → `make_vo4.py <dir> --tempo 0.92` → `align2.py vo16.wav script.txt align.json` →
`render_<ep>.py still/guide <t…>` checks → `audio_<ep>.py` → render two halves (`range f0 f1 out.mp4`) → concat + mux.
