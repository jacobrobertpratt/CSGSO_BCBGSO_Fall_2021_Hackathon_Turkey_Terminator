from translator import generate_phrase_objects, Phrase
from typing import List, Tuple
from tqdm import tqdm


def generate_dataset(phr: List[Phrase]) -> List[Tuple[List[float], List[float]]]:
    result = []
    for phrase in tqdm(phr, desc="Generating dataset"):
        for e, _ in phrase.get_words():
            result.append(phrase.to_array(e))
    return result


if __name__ == '__main__':
    phrases = generate_phrase_objects('./data/embedded_phrases.csv', './data/test_reduced_phrases_w_indices.txt')
    dataset = generate_dataset(phrases)
    print('Generated a dataset with {} entries'.format(len(dataset)))
