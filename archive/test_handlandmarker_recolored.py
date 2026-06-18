import cv2
import mediapipe as mp
import numpy as np

# -----------------------------
# Load image
# -----------------------------

image_path = "/home/cpsstudent/icp_project/output/frames/cam1/GX010084/GX010084_frame_000450.jpg"

image = cv2.imread(image_path)

if image is None:
    print("Could not load image")
    exit()

# Make image larger
image = cv2.resize(image, None, fx=2, fy=2)

# -----------------------------
# Convert blue gloves -> orange
# -----------------------------

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Blue glove range
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([140, 255, 255])

mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Change blue hue to orange hue
hsv_recolored = hsv.copy()

# OpenCV hue:
# Blue ≈ 120
# Orange/Skin ≈ 15-25

hsv_recolored[:, :, 0][mask > 0] = 20

# Slightly reduce saturation
hsv_recolored[:, :, 1][mask > 0] = 120

recolored = cv2.cvtColor(
    hsv_recolored,
    cv2.COLOR_HSV2BGR
)

# -----------------------------
# MediaPipe setup
# -----------------------------

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="models/hand_landmarker.task"
    ),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=8,
    min_hand_detection_confidence=0.05,
    min_hand_presence_confidence=0.05
)

# -----------------------------
# Run detector
# -----------------------------

rgb = cv2.cvtColor(
    recolored,
    cv2.COLOR_BGR2RGB
)

mp_image = mp.Image(
    image_format=mp.ImageFormat.SRGB,
    data=rgb
)

with HandLandmarker.create_from_options(options) as landmarker:

    result = landmarker.detect(mp_image)

    print("\nHands detected:", len(result.hand_landmarks))

    for hand in result.hand_landmarks:

        for landmark in hand:

            x = int(
                landmark.x * recolored.shape[1]
            )

            y = int(
                landmark.y * recolored.shape[0]
            )

            cv2.circle(
                recolored,
                (x, y),
                4,
                (0, 255, 0),
                -1
            )

# -----------------------------
# Show images
# -----------------------------

cv2.imshow("Original", image)
cv2.imshow("Recolored Gloves", recolored)

cv2.waitKey(0)
cv2.destroyAllWindows()