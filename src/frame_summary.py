import os


def count_frames(base_folder="output/frames"):

    total_frames = 0
    cam1_frames = 0
    cam2_frames = 0
    total_videos = 0

    for root, dirs, files in os.walk(base_folder):

        jpg_files = [f for f in files if f.endswith(".jpg")]

        if len(jpg_files) > 0:
            total_videos += 1

        total_frames += len(jpg_files)

        if "cam1" in root:
            cam1_frames += len(jpg_files)

        if "cam2" in root:
            cam2_frames += len(jpg_files)

    print("\n========== FRAME SUMMARY ==========")
    print("Total videos processed:", total_videos)
    print("Total extracted frames:", total_frames)
    print("Frames from cam1:", cam1_frames)
    print("Frames from cam2:", cam2_frames)
    print("===================================\n")


if __name__ == "__main__":
    count_frames()