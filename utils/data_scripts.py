from ADCpoly_binParser.parser import MemoryFrame

def get_single_measurement(frame: MemoryFrame, channel_num: int) -> tuple[list, list]:
    adc_cells = 1024
    adc_timestep = 0.2  # ns

    if channel_num > 7:
        print('Count from 0')
        raise IndexError

    ch_data: list[int] = []
    for cell in range(adc_cells):
        ch_data.append(frame.cells[cell][channel_num])


    return [adc_timestep * count for count in range(adc_cells)], ch_data
