import os
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge as MplWedge
import matplotlib


def get_folder_size(path: str) -> int:
    """Recursively calculate the total size of a folder in bytes."""
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += get_folder_size(entry.path)
            except OSError:
                pass
    return total


def format_size(size_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes //= 1024
    return f"{size_bytes:.1f} PB"


def main():
    if len(sys.argv) > 1:
        parent = sys.argv[1]
    else:
        parent = input("Enter the parent folder path: ").strip().strip('"')

    if not os.path.isdir(parent):
        print(f"Error: '{parent}' is not a valid directory.")
        sys.exit(1)

    folders = [
        entry.name
        for entry in os.scandir(parent)
        if entry.is_dir(follow_symlinks=False)
    ]

    if not folders:
        print("No subfolders found in the specified directory.")
        sys.exit(0)

    print(f"\nCalculating sizes for {len(folders)} folder(s) in '{parent}'...")
    sizes = {}
    for name in sorted(folders):
        path = os.path.join(parent, name)
        size = get_folder_size(path)
        sizes[name] = size
        print(f"  {name}: {format_size(size)}")

    # Filter out empty folders for the chart
    non_empty = {k: v for k, v in sizes.items() if v > 0}
    if not non_empty:
        print("\nAll folders are empty — nothing to chart.")
        sys.exit(0)

    labels = list(non_empty.keys())
    values = list(non_empty.values())

    total = sum(values)

    def autopct(pct):
        if pct <= 2:
            return ""
        size = total * pct / 100
        return f"{format_size(size)}\n{pct:.1f}%"

    fig, ax = plt.subplots(figsize=(10, 7))
    pie_result = ax.pie(
        values,
        labels=None,
        autopct=autopct,
        startangle=140,
        pctdistance=0.75,
    )
    wedges = pie_result[0]
    autotexts = pie_result[2] if len(pie_result) > 2 else []

    for at in autotexts:
        at.set_fontsize(8)

    # Legend with size labels and percentage
    legend_labels = [
        f"{name}  ({format_size(sz)},  {sz / total * 100:.1f}%)"
        for name, sz in zip(labels, values)
    ]
    ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9)

    ax.set_title(
        f"Folder sizes in: {parent}\nTotal: {format_size(total)}",
        pad=20,
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
