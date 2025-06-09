import customtkinter as ctk
import subprocess
import os
import sys

def run():
    app = ctk.CTk()
    app.title("勤怠用 - 管理者メニュー")
    app.geometry("400x400")

    ctk.CTkLabel(app, text="勤怠用 管理者メニュー", font=("Arial", 18)).pack(pady=20)

    def open_employee_register():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "admin_employee_register.py"))
        subprocess.Popen([sys.executable, path])

    def open_attendance_check():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "admin_attendance_check.py"))
        subprocess.Popen([sys.executable, path])

    def open_face_register():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "face_review_register.py"))
        subprocess.Popen([sys.executable, path])

    ctk.CTkButton(app, text="① 従業員登録", width=250, command=open_employee_register).pack(pady=10)
    ctk.CTkButton(app, text="② 勤怠記録の確認", width=250, command=open_attendance_check).pack(pady=10)
    ctk.CTkButton(app, text="③ 未認識顔の登録", width=250, command=open_face_register).pack(pady=10)

    ctk.CTkButton(app, text="終了", fg_color="gray", command=app.destroy).pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    run()
