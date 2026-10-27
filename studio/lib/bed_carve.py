"""Make room for the voice inside music+SFX: when the VO is talking, dip the bed's
presence band (1.2-5 kHz, where words live) and its hiss band (6-16 kHz, whooshes/cymbals)."""
import numpy as np
from scipy import signal
SR = 48000


def _env(x, ms):
    n = max(1, int(SR * ms / 1000)); return np.sqrt(np.convolve(x * x, np.ones(n) / n, "same") + 1e-18)


def _smooth(g, att, rel):
    D = 32; gd = g[::D]; od = np.empty_like(gd); y = 0.0
    a = np.exp(-D / (SR * att)); r = np.exp(-D / (SR * rel))
    for i, v in enumerate(gd):
        c = a if v > y else r; y = c * y + (1 - c) * v; od[i] = y
    return np.interp(np.arange(len(g)), np.arange(len(gd)) * D, od)


def carve(bed, vo, presence_db=7.0, hiss_db=8.0):
    """bed: (N,2) float, vo: (N,) float aligned. Returns carved bed."""
    e = _env(vo, 25); act = np.clip(e / (np.percentile(e[e > 1e-5], 90) + 1e-12) * 1.4, 0, 1)
    act = _smooth(act, 0.02, 0.25)
    taps = 1023; pad = np.zeros((taps // 2, bed.shape[1]))
    def band(lo, hi):
        h = signal.firwin(taps, [lo, hi], pass_zero=False, fs=SR)
        return signal.lfilter(h, 1, np.concatenate([bed, pad]), axis=0)[taps // 2:]
    pres = band(1200, 5000); hiss = band(6000, 16000)
    gp = 1 - (1 - 10 ** (-presence_db / 20)) * act; gh = 1 - (1 - 10 ** (-hiss_db / 20)) * act
    return bed + pres * (gp - 1)[:, None] + hiss * (gh - 1)[:, None]


# ---- word guard (R&D 27 Oct 2026, lab/sound/): SFX hits and loud music notes on top of words ----
def _phone(x, lo=300.0, hi=10000.0):
    return signal.sosfilt(signal.butter(4, [lo, hi], "band", fs=SR, output="sos"), x)


def _smooth_min(g, att_ms, rel_ms):
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    w = max(1, int(SR * att_ms / 1000)); r = max(1, int(SR * rel_ms / 1000))
    g1 = minimum_filter1d(g, size=2 * max(w, r) + 1)
    return uniform_filter1d(g1, size=2 * w + 1) if w > 1 else g1


def guard(bed, vo, ld=12.0, max_dip=10.0):
    """While the narrator talks, keep the bed (music + SFX) >= `ld` dB under the voice on a phone speaker (300 Hz-10 kHz),
    bed measured on 50 ms windows vs the voice's syllable level (300 ms); dips at most `max_dip` dB. bed (N,2), vo (N,).
    Lab (printer ink / gas station / Hoover): momentary LD p5 7.5-8.5 -> ~12 LU, phone ESTOI +0.01, gaps -0.7 LU."""
    from scipy.ndimage import uniform_filter1d
    env = lambda x, ms: np.sqrt(uniform_filter1d(x * x, max(1, int(SR * ms / 1000))) + 1e-20)
    ev = env(_phone(vo), 300); eb = env(_phone(bed.mean(1)), 50)
    act = ev > np.percentile(ev[ev > 1e-6], 50) * 0.1
    g = np.where(act, np.minimum(1.0, ev * 10 ** (-ld / 20) / (eb + 1e-12)), 1.0)
    g = _smooth_min(np.maximum(g, 10 ** (-max_dip / 20)), 8, 60)
    return bed * g[:, None]
