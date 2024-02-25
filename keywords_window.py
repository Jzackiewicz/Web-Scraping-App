from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class KeyWordsEditWindow(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Okno Dialogowe")
        self.setGeometry(200, 200, 200, 500)

        self.keywords = self.get_keywords_from_file()

        self.keywords_list = KeywordsList(self)
        self.keywords_table = KeywordsTable(self)

        cancel_button = QPushButton("Anuluj")
        cancel_button.clicked.connect(self.reject)

        save_button = QPushButton("Zapisz")
        save_button.clicked.connect(lambda _: print("ddd"))

        button_layout = QHBoxLayout()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)

        main_layout = QVBoxLayout()

        main_layout.addWidget(self.keywords_list)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def save_and_close(self):
        print("zapisz")
        # edited_text = self.text_edit.toPlainText()
        # print("Zapisano tekst:", edited_text)
        # self.accept()

    def get_keywords_from_file(self):
        words_list = []
        with open("KEYWORDS.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                words = line.split(";")
                for word in words:
                    words_list.append(word.strip())
        return words_list


class KeywordsTable(QTableWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.words = self.parent.keywords
        self.setColumnCount(1)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

        for i, word in enumerate(self.words):
            self.insertRow(i)
            item = QTableWidgetItem(word)
            print(item)
            self.setItem(0, i, item)


class KeywordsList(QListWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.words = self.parent.keywords

        for word in self.words:
            item = QListWidgetItem(word)
            self.addItem(item)

        self.setAlternatingRowColors(True)
        self.itemDoubleClicked.connect(self.editItem)
        # self.itemClicked.connect(self.on_list_item_clicked)

    # def on_list_item_clicked(self, item):
    #     if not item.text():  # Sprawdzenie, czy wybrany element jest pusty
    #         self.list_widget.editItem(item)

    def edit_item(self, item):
        index = self.row(item)
        edit = QLineEdit(item.text())
        self.setItemWidget(item, edit)
        edit.editingFinished.connect(lambda: self.update_item(index, edit))
        self.extract_items()

    def extract_items(self):
        items = []
        for x in range(self.count()):
            items.append(self.item(x).text())
        print(items)

    def update_item(self, index, edit):
        item = self.item(index)
        item.setText(edit.text())
        self.setItemWidget(item, None)
        edit.deleteLater()
