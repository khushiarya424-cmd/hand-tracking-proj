import os
from frame_filter import load_no_motion_ranges
from extract_useful_frames import extract_useful_frames_from_video


video_path = "/mnt/cps_scratch1_tmp/icp_project_ip6.b/videos/Saubermacher_161125/cam1/GX020084.MP4"


no_motion_data = load_no_motion_ranges("output/metadata/no_motion_clean.txt")

video_filename = os.path.basename(video_path)
ranges = no_motion_data.get(video_filename, [])

print("Video:", video_path)
print("No-motion ranges found:", len(ranges))

extract_useful_frames_from_video(
    video_path=video_path,
    no_motion_ranges=ranges,
    output_base_folder="output/frames_test",
    save_every_n_frames=30
)