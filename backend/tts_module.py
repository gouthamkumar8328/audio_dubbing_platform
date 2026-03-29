"""
Text-to-Speech Module with Multiple Provider Support
- ElevenLabs (with newer models)
- Google Cloud TTS
- Azure TTS
- gTTS (Free fallback)
"""

import os
import subprocess
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')


class TTSProvider:
    """Base TTS Provider"""
    
    @staticmethod
    def generate_speech(text: str, target_lang: str, speaker_id: str = "1") -> str:
        raise NotImplementedError


class ElevenLabsTTS(TTSProvider):
    """ElevenLabs TTS - Updated to use latest models"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
        
        # Standard voice IDs that work on all tiers
        self.voice_map = {
            "Speaker_1": "21m00Tcm4TlvDq8ikWAM",  # Rachel
            "Speaker_2": "AZnzlk1XvdvUeBnXmlld",  # Adam
            "Speaker_3": "EXAVITQu4vr4xnSDxMaL",  # Bella
        }
        
        if not api_key or len(api_key.strip()) == 0:
            raise Exception("ElevenLabs API key is empty")
        
        print(f"✓ ElevenLabs initialized")
    
    def generate_speech(self, text: str, target_lang: str, speaker_id: str = "1") -> str:
        """Generate speech using ElevenLabs with latest models"""
        try:
            import requests
            
            if not text or len(text.strip()) == 0:
                return ""
            
            print(f"    🔊 ElevenLabs: Generating natural voice...")
            
            voice_id = self.voice_map.get(speaker_id, "21m00Tcm4TlvDq8ikWAM")
            
            output_mp3 = f"./outputs/tts_{speaker_id}_{target_lang}_{abs(hash(text[:20]))}.mp3"
            os.makedirs("./outputs", exist_ok=True)
            
            # Use the latest TTS model (not deprecated)
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            headers = {
                "xi-api-key": self.api_key.strip(),
                "Content-Type": "application/json"
            }
            
            # Limit text
            text_to_send = text[:1000] if len(text) > 1000 else text
            
            # Use latest model
            data = {
                "text": text_to_send,
                "model_id": "eleven_multilingual_v2",  # Latest model
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                with open(output_mp3, 'wb') as f:
                    f.write(response.content)
                
                # Convert to WAV
                wav_output = output_mp3.replace('.mp3', '.wav')
                cmd = [
                    'ffmpeg', '-i', output_mp3,
                    '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
                    wav_output, '-y', '-loglevel', 'error'
                ]
                subprocess.run(cmd, check=True, capture_output=True, timeout=30)
                
                if os.path.exists(output_mp3):
                    os.remove(output_mp3)
                
                print(f"    ✓ ElevenLabs voice generated")
                return wav_output
            else:
                error_msg = response.text[:200] if response.text else str(response.status_code)
                print(f"    ⚠️ ElevenLabs error: {response.status_code}")
                
                # If model not available, try standard model
                if "model" in error_msg.lower() or response.status_code == 401:
                    print(f"    Retrying with standard model...")
                    data["model_id"] = "eleven_monolingual_v1"
                    response = requests.post(url, json=data, headers=headers, timeout=30)
                    
                    if response.status_code == 200:
                        with open(output_mp3, 'wb') as f:
                            f.write(response.content)
                        
                        wav_output = output_mp3.replace('.mp3', '.wav')
                        cmd = [
                            'ffmpeg', '-i', output_mp3,
                            '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
                            wav_output, '-y', '-loglevel', 'error'
                        ]
                        subprocess.run(cmd, check=True, capture_output=True, timeout=30)
                        
                        if os.path.exists(output_mp3):
                            os.remove(output_mp3)
                        
                        print(f"    ✓ ElevenLabs voice generated (standard model)")
                        return wav_output
                
                return ""
        
        except Exception as e:
            print(f"    ⚠️ ElevenLabs exception: {e}")
            return ""


class GoogleCloudTTS(TTSProvider):
    """Google Cloud Text-to-Speech - Free tier available"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        if api_key and os.path.isfile(api_key):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key
    
    def generate_speech(self, text: str, target_lang: str, speaker_id: str = "1") -> str:
        """Generate speech using Google Cloud TTS"""
        try:
            from google.cloud import texttospeech
            
            if not text or len(text.strip()) == 0:
                return ""
            
            print(f"    🔊 Google Cloud TTS: Generating voice...")
            
            client = texttospeech.TextToSpeechClient()
            
            # Language codes
            lang_codes = {
                'hi': 'hi-IN',
                'es': 'es-ES',
                'fr': 'fr-FR',
                'de': 'de-DE',
                'ja': 'ja-JP',
                'ar': 'ar-SA',
            }
            
            lang_code = lang_codes.get(target_lang, 'en-US')
            
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=lang_code,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16
            )
            
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            output_wav = f"./outputs/tts_{speaker_id}_{target_lang}_{abs(hash(text[:20]))}.wav"
            os.makedirs("./outputs", exist_ok=True)
            
            with open(output_wav, 'wb') as out:
                out.write(response.audio_content)
            
            print(f"    ✓ Google Cloud voice generated")
            return output_wav
        
        except Exception as e:
            print(f"    ⚠️ Google Cloud error: {e}")
            return ""


