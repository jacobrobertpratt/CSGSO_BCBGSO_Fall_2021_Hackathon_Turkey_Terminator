import pathlib
from typing import List, Tuple, Dict
from tqdm import tqdm
import re


class Phrase:
    max_word_length = 120

    def __init__(self, ne: str, edges: Dict[int, List[int]], embedding: List[float], oe: str = ''):
        self.ne = ne
        self.oe = oe
        self.edges = edges
        self.embedding = embedding

    def __repr__(self):
        return '{} <- {}'.format(self.ne, self.oe)

    def __getitem__(self, item: int) -> str:
        return self.ne.split()[item]

    @staticmethod
    def word2vec(w: str) -> List[float]:
        b = w.encode('utf8')
        if len(b) > Phrase.max_word_length:
            b = b[:Phrase.max_word_length]
            return list(map(float, b))
        if len(b) < Phrase.max_word_length:
            b = list(map(float, b))
            diff = Phrase.max_word_length - len(b)
            b += [0.0]*diff
            return b
        return list(map(float, b))

    @staticmethod
    def vec2word(v: List[float]) -> str:
        b = []
        vi = 0
        while vi < len(v):
            vt = int(v[vi])
            try:
                if 0 <= vt <= 0x7f:
                    b.append(bytes([vt]).decode('utf8'))
                    vi += 1
                elif 0xc2 <= vt <= 0xf4 and vi < len(v) - 1:
                    clength = 1
                    b2 = int(v[vi + 1])
                    while 0x80 <= b2 <= 0xbf:
                        clength += 1
                        if clength >= 4 or vi + clength >= len(v):
                            break
                        b2 = int(v[vi + clength])
                    try:
                        b.append(bytes(list(map(int, v[vi:vi + clength]))).decode('utf8'))
                    except UnicodeDecodeError:
                        b.append('?')
                    vi += clength
                else:
                    b.append('?')
                    vi += 1
            except UnicodeDecodeError:
                b.append('?')
        return ''.join(b)

    @staticmethod
    def get_feature_vector(w: str, embed: List[float], index: int) -> List[float]:
        return Phrase.word2vec(w) + embed + [float(index)]

    def get_words(self) -> List[Tuple[int, str]]:
        result = []
        words = self.ne.split()
        for s in self.edges:
            result.append((s, words[s]))
        return result

    def translate(self, edge: int) -> str:
        if edge in self.edges:
            words = self.oe.split()
            return ' '.join([words[e] for e in self.edges[edge]])
        return ''

    def to_array(self, word: int) -> Tuple[List[float], List[float]]:
        return self.get_feature_vector(self[word], self.embedding, word), self.word2vec(self.translate(word))


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


def read_indices(path: pathlib.Path, embeddings: Dict[str, List[float]]) -> List[Phrase]:
    result = []
    with open(path, 'rb') as fp:
        data = fp.read()
        lines = data.decode('utf8').split('\n')
        for i in tqdm(range(0, len(lines) - 3, 4), desc="Reading word indices"):
            oe_sentence = lines[i].strip()
            ne_sentence = lines[i + 1].strip()
            edge_parts = lines[i + 2].split()
            edges = {}
            for e in range(0, len(edge_parts) - 1, 2):
                src = int(edge_parts[e])
                trgt = edge_parts[e + 1]
                trgt = list(map(int, trgt.split('.'))) if '.' in trgt else [int(trgt)]
                edges[src] = trgt
            result.append(Phrase(ne_sentence, edges, embeddings[ne_sentence], oe_sentence))
    return result


def read_word_embeddings(path: pathlib.Path) -> Dict[str, List[float]]:
    result = {}
    with open(path, 'rb') as fp:
        lines = (fp.read()).decode('utf8').split('\n')
        for line in tqdm(lines, desc="Reading word embeddings"):
            if len(line) > 3:
                segs = line.split(',')
                embedding = list(map(float, segs[-512:]))
                sentence = ','.join(segs[:-512])
                result[sentence] = embedding
    return result


def generate_phrase_objects(emb_path: pathlib.Path, index_path: pathlib.Path) -> List[Phrase]:
    # create_word_embeddings(emb_path, './data/embedded_phrases.csv')
    embeddings = read_word_embeddings('./data/embedded_phrases.csv')
    return read_indices(index_path, embeddings)


if __name__ == '__main__':
    phrases = read_phrases('./data/phrases.txt')
    write_phrases(phrases, './data/more_phrases.txt')
    print(phrases)
