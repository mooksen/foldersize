# Usage: python compare_folders.py <folder1> <folder2> [--only folder1|folder2]
# This script compares two folders and reports differences in their contents. It checks for files that exist only in one folder, files that exist in both but differ in content, and can optionally show only files exclusive to one folder along with their sizes.

import os
import hashlib
import argparse
from pathlib import Path


def file_hash(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def get_relative_files(folder: str) -> set:
    base = Path(folder)
    return {str(p.relative_to(base)) for p in base.rglob("*") if p.is_file()}


def human_size(nbytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if nbytes < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} PB"


def compare_folders(folder1: str, folder2: str):
    files1 = get_relative_files(folder1)
    files2 = get_relative_files(folder2)

    results = []

    for rel in sorted(files1 | files2):
        p1 = Path(folder1) / rel
        p2 = Path(folder2) / rel

        if p1.exists() and p2.exists():
            if file_hash(str(p1)) != file_hash(str(p2)):
                results.append((rel, "Both (different)", None))
        elif p1.exists():
            results.append((rel, "Folder1 only", p1.stat().st_size))
        else:
            results.append((rel, "Folder2 only", p2.stat().st_size))

    return results


def main():
    parser = argparse.ArgumentParser(description="Compare two folders and report differences.")
    parser.add_argument("folder1", help="Path to folder 1")
    parser.add_argument("folder2", help="Path to folder 2")
    parser.add_argument(
        "--only",
        choices=["folder1", "folder2"],
        help="Show only files that exist exclusively in the specified folder, with their sizes.",
    )
    args = parser.parse_args()

    results = compare_folders(args.folder1, args.folder2)

    if args.only:
        label = "Folder1 only" if args.only == "folder1" else "Folder2 only"
        results = [(rel, status, size) for rel, status, size in results if status == label]

    if not results:
        print("No differences found.")
        return

    col_width = max(len(r[0]) for r in results) + 2
    show_size = args.only is not None
    header = f"{'File':<{col_width}}  {'Size':<12}  Status" if show_size else f"{'File':<{col_width}}  Status"
    print(header)
    print("-" * (col_width + (30 if show_size else 20)))
    for rel, status, size in results:
        if show_size:
            print(f"{rel:<{col_width}}  {human_size(size):<12}  {status}")
        else:
            print(f"{rel:<{col_width}}  {status}")

    if show_size:
        total = sum(size for _, _, size in results if size is not None)
        print("-" * (col_width + 30))
        print(f"{'Total':<{col_width}}  {human_size(total):<12}  ({len(results)} files)")
    else:
        only1 = sum(1 for _, status, _ in results if status == "Folder1 only")
        only2 = sum(1 for _, status, _ in results if status == "Folder2 only")
        print("-" * (col_width + 20))
        print(f"Folder1 only: {only1} file(s)   Folder2 only: {only2} file(s)   Both (different): {len(results) - only1 - only2} file(s)")


if __name__ == "__main__":
    main()
