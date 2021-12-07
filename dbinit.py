from controllers.sql import SQLController
from controllers.ui import debug

import json
from settings import data_path
from typing import List
import os.path as path
from tqdm import tqdm


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
        cont.insert_record('old_english_words', tuples)


if __name__ == '__main__':
    initialize_database()
