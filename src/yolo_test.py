from ultralytics import YOLO

model = YOLO(
    "/home/cpsstudent/icp_project/runs/detect/glove_detector-2/weights/best.pt"
)

model.predict(
    source="/home/cpsstudent/icp_project/GL020084.mp4",
    conf=0.50,
    save=True
)

print("Done")