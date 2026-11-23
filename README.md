# Screenshot and Recording Renamer

A small Python desktop app (Tkinter) that renames a folder of screenshots and screen recordings by the date and time they were taken.

```
Screenshot 2026-11-10 113915.png  -->  2026-11-10 11.39.15_001.png
Screenshot 2026-11-10 114423.png  -->  2026-11-10 11.44.24_002.png
Screenshot 2026-11-11 092028.png  -->  2026-11-11 09.20.28_001.png
```

## Features
- Renames `.png` screenshots and `.mp4` screen recordings (any letter case, like `.PNG` or `.MP4`); other files are left alone
- Screenshots and recordings share one counter per day, so they stay in time order
- Pick a folder with a dialog and preview every `old --> new` name before anything changes
- Sorts files by date modified; numbering restarts at `001` each day
- Safe two-pass rename (via temporary names), so new names never collide with existing ones
- Running it again on already-renamed files changes nothing
- Asks for confirmation before renaming
- Shows an error popup instead of crashing if a file is missing or locked

## Requirements
- Python 3.8+ (Tkinter is included with Python on Windows and macOS)
- On Linux you may need: `sudo apt install python3-tk`

## Usage
```bash
python "Screenshot and Recording Renamer.py"
```
1. Click **Choose Folder** and pick your screenshots or recordings folder.
2. Check the preview.
3. Click **Rename Files** and confirm.

Tip: try it on a folder of copies first.

The window opens small. Drag its edge to make it bigger if long names in the preview are cut off.

## Desktop shortcut (Windows)
To open the app without a console window, make a desktop shortcut that runs it with `pythonw.exe`:

1. Right-click the desktop, choose **New > Shortcut**.
2. For the location, enter the full path to `pythonw.exe` in quotes, a space, then the full path to `Screenshot and Recording Renamer.py` in quotes. For example:
   ```
   "C:\Path\To\Python\pythonw.exe" "C:\Path\To\Screenshot-and-Recording-Renamer\Screenshot and Recording Renamer.py"
   ```
3. Name it something like **Rename Screenshots & Recordings**.

If you move or rename the `.py` file, update the shortcut's **Target** (right-click it, then **Properties**).

With `pythonw.exe` there's no console, so error messages and `print()` output won't show. Run it from VS Code or a terminal to debug.
