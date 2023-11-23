import speech_recognition as sr
import pygame
import random
import string
import time
import requests
import os
from openai import OpenAI
from decouple import config

from modules.voices import Rachel


class AudioRecorder:
    """Audio recorder that records audio from the default microphone."""
    def __init__(self):
        self.__recognizer = sr.Recognizer()
        self.__random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        self.audio_dir = "audio/"
        self.file_name = f"recording_{self.__random_string}.wav"
        os.makedirs(self.audio_dir, exist_ok=True)

    def record(self):
        with sr.Microphone() as source:
            print("\nRecording audio...")
            audio = self.__recognizer.listen(source)

        with open(os.path.join(self.audio_dir, self.file_name), "wb+") as file:
            file.write(audio.get_wav_data())
            print(f"Audio recorded and saved as '{self.file_name}' in '{self.audio_dir}' folder!")


class AudioProcess:
    """Transcribe and Translate to EN text from audio file."""
    def __init__(self):
        self.client = OpenAI(api_key=config("OPENAI_API_KEY"))
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

        timestamp = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        self.audio_dir = "audio/"
        self.file_name = f"eleven_tts_{timestamp}.mp3"
        os.makedirs(self.audio_dir, exist_ok=True)

    def generate(self):
        chunk_size = 1024
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": config("ELEVENLABS_API_KEY")
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

        with open(os.path.join(self.audio_dir, self.file_name), "wb+") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

        print(f"\nAudio saved to '{self.audio_dir}{self.file_name}'.")

    def play(self):
        print("\nWait for playback...")
        pygame.mixer.init()
        sound = pygame.mixer.Sound(os.path.join(self.audio_dir, self.file_name))
        sound.play()
        time.sleep(sound.get_length())
