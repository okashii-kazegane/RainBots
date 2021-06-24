import os
from pathlib import Path

from Rain.Common.Configs import Configs


class Greeting:
    def __init__(self, filename):
        self.greeting = ''
        self.filename = filename
        self.setup(self.greeting)

    def setup(self, greeting) -> None:
        if not os.path.exists(str(self.filename)):
            self.greeting = greeting
            os.makedirs(str(self.filename))
            with open(Path(self.filename, Configs.greetingFileName), 'w+') as greet_file:
                greet_file.write(self.greeting)

    def get(self) -> str:
        self.setup(self.greeting)
        with open(Path(self.filename, Configs.greetingFileName), 'r') as greet_file:
            self.greeting = greet_file.read()
        return self.greeting

    def update(self, greeting) -> None:
        self.greeting = greeting.replace('\\n', '\n')
        with open(Path(self.filename, Configs.greetingFileName), 'w+') as greet_file:
            greet_file.write(self.greeting)
