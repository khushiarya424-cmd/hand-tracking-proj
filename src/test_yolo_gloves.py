from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

image_path = "/home/cpsstudent/icp_project/output/frames/cam1/GX010084/GX010084_frame_000030.jpg"

results = model(
    image_path,
    conf=0.1
)

print(results[0].boxes)

annotated = results[0].plot()

cv2.imshow("YOLO", annotated)
cv2.waitKey(0)
cv2.destroyAllWindows()