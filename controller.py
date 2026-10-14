# controller.py
import subprocess
import os
import webbrowser
import pyautogui
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Install extras:  pip install pyautogui pycaw comtypes pillow

# ── App launcher ──────────────────────────────────────────
APP_MAP = {
    "chrome":      r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox":     r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "notepad":     "notepad.exe",
    "calculator":  "calc.exe",
    "explorer":    "explorer.exe",
    "word":        r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel":       r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "spotify":     os.path.expanduser(r"~\AppData\Roaming\Spotify\Spotify.exe"),
    "vscode":      os.path.expanduser(r"~\AppData\Local\Programs\Microsoft VS Code\Code.exe"),
    "settings":    "ms-settings:",         # Windows Settings
    "task manager":"taskmgr.exe",
}

def open_app(name: str):
    name = name.lower().strip()
    path = APP_MAP.get(name)
    if path:
        if path.startswith("ms-"):
            os.startfile(path)
        else:
            subprocess.Popen([path])
        return f"Opening {name}."
    # Fallback: try to launch by name directly
    try:
        subprocess.Popen([name])
        return f"Trying to open {name}."
    except Exception:
        return f"I couldn't find {name} on your system."

# ── Web search ────────────────────────────────────────────
def search_web(query: str):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching for {query}."

def open_url(url: str):
    webbrowser.open(url)
    return f"Opening {url}."

# ── Volume control ────────────────────────────────────────
def _get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def set_volume(level: int):
    """level = 0-100"""
    vol = _get_volume_interface()
    vol.SetMasterVolumeLevelScalar(level / 100, None)
    return f"Volume set to {level}%."

def mute_volume():
    _get_volume_interface().SetMute(1, None)
    return "Muted."

def unmute_volume():
    _get_volume_interface().SetMute(0, None)
    return "Unmuted."

# ── Screen & keyboard ─────────────────────────────────────
def take_screenshot(path="screenshot.png"):
    img = pyautogui.screenshot()
    img.save(path)
    return f"Screenshot saved to {path}."

def type_text(text: str):
    time.sleep(0.5)
    pyautogui.typewrite(text, interval=0.04)
    return f"Typed: {text}"

def press_key(key: str):
    """e.g. 'enter', 'esc', 'ctrl+c', 'win'"""
    keys = key.split('+')
    if len(keys) > 1:
        pyautogui.hotkey(*keys)
    else:
        pyautogui.press(key)
    return f"Pressed {key}."

# ── System commands ───────────────────────────────────────
def shutdown():
    subprocess.run(["shutdown", "/s", "/t", "30"])
    return "Shutting down in 30 seconds."

def restart():
    subprocess.run(["shutdown", "/r", "/t", "30"])
    return "Restarting in 30 seconds."

def cancel_shutdown():
    subprocess.run(["shutdown", "/a"])
    return "Shutdown cancelled."

def lock_screen():
    subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
    return "Screen locked."

def list_running_apps():
    result = subprocess.run(["tasklist"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')[3:13]  # top 10 processes
    return "\n".join(lines)