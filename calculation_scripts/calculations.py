from statistics import mode, median

from ADCpoly_binParser.parser import MemoryFrame


def get_signals_integrals(frames: list[MemoryFrame], channel_number: int) -> None:
    adc_counts = 1024
    adc_timestep = 0.2  # ns
    bit_depth = 2**14   # bit depth
    adc_range = 1000 # 1 volt

    sig_borders = [575, 815, 815 - 575] # approx cells numbers and len
    all_integrals = []
    for frame in frames:
        signal = frame.adc_channels[channel_number]
        temp = mode(signal) * sig_borders[2] - sum(signal[sig_borders[0]:sig_borders[1]])
        #all_integrals.append(temp)
        all_integrals.append(temp * adc_range * adc_timestep / bit_depth)

    return median(all_integrals)