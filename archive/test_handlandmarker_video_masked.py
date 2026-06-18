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
    min_hand_detection_confidence=0.3,
    min_tracking_confidence=0.3
)

landmarker = HandLandmarker.create_from_options(options)

# -----------------------------
# Video
# -----------------------------

video_path = "/mnt/cps_scratch1_tmp/icp_project_ip6.b/videos/Saubermacher_161125/cam2/GL020084.LRV"

cap = cv2.VideoCapture(video_path)

frame_id = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_id += 1

    # -----------------------------
    # HSV Blue Glove Mask
    # -----------------------------

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = (90, 50, 50)
    upper_blue = (140, 255, 255)

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    glove_only = cv2.bitwise_and(
        frame,
        frame,
        mask=mask
    )

    # -----------------------------
    # MediaPipe
    # -----------------------------

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))

    result = landmarker.detect_for_video(
        mp_image,
        timestamp_ms
    )

    print("Detected hands:", len(result.hand_landmarks))

    # -----------------------------
    # Draw landmarks
    # -----------------------------

    if result.hand_landmarks:

        cv2.putText(
            frame,
            f"Hands: {len(result.hand_landmarks)}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        for hand in result.hand_landmarks:

            for landmark in hand:

                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])

                cv2.circle(
                    frame,
                    (x, y),
                    3,
                    (0, 255, 0),
                    -1
                )

    cv2.imshow("Hand Tracking", frame)

    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
landmarker.close()