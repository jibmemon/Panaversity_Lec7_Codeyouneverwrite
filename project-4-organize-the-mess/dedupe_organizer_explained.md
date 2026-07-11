# Dedupe Organizer — How It Maps to the Spec

## Problem

Digital clutter (duplicate files, forgotten downloads, oversized files) builds up over time. This project finds and organizes it safely, without risking damage to real files.

## Initial Prompt

> I have a messy folder. Write any script that: (1) finds duplicate files based on file content, (2) flags files over 500KB, (3) groups files by type. Before doing anything, the script must run in a safe "dry run" mode by default that only prints the full plan and must NOT touch, move, rename, or delete anything unless I explicitly pass an `--execute` flag.

## Deliverable

`dedupe_organizer.py` — a single Python script, no external dependencies.

## How It Maps to the Spec, Point by Point

| Requirement | Implementation |
|---|---|
| **Dry-run by default** | Running `python3 dedupe_organizer.py /path/to/folder` only prints the full plan (duplicate sets, oversized files, type groupings). Zero disk writes. |
| **Duplicates by content, not filename** | Uses SHA-256 hashing on file contents, so files with different names/extensions but identical bytes are still correctly grouped as duplicates. |
| **Oversized flag (> 500KB)** | Configurable via `--size-threshold`. Files are flagged in a review list but still get organized normally — flagged does not mean removed. |
| **Grouped by type** | Categories: Images, Documents, Videos, Audio, Archives, Code, Other. |
| **`--execute` required to touch anything** | Without it, nothing is written. Even with it, the script only *copies* into a new `organized_output/` folder — the source folder is never moved, renamed, or deleted. |
| **Automatic backup** | Before executing, the script zips the entire source folder into the output directory (`_source_backup_<timestamp>.zip`). Disable with `--no-backup` (not recommended). |
| **Automatic verification** | After executing, the script re-hashes every original file and prints an explicit ✔ / ✘ confirmation that the source folder is unchanged — no need to remember to check by hand. |

## Usage

```bash
# Dry run (default, safe, read-only)
python3 dedupe_organizer.py /path/to/messy_folder

# Actually organize (copies into a new folder, source untouched)
python3 dedupe_organizer.py /path/to/messy_folder --execute

# Custom output folder / size threshold
python3 dedupe_organizer.py /path/to/messy_folder --execute \
    --output /path/to/organized --size-threshold 1000000
```

## Improved Prompts Applied

- Confirmed the full plan is always printed before anything runs.
- Results are written into a **new** folder rather than modifying originals.
- Added an explicit confirmation step that the original folder is unchanged after execution.

## Verification (Actually Tested, Not Just Claimed)

A synthetic messy folder was built to stress-test the logic:

- `report.txt`, `report_copy.docx`, and a copy inside a subfolder — same content, three different names/extensions/locations.
- `big_photo.jpg` — 585.9KB (oversized).
- `notes.md`, `tiny.png` — normal unique files.

**Steps taken, in the required safety order:**

1. Ran dry-run — reviewed the full plan before anything else.
2. Ran `--execute` — script created its own automatic zip backup first, then copied files into `organized_output/`.
3. Ran an **independent** `md5sum` + `diff` check outside the script, comparing every source file's hash before and after execution.

**Result:** all 6 original files were confirmed byte-for-byte identical before and after — `diff` reported no changes.

**Output folder structure produced:**

```
organized_output/
├── Documents/
│   ├── notes.md
│   └── report_copy.docx      (first copy — kept as "original")
├── Images/
│   ├── big_photo.jpg
│   └── tiny.png
├── _duplicates_for_review/
│   ├── report.txt
│   └── duplicate_in_subfolder.txt
├── _oversized_review.txt
└── _source_backup_<timestamp>.zip
```

## What Worked / What Didn't

- Hashing file **contents** (not just filenames) correctly caught duplicates that had different names but identical content — this was the core requirement and it held up under testing.
- The dry-run/execute split made the script safe by default — the script's normal behavior is always the read-only preview; nothing happens by accident.
- Adding an automatic backup + automatic post-execution verification goes beyond the original manual process and removes the chance of forgetting to check.

## Final Result

Found 1 duplicate set (3 files, same content) and 1 oversized file worth reviewing, all confirmed safe — the original folder was untouched throughout the entire process, verified independently outside the script itself.
