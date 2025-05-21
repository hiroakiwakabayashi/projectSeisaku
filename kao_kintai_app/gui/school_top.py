# kao_kintai_app/gui/school_top.py
import customtkinter as ctk

def run():
    app = ctk.CTk()
    app.title("学校用トップ画面")
    app.geometry("400x300")

    label = ctk.CTkLabel(app, text="📚 学校用モードです", font=("Arial", 18))
    label.pack(pady=100)

    app.mainloop()
