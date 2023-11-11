import string
import random
import time
import json


class RandomGenerator:
    """Random String Generator. Default length is 10 characters."""
    def __init__(self, length=10):
        self.length = length

    def random_string(self):
        s = string.ascii_lowercase + string.digits
        o = "".join(random.choices(s, k=self.length))

        return o

    def random_digits(self):
        s = string.digits
        o = "".join(random.choices(s, k=self.length))

        return o

    def random_letters(self):
        s = string.ascii_letters
        o = "".join(random.choices(s, k=self.length))

        return o


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
            return "\nYou didn't called the start_timer() method before!"


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
