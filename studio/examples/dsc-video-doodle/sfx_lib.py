sfx = np.zeros((NS, 2), np.float32)


def add(x, t, gain=1.0):
    i = int(t * SR)
    if i < 0: x = x[-i:]; i = 0
    j = min(NS, i + len(x))
    if j > i: sfx[i:j] += x[: j - i] * gain


def whoosh(dur=0.5, peak=0.55, f_lo=300, f_hi=3800, level=-21):
    n = int(dur * SR); noise = rng.standard_normal(n).astype(np.float32)
    f, t2, Z = signal.stft(noise, SR, nperseg=1024); x = t2 / dur
    fc = np.where(x < peak, f_lo * (f_hi / f_lo) ** (x / peak), f_hi * (f_lo * 1.6 / f_hi) ** ((x - peak) / (1 - peak)))
    mask = np.exp(-0.5 * ((np.log2(np.maximum(f, 20))[:, None] - np.log2(fc)[None]) / 0.8) ** 2)
    _, w = signal.istft(Z * mask, SR, nperseg=1024); w = w[:n]; te = np.arange(n) / n
    w = w * np.where(te < peak, (te / peak) ** 2.5, np.exp(-(te - peak) / 0.12)); w = w / (np.abs(w).max() + 1e-9) * db(level)
    p = np.linspace(0, 1, n); return np.stack([w * (1 - 0.5 * p), w * (0.5 + 0.5 * p)], 1)


def boom(level=-14, tau=0.45):
    n = int(1.3 * SR); t2 = np.arange(n) / SR; fr = 32 + 80 * np.exp(-t2 / 0.06)
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / tau) * np.minimum(1, t2 / 0.003)
    cl = signal.sosfilt(signal.butter(2, 1800, "low", fs=SR, output="sos"), rng.standard_normal(n)) * np.exp(-t2 / 0.015)
    x = s + 0.3 * cl / np.abs(cl).max(); x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def click(level=-30):
    n = int(0.03 * SR); t2 = np.arange(n) / SR
    x = signal.sosfilt(signal.butter(2, [1500, 7000], "band", fs=SR, output="sos"), rng.standard_normal(n)) * np.exp(-t2 / 0.004)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x * 0.9], 1)


def pop(level=-26, f0=900):
    n = int(0.12 * SR); t2 = np.arange(n) / SR; fr = f0 * (1 + 1.2 * np.exp(-t2 / 0.012))
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.03) * np.minimum(1, t2 / 0.001)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def ding(level=-26, f0=1318.5):
    n = int(1.2 * SR); t2 = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f0 * r * t2) * np.exp(-t2 / d) for r, a, d in ((1, 1, 0.5), (2.0, 0.35, 0.25), (2.76, 0.2, 0.15)))
    x *= np.minimum(1, t2 / 0.002); x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def scratch(level=-24, dur=0.32):
    n = int(dur * SR); t2 = np.arange(n) / SR
    x = signal.sosfilt(signal.butter(2, [800, 5000], "band", fs=SR, output="sos"), rng.standard_normal(n))
    x *= (0.6 + 0.4 * np.sin(2 * np.pi * 38 * t2)) * np.minimum(1, t2 / 0.01) * np.exp(-t2 / 0.2)
    x = x / np.abs(x).max() * db(level); return np.stack([x * 0.8, x], 1)





def card_in(t, lv=-27):
    add(whoosh(0.35, level=lv, f_lo=700, f_hi=5200), t - 0.22); add(pop(lv + 2, 900), t + 0.05)


def swish(t, lv=-26):  # highlighter swipe
    add(whoosh(0.3, peak=0.4, f_lo=1500, f_hi=7000, level=lv), t - 0.12)


def glitch(t, lv=-23):
    add(scratch(lv, 0.22), t - 0.08)
    for i in range(4): add(click(lv - 6), t - 0.08 + i * 0.045)


