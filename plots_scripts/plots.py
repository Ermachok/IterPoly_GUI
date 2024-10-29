import matplotlib.pyplot as plt

from ADCpoly_binParser.parser import MemoryFrame

def plot_single_signal(times: list, ch_data: list) -> None:
    plt.plot(times, ch_data)
    plt.show()


def plot_several_signals(frames: list[MemoryFrame], channel_number: int) -> None:
    adc_counts = 1024
    timestep = 0.2  # ns

    time = [timestep * count for count in range(adc_counts)]

    for frame in frames:
        plt.plot(time, [frame.cells[cell][channel_number] for cell in range(adc_counts)])

    plt.show()