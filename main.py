import os

from ADCpoly_binParser.parser import parse_bin_file, apply_stop_point_shift
from utils.data_scripts import get_single_measurement
from plots_scripts.plots import plot_single_signal, plot_several_signals

if __name__ ==  '__main__':
    file_path = r"C:\development\IterPoly_GUI\data_folder\no_lamp\side_a_fast_data.bin"

    if os.path.exists(file_path):
        file_header, frames = parse_bin_file(file_path)
        print(f"Side: {file_header.side}, Mode: {file_header.mode}, Frame Count: {file_header.frame_count}")
        print(f"First Frame Stop Point: {frames[0].header.stop_point}, Timestamp: {frames[0].header.timestamp}")
    else:
        print("File not found!")
        raise FileExistsError('No such file')

    #apply_stop_point_shift(frames)
    plot_several_signals(frames[1:30], 6)