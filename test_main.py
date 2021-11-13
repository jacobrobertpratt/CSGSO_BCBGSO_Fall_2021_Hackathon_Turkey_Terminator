import pickle
import re
from translator import Phrase
from embeddings import embed
import numpy as np


if __name__ == '__main__':
    model_name = './models/knn.sav'
    with open(model_name, 'rb') as fp:
        model = pickle.load(fp)
    sentences = re.split(r'[.;"]', input('What to translate? '))
    embeddings = embed(sentences).numpy()
    phrases = []
    for sentence, emb in zip(sentences, embeddings):
        words = sentence.split()
        for wi, word in enumerate(words):
            phrases.append(Phrase.get_feature_vector(word, emb.tolist(), wi))
    predictions = model.predict(np.array(phrases, dtype='float'))
    oe_text = ' '.join([Phrase.vec2word(pred) for pred in predictions])
    print(oe_text)
