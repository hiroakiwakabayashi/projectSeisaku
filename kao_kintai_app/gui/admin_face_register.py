# kao_kintai_app/gui/face_review_register.py

import customtkinter as ctk
from PIL import Image, ImageTk
import os
import shutil
import csv

UNRECOGNIZED_DIR = "unrecognized_faces"
KNOWN_DIR = "known_faces"
LOG_PATH = "unrecognized_faces_log.csv"

def run():
    app = ctk.CTk()
    app.title("未認識顔の確認・登録")
    app.geometry("800x600")

    os.makedirs(KNOWN_DIR, exist_ok=True)

    # ログと画像の読み込み
    def load_unregistered_list():
        entries = []
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 3 and row[2] == "未紐付":
                        entries.append(row[0])
        return entries

    pending_faces = load_unregistered_list()
    if not pending_faces:
        print("✅ 未登録画像はありません")
        return

    current_index = 0

    # --- UI ---
    frame_images = ctk.CTkFrame(app)
    frame_images.pack(pady=10)

    label_log = ctk.CTkLabel(frame_images, text="未認識画像")
    label_log.grid(row=0, column=0, padx=10)
    label_known = ctk.CTkLabel(frame_images, text="登録済み画像（あれば）")
    label_known.grid(row=0, column=1, padx=10)

    panel_new = ctk.CTkLabel(frame_images, text="")
    panel_new.grid(row=1, column=0)
    panel_old = ctk.CTkLabel(frame_images, text="")
    panel_old.grid(row=1, column=1)

    entry_id = ctk.CTkEntry(app, width=200, placeholder_text="学籍番号または職番")
    entry_id.pack(pady=10)

    def display_images():
        filename = pending_faces[current_index]
        new_path = os.path.join(UNRECOGNIZED_DIR, filename)
        img = Image.open(new_path).resize((200, 200))
        panel_new.configure(image=ImageTk.PhotoImage(img))
        panel_new.image = ImageTk.PhotoImage(img)

        # 既存画像（あるなら）
        sid = entry_id.get().strip()
        if sid:
            old_path = os.path.join(KNOWN_DIR, f"{sid}.jpg")
            if os.path.exists(old_path):
                img_old = Image.open(old_path).resize((200, 200))
                panel_old.configure(image=ImageTk.PhotoImage(img_old))
                panel_old.image = ImageTk.PhotoImage(img_old)
            else:
                panel_old.configure(image=None, text="なし")

    def next_image():
        nonlocal current_index
        if current_index + 1 < len(pending_faces):
            current_index += 1
            panel_old.configure(image=None, text="")
            entry_id.delete(0, "end")
            display_images()
        else:
            print("✅ 全て確認しました")
            app.destroy()

    def register_image():
        sid = entry_id.get().strip()
        if not sid:
            print("⚠ 学籍番号が未入力です")
            return
        filename = pending_faces[current_index]
        src_path = os.path.join(UNRECOGNIZED_DIR, filename)
        dst_path = os.path.join(KNOWN_DIR, f"{sid}.jpg")
        shutil.copyfile(src_path, dst_path)

        # ログ更新
        updated = []
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for row in csv.reader(f):
                if row[0] == filename:
                    row[2] = "紐付済"
                updated.append(row)
        with open(LOG_PATH, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(updated)

        # ファイル削除 & 次へ
        os.remove(src_path)
        print(f"✅ {sid} として登録完了")
        next_image()

    # --- ボタン ---
    frame_buttons = ctk.CTkFrame(app)
    frame_buttons.pack(pady=10)

    btn_compare = ctk.CTkButton(frame_buttons, text="比較表示", command=display_images)
    btn_compare.grid(row=0, column=0, padx=10)

    btn_register = ctk.CTkButton(frame_buttons, text="登録", command=register_image)
    btn_register.grid(row=0, column=1, padx=10)

    btn_skip = ctk.CTkButton(frame_buttons, text="スキップ", command=next_image)
    btn_skip.grid(row=0, column=2, padx=10)

    display_images()
    app.mainloop()
