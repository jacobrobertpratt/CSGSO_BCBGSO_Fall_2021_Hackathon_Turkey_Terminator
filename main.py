import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
import pickle
import re
import numpy as np
from translator import embed, Phrase


def main_window(m):
    app = QApplication(sys.argv)

    w = QWidget()
    main_layout = QHBoxLayout()

    ne_entry_w = QWidget()
    ne_entry_layout = QVBoxLayout()
    ne_entry_layout.addWidget(QLabel('Modern English'))
    ne_entry = QTextEdit()
    ne_entry_layout.addWidget(ne_entry)

    translate_button = QPushButton('Translate')
    translate_button.setEnabled(False)

    ne_entry_layout.addWidget(translate_button)
    ne_entry_w.setLayout(ne_entry_layout)

    main_layout.addWidget(ne_entry_w)

    oe_entry_w = QWidget()
    oe_entry_layout = QVBoxLayout()
    oe_entry_layout.addWidget(QLabel('Old English'))
    oe_entry = QTextEdit()
    oe_entry.setEnabled(False)
    oe_entry_layout.addWidget(oe_entry)
    oe_entry_w.setLayout(oe_entry_layout)

    main_layout.addWidget(oe_entry_w)

    w.setLayout(main_layout)
    w.show()

    # Setting up the sockets
    def ne_text_callback():
        if len(ne_entry.document().toPlainText()) > 0:
            translate_button.setEnabled(True)
            if ne_entry.document().isModified():
                pass
        else:
            translate_button.setEnabled(False)

    ne_entry.textChanged.connect(ne_text_callback)

    def translate_clicked():
        sentences = re.split(r'[.;"]', ne_entry.document().toPlainText())
        embeddings = embed(sentences)
        phrases = []
        for sentence, emb in zip(sentences, embeddings):
            words = sentence.split()
            for wi, word in enumerate(words):
                phrases.append(Phrase.get_feature_vector(word, emb, wi))
        predictions = m.predict(np.array(phrases, dtype='float'))
        oe_text = '.'.join([Phrase.vec2word(pred) for pred in predictions])
        oe_entry.setText(oe_text)

    translate_button.clicked.connect(translate_clicked)

    app.exec()


if __name__ == '__main__':
    model_name = './models/ada_boost.sav'
    with open(model_name, 'rb') as fp:
        model = pickle.load(fp)
    main_window(model)

