import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import page_scraping
import exceptions
from keywords_window import KeyWordsEditWindow
from table_box import ClickableTable


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Org")
        self.setGeometry(100, 100, 900, 400)

        self.bold_font = QFont()
        self.bold_font.setBold(True)

        self.data = None

        # Tworzenie widgetów
        self.url_input = QLineEdit(self)
        self.table = ClickableTable(self)

        self.send_button = QPushButton("Wyślij", self)
        self.send_button.clicked.connect(self.on_click_send_button)

        self.keywords_button = QPushButton("Edytuj słowa kluczowe", self)
        self.keywords_button.clicked.connect(self.on_click_keywords_button)

        # Ustawienie layoutu
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.url_input, 0, 0, 1, 5)
        self.main_layout.addWidget(self.send_button, 1, 0, 1, 3)
        self.main_layout.addWidget(self.keywords_button, 1, 4, 1, 1)
        self.main_layout.addWidget(self.table, 2, 0, 6, 5)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        # Po kliknięciu przycisku "Wyślij"


    def on_click_send_button(self):
        url = self.url_input.text()

        try:
            self.data = page_scraping.scrape_page(url)
            self.table.update_table()
        except:
            if url == "":
                exceptions.MissingURL()
            else:
                exceptions.BadURL()

    def on_click_keywords_button(self):
        keywords_edit_window = KeyWordsEditWindow(self)
        keywords_edit_window.exec()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
