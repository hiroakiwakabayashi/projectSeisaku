import customtkinter as ctk
import cv2
import face_recognition
import os
import sys
import json
import sqlite3
import numpy as np
from datetime import datetime
from tkinter import filedialog
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

KNOWN_FACES_DIR = "known_faces"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/school_config.json"))

def load_db_path():
    if not os.path.exists(CONFIG_PATH):
        return "school_db.sqlite3"
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("db_path", "school_db.sqlite3")

def save_face_image(student_id, image):
    filename = f"{student_id}.jpg"
    path = os.path.join(KNOWN_FACES_DIR, filename)
    cv2.imwrite(path, image)
    return path

def register_to_db(db_path, student_id, name, student_class, gender, email):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT,
                student_class TEXT,
                gender TEXT,
                email TEXT,
                registered_at TEXT
            )
        """)

        cur.execute("""
            INSERT OR REPLACE INTO students
            (student_id, name, student_class, gender, email, registered_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            name,
            student_class,
            gender,
            email,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("DB登録エラー:", e)
        return False

def run():
    app = ctk.CTk()
    app.title("学生登録")
    app.geometry("600x750")

    ctk.CTkLabel(app, text="学生登録フォーム", font=("Arial", 20)).pack(pady=20)

    entry_frame = ctk.CTkFrame(app)
    entry_frame.pack(pady=10)

    # 各入力項目
    labels_entries = {
        "学籍番号": ctk.CTkEntry(entry_frame, width=250),
        "氏名": ctk.CTkEntry(entry_frame, width=250),
        "クラス": ctk.CTkEntry(entry_frame, width=250),
        "性別": ctk.CTkEntry(entry_frame, width=250),
        "メールアドレス": ctk.CTkEntry(entry_frame, width=250),
    }

    for i, (label_text, entry) in enumerate(labels_entries.items()):
        ctk.CTkLabel(entry_frame, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry.grid(row=i, column=1, padx=10, pady=5)

    captured_image = None
    result_label = ctk.CTkLabel(app, text="")
    result_label.pack()

    def capture_from_camera():
        nonlocal captured_image
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            captured_image = frame
            result_label.configure(text="📷 カメラ画像を取得しました")
        else:
            result_label.configure(text="⚠ カメラ取得失敗")
        cap.release()

    def select_image():
        nonlocal captured_image
        file_path = filedialog.askopenfilename(filetypes=[("画像ファイル", "*.jpg *.png")])
        if file_path:
            img = cv2.imread(file_path)
            captured_image = img
            result_label.configure(text=f"🖼 画像選択済み: {os.path.basename(file_path)}")

    def register_student():
        db_path = load_db_path()
        student_id = labels_entries["学籍番号"].get().strip()
        name = labels_entries["氏名"].get().strip()
        student_class = labels_entries["クラス"].get().strip()
        gender = labels_entries["性別"].get().strip()
        email = labels_entries["メールアドレス"].get().strip()

        if not student_id or not name:
            result_label.configure(text="⚠ 学籍番号と氏名は必須です")
            return
        if captured_image is None:
            result_label.configure(text="⚠ 顔画像を登録してください")
            return

        face_locations = face_recognition.face_locations(captured_image)
        if not face_locations:
            result_label.configure(text="⚠ 顔が検出できません")
            return

        save_face_image(student_id, captured_image)

        if register_to_db(db_path, student_id, name, student_class, gender, email):
            result_label.configure(text=f"✅ {name} ({student_id}) を登録しました")
        else:
            result_label.configure(text="❌ データベース登録に失敗しました")

    ctk.CTkButton(app, text="📷 カメラで撮影", command=capture_from_camera).pack(pady=5)
    ctk.CTkButton(app, text="🖼 ファイルから選択", command=select_image).pack(pady=5)
    ctk.CTkButton(app, text="✅ 登録する", command=register_student).pack(pady=15)

    def go_back():
        import subprocess
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "school_admin_menu.py"))
        subprocess.Popen([sys.executable, path])
        app.destroy()

    ctk.CTkButton(app, text="🔙 戻る", fg_color="gray", command=go_back).pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    run()
