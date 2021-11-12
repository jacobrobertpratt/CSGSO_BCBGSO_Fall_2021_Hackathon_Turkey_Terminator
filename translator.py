import json
import pathlib
from typing import List, Tuple, Dict, Union
import random as rng
from tqdm import tqdm


poses = ['pron', 'prep', 'root', 'adv', 'det', 'verb', 'adj', 'noun', 'conj']


class DictionaryEntry:
    def __init__(self, name: str, pos: str, oe_equiv: str, innovation: bool, pg_equiv: str):
        self.name = name
        self.pos = pos
        self.oe_equiv = oe_equiv
        self.innovation = innovation
        self.pg_equiv = pg_equiv


def entry_from_json(s: str) -> Union[None, DictionaryEntry]:
    datum = json.loads(s)
    if 'translations' in datum and datum['pos'] in poses:
        translations = [d['lang'] for d in datum['translations']]
        innovation = True
        oe_equiv = ''
        pg_equiv = ''
        if 'ang' in translations:
            trans = None
            for t in datum['translations']:
                if t['lang'] == 'ang':
                    trans = t
                    break
            oe_equiv = trans['word']
            innovation = False
            if 'gem-pro' in translations:
                trans = None
                for t in datum['translations']:
                    if t['lang'] == 'gem-pro':
                        trans = t
                        break
                pg_equiv = trans['word']
        return DictionaryEntry(datum['word'], datum['pos'], oe_equiv, innovation, pg_equiv)
    return None


class WiktionaryController:
    def __init__(self, filepath: pathlib.Path):
        self.filename = filepath
        self.data = None
        self.prepared = False

    def prepare(self):
        print('Loading dictionary...')
        with open(self.filename, mode='r') as fp:
            self.data = [d for d in [entry_from_json(line) for line in tqdm(fp.readlines())] if d is not None]
        self.prepared = True
        print('Dictionary Loaded.')

