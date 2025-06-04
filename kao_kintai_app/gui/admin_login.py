import customtkinter as ctk
import json
import os
import sys
import subprocess
import bcrypt

INIT_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/init_config.json"))

def load_mode_config():
    if not os.path.exists(INIT_CONFIG_PATH):
        return None, "初期設定ファイル（init_config.json）が見つかりません。"

    with open(INIT_CONFIG_PATH, "r", encoding="utf-8") as f:
        init = json.load(f)
        mode = init.get("mode")

        if mode == "学校用":
            config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/school_config.json"))
        elif mode == "勤怠用":
            config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/work_config.json"))
        else:
            return None, "モードの値が不正です（学校用／勤怠用のみ対応）。"

        if not os.path.exists(config_path):
            return None, f"{mode} の設定ファイルが存在しません（{config_path}）"

        with open(config_path, "r", encoding="utf-8") as cf:
            config = json.load(cf)
            config["mode"] = mode  # モード情報も含めて返す
            return config, None

def run():
    app = ctk.CTk()
    app.title("管理者ログイン")
    app.geometry("400x300")

    ctk.CTkLabel(app, text="管理者ログイン", font=("Arial", 18)).pack(pady=20)

    ctk.CTkLabel(app, text="ID").pack()
    entry_id = ctk.CTkEntry(app, width=200)
    entry_id.pack(pady=5)

    ctk.CTkLabel(app, text="パスワード").pack()
    entry_pass = ctk.CTkEntry(app, width=200, show="*")
    entry_pass.pack(pady=5)

    result_label = ctk.CTkLabel(app, text="", text_color="red")
    result_label.pack(pady=5)

    def login():
        user_id = entry_id.get().strip()
        user_pass = entry_pass.get().strip()

        config, error = load_mode_config()
        if error:
            result_label.configure(text=error)
            return

        admin_id = config.get("admin_id")
        admin_hash = config.get("admin_password_hash")
        mode = config.get("mode")

        if not all([admin_id, admin_hash, mode]):
            result_label.configure(text="設定が不完全です（ID/PW/モード）")
            return

        if user_id == admin_id and bcrypt.checkpw(user_pass.encode(), admin_hash.encode()):
            result_label.configure(text="✅ ログイン成功", text_color="green")
            app.after(500, lambda: open_admin_menu(mode, app))
        else:
            result_label.configure(text="❌ ログイン失敗")

    def open_admin_menu(mode, root):
        root.destroy()
        if mode == "学校用":
            target = os.path.abspath(os.path.join(os.path.dirname(__file__), "school_admin_menu.py"))
        elif mode == "勤怠用":
            target = os.path.abspath(os.path.join(os.path.dirname(__file__), "work_admin_menu.py"))
        else:
            print("未定義のモードです")
            return

        subprocess.Popen([sys.executable, target])

    ctk.CTkButton(app, text="ログイン", command=login).pack(pady=15)
    ctk.CTkButton(app, text="終了", fg_color="gray", command=app.destroy).pack()

    app.mainloop()

if __name__ == "__main__":
    run()
