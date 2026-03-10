import numpy as np

def make_axes(fc, fs, decim, n_fft):
    c = 299_792_458.0
    lam = c / fc
    fs_doppler = fs / decim
    freq = np.fft.fftshift(np.fft.fftfreq(n_fft, d=1 / fs_doppler))
    speed_kmh = (freq * lam / 2.0) * 3.6
    return lam, fs_doppler, freq, speed_kmh

def make_lpf(decim):
    return np.ones(decim, dtype=np.float32) / decim

def get_decimated_signal(rx, decim, n_fft, lpf):
    if isinstance(rx, (list, tuple)):
        rx = rx[0]

    x = np.asarray(rx, dtype=np.complex64)
    x = x - np.mean(x)
    x = np.convolve(x, lpf, mode="same")
    x = x[::decim]

    if len(x) < n_fft:
        raise RuntimeError("Too few samples after decimation")

    x = x[:n_fft]
    x = x - np.mean(x)
    return x

def compute_spectrum_db(x, window):
    X = np.fft.fftshift(np.fft.fft(x * window))
    mag = np.abs(X)
    return 20 * np.log10(mag + 1e-12)

def detect_peak(spec_db, freq, speed_kmh, guard_hz, peak_above_noise_db):
    valid = np.abs(freq) > guard_hz

    peak_idx = np.argmax(spec_db[valid])
    peak_global = np.where(valid)[0][peak_idx]

    peak_db = spec_db[peak_global]
    noise_floor = np.median(spec_db[valid])

    if peak_db < noise_floor + peak_above_noise_db:
        return 0.0, 0.0, noise_floor, noise_floor

    fd = freq[peak_global]
    v_kmh = speed_kmh[peak_global]
    return fd, v_kmh, peak_db, noise_floor