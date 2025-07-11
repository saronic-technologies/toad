import tkinter as tk
import time
import tkinter.messagebox as messagebox
from utils import send_crystal_command, send_local_command

class PauseUnpauseGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pause/Unpause GUI")

        self.is_unpaused = False
        self.unpause_start_time = None
        self.total_unpause_time = 0
        self.start_button_clicked = False

        self.pause_button = tk.Button(self.root, text="PAUSE", command=self.pause, state=tk.DISABLED)
        self.pause_button.pack(pady=10)

        self.unpause_button = tk.Button(self.root, text="UNPAUSE", command=self.unpause, state=tk.DISABLED)
        self.unpause_button.pack(pady=10)

        self.time_label = tk.Label(self.root, text="Total Unpause Time: 0 seconds")
        self.time_label.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Status: N/A")
        self.status_label.pack(pady=10)

        self.start_button = tk.Button(self.root, text="START doompctl", command=self.start_doompctl, state=tk.NORMAL)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="STOP doompctl", command=self.stop_doompctl, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.filesize_label = tk.Label(self.root, text="calibration.mcap filesize: N/A")
        self.filesize_label.pack(pady=10)

        self.update_time()

    def start_doompctl(self):
        if not self.start_button_clicked:
            self.start_button_clicked = True
            self.start_button.config(state=tk.DISABLED)
            self.status_label.config(text="Status: Started")
            self.pause_button.config(state=tk.NORMAL)
            self.unpause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)

            # Automatically toggle unpause and start the timer
            self.unpause()

    def stop_doompctl(self):
        response = messagebox.askyesno("Confirm Stop", "Once doomper is stopped this GUI will close. Are you sure?")
        if response:
            self.status_label.config(text="Status: Stopped")
            self.pause_button.config(state=tk.DISABLED)
            self.unpause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.root.destroy()

    def pause(self):
        if self.is_unpaused:
            self.is_unpaused = False
            self.pause_button.config(state=tk.DISABLED)
            self.unpause_button.config(state=tk.NORMAL)
            self.total_unpause_time += time.time() - self.unpause_start_time
            self.status_label.config(text="Status: Pause")

            # Update calibration.mcap filesize
            filesize = self.get_calibration_filesize()
            self.filesize_label.config(text=f"calibration.mcap filesize: {filesize} bytes")

    def unpause(self):
        if not self.is_unpaused:
            self.is_unpaused = True
            self.unpause_start_time = time.time()
            self.pause_button.config(state=tk.NORMAL)
            self.unpause_button.config(state=tk.DISABLED)
            self.status_label.config(text="Status: Unpause")

            # Indicate that filesize is not live updated
            self.filesize_label.config(text="calibration.mcap filesize: ...")

    def get_calibration_filesize(self):
        try:
            mcap_filesize = None # this should be a command to retrieve the filesize of the mcap
            return mcap_filesize
        except FileNotFoundError:
            return "File not found"

    def update_time(self):
        if self.is_unpaused:
            elapsed_time = time.time() - self.unpause_start_time
            self.time_label.config(text=f"Total Unpause Time: {self.total_unpause_time + elapsed_time:.2f} seconds")
        else:
            self.time_label.config(text=f"Total Unpause Time: {self.total_unpause_time:.2f} seconds")
        self.root.after(100, self.update_time)

    def run(self):
        self.root.mainloop()