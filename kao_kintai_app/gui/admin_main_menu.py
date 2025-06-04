import customtkinter as ctk
import subprocess
import os
import sys

def run():
    app = ctk.CTk()
    app.title("管理者メニュー")
    app.geometry("400x400")

    ctk.CTkLabel(app, text="管理者用メニュー", font=("Arial", 20)).pack(pady=20)

    def open_school_admin():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "school_admin_menu.py"))
        subprocess.Popen([sys.executable, path])
        app.destroy()

    def open_work_admin():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "work_admin_menu.py"))
        subprocess.Popen([sys.executable, path])
        app.destroy()

    ctk.CTkButton(app, text="🎓 学校用 管理メニュー", command=open_school_admin, width=220).pack(pady=15)
    ctk.CTkButton(app, text="🧑‍💼 勤怠用 管理メニュー", command=open_work_admin, width=220).pack(pady=15)

    ctk.CTkButton(app, text="🔙 戻る", fg_color="gray", command=app.destroy).pack(pady=30)

    app.mainloop()

if __name__ == "__main__":
    run()
