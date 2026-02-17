import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import time
import threading
import pygame
import os

class AdvancedAlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Pro Alarm Clock")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        
        # Initialize Pygame Mixer for audio
        pygame.mixer.init()
        self.sound_file = 'Sapphire - (Raag.Fm).mp3'
        
        # State variables
        self.alarm_thread = None
        self.alarm_time = None
        self.is_alarm_set = False
        self.is_playing = False

        self.setup_ui()
        self.update_live_clock()

    def setup_ui(self):
        """Builds the graphical user interface."""
        # Main Container
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        # Live Clock Display
        self.clock_label = tk.Label(frame, text="", font=("Helvetica", 32, "bold"), fg="#333333")
        self.clock_label.pack(pady=10)

        # Instructions
        tk.Label(frame, text="Set Alarm Time (24-Hour Format)", font=("Helvetica", 10)).pack(pady=5)

        # Time Input Frame (Hours : Minutes : Seconds)
        input_frame = tk.Frame(frame)
        input_frame.pack(pady=10)

        # Spinboxes for foolproof input (prevents user from typing letters)
        self.hour_var = tk.StringVar(value="00")
        self.min_var = tk.StringVar(value="00")
        self.sec_var = tk.StringVar(value="00")

        tk.Spinbox(input_frame, from_=0, to=23, wrap=True, textvariable=self.hour_var, width=3, font=("Helvetica", 16), format="%02.0f").pack(side=tk.LEFT, padx=5)
        tk.Label(input_frame, text=":", font=("Helvetica", 16, "bold")).pack(side=tk.LEFT)
        tk.Spinbox(input_frame, from_=0, to=59, wrap=True, textvariable=self.min_var, width=3, font=("Helvetica", 16), format="%02.0f").pack(side=tk.LEFT, padx=5)
        tk.Label(input_frame, text=":", font=("Helvetica", 16, "bold")).pack(side=tk.LEFT)
        tk.Spinbox(input_frame, from_=0, to=59, wrap=True, textvariable=self.sec_var, width=3, font=("Helvetica", 16), format="%02.0f").pack(side=tk.LEFT, padx=5)

        # Status Label
        self.status_label = tk.Label(frame, text="No alarm set.", font=("Helvetica", 10, "italic"), fg="#666666")
        self.status_label.pack(pady=10)

        # Buttons Frame
        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=10)

        self.set_btn = ttk.Button(btn_frame, text="Set Alarm", command=self.set_alarm)
        self.set_btn.grid(row=0, column=0, padx=5)

        self.snooze_btn = ttk.Button(btn_frame, text="Snooze (5m)", command=self.snooze_alarm, state=tk.DISABLED)
        self.snooze_btn.grid(row=0, column=1, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="Stop Alarm", command=self.stop_alarm, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=2, padx=5)

    def update_live_clock(self):
        """Updates the digital clock on the GUI every 1000 milliseconds (1 second)."""
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.clock_label.config(text=current_time)
        
        # Schedule this function to run again in 1000ms
        self.root.after(1000, self.update_live_clock)

    def set_alarm(self):
        """Grabs the input from spinboxes and starts the background alarm thread."""
        # Format the spinbox inputs into HH:MM:SS
        h = self.hour_var.get().zfill(2)
        m = self.min_var.get().zfill(2)
        s = self.sec_var.get().zfill(2)
        
        self.alarm_time = f"{h}:{m}:{s}"
        self.is_alarm_set = True

        self.status_label.config(text=f"Alarm successfully set for {self.alarm_time}", fg="green")
        self.set_btn.config(state=tk.DISABLED)

        # Start the checking loop in a separate thread so it doesn't freeze the GUI
        self.alarm_thread = threading.Thread(target=self.check_alarm_loop, daemon=True)
        self.alarm_thread.start()

    def check_alarm_loop(self):
        """Runs in the background, checking the time continuously."""
        while self.is_alarm_set:
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            
            if current_time == self.alarm_time:
                self.trigger_alarm()
                break
                
            time.sleep(1) # Sleep the background thread, not the main GUI

    def trigger_alarm(self):
        """Plays the sound and updates the UI to allow stopping/snoozing."""
        self.is_alarm_set = False
        self.is_playing = True
        
        self.status_label.config(text="WAKE UP!", fg="red", font=("Helvetica", 12, "bold"))
        self.snooze_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)

        if os.path.exists(self.sound_file):
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play(-1) # -1 makes the music loop endlessly until stopped
        else:
            messagebox.showerror("Error", f"Sound file '{self.sound_file}' not found!")

    def stop_alarm(self):
        """Stops the music and resets the UI."""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            
        self.is_alarm_set = False
        self.status_label.config(text="Alarm stopped.", fg="#666666", font=("Helvetica", 10, "italic"))
        self.reset_buttons()

    def snooze_alarm(self):
        """Stops current music and adds 5 minutes to the alarm time."""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            
        # Calculate new time (+5 minutes)
        now = datetime.datetime.now()
        snooze_time = now + datetime.timedelta(minutes=5)
        self.alarm_time = snooze_time.strftime('%H:%M:%S')
        
        self.is_alarm_set = True
        self.status_label.config(text=f"Snoozed. Next alarm at {self.alarm_time}", fg="orange")
        self.reset_buttons()
        self.set_btn.config(state=tk.DISABLED)
        
        # Restart the background thread
        self.alarm_thread = threading.Thread(target=self.check_alarm_loop, daemon=True)
        self.alarm_thread.start()

    def reset_buttons(self):
        self.set_btn.config(state=tk.NORMAL)
        self.snooze_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    app = AdvancedAlarmClock(root)
    root.mainloop()
