# kao_kintai_app/main.py
import customtkinter as ctk
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "init_config.json")

class InitialSettingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("初期設定 - 顔認証勤怠アプリ")
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="アプリの用途を選んでください", font=("Arial", 18))
        self.label.pack(pady=20)

        self.usage_var = ctk.StringVar(value="学校用")
        self.radio_school = ctk.CTkRadioButton(self, text="学校用", variable=self.usage_var, value="学校用")
        self.radio_work = ctk.CTkRadioButton(self, text="勤怠用", variable=self.usage_var, value="勤怠用")
        self.radio_school.pack(pady=5)
        self.radio_work.pack(pady=5)

        self.confirm_button = ctk.CTkButton(self, text="決定", command=self.confirm_selection)
        self.confirm_button.pack(pady=30)

    def confirm_selection(self):
        selected_mode = self.usage_var.get()

        config_data = {
            "mode": selected_mode
        }

        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)

        print(f"✅ 選択されたモード「{selected_mode}」を {CONFIG_PATH} に保存しました。")
        self.destroy()

if __name__ == "__main__":
    app = InitialSettingApp()
    app.mainloop()
