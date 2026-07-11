#!/usr/bin/env python3
"""
dedupe_organizer.py
--------------------
Scans a messy folder and:
  1. Finds duplicate files based on CONTENT (hash), not filename.
  2. Flags files over a size threshold (default 500KB) for review.
  3. Groups files by type (Images, Documents, Videos, Archives, Code, Other).

SAFE BY DEFAULT:
  - Running the script with no flags does a DRY RUN ONLY.
    It prints the full plan and touches nothing on disk.
  - Nothing is copied, moved, renamed, or deleted unless you pass --execute.
  - Even with --execute, the SOURCE folder is never modified. Everything
    organized gets COPIED into a new output folder (default: ./organized_output).
  - Before executing, a zip backup of the source folder is made automatically
    (disable with --no-backup, not recommended).
  - After executing, the script re-hashes every original file and confirms
    the source folder is byte-for-byte unchanged.

USAGE:
  Dry run (default, safe, read-only):
    python3 dedupe_organizer.py /path/to/messy_folder

  Actually organize (copies into a new folder, source untouched):
    python3 dedupe_organizer.py /path/to/messy_folder --execute

  Custom output folder / size threshold:
    python3 dedupe_organizer.py /path/to/messy_folder --execute \
        --output /path/to/organized --size-threshold 1000000
"""

import argparse
import hashlib
import os
import shutil
import sys
import zipfile
from collections import defaultdict
from datetime import datetime

TYPE_MAP = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".heic"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"},
    "Videos": {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "Code": {".py", ".js", ".html", ".css", ".json", ".java", ".c", ".cpp", ".sh", ".ipynb"},
}

def categorize(ext):
    ext = ext.lower()
    for category, exts in TYPE_MAP.items():
        if ext in exts:
            return category
    return "Other"


