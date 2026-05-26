#This file will remove very tiny no-motion ranges.

import re
import os


def clean_no_motion_file(
    input_file="output/metadata/no_motion.txt",
    output_file="output/metadata/no_motion_clean.txt",
    min_length=30
):
    """
    Reads no_motion.txt and removes very small no-motion ranges.

    Example line:
    /path/video.mp4 no-motion-frame{985-1001}

    If range length is smaller than min_length, we ignore it.
    """

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        return

    cleaned_lines = []
    total_ranges = 0
    kept_ranges = 0
    removed_ranges = 0

    with open(input_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if not line:
            continue

        total_ranges += 1

        # Find frame range inside {start-end}
        match = re.search(r"\{(\d+)-(\d+)\}", line)

        if not match:
            print("Skipping invalid line:", line)
            continue

        start = int(match.group(1))
        end = int(match.group(2))

        length = end - start + 1

        if length >= min_length:
            cleaned_lines.append(line)
            kept_ranges += 1
        else:
            removed_ranges += 1

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as f:
        for line in cleaned_lines:
            f.write(line + "\n")

    print("Cleaning completed.")
    print("Total ranges:", total_ranges)
    print("Kept ranges:", kept_ranges)
    print("Removed small ranges:", removed_ranges)
    print("Saved cleaned file to:", output_file)


if __name__ == "__main__":
    clean_no_motion_file()

#calculates how many frames are in that no-motion range.
#If length is at least 30 frames, it keeps it.
#If it is less than 30, it removes it.