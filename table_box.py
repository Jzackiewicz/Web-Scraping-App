import time
import webbrowser

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ClickableTable(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setColumnCount(3)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().hide()
        self.clicked.connect(self.on_click)

        self.click_time = 0

    def on_click(self, index):
        row = index.row()
        self.selectRow(row)

        time_dif = time.time() - self.click_time
        self.click_time = time.time()

        if time_dif <= 0.3:
            self.on_double_click(index)
            self.click_time = 0

    def on_double_click(self, index):
        url = self.parent.data[index.row()].link
        webbrowser.open(url, new=0, autoraise=True)

    def update_table(self):
        for i, offer in enumerate(self.parent.data):
            self.insertRow(i)
            self.setRowHeight(i, 40)
            item_org = QTableWidgetItem(str(offer.organizator))
            item_nazwa = QTableWidgetItem(str(offer.nazwa))
            item_nazwa.setFont(self.parent.bold_font)
            item_termin = QTableWidgetItem(str(offer.termin))

            items = [item_nazwa, item_org, item_termin]
            for j, item in enumerate(items):
                item.setFlags(Qt.ItemIsEditable | Qt.ItemIsSelectable)
                self.setItem(i, j, item)

        # Formatowanie kolumn tabeli
        self.setWordWrap(True)
        self.resizeColumnToContents(0)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
