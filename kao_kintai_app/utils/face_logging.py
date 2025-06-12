import os
import cv2
from datetime import datetime

UNKNOWN_DIR = "unknown_faces"
os.makedirs(UNKNOWN_DIR, exist_ok=True)

def save_unrecognized_face_with_id(frame, user_id):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{user_id}_{timestamp}.jpg"
    path = os.path.join(UNKNOWN_DIR, filename)
    cv2.imwrite(path, frame)
    return path
