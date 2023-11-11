import speech_recognition as sr
import pygame
import random
import string
import time
import requests
from openai import OpenAI

from modules.voices import Rachel
from keys import OPENAI_API_KEY, ELEVENLABS_API_KEY


class AudioRecorder:
    """Audio recorder that records audio from the default microphone."""
    def __init__(self):
        self.__recognizer = sr.Recognizer()
        self.__random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        self.file_name = f"audio/recording_{self.__random_string}.wav"

    def record(self):
        with sr.Microphone() as source:
            print("\nRecording audio...")
            audio = self.__recognizer.listen(source)

        with open(self.file_name, "wb") as file:
            file.write(audio.get_wav_data())
            print(f"Audio recorded and saved as 'recording_{self.__random_string}.wav' in 'audio/' folder!")


class AudioProcess:
    """Transcribe and Translate to EN text from audio file."""
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.file = None
        self.response_text = None
        self.model = "whisper-1"

    def transcribe(self, file):
        self.file = open(file, "rb")
        self.response_text = self.client.audio.transcriptions.create(model=self.model, file=self.file,
                                                                     response_format="text", language="en",
                                                                     temperature=0.3)

        return self.response_text

    def translate(self, file):
        self.file = open(file, "rb")
        self.response_text = self.client.audio.translations.create(model=self.model, file=self.file,
                                                                   response_format="text", temperature=0.3)

        return self.response_text


class TextToSpeech:
    """Text-To-Speech using ElevenLabs API."""
    def __init__(self, text, voice=Rachel):
        self.text = text
        self.voice = voice

    def play(self):
        chunk_size = 1024
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }

        data = {
            "text": self.text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        response = requests.post(url, json=data, headers=headers)
        timestamp = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        with open(f"audio/eleven_tts_{timestamp}.mp3", "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

        pygame.mixer.init()
        sound = pygame.mixer.Sound(f"audio/eleven_tts_{timestamp}.mp3")
        sound.play()
        time.sleep(sound.get_length())
        print(f"\nAudio saved to 'audio/eleven_tts_{timestamp}.mp3'.")