def doorbell(level=-17):
    out = []
    for f0, dur in ((659.25, 0.55), (523.25, 1.1)):
        n_ = int(dur * SR); t2 = np.arange(n_) / SR
        x = sum(a * np.sin(2 * np.pi * f0 * r * t2) * np.exp(-t2 / dd) for r, a, dd in ((1, 1, 0.6), (2.0, 0.25, 0.3), (3.0, 0.1, 0.15)))
        out.append(x * np.minimum(1, t2 / 0.003))
    x = np.concatenate(out); x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def buzzer(level=-19, dur=0.55):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = signal.square(2 * np.pi * 118 * t2) * 0.6 + signal.square(2 * np.pi * 121 * t2) * 0.4
    x = signal.sosfilt(signal.butter(2, 2500, "low", fs=SR, output="sos"), x) * np.minimum(1, t2 / 0.01) * np.minimum(1, (dur - t2) / 0.05)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def chaching(level=-18):
    a_ = ding(level, 2093)[: int(0.5 * SR)]; b_ = ding(level + 1, 2637)
    out = np.zeros((int(0.12 * SR) + len(b_), 2), np.float32); out[: len(a_)] += a_; out[int(0.12 * SR):] += b_
    nz = signal.sosfilt(signal.butter(2, [3000, 9000], "band", fs=SR, output="sos"), rng.standard_normal(int(0.25 * SR)))
    nz *= np.exp(-np.arange(len(nz)) / SR / 0.06); nz = nz / np.abs(nz).max() * db(level - 6)
    out[: len(nz)] += np.stack([nz, nz], 1); return out


def thud(level=-15):
    return boom(level, 0.18) + np.pad(click(level - 4), ((0, int(1.3 * SR) - int(0.03 * SR)), (0, 0)))


def beep(level=-22, f0=2900, dur=0.11):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = np.sin(2 * np.pi * f0 * t2) * np.minimum(1, t2 / 0.004) * np.minimum(1, (dur - t2) / 0.01)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def creak(level=-26, dur=0.5):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    fr = 180 + 60 * np.sin(2 * np.pi * 3 * t2)
    x = signal.sawtooth(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.25)
    x = signal.sosfilt(signal.butter(2, [400, 2500], "band", fs=SR, output="sos"), x)
    x = x / np.abs(x).max() * db(level); return np.stack([x * 0.8, x], 1)


def scratch_card(t0, dur, level=-22):
    n_ = int(dur * SR); tt_ = np.arange(n_) / SR
    x = signal.sosfilt(signal.butter(2, [1800, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_))
    x *= (0.45 + 0.55 * np.abs(np.sin(2 * np.pi * 9 * tt_))) * np.minimum(1, np.minimum(tt_, dur - tt_) / 0.03)
    add(np.stack([x, x * 0.9], 1).astype(np.float32) / np.abs(x).max() * db(level), t0)


def clink(t0, level=-24, f0=3300):
    add(ding(level, f0)[: int(0.25 * SR)], t0); add(ding(level - 4, f0 * 1.31)[: int(0.2 * SR)], t0 + 0.012)


def honk(level=-19, dur=0.42):
    n_ = int(dur * SR); tt_ = np.arange(n_) / SR
    x = signal.square(2 * np.pi * 349 * tt_) * 0.5 + signal.square(2 * np.pi * 440 * tt_) * 0.5
    x = signal.sosfilt(signal.butter(2, 2200, "low", fs=SR, output="sos"), x) * np.minimum(1, tt_ / 0.01) * np.minimum(1, (dur - tt_) / 0.04)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1).astype(np.float32)


