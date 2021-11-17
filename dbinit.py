from controllers.sql import SQLController
import json
from settings import data_path
from typing import List
import os.path as path


def read_words() -> List[dict]:
    with open(path.join(data_path, 'kaikki.org-dictionary-English.json'), 'rb') as fp:
        lines = fp.read().decode('utf8').split('\n')
        return [json.loads(line) for line in lines]
