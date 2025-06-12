import customtkinter as ctk
import cv2
import face_recognition
import os
import sys
import subprocess
import sqlite3
import numpy as np
from PIL import Image
from datetime import datetime
from customtkinter import CTkImage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.face_logging import save_unrecognized_face_with_id
from utils.db_utils import load_db_path  # 必要に応じて作成

KNOWN_FACES_DIR = "known_faces"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

previous_encoding = None

def recognize_face_from_frame(frame):
    global previous_encoding
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    known_encodings = []
    known_ids = []

    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(path)
            encs = face_recognition.face_encodings(image)
            if encs:
                known_encodings.append(encs[0])
                known_ids.append(os.path.splitext(filename)[0])

    for encoding in face_encodings:
        if previous_encoding is not None:
            distance = np.linalg.norm(previous_encoding - encoding)
            if distance < 0.01:
                print("⚠ スプーフィングの可能性あり（静止画像）")
                return "SPOOF_DETECTED"

        previous_encoding = encoding

        matches = face_recognition.compare_faces(known_encodings, encoding)
        if True in matches:
            idx = matches.index(True)
            return known_ids[idx]

    return None

def run(mode="学校用"):
    app = ctk.CTk()
    app.title(f"顔認証（{mode}）")
    app.geometry("720x700")

    video_label = ctk.CTkLabel(app, text="")
    video_label.pack(pady=10)

    result_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
    result_label.pack(pady=5)

    cap = cv2.VideoCapture(0)
    app.ctk_img_ref = None
    failed_frame = None
    recognized_id = None

    entry_frame = ctk.CTkFrame(app)
    entry_label = ctk.CTkLabel(entry_frame, text="学籍番号（社員番号）を入力：")
    entry_input = ctk.CTkEntry(entry_frame, width=200)
    entry_submit = ctk.CTkButton(entry_frame, text="登録", command=lambda: submit_unrecognized())

    def show_entry_ui():
        entry_label.pack(pady=5)
        entry_input.pack(pady=5)
        entry_submit.pack(pady=5)
        entry_frame.pack(pady=10)

    def hide_entry_ui():
        entry_frame.pack_forget()
        entry_input.delete(0, ctk.END)

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = img.resize((480, 360))
            ctk_img = CTkImage(light_image=img, size=(480, 360))
            video_label.configure(image=ctk_img)
            app.ctk_img_ref = ctk_img
        video_label.after(30, update_frame)

    action_var = ctk.StringVar(value="出勤")
    action_frame = ctk.CTkFrame(app)
    action_label = ctk.CTkLabel(action_frame, text="")
    action_buttons = []

    def show_action_selection(user_id):
        action_label.configure(text=f"✅ {user_id} さんとして認識しました。操作を選択してください。")
        action_label.pack(pady=5)
        options = ["出勤", "退勤", "休憩開始", "休憩終了"]
        for action in options:
            btn = ctk.CTkRadioButton(action_frame, text=action, variable=action_var, value=action)
            btn.pack(anchor="w", padx=30)
            action_buttons.append(btn)
        ctk.CTkButton(action_frame, text="実行", command=execute_action).pack(pady=10)
        action_frame.pack(pady=10)

    def hide_action_selection():
        for widget in action_frame.winfo_children():
            widget.destroy()
        action_frame.pack_forget()

    def execute_action():
        action = action_var.get()
        user_id = recognized_id
        timestamp = datetime.now().strftime("%H:%M:%S")
        result_label.configure(text=f"✅ {user_id} が「{action}」しました（{timestamp}）")
        save_attendance(user_id, action)
        hide_action_selection()

    def handle_school_action(action):
        nonlocal failed_frame
        hide_entry_ui()
        ret, frame = cap.read()
        if not ret:
            result_label.configure(text="📷 カメラ取得失敗")
            return

        user_id = recognize_face_from_frame(frame)
        if user_id:
            timestamp = datetime.now().strftime("%H:%M:%S")
            result_label.configure(text=f"✅ {user_id} が {action} しました（{timestamp}）")
            save_attendance(user_id, action)
        else:
            result_label.configure(text="❌ 顔認証失敗：IDを入力してください")
            failed_frame = frame.copy()
            show_entry_ui()

    def handle_work_face_capture():
        nonlocal recognized_id, failed_frame
        hide_entry_ui()
        hide_action_selection()
        ret, frame = cap.read()
        if not ret:
            result_label.configure(text="📷 カメラ取得失敗")
            return

        user_id = recognize_face_from_frame(frame)
        if user_id:
            recognized_id = user_id
            show_action_selection(user_id)
        else:
            result_label.configure(text="❌ 顔認証失敗：IDを入力してください")
            failed_frame = frame.copy()
            show_entry_ui()

    def submit_unrecognized():
        nonlocal failed_frame
        entered_id = entry_input.get().strip()
        db_path = load_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if not entered_id:
            result_label.configure(text="⚠ IDを入力してください")
            return

        if failed_frame is not None:
            save_unrecognized_face_with_id(failed_frame, entered_id)
            result_label.configure(text=f"📸 未認識画像を {entered_id} として保存しました")
            hide_entry_ui()
        else:
            try:
                if mode == "学校用":
                    cursor.execute("SELECT name FROM students WHERE id = ?", (entered_id,))
                else:
                    cursor.execute("SELECT name FROM employees WHERE id = ?", (entered_id,))
                row = cursor.fetchone()
                if row:
                    name = row[0]
                    action = "出席" if mode == "学校用" else "手動登録"
                    save_attendance(entered_id, action)
                    result_label.configure(text=f"✅ {name}（{entered_id}）を登録しました")
                    hide_entry_ui()
                else:
                    result_label.configure(text="⚠ 登録されていないIDです")
            except Exception as e:
                result_label.configure(text=f"❌ DBエラー: {e}")
            finally:
                conn.close()

    def save_attendance(user_id, action):
        db_path = load_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO attendance (user_id, action, timestamp) VALUES (?, ?, ?)",
                    (user_id, action, timestamp))
        conn.commit()
        conn.close()

    def open_user():
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "user_main.py"))
        subprocess.Popen([sys.executable, script_path])

    def open_admin():
        from gui import admin_login
        app.destroy()
        admin_login.run()

    btn_frame = ctk.CTkFrame(app)
    btn_frame.pack(pady=10)

    if mode == "学校用":
        ctk.CTkButton(btn_frame, text="出席", width=120, command=lambda: handle_school_action("出席")).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="退出", width=120, command=lambda: handle_school_action("退出")).grid(row=0, column=1, padx=10)
    else:
        ctk.CTkButton(btn_frame, text="顔を撮影する", command=handle_work_face_capture).pack()

    nav_frame = ctk.CTkFrame(app)
    nav_frame.pack(pady=10)
    ctk.CTkButton(nav_frame, text="利用者画面", width=150, command=open_user).grid(row=0, column=0, padx=10)
    ctk.CTkButton(nav_frame, text="管理者画面", width=150, command=open_admin).grid(row=0, column=1, padx=10)

    btn_exit = ctk.CTkButton(app, text="終了", fg_color="gray", command=lambda: [cap.release(), app.destroy()])
    btn_exit.pack(pady=10)

    update_frame()
    app.mainloop()

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "学校用"
    run(mode=mode)
