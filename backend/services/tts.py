from elevenlabs import generate, set_api_key

set_api_key("YOUR_API_KEY")

def generate_voice(text, voice, output_path):
    audio = generate(
        text=text,
        voice=voice,
        model="eleven_multilingual_v2"
    )

    with open(output_path, "wb") as f:
        f.write(audio)