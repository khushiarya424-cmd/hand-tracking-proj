#This is the main next-step file.
#It will:
#Open videos from cam1 and cam2
#Read frames one by one
#Check if frame is in no_motion_clean.txt
#Skip no-motion frames
#Save useful frames into output/frames

import os
import cv2
from frame_filter import load_no_motion_ranges, is_no_motion_frame


def get_camera_name(video_path):
    """
    Finds whether video belongs to cam1 or cam2.
    """

    path_parts = video_path.split(os.sep)

    if "cam1" in path_parts:
        return "cam1"

    if "cam2" in path_parts:
        return "cam2"

    return "unknown_cam"


def create_safe_video_name(video_path):
    """
    Creates a safe folder name from video filename.

    Example:
    GX020084.MP4 -> GX020084
    """

    filename = os.path.basename(video_path)
    name_without_ext = os.path.splitext(filename)[0]

    return name_without_ext


def extract_useful_frames_from_video(
    video_path,
    no_motion_ranges,
    output_base_folder="output/frames",
    save_every_n_frames=30
):
    """
    Extracts useful frames from one video.

    save_every_n_frames = 30 means:
    save 1 useful frame after every 30 frames.

    This avoids saving too many images.
    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video:", video_path)
        return

    camera_name = get_camera_name(video_path)
    video_name = create_safe_video_name(video_path)

    output_folder = os.path.join(output_base_folder, camera_name, video_name)
    os.makedirs(output_folder, exist_ok=True)

    frame_number = 0
    saved_count = 0
    skipped_no_motion = 0

    print("\nProcessing video:", video_path)
    print("Saving frames to:", output_folder)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_number += 1

        # Check if frame is inside no-motion range
        if is_no_motion_frame(frame_number, no_motion_ranges):
            skipped_no_motion += 1
            continue

        # Save only every Nth useful frame
        if frame_number % save_every_n_frames != 0:
            continue

        output_filename = f"{video_name}_frame_{frame_number:06d}.jpg"
        output_path = os.path.join(output_folder, output_filename)

        cv2.imwrite(output_path, frame)
        saved_count += 1

        if saved_count % 100 == 0:
            print("Saved", saved_count, "frames so far from", video_name)

    cap.release()

    print("Finished:", video_path)
    print("Total frames read:", frame_number)
    print("No-motion frames skipped:", skipped_no_motion)
    print("Useful frames saved:", saved_count)


def extract_from_all_videos(
    videos_base_folder="videos/Saubermacher_161125",
    no_motion_file="output/metadata/no_motion_clean.txt",
    output_base_folder="output/frames",
    save_every_n_frames=30
):
    """
    Goes through cam1 and cam2 folders and extracts useful frames.
    """

    no_motion_data = load_no_motion_ranges(no_motion_file)

    video_extensions = (".mp4", ".MP4", ".avi", ".AVI", ".mov", ".MOV")

    total_videos = 0

    for root, dirs, files in os.walk(videos_base_folder):
        for file in files:
            if file.endswith(video_extensions):
                video_path = os.path.join(root, file)

                total_videos += 1

                # Get ranges for this specific video

                video_filename = os.path.basename(video_path)
                ranges = no_motion_data.get(video_filename, [])

                if len(ranges) == 0:
                    print("\nWarning: No no-motion ranges found for:")
                    print(video_path)
                    print("This video will be processed normally.")

                extract_useful_frames_from_video(
                    video_path=video_path,
                    no_motion_ranges=ranges,
                    output_base_folder=output_base_folder,
                    save_every_n_frames=save_every_n_frames
                )

    print("\nAll videos processed.")
    print("Total videos processed:", total_videos)


if __name__ == "__main__":
    extract_from_all_videos(
        videos_base_folder="/mnt/cps_scratch1_tmp/icp_project_ip6.b/videos/Saubermacher_161125",
        no_motion_file="output/metadata/no_motion_clean.txt",
        output_base_folder="output/frames",
        save_every_n_frames=30
    )