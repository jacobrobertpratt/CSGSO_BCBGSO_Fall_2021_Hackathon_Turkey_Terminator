from translator import read_phrases
import pathlib
import tensorflow_hub as hub
from tqdm import tqdm

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")


def create_word_embeddings(path: pathlib.Path, outpath: pathlib.Path):
    phrases = read_phrases(path)
    ne = [p[1] for p in phrases]
    embeddings = embed(ne)
    lines = []
    for sentence, embedding in tqdm(zip(ne, embeddings)):
        line = (sentence + ',' + ','.join(map(str, embedding)) + '\n').replace('tf.Tensor(', '').replace(', shape=(), dtype=float32)', '')
        lines.append(line.encode('utf8'))
    with open(outpath, 'wb+') as fp:
        fp.writelines(lines)


if __name__ == '__main__':
    create_word_embeddings('./data/reduced_phrases.txt', './data/embedded_phrases.csv')
