# Modern English to Old English Machine Translator
## Turkey Terminator
This project aims to further the progress of Old English translation by utilizing AI. By training the model to learn the language changes that occured between Modern English and Old English, we should be able to predict what Modern English words that have no Old English translations would look like in Old English.

## Data Preprocessing
We compiled the wiktionary dump, which we got from [here](https://github.com/tatuylonen/wiktextract), of English etymology. We reviewed the dump and searched for words. We marked words with their part of speech and whether or not they have ancestor forms. If they do have ancestors, we added the Old English and Proto-Germanic forms. We took the words that we kept and place in a CSV file in order to reduce the file size. The original file size was 3 gb. The reduced file size is about 10 mb.
