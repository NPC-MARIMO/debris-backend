from ultralytics import YOLO
import numpy as np
import cv2
import uuid

# Load model once
model = YOLO("model/best.pt")

def detect_debris(image_bytes):

    # Convert bytes → numpy image
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = model(img)

    detections = []

    for box in results[0].boxes:

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        conf = float(box.conf[0].cpu().numpy())

        detections.append({
            "object_id": str(uuid.uuid4()),
            "bbox": [float(x1), float(y1), float(x2), float(y2)],
            "confidence": conf
        })

    return detections
