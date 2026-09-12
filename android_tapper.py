import subprocess
import tkinter as tk
import threading

# Define your 5 target spots here (X, Y)
# The bot will read from top to bottom based on how many spots you select in the GUI.
SPOTS = [
    (733, 1225),  # Spot 1
    (500, 1000),  # Spot 2
    (600, 1100),  # Spot 3
    (300, 800),   # Spot 4
    (800, 867),   # Spot 5 
    (493, 855)  # Spot 6
]
ADB_PATH = r"C:\Users\KALEB\Desktop\power tapper\platform-tools\adb.exe"

class AutoTapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Tapper")
        self.root.geometry("350x200") # Made the window slightly larger to fit the new menu
        self.root.attributes("-topmost", True)
        
        self.running = False

        self.title_label = tk.Label(root, text="High-Speed Multi-Tapper", font=("Helvetica", 12, "bold"))
        self.title_label.pack(pady=10)

        # --- New Feature: Dropdown for selecting number of spots ---
        self.num_spots_var = tk.IntVar(value=1)
        
        spot_frame = tk.Frame(root)
        spot_frame.pack(pady=5)
        
        tk.Label(spot_frame, text="Number of spots to tap:").pack(side=tk.LEFT)
        
        # Creates a dropdown menu with options 1 through 5
        self.spot_menu = tk.OptionMenu(spot_frame, self.num_spots_var, 1, 2, 3, 4, 5, 6)
        self.spot_menu.pack(side=tk.LEFT, padx=6)
        # -----------------------------------------------------------

        self.status_label = tk.Label(root, text="Status: Stopped", fg="red", font=("Helvetica", 10))
        self.status_label.pack(pady=6)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.start_btn = tk.Button(button_frame, text="START", width=10, bg="green", fg="white", command=self.start_tapping)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = tk.Button(button_frame, text="STOP", width=10, bg="red", fg="white", command=self.stop_tapping)
        self.stop_btn.grid(row=0, column=1, padx=6)

    def tap_loop(self, num_spots):
        # Dynamically grabs only the number of spots you selected
        active_spots = SPOTS[:num_spots]
        
        # Builds the chained ADB command for the selected spots
        single_sequence = " ; ".join([f"input tap {x} {y}" for x, y in active_spots])
        
        # Duplicates the sequence in one command block to maintain maximum tapping speed
        rapid_command = f"{single_sequence} ; {single_sequence}"
        
        while self.running:
            subprocess.run(
                [ADB_PATH, "shell", rapid_command],
                capture_output=True
            )

    def start_tapping(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="Status: Tapping...", fg="green")
            
            # Disable the dropdown menu while running so it can't be changed mid-tap
            self.spot_menu.config(state="disabled")
            
            # Pass the selected number of spots into the background thread
            selected_spots = self.num_spots_var.get()
            threading.Thread(target=self.tap_loop, args=(selected_spots,), daemon=True).start()

    def stop_tapping(self):
        self.running = False
        self.status_label.config(text="Status: Stopped", fg="red")
        
        # Re-enable the dropdown menu when stopped
        self.spot_menu.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTapperApp(root)
    root.mainloop()