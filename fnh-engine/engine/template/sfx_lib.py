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


def crt_off(level=-17, dur=0.5):
    n_ = int(dur * SR); tt_ = np.arange(n_) / SR
    fr = 1600 * np.exp(-tt_ / 0.12) + 60
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt_ / 0.2) + 0.3 * rng.standard_normal(n_) * np.exp(-tt_ / 0.05)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1).astype(np.float32)


def bubbles(t0, n_=7, level=-26):
    for i in range(n_): add(pop(level - (i % 3), 1300 + 220 * (i % 4)), t0 + i * 0.11 + 0.03 * (i % 2))


# ---- foley added by FreshNestHub ep 10 (sugar rush): vinyl record scratch, candy-wrapper crinkle, cartoon boing, key jingle, lock click ----
def rec_scratch(level=-16):
    """vinyl record scratch ('wikka'): two fast strokes = band-passed noise + a buzzy tone whose pitch follows the hand speed."""
    out = []
    for d, up in ((0.11, True), (0.16, False)):
        n_ = int(d * SR); t2 = np.arange(n_) / SR; k = t2 / d
        sp = np.sin(np.pi * k) if up else np.sin(np.pi * k) ** 0.7
        fr = 120 + 1400 * sp
        tone = signal.sawtooth(2 * np.pi * np.cumsum(fr) / SR) * 0.6
        noi = rng.standard_normal(n_)
        f_, t_, Z = signal.stft(noi, SR, nperseg=256)
        fc = 400 + 3000 * np.interp(t_ / d, k, sp)
        mask = np.exp(-0.5 * ((np.log2(np.maximum(f_, 20))[:, None] - np.log2(fc)[None]) / 0.6) ** 2)
        _, w_ = signal.istft(Z * mask, SR, nperseg=256); w_ = w_[:n_]
        x = (tone + 1.5 * w_ / (np.abs(w_).max() + 1e-9)) * sp
        out.append(x)
    x = np.concatenate(out); x = signal.sosfilt(signal.butter(2, [150, 6000], "band", fs=SR, output="sos"), x)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x * 0.9], 1)


def crinkle(level=-24, dur=0.45):
    """candy-wrapper crinkle: sparse bright crackles with a slow envelope."""
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_) * (rng.random(n_) < 0.02)
    x = signal.sosfilt(signal.butter(2, [2500, 11000], "band", fs=SR, output="sos"), x)
    x = signal.lfilter([1], [1, -0.6], x) * np.sin(np.pi * t2 / dur)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, np.roll(x, 90)], 1)


def boing(level=-20, f0=220, dur=0.5):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    fr = f0 * (1 + 0.35 * np.sin(2 * np.pi * 14 * t2) * np.exp(-t2 / 0.25)) * (1 + 0.6 * np.exp(-t2 / 0.03))
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.22) * np.minimum(1, t2 / 0.003)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def jingle(level=-24):
    out = np.zeros((int(0.55 * SR), 2), np.float32)
    for j in range(5):
        y = ding(level - 4, 3200 + 500 * rng.random())[: int(0.25 * SR)] * np.exp(-np.arange(int(0.25 * SR)) / SR / 0.05)[:, None]
        i = int(j * 0.05 * SR); out[i:i + len(y)] += y
    return out


