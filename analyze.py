import subprocess
import json
import os


def analyze_video(file_path):
    result = subprocess.run(
        [
            ".\\ffmpeg\\ffprobe.exe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            file_path
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {
            "error": result.stderr
        }

    data = json.loads(result.stdout)

    result_data = {
        "file": {
            "name": os.path.basename(file_path),
            "size": os.path.getsize(file_path),
            "format": data.get("format", {}).get("format_name"),
            "duration": data.get("format", {}).get("duration")
        },
        "video": [],
        "audio": [],
        "subtitles": []
    }

    for stream in data.get("streams", []):

        if stream.get("codec_type") == "video":
            result_data["video"].append({
                "codec": stream.get("codec_name"),
                "width": stream.get("width"),
                "height": stream.get("height"),
                "fps": stream.get("r_frame_rate"),
                "bitrate": stream.get("bit_rate"),
                "pixel_format": stream.get("pix_fmt")
            })

        elif stream.get("codec_type") == "audio":
            result_data["audio"].append({
                "codec": stream.get("codec_name"),
                "language": stream.get("tags", {}).get("language"),
                "channels": stream.get("channels"),
                "sample_rate": stream.get("sample_rate"),
                "bitrate": stream.get("bit_rate")
            })

        elif stream.get("codec_type") == "subtitle":
            result_data["subtitles"].append({
                "codec": stream.get("codec_name"),
                "language": stream.get("tags", {}).get("language"),
                "title": stream.get("tags", {}).get("title")
            })

    return result_data
