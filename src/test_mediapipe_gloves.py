import cv2
import mediapipe as mp

# Load MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Read image
image_path = "/home/cpsstudent/icp_project/output/frames/cam1/cam1_20251118_151020/cam1_20251118_151020_frame_005430.jpg"

image = cv2.imread(image_path)

if image is None:
    print("Could not load image")
    exit()


# so the hand becomes larger
image = cv2.resize(image, None, fx=2, fy=2)
# Convert BGR -> RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Create detector
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5
) as hands:

    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:

        print("Hand detected!")

        for hand_landmarks in results.multi_hand_landmarks:

            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    else:
        print("No hand detected")

cv2.imshow("MediaPipe Hand Detection", image)

cv2.waitKey(0)
cv2.destroyAllWindows()