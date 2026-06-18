from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="/home/cpsstudent/icp_project/yolo_dataset/data.yaml",
    epochs=50,
    imgsz=640,
    batch=8,
    name="glove_detector"
)