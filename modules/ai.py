import os
import pygame
import time
import requests
from openai import OpenAI

from modules.utility import load_json, save_json, RandomGenerator
from keys import OPENAI_API_KEY


class ChatGPT:
    """ChatGPT Class"""

    def __init__(self, model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        self.messages = [
            {
                "role": "system",
                "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as "
                           "possible."
            }
        ]
        self.prompt = None
        self.completion = None

    def ask(self, prompt):
        self.prompt = prompt

        if self.prompt:
            self.messages.append(
                {"role": "user", "content": self.prompt}
            )

        self.completion = self.client.chat.completions.create(model=self.model, messages=self.messages)
        self.messages.append({"role": "assistant", "content": str(self.completion.choices[0].message.content)})

        return self.completion.choices[0].message.content

    def clear_chat(self):
        self.messages = [
            {
                "role": "system",
                "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as "
                           "possible."
            }
        ]

        # return "\nChat reset successfully!"

    def save_chat(self, chat_name):
        json_data = self.messages
        file = f"data/chat_{chat_name}.json"
        save_json(file, json_data)

    def load_chat(self, file):
        self.messages = load_json(file)

    @staticmethod
    def delete_chat(chat_name):
        script_path = f"data/chat_{chat_name}.json"
        os.remove(script_path)
        print("\nChat deleted successfully.")

    def set_system_message(self, system_prompt):
        self.messages = [{"role": "system", "content": system_prompt}]

    def get_models(self):
        models_list = self.client.models.list().data
        models = [x.id for x in models_list]

        return sorted(models)

    def speak(self):
        timestamp = RandomGenerator(8).random_string()
        speech_file_path = f"audio/openai_tts_{timestamp}.wav"
        speech = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=self.completion.choices[0].message.content
        )

        speech.stream_to_file(speech_file_path)

        print("\nWait for Playback...")
        pygame.mixer.init()
        sound = pygame.mixer.Sound(speech_file_path)
        sound.play()
        time.sleep(sound.get_length())
        print(f"\nAudio saved to '{speech_file_path}'.")


class ImageDallE:
    """Image Generation with the OpenAI DALL-E model."""

    def __init__(self, model="dall-e-3"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        self.prompt = None
        self.response = None
        self.image_url = None

    def generate_image(self, prompt):
        self.prompt = prompt
        self.response = self.client.images.generate(
            model=self.model,
            prompt=self.prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        self.image_url = self.response.data[0].url

        return f"\nImage URL: {self.image_url}"

    def save_image(self, name=RandomGenerator(6).random_string()):
        request_response = requests.get(self.image_url, stream=True)
        try:
            if request_response.status_code == 200:
                timestamp = name
                image_filename = f"image_folder/image_{timestamp}.png"

                with open(image_filename, "wb") as f:
                    for chunk in request_response.iter_content(8192):
                        f.write(chunk)
                print(f"\nImaged saved at: {image_filename}.")
            else:
                print("\nFailed to get image!")
        except FileNotFoundError:
            print("\nFile not saved! Create a directory called 'image_folder'.")

    @staticmethod
    def delete_image(image_name):
        image_path = f"image_folder/image_{image_name}.png"
        os.remove(image_path)
        print("\nImage deleted successfully.")
