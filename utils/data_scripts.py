import json
import os

from numpy.ma.extras import median

from ADCpoly_binParser.parser import MemoryFrame, parse_bin_file

ADC_COUNTS = 1024
ADC_CHANNELS = 8


def get_single_measurement(frame: MemoryFrame, channel_num: int) -> tuple[list, list]:
    adc_timestep = 0.2  # ns

    if channel_num > 7:
        print("Count from 0")
        raise IndexError

    ch_data: list[int] = []
    for cell in range(ADC_COUNTS):
        ch_data.append(frame.adc_channels[cell][channel_num])

    return [adc_timestep * count for count in range(ADC_COUNTS)], ch_data


def write_calibration_data_from_zero_lvl(
    input_file_path: str, output_file_path: str
) -> dict:
    channels_number = 8
    adc_cells_number = 1024

    if os.path.exists(input_file_path):
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

    apply_stop_point_shift(frames)

    all_channels = []
    for ch in range(channels_number):
        channel_cells = []
        for cell in range(adc_cells_number):
            one_cell_in_frames = []
            for frame in frames:
                one_cell_in_frames.append(frame.adc_channels[ch][cell])
            median_cell = median(one_cell_in_frames)
            channel_cells.append(median_cell)
        all_channels.append(channel_cells)

    result = {f"ch_{i}": all_channels[i] for i in range(channels_number)}

    with open(output_file_path, "w") as output:
        json.dump(result, output, indent=4)

    return result


def apply_stop_point_shift(frames: list[MemoryFrame]) -> None:
    for frame in frames:
        frame.adc_channels = (
            frame.adc_channels[ADC_COUNTS - frame.header.stop_point :]
            + frame.adc_channels[: ADC_COUNTS - frame.header.stop_point]
        )


def apply_calibrations(frames: list[MemoryFrame], calibration_file_path: str) -> None:
    with open(calibration_file_path, "r") as calibraton_file:
        calibration_data = json.load(calibraton_file)

    for frame in frames:
        for ch in range(ADC_CHANNELS):
            frame.adc_channels[ch] = [
                frame.adc_channels[ch][cell] - calibration_data[f"ch_{ch}"][cell]
                for cell in range(ADC_COUNTS)
            ]


if __name__ == "__main__":
    file_path = r"../data_folder/side_b_fast_data.bin"
    output_file = "../calibrations/adc0_side_a_calibration_30_05_2025.json"
    a = write_calibration_data_from_zero_lvl(file_path, output_file)
