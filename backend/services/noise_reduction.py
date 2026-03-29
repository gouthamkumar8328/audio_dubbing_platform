import subprocess

def denoise_audio(input_path, output_path):
    subprocess.run([
        "deepFilter", input_path, "-o", output_path
    ])
    return output_path