def sizzle(dur=1.2, level=-32):
    """griddle: band-limited noise with random crackle (HOW TO START EP 3)"""
    n_ = int(dur * SR); x = signal.sosfilt(signal.butter(2, [2500, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_))
    cr = (rng.random(n_) > 0.9994).astype(np.float32); cr = signal.sosfilt(signal.butter(2, 3000, "high", fs=SR, output="sos"), cr) * 6
    te = np.arange(n_) / n_; x = (x + cr) * np.minimum(1, te / 0.1) * np.minimum(1, (1 - te) / 0.25); x = x / (np.abs(x).max() + 1e-9) * db(level)
    return np.stack([x, x], 1).astype(np.float32)


def hose(dur=1.0, level=-30):
    """water spray: bright steady noise"""
    n_ = int(dur * SR); x = signal.sosfilt(signal.butter(2, [1200, 7000], "band", fs=SR, output="sos"), rng.standard_normal(n_))
    te = np.arange(n_) / n_; x = x * (0.8 + 0.2 * np.sin(te * 40)) * np.minimum(1, te / 0.06) * np.minimum(1, (1 - te) / 0.12); x = x / (np.abs(x).max() + 1e-9) * db(level)
    return np.stack([x, x], 1).astype(np.float32)


def rattle(dur=0.9, level=-26, rate=16.0):
    """roll-up door / shutter: a fast train of metal clicks"""
    n_ = int(dur * SR); x = np.zeros(n_, np.float32); c = int(0.012 * SR); k_ = np.exp(-np.arange(c) / (0.003 * SR)) * rng.standard_normal(c)
    for i in range(int(dur * rate)):
        a = int(i / rate * SR)
        if a + c < n_: x[a:a + c] += (k_ * (0.7 + 0.3 * rng.random())).astype(np.float32)
    x = signal.sosfilt(signal.butter(2, 600, "high", fs=SR, output="sos"), x); x = x / (np.abs(x).max() + 1e-9) * db(level)
    return np.stack([x, x], 1).astype(np.float32)


def crt_off(level=-17, dur=0.5):
    n_ = int(dur * SR); tt_ = np.arange(n_) / SR
    fr = 1600 * np.exp(-tt_ / 0.12) + 60
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt_ / 0.2) + 0.3 * rng.standard_normal(n_) * np.exp(-tt_ / 0.05)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1).astype(np.float32)


def bubbles(t0, n_=7, level=-26):
    for i in range(n_): add(pop(level - (i % 3), 1300 + 220 * (i % 4)), t0 + i * 0.11 + 0.03 * (i % 2))


# motor whirr (vacuum, drill, fan) + jet fly-by — added 28 Oct 2026 (Hoover video); stereo like the others
def whirr(dur=1.2, level=-28, f0=180.0):
    tt = np.arange(int(dur * SR)) / SR; env = np.clip(tt / 0.25, 0, 1) * np.clip((dur - tt) / 0.3, 0, 1)
    tone = sum(np.sin(2 * np.pi * f0 * h * tt * (1 + 0.04 * np.sin(2 * np.pi * 3 * tt))) / h for h in (1, 2, 3, 5))
    noise = signal.sosfilt(signal.butter(2, [600, 5000], "band", fs=SR, output="sos"), np.random.default_rng(3).standard_normal(len(tt)))
    x = (0.6 * tone / 2 + 0.4 * noise) * env; x = (x / (np.abs(x).max() + 1e-9) * db(level)).astype(np.float32); return np.stack([x, x], 1)


def jet(dur=2.2, level=-24):
    tt = np.arange(int(dur * SR)) / SR; env = np.exp(-((tt - dur * 0.55) / (dur * 0.28)) ** 2)
    nz = np.random.default_rng(9).standard_normal(len(tt))
    lo = signal.sosfilt(signal.butter(2, [200, 2400], "band", fs=SR, output="sos"), nz)
    x = lo * env; x = (x / (np.abs(x).max() + 1e-9) * db(level)).astype(np.float32); p = np.linspace(0, 1, len(x)); return np.stack([x * (1 - 0.6 * p), x * (0.4 + 0.6 * p)], 1)


def rotor(dur=1.5, level=-30, f0=210.0):
    """small quadcopter buzz: 4 detuned saw-ish rotors + band noise, slow flutter (drone episodes, 1 Nov 2026)"""
    n_ = int(dur * SR); t_ = np.arange(n_) / SR; x = np.zeros(n_, np.float32)
    for i, df in enumerate((0.0, 3.1, -2.4, 5.2)):
        ph = 2 * np.pi * (f0 + df) * t_; x += (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)).astype(np.float32)
    nz = signal.sosfilt(signal.butter(2, [800, 5000], "band", fs=SR, output="sos"), rng.standard_normal(n_)).astype(np.float32)
    x = x / (np.abs(x).max() + 1e-9) + 0.35 * nz / (np.abs(nz).max() + 1e-9)
    x *= (1 + 0.15 * np.sin(2 * np.pi * 7 * t_)).astype(np.float32)
    e = np.minimum(1, np.minimum(t_ / 0.15, (dur - t_) / 0.3)).clip(0, 1).astype(np.float32)
    x = x * e; x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * 10 ** (level / 20)
    return np.stack([x, x], 1)


