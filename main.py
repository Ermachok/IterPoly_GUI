import os

from ADCpoly_binParser.parser import parse_bin_file
from calculation_scripts.calculations import get_signals_integrals
from plots_scripts.plots import plot_several_signals, plot_single_signal
from utils.data_scripts import (apply_calibrations, apply_stop_point_shift,
                                get_single_measurement)

if __name__ == "__main__":
    file_path = r"data_folder/side_b_fast_data.bin"
    # file_path = r"C:\development\IterPoly_GUI\data_folder\calibration_files\0_lvl_side_a_fast_data.bin"
    if os.path.exists(file_path):
        file_header, frames = parse_bin_file(file_path)
        print(
            f"Side: {file_header.side}, Mode: {file_header.mode}, Frame Count: {file_header.frame_count}"
        )
        print(
            f"First Frame Stop Point: {frames[0].header.stop_point}, Timestamp: {frames[0].header.timestamp}"
        )
    else:
        print("File not found!")
        raise FileExistsError("No such file")

    apply_stop_point_shift(frames=frames)
    apply_calibrations(
        frames=frames, calibration_file_path="calibrations/adc0_side_a_calibration.json"
    )
    plot_several_signals(frames, 5)

    # print(get_signals_integrals(frames[:1000], channel_number=6))
