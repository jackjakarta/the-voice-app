import os
import pygame
import time
import requests
from openai import OpenAI
from decouple import config

from modules.utility import load_json, save_json, RandomGenerator


class ChatGPT:
    """ChatGPT Class"""

    def __init__(self, model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=config("OPENAI_API_KEY"))
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
        chats_dir = "chats/"
        file = f"chat_{chat_name}.json"
        os.makedirs(chats_dir, exist_ok=True)
        save_json(os.path.join(chats_dir, file), json_data)

    def load_chat(self, chat_name):
        chats_dir = "chats/"
        file = f"chat_{chat_name}.json"
        os.makedirs(chats_dir, exist_ok=True)
        self.messages = load_json(os.path.join(chats_dir, file))

    @staticmethod
    def delete_chat(chat_name):
        chats_dir = "chats/"
        file = f"chat_{chat_name}.json"
        os.makedirs(chats_dir, exist_ok=True)
        os.remove(os.path.join(chats_dir, file))
        print("\nChat deleted successfully.")

    def set_system_message(self, system_prompt):
        self.messages = [{"role": "system", "content": system_prompt}]

    def get_models(self):
        models_list = self.client.models.list().data
        models = [x.id for x in models_list]

        return sorted(models)

    def speak(self):
        timestamp = RandomGenerator(8).random_string()
        speech_file_dir = "audio/"
        speech_file_name = f"openai_tts_{timestamp}.wav"
        os.makedirs(speech_file_dir, exist_ok=True)

        speech = self.client.audio.speech.create(
            model="tts-1-hd",
            voice="fable",
            input=self.completion.choices[0].message.content
        )

        speech.stream_to_file(os.path.join(speech_file_dir, speech_file_name))

        print("\nWait for Playback...")
        pygame.mixer.init()
        sound = pygame.mixer.Sound(os.path.join(speech_file_dir, speech_file_name))
        sound.play()
        time.sleep(sound.get_length())
        print(f"\nAudio saved to '{os.path.join(speech_file_dir, speech_file_name)}'.")


class ImageDallE:
    """Image Generation with the OpenAI DALL-E model."""

    def __init__(self, model="dall-e-3"):
        self.client = OpenAI(api_key=config("OPENAI_API_KEY"))
        self.model = model
        self.prompt = None
        self.response = None
        self.image_url = None

    def generate_image(self, prompt):
        self.prompt = prompt
        self.response = self.client.images.generate(
            model=self.model,
            prompt=self.prompt,
            size="1792x1024",
            quality="hd",
            n=1,
        )
        self.image_url = self.response.data[0].url

        return f"\nImage URL: {self.image_url}"

    def save_image(self, name=RandomGenerator(6).random_string()):
        request_response = requests.get(self.image_url, stream=True)
        if request_response.status_code == 200:
            timestamp = name
            image_dir = "images/"
            image_filename = f"image_{timestamp}.png"
            os.makedirs(image_dir, exist_ok=True)

            with open(os.path.join(image_dir, image_filename), "wb+") as f:
                for chunk in request_response.iter_content(8192):
                    f.write(chunk)
            print(f"\nImaged saved at: {image_dir}{image_filename}.")
        else:
            print("\nFailed to get image!")

    @staticmethod
    def delete_image(image_name):
        image_dir = "image_folder/"
        image_filename = f"image_{image_name}.png"
        os.remove(os.path.join(image_dir, image_filename))
        print("\nImage deleted successfully.")
