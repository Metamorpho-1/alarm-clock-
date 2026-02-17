# Python Desktop Alarm Clock (GUI, Multithreading & Custom OS Audio)

Hey there! Welcome to my Python Desktop Alarm Clock. 

I initially wrote this as a simple command-line script, but I wanted to challenge myself to build a fully functional, event-driven desktop application. Transitioning from a terminal script to a Graphical User Interface (GUI) introduced a major challenge: **blocking operations**. If you tell a GUI program to `time.sleep()`, the entire window freezes. 

To solve this, I completely refactored the application using **Object-Oriented Programming (OOP)** and the `threading` module to keep the clock ticking in the background while the UI stays buttery smooth.

## Core Features

* **Custom Audio File Explorer:** Integrated `tkinter.filedialog` so users can securely browse their host operating system and select any custom `.mp3` or `.wav` file for their alarm tone. 
* **Responsive GUI:** Built with `tkinter`, featuring a clean, live-updating digital clock display.
* **Multithreading:** The alarm-checking loop runs on a background daemon thread. This ensures the main application window never freezes or becomes unresponsive while waiting for the alarm to trigger.
* **Foolproof Input Validation:** Implemented `tk.Spinbox` widgets to prevent input crashes, and added OS-level path validation so the alarm cannot be set unless a valid audio file actually exists.
* **Snooze & Stop Logic:** Includes a built-in 5-minute snooze function that dynamically recalculates the target time and safely restarts the background thread.
* **Endless Audio Playback:** Utilizes the `pygame` mixer to load and infinitely loop the selected MP3 file until the user explicitly clicks "Stop" or "Snooze".

## How to Run It Locally

### Prerequisites
You will need Python installed on your machine, along with the `pygame` library for the audio playback.

1. Clone this repository:
   ```bash
   git clone [https://github.com/YOUR-USERNAME/python-gui-alarm.git](https://github.com/YOUR-USERNAME/python-gui-alarm.git)
   cd python-gui-alarm

2. Install the required audio library:
   ```bash
   pip install pygame

3. Run the app:
   ```bash
   python gui_alarm_clock.py

How to Use
Click Browse Audio... and select an .mp3 or .wav file from your computer.

Use the spinboxes to set your desired alarm time in 24-hour format.

Click Set Alarm. You can let the app run in the background; it will not freeze your computer.

When the alarm triggers, you can either Stop it completely or hit Snooze to get 5 more minutes of sleep!

What I Learned
Building this application was a massive leap forward in my understanding of desktop software architecture. I specifically learned:

1. How to structure tkinter applications using classes (OOP) to avoid messy global variables and manage the application "state" effectively.

2. The critical importance of the Python Global Interpreter Lock (GIL) and how to use threading.Thread(daemon=True) to offload blocking tasks so the main thread can continue rendering the UI.

3. Interacting with the host Operating System securely using os.path and file dialogs.

What's Next?
If I come back to expand this project, I plan to package it as a standalone .exe executable file using PyInstaller, so anyone can download and run the clock without needing to install Python or use a terminal.

   
