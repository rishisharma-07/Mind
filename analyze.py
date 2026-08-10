import subprocess
result=subprocess.run([".\\ffmpeg\\ffprobe.exe", "1.mp4"], capture_output=True, text=True)
print(result.stderr)