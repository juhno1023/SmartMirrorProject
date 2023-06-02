import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('LineEdit')
        self.resize(800, 800)

        self.testBox = QTextBrowser(self)

        self.line_edit = QLineEdit(self)
        self.line_edit.move(75, 75)
        self.text_label = QLabel(self)
        self.text_label.move(75, 125)
        self.text_label.setText('hello world')
        self.button = QPushButton(self)
        self.button.move(75, 175)
        self.button.setText('Get Text')
        self.button.clicked.connect(self.button_event)

        self.show()

    def button_event(self):
        text = self.line_edit.text()  # line_edit text 값 가져오기
        self.text_label.setText(text)  # label에 text 설정하기
        self.testBox.resize(int(text), 300)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()

    sys.exit(app.exec_())
