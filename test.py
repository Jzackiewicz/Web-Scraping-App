import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import webbrowser
import page_scraping


class ClickableTable(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setColumnCount(3)

        self.clicked.connect(self.on_click)

        self.click_time = 0

    def on_click(self, index):
        row = index.row()
        self.selectRow(row)

        time_dif = time.time() - self.click_time
        self.click_time = time.time()

        if time_dif <= 0.5:
            self.on_double_click(index)
            self.click_time = 0

    def on_double_click(self, index):
        url = self.parent.data[index.row()].link
        webbrowser.open(url, new=0, autoraise=True)

    def update_table(self):
        for i, offer in enumerate(self.parent.data):
            self.insertRow(i)
            for j, var in enumerate(vars(offer).values()):
                item = QTableWidgetItem(str(var))
                item.setFlags(Qt.ItemIsEditable | Qt.ItemIsSelectable)
                self.setItem(i, j, item)
        self.rowHeight(60)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = None
        self.setWindowTitle("Org")
        self.setGeometry(100, 100, 900, 400)

        # Tworzenie widgetów
        self.url_input = QLineEdit(self)
        self.send_button = QPushButton("Wyślij", self)
        self.table = ClickableTable(self)


        # Ustawienie layoutu
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.url_input)
        main_layout.addWidget(self.send_button)
        main_layout.addWidget(self.table)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Po kliknięciu przycisku "Wyślij"
        self.send_button.clicked.connect(self.on_click_button)

    def on_click_button(self):
        url = self.url_input.text()
        try:
            self.data = page_scraping.scrape_page(url)
        except:
            print("url")
            return -1

        self.table.update_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