def lock_click(level=-15):
    out = np.zeros((int(0.12 * SR), 2), np.float32)
    for k, (d0, f0) in enumerate(((0.0, 3200), (0.045, 2400))):
        n_ = int(0.05 * SR); t2 = np.arange(n_) / SR
        x = (np.sin(2 * np.pi * f0 * t2) + 0.6 * signal.sosfilt(signal.butter(2, [1500, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_))) * np.exp(-t2 / 0.006)
        i = int(d0 * SR); out[i:i + n_] += np.stack([x, x], 1)
    return out / np.abs(out).max() * db(level)

# ---- ep 11 foley: ice_crack (freeze-over), sip (slurp), chatter (teeth), wind (cold gust) ----
def ice_crack(level=-16, dur=0.6):
    """freeze-over: dense bright crackles that thin out + a low 'crunch' body (ice forming fast)."""
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    dens = 0.08 * np.exp(-t2 / 0.18) + 0.004
    x = rng.standard_normal(n_) * (rng.random(n_) < dens)
    x = signal.lfilter([1], [1, -0.85], x)
    hi = signal.sosfilt(signal.butter(2, [1800, 12000], "band", fs=SR, output="sos"), x)
    lo = signal.sosfilt(signal.butter(2, [120, 900], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.exp(-t2 / 0.06)
    y = hi / (np.abs(hi).max() + 1e-9) + 0.6 * lo / (np.abs(lo).max() + 1e-9)
    y = y / np.abs(y).max() * db(level); return np.stack([y, np.roll(y, 70)], 1)


def sip(level=-24, dur=0.35):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_); fc = 900 + 1600 * t2 / dur
    y = np.zeros(n_)
    for i in range(0, n_, 512):
        sos = signal.butter(2, [fc[i] * 0.7, fc[i] * 1.3], "band", fs=SR, output="sos"); y[i:i + 512] = signal.sosfilt(sos, x[i:i + 512])
    y *= np.sin(np.pi * t2 / dur) ** 0.6 * (0.6 + 0.4 * np.sin(2 * np.pi * 18 * t2))
    y = y / (np.abs(y).max() + 1e-9) * db(level); return np.stack([y, y], 1)


def chatter(level=-26, dur=0.6, rate=16):
    out = np.zeros(int(dur * SR))
    for j in range(int(dur * rate)):
        c = pop(level, 2200 + 300 * rng.random())[:, 0][: int(0.03 * SR)] * np.exp(-np.arange(int(0.03 * SR)) / SR / 0.006)
        i = int(j / rate * SR); out[i:i + len(c)] += c[: len(out) - i]
    return np.stack([out, out], 1)


def wind(level=-27, dur=1.2):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_); y = np.zeros(n_)
    fc = 600 + 500 * np.sin(np.pi * t2 / dur) + 200 * np.sin(2 * np.pi * 1.3 * t2)
    for i in range(0, n_, 1024):
        sos = signal.butter(2, [fc[i] * 0.8, fc[i] * 1.25], "band", fs=SR, output="sos"); y[i:i + 1024] = signal.sosfilt(sos, x[i:i + 1024])
    y *= np.sin(np.pi * t2 / dur) ** 1.2
    y = y / (np.abs(y).max() + 1e-9) * db(level); return np.stack([y, np.roll(y, 300)], 1)


# ---- ep 12 (silver leaf): metal strike, paper rustle, metal-detector beeps ----
def clang(level=-20, f0=1250, dur=0.5):
    """metal strike: a few inharmonic partials (bar/plate modes) with fast attack + a click of noise."""
    n_ = int(dur * SR); t2 = np.arange(n_) / SR; y = np.zeros(n_)
    for r, a, tau in ((1.0, 1.0, 0.18), (2.76, 0.6, 0.09), (5.4, 0.35, 0.05), (8.93, 0.2, 0.03)):
        y += a * np.sin(2 * np.pi * f0 * r * t2 + rng.uniform(0, 6)) * np.exp(-t2 / tau)
    y += 0.5 * signal.sosfilt(signal.butter(2, [2000, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.exp(-t2 / 0.004)
    y = y / np.abs(y).max() * db(level); return np.stack([y, np.roll(y, 40)], 1)


def rustle(level=-26, dur=0.5):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_) * (0.4 + 0.6 * (rng.random(n_) < 0.08))
    y = signal.sosfilt(signal.butter(2, [1500, 7000], "band", fs=SR, output="sos"), x) * np.sin(np.pi * t2 / dur) ** 0.7
    y = y / (np.abs(y).max() + 1e-9) * db(level); return np.stack([y, np.roll(y, 120)], 1)


def det_beep(t0, t1, level=-25, f0=1900):
    """metal detector: beeps that get faster and higher until t1."""
    tt = t0; k = 0
    while tt < t1:
        q = clamp((tt - t0) / max(0.1, t1 - t0)); add(beep(level, f0 + 700 * q, 0.06), tt); tt += 0.32 - 0.24 * q; k += 1



# ---- ep 13 foley: chop (knife through onion onto a board), hiss (gas), snip (scissors), plip (water drop), sizzle (frying pan), squirt (juice spray) ----
def _st(y, d=60): return np.stack([y, np.roll(y, d)], 1)


def chop(level=-20):
    """knife through an onion onto a board: wet crunch + a low wooden knock."""
    n_ = int(0.25 * SR); t2 = np.arange(n_) / SR
    cr = signal.sosfilt(signal.butter(2, [900, 6000], "band", fs=SR, output="sos"), rng.standard_normal(n_) * (rng.random(n_) < 0.3)) * np.exp(-t2 / 0.04)
    kn = np.sin(2 * np.pi * 180 * t2) * np.exp(-t2 / 0.05) + 0.5 * np.sin(2 * np.pi * 420 * t2) * np.exp(-t2 / 0.02)
    y = 0.7 * cr / (np.abs(cr).max() + 1e-9) + kn / np.abs(kn).max()
    return _st(y / np.abs(y).max() * db(level))


def hiss(level=-24, dur=0.8):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    y = signal.sosfilt(signal.butter(2, [2500, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.sin(np.pi * t2 / dur) ** 0.6
    return _st(y / np.abs(y).max() * db(level), 200)


def snip(level=-20):
    out = np.zeros(int(0.2 * SR))
    for k, f0 in ((0, 3800), (int(0.07 * SR), 4300)):
        t2 = np.arange(int(0.05 * SR)) / SR; y = np.sin(2 * np.pi * f0 * t2) * np.exp(-t2 / 0.008) + 0.4 * rng.standard_normal(len(t2)) * np.exp(-t2 / 0.003)
        out[k:k + len(y)] += y
    return _st(out / np.abs(out).max() * db(level))


def plip(level=-24, f0=900):
    t2 = np.arange(int(0.12 * SR)) / SR; f = f0 + 1400 * np.exp(-t2 / 0.02)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t2 / 0.03)
    return _st(y / np.abs(y).max() * db(level))


def sizzle(level=-26, dur=2.0):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    y = signal.sosfilt(signal.butter(2, [3000, 11000], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * 0.4
    cr = (rng.random(n_) < 0.0015) * rng.uniform(-1, 1, n_); y += signal.sosfilt(signal.butter(2, 2000, "high", fs=SR, output="sos"), cr) * 3
    y *= np.minimum(1, np.minimum(t2 / 0.2, (dur - t2) / 0.3))
    return _st(y / np.abs(y).max() * db(level), 300)


def squirt(level=-24, dur=0.35):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    y = signal.sosfilt(signal.butter(2, [600, 4000], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.exp(-t2 / 0.08)
    return _st(y / np.abs(y).max() * db(level), 90)
