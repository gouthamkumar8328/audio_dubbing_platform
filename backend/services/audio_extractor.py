import subprocess

def extract_audio(video_path, output_audio):
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le",
        output_audio
    ])
    return output_audio