import os
from read_video import play_video

print("Starting code...")

base_folder = "/mnt/cps_scratch1_tmp/icp_project_ip6.b/videos/Saubermacher_161125"

for root, dirs, files in os.walk(base_folder):

    for file in files:

        if file.endswith(".MP4") or file.endswith(".mp4"):

            video_path = os.path.join(root, file)

            print("\nProcessing:", video_path)

            play_video(video_path)