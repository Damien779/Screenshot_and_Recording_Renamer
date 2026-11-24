# Screenshot and Recording Renamer
# Renames screenshots (.png) and screen recordings (.mp4) by the date and time
# each file was last modified, like:
#   2026-11-22 19.05.12_001.png
# It can search one folder or a main folder plus all of its subfolders.
# Files are renamed where they are; nothing is moved between folders.
# The counter (_001, _002, ...) starts over at 1 each new day, separately in
# each folder.

import os                               # file and folder tools (walk, rename, paths)
import tkinter as tk                    # the window and widgets
from datetime import datetime           # turns timestamps into readable dates
from tkinter import filedialog, messagebox  # folder picker and popup dialogs

FILE_TYPES = (".png", ".mp4")  # the extensions this app renames (compared in lowercase)

# Text shown in the Instructions window. Triple quotes let a string span many lines.
HELP_TEXT = """What this app does
Renames screenshots (.png) and screen recordings (.mp4) by the date and time
each file was last modified, for example:
    Screenshot 2026-11-22 190512.png  -->  2026-11-22 19.05.12_001.png

How to use it
1. Leave "Include subfolders" ticked to search the folder you pick and every
   folder inside it. Untick it to rename only the files in that one folder.
2. Click Choose Folder and pick the main folder (for example, your tickets folder).
3. Check the preview. Each line shows the file's subfolder, its current name,
   and its new name. Nothing has changed yet.
4. Click Rename Files, then Yes to confirm.

Good to know
- Files stay in the folder they're in. Only their names change.
- The number at the end (_001, _002...) starts over each day, separately in
  each folder, so screenshots and recordings stay in time order.
- Files that already have the right name are skipped, so running it again
  is safe.
- Hidden folders (names starting with a dot, like .git) are skipped.
- If a file is open in another program, the rename stops and shows an error.
  Close the file and try again.
- Tip: try it on a copy of a folder first."""


# Build the plan for ONE folder: a list of (folder, old name, new name),
# without renaming anything yet.
def plan_one_folder(folder):
    # Helper: returns a file's modified time, used to sort files oldest first.
    def get_time(filename):
        return os.path.getmtime(os.path.join(folder, filename))

    plan = []  # empty list to collect (folder, old, new) for this folder
    number = 1  # the counter added to the end of each name
    last_day = ""  # the day of the last file, so the counter can reset each day

    # Only screenshots and recordings. .lower() makes .PNG and .MP4 match too.
    files = [name for name in os.listdir(folder)
             if name.lower().endswith(FILE_TYPES) and os.path.isfile(os.path.join(folder, name))]
    files.sort(key=get_time)  # oldest first

    for filename in files:
        ext = os.path.splitext(filename)[1]  # keep the original extension
        seconds = os.path.getmtime(os.path.join(folder, filename))  # seconds since 1970
        taken = datetime.fromtimestamp(seconds)  # convert to date time
        date_text = taken.strftime("%Y-%m-%d %H.%M.%S")  # format the date time
        day = taken.strftime("%Y-%m-%d")  # just the date, to check for a new day
        if day != last_day:  # new day: start the counter over
            number = 1
            last_day = day
        new_name = f"{date_text}_{number:03d}{ext}"  # :03d pads to 3 digits
        if filename != new_name:  # skip files that already have the right name
            plan.append((folder, filename, new_name))
        number += 1

    return plan


# Build the plan for the main folder, and its subfolders if include_subfolders is True.
def make_plan(main_folder, include_subfolders):
    if not include_subfolders:
        return plan_one_folder(main_folder)

    plan = []
    # os.walk visits main_folder and then every folder inside it, at any depth.
    # For each one it gives: the folder's path, the names of its subfolders,
    # and the names of its files.
    for current, subfolders, _files in os.walk(main_folder):
        # Skip hidden folders like .git. Changing subfolders[:] in place tells
        # os.walk not to go into the ones we removed.
        subfolders[:] = sorted(d for d in subfolders if not d.startswith("."))
        try:
            plan.extend(plan_one_folder(current))
        except OSError:
            pass  # a folder we can't read (no permission): skip it
    return plan


