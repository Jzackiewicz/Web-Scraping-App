import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import exceptions
from keywords_window import KeyWordsEditWindow
from page_scraping import ScrapedPage
from table_box import ClickableTable


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Org")
        self.setGeometry(200, 200, 900, 400)

        self.bold_font = QFont()
        self.bold_font.setBold(True)

        self.data = None

        self.table = ClickableTable(self)

        self.url_input_pbar_layout = TextAndProgressBar(self)

        self.send_button = QPushButton("Wyślij", self)
        self.send_button.clicked.connect(self.url_input_pbar_layout.on_click_send_button)

        self.keywords_button = QPushButton("Edytuj słowa kluczowe", self)
        self.keywords_button.clicked.connect(self.on_click_keywords_button)

        self.clear_button = QPushButton("Usuń link", self)
        self.clear_button.clicked.connect(self.url_input_pbar_layout.on_click_clear_button)

        # Ustawienie layoutu
        self.main_layout = QGridLayout()
        self.main_layout.addLayout(self.url_input_pbar_layout, 0, 0, 4, 1)
        self.main_layout.addWidget(self.clear_button, 0, 4, 1, 1)
        self.main_layout.addWidget(self.send_button, 1, 0, 1, 4)
        self.main_layout.addWidget(self.keywords_button, 1, 4, 1, 1)
        self.main_layout.addWidget(self.table, 2, 0, 6, 5)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def on_click_keywords_button(self):
        keywords_edit_window = KeyWordsEditWindow(self)
        keywords_edit_window.exec()


class TextAndProgressBar(QStackedLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.url_input = QLineEdit()
        # self.url_input.setStyleSheet("* { background-color: rgba(0, 0, 0, 50); }")
        self.url_input.setPlaceholderText("Wprowadź adres URL...")
        self.url_input.setMaximumHeight(22)

        # self.pbar = QProgressBar()
        # self.pbar.setValue(100)
        # self.pbar.setMaximumHeight(22)
        # self.pbar.setTextVisible(False)

        self.setStackingMode(QStackedLayout.StackAll)

        # Program działa zbyt szybko, żeby użycie progress baru było sensowne
        # self.addWidget(self.pbar)
        self.addWidget(self.url_input)

    def on_click_send_button(self):
        url = self.url_input.text()
        try:
            self.parent.data = ScrapedPage(url).filtered_ads
            self.parent.table.update_table()
        except:
            if url == "":
                exceptions.MissingURL()
            else:
                exceptions.BadURL()

    def on_click_clear_button(self):
        self.url_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
