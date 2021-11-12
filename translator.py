import json
import pathlib
from typing import List, Tuple
import enum
import random as rng


class POSEnum(enum.Enum):
    Noun = 0
    Adjective = 1
    Verb = 2
    Adverb = 3
    Preposition = 4


class WiktionaryController:
    def __init__(self, filepath: pathlib.Path):
        self.filename = filepath
        self.data = None
        self.prepared = False

    def prepare(self):
        print('Loading dictionary...')
        with open(self.filename, mode='r') as fp:
            self.data = json.load(fp)
        self.prepared = True
        print('Dictionary Loaded.')

    def sample(self, n: int = 1) -> List[Tuple[str, str, POSEnum]]:
        samples = rng.sample(self.data, n)

