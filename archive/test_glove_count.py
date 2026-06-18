import cv2
import numpy as np

# -----------------------------
# Load image
# -----------------------------

image_path = "/home/cpsstudent/icp_project/output/frames/cam1/GX020084/GX020084_frame_001980.jpg"

image = cv2.imread(image_path)

if image is None:
    print("Could not load image")
    exit()

# -----------------------------
# Convert to HSV
# -----------------------------

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Blue glove range
lower_blue = np.array([80, 30, 30])
upper_blue = np.array([150, 255, 255])

mask = cv2.inRange(
    hsv,
    lower_blue,
    upper_blue
)

# -----------------------------
# Remove noise
# -----------------------------

kernel = np.ones((5, 5), np.uint8)

mask = cv2.morphologyEx(
    mask,
    cv2.MORPH_OPEN,
    kernel
)

mask = cv2.morphologyEx(
    mask,
    cv2.MORPH_CLOSE,
    kernel
)

# -----------------------------
# Find connected components
# -----------------------------

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)

glove_count = 0

for i in range(1, num_labels):  # skip background

    area = stats[i, cv2.CC_STAT_AREA]

    # Ignore tiny blobs
    if area < 5000:
        continue

    glove_count += 1

    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]

    ratio=w/h
    if ratio < 0.2 or ratio > 5:
        continue

    cv2.rectangle(
        image,
        (x, y),
        (x + w, y + h),
        (0, 255, 0),
        2
    )

    cv2.putText(
        image,
        f"Glove {glove_count}",
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

# -----------------------------
# Show count
# -----------------------------

print("Detected Gloves:", glove_count)

cv2.putText(
    image,
    f"Gloves: {glove_count}",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
)

# -----------------------------
# Display
# -----------------------------

cv2.imshow("Mask", mask)
cv2.imshow("Glove Count", image)

cv2.waitKey(0)
cv2.destroyAllWindows()