def hash_file(path, block_size=65536):
    """Return sha256 hash of a file's CONTENT."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_folder(source):
    """Walk the source folder (read-only) and collect metadata for every file."""
    records = []
    for root, _dirs, files in os.walk(source):
        for name in files:
            full_path = os.path.join(root, name)
            try:
                size = os.path.getsize(full_path)
                file_hash = hash_file(full_path)
            except (OSError, PermissionError) as e:
                print(f"  [!] Skipping unreadable file: {full_path} ({e})")
                continue
            ext = os.path.splitext(name)[1]
            records.append({
                "path": full_path,
                "name": name,
                "ext": ext,
                "size": size,
                "hash": file_hash,
                "category": categorize(ext),
            })
    return records


def find_duplicates(records):
    """Group files by content hash; only groups with >1 file are duplicates."""
    by_hash = defaultdict(list)
    for r in records:
        by_hash[r["hash"]].append(r)
    return {h: recs for h, recs in by_hash.items() if len(recs) > 1}


def find_oversized(records, threshold_bytes):
    return [r for r in records if r["size"] > threshold_bytes]


def human_size(n):
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def print_plan(records, duplicates, oversized, threshold_bytes, output_dir):
    print("=" * 70)
    print("DRY RUN — PLAN ONLY. Nothing on disk has been touched.")
    print("=" * 70)
    print(f"Files scanned: {len(records)}")
    print(f"Planned output folder (created only on --execute): {output_dir}\n")

    print("-" * 70)
    print(f"1) DUPLICATE SETS FOUND (by content hash): {len(duplicates)}")
    print("-" * 70)
    if not duplicates:
        print("  None found.")
    for i, (h, recs) in enumerate(duplicates.items(), 1):
        print(f"  Set {i}  (hash {h[:10]}...):")
        for r in recs:
            marker = "KEEP (first copy)" if r is recs[0] else "duplicate -> would go to _duplicates_for_review/"
            print(f"    - {r['path']}  [{human_size(r['size'])}]  {marker}")
    print()

    print("-" * 70)
    print(f"2) OVERSIZED FILES FLAGGED (> {human_size(threshold_bytes)}): {len(oversized)}")
    print("-" * 70)
    if not oversized:
        print("  None found.")
    for r in oversized:
        print(f"  - {r['path']}  [{human_size(r['size'])}]  -> flagged in _oversized_review.txt, still organized normally")
    print()

    print("-" * 70)
    print("3) GROUPING BY TYPE (planned folder structure under output folder)")
    print("-" * 70)
    by_category = defaultdict(list)
    for r in records:
        by_category[r["category"]].append(r)
    for cat, recs in sorted(by_category.items()):
        print(f"  {output_dir}/{cat}/   <- {len(recs)} file(s)")
    print()
    print("=" * 70)
    print("No files were copied, moved, renamed, or deleted.")
    print("Re-run with --execute to actually create the organized copy.")
    print("=" * 70)


def make_backup_zip(source, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(output_dir, f"_source_backup_{stamp}.zip")
    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(source):
            for name in files:
                full_path = os.path.join(root, name)
                arcname = os.path.relpath(full_path, source)
                zf.write(full_path, arcname)
    return backup_path


def execute_plan(records, duplicates, oversized, output_dir):
    """Copies files into the organized output folder. NEVER touches the source."""
    os.makedirs(output_dir, exist_ok=True)

    duplicate_paths = set()
    for recs in duplicates.values():
        for r in recs[1:]:  # everything after the first copy is a duplicate
            duplicate_paths.add(r["path"])

    dup_review_dir = os.path.join(output_dir, "_duplicates_for_review")
    copied = 0

    for r in records:
        if r["path"] in duplicate_paths:
            dest_dir = dup_review_dir
        else:
            dest_dir = os.path.join(output_dir, r["category"])
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, r["name"])
        # avoid overwriting same-named different files
        base, ext = os.path.splitext(dest_path)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = f"{base}_{counter}{ext}"
            counter += 1
        shutil.copy2(r["path"], dest_path)  # copy2 preserves metadata; source untouched
        copied += 1

    review_file = os.path.join(output_dir, "_oversized_review.txt")
    with open(review_file, "w") as f:
        f.write("Files flagged as oversized (for manual review):\n\n")
        for r in oversized:
            f.write(f"{r['path']}  [{human_size(r['size'])}]\n")

    return copied, dup_review_dir, review_file


def verify_source_unchanged(pre_hashes, source):
    """Re-hash the source folder and compare against the pre-execution snapshot."""
    post_records = scan_folder(source)
    post_hashes = {r["path"]: r["hash"] for r in post_records}

    missing = [p for p in pre_hashes if p not in post_hashes]
    changed = [p for p in pre_hashes if p in post_hashes and post_hashes[p] != pre_hashes[p]]
    added = [p for p in post_hashes if p not in pre_hashes]

    print("\n" + "=" * 70)
    print("VERIFICATION — confirming the source folder was not modified")
    print("=" * 70)
    if not missing and not changed and not added:
        print(f"✔ All {len(pre_hashes)} original files are present and byte-for-byte unchanged.")
    else:
        if missing:
            print(f"✘ {len(missing)} file(s) missing from source (unexpected!):")
            for p in missing:
                print(f"    - {p}")
        if changed:
            print(f"✘ {len(changed)} file(s) have different content than before (unexpected!):")
            for p in changed:
                print(f"    - {p}")
        if added:
            print(f"ℹ {len(added)} new file(s) appeared in source since the scan (not caused by this script).")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Find duplicates, flag oversized files, and organize by type — safely.")
    parser.add_argument("source", help="Path to the messy folder to scan")
    parser.add_argument("--execute", action="store_true", help="Actually copy/organize files. Without this flag, only a dry-run plan is printed.")
    parser.add_argument("--output", default="organized_output", help="Output folder for organized copies (default: ./organized_output)")
    parser.add_argument("--size-threshold", type=int, default=500 * 1024, help="Size in bytes above which a file is flagged (default: 500KB)")
    parser.add_argument("--no-backup", action="store_true", help="Skip the automatic zip backup before executing (not recommended)")
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(f"Error: '{args.source}' is not a valid folder.")
        sys.exit(1)

    print(f"Scanning: {args.source}\n")
    records = scan_folder(args.source)
    duplicates = find_duplicates(records)
    oversized = find_oversized(records, args.size_threshold)

    if not args.execute:
        print_plan(records, duplicates, oversized, args.size_threshold, args.output)
        return

    # --execute path
    pre_hashes = {r["path"]: r["hash"] for r in records}

    print_plan(records, duplicates, oversized, args.size_threshold, args.output)
    print("\n>>> --execute flag detected. Proceeding to organize a COPY. Source folder will not be touched. <<<\n")

    if not args.no_backup:
        backup_path = make_backup_zip(args.source, args.output)
        print(f"Backup created: {backup_path}\n")

    copied, dup_dir, review_file = execute_plan(records, duplicates, oversized, args.output)
    print(f"Done. {copied} file(s) copied into: {args.output}")
    print(f"  Duplicates set aside for your review in: {dup_dir}")
    print(f"  Oversized file list written to: {review_file}")

    verify_source_unchanged(pre_hashes, args.source)


if __name__ == "__main__":
    main()
