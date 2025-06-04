# main.py
from gui import school_config, work_config
import customtkinter as ctk

def start_school_mode():
    school_config.run()

def start_work_mode():
    work_config.run()

def run():
    app = ctk.CTk()
    app.title("モード選択（デモ用）")
    app.geometry("400x300")

    ctk.CTkLabel(app, text="モードを選択してください", font=("Arial", 18)).pack(pady=30)

    ctk.CTkButton(app, text="🎓 学校用モード（出席）", command=lambda: [app.destroy(), start_school_mode()]).pack(pady=10)
    ctk.CTkButton(app, text="🧑‍💼 勤怠用モード（労働）", command=lambda: [app.destroy(), start_work_mode()]).pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    run()
