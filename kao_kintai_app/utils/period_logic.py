# kao_kintai_app/gui/face_recognition_screen.py

import customtkinter as ctk
import cv2
import face_recognition
import os
import numpy as np
import sqlite3
from datetime import datetime


DB_PATH = "school_db.sqlite3"  # または work_db.sqlite3 に切り替え可
KNOWN_FACES_DIR = "known_faces"

from datetime import datetime

def get_attended_periods(entry_time: datetime, exit_time: datetime):
    """
    仮のロジック：出席したコマを返す（常に1〜3コマとみなす）
    """
    return [1, 2, 3]

def recognize_face_from_camera():
    known_encodings = []
    known_ids = []

    # 顔データ読み込み
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                name = os.path.splitext(filename)[0]
                known_ids.append(name)

    cap = cv2.VideoCapture(0)
    identified_id = None

    while True:
        ret, frame = cap.read()
        rgb = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for encoding, loc in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, encoding)
            if True in matches:
                match_idx = matches.index(True)
                identified_id = known_ids[match_idx]
                top, right, bottom, left = loc
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, identified_id, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                break

        cv2.imshow("顔認証中 - ESCで終了", frame)
        if cv2.waitKey(1) & 0xFF == 27 or identified_id:
            break

    cap.release()
    cv2.destroyAllWindows()
    return identified_id

def check_user_type(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 学生テーブルにあるか？
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (user_id,))
    student = cursor.fetchone()

    # 労働者テーブルにあるか？
    cursor.execute("SELECT * FROM workers WHERE id = ?", (user_id,))
    worker = cursor.fetchone()

    conn.close()

    if student:
        return "学生"
    elif worker:
        return "労働者"
    else:
        return "不明"

def run():
    app = ctk.CTk()
    app.title("顔認証ログイン")
    app.geometry("400x300")

    label = ctk.CTkLabel(app, text="顔認証 or 管理者ログインを選択", font=("Arial", 16))
    label.pack(pady=30)

    result_label = ctk.CTkLabel(app, text="")
    result_label.pack(pady=10)

    def start_recognition():
        user_id = recognize_face_from_camera()
        if user_id:
            user_type = check_user_type(user_id)
            result_label.configure(text=f"{user_type}として認識：{user_id}")

            # 🔜 ここで画面遷移処理（例：student_main.run(user_id)）
            app.after(2000, app.destroy)
        else:
            result_label.configure(text="⚠ 顔認識に失敗しました")

    btn_recognize = ctk.CTkButton(app, text="顔認証でログイン", command=start_recognition)
    btn_recognize.pack(pady=10)

    def go_to_admin():
        from gui import admin_login
        app.destroy()
        admin_login.run(mode="学校用")  # or 勤怠用

    btn_admin = ctk.CTkButton(app, text="管理者としてログイン", command=go_to_admin)
    btn_admin.pack(pady=10)

    app.mainloop()
