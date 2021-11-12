import json
import pathlib
from typing import List, Tuple, Dict, Union
import enum
import random as rng
from tqdm import tqdm


poses = ['pron', 'prep', 'root', 'adv', 'det', 'verb', 'adj', 'noun', 'conj']


class POSEnum(enum.Enum):
    Noun = 0
    Adjective = 1
    Verb = 2
    Adverb = 3
    Preposition = 4


class DictionaryEntry:
    def __init__(self, name: str, pos: POSEnum, oe_equiv: str, innovation: bool, pg_equiv: str):
        self.name = name
        self.pos = pos
        self.oe_equiv = oe_equiv
        self.innovation = innovation
        self.pg_equiv = pg_equiv


def entry_from_json(s: str) -> Union[None, DictionaryEntry]:
    datum = json.loads(s)
    if 'translations' in datum:
        translations = [d['lang'] for d in datum['translations']]
        innovation = True
        if 'ang' in translations:
            trans = None
            for t in datum['translations']:
                if t['lang'] == 'ang':
                    trans = t
                    break
        return DictionaryEntry(datum['word'], POSEnum(datum['pos']), )
    return None


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

