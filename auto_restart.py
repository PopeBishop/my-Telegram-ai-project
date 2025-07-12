import subprocess
import sys
import time
import os
import fcntl  # For OS-level locking
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ✅ OS-level lock file (prevents duplicates reliably)
lock_file_path = "/tmp/auto_restart.lock"
lock_file = open(lock_file_path, "w")

try:
    fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    print("🚫 auto_restart.py is already running.")
    sys.exit(0)

print(f"✅ auto_restart.py is running with PID {os.getpid()}")


# 📂 Watchdog handler
class RestartOnChange(FileSystemEventHandler):
    def __init__(self, script_path):
        self.script_path = script_path
        self.process = None
        self.restart_script()

    def restart_script(self):
        if self.process:
            print("🔄 Restarting script...")
            self.process.terminate()
            self.process.wait()
        print("🚀 Starting script...")
        self.process = subprocess.Popen([sys.executable, self.script_path])

    def on_modified(self, event):
        if event.src_path.endswith(self.script_path):
            print(f"🔍 Detected change in {event.src_path}")
            self.restart_script()

# 🏁 Main logic
if __name__ == "__main__":
    script_to_watch = "bot.py"
    event_handler = RestartOnChange(script_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    print(f"👁️ Watching {script_to_watch} for changes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.terminate()
    observer.join()
