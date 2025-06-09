import subprocess
import platform
import os

venv_dir = ".venv"
system = platform.system()
if system == "Windows":
    venv_activate = os.path.join(venv_dir, "Scripts", "activate.bat")
elif system in ["Linux", "Darwin"]:  # macOS/Linux
    venv_activate = os.path.join(venv_dir, "bin", "activate")
else:
    print("Unsupported OS")
    exit()

if not os.path.exists(venv_dir):
    print("🔧 Virtual environment not found. Creating one...")
    subprocess.run(["python", "-m", "venv", venv_dir])
    print("✅ Virtual environment created.")

    print("🔄 Installing dependencies...")
    subprocess.run(
        f"{venv_activate} && python -m pip install -r requirements.txt ", shell=True)

    print("✅ Dependencies installed.")

def open_terminal(command, title):
    if system == "Windows":
        full_command = f'start cmd /k "title {title} && {venv_activate} && {command}"'
        subprocess.Popen(full_command, shell=True)
    elif system == "Linux":
        full_command = f"gnome-terminal -- bash -c 'source {venv_activate} && {command}; exec bash'"
        subprocess.Popen(full_command, shell=True)
    elif system == "Darwin":  # macOS
        full_command = f'osascript -e \'tell application "Terminal" to do script "source {venv_activate} && {command}"\''
        subprocess.Popen(full_command, shell=True)


open_terminal("main.py", "Vodu Dow")

