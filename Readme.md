# Blackhole Sync Tool

A lightweight local sync tool designed to work with Obsidian vaults using iCloud — without requiring Obsidian Sync.

---

## 🚀 Why this tool exists

Obsidian Sync is a paid feature.
For small note libraries, a full subscription may not feel necessary.

This tool provides a simple alternative:

* Use iCloud for basic file sync
* Use this tool to control *what actually syncs*

---

## 🧠 Core Idea

* Your **main vault lives locally (PC)**
* iCloud acts as a **mirror / transport layer**
* This tool manages **controlled sync between them**

---

## 📁 Folder Logic

### On PC (Local Vault)

* Main working vault
* Obsidian runs from here
* New notes go into: `Inbox`

### On iPhone (iCloud Vault)

* Synced via iCloud
* New notes go into: `Ios_notes`

---

## 🔁 Sync Rules

### Part 1 — Scan / Sync (Local → iCloud)

* Compares local and iCloud folders
* Copies:

  * New files
  * Modified files
* Deletes:

  * Files in iCloud not present locally
* Preserves folder structure

### ❗ Exclusions (Important)

The following folders are **never touched**:

* `.obsidian`
* `Ios_notes`

They are:

* not scanned
* not synced
* not deleted

---

### Part 2 — Fetch iOS Notes (iCloud → Local)

* Scans `Ios_notes` folder in iCloud
* Copies files to local `Inbox`
* Verifies successful copy
* Deletes from iCloud after success

#### Conflict Handling

* If file exists in both:

  * Newer file **overwrites older one**

---

### Part 3 — Backup

* Creates a ZIP backup of the local vault
* Uses **no compression (fastest)**
* Saved with date/time naming

---

## 🖥️ Features

* Scan before sync (safe workflow)
* Clear preview of:

  * Files to copy
  * Files to delete
* One-click sync
* iOS note ingestion system
* Fast backup system
* Simple UI

---

## ⚙️ How It Works (Workflow)

1. Write notes on PC → saved in `Inbox`
2. Sync → pushed to iCloud
3. Write notes on iPhone → saved in `Ios_notes`
4. Use **Fetch iOS Data**
5. Notes move to local `Inbox`
6. Next sync distributes them properly

---

## 📌 Important Notes

* This tool is designed for **personal workflows**
* Not intended as a full replacement for Obsidian Sync
* Always keep backups (use built-in backup feature)

---

## 🧩 Requirements

* Windows 10/11
* iCloud for Windows
* Obsidian installed

---

## 📦 Build

This project can be converted into an `.exe` using PyInstaller.

---

## 💬 About

Developed by Ankit Sharma
with assistance from ChatGPT Go

---

## 🪪 License

Free to use for personal workflows
