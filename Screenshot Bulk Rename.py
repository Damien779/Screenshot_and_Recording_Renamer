import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox


def make_plan(folder):
    def get_time(filename):
        path = os.path.join(folder, filename)
        return os.path.getmtime(path)

    plan = [] #NEW: empty list to collectnew pairs of old and new names
    number = 1
    last_day = ""
    files = sorted(os.listdir(folder), key=get_time)

    for filename in files:
        if filename.endswith(".png"):
            new_name, ext = os.path.splitext(filename)
            path = os.path.join(folder, filename)
            seconds = os.path.getmtime(path)  # a big number: seconds since 1970
            taken = datetime.fromtimestamp(seconds)  # convert to date time
            date_text = taken.strftime("%Y-%m-%d %H.%M.%S")  # format the date time
            day = taken.strftime("%Y-%m-%d")
            if day != last_day:
                number = 1
                last_day = day
            new_name = f"{date_text}_{number:03d}{ext}"
            if filename != new_name:
                plan.append((filename, new_name))
            number += 1

    return plan

def do_rename(folder, plan):
    temp_list = []

    for i, (old, new) in enumerate(plan):
        ext = os.path.splitext(old)[1]  # get the extension of the old file
        tmp = f"temp_{i:03d}{ext}"  # create a temporary name with the same extension
        temp_list.append((old, tmp, new))  # old -> temp -> new

    for old, tmp, _ in temp_list:
        os.rename(os.path.join(folder, old), os.path.join(folder, tmp))

    for _, tmp, new in temp_list:
        os.rename(os.path.join(folder, tmp), os.path.join(folder, new))


folder = ""
plan = []

def choose_folder():
    global folder, plan
    folder = filedialog.askdirectory()

    if folder == "":
        label.config(text="No folder selected")
        plan = []
        show_preview()
        return

    plan = make_plan(folder)
    show_preview()

    if not plan:
        label.config(text="No files to rename")
        return
    label.config(text=f"Selected folder: {folder} ({len(plan)} files to rename)")

def show_preview():
    preview.delete(0, tk.END)
    for old, new in plan:
        preview.insert(tk.END, f"{old} --> {new}")

def rename_files():
    global plan
    if not plan:
        label.config(text="Choose a folder")
        return
    answer = messagebox.askyesno("Confirm Rename", f"Are you sure you want to rename {len(plan)} files?")
    if not answer:
        label.config(text="Rename cancelled")
        return
    try:
        do_rename(folder, plan)
        label.config(text=f"Renamed {len(plan)} files")
        plan = []
        show_preview()
    except OSError as e:
        messagebox.showerror("Error", f"An error occurred while renaming files: {e}")
        label.config(text="Rename failed")
        plan = make_plan(folder)
        show_preview()

window = tk.Tk()
window.title("Bulk File Renamer")
window.geometry("800x500")

label = tk.Label(window, text="Bulk File Renamer")
label.pack()

choose_folder_button = tk.Button(window, text="Choose Folder", command=choose_folder)
choose_folder_button.pack()

preview = tk.Listbox(window, width=100)
preview.pack(fill="both", expand=True)

rename_button = tk.Button(window, text="Rename Files", command=rename_files)
rename_button.pack()

window.mainloop()