# Rename every file in the plan.
# Two passes: first to temp names, then to the final names. This stops one
# file's new name from clashing with another file's old name partway through.
def do_rename(plan):
    temp_list = []

    for i, (folder, old, new) in enumerate(plan):  # enumerate gives a number (i) for each entry
        ext = os.path.splitext(old)[1]  # get the extension of the old file
        tmp = f"temp_{i:04d}{ext}"  # a temporary name, unique for each file
        temp_list.append((folder, old, tmp, new))  # old -> temp -> new, in the same folder

    # Pass 1: old name -> temp name. The _ means "this value isn't used here."
    for folder, old, tmp, _ in temp_list:
        os.rename(os.path.join(folder, old), os.path.join(folder, tmp))

    # Pass 2: temp name -> final name
    for folder, _, tmp, new in temp_list:
        os.rename(os.path.join(folder, tmp), os.path.join(folder, new))


# Globals shared by the button functions below
main_folder = ""  # the folder the user picked
plan = []  # the current rename plan
help_window = None  # the Instructions window, if it's open

# Build the plan for the chosen folder and show it.
def refresh_plan():
    global plan
    plan = make_plan(main_folder, include_subfolders.get())
    show_preview()
    if not plan:  # empty list: nothing needs renaming
        label.config(text=f"No files to rename in {main_folder}")
        return
    folders = len({folder for folder, _, _ in plan})  # a set keeps each folder once
    label.config(text=f"{main_folder}: {len(plan)} files to rename in {folders} folder(s)")

# "Choose Folder" button: pick a folder, build the plan, and show the preview.
def choose_folder():
    global main_folder, plan
    picked = filedialog.askdirectory()  # returns "" if the user cancels

    if picked == "":  # canceled: clear everything
        main_folder = ""
        label.config(text="No folder selected")
        plan = []
        show_preview()
        return

    main_folder = picked
    refresh_plan()

# "Include subfolders" tick box: rebuild the preview when it changes.
def subfolders_changed():
    if main_folder:
        refresh_plan()

# Fill the preview list with "subfolder\old --> new" lines.
def show_preview():
    preview.delete(0, tk.END)  # clear the old preview first
    for folder, old, new in plan:
        # relpath gives the path from the main folder, like "Ticket 123\Screenshot.png"
        shown = os.path.relpath(os.path.join(folder, old), main_folder)
        preview.insert(tk.END, f"{shown} --> {new}")

# "Rename Files" button: confirm, then rename everything in the plan.
def rename_files():
    global plan
    if not plan:
        label.config(text="Choose a folder")
        return
    answer = messagebox.askyesno("Confirm Rename", f"Are you sure you want to rename {len(plan)} files?")
    if not answer:  # the user clicked No
        label.config(text="Rename cancelled")
        return
    try:
        do_rename(plan)
        label.config(text=f"Renamed {len(plan)} files")
        plan = []  # done, so clear the plan and the preview
        show_preview()
    except OSError as e:  # for example, a file is open in another program
        messagebox.showerror("Error", f"An error occurred while renaming files: {e}")
        label.config(text="Rename failed")
        refresh_plan()  # rebuild the plan from what's in the folders now

# "Instructions" button: open a window with HELP_TEXT.
def show_instructions():
    global help_window
    # If it's already open, bring it to the front instead of opening a second one
    if help_window is not None and help_window.winfo_exists():
        help_window.lift()
        return

    help_window = tk.Toplevel(window)  # a second window that belongs to the main one
    help_window.title("Instructions")
    help_window.resizable(False, False)
    tk.Label(help_window, text=HELP_TEXT, justify="left", padx=12, pady=10).pack()
    tk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=(0, 10))

# ---- Window setup ----
window = tk.Tk()
window.title("Screenshot & Recording Renamer")
window.geometry("450x320")  # width x height in pixels

label = tk.Label(window, text="Screenshot & Recording Renamer", wraplength=430)  # also used for status messages
label.pack()

# Choose Folder and Instructions side by side in one row
top_row = tk.Frame(window)
top_row.pack()
choose_folder_button = tk.Button(top_row, text="Choose Folder", command=choose_folder)
choose_folder_button.pack(side="left", padx=4)
instructions_button = tk.Button(top_row, text="Instructions", command=show_instructions)
instructions_button.pack(side="left", padx=4)

include_subfolders = tk.BooleanVar(value=True)  # ticked by default
tk.Checkbutton(window, text="Include subfolders", variable=include_subfolders,
               command=subfolders_changed).pack()

preview = tk.Listbox(window, width=100)  # shows the planned renames
preview.pack(fill="both", expand=True)  # stretches with the window

rename_button = tk.Button(window, text="Rename Files", command=rename_files)
rename_button.pack()

window.mainloop()  # keeps the window open and responding to clicks
