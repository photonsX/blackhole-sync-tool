# Blackhole Sync Tool

A lightweight desktop sync tool for Obsidian users who work across **Windows PC** and **iPhone via iCloud**.

---

## How It Works

```
iPhone (Obsidian iOS)
    ↓ auto
iCloud cloud
    ↓ auto
iCloud Windows Folder (IC)
    ↕ this app
D Drive Local Folder (LF)
```

The app manages the **IC ↔ LF** sync. Everything above is handled automatically by iCloud.

---

## Features

- **Two-way sync** — latest timestamp wins, both directions
- **Delete awareness** — deletions on either side move the other copy to `_recycle_bin`, never lost silently
- **Recycle bin** — files named `FileName_LC_DDMM_HHMM.ext.bkp` or `FileName_IC_DDMM_HHMM.ext.bkp`
- **Auto-purge** — recycle bin files older than 14 days sent to Windows Recycle Bin
- **iCloud file check** — skips cloud-only placeholder files not yet downloaded
- **Obsidian launcher** — syncs before opening, syncs again after close
- **Backup** — zips LF to timestamped archive

---

## Usage

1. Run `Blackhole Sync tool_v02.exe`
2. Open **Settings** and set all four paths
3. Press **▶ Launch Obsidian** to start your session
4. Work normally in Obsidian
5. Close Obsidian — app auto-syncs and exits

**▶ Launch Obsidian** — pre-session sync → opens Obsidian → post-session sync on close

**⟳ Sync Now** — manual sync without opening Obsidian

---

## First Run

On first run `sync_state.json` does not exist. The app performs a full two-way sync and writes the state file. No deletions are processed on first run. This is safe.

---

## Excluded Folders

These folders are never touched by sync:

| Folder | Reason |
|---|---|
| `.obsidian` | Obsidian app data |
| `_recycle_bin` | Recycle bin lives in LF only, never synced to IC |

---

## Files Created at Runtime

| File | Purpose |
|---|---|
| `config.json` | Saved paths and settings |
| `sync_state.json` | Delete log — records all known files after each sync |

Both files live next to `Blackhole Sync tool_v02.exe`. Keep `Blackhole Sync tool_v02.exe` in a permanent folder.

---

## Requirements

**Python (if running from source):**
```
pip install send2trash
pip install pyinstaller
```

**Build exe:**
```
python -m PyInstaller --onefile --windowed --icon=icon.ico main.py
```

---

## Prerequisites

- Windows 10 / 11
- iCloud for Windows installed with **"Always keep on this device"** enabled on the blackhole folder
- Windows Time Sync enabled (Settings → Time & Language → Sync now)

> **Important:** Windows clock must be accurate. Sync decisions are based on file modification timestamps. Clock drift between devices will cause wrong-file-wins errors. Enable automatic time sync and verify before first use.

---

## Recycle Bin Naming

```
ideas_LC_0605_1430.md.bkp   ← deleted from LC, IC copy recycled
ideas_IC_0605_1430.md.bkp   ← deleted from IC, LC copy recycled
```

- `LC` — deletion originated on Local Folder (PC)
- `IC` — deletion originated on iCloud Folder (iPhone)
- Format: `DDMM_HHMM` (24-hour)

---

## Developed By

Ankit Sharma — built with [Claude](https://claude.ai) (Anthropic)
