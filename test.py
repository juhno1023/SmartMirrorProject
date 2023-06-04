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

#대형 휠체어 높이 = 400mm
#스마트 미러 앞에서 터치할 수 있는 최대 범위 = 75cm (+- 5cm)

#코의 높이가 27정도 일 떄, 75cm 까지 접근 가능
#코의 높이가 43정도 일 때, 90cm 까지 접근 가능
#코의 높이가 79정도 일 때, 115cm 까지 접근 가능

#대형 휠체어 높이 = 400mm
#스마트 미러 앞에서 터치할 수 있는 최대 범위 = 75cm (+- 5cm)

#코의 높이가 27정도 일 떄, 70cm 까지 접근 가능 = 2.59, 43
#코의 높이가 54정도 일 때, 95cm 까지 접근 가능 = 1.75, 41
#코의 높이가 81정도 일 때, 121cm 까지 접근 가능 = 1.49, 40 

#코의 높이가 43정도 일 때, 90cm 까지 접근 가능 = 2.09
#코의 높이가 79정도 일 때, 115cm 까지 접근 가능 = 1.45


# 40cm 앞에서 휠체어를 타고 있는 동안, 78cm까지 터치 가능 = 코의 높이 31 = 47 (팔길이가 약 61.5CM 정도 되는 여성)
# 40cm 앞에서 휠체어를 타고 있는 동안, 79cm까지 터치 가능 = 코의 높이 31 = 48 
# 40cm 앞에서 휠체어를 타고 있는 동안, 78cm까지 터치 가능 = 코의 높이 32 = 46 

# 40cm 앞에서 휠체어를 타고 있는 동안, 82cm까지 터치 가능 = 코의 높이 33 = 49 (팔길이가 약 65.5CM 정도 되는 남성)
# 40cm 앞에서 휠체어를 타고 있는 동안, 87cm까지 터치 가능 = 코의 높이 36 = 51
# 40cm 앞에서 휠체어를 타고 있는 동안, 86cm까지 터치 가능 = 코의 높이 35 = 51

# 40cm 앞에서 휠체어를 타고 있는 동안, 102cm까지 터치 가능 = 코의 높이 39 = 63 (팔길이가 약 73.5CM 정도 되는 남성)
# 40cm 앞에서 휠체어를 타고 있는 동안, 103cm까지 터치 가능 = 코의 높이 40 = 63
# 40cm 앞에서 휠체어를 타고 있는 동안, 86cm까지 터치 가능 = 코의 높이 35 = 51


#50 127 - 43 = 85cm
#70 127 - 37 = 90cm
#120 --> 1920 == 16,  0-1920, 10-1760 
#77

#131.5 - 106.5 = 
