# exec'd inside a project's mix.py right after `mix = VO + bed` (lab only). Env: GUARD (dB, 0 = off), PRELIM (1 = true-peak
# pre-limit so loudnorm stays linear), TAG (stem names). Saves work/stem_vo_<TAG>.wav, work/stem_bed_<TAG>.wav.
import os as _os, sys as _sys
_sys.path.insert(0, "/home/claude/nextbignow-videos/studio/lab/sound"); import soundlab as _sl
_tag = _os.environ.get("TAG", "A"); _gd = float(_os.environ.get("GUARD", "0"))
if _gd > 0:
    bed, _g = _sl.guard(bed, vo, ld=_gd, max_dip=float(_os.environ.get('GMAX', '18')))
    print(f"guard {_gd} dB: bed dipped >1 dB on {100*np.mean(_g < 0.89):.1f}% of samples, max dip {-20*np.log10(_g.min()):.1f} dB")
mix = VO + bed
if _os.environ.get("PRELIM") == "1":
    _tgt = float(_os.environ.get("TGT", "-11")); _tp = float(_os.environ.get("TPT", "-1.5"))
    _r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", "48000", "-ac", "2", "-i", "-", "-af", "ebur128=peak=true", "-f", "null", "-"],
                        input=mix.astype(np.float32).tobytes(), capture_output=True)
    _t = _r.stderr.decode(); _I = float(_t.split("I:")[-1].split("LUFS")[0]); _pk = float(_t.split("Peak:")[-1].split("dBFS")[0])
    _ceil = _tp - (_tgt - _I) - 0.3
    if _pk > _ceil:
        mix, _lg = _sl.true_peak_limit(mix, _ceil)
        print(f"prelimit: I {_I:.1f} TP {_pk:.1f} -> ceiling {_ceil:.1f} dBTP, max GR {-20*np.log10(_lg.min()):.1f} dB on {100*np.mean(_lg<0.99):.2f}% of samples")
sf.write(f"{B}/work/stem_vo_{_tag}.wav", vo, SR, subtype="FLOAT"); sf.write(f"{B}/work/stem_bed_{_tag}.wav", bed, SR, subtype="FLOAT")
