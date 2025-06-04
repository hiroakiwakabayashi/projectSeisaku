import customtkinter as ctk
import sqlite3
import os
import json
import sys
from tkinter import ttk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/school_config.json"))

def load_db_path():
    if not os.path.exists(CONFIG_PATH):
        return "school_db.sqlite3"
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("db_path", "school_db.sqlite3")

def run():
    app = ctk.CTk()
    app.title("出席コマ管理")
    app.geometry("800x600")

    db_path = load_db_path()

    ctk.CTkLabel(app, text="出席コマ編集", font=("Arial", 20)).pack(pady=10)

    frame_top = ctk.CTkFrame(app)
    frame_top.pack(pady=10)

    ctk.CTkLabel(frame_top, text="学籍番号").grid(row=0, column=0, padx=10)
    entry_id = ctk.CTkEntry(frame_top, width=200)
    entry_id.grid(row=0, column=1, padx=10)

    tree_frame = ctk.CTkFrame(app)
    tree_frame.pack(pady=10)

    columns = ("date", "period", "status")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack()

    def load_attendance():
        student_id = entry_id.get().strip()
        if not student_id:
            return
        tree.delete(*tree.get_children())
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS attendances (
                student_id TEXT,
                date TEXT,
                period INTEGER,
                status TEXT
            )
        """)
        cur.execute("SELECT date, period, status FROM attendances WHERE student_id = ? ORDER BY date, period", (student_id,))
        for row in cur.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def save_changes():
        student_id = entry_id.get().strip()
        if not student_id:
            return
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM attendances WHERE student_id = ?", (student_id,))
        for item in tree.get_children():
            values = tree.item(item, "values")
            date, period, status = values
            cur.execute("INSERT INTO attendances VALUES (?, ?, ?, ?)", (student_id, date, int(period), status))
        conn.commit()
        conn.close()

    def edit_selected():
        selected = tree.selection()
        if not selected:
            return
        item = selected[0]
        values = tree.item(item, "values")
        date, period, status = values

        def update_status():
            new_status = status_var.get()
            tree.item(item, values=(date, period, new_status))
            popup.destroy()

        popup = ctk.CTkToplevel(app)
        popup.title("出席区分を編集")
        status_var = ctk.StringVar(value=status)
        options = ["出席", "遅刻", "欠席", "公欠"]
        ctk.CTkOptionMenu(popup, values=options, variable=status_var).pack(pady=10)
        ctk.CTkButton(popup, text="更新", command=update_status).pack(pady=10)

    def go_back():
        import subprocess
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "school_admin_menu.py"))
        subprocess.Popen([sys.executable, path])
        app.destroy()

    ctk.CTkButton(app, text="🔍 出席履歴を読み込む", command=load_attendance).pack(pady=5)
    ctk.CTkButton(app, text="✏ 選択行を編集", command=edit_selected).pack(pady=5)
    ctk.CTkButton(app, text="💾 保存", command=save_changes).pack(pady=5)
    ctk.CTkButton(app, text="🔙 戻る", fg_color="gray", command=go_back).pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    run()
