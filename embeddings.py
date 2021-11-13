from translator import read_phrases
import pathlib
import tensorflow_hub as hub


def create_word_dictionaries(path: pathlib.Path):
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")

