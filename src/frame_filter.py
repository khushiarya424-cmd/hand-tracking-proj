#This file will read "no_motion_clean.txt" and help us check Should this frame be skipped or saved?
import re
import os


def load_no_motion_ranges(no_motion_file="output/metadata/no_motion_clean.txt"):
    """
    Loads no-motion ranges from file.

    Uses only video filename as key.

    Example:
    /old/path/cam1/GX020084.MP4 no-motion-frame{100-200}

    becomes:

    {
        "GX020084.MP4": [(100, 200)]
    }
    """

    no_motion_data = {}

    if not os.path.exists(no_motion_file):
        print(f"Warning: {no_motion_file} not found")
        return no_motion_data

    with open(no_motion_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if not line:
            continue

        parts = line.split(" no-motion-frame")

        if len(parts) != 2:
            print("Skipping invalid line:", line)
            continue

        video_path = parts[0]

        video_filename = os.path.basename(video_path)

        match = re.search(r"\{(\d+)-(\d+)\}", line)

        if not match:
            print("Skipping invalid range:", line)
            continue

        start = int(match.group(1))
        end = int(match.group(2))

        if video_filename not in no_motion_data:
            no_motion_data[video_filename] = []

        no_motion_data[video_filename].append((start, end))

    print("Loaded no-motion data for", len(no_motion_data), "videos")

    return no_motion_data


def is_no_motion_frame(frame_number, ranges):
    """
    Checks if current frame number is inside any no-motion range.
    """

    for start, end in ranges:
        if start <= frame_number <= end:
            return True

    return False
