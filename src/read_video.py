import cv2

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video")
        return

    prev_gray = None
    frame_count = 0

    no_motion_ranges = []
    start = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gray)

            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

            thresh = cv2.GaussianBlur(thresh, (5,5), 0)

            motion_score = thresh.sum()
            print("Frame:", frame_count, "Motion:", motion_score)
            

            if motion_score < 120000000:
                if start is None:
                    start = frame_count
            else:
                if start is not None:
                    no_motion_ranges.append((start, frame_count))
                    start = None

        prev_gray = gray
    if start is not None:
     no_motion_ranges.append((start, frame_count))

    cap.release()

    # Save results
    with open("no_motion.txt", "w") as f:
        for s, e in no_motion_ranges:
            f.write(f"{video_path} no-motion-frame{{{s}-{e}}}\n")

    print("Done. Results saved in no_motion.txt") 