# kao_kintai_app/utils/face_logging.py

import os
import cv2
import csv
from datetime import datetime

UNRECOGNIZED_DIR = "unrecognized_faces"
LOG_CSV = "unrecognized_faces_log.csv"
os.makedirs(UNRECOGNIZED_DIR, exist_ok=True)

def save_unrecognized_face_with_id(frame, entered_id):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{entered_id}_{timestamp}.jpg"
    filepath = os.path.join(UNRECOGNIZED_DIR, filename)
    cv2.imwrite(filepath, frame)

    # CSVログにも記録
    with open(LOG_CSV, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([entered_id, timestamp, filepath])
