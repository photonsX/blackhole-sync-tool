import os
import shutil
import json
import zipfile
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

CONFIG_FILE = "config.json"
APP_VERSION = "v1.0.0"

# ---------------- CONFIG ----------------
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"source": "", "dest": "", "backup": ""}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

config = load_config()

# ---------------- GLOBAL STATE ----------------
scan_done = False
scan_results = {"copy": [], "delete": []}

# ---------------- HELPERS ----------------
def is_excluded(path):
    parts = path.split(os.sep)
    return ".obsidian" in parts or "Ios_notes" in parts

def log(msg):
    panel.insert(tk.END, msg + "\n")
    panel.see(tk.END)

# ---------------- SCAN LOGIC ----------------
def scan_diff(src, dst):
    to_copy = []
    to_delete = []

    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in [".obsidian", "Ios_notes"]]

        rel = os.path.relpath(root, src)
        dest_root = os.path.join(dst, rel)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_root, file)

            if not os.path.exists(dst_file):
                to_copy.append(src_file)
            else:
                if os.path.getmtime(src_file) > os.path.getmtime(dst_file):
                    to_copy.append(src_file)

    for root, dirs, files in os.walk(dst):
        dirs[:] = [d for d in dirs if d not in [".obsidian", "Ios_notes"]]

        rel = os.path.relpath(root, dst)
        src_root = os.path.join(src, rel)

        for file in files:
            dst_file = os.path.join(root, file)
            src_file = os.path.join(src_root, file)

            if not os.path.exists(src_file):
                to_delete.append(dst_file)

    return to_copy, to_delete

# ---------------- SYNC ----------------
def perform_sync_from_scan():
    src = config["source"]
    dst = config["dest"]

    to_copy = scan_results["copy"]
    to_delete = scan_results["delete"]

    if not to_copy and not to_delete:
        log("Nothing to sync")
        return

    for file in to_copy:
        rel = os.path.relpath(file, src)
        dest_file = os.path.join(dst, rel)

        if is_excluded(dest_file):
            continue

        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        shutil.copy2(file, dest_file)
        log(f"Copied: {rel}")

    for file in to_delete:
        if is_excluded(file):
            continue

        if os.path.exists(file):
            os.remove(file)
            log(f"Deleted: {file}")

    log("✅ Sync Completed")

# ---------------- BACKUP ----------------
def backup_source():
    src = config["source"]
    backup_path = config["backup"]

    if not os.path.exists(src):
        messagebox.showerror("Error", "Invalid Source Path")
        return

    name = "backup_" + datetime.now().strftime("%Y-%m-%d_%H-%M") + ".zip"
    zip_path = os.path.join(backup_path, name)

    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_STORED) as z:
        for root, dirs, files in os.walk(src):
            for file in files:
                full = os.path.join(root, file)
                rel = os.path.relpath(full, src)
                z.write(full, rel)

    log(f"Backup created: {name}")

# ---------------- FETCH IOS ----------------
def fetch_ios():
    ios_path = os.path.join(config["dest"], "Ios_notes")
    inbox_path = os.path.join(config["source"], "Inbox")

    panel.delete(1.0, tk.END)

    if not os.path.exists(ios_path):
        log("Ios_notes folder not found")
        return

    files = os.listdir(ios_path)

    if not files:
        log("Nothing to fetch")
        return

    os.makedirs(inbox_path, exist_ok=True)

    copied_files = []

    for file in files:
        src_file = os.path.join(ios_path, file)
        dst_file = os.path.join(inbox_path, file)

        copy = True

        if os.path.exists(dst_file):
            if os.path.getmtime(dst_file) > os.path.getmtime(src_file):
                copy = False

        if copy:
            shutil.copy2(src_file, dst_file)

            if os.path.exists(dst_file):
                os.remove(src_file)
                copied_files.append(file)

    if copied_files:
        log("Fetched files:")
        for f in copied_files:
            log(f"✔ {f}")
        log(f"\nTotal files fetched: {len(copied_files)}")
    else:
        log("No files were copied (all up-to-date)")

    log("✅ Fetch Completed")

# ---------------- BUTTON LOGIC ----------------
def scan_or_sync():
    global scan_done, scan_results

    if not config["source"] or not config["dest"]:
        messagebox.showerror("Error", "Please set paths in settings")
        return

    if not scan_done:
        to_copy, to_delete = scan_diff(config["source"], config["dest"])

        scan_results["copy"] = to_copy
        scan_results["delete"] = to_delete

        panel.delete(1.0, tk.END)

        if not to_copy and not to_delete:
            log("✅ Everything already in sync")
            scan_done = False
            sync_btn.config(text="Scan")
            return

        log("FILES TO COPY:")
        for f in to_copy:
            log(f)

        log("\nFILES TO DELETE:")
        for f in to_delete:
            log(f)

        scan_done = True
        sync_btn.config(text="Sync")

    else:
        perform_sync_from_scan()
        scan_done = False
        sync_btn.config(text="Scan")

# ---------------- SETTINGS UI ----------------
def open_settings():
    win = tk.Toplevel(root)
    win.title("Settings")

    def browse(var):
        path = filedialog.askdirectory()
        if path:
            var.set(path)

    src_var = tk.StringVar(value=config["source"])
    dst_var = tk.StringVar(value=config["dest"])
    bkp_var = tk.StringVar(value=config["backup"])

    for label, var in [("Source", src_var), ("Destination", dst_var), ("Backup", bkp_var)]:
        frame = tk.Frame(win)
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text=label, width=12).pack(side="left")
        tk.Entry(frame, textvariable=var, width=40).pack(side="left")
        tk.Button(frame, text="Browse", command=lambda v=var: browse(v)).pack(side="left")

    def save():
        config["source"] = src_var.get()
        config["dest"] = dst_var.get()
        config["backup"] = bkp_var.get()

        save_config(config)
        messagebox.showinfo("Saved", "Settings Saved")
        win.destroy()

    tk.Button(win, text="Save", command=save).pack(pady=10)

# ---------------- ABOUT ----------------
def open_about():
    messagebox.showinfo(
        "About",
        f"Blackhole Sync Tool {APP_VERSION}\n\n"
        "Developed by Ankit Sharma\n"
        "with assistance from ChatGPT Go"
    )

# ---------------- UI ----------------
root = tk.Tk()
root.title(f"Blackhole Sync Tool {APP_VERSION}")
root.geometry("800x500")

top_frame = tk.Frame(root)
top_frame.pack(fill="x")

tk.Button(top_frame, text="⚙ Settings", command=open_settings).pack(side="left", padx=5, pady=5)
tk.Button(top_frame, text="ℹ About", command=open_about).pack(side="left", padx=5)

sync_btn = tk.Button(top_frame, text="Scan", command=scan_or_sync)
sync_btn.pack(side="left", padx=5)

tk.Button(top_frame, text="Backup", command=backup_source).pack(side="left", padx=5)
tk.Button(top_frame, text="Fetch iOS Data", command=fetch_ios).pack(side="left", padx=5)

panel = tk.Text(root)
panel.pack(fill="both", expand=True)

root.mainloop()