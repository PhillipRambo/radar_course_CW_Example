import time
import numpy as np
import adi

def setup_sdr(cfg):
    sdr = adi.Pluto(cfg.URI)
    sdr.sample_rate = int(cfg.FS)

    sdr.rx_lo = int(cfg.FC)
    sdr.rx_rf_bandwidth = int(cfg.FS)
    sdr.rx_buffer_size = int(cfg.N_RAW)
    sdr.gain_control_mode_chan0 = "manual"
    sdr.rx_hardwaregain_chan0 = cfg.RX_GAIN
    sdr.rx_enabled_channels = [0]

    sdr.tx_lo = int(cfg.FC)
    sdr.tx_rf_bandwidth = int(cfg.FS)
    sdr.tx_hardwaregain_chan0 = cfg.TX_GAIN
    sdr.tx_enabled_channels = [0]
    sdr.tx_cyclic_buffer = True

    return sdr

def start_tx(sdr, cfg):
    try:
        sdr.tx_destroy_buffer()
    except Exception:
        pass
    if cfg.TX_TONE_HZ == 0:
        tx = 0.5 * np.ones(cfg.TX_LEN, dtype=np.complex64)
    else:
        n = np.arange(cfg.TX_LEN)
        tx = 0.5 * np.exp(1j * 2 * np.pi * cfg.TX_TONE_HZ * n / cfg.FS).astype(np.complex64)

    tx *= 2**14
    sdr.tx(tx)
    time.sleep(0.1)

def stop_tx(sdr):
    try:
        sdr.tx_destroy_buffer()
    except Exception:
        pass

def flush_rx(sdr, n=5):
    for _ in range(n):
        sdr.rx()