from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from pathlib import Path
import uuid
import subprocess
import warnings

warnings.filterwarnings('ignore')

print("\n" + "="*70)
print("AI AUDIO DUBBING PLATFORM (FIXED VERSION)")
print("Using: SpeechRecognition + Google Translate + gTTS")
print("="*70 + "\n")

app = FastAPI(title="AI Audio Dubbing", version="4.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("./uploads")
OUTPUT_DIR = Path("./outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

SUPPORTED_LANGUAGES = {
    "hindi": "hi",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "japanese": "ja",
    "arabic": "ar",
}

# ------------------ ASR ------------------
def transcribe_audio(audio_path: str) -> list:
    import speech_recognition as sr

    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    text = recognizer.recognize_google(audio)
    print(f"✓ Transcribed: {text[:100]}...")

    sentences = text.replace('?', '.').replace('!', '.').split('.')
    segments = []

    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if sentence:
            segments.append({
                'speaker': f"Speaker_{(i % 2) + 1}",
                'start': i * 2.0,
                'end': (i + 1) * 2.0,
                'text': sentence,
            })

    print(f"✓ Found {len(segments)} segments")
    return segments


# ------------------ TRANSLATION ------------------
from deep_translator import GoogleTranslator

def translate_text(text: str, target_lang: str) -> str:
    try:
        lang_map = {
            "hindi": "hi",
            "spanish": "es",
            "french": "fr",
            "german": "de",
            "japanese": "ja",
            "arabic": "ar"
        }

        target_code = lang_map.get(target_lang.lower(), "en")

        print(f"    🌐 Translating to {target_lang}...")

        translated = GoogleTranslator(
            source='auto',
            target=target_code
        ).translate(text)

        print(f"    ✓ Translated: {translated[:80]}...")
        return translated

    except Exception as e:
        print(f"    ❌ Translation failed: {e}")
        return text


# ------------------ TTS ------------------
def generate_speech(text: str, target_lang: str, speaker_id: str) -> str:
    from gtts import gTTS

    lang_map = {
        "hindi": "hi",
        "spanish": "es",
        "french": "fr",
        "german": "de",
        "japanese": "ja",
        "arabic": "ar"
    }

    lang_code = lang_map.get(target_lang, "en")

    output_mp3 = f"./outputs/tts_{uuid.uuid4()}.mp3"
    output_wav = output_mp3.replace('.mp3', '.wav')

    print(f"    🔊 Generating {lang_code} speech...")

    tts = gTTS(text=text, lang=lang_code, slow=False, tld="co.in")
    tts.save(output_mp3)

    subprocess.run([
        'ffmpeg', '-i', output_mp3,
        '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
        output_wav, '-y', '-loglevel', 'error'
    ], check=True)

    os.remove(output_mp3)

    return output_wav


# ------------------ API ------------------
@app.post("/dub")
async def dub_audio(file: UploadFile = File(...), target_language: str = Form(...)):
    try:
        if target_language.lower() not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail="Unsupported language")

        # Save file
        unique_filename = f"{uuid.uuid4()}{Path(file.filename).suffix}"
        input_path = UPLOAD_DIR / unique_filename

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        audio_path = str(input_path)

        # Convert to WAV
        if not audio_path.endswith('.wav'):
            wav_path = audio_path.replace(Path(audio_path).suffix, '.wav')
            subprocess.run([
                'ffmpeg', '-i', audio_path,
                '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
                wav_path, '-y', '-loglevel', 'error'
            ], check=True)
            audio_path = wav_path

        print(f"\n📁 Processing: {file.filename}")

        segments = transcribe_audio(audio_path)

        dubbed_segments = []

        for i, seg in enumerate(segments):
            print(f"\nSegment {i+1}:")
            text = seg['text']

            translated = translate_text(text, target_language.lower())

            dubbed_audio = generate_speech(
                translated,
                target_language.lower(),
                seg['speaker']
            )

            dubbed_segments.append(dubbed_audio)

        if not dubbed_segments:
            raise Exception("No audio generated")

        # 🔥 MERGE AUDIO FILES
        final_audio = f"./outputs/final_{uuid.uuid4()}.wav"
        concat_file = f"./outputs/concat_{uuid.uuid4()}.txt"

        with open(concat_file, "w") as f:
            for audio in dubbed_segments:
                f.write(f"file '{os.path.abspath(audio)}'\n")

        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            final_audio
        ], check=True)

        os.remove(concat_file)

        return {
            "success": True,
            "output_file": os.path.basename(final_audio),
            "download_url": f"/download/{os.path.basename(final_audio)}",
            "segments": len(dubbed_segments)
        }

    except Exception as e:
        print("❌ ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
async def download(filename: str):
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, media_type="audio/wav", filename=filename)


@app.get("/")
async def root():
    return {"message": "AI Dubbing API Running 🚀"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)