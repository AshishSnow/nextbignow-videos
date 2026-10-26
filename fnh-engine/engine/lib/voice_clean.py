"""Clean-voice chain v2 for ElevenLabs takes.
Usage: voice_clean.py in.(mp3|wav) out.wav [tempo]
  1. decode 48 kHz mono float
  2. optional time-stretch with Rubber Band R3 (pedalboard, formant-preserving) instead of ffmpeg R2
  3. high-pass 80 Hz, small mud cut
  4. gentle RMS compressor (before de-ess so it can't push S back up)
  5. split-band de-esser (4.2-11 kHz) that only touches loud S / SH / T sounds
  6. MP3-artifact cleanup: soft shelf above 9 kHz + low-pass 15.5 kHz
  7. downward expander in the gaps (breaths, hiss, codec noise -> clean silence)
  8. peak -1 dBFS
"""
import sys, subprocess, numpy as np, soundfile as sf
from scipy import signal

SR = 48000


def load(p):
    tmp = "/tmp/_vc_in.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-ac", "1", "-ar", str(SR), "-c:a", "pcm_f32le", tmp], check=True)
    return sf.read(tmp, dtype="float32")[0].astype(np.float64)


def env_rms(x, ms):
    n = max(1, int(SR * ms / 1000))
    return np.sqrt(np.convolve(x * x, np.ones(n) / n, "same") + 1e-18)


def smooth_gain(g, att_ms, rel_ms):
    """one-pole smoothing: fast when gain drops (attack), slow when it recovers (release)."""
    a = np.exp(-1 / (SR * att_ms / 1000)); r = np.exp(-1 / (SR * rel_ms / 1000))
    out = np.empty_like(g); y = 1.0
    # vectorised enough for a 60 s VO (2.9 M samples) via block loop on decimated control signal
    D = 16; gd = g[::D]; od = np.empty_like(gd)
    a = a ** D; r = r ** D
    for i, v in enumerate(gd):
        c = a if v < y else r
        y = c * y + (1 - c) * v; od[i] = y
    out = np.interp(np.arange(len(g)), np.arange(len(gd)) * D, od)
    return out


def peq(f0, gain_db, q):
    A = 10 ** (gain_db / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w), 1 - al * A]; a = [1 + al / A, -2 * np.cos(w), 1 - al / A]
    return signal.tf2sos(np.array(b) / a[0], np.array(a) / a[0])


def shelf_hi(f0, gain_db):
    A = 10 ** (gain_db / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / 2 * np.sqrt(2)
    c = np.cos(w)
    b = [A * ((A + 1) + (A - 1) * c + 2 * np.sqrt(A) * al), -2 * A * ((A - 1) + (A + 1) * c), A * ((A + 1) + (A - 1) * c - 2 * np.sqrt(A) * al)]
    a = [(A + 1) - (A - 1) * c + 2 * np.sqrt(A) * al, 2 * ((A - 1) - (A + 1) * c), (A + 1) - (A - 1) * c - 2 * np.sqrt(A) * al]
    return signal.tf2sos(np.array(b) / a[0], np.array(a) / a[0])


def clean(x, tempo=1.0, deess_target=-11.0, verbose=True):
    if abs(tempo - 1) > 1e-3:
        import pedalboard
        x = pedalboard.time_stretch(x.astype(np.float32)[None, :], SR, stretch_factor=tempo, high_quality=True,
                                    transient_mode="mixed", preserve_formants=True)[0].astype(np.float64)
    # 3. tone
    x = signal.sosfilt(signal.butter(2, 80, "high", fs=SR, output="sos"), x)
    x = signal.sosfilt(peq(320, -1.5, 1.0), x)
    # 4. compressor (RMS 20 ms, thr = vowel level -8 dB, 2.2:1)
    e = env_rms(x, 20); thr = np.median(e[e > np.percentile(e, 70)]) * 10 ** (-8 / 20)
    gc = np.where(e > thr, (e / thr) ** (1 / 2.2 - 1), 1.0)
    x = x * smooth_gain(gc, 8, 140)
    # 5. split-band de-esser (linear-phase band so low + band sums back perfectly)
    taps = 511
    bp = signal.firwin(taps, [4200, 11000], pass_zero=False, fs=SR)
    xd = np.concatenate([x, np.zeros(taps // 2)])
    band = signal.lfilter(bp, 1, xd)[taps // 2:]
    rest = x - band
    eb = env_rms(band, 3); ef = env_rms(x, 12)
    vowel_lvl = np.median(ef[ef > np.percentile(ef, 70)])
    limit = vowel_lvl * 10 ** (deess_target / 20)            # S energy allowed up to this level
    over = np.maximum(eb / limit, 1.0)
    g = over ** (-0.75)                                         # ratio 4:1 above the limit
    g = np.maximum(g, 10 ** (-12 / 20))                         # never more than -12 dB
    g = smooth_gain(g, 0.8, 35)
    x = rest + band * g
    if verbose:
        print(f"  de-ess: max reduction {20*np.log10(g.min()):.1f} dB, active {(g < 0.89).mean()*100:.1f}% of time")
    # 6. codec cleanup + adaptive tilt: bright/fizzy voices get their 7 kHz+ sheen pulled toward a natural level
    f_, t_, Z = signal.stft(x, SR, nperseg=2048, noverlap=1568); P = np.abs(Z) ** 2
    lo = P[(f_ >= 100) & (f_ < 1000)].sum(0) + 1e-20; hi = P[(f_ >= 7000) & (f_ < 12000)].sum(0) + 1e-20
    tot = 10 * np.log10(P.sum(0) + 1e-20); vo_ = (tot > np.percentile(tot, 95) - 18) & (lo / (P.sum(0) + 1e-20) > 0.5)
    fizz = 10 * np.log10(np.median(hi[vo_] / lo[vo_])) if vo_.any() else -36.0
    tilt = float(np.clip(-33.0 - fizz, -5.0, 0.0))
    if tilt < -0.2: x = signal.sosfilt(shelf_hi(6500, tilt), x)
    if verbose: print(f"  fizz {fizz:.1f} dB -> tilt {tilt:.1f} dB @6.5k")
    x = signal.sosfilt(shelf_hi(9500, -2.0), x)
    x = signal.sosfilt(signal.butter(4, 15500, "low", fs=SR, output="sos"), x)
    # 7. expander in gaps: below speech floor -> fade to -30 dB (with 15 ms look-ahead, 90 ms hold)
    e = env_rms(x, 10); pk = np.percentile(e, 95); fl = pk * 10 ** (-40 / 20)
    open_ = e > fl
    hold = int(0.09 * SR); look = int(0.015 * SR)
    o = np.convolve(open_.astype(float), np.ones(hold + look), "full")[look:look + len(x)] > 0
    ge = np.where(o, 1.0, 10 ** (-30 / 20))
    x = x * smooth_gain(ge, 3, 60)
    # 8. peak
    x = x / (np.abs(x).max() + 1e-9) * 10 ** (-1 / 20)
    return x.astype(np.float32)


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    tempo = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    y = clean(load(src), tempo)
    sf.write(dst, y, SR, subtype="FLOAT")
    print("wrote", dst, f"{len(y)/SR:.2f}s")
