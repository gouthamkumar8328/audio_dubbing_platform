import whisper

model = whisper.load_model("medium")

def transcribe(audio_path):
    result = model.transcribe(audio_path)
    return result["segments"]