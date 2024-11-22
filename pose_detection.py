import cv2

def gen_frames():
    cap = cv2.VideoCapture(0)  # Use the webcam
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    while cap.isOpened():
        success, frame = cap.read()  # Read the frame from the webcam
        if not success:
            print("Error: Unable to read frame from camera.")
            break

        # Convert the frame to JPEG format.
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("Error: Unable to encode frame as JPEG.")
            continue

        frame = buffer.tobytes()

        # Use multipart/x-mixed-replace content type to stream the frames
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()  # Release the video capture object
    cv2.destroyAllWindows()  # Destroy any OpenCV windows (if any were opened)
