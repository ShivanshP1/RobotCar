import cv2
from ultralytics import YOLO

USE_FPS_COUNTER = False  # Set to False to disable FPS counter
MODEL_TYPE = "yolov8n.pt"  # Use "yolov8n.pt" for a smaller model (YOLOv8 nano)

STOP_SIGN_LABEL = 11  # Label for stop sign, adjust according to your model
CONFIDENCE_THRESHOLD = 0.92  # Minimum confidence to consider a detection valid
FOCAL_LENGTH = 500  # Example focal length (in pixels), you may need to calibrate this
REAL_OBJECT_WIDTH = 0.06  # Actual width of the stop sign (in meters)

def detect_objects(image):
    """Perform object detection on the input image."""
    results = model(image)  # Call the model to detect objects
    return results

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

        # Check each result for stop signs
        for result in results:
            # Get class IDs and confidences from the detection results
            class_ids = result.boxes.cls
            confidences = result.boxes.conf
            
            # Check each detection
            for class_id, confidence in zip(class_ids, confidences):
                if class_id == STOP_SIGN_LABEL and confidence > CONFIDENCE_THRESHOLD:
                    print(f"Stop sign detected with confidence: {confidence:.2f}")
                
            annotated_frame = result.plot()  
            cv2.imshow("YOLOv8 Object Detection", annotated_frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()