from PyQt5.QtWidgets import *


class KeyWordsEditWindow(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Okno Dialogowe")
        self.setGeometry(200, 200, 300, 200)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Wprowadź tekst...")

        cancel_button = QPushButton("Anuluj")
        cancel_button.clicked.connect(self.reject)

        save_button = QPushButton("Zapisz")
        save_button.clicked.connect(self.save_and_close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.text_edit)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def save_and_close(self):
        edited_text = self.text_edit.toPlainText()
        print("Zapisano tekst:", edited_text)
        self.accept()