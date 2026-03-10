import numpy as np
import matplotlib.pyplot as plt

def create_plots(n_fft, fs_doppler, freq, mask):
    t = np.arange(n_fft) / fs_doppler

    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    line_i, = ax1.plot(t, np.zeros(n_fft), label="I")
    line_q, = ax1.plot(t, np.zeros(n_fft), label="Q")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Amplitude")
    ax1.set_title("Received baseband after decimation")
    ax1.grid(True)
    ax1.legend()

    line_fft, = ax2.plot(freq[mask], np.zeros(np.sum(mask)))
    ax2.set_xlabel("Doppler frequency [Hz]")
    ax2.set_ylabel("Magnitude [dB]")
    ax2.set_title("CW Doppler spectrum")
    ax2.grid(True)

    text_box = ax2.text(
        0.02, 0.98, "",
        transform=ax2.transAxes,
        va="top",
        ha="left",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85)
    )

    return fig, ax1, ax2, line_i, line_q, line_fft, text_box