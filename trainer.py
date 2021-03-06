from translator import generate_phrase_objects, Phrase
from decisiontree import LetterClassifier
from typing import List, Tuple
from tqdm import tqdm
from sklearn import tree, neighbors, ensemble, svm
from sklearn.model_selection import train_test_split
import numpy as np
import os
import pathlib
import pickle


def save_model(path: pathlib.Path, model):
    print('Saving model {}'.format(path))
    with open(path, 'wb+') as fp:
        pickle.dump(model, fp)


def generate_dataset(phr: List[Phrase]) -> List[Tuple[List[float], List[float]]]:
    result = []
    for phrase in tqdm(phr, desc="Generating dataset"):
        for e, _ in phrase.get_words():
            result.append(phrase.to_array(e))
    return result


def train_knn(train: Tuple[List[List[float]], List[List[float]]], test: Tuple[List[List[float]], List[List[float]]],
              k: int = 5):
    trainx, trainy = train
    print('KNN model with k={}:'.format(k))
    knn = neighbors.KNeighborsRegressor(k, n_jobs=os.cpu_count())
    print('Fitting Model...')
    model = knn.fit(trainx, trainy)
    print('Training Accuracy: {}%'.format(model.score(trainx, trainy) * 100))
    testx, testy = test
    print('Inference Accuracy: {}%'.format(model.score(testx, testy) * 100))
    model_filename = 'knn.sav'
    save_model(pathlib.Path('./models', model_filename), model)


# def train_svm(train: Tuple[List[List[float]], List[List[float]]],
#               test: Tuple[List[List[float]], List[List[float]]]):
#     trainx, trainy = train
#     print('Decision Support Vector Machine model:')
#     model = svm.SVR()
#     print('Fitting Model...')
#     model = model.fit(trainx, trainy)
#     print('Training Accuracy: {}%'.format(model.score(trainx, trainy) * 100))
#     testx, testy = test
#     print('Inference Accuracy: {}%'.format(model.score(testx, testy) * 100))
#     model_filename = 'decision_tree.sav'
#     save_model(pathlib.Path('./models', model_filename), model)


def train_svm_letter(train: Tuple[List[List[float]], List[List[float]]],
                     test: Tuple[List[List[float]], List[List[float]]]):
    trainx, trainy = train
    print('Decision Support Vector Machine model:')
    model = LetterClassifier(svm.SVR())
    print('Fitting Model...')
    model = model.fit(trainx, trainy)
    print('Training Accuracy: {}%'.format(model.score(trainx, trainy) * 100))
    testx, testy = test
    print('Inference Accuracy: {}%'.format(model.score(testx, testy) * 100))
    model_filename = 'svm_letter.sav'
    save_model(pathlib.Path('./models', model_filename), model)


def train_decision_tree(train: Tuple[List[List[float]], List[List[float]]],
                        test: Tuple[List[List[float]], List[List[float]]]):
    trainx, trainy = train
    print('Decision Tree model:')
    model = tree.DecisionTreeRegressor()
    print('Fitting Model...')
    model = model.fit(trainx, trainy)
    print('Training Accuracy: {}%'.format(model.score(trainx, trainy) * 100))
    testx, testy = test
    print('Inference Accuracy: {}%'.format(model.score(testx, testy) * 100))
    model_filename = 'decision_tree.sav'
    save_model(pathlib.Path('./models', model_filename), model)


def train_decision_tree_letter(train: Tuple[List[List[float]], List[List[float]]],
                        test: Tuple[List[List[float]], List[List[float]]]):
    trainx, trainy = train
    print('Decision Tree Letter model:')
    model = LetterClassifier(tree.DecisionTreeClassifier())
    print('Fitting Model...')
    model = model.fit(trainx, trainy)
    print('Training Accuracy: {}%'.format(model.score(trainx, trainy) * 100))
    testx, testy = test
    print('Inference Accuracy: {}%'.format(model.score(testx, testy) * 100))
    model_filename = 'decision_tree_letter.sav'
    save_model(pathlib.Path('./models', model_filename), model)


# def train_decision_boost(train: Tuple[List[List[float]], List[List[float]]],
#                          test: Tuple[List[List[float]], List[List[float]]]):
#     trainx, trainy = train
#     print('AdaBoost Decision Tree model:')
#     model = ensemble.AdaBoostClassifier(tree.DecisionTreeClassifier())
#     print('Fitting Model...')
#     model = model.fit(trainx, trainy)
#     print('Training Accuracy: {}%'.format(model.score(trainx, trainy) * 100))
#     testx, testy = test
#     print('Inference Accuracy: {}%'.format(model.score(testx, testy) * 100))
#     model_filename = 'ada_boost.sav'
#     save_model(pathlib.Path('./models', model_filename), model)


def train_decision_boost_letter(train: Tuple[List[List[float]], List[List[float]]],
                         test: Tuple[List[List[float]], List[List[float]]]):
    trainx, trainy = train
    print('AdaBoost Decision Tree model:')
    model = LetterClassifier(ensemble.AdaBoostClassifier(tree.DecisionTreeClassifier()))
    print('Fitting Model...')
    model = model.fit(trainx, trainy)
    print('Training Accuracy: {}%'.format(model.score(trainx, trainy) * 100))
    testx, testy = test
    print('Inference Accuracy: {}%'.format(model.score(testx, testy) * 100))
    model_filename = 'ada_boost_letter.sav'
    save_model(pathlib.Path('./models', model_filename), model)


if __name__ == '__main__':
    phrases = generate_phrase_objects('./data/embedded_phrases.csv', './data/reduced_phrases_w_indices.txt')
    dataset = generate_dataset(phrases)
    print('Generated a dataset with {} entries'.format(len(dataset)))
    X = [d[0] for d in dataset]
    X = np.array(X, dtype='float')
    Y = np.array([d[1] for d in dataset], dtype='float')
    trainx, testx, trainy, testy = train_test_split(X, Y, test_size=0.2)
    train = (trainx, trainy)
    test = (testx, testy)
    train_knn(train, test)
    # train_svm(train, test)
    train_decision_tree(train, test)
    # train_decision_boost(train, test)
    train_decision_tree_letter(train, test)
    train_decision_boost_letter(train, test)
    # train_svm_letter(train, test)
