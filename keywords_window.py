from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class KeyWordsEditWindow(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Edycja słów kluczowych")
        self.setGeometry(700, 200, 200, 350)
        self.keywords_list = KeywordsList(self)

        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.clicked.connect(self.reject)

        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.keywords_list.save_keywords)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.save_button)

        self.keyword_layout = QGridLayout()
        self.text_box = QLineEdit()
        self.text_add_button = QPushButton("Dodaj")
        self.text_add_button.clicked.connect(self.keywords_list.add_keyword_to_list)
        self.keyword_layout.addWidget(self.text_box, 0, 0, 1, 3)
        self.keyword_layout.addWidget(self.text_add_button, 0, 4, 1, 1)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.keywords_list)
        main_layout.addLayout(self.keyword_layout)
        main_layout.addLayout(self.button_layout)

        self.setLayout(main_layout)


class KeywordsList(QListWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.keywords_txt_dir = "KEYWORDS.txt"

        self.keywords = self.get_keywords_from_file()
        self.setAlternatingRowColors(True)

        for word in self.keywords:
            item = QListWidgetItem(word)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.addItem(item)

    def extract_items(self):
        items = []
        for x in range(self.count()):
            items.append(self.item(x).text())
        return items

    def add_keyword_to_list(self):
        new_word = self.parent.text_box.text()
        if new_word != "":
            item = QListWidgetItem(new_word)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.addItem(item)
        self.parent.text_box.clear()

    def save_keywords(self):
        words = self.extract_items()
        with open(self.keywords_txt_dir, "w") as f:
            for word in words:
                if word != "":
                    f.writelines(word + "\n")
        self.parent.close()

    def get_keywords_from_file(self):
        words_list = []
        with open(self.keywords_txt_dir, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line != "":
                    words_list.append(line.strip())
        return words_list
