import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ADCpoly_binParser.parser import parse_bin_file

from calculation_scripts.calculations import calculate_amplitude, calculate_fwhm


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("File Parser and Plotter")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.file_path = ""
        self.frames = []
        for row_num in range(5):
            self.root.grid_rowconfigure(row_num, weight=0)
        self.root.grid_rowconfigure(5, weight=1)

        for column_num in range(5):
            self.root.grid_columnconfigure(column_num, weight=0)
        self.root.grid_columnconfigure(5, weight=12)

        self.select_file_btn = tk.Button(self.root, text="Select File", command=self.select_file, width=10)
        self.parse_file_btn = tk.Button(self.root, text="Parse File", command=self.parse_file, state=tk.DISABLED,
                                        width=10)

        self.select_file_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=1)
        self.parse_file_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=1)

        self.plot_graph_btn = tk.Button(self.root, text="Plot Graph", command=self.plot_graph, state=tk.DISABLED,
                                        width=10)
        self.plot_graph_btn.grid(row=0, column=1, padx=5, pady=10, sticky="ew", columnspan=1)

        self.frame_label = tk.Label(self.root, text="Frame Number:")
        self.frame_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        self.frame_entry = tk.Entry(self.root, width=5)
        self.frame_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.channel_label = tk.Label(self.root, text="Channel Number:")
        self.channel_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")

        self.channel_entry = tk.Entry(self.root, width=5)
        self.channel_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        self.average_btn = tk.Button(self.root, text="Plot average signals", command=self.plot_average_signal,
                                     state=tk.DISABLED, width=10)
        self.average_btn.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        self.amplitude_label = tk.Label(self.root, text="Signal amplitudes: ", anchor="w")
        self.amplitude_label.grid(row=1, column=4, padx=5, pady=5, sticky="w")

        self.fwhm_label = tk.Label(self.root, text="Signal FWHM: ", anchor="w")
        self.fwhm_label.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=6, pady=20, sticky="nsew")

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin")])
        if self.file_path:
            messagebox.showinfo("File Selected", f"Selected file: {self.file_path}")
            self.parse_file_btn.config(state=tk.NORMAL)

    def parse_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected")
            return

        try:
            file_header, frames = parse_bin_file(self.file_path)
            self.frames = frames
            messagebox.showinfo("Success", f"Parsing complete. Number of frames: {len(frames)}")
            self.plot_graph_btn.config(state=tk.NORMAL)
            self.average_btn.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse the file: {e}")

    def plot_graph(self):
        frame_number = self.frame_entry.get()
        ch_numbers = self.channel_entry.get()

        if not frame_number.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid number for frame")
            return

        frame_number = int(frame_number)

        if frame_number < 0 or frame_number >= len(self.frames):
            messagebox.showerror("Invalid Frame", f"Frame number should be between 0 and {len(self.frames) - 1}")
            return

        try:
            ch_numbers = [int(ch.strip()) for ch in ch_numbers.split(',')]
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for channels, separated by commas")
            return

        invalid_channels = [ch for ch in ch_numbers if ch < 0 or ch >= len(self.frames[frame_number].adc_channels)]
        if invalid_channels:
            messagebox.showerror("Invalid Channel", f"Invalid channels: {', '.join(map(str, invalid_channels))}")
            return

        self.ax.clear()

        for ch_number in ch_numbers:
            channel_data = self.frames[frame_number].adc_channels[ch_number]
            times = list(range(1024))

            self.ax.plot(times, channel_data, label=f"Channel {ch_number}")

        self.ax.set_title(f"Graph for Frame {frame_number}")
        self.ax.legend()
        self.ax.grid()
        self.ax.set_ylabel('adc counts, a.u.')
        self.ax.set_xlabel('time, ns')
        self.canvas.draw()

    def plot_average_signal(self, adc_timestep: float = 0.2):
        ch_numbers = self.channel_entry.get()

        try:
            ch_numbers = [int(ch.strip()) for ch in ch_numbers.split(',')]
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for channels, separated by commas")
            return

        averaged_data = {}
        amplitudes = {}
        fwhms = {}

        for ch_number in ch_numbers:
            if ch_number < 0 or ch_number >= len(self.frames[0].adc_channels):
                messagebox.showerror("Invalid Channel", f"Channel {ch_number} is out of range")
                return

            summed_data = [0] * 1024
            frame_count = 0

            for frame in self.frames[:500]:
                channel_data = frame.adc_channels[ch_number]
                summed_data = [sum_value + channel_data[i] for i, sum_value in enumerate(summed_data)]
                frame_count += 1

            averaged_data[ch_number] = [sum_value / frame_count for sum_value in summed_data]

            amplitude = calculate_amplitude(averaged_data[ch_number])
            amplitudes[ch_number] = amplitude

            fwhms[ch_number] = calculate_fwhm(averaged_data[ch_number]) * adc_timestep

        amplitude_text = "; ".join([f"Ch {ch}: {amplitudes[ch]:.2f}" for ch in ch_numbers])
        fwhm_text = "; ".join([f"Ch {ch}: {fwhms[ch]:.2f} ns" for ch in ch_numbers])

        self.amplitude_label.config(text=f"Signals amplitudes (mV): {amplitude_text}")
        self.fwhm_label.config(text=f"Signal FWHM: {fwhm_text}")

        self.ax.clear()

        times = [i * adc_timestep for i in range(1024)]
        for ch_number, data in averaged_data.items():
            self.ax.plot(times, data, label=f"Channel {ch_number} (avg)")

        self.ax.set_title("Average Signal")
        self.ax.legend()
        self.ax.set_ylabel('adc counts, a.u.')
        self.ax.set_xlabel('time, ns')
        self.ax.set_xlim([90, 190])
        self.ax.grid()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
