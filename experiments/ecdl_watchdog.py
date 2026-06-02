import time
import subprocess
import os
from pathlib import Path

LOG_FILE = Path(r"d:\field\experiments") / time.strftime("%Y-%m-%d") / "orchestrator.log"
SCRIPT_PATH = Path(r"d:\field\06_Tools\ecdl_orchestrator.py")

def send_notification(title, message):
    ps_command = f"powershell -Command \"[Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('{message}', '{title}')\""
    # Note: MessageBox is blocking. For non-blocking toast:
    toast_command = f"powershell -Command \"Add-Type -AssemblyName System.Windows.Forms; $notify = New-Object System.Windows.Forms.NotifyIcon; $notify.Icon = [System.Drawing.SystemIcons]::Information; $notify.Visible = $true; $notify.ShowBalloonTip(5000, '{title}', '{message}', [System.Windows.Forms.ToolTipIcon]::Info)\""
    subprocess.Popen(toast_command, shell=True)

def check_progress():
    if not LOG_FILE.exists():
        return False
    
    last_mod = os.path.getmtime(LOG_FILE)
    if (time.time() - last_mod) > 300: # 5 minutes of silence
        return False
    return True

print("Watchdog started...")
while True:
    if not check_progress():
        print("Orchestrator seems stuck or not started. Restarting...")
        send_notification("ECDL Watchdog", "Restarting Orchestrator due to inactivity.")
        subprocess.Popen(["python", str(SCRIPT_PATH)], creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    time.sleep(300) # Check every 5 minutes
