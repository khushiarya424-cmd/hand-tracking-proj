import cv2
import mediapipe as mp

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
    running_mode=VisionRunningMode.VIDEO,
    num_hands=4,
    min_hand_detection_confidence=0.03,
    min_hand_presence_confidence=0.03,
    min_tracking_confidence=0.03
)

# -----------------------------
# Video path
# -----------------------------

video_path = "/mnt/cps_scratch1_tmp/icp_project_ip6.b/videos/Saubermacher_161125/cam2/GL020084.LRV"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Could not open video")
    exit()

# -----------------------------
# Hand detector
# -----------------------------

with HandLandmarker.create_from_options(options) as landmarker:

    frame_number = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_number += 1

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        timestamp_ms = frame_number * 33

        result = landmarker.detect_for_video(
            mp_image,
            timestamp_ms
        )

        # Draw landmarks
        for hand_landmarks in result.hand_landmarks:

            for landmark in hand_landmarks:

                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])

                cv2.circle(
                    frame,
                    (x, y),
                    3,
                    (0, 255, 0),
                    -1
                )

        cv2.putText(
            frame,
            f"Hands: {len(result.hand_landmarks)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("Hand Landmarker Video", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()