# Screenshot and Recording Renamer
# Renames screenshots (.png) and screen recordings (.mp4) in a folder by the
# date and time each file was last modified, like:
#   2026-11-22 19.05.12_001.png
# The counter (_001, _002, ...) starts over at 1 each new day.

import os                               # file and folder tools (listdir, rename, paths)
import tkinter as tk                    # the window and widgets
from datetime import datetime           # turns timestamps into readable dates
from tkinter import filedialog, messagebox  # folder picker and popup dialogs


# Build the list of (old name, new name) pairs without renaming anything yet.
def make_plan(folder):
    # Helper: returns a file's modified time, used to sort files oldest first.
    def get_time(filename):
        path = os.path.join(folder, filename)
        return os.path.getmtime(path)

    plan = []  # empty list to collect pairs of old and new names
    number = 1  # the counter added to the end of each name
    last_day = ""  # the day of the last file, so the counter can reset each day
    files = sorted(os.listdir(folder), key=get_time)  # every file, oldest first

    for filename in files:
        # Only screenshots and recordings. .lower() makes .PNG and .MP4 match too.
        if filename.lower().endswith((".png", ".mp4")):
            new_name, ext = os.path.splitext(filename)  # split into name and extension
            path = os.path.join(folder, filename)
            seconds = os.path.getmtime(path)  # a big number: seconds since 1970
            taken = datetime.fromtimestamp(seconds)  # convert to date time
            date_text = taken.strftime("%Y-%m-%d %H.%M.%S")  # format the date time
            day = taken.strftime("%Y-%m-%d")  # just the date, to check for a new day
            if day != last_day:  # new day: start the counter over
                number = 1
                last_day = day
            new_name = f"{date_text}_{number:03d}{ext}"  # :03d pads to 3 digits; keeps the original extension
            if filename != new_name:  # skip files that already have the right name
                plan.append((filename, new_name))
            number += 1

    return plan

# Rename every file in the plan.
# Two passes: first to temp names, then to the final names. This stops one
# file's new name from clashing with another file's old name partway through.
def do_rename(folder, plan):
    temp_list = []

    for i, (old, new) in enumerate(plan):  # enumerate gives a number (i) for each pair
        ext = os.path.splitext(old)[1]  # get the extension of the old file
        tmp = f"temp_{i:03d}{ext}"  # create a temporary name with the same extension
        temp_list.append((old, tmp, new))  # old -> temp -> new

    # Pass 1: old name -> temp name. The _ means "this value isn't used here."
    for old, tmp, _ in temp_list:
        os.rename(os.path.join(folder, old), os.path.join(folder, tmp))

    # Pass 2: temp name -> final name
    for _, tmp, new in temp_list:
        os.rename(os.path.join(folder, tmp), os.path.join(folder, new))


# Globals shared by the button functions below
folder = ""  # the folder the user picked
plan = []  # the current rename plan for that folder

# "Choose Folder" button: pick a folder, build the plan, and show the preview.
def choose_folder():
    global folder, plan
    folder = filedialog.askdirectory()  # returns "" if the user cancels

    if folder == "":  # canceled: clear everything
        label.config(text="No folder selected")
        plan = []
        show_preview()
        return

    plan = make_plan(folder)
    show_preview()

    if not plan:  # empty list: nothing needs renaming
        label.config(text="No files to rename")
        return
    label.config(text=f"Selected folder: {folder} ({len(plan)} files to rename)")

# Fill the preview list with "old --> new" lines.
def show_preview():
    preview.delete(0, tk.END)  # clear the old preview first
    for old, new in plan:
        preview.insert(tk.END, f"{old} --> {new}")

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
        do_rename(folder, plan)
        label.config(text=f"Renamed {len(plan)} files")
        plan = []  # done, so clear the plan and the preview
        show_preview()
    except OSError as e:  # for example, a file is open in another program
        messagebox.showerror("Error", f"An error occurred while renaming files: {e}")
        label.config(text="Rename failed")
        plan = make_plan(folder)  # rebuild the plan from what's in the folder now
        show_preview()

# ---- Window setup ----
window = tk.Tk()
window.title("Screenshot & Recording Renamer")
window.geometry("800x500")  # width x height in pixels

label = tk.Label(window, text="Screenshot & Recording Renamer")  # also used for status messages
label.pack()

choose_folder_button = tk.Button(window, text="Choose Folder", command=choose_folder)
choose_folder_button.pack()

preview = tk.Listbox(window, width=100)  # shows the planned renames
preview.pack(fill="both", expand=True)  # stretches with the window

rename_button = tk.Button(window, text="Rename Files", command=rename_files)
rename_button.pack()

window.mainloop()  # keeps the window open and responding to clicks
