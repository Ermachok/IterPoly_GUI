from statistics import mode, median

from ADCpoly_binParser.parser import MemoryFrame

import numpy as np


def calculate_fwhm(signal):
    signal = np.array(signal)

    signal_mode = mode(signal)
    min_value = min(signal)
    amplitude = abs(signal_mode - min_value)

    above_half_max = np.where(signal <= signal_mode - amplitude/2)[0]

    if len(above_half_max) == 0:
        return 0

    left_index = above_half_max[0]
    right_index = above_half_max[-1]

    fwhm = right_index - left_index

    return fwhm


def calculate_amplitude(signal: list) -> float:
    bit_depth = 2 ** 14  # bit depth
    adc_range = 1000
    signal_mode = mode(signal)
    min_val = min(signal)
    amplitude = abs(signal_mode - min_val)
    return amplitude / bit_depth * adc_range


def get_signals_integrals(frames: list[MemoryFrame], channel_number: int) -> None:
    adc_counts = 1024
    adc_timestep = 0.2  # ns
    bit_depth = 2 ** 14  # bit depth
    adc_range = 1000  # 1 volt

    sig_borders = [575, 815, 815 - 575]  # approx cells numbers and len
    all_integrals = []
    for frame in frames:
        signal = frame.adc_channels[channel_number]
        temp = mode(signal) * sig_borders[2] - sum(signal[sig_borders[0]:sig_borders[1]])
        # all_integrals.append(temp)
        all_integrals.append(temp * adc_range * adc_timestep / bit_depth)

    return median(all_integrals)