class AzureTTS(TTSProvider):
    """Microsoft Azure Cognitive Services TTS - Free tier available"""
    
    def __init__(self, api_key: str, region: str = "eastus"):
        self.api_key = api_key
        self.region = region
    
    def generate_speech(self, text: str, target_lang: str, speaker_id: str = "1") -> str:
        """Generate speech using Azure TTS"""
        try:
            import requests
            
            if not text or len(text.strip()) == 0:
                return ""
            
            print(f"    🔊 Azure TTS: Generating voice...")
            
            url = f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"
            
            headers = {
                'Ocp-Apim-Subscription-Key': self.api_key,
                'Content-Type': 'application/ssml+xml',
                'X-Microsoft-OutputFormat': 'audio-16khz-32kbitrate-mono-mp3'
            }
            
            voice_map = {
                'hi': 'hi-IN-MadhurNeural',
                'es': 'es-ES-AlvaroNeural',
                'fr': 'fr-FR-HenriNeural',
                'de': 'de-DE-ConradNeural',
                'ja': 'ja-JP-KeitaNeural',
                'ar': 'ar-SA-HamedNeural',
            }
            
            voice = voice_map.get(target_lang, 'en-US-AriaNeural')
            
            ssml_text = f"""
            <speak version='1.0' xml:lang='en-US'>
                <voice name='{voice}'>
                    {text}
                </voice>
            </speak>
            """
            
            response = requests.post(url, headers=headers, data=ssml_text.encode('utf-8'), timeout=30)
            
            if response.status_code == 200:
                output_mp3 = f"./outputs/tts_{speaker_id}_{target_lang}_{abs(hash(text[:20]))}.mp3"
                output_wav = output_mp3.replace('.mp3', '.wav')
                os.makedirs("./outputs", exist_ok=True)
                
                with open(output_mp3, 'wb') as f:
                    f.write(response.content)
                
                cmd = [
                    'ffmpeg', '-i', output_mp3,
                    '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
                    output_wav, '-y', '-loglevel', 'error'
                ]
                subprocess.run(cmd, check=True, capture_output=True, timeout=30)
                
                if os.path.exists(output_mp3):
                    os.remove(output_mp3)
                
                print(f"    ✓ Azure voice generated")
                return output_wav
            else:
                print(f"    ⚠️ Azure error: {response.status_code}")
                return ""
        
        except Exception as e:
            print(f"    ⚠️ Azure error: {e}")
            return ""


class ImprovedGTTS(TTSProvider):
    """Improved gTTS with better quality settings"""
    
    def generate_speech(self, text: str, target_lang: str, speaker_id: str = "1") -> str:
        """Generate speech using improved gTTS"""
        try:
            from gtts import gTTS
            
            if not text or len(text.strip()) == 0:
                return ""
            
            print(f"    🔊 Using improved gTTS...")
            
            lang_map = {
                'hi': 'hi', 'es': 'es', 'fr': 'fr',
                'de': 'de', 'ja': 'ja', 'ar': 'ar',
            }
            
            lang_code = lang_map.get(target_lang, 'en')
            
            output_mp3 = f"./outputs/tts_{speaker_id}_{target_lang}_{abs(hash(text[:20]))}.mp3"
            output_wav = output_mp3.replace('.mp3', '.wav')
            
            os.makedirs("./outputs", exist_ok=True)
            
            # Generate with better settings
            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(output_mp3)
            
            # Convert to WAV
            cmd = [
                'ffmpeg', '-i', output_mp3,
                '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
                output_wav, '-y', '-loglevel', 'error'
            ]
            subprocess.run(cmd, check=True, capture_output=True, timeout=30)
            
            if os.path.exists(output_mp3):
                os.remove(output_mp3)
            
            print(f"    ✓ gTTS voice generated")
            return output_wav
        
        except Exception as e:
            print(f"    ⚠️ gTTS error: {e}")
            return ""


class TTSManager:
    """Manages TTS provider selection and fallback"""
    
    def __init__(self, provider: str = "elevenlabs", api_key: str = None):
        self.provider = provider.lower() if provider else "gtts"
        self.api_key = api_key
        self.tts = self._init_provider()
        self.fallback_tts = ImprovedGTTS()  # Always have gTTS as fallback
    
    def _init_provider(self):
        """Initialize TTS provider"""
        
        if self.provider == "elevenlabs":
            if self.api_key and len(self.api_key.strip()) > 0:
                try:
                    print("✓ Initializing ElevenLabs TTS")
                    return ElevenLabsTTS(self.api_key)
                except Exception as e:
                    print(f"⚠️ ElevenLabs init failed: {e}, using gTTS")
                    return ImprovedGTTS()
            else:
                print("⚠️ ElevenLabs API key not provided, using gTTS")
                return ImprovedGTTS()
        
        elif self.provider == "google" and self.api_key:
            print("✓ Using Google Cloud TTS")
            return GoogleCloudTTS(self.api_key)
        
        elif self.provider == "azure" and self.api_key:
            print("✓ Using Azure TTS")
            return AzureTTS(self.api_key)
        
        else:
            print("✓ Using gTTS (Free)")
            return ImprovedGTTS()
    
    def generate_speech(self, text: str, target_lang: str, speaker_id: str = "1") -> str:
        """Generate speech with smart fallback"""
        try:
            result = self.tts.generate_speech(text, target_lang, speaker_id)
            if result and os.path.exists(result):
                return result
        except Exception as e:
            print(f"⚠️ Primary TTS failed: {e}")
        
        # Always fall back to gTTS
        print("    ⚠️ Falling back to free gTTS...")
        return self.fallback_tts.generate_speech(text, target_lang, speaker_id)


__all__ = ['TTSManager', 'ElevenLabsTTS', 'GoogleCloudTTS', 'AzureTTS', 'ImprovedGTTS']