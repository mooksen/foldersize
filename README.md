# foldersize

Visualise how disk space is distributed across the immediate subfolders of any directory.
The script recursively measures each subfolder's total size, prints a summary to the terminal, and displays an interactive pie chart.

## Features

- Prompts for a folder path at startup (or accepts it as a command-line argument)
- Recursively calculates the size of every subfolder
- Prints a human-readable size summary (B / KB / MB / GB / TB) to the terminal
- Renders a pie chart where each wedge shows the size and percentage of the total
- A legend lists every folder with its size and share of the total
- Gracefully skips inaccessible paths (permission errors, Windows MAX_PATH limits)

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) **or** pip

## Installation

```bash
# Clone / navigate to the project folder, then:
uv sync
```

Or with pip:

```bash
pip install matplotlib
```

## Usage

### Interactive (prompted)

```bash
uv run main.py
```

You will be asked to enter a folder path:

```
Enter the parent folder path: C:\Users\You\Projects
```

### Pass the path as an argument

```bash
uv run main.py "C:\Users\You\Projects"
```

## Example output

Terminal:

```
Calculating sizes for 5 folder(s) in 'C:\Users\You\Projects'...
  .git: 2.8 GB
  .venv: 700.8 MB
  docs: 377.5 MB
  src: 109.1 MB
  tests: 35.5 KB
```

A pie chart window then opens showing each folder as a wedge labelled with its size and percentage.
Wedges smaller than 2 % of the total are unlabelled on the chart to avoid clutter but still appear in the legend.
