import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout


def main_window():
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
        # TODO Do the Translation
        oe_entry.setText('You translated {}'.format(ne_entry.document().toPlainText()))

    translate_button.clicked.connect(translate_clicked)

    app.exec()


if __name__ == '__main__':
    main_window()

