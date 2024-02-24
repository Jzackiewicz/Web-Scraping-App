from PyQt5.QtWidgets import QMessageBox


class BadURL(QMessageBox):
    def __init__(self):
        super().__init__()
        msg = "Nieprawidłowy adres URL!"
        self.setWindowTitle("Error!")
        self.setText(msg)
        self.exec_()


class MissingURL(QMessageBox):
    def __init__(self):
        super().__init__()
        msg = "Brak adresu URL!"
        self.setWindowTitle("Error!")
        self.setText(msg)
        self.exec_()
