import customtkinter as ctk
import cv2
import face_recognition
import os
import sys
import subprocess
import numpy as np
from PIL import Image
from datetime import datetime
from customtkinter import CTkImage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.face_logging import save_unrecognized_face_with_id

KNOWN_FACES_DIR = "known_faces"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

def recognize_face_from_frame(frame):
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
        matches = face_recognition.compare_faces(known_encodings, encoding)
        if True in matches:
            idx = matches.index(True)
            return known_ids[idx]
    return None

def run(mode="学校用"):
    app = ctk.CTk()
    app.title(f"顔認証（{mode}）")
    app.geometry("700x620")

    video_label = ctk.CTkLabel(app, text="")
    video_label.pack(pady=10)

    result_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
    result_label.pack(pady=5)

    cap = cv2.VideoCapture(0)
    app.ctk_img_ref = None
    failed_frame = None

    entry_frame = ctk.CTkFrame(app)
    entry_label = ctk.CTkLabel(entry_frame, text="学籍番号（または社員番号）を入力してください：")
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

    def handle_action(action):
        nonlocal failed_frame
        hide_entry_ui()
        ret, frame = cap.read()
        if not ret:
            result_label.configure(text="📷 カメラ取得失敗")
            return

        user_id = recognize_face_from_frame(frame)
        if user_id:
            timestamp = datetime.now().strftime("%H:%M:%S")
            result_label.configure(text=f"✅ {user_id} が「{action}」しました（{timestamp}）")
        else:
            result_label.configure(text="❌ 顔認証失敗：IDを入力してください")
            failed_frame = frame.copy()
            show_entry_ui()

    def submit_unrecognized():
        nonlocal failed_frame
        entered_id = entry_input.get().strip()
        if entered_id and failed_frame is not None:
            save_unrecognized_face_with_id(failed_frame, entered_id)
            result_label.configure(text=f"📸 未認識画像を {entered_id} として保存しました")
            hide_entry_ui()
        else:
            result_label.configure(text="⚠ 入力がありません")

    def open_menu():
        menu_win = ctk.CTkToplevel(app)
        menu_win.title("メニュー")
        menu_win.geometry("250x150")
        menu_win.attributes("-topmost", True)

        def open_user():
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "user_main.py"))
            subprocess.Popen([sys.executable, script_path])

        def open_admin():
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "admin_main_menu.py"))
            subprocess.Popen([sys.executable, script_path])

        ctk.CTkLabel(menu_win, text="画面遷移メニュー").pack(pady=10)
        ctk.CTkButton(menu_win, text="利用者画面", command=open_user).pack(pady=5)
        ctk.CTkButton(menu_win, text="管理者画面", command=open_admin).pack(pady=5)

    btn_frame = ctk.CTkFrame(app)
    btn_frame.pack(pady=10)

    if mode == "勤怠用":
        ctk.CTkButton(btn_frame, text="出勤", width=120, command=lambda: handle_action("出勤")).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="退勤", width=120, command=lambda: handle_action("退勤")).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="休憩開始", width=120, command=lambda: handle_action("休憩開始")).grid(row=1, column=0, padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="休憩終了", width=120, command=lambda: handle_action("休憩終了")).grid(row=1, column=1, padx=5, pady=5)
    else:
        ctk.CTkButton(btn_frame, text="出席", width=120, command=lambda: handle_action("出席")).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="退出", width=120, command=lambda: handle_action("退出")).grid(row=0, column=1, padx=10)

    btn_menu = ctk.CTkButton(app, text="≡ メニュー", width=80, command=open_menu)
    btn_menu.pack(pady=5)

    btn_exit = ctk.CTkButton(app, text="終了", fg_color="gray", command=lambda: [cap.release(), app.destroy()])
    btn_exit.pack(pady=5)

    update_frame()
    app.mainloop()

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "学校用"
    run(mode=mode)
