import string
import random
import time
import json
from datetime import datetime, timezone, timedelta


class RandomGenerator:
    """Random String Generator. Default length is 10 characters."""
    def __init__(self):
        self.length = None

    def random_string(self, length=6):
        self.length = length

        characters = string.ascii_lowercase + string.digits
        random_generate = "".join(random.choices(characters, k=self.length))

        return random_generate

    def random_digits(self, length=6):
        self.length = length

        characters = string.digits
        random_generate = "".join(random.choices(characters, k=self.length))

        return random_generate

    def random_letters(self, length=6):
        self.length = length

        characters = string.ascii_letters
        random_generate = "".join(random.choices(characters, k=self.length))

        return random_generate

    @staticmethod
    def timestamp():
        timestamp = time.time()
        time_zone = timezone(timedelta(hours=1))  # Adjust time zone
        datetime_obj = datetime.fromtimestamp(timestamp, tz=time_zone)
        formatted_date = datetime_obj.strftime('%d-%m-%Y')
        formatted_time = datetime_obj.strftime('%H-%M')

        timestamp_formatted = f"{formatted_date}_{formatted_time}"

        return timestamp_formatted


class Duration:
    """Calculates the duration of a process"""
    def __init__(self):
        self.start_time = None
        self.duration = None

    def start_timer(self):
        self.start_time = time.time()

    def get_duration(self):
        try:
            end_time = time.time()
            self.duration = end_time - self.start_time

            return f"\nIt took {self.duration:.2f} seconds to complete the task."
        except TypeError:
            return "\nYou didn't call the start_timer() method before!"


def load_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def save_to_text(file, content):
    with open(file, "a") as f:
        f.write(content)
        print(f"Data saved to {file} file!")
