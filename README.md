# CW Doppler Radar Example (PlutoSDR)

Small Python example showing how to measure speed using a **continuous wave (CW) Doppler radar** with a PlutoSDR.

The script transmits a carrier, receives the reflected signal, finds the Doppler frequency shift, and converts it to speed.

---

## Files

```
.
├── main.py                         # main program (runs the radar processing loop)
├── config.py                       # system configuration and parameters
├── calculations/
│   └── calculation_sheet.ipynb     # notes / calculations used for development
└── radar/
    ├── device.py                   # PlutoSDR setup and TX/RX control
    ├── dsp.py                      # signal processing (decimation, FFT, peak detection)
    ├── clutter.py                  # background spectrum measurement
    └── plotting.py                 # real-time plotting utilities
```

**main.py**  
Runs the radar loop: receive samples, compute Doppler spectrum, detect peak, show plots.

**config.py**  
Contains system parameters like frequency, gains, FFT size, etc.

**radar/device.py**  
Handles PlutoSDR setup and TX/RX control.

**radar/dsp.py**  
Signal processing utilities:
- decimation
- FFT
- Doppler axis
- peak detection

**radar/clutter.py**  
Measures a background spectrum so stationary clutter can be subtracted.

---

## Basic idea

A CW radar measures Doppler shift: fd = 2v /`λ`


where  
- `fd` = Doppler frequency  
- `v` = target velocity  
- `λ` = wavelength  

The FFT peak in the Doppler spectrum gives the velocity.

---

## Requirements

numpy
matplotlib
pyadi-iio


The program will:

1. Connect to the PlutoSDR  
2. Start transmitting a tone  
3. Measure background clutter  
4. Continuously estimate Doppler speed  

Press **Ctrl+C** to stop.

---

## Notes

- Only radial velocity is measured.
- Stationary reflections are suppressed using background subtraction.
- Doppler resolution depends on FFT size and decimation.

