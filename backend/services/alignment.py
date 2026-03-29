import subprocess

def adjust_audio(input_audio, output_audio, speed):
    subprocess.run([
        "ffmpeg", "-y", "-i", input_audio,
        "-filter:a", f"atempo={speed}",
        output_audio
    ])