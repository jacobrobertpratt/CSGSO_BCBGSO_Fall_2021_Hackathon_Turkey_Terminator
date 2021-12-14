from controllers.sql import SQLController
from controllers.ui import debug
from utils.grammar import noun_declensions, case_list, plurality_list

import json
from settings import data_path
from typing import List, Tuple, Dict
import os.path as path
from tqdm import tqdm
import re


etymology_names = ['inh', 'der']
language_codes = ['ang', 'en']


def initialize_database():
    cont = SQLController.get_instance()
    cont.reset_database()

    debug('Reading English Words')
    with open(path.join(data_path, 'kaikki.org-dictionary-English.json'), 'rb') as fp:
        lines = fp.read().decode('utf8').split('\n')
        tuples = []
        for li, line in enumerate(tqdm(lines[:-1])):
            j = json.loads(line)
            name = '"{}"'.format(j['word'].replace('"', "'"))
            pos = '"{}"'.format(j['pos'].replace('"', "'"))
            for sense in j['senses']:
                conj = True
                if 'form_of' not in sense:
                    conj = False
                definition = '"{}"'.format(
                    ('. '.join(sense['glosses']) if 'glosses' in sense else '').replace('"', "'"))
                tuples.append((name, pos, definition, li, conj))
        cont.insert_record('english_words', tuples)

    debug('Reading Old English Words')
    with open(path.join(data_path, 'kaikki.org-dictionary-OldEnglish.json'), 'rb') as fp:
        lines = fp.read().decode('utf8').split('\n')
        tuples = []
        declensions = []
        for li, line in enumerate(tqdm(lines[:-1])):
            j = json.loads(line)
            name = '"{}"'.format(j['word'].replace('"', "'"))
            pos = '"{}"'.format(j['pos'].replace('"', "'"))
            for sense in j['senses']:
                conj = True
                if 'form_of' not in sense:
                    conj = False
                else:
                    # Detect Declensions
                    if j['pos'] == 'noun':
                        cases = find_declensions(sense['tags'])
                        for c, p in cases:
                            for f in sense['form_of']:
                                debug('{} is the {} {} form of {}'.format(name, c, p, f['word']))
                                declensions.append((f['word'], c, p))
                definition = '"{}"'.format(
                    ('. '.join(sense['glosses']) if 'glosses' in sense else '').replace('"', "'"))
                tuples.append((name, pos, definition, li, conj))
        cont.insert_record('old_english_words', tuples)

        # Insert Declensions


def find_declensions(sense: List[str]) -> List[Tuple[str, str]]:
    cases = []
    pluralities = []
    for tag in sense:
        if tag in case_list:
            cases.append(tag)

        if tag in plurality_list:
            pluralities.append(tag)

    tuples = []
    for c in cases:
        for p in pluralities:
            tuples.append((c, p))

    return tuples


def insert_declensions(declensions: List[Tuple[str, str, str]]):
    cont = SQLController.get_instance()

    debug('Inserting Noun Declension Table')
    words = list(set(['"{}"'.format(d[0].replace('"', "'")) for d in declensions]))
    where_clause = 'name in ({})'.format(','.join(words)) if len(words) > 1 else 'name = {}'.format(words[0])
    indices = cont.select_conditional('old_english_words', 'id, name', where_clause)

    debug('Generating foreign key dictionary')
    index_dict = {}
    for index, name in indices:
        if name not in index_dict:
            index_dict[name] = index

    debug('linking...')
    cont.insert_record('declensions', [(index_dict[w], p, c) for w, p, c in declensions])


if __name__ == '__main__':
    initialize_database()
