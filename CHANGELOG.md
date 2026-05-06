# Changelog

## v2.1.0
- Added delete-aware two-way sync via `sync_state.json`
- Deletions on LC recycle the IC copy tagged `_LC_DDMM_HHMM`
- Deletions on IC recycle the LC copy tagged `_IC_DDMM_HHMM`
- Latest timestamp always wins on conflict
- Overwritten file moves to recycle before being replaced

## v2.0.0
- Complete rewrite from ground up
- True two-way sync between Local Folder (LF) and iCloud Folder (IC)
- `_recycle_bin` folder in LF replaces hard deletes
- Auto-purge recycle bin files older than 14 days via `send2trash`
- iCloud cloud-only file detection using Windows file attributes
- Python wrapper launches Obsidian, syncs before open and after close
- Dark theme log panel with colour-coded sync events
- Settings window with four paths: LF, IC, Obsidian.exe, Backup
- Backup zips LF to timestamped archive

## v1.0.0
- One-way sync from D Drive to iCloud
- Scan preview before sync executes
- Fetch iOS notes from `Ios_notes` folder to `Inbox`
- Backup to zip
- Settings: Source, Destination, Backup paths
