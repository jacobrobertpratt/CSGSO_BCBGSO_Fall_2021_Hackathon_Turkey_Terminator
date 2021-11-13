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
            oe_sentences = re.split(r'[.";?!]', lines[i])
            ne_sentences = re.split(r'[.";?!]', lines[i + 1])
            for oe, ne in zip(oe_sentences, ne_sentences):
                if len(oe) > 2 and len(ne) > 2:
                    result.append((oe.strip().strip(',:'), ne.strip().strip(',:')))
    return result


def write_phrases(phrases: List[Tuple[str, str]], path: pathlib.Path):
    with open(path, 'wb+') as fp:
        for oe, ne in phrases:
            fp.write((oe + '\n').encode('utf8'))
            fp.write((ne + '\n\n').encode('utf8'))


if __name__ == '__main__':
    phrases = read_phrases('./data/phrases.txt')
    write_phrases(phrases, './data/more_phrases.txt')
    print(phrases)
