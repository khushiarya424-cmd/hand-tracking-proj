# hand-tracking-proj
# Industrial Video Preprocessing and Frame Extraction Pipeline
## Project Overview

This project processes industrial surveillance videos from two cameras (`cam1` and `cam2`) to reduce unnecessary data and prepare useful frames for further computer vision analysis such as object detection, hand detection, or worker activity analysis.

The pipeline performs:

1. Motion analysis on videos
2. Detection of low-motion (no-motion) frame ranges
3. Cleaning of noisy no-motion metadata
4. Extraction of useful frames only
5. Preparation for YOLO-based detection

# Project Pipeline

RAW VIDEOS
↓
Motion Analysis
↓
no_motion.txt
↓
Metadata Cleaning
↓
no_motion_clean.txt
↓
Frame Filtering
↓
Useful Frame Extraction
↓
output/frames/
↓
YOLO Detection (next stage)

# Folder Structure
```text
project/
│
├── src/
│   ├── main.py
│   ├── read_video.py
│   ├── clean_no_motion.py
│   ├── frame_filter.py
│   ├── extract_useful_frames.py
│   ├── test_extract_one_video.py
│
├── output/
│   ├── metadata/
│   │   ├── no_motion_clean.txt
│   │
│   ├── frames/
│   │   ├── cam1/
│   │   └── cam2/
│
├── videos/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# File Descriptions

## main.py
Iterates through all videos and sends them for motion analysis.

## read_video.py
Reads videos frame-by-frame using OpenCV and detects low-motion frame ranges.

## clean_no_motion.py
Removes tiny/noisy no-motion ranges and creates cleaned metadata.

## frame_filter.py
Loads cleaned metadata and checks whether a frame should be skipped.

## extract_useful_frames.py
Extracts useful frames while skipping no-motion ranges.

## test_extract_one_video.py
Tests frame extraction on a single video before processing all videos.

# Technologies Used

- Python
- OpenCV
- NumPy
- YOLO (next stage)

---

# Current Status

✔ Motion analysis completed  
✔ No-motion metadata generated  
✔ Metadata cleaned  
✔ Useful frame extraction completed  
⬜ YOLO detection pipeline  
⬜ Detection analysis and visualization  

---

# Future Work

- YOLO-based worker/object detection
- Hand detection
- Activity analysis
- Safety monitoring
- Multi-camera synchronization

---

# Author

Khushi Arya
