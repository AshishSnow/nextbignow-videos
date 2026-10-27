"""Sound lab helpers (R&D 27 Oct 2026): phone-speaker simulation, speech-over-bed metrics, a word guard for the bed
and a true-peak pre-limiter so ffmpeg loudnorm can stay in linear mode."""
import numpy as np
from scipy import signal
from scipy.ndimage import minimum_filter1d, uniform_filter1d
SR = 48000


def phone(x, sr=SR, lo=300.0, hi=10000.0):
    """Crude smartphone loudspeaker: little below ~300 Hz, soft top end. Mono in, mono out."""
    sos = signal.butter(4, [lo, hi], "band", fs=sr, output="sos")
    return signal.sosfilt(sos, x)


def _env(x, ms, sr=SR):
    n = max(1, int(sr * ms / 1000)); return np.sqrt(uniform_filter1d(x * x, n) + 1e-20)


def smooth_min(g, att_ms, rel_ms, sr=SR):
    """Gain smoothing that never exceeds the raw gain: min-filter (look-ahead/behind) then average."""
    w = max(1, int(sr * att_ms / 1000)); r = max(1, int(sr * rel_ms / 1000))
    g1 = minimum_filter1d(g, size=2 * max(w, r) + 1)
    return uniform_filter1d(g1, size=2 * w + 1) if w > 1 else g1


def guard(bed, vo, ld=12.0, max_dip=18.0, sr=SR):
    """Word guard: while the narrator talks, keep the bed (music + SFX) at least `ld` dB under the voice
    in the phone band, measured on 50 ms windows against the voice's syllable level (300 ms). bed (N,2), vo (N,)."""
    pv = phone(vo, sr); pb = phone(bed.mean(1), sr)
    ev = _env(pv, 300, sr); eb = _env(pb, 50, sr)
    act = ev > (np.percentile(ev[ev > 1e-6], 50) * 0.1)          # voice present (within ~20 dB of its median)
    allow = ev * 10 ** (-ld / 20)
    g = np.where(act, np.minimum(1.0, allow / (eb + 1e-12)), 1.0)
    g = np.maximum(g, 10 ** (-max_dip / 20))                     # never dig more than max_dip dB
    g = smooth_min(g, 8, 60, sr)
    return bed * g[:, None], g


def true_peak_limit(x, ceiling_db, sr=SR):
    """Look-ahead limiter on 4x-oversampled peaks. x (N,2). Returns limited x (gain-only, no clipping)."""
    up = signal.resample_poly(x, 4, 1, axis=0)
    pk = np.abs(up).max(1).reshape(-1, 4).max(1)[: len(x)]
    if len(pk) < len(x): pk = np.pad(pk, (0, len(x) - len(pk)))
    c = 10 ** (ceiling_db / 20)
    g = np.minimum(1.0, c / (pk + 1e-12))
    g = smooth_min(g, 2, 40, sr)
    return x * g[:, None], g
