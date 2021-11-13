import pathlib
from typing import List, Tuple
from tqdm import tqdm
import re


def read_phrases(path: pathlib.Path) -> List[Tuple[str, str]]:
    result = []
    with open(path, 'rb') as fp:
        data = fp.read()
        lines = data.decode('utf8').split('\n')
        for i in tqdm(range(0, len(lines) - 2, 3)):
            oe_sentences = re.split(r'[."]', lines[i])
            ne_sentences = re.split(r'[."]', lines[i + 1])
            for oe, ne in zip(oe_sentences, ne_sentences):
                if len(oe) > 2 and len(ne) > 2:
                    result.append((oe.strip().strip(',:'), ne.strip().strip(',:')))
    return result


if __name__ == '__main__':
    phrases = read_phrases('./data/phrases.txt')
    print(phrases)
