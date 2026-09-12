# Power Tapper

A small toolkit of auto-clicker / auto-tapper utilities for benchmarking and automating rapid taps/clicks, on both Android devices and PC.

## Contents

- **`android_tapper.py`** — Tkinter GUI that uses [ADB](https://developer.android.com/tools/adb) to rapid-fire `input tap` commands at up to 6 predefined coordinates on a connected Android device/emulator. Choose how many spots to cycle through via a dropdown, then START/STOP the tapping loop.
- **`pc_tapper.py`** — Tkinter GUI PC auto-clicker built on `pyautogui`, `pynput`, and `keyboard`. Hold **Ctrl + Left Click** to record target spots, choose Single/Double click mode, then press **F8** to start and **F9** to stop rapid-clicking through the recorded spots.
- **`cps_tester.html`** — Standalone HTML page that measures clicks-per-second (CPS) over a user-defined test duration. Open it directly in any browser — no build step required.

## Requirements

### PC Tapper (`pc_tapper.py`)
- Python 3.x
- Install dependencies:
  ```
  pip install -r requirements.txt
  ```

### Android Tapper (`android_tapper.py`)
- Python 3.x (uses only the standard library: `subprocess`, `tkinter`, `threading`)
- [Android Platform Tools (ADB)](https://developer.android.com/tools/releases/platform-tools) — download and place the `platform-tools` folder next to the script, then update `ADB_PATH` in `android_tapper.py` to match your local path.
- USB debugging enabled on the target Android device, connected via USB or Wi-Fi debugging.
- Edit the `SPOTS` list in `android_tapper.py` with your own screen coordinates before use.

### Optional: scrcpy
- [scrcpy](https://github.com/Genymobile/scrcpy) is handy for mirroring/viewing your Android device's screen on the PC to determine tap coordinates for `android_tapper.py`. It is not required and is not bundled in this repository — download it separately if needed.

## Usage

**PC Tapper**
```
python pc_tapper.py
```
1. Hold `Ctrl` and left-click on the screen to record one or more target spots.
2. Choose a click mode (Single/Double).
3. Press `F8` to start tapping through the recorded spots, `F9` to stop.

**Android Tapper**
```
python android_tapper.py
```
1. Make sure your device is connected and visible via `adb devices`.
2. Edit `SPOTS` in the script with the coordinates you want to tap.
3. Choose the number of spots to use from the dropdown, then click START/STOP.

**CPS Tester**

Just open `cps_tester.html` in a web browser and start clicking inside the target area.

## Disclaimer

This project automates rapid input (taps/clicks). Use responsibly and only where automation is permitted — automating input in online games or services may violate their terms of service.
