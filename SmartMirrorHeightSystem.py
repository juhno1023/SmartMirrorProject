import sys
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QTime, QDate, QSize
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QTextEdit
from PyQt5 import QtWidgets, uic, QtCore
import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("schedule.db")  # 데이터베이스 파일명 지정

if not database.open():
    print("Failed to open database.")
    sys.exit(1)

# 일정 데이터 테이블 생성
query = QSqlQuery()
query.exec_(
    "CREATE TABLE IF NOT EXISTS schedules (date TEXT PRIMARY KEY, text TEXT)")

# UI 파일 연결 코드
UI_class = uic.loadUiType("main.ui")[0]
UI_class2 = uic.loadUiType("edit.ui")[0]  # 다른 UI 파일 연결 코드
UI_class3 = uic.loadUiType("editPOP.ui")[0]

class MyWindow(QMainWindow, UI_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.updateDateTime()
        self.startEditBtn.clicked.connect(self.openOtherPage)
        self.setFixedSize(QSize(1080, 1920))
        self.startEditBtn.clicked.connect(self.resizeTextBrowser)
        # Initialize the video capture
        self.cap = cv2.VideoCapture(0)

        # Create the FaceMesh instance
        self.face_mesh = mp_face_mesh.FaceMesh()

        # 1초마다 updateDateTime 함수 호출
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)

    #     self.showScheduleDataInTextBox(self.textBrowser_3)

    # def showScheduleDataInTextBox(self, text_browser):
    #     # 데이터베이스에서 저장된 일정 데이터를 가져와서 text_browser에 표시
    #     query = QSqlQuery()
    #     query.exec_("SELECT date, text FROM schedules")
    #     schedule_text = ""
    #     while query.next():
    #         date = query.value(0).toString()
    #         text = query.value(1).toString()
    #         schedule_text += f"{date}: {text}\n"
    #     text_browser.setText(schedule_text)

    def updateDateTime(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        current_date = QDate.currentDate().toString("yyyy년 MM월 dd일")
        self.textBrowser.setHtml(f'''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
        <html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
        p, li {{ white-space: pre-wrap; }}
        hr {{ height: 1px; border-width: 0; }}
        li.unchecked::marker {{ content: "\2610"; }}
        li.checked::marker {{ content: "\2612"; }}
        </style></head><body style=" font-family:'.AppleSystemUIFont'; font-size:30pt; font-weight:400; font-style:normal;">
        <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:45pt; font-weight:700; color:#ffffff;">현재 시간: </span><span style=" font-size:45pt; font-weight:700; color:#7bb36d;">{current_time}</span></p>
        <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:45pt; font-weight:700; color:#ffffff;"> 날짜: </span><span style=" font-size:45pt; font-weight:700; color:#7bb36d;">{current_date}</span></p></body></html>''')

    def openOtherPage(self):
        other_page = OtherPage()
        other_page.loadScheduleData()  # 데이터베이스에서 일정 데이터 불러오기
        other_page.restoreScheduleData()  # 일정 데이터 출력
        self.setCentralWidget(other_page)

    def resizeTextBrowser(self):
        ret, frame = self.cap.read()

        if not ret:
            return

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                nose_tip = face_landmarks.landmark[4]  # Use the index value 4 for the nose tip landmark

                top_right = (frame.shape[1], 0)
                bottom_right = (frame.shape[1], frame.shape[0])

                distance_right_points = (
                (bottom_right[0] - top_right[0]) ** 2 + (bottom_right[1] - top_right[1]) ** 2) ** 0.5
                distance_nose_to_line = abs((bottom_right[1] - top_right[1]) * nose_tip.x - (
                    bottom_right[0] - top_right[0])
                                        * nose_tip.y + bottom_right[0] * top_right[1] - bottom_right[1] * top_right[
                                            0]) / distance_right_points
                
                distance_nose_to_line = (distance_nose_to_line - 639) * 100
                distance_nose_to_line = ((distance_nose_to_line + 42) * 16)
                other_page = self.centralWidget()
                calendar_widget = other_page.calendarWidget

                current_pos = calendar_widget.pos()  # 현재 위치 가져오기
                new_pos = QPoint(current_pos.x(), current_pos.y() - int(distance_nose_to_line))  # 새로운 위치 계산
                calendar_widget.move(new_pos)  # 위젯 위치 이동

                textBrowser = other_page.textBrowser
                if distance_nose_to_line >= 1300:
                    current_pos_2 = textBrowser.pos()
                    new_pos_2 = QPoint(current_pos_2.x(), current_pos_2.y() + 1000)  # 새로운 위치 계산
                    textBrowser.move(new_pos_2)  # 위젯 위치 이동
    
                
class OtherPage(QWidget, UI_class2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backhome.clicked.connect(self.openMainPage)
        self.calendarWidget.selectionChanged.connect(self.showSelectedDate)

        # 일정을 저장할 변수 초기화
        self.schedule_data = {}

        # 저장된 일정 데이터 복원
        self.restoreScheduleData()

        # 데이터베이스에서 일정 데이터 불러오기
        self.loadScheduleData()

        self.textBrowser_2.setHtml('''
        <html>
        <head>
            <meta charset="utf-8" />
            <style type="text/css">
                body {
                    font-family: '.AppleSystemUIFont';
                    font-size: 30pt;
                    font-weight: 300;
                    font-style: normal;
                    color: #FFFFFF;
                }
            </style>
        </head>
        <body>
            <p align="left"> 이번달 일정 : </p>
        </body>
        </html>
        ''')

    def showSelectedDate(self):
        selected_date = self.calendarWidget.selectedDate()
        dialog = EditPOPDialog(selected_date)
        dialog.setWindowTitle(selected_date.toString("yyyy년 MM월 dd일 일정 추가하기"))

        if dialog.exec_() == QDialog.Accepted:
            text = dialog.textEdit.toPlainText()
            self.textBrowser.append(f'{selected_date.toString("yyyy년 MM월 dd일")}: {text}')
            self.schedule_data[selected_date.toString("yyyy-MM-dd")] = text  # 일정 데이터 저장
            
            current_date = QtCore.QDate.currentDate()

            curDate = current_date.toString("yyyy년 MM월 dd일")
            selDate = selected_date.toString("yyyy년 MM월 dd일")
            main_window = self.parent()
            if curDate == selDate:
                main_window.textBrowser_4.setStyleSheet("color: white;")
                main_window.textBrowser_4.setText(f'{text}')


    def loadScheduleData(self):
        # 데이터베이스에서 저장된 일정 데이터를 불러옴
        query = QSqlQuery()
        query.exec_("SELECT date, text FROM schedules")

        while query.next():
            date = query.value(0).toString()
            text = query.value(1).toString()
            self.schedule_data[date.toString("yyyy-MM-dd")] = text

    def restoreScheduleData(self):
        # 선택된 날짜에 해당하는 일정 데이터를 텍스트 창에 표시
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        if selected_date in self.schedule_data:
            self.textBrowser_2.setText(self.schedule_data[selected_date])
        else:
            self.textBrowser_2.clear()

    def openMainPage(self):
        main_page = MyWindow()
        self.parent().setCentralWidget(main_page)

    def closeEvent(self, event):
        # 프로그램 종료 시 일정 데이터를 데이터베이스에 저장
        query = QSqlQuery()
        query.exec_("DELETE FROM schedules")  # 기존의 일정 데이터 삭제
        for date, text in self.schedule_data.items():
            query.exec_(
                f"INSERT INTO schedules (date, text) VALUES ('{date}', '{text}')")

        event.accept()

class EditPOPDialog(QDialog, UI_class3):
    def __init__(self, selected_date):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(selected_date.toString("yyyy년 MM월 dd일 일정 추가하기"))
        self.accepted_text = None
        self.textEdit = self.findChild(QTextEdit, "textEdit")  # textEdit 위젯 찾기

        self.button1.clicked.connect(lambda: self.buttonClicked(self.button1.text()))
        self.button2.clicked.connect(lambda: self.buttonClicked(self.button2.text()))
        self.button3.clicked.connect(lambda: self.buttonClicked(self.button3.text()))
        self.button4.clicked.connect(lambda: self.buttonClicked(self.button4.text()))
        self.button5.clicked.connect(lambda: self.buttonClicked(self.button5.text()))
        self.button6.clicked.connect(lambda: self.buttonClicked(self.button6.text()))
        self.button7.clicked.connect(lambda: self.buttonClicked(self.button7.text()))
        self.button8.clicked.connect(lambda: self.buttonClicked(self.button8.text()))
        self.button9.clicked.connect(lambda: self.buttonClicked(self.button9.text()))


    def buttonClicked(self, text):
        self.textEdit.setPlainText(text)  # 버튼의 텍스트를 textEdit에 입력
        self.accepted_text = text
        self.accept()

    def accept(self):
        super().accept()

    def getAcceptedText(self):
        return self.accepted_text
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyWindow()
    main_window.show()
    sys.exit(app.exec_())

# class CustomInputDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("일정 추가")
#         self.layout = QVBoxLayout()
#         self.textEdit = QTextEdit()
#         self.layout.addWidget(self.textEdit)
#         self.buttonBox = QDialogButtonBox(
#             QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
#         self.buttonBox.accepted.connect(self.accept)
#         self.buttonBox.rejected.connect(self.reject)
#         self.layout.addWidget(self.buttonBox)
#         self.setLayout(self.layout)

# import cv2
# import mediapipe as mp

# mp_drawing = mp.solutions.drawing_utils
# mp_face_mesh = mp.solutions.face_mesh

# cap = cv2.VideoCapture(0)

# face_mesh = mp_face_mesh.FaceMesh()

# while True:
#     ret, frame = cap.read()

#     if not ret:
#         break

#     image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     results = face_mesh.process(image_rgb)

#     if results.multi_face_landmarks:
#         for face_landmarks in results.multi_face_landmarks:
#             # Get the coordinates of the nose tip
#             nose_tip = face_landmarks.landmark[4]

#             # Get the coordinates of the top and bottom right keypoints
#             top_right = (frame.shape[1], 0)
#             bottom_right = (frame.shape[1], frame.shape[0])

#             # Calculate the distance between the top and bottom right keypoints
#             distance_right_points = (
#                 (bottom_right[0] - top_right[0]) ** 2 + (bottom_right[1] - top_right[1]) ** 2) ** 0.5

#             # Calculate the distance between the nose tip and the line connecting the right keypoints
#             distance_nose_to_line = abs((bottom_right[1] - top_right[1]) * nose_tip.x - (bottom_right[0] - top_right[0])
#                                         * nose_tip.y + bottom_right[0] * top_right[1] - bottom_right[1] * top_right[0]) / distance_right_points

#             # Draw the right keypoints and the line connecting them
#             cv2.circle(frame, top_right, 5, (0, 0, 255), -1)
#             cv2.circle(frame, bottom_right, 5, (0, 0, 255), -1)
#             cv2.line(frame, top_right, bottom_right, (0, 0, 255), 2)

#             # Draw the nose tip
#             cv2.circle(frame, (int(
#                 nose_tip.x * frame.shape[1]), int(nose_tip.y * frame.shape[0])), 5, (0, 255, 0), -1)

#             # Display the distance on the frame
#             cv2.putText(frame, f"Distance: {distance_nose_to_line:.2f}", (
#                 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#     cv2.imshow('Head Tracking', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()