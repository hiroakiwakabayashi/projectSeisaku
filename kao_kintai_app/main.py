# kao_kintai_app/main.py

from gui import school_config, work_config
import json
import os

CONFIG_PATH = "config/init_config.json"

def save_mode(mode):
    os.makedirs("config", exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"mode": mode}, f, indent=4)
    print(f"✅ 選択されたモード「{mode}」を保存しました。")

    if mode == "学校用":
        school_config.run()
    elif mode == "勤怠用":
        work_config.run()

if __name__ == "__main__":
    import customtkinter as ctk
    app = ctk.CTk()
    app.title("モード選択")
    app.geometry("400x300")

    label = ctk.CTkLabel(app, text="どちらのモードで開始しますか？", font=("Arial", 18))
    label.pack(pady=40)

    btn_school = ctk.CTkButton(app, text="学校用（出席）", command=lambda: save_mode("学校用"))
    btn_school.pack(pady=10)

    btn_work = ctk.CTkButton(app, text="勤怠用（労働）", command=lambda: save_mode("勤怠用"))
    btn_work.pack(pady=10)

    app.mainloop()
