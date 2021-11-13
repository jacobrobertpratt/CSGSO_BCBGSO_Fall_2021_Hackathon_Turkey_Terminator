from typing import List


class LetterClassifier:
    def __init__(self, base_classifier, max_letters: int = 120):
        self.base_classifier = base_classifier
        self.num_classifiers = max_letters
        self.classifiers = []

    def fit(self, x, y):
        self.classifiers.clear()
        for letter in range(self.num_classifiers):
            new_y = [yt[letter] for yt in y]
            self.classifiers.append(self.base_classifier.fit(x, new_y))
        return self

    def predict(self, x) -> List[List[float]]:
        columns = [clf.predict(x) for clf in self.classifiers]
        result = [[columns[c][r] for c in range(self.num_classifiers)] for r in range(len(x))]
        return result

    def score(self, x, y) -> float:
        predictions = self.predict(x)
        correct = 0
        for pred, yt in zip(predictions, y):
            # correct += sum([int(p) == int(ytt) for p, ytt in zip(pred, yt)]) / self.num_classifiers
            if all([int(p) == int(ytt) for p, ytt in zip(pred, yt)]):
                correct += 1
        return correct / len(predictions)
