import subprocess
import time
import threading
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# --- Bot Reloader ---
class BotReloader(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.start_bot()

    def start_bot(self):
        print("[BOT] Starting bot...")
        self.process = subprocess.Popen(
            ["python", self.script],
            creationflags=subprocess.CREATE_NO_WINDOW  # Hides console window (Windows only)
        )

    def on_modified(self, event):
        if event.src_path.endswith(self.script):
            print("[BOT] Script changed. Restarting...")
            self.restart_bot()

    def restart_bot(self):
        self.process.kill()
        time.sleep(1)
        self.start_bot()

    def stop_bot(self):
        if self.process:
            print("[BOT] Stopping bot...")
            self.process.kill()

# --- Tray Icon ---
def create_tray_icon(reloader, observer):
    def exit_app(icon, item):
        icon.visible = False
        reloader.stop_bot()
        observer.stop()
        observer.join()
        icon.stop()
        sys.exit()

    def restart_bot(icon, item):
        reloader.restart_bot()

    # Create simple tray icon (red dot)
    icon_img = Image.new('RGB', (64, 64), color=(255, 0, 0))
    draw = ImageDraw.Draw(icon_img)
    draw.ellipse((16, 16, 48, 48), fill=(255, 255, 255))

    icon = Icon("TelegramBot", icon_img, "Telegram Bot", menu=Menu(
        MenuItem("Restart Bot", restart_bot),
        MenuItem("Exit", exit_app)
    ))

    return icon

# --- Main ---
def main():
    script_to_run = "main.py"

    # Start bot and watchdog
    reloader = BotReloader(script_to_run)
    observer = Observer()
    observer.schedule(reloader, ".", recursive=False)
    observer.start()

    # Run tray icon
    icon = create_tray_icon(reloader, observer)
    tray_thread = threading.Thread(target=icon.run)
    tray_thread.daemon = True
    tray_thread.start()

    print("[TRAY] Bot is running in background.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        reloader.stop_bot()
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
