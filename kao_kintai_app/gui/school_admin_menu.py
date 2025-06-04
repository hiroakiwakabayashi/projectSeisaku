import customtkinter as ctk
import subprocess
import os
import sys

def run():
    app = ctk.CTk()
    app.title("学校用 管理者メニュー")
    app.geometry("500x400")

    ctk.CTkLabel(app, text="学校用 管理メニュー", font=("Arial", 20)).pack(pady=20)

    def open_student_register():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "admin_student_register.py"))
        subprocess.Popen([sys.executable, path])

    def open_attendance_editor():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "admin_attendance_editor.py"))
        subprocess.Popen([sys.executable, path])

    def open_face_review():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "face_review_register.py"))
        subprocess.Popen([sys.executable, path])

    def go_back():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "face_recognition_screen.py"))
        subprocess.Popen([sys.executable, path, "学校用"])
        app.destroy()

    # 各ボタン
    ctk.CTkButton(app, text="👨‍🎓 学生登録", width=250, command=open_student_register).pack(pady=10)
    ctk.CTkButton(app, text="🕒 出席コマ管理", width=250, command=open_attendance_editor).pack(pady=10)
    ctk.CTkButton(app, text="📷 未認識顔の確認・登録", width=250, command=open_face_review).pack(pady=10)
    ctk.CTkButton(app, text="🔙 戻る", fg_color="gray", width=150, command=go_back).pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    run()
