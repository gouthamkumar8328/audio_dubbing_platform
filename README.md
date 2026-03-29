# AI Audio Dubbing Platform

## Overview

An end-to-end AI-powered audio dubbing platform that converts speech from a source language into a target language while preserving timing, structure, and natural flow.

The system processes audio or video input, performs transcription, translation, and speech synthesis, and generates a synchronized dubbed output.

---

## Key Features

* Automatic Speech Recognition (ASR)
* Multilingual Translation
* Text-to-Speech (TTS)
* Multi-speaker simulation
* Audio alignment and merging
* Supports MP3, WAV, and MP4 formats
* FastAPI backend with React frontend

---

## System Architecture

```
                +------------------+
                |   Input Media    |
                | (Audio / Video)  |
                +--------+---------+
                         |
                         v
                +------------------+
                | Audio Extraction |
                |    (FFmpeg)      |
                +--------+---------+
                         |
                         v
                +------------------+
                |       ASR        |
                | SpeechRecognition|
                +--------+---------+
                         |
                         v
                +------------------+
                |   Translation    |
                | Google Translator|
                +--------+---------+
                         |
                         v
                +------------------+
                |       TTS        |
                |      gTTS        |
                +--------+---------+
                         |
                         v
                +------------------+
                | Audio Merging    |
                |     FFmpeg       |
                +--------+---------+
                         |
                         v
                +------------------+
                |  Dubbed Output   |
                +------------------+
```

---

## Workflow

1. Upload audio or video file
2. Extract audio using FFmpeg
3. Convert speech to text using ASR
4. Translate text into the target language
5. Convert translated text to speech
6. Merge all generated audio segments
7. Produce the final dubbed output

---

## Tech Stack

### Backend

* FastAPI
* Python

### Frontend

* React.js
* Tailwind CSS

### AI and Processing

* SpeechRecognition (ASR)
* deep-translator (Translation)
* gTTS (Text-to-Speech)

### Tools

* FFmpeg (Audio processing)

---

## Project Structure

```
audio_dubbing_platform/
│
├── backend/
│   ├── main.py
│   ├── uploads/
│   ├── outputs/
│
├── frontend/
│   ├── src/
│   ├── components/
│
├── README.md
└── requirements.txt
```

---

## How to Run

### Backend

```
cd backend
pip install -r requirements.txt
python main.py
```

---

### Frontend

```
cd frontend
npm install
npm run dev
```

---

## API Endpoints

| Method | Endpoint             | Description                           |
| ------ | -------------------- | ------------------------------------- |
| POST   | /dub                 | Upload file and generate dubbed audio |
| GET    | /download/{filename} | Download output audio                 |

---

## Demo Flow

* Upload media file
* Select target language
* Process dubbing
* Download translated audio

---

## Future Enhancements

* Speaker diarization
* Voice cloning
* Lip-sync alignment
* Real-time dubbing
* Expanded language support

---

## Author

Goutham Kumar

---

## Acknowledgements

* Open-source AI tools
* FFmpeg community
* FastAPI ecosystem
