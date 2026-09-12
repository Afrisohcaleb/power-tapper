import pyautogui
import keyboard
import tkinter as tk
import threading
import time
from pynput import mouse

class PCTapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Multi-Tapper")
        self.root.geometry("350x300")
        self.root.attributes("-topmost", True)
        
        self.running = False
        self.spots = []
        
        # UI Elements
        self.title_label = tk.Label(root, text="PC Auto-Tapper", font=("Helvetica", 12, "bold"))
        self.title_label.pack(pady=10)
        
        self.info_label = tk.Label(root, text="Hold 'Ctrl' + Left Click to record a spot.", fg="blue")
        self.info_label.pack(pady=2)

        # Mode Selection Dropdown
        mode_frame = tk.Frame(root)
        mode_frame.pack(pady=5)
        tk.Label(mode_frame, text="Click Mode:").pack(side=tk.LEFT)
        self.click_mode = tk.StringVar(value="Single Click")
        self.mode_menu = tk.OptionMenu(mode_frame, self.click_mode, "Single Click", "Double Click")
        self.mode_menu.pack(side=tk.LEFT, padx=5)
        
        self.spots_label = tk.Label(root, text="Target Spots Recorded: 0", font=("Helvetica", 10))
        self.spots_label.pack(pady=5)
        
        self.status_label = tk.Label(root, text="Status: Stopped", fg="red", font=("Helvetica", 10))
        self.status_label.pack(pady=5)
        
        self.warning_label = tk.Label(root, text="Press F8 to START  |  Press F9 to STOP", font=("Helvetica", 9, "bold"))
        self.warning_label.pack(pady=10)
        
        self.clear_btn = tk.Button(root, text="Clear Recorded Spots", command=self.clear_spots)
        self.clear_btn.pack(pady=5)

        # Start the background listeners
        threading.Thread(target=self.keyboard_listener, daemon=True).start()
        
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.mouse_listener.start()

    def clear_spots(self):
        self.spots.clear()
        self.spots_label.config(text=f"Target Spots Recorded: {len(self.spots)}")

    def on_mouse_click(self, x, y, button, pressed):
        """Listens for mouse clicks globally."""
        if pressed and button == mouse.Button.left:
            if keyboard.is_pressed('ctrl'):
                actual_x, actual_y = pyautogui.position()
                if (actual_x, actual_y) not in self.spots:
                    self.spots.append((actual_x, actual_y))
                    self.root.after(0, lambda: self.spots_label.config(text=f"Target Spots Recorded: {len(self.spots)}"))

    def keyboard_listener(self):
        """Listens for Start/Stop hotkeys."""
        while True:
            if keyboard.is_pressed('f8') and not self.running and len(self.spots) > 0:
                self.running = True
                self.root.after(0, lambda: self.status_label.config(text="Status: Tapping...", fg="green"))
                
                # Grabs the selected mode and passes it safely into the background thread
                selected_mode = self.click_mode.get()
                threading.Thread(target=self.tap_loop, args=(selected_mode,), daemon=True).start()
                time.sleep(0.3)
                
            elif keyboard.is_pressed('f9') and self.running:
                self.running = False
                self.root.after(0, lambda: self.status_label.config(text="Status: Stopped", fg="red"))
                time.sleep(0.3)
            
            time.sleep(0.05)

    def tap_loop(self, mode):
        # Removes PyAutoGUI's safety delay entirely for maximum speed
        pyautogui.PAUSE = 0 
        
        while self.running:
            for x, y in self.spots:
                if mode == "Double Click":
                    pyautogui.click(x=x, y=y, clicks=2, interval=0.05)
                else:
                    pyautogui.click(x=x, y=y)
                
                if not self.running:
                    break

if __name__ == "__main__":
    root = tk.Tk()
    app = PCTapperApp(root)
    root.mainloop()