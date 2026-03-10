import numpy as np
import config as cfg

from radar.device import setup_sdr, start_tx, stop_tx, flush_rx
from radar.dsp import make_axes, make_lpf, get_decimated_signal, compute_spectrum_db, detect_peak
from radar.clutter import measure_background
from radar.plotting import create_plots

def main():
    lam, fs_doppler, freq, speed_kmh = make_axes(cfg.FC, cfg.FS, cfg.DECIM, cfg.N_FFT)
    doppler_res = fs_doppler / cfg.N_FFT
    mask = np.abs(freq) <= cfg.PLOT_DOPPLER_HZ
    window = np.hanning(cfg.N_FFT)
    lpf = make_lpf(cfg.DECIM)

    print(f"Wavelength: {lam:.4f} m")
    print(f"Effective Doppler sample rate: {fs_doppler:.1f} Hz")
    print(f"Doppler resolution: {doppler_res:.2f} Hz")

    sdr = setup_sdr(cfg)
    start_tx(sdr, cfg)
    flush_rx(sdr, 3)

    print("Scanning stationary background...")
    background_spec_db = measure_background(
        sdr, cfg.BG_FRAMES, cfg.DECIM, cfg.N_FFT, lpf, window
    )

    fig, ax1, ax2, line_i, line_q, line_fft, text_box = create_plots(
        cfg.N_FFT, fs_doppler, freq, mask
    )

    display_spec_db = None

    try:
        while True:
            rx = sdr.rx()
            x = get_decimated_signal(rx, cfg.DECIM, cfg.N_FFT, lpf)
            mag_db = compute_spectrum_db(x, window)
            mag_db_clean = mag_db - background_spec_db

            if display_spec_db is None:
                display_spec_db = mag_db_clean.copy()
            else:
                a = cfg.SPECTRUM_SMOOTH_ALPHA
                display_spec_db = a * display_spec_db + (1 - a) * mag_db_clean

            fd, v_kmh, peak_db, noise_floor = detect_peak(
                display_spec_db,
                freq,
                speed_kmh,
                cfg.GUARD_HZ,
                cfg.PEAK_ABOVE_NOISE_DB,
            )

            i = np.real(x)
            q = np.imag(x)

            line_i.set_ydata(i)
            line_q.set_ydata(q)
            ax1.set_ylim(min(i.min(), q.min()) - 100, max(i.max(), q.max()) + 100)

            line_fft.set_ydata(display_spec_db[mask])
            ax2.set_ylim(display_spec_db[mask].min() - 3, display_spec_db[mask].max() + 3)

            if fd == 0:
                direction = "no reliable motion"
            else:
                direction = "approaching" if fd > 0 else "receding"

            text_box.set_text(
                f"Peak Doppler: {fd:+.1f} Hz\n"
                f"Speed: {v_kmh:+.2f} km/h\n"
                f"Direction: {direction}\n"
                f"Noise floor: {noise_floor:.1f} dB\n"
                f"Peak level: {peak_db:.1f} dB\n"
                f"Resolution: {doppler_res:.2f} Hz"
            )

            fig.canvas.draw()
            fig.canvas.flush_events()

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        stop_tx(sdr)

if __name__ == "__main__":
    main()