def shutter(level=-22):
    """camera shutter: two quick filtered clicks"""
    n_ = int(0.09 * SR); a = rng.standard_normal(n_).astype(np.float32) * np.exp(-np.arange(n_) / (0.006 * SR)).astype(np.float32)
    a = signal.sosfilt(signal.butter(2, [1500, 7000], "band", fs=SR, output="sos"), a).astype(np.float32)
    x = np.zeros(int(0.14 * SR), np.float32); x[:n_] += a; x[int(0.05 * SR):int(0.05 * SR) + n_] += 0.7 * a
    x = x / (np.abs(x).max() + 1e-9) * 10 ** ((level + 8) / 20)
    return np.stack([x, x], 1)


def bell_shake(dur=0.6, level=-26):
    """sleigh-bell shake: fast noise grains in a high band"""
    n = int(dur * SR); x = np.zeros(n, np.float32); r = np.random.default_rng(int(dur * 1000) + 7)
    for q in np.arange(0, dur - 0.03, 0.055):
        a = int(q * SR); l = int(0.045 * SR); g = r.standard_normal(l) * np.exp(-np.arange(l) / (0.012 * SR)) * (0.6 + 0.4 * r.random())
        x[a:a + l] += g[: max(0, n - a)]
    x = signal.sosfilt(signal.butter(2, [4500, 11000], "band", fs=SR, output="sos"), x)
    x = x * (np.clip(np.arange(n) / (0.04 * SR), 0, 1) * np.clip((n - np.arange(n)) / (0.2 * SR), 0, 1))
    x = x / (np.abs(x).max() + 1e-9) * 10 ** (level / 20)
    return np.stack([x, x], 1).astype(np.float32)


def tape_zip(dur=1.5, level=-30):
    """tape measure pulled out: ratchet clicks that speed up over a soft whirr"""
    n = int(dur * SR); x = np.zeros(n, np.float32); tq = 0.0; gap = 0.06; r = np.random.default_rng(11)
    while tq < dur - 0.01:
        a = int(tq * SR); l = int(0.008 * SR); x[a:a + l] += (r.standard_normal(l) * np.exp(-np.arange(l) / (0.002 * SR)))[: max(0, n - a)]; tq += gap; gap = max(0.022, gap * 0.97)
    x = signal.sosfilt(signal.butter(2, [1200, 7000], "band", fs=SR, output="sos"), x)
    x = x / (np.abs(x).max() + 1e-9) * 10 ** (level / 20)
    return np.stack([x, x], 1).astype(np.float32)


def rewind(dur=0.42, level=-30):
    """cassette rewind chirp: rising warble, used on chapter whips (lo-fi episode, 6 Nov)"""
    n = int(dur * SR); t2 = np.arange(n) / SR; fr = 500 + 2600 * (t2 / dur) ** 1.6 + 240 * np.sin(2 * np.pi * 34 * t2)
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) + 0.35 * signal.sosfilt(signal.butter(2, [1500, 6000], "band", fs=SR, output="sos"), rng.standard_normal(n))
    x = x * np.sin(np.pi * t2 / dur) ** 0.7; x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x * 0.9, x], 1).astype(np.float32)


def hanger(level=-30, f0=2350.0):
    """wire hanger on a metal rail: two thin inharmonic clinks"""
    n = int(0.35 * SR); t2 = np.arange(n) / SR; x = np.zeros(n)
    for dt, a in ((0.0, 1.0), (0.055, 0.6)):
        i = int(dt * SR); tt = t2[: n - i]
        x[i:] += a * sum(w * np.sin(2 * np.pi * f0 * r * tt) * np.exp(-tt / d) for r, w, d in ((1, 1, 0.06), (1.47, 0.6, 0.04), (2.31, 0.4, 0.025)))
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x * 0.85], 1).astype(np.float32)


def stamp_hit(level=-20):
    """rubber stamp on paper: low thump + short paper slap"""
    n = int(0.22 * SR); t2 = np.arange(n) / SR
    lo = np.sin(2 * np.pi * np.cumsum(70 + 90 * np.exp(-t2 / 0.02)) / SR) * np.exp(-t2 / 0.05)
    hi = signal.sosfilt(signal.butter(2, [900, 5200], "band", fs=SR, output="sos"), rng.standard_normal(n)) * np.exp(-t2 / 0.012)
    x = lo + 0.5 * hi / (np.abs(hi).max() + 1e-9); x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1).astype(np.float32)
