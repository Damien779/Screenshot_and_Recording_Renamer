# Screenshot and Recording Renamer

A small Python desktop app (Tkinter) that renames screenshots and screen recordings by the date and time they were taken. It can search one folder, or a main folder and all of its subfolders (for example, a tickets folder with one subfolder per ticket). Folders you use often can be saved and renamed all at once.

```
Screenshot 2026-11-10 113915.png  -->  2026-11-10 11.39.15_001.png
Screenshot 2026-11-10 114423.png  -->  2026-11-10 11.44.24_002.png
Screenshot 2026-11-11 092028.png  -->  2026-11-11 09.20.28_001.png
```

With subfolders, the preview shows where each file is:

```
Ticket 101\Screenshot 2026-11-10 113915.png  -->  2026-11-10 11.39.15_001.png
Ticket 101\clip.mp4                          -->  2026-11-10 11.41.02_002.mp4
Ticket 102\Screenshot 2026-11-11 092028.png  -->  2026-11-11 09.20.28_001.png
```

## Features
- Renames `.png` screenshots and `.mp4` screen recordings (any letter case, like `.PNG` or `.MP4`); other files are left alone
- **Include subfolders** (on by default): searches the folder you pick and every folder inside it, at any depth. Untick it to rename only the files in that one folder
- Files are renamed where they are; nothing is moved between folders
- Screenshots and recordings share one counter per day, per folder, so they stay in time order
- Hidden folders (names starting with a dot, like `.git`) are skipped
- **Saved folders**: save folders you rename often, then rename them all at once with **Rename Saved**. The list is kept between runs in `saved_folders.json` next to the app. Saved folders that no longer exist are skipped, and a folder saved inside another saved folder isn't renamed twice
- **Instructions** button opens a window that explains how to use the app
- Pick a folder with a dialog and preview every `old --> new` name (with its subfolder) before anything changes
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
1. Leave **Include subfolders** ticked to search every folder inside the one you pick, or untick it for just that folder. Changing it after choosing a folder updates the preview.
2. Click **Choose Folder** and pick your screenshots or recordings folder (or the main folder that holds them).
3. Check the preview. Nothing has changed yet.
4. Click **Rename Files** and confirm.

### Saved folders
1. Pick a folder with **Choose Folder**, then click **Save Folder**. Repeat for each folder you rename often.
2. Click **Rename Saved** to preview every saved folder at once. Each line starts with the saved folder's name:
   ```
   Tickets\Ticket 101\Screenshot 2026-11-10 113915.png  -->  2026-11-10 11.39.15_001.png
   Recordings\clip.mp4                                 -->  2026-11-11 08.02.44_001.mp4
   ```
3. Click **Rename Files** and confirm.

Click **Saved Folders** to see the list. Select a folder and click **Remove** to take it off (the folder and its files aren't touched).

`saved_folders.json` holds your own folder paths, so it's listed in `.gitignore` and isn't committed.

Click **Instructions** any time for a quick how-to.

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
