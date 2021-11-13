# Modern English to Old English Machine Translator
## Turkey Terminator
This project aims to further the progress of Old English translation by utilizing AI. By training the model to learn the language changes that occured between Modern English and Old English, we should be able to predict what Modern English words that have no Old English translations would look like in Old English.

## Data Preprocessing
While initially we tried to compile a wiktionary dump from [here](https://github.com/tatuylonen/wiktextract) into a [CSV file](./data/reduced_data.csv) so that we could train our model on a single word basis, we quickly realized that conjugating strong OE verbs for training wasn't feasible, so we decided to do a corpus based approach instead, we found a paper [Take Help from Elder Brother: Old to Modern
English NMT with Phrase Pair Feedback](https://mohammedhasanuzzaman.github.io/papers/CICLING3.pdf) that described a phrase pair method that can be used to train models, so we extracted the data that they used [The_Homilies_of_the_Anglo-Saxon_Church.pdf](./data/The_Homilies_of_the_Anglo-Saxon_Church.pdf). We manually split the words in a plain text format so that we could parse them with python [phrases.txt](./data/phrases.txt).
There were several typos in the phrases once we had them split up into pairs, though, so we spent a lot of time correcting the data.

### Sentence Encodings
In order to assist the model in understanding context and conjugations, we used word embeddings.
Google has a prebuilt model called the [Universal Sentence Encoder](https://www.tensorflow.org/hub/tutorials/semantic_similarity_with_tf_hub_universal_encoder)
we used this to encode all of the training set into vectors of 512 floating point numbers, then fed them in 
along side the word that we had in question.

### Word indices
Though we had sentences that were directly translated, it wasn't clear as to which words correlated to which words in the 
cognate sentence, thus, we manually indexed them linking the words from each sentence to the corresponding word in the translation.
This was in the [reduced_phrases_w_indices.txt](./data/reduced_phrases_w_indices.txt) file.

## Model Selection
### Letter Classifiers
In addition to using normal regression techniques, I also created a model that assigned a base estimator to each of 120 letters.
Each classifier is responsible for one letter of the output word, this allowed me to use the BoostingClassifier from`sklearn` since it required that the
labels be a 1D array instead of the 2D array that I had.

### Results
Several models were tested, overall, we saw good accuracy with kNN and the basic Decision Tree regressors.
All in all with 1011 data entries, and a Train/Test split of 80/20% I was able to achieve

| Model  | Training Accuracy | Testing Accuracy |
| ------------- | ------------- | ------ |
| kNN (k=5)  | 93.52%  | 89.47% |
| Decision Tree  | 100%  | 85.08% |
| Letter Decision Tree | 100% | 22.66% |
| Letter AdaBoosted Decision Tree | 100% | 22.17% |

Overall, the Decision Tree was used as a compromise between execution time and accuracy.

## Conclusion
I set out at the beginning of this hackathon to create a translator from modern english to old english.
And I believe that I succeeded. But don't take my word for it, see for yourself.

## Future Works

If I had the time, I would have liked to do this with a real neural network. But first and foremost,
the dataset that I had was incomplete, I was only able to prepare a corpus of ~1000 words, when I definitely
had more than 500k available. In order to finish the project in time, I had to do two things:
1. Reduce the corpus size, this is why the lines are in the [reduced_phrases.txt](./data/reduced_phrases.txt) and not in [more_phrases.txt](./data/more_phrases.txt).
2. I had to accept that I wasn't going to have enough time to index all of the words in all of the phrases, so I did the ones that I could the ones that are complete,
as well as the ones that are not ar ein [reduced_phrases_w_indices.txt](./data/reduced_phrases_w_indices.txt).

To fix this, the rest of the corpus needs to be filled in, fixing typos in the phrases document, figuring out how to get them to line up.
Usually this is just replacing `;` with `,` and vice versa. The only issue is that it takes a lot of time to prepare them,
and it's tedious to do alone. I had some help, and I'd like to thank Henlee and Aidan for keeping me company
whilst I worked.

## Installation
### Prerequisits
You'll need a python environment with the following packages
- scikit-learn
- tensorflow-hub
- pyqt5
- tqdm

```shell
pip install scikit-learn tensorflow-hub pyqt5 tqdm
```

I had some issues getting tensorflow-hub to work, if you have the same issue, try this

```shell
pip install --upgrade tensorflow-estimator==2.3.0
```

## Execution
To run the gui translator, you simply need to run `python main.py` from the terminal.
The gui is simple, there's an input text box, and an output box, the translate button will be disabled unless there's text in the modern english text box.
Once you click translate the bar on the bottom will indicate the translation progress, **Note** it can take quite some time
to do the word embeddings for the sentences, during which it may look like the window is unresponsive, please be patient.

Enjoy!
