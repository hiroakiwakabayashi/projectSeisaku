import os
import subprocess
import sys
import venv

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def create_virtualenv(env_name="venv"):
    print(f"✅ 仮想環境 `{env_name}` を作成中...")
    venv.create(env_name, with_pip=True)
    print("✅ 仮想環境作成完了。")

def install_packages(env_name="venv"):
    pip_path = os.path.join(env_name, "Scripts", "pip.exe")  # Windows用
    print("✅ 必要なパッケージをインストール中...")
    run_command(f'"{pip_path}" install --upgrade pip')
    run_command(f'"{pip_path}" install opencv-python face_recognition dlib Flask pywebview PySimpleGUI bcrypt fpdf')
    print("✅ パッケージインストール完了。")

def create_project_structure():
    print("✅ プロジェクトディレクトリを作成中...")
    os.makedirs("kao_kintai_app/gui", exist_ok=True)
    os.makedirs("kao_kintai_app/face_recognition", exist_ok=True)
    os.makedirs("kao_kintai_app/db", exist_ok=True)
    os.makedirs("kao_kintai_app/utils", exist_ok=True)
    os.makedirs("kao_kintai_app/config", exist_ok=True)
    with open("kao_kintai_app/main.py", "w") as f:
        f.write("# メインアプリ起動ポイント\n")
    print("✅ ディレクトリ構造作成完了。")

if __name__ == "__main__":
    print("🔧 顔認証勤怠アプリ 環境構築 開始 🔧")
    create_virtualenv()
    install_packages()
    create_project_structure()
    print("🎉 環境構築完了！仮想環境を有効化して開発を始めてください。")
