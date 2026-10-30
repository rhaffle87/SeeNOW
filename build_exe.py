# build_exe.py
import os
import sys
import subprocess
import customtkinter

def build():
    print("Mempersiapkan kompilasi SeeNOW (Smart Exam Engine & Navigated Optical Workflow) ke .exe...")

    ctk_path = os.path.dirname(customtkinter.__file__)
    sep = ";" if sys.platform == "win32" else ":"

    add_data = [
        f"--add-data={ctk_path}{sep}customtkinter/",
        f"--add-data=core/som_injector.js{sep}core/",
        f"--add-data=config.json.example{sep}."
    ]

    hidden_imports = [
        "--hidden-import=playwright",
        "--hidden-import=customtkinter",
        "--hidden-import=PIL",
        "--hidden-import=keyboard",
        "--hidden-import=mss",
        "--hidden-import=pyautogui",
        "--hidden-import=openai",
        "--hidden-import=httpx",
        "--hidden-import=pydantic"
    ]

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name=SeeNOW",
        *add_data,
        *hidden_imports,
        "main.py"
    ]

    print("Menjalankan perintah PyInstaller:")
    print(" ".join(cmd))
    subprocess.check_call(cmd)
    print("\n[SUCCESS] Kompilasi berhasil! Executable tersedia di: dist/SeeNOW/SeeNOW.exe")

if __name__ == "__main__":
    build()
