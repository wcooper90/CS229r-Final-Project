import random
from .config import CONFIGURATION


class Environment:

    def __init__(self):
        self.config = CONFIGURATION()

    def generate_environment(self):
        number = f'{random.getrandbits(32):=032b}'
        return  number
