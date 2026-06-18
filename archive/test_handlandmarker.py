import cv2
import mediapipe as mp

# -----------------------------
# Load image
# -----------------------------

image_path = "/home/cpsstudent/icp_project/output/frames/cam1/GX010084/GX010084_frame_000030.jpg"

image = cv2.imread(image_path)

if image is None:
    print("Could not load image")
    exit()

# enlarge image a bit
image = cv2.resize(image, None, fx=2, fy=2)

# convert BGR -> RGB
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# -----------------------------
# Create MediaPipe Image
# -----------------------------

mp_image = mp.Image(
    image_format=mp.ImageFormat.SRGB,
    data=rgb_image
)

# -----------------------------
# Create Hand Landmarker
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
# Run detection
# -----------------------------

with HandLandmarker.create_from_options(options) as landmarker:

    result = landmarker.detect(mp_image)

    print("\nHands detected:", len(result.hand_landmarks))

    for i, hand_landmarks in enumerate(result.hand_landmarks):

        print(f"\nHand {i+1}")

        if i < len(result.handedness):
            print(
                "Handedness:",
                result.handedness[i][0].category_name,
                "Confidence:",
                result.handedness[i][0].score
            )

        # draw landmarks
        for landmark in hand_landmarks:

            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])

            cv2.circle(image, (x, y), 4, (0, 255, 0), -1)

# -----------------------------
# Show result
# -----------------------------

cv2.imshow("Hand Landmarker", image)
cv2.waitKey(0)
cv2.destroyAllWindows()