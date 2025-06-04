import customtkinter as ctk

def run():
    app = ctk.CTk()
    app.title("勤怠用 - 管理メニュー")
    app.geometry("400x300")
    ctk.CTkLabel(app, text="勤怠用管理者メニュー", font=("Arial", 18)).pack(pady=30)
    ctk.CTkButton(app, text="終了", fg_color="gray", command=app.destroy).pack(pady=30)
    app.mainloop()

if __name__ == "__main__":
    run()
