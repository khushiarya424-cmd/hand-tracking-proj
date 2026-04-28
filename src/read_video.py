import cv2
import os
def play_video(video_path):
    print("Function started...")
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video")
        return
    frame_count = 0


    while True:
        ret, frame = cap.read()
        print("Reading frame..")

        if not ret:
            break
        frame_count+= 1
        
        print("Frame: ", frame_count, flush=True)

        if frame_count % 10 == 0:
            print("Saving to:", os.path.abspath(f"frames/frame_{frame_count}.jpg"))
            cv2.imwrite(f"frames/frame_{frame_count}.jpg", frame)
        


        cv2.imshow("Video", frame)

        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()