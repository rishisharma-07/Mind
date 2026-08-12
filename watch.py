from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from convert import convert_video

import os
import time
from analyze import analyze_video

VIDEO_EXTENSIONS = (
    ".mp4",
    ".mkv",
    ".avi",
    ".webm",
    ".flv",
    ".m4v",
    ".wmv"
)

def wait_until_file_ready(file_path):
    previous_size = -1

    while True:

        try:
            current_size = os.path.getsize(file_path)

            if current_size == previous_size:
                return

            previous_size = current_size

            time.sleep(2)

        except PermissionError:
            time.sleep(2)

        except FileNotFoundError:
            return
        
class WatchHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        file_path = event.src_path

        if file_path.lower().endswith(VIDEO_EXTENSIONS):

            print("\n📥 New video detected!")
            print(os.path.basename(file_path))

            print("Waiting for file to finish copying...")

            wait_until_file_ready(file_path)

            print("Copy complete!")

            info = analyze_video(file_path)

            convert_video(file_path)
        
def start_watching():

    folder = "watch_folder"

    os.makedirs(folder, exist_ok=True)

    observer = Observer()

    observer.schedule(
        WatchHandler(),
        folder,
        recursive=False
    )

    observer.start()

    print("👀 Mind is watching the folder...")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    start_watching()