import cv2
import time
from ultralytics import YOLO

USE_FPS_COUNTER = True  # Set to False to disable FPS counter
MODEL_TYPE = "yolov8n.pt"  # Use "yolov8n.pt" for a smaller model (YOLOv8 nano)

STOP_SIGN_LABEL = 9  # Label for stop sign, adjust according to your model
FOCAL_LENGTH = 500  # Example focal length (in pixels), you may need to calibrate this
REAL_OBJECT_WIDTH = 0.06  # Actual width of the stop sign (in meters)

def detect_objects(image):
    """Perform object detection on the input image."""
    results = model(image)  # Call the model to detect objects
    return results

def display_fps(frame, prev_time):
    """Calculate and display FPS on the frame."""
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return curr_time

# ==================== Main Program ====================
if __name__ == "__main__":
    # Suppress the ultralytics' logger output
    import logging
    logging.getLogger("ultralytics").setLevel(logging.ERROR)

    # Load the YOLOv8 model (small version for faster detection)
    model = YOLO(MODEL_TYPE)

    cap = cv2.VideoCapture(0)
    prev_time = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection
        results = detect_objects(frame)

        # Display FPS if enabled
        if USE_FPS_COUNTER:
            prev_time = display_fps(frame, prev_time)


        for result in results:
            annotated_frame = result.plot()  
            cv2.imshow("YOLOv8 Object Detection", annotated_frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
