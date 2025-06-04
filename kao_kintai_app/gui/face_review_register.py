import customtkinter as ctk
import os
import shutil
import cv2
from PIL import Image
from customtkinter import CTkImage

UNRECOGNIZED_DIR = "unrecognized_faces"
KNOWN_DIR = "known_faces"

os.makedirs(UNRECOGNIZED_DIR, exist_ok=True)
os.makedirs(KNOWN_DIR, exist_ok=True)

def run():
    app = ctk.CTk()
    app.title("未認識顔 登録確認")
    app.geometry("700x600")

    ctk.CTkLabel(app, text="未認識画像の確認・登録", font=("Arial", 20)).pack(pady=10)

    current_image = [None]
    image_label = ctk.CTkLabel(app, text="")
    image_label.pack(pady=10)

    id_entry = ctk.CTkEntry(app, placeholder_text="学籍番号 or 社員番号を入力", width=200)
    id_entry.pack(pady=5)

    result_label = ctk.CTkLabel(app, text="")
    result_label.pack(pady=5)

    unrecognized_files = sorted([
        f for f in os.listdir(UNRECOGNIZED_DIR)
        if f.lower().endswith((".jpg", ".png"))
    ])

    index = [0]

    def show_image():
        if not unrecognized_files:
            result_label.configure(text="✅ すべて処理済みです")
            image_label.configure(image="")
            return

        file = unrecognized_files[index[0]]
        path = os.path.join(UNRECOGNIZED_DIR, file)
        img = Image.open(path).resize((400, 300))
        ctk_img = CTkImage(light_image=img, size=(400, 300))
        image_label.configure(image=ctk_img)
        image_label.image = ctk_img  # 保持しないと消える
        current_image[0] = file
        result_label.configure(text=f"画像ファイル：{file}")

    def register_image():
        student_id = id_entry.get().strip()
        if not student_id:
            result_label.configure(text="⚠ IDを入力してください")
            return
        src = os.path.join(UNRECOGNIZED_DIR, current_image[0])
        dst = os.path.join(KNOWN_DIR, f"{student_id}.jpg")
        shutil.copy(src, dst)
        os.remove(src)
        result_label.configure(text=f"✅ {student_id} として登録しました")
        unrecognized_files.pop(index[0])
        if index[0] >= len(unrecognized_files):
            index[0] = 0
        show_image()

    def skip_image():
        index[0] = (index[0] + 1) % len(unrecognized_files)
        show_image()

    def delete_image():
        os.remove(os.path.join(UNRECOGNIZED_DIR, current_image[0]))
        result_label.configure(text=f"🗑 {current_image[0]} を削除しました")
        unrecognized_files.pop(index[0])
        if index[0] >= len(unrecognized_files):
            index[0] = 0
        show_image()

    btn_frame = ctk.CTkFrame(app)
    btn_frame.pack(pady=10)

    ctk.CTkButton(btn_frame, text="✅ 登録", width=120, command=register_image).grid(row=0, column=0, padx=10)
    ctk.CTkButton(btn_frame, text="➡ スキップ", width=120, command=skip_image).grid(row=0, column=1, padx=10)
    ctk.CTkButton(btn_frame, text="🗑 削除", fg_color="red", width=120, command=delete_image).grid(row=0, column=2, padx=10)

    def go_back():
        import subprocess, sys
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "school_admin_menu.py"))
        subprocess.Popen([sys.executable, path])
        app.destroy()

    ctk.CTkButton(app, text="🔙 戻る", fg_color="gray", command=go_back).pack(pady=20)

    show_image()
    app.mainloop()

if __name__ == "__main__":
    run()
