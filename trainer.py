from translator import generate_phrase_objects


if __name__ == '__main__':
    phrases = generate_phrase_objects('./data/embedded_phrases.csv', './data/test_reduced_phrases_w_indices.txt')
