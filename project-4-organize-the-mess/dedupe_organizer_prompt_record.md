# Prompt Record — Digital Clutter Organizer

**Date logged:** 2026-07-11

## Problem

Digital clutter (duplicate files, forgotten downloads, oversized files) builds up over time. This project finds and organizes it safely, without risking damage to real files.

## Initial Prompt

> I have a messy folder. Write any script that: (1) finds duplicate files based on file content, (2) flags files over 500KB, (3) groups files by type. Before doing anything, the script must run in a safe "dry run" mode by default that only prints the full plan and must NOT touch, move, rename, or delete anything unless I explicitly pass an `--execute` flag.

## Improved Prompts

- Asked it to confirm the plan was shown in full before anything ran.
- Asked it to write results into a new folder rather than modifying originals.
- Asked for confirmation that the original folder was unchanged after execution.

## Verification

Followed the required safety order exactly: made a full backup of the folder before running anything, reviewed the complete dry-run plan, and only then approved execution. Afterward, manually confirmed all original files were still present, unchanged, in the source folder.

## What Worked / What Didn't

Hashing file contents (not just filenames) correctly caught duplicates that had different names but identical content. The dry-run/execute split made it safe by default — the script's normal behavior is always the read-only preview.

## Final Result

Found 3 sets of duplicate files and one oversized file worth reviewing, all confirmed safe — the original folder was untouched throughout the entire process.

## Deliverables Produced

| File | Purpose |
|---|---|
| `dedupe_organizer.py` | The script: content-hash duplicate detection, oversized flagging, type grouping, dry-run default, `--execute` flag, automatic backup, automatic post-run verification |
| `dedupe_organizer_explained.md` | Point-by-point mapping of the script to this spec, usage instructions, and actual test results |

## Possible Next Steps (for chaining in a future session)

- Point the script at the real messy folder and review the actual dry-run plan before executing.
- Decide what to do with the `_duplicates_for_review` folder (delete manually, archive, etc. — the script never auto-deletes).
- Consider adding a scheduled/recurring run (e.g. weekly) if clutter builds up continuously.
- Consider adding an option to skip system/hidden files or exclude specific subfolders.
