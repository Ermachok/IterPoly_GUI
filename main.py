import os

from ADCpoly_binParser.parser import parse_bin_file
from utils.data_scripts import get_single_measurement, apply_calibrations, apply_stop_point_shift
from plots_scripts.plots import plot_single_signal, plot_several_signals
from calculation_scripts.calculations import get_signals_integrals

if __name__ ==  '__main__':
    file_path = r"C:\development\IterPoly_GUI\data_folder\31_10_2024\no_lamp\side_a_fast_data_ng9.bin"
    #file_path = r"C:\development\IterPoly_GUI\data_folder\calibration_files\0_lvl_side_a_fast_data.bin"
    if os.path.exists(file_path):
        file_header, frames = parse_bin_file(file_path)
        print(f"Side: {file_header.side}, Mode: {file_header.mode}, Frame Count: {file_header.frame_count}")
        print(f"First Frame Stop Point: {frames[0].header.stop_point}, Timestamp: {frames[0].header.timestamp}")
    else:
        print("File not found!")
        raise FileExistsError('No such file')


    plot_several_signals(frames[:100], 6)

    print(get_signals_integrals(frames[:1000], channel_number=6))