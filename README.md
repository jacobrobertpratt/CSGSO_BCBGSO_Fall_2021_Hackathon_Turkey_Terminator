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
