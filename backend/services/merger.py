import subprocess

def merge_audio(file_list_path, output_path):
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", file_list_path,
        "-c", "copy",
        output_path
    ])