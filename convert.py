import subprocess
import os
from notify import show_notification
# Path to FFmpeg
FFMPEG_PATH = os.path.join("ffmpeg", "ffmpeg.exe")


def convert_video(input_file):

    # Create output filename
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_folder, file_name + ".mov")

    # FFmpeg command
    command = [
        FFMPEG_PATH,
        "-i",
        input_file,
        output_file
    ]

    print("=" * 40)
    print("MIND")
    print("=" * 40)
    print(f"File: {os.path.basename(input_file)}")
    print("Status: Converting...")

    result = subprocess.run(
         command,
         stdout=subprocess.DEVNULL,
         stderr=subprocess.DEVNULL
)
    if result.returncode == 0:
        print("✅ Conversion Complete")
        print(f"Output: {os.path.basename(output_file)}")

        show_notification(
            "Mind",
            f"{os.path.basename(output_file)} is ready!"
        )

        return output_file

    else:
        print("❌ Conversion Failed")
        return None