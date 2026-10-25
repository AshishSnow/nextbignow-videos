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
