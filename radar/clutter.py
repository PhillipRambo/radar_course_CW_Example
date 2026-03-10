import numpy as np
from .dsp import get_decimated_signal, compute_spectrum_db

def measure_background(sdr, frames, decim, n_fft, lpf, window):
    background = np.zeros(n_fft, dtype=np.float64)

    for k in range(frames):
        rx = sdr.rx()
        x = get_decimated_signal(rx, decim, n_fft, lpf)
        background += compute_spectrum_db(x, window)
        print(f"Background frame {k+1}/{frames}")

    return background / frames