import cv2
import numpy as np

image_path = "/home/cpsstudent/icp_project/output/frames/cam1/GX010084/GX010084_frame_000030.jpg"

image = cv2.imread(image_path)

if image is None:
    print("Could not load image")
    exit()

# BGR -> HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Blue glove range
lower_blue = np.array([80, 30, 30])
upper_blue = np.array([150, 255, 255])

mask = cv2.inRange(
    hsv,
    lower_blue,
    upper_blue
)

result = cv2.bitwise_and(
    image,
    image,
    mask=mask
)

cv2.imshow("Original", image)
cv2.imshow("Blue Mask", mask)
cv2.imshow("Blue Gloves", result)

cv2.waitKey(0)
cv2.destroyAllWindows()