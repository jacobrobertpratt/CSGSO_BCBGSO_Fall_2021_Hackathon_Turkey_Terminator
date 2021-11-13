
class LetteredClassifier:
    def __init__(self, base_classifier, max_letters: int = 120):
        self.base_classifier = base_classifier
        self.num_classifiers = max_letters
        self.classifiers = []

    def fit(self, x, y):
        
