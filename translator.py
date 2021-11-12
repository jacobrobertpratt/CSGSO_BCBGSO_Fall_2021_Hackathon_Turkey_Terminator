import json
import pathlib
from typing import List, Tuple, Dict, Union
import random as rng
from tqdm import tqdm
import re


poses = ['pron', 'prep', 'root', 'adv', 'det', 'verb', 'adj', 'noun', 'conj']


class DictionaryEntry:
    def __init__(self, name: str, pos: str, oe_equiv: str, innovation: bool, pg_equiv: str, pie_equiv: str):
        self.name = name
        self.pos = pos
        self.oe_equiv = oe_equiv
        self.innovation = innovation
        self.pg_equiv = pg_equiv
        self.pie_equiv = pie_equiv

    def __repr__(self):
        return '{}[{}] <- {} <- {} <- {}'.format(self.name, self.pos, self.oe_equiv, self.pg_equiv, self.pie_equiv)


def entry_from_json(s: str) -> Union[None, DictionaryEntry]:
    datum = json.loads(s)
    innovation = True
    oe_equiv = ''
    pg_equiv = ''
    pie_equiv = ''
    if 'etymology_text' in datum:
        if 'from old english' in datum['etymology_text'].lower():
            innovation = False
            m = re.search(r'Old English \*?(?P<oe>[^ ,]+)', datum['etymology_text'])
            if m is not None:
                oe_equiv = m.group('oe')
            if 'from proto-germanic' in datum['etymology_text'].lower():
                m = re.search(r'Proto-Germanic \*?(?P<pg>[^ ,]+)', datum['etymology_text'])
                if m is not None:
                    pg_equiv = m.group('pg')
            if 'from proto-indo-european' in datum['etymology_text'].lower():
                m = re.search(r'Proto-Indo-European \*?(?P<pie>[^ ,]+)', datum['etymology_text'])
                if m is not None:
                    pie_equiv = m.group('pie')
        return DictionaryEntry(datum['word'], datum['pos'], oe_equiv, innovation, pg_equiv, pie_equiv)
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

    def sample(self, n: int = 1) -> List[DictionaryEntry]:
        if self.data:
            return rng.sample([d for d in self.data if not d.innovation], n)
        return []


if __name__ == '__main__':
    # Data Preprocessing
    w = WiktionaryController('./data/kaikki.org-dictionary-English.json')
    w.prepare()
    print('Writing CSV file...')
    with open('./data/reduced_data.csv', 'wb+') as fp:
        fp.write('modern_english,old_english,proto_germanic,proto_indo_european,pos,innovation\n'.encode('utf8'))
        fp.writelines(['"{}","{}","{}","{}","{}",{}\n'.format(d.name, d.oe_equiv, d.pg_equiv, d.pie_equiv,
                                                              d.pos,  d.innovation).encode('utf8') for d in w.data])
    print('\n'.join(repr(d) for d in w.sample(100)))
