import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

cap = cv2.VideoCapture(0)

face_mesh = mp_face_mesh.FaceMesh()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Get the coordinates of the nose tip
            nose_tip = face_landmarks.landmark[4]

            # Get the coordinates of the top and bottom right keypoints
            top_right = (frame.shape[1], 0)
            bottom_right = (frame.shape[1], frame.shape[0])

            # Calculate the distance between the top and bottom right keypoints
            distance_right_points = ((bottom_right[0] - top_right[0]) ** 2 + (bottom_right[1] - top_right[1]) ** 2) ** 0.5

            # Calculate the distance between the nose tip and the line connecting the right keypoints
            distance_nose_to_line = abs((bottom_right[1] - top_right[1]) * nose_tip.x - (bottom_right[0] - top_right[0]) * nose_tip.y + bottom_right[0] * top_right[1] - bottom_right[1] * top_right[0]) / distance_right_points

            # Draw the right keypoints and the line connecting them
            cv2.circle(frame, top_right, 5, (0, 0, 255), -1)
            cv2.circle(frame, bottom_right, 5, (0, 0, 255), -1)
            cv2.line(frame, top_right, bottom_right, (0, 0, 255), 2)

            # Draw the nose tip
            cv2.circle(frame, (int(nose_tip.x * frame.shape[1]), int(nose_tip.y * frame.shape[0])), 5, (0, 255, 0), -1)
            distance_nose_to_line = (distance_nose_to_line - 639) * 100
            # Display the distance on the frame
            cv2.putText(frame, f"Distance: {distance_nose_to_line:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Head Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# import sys
# from PyQt5.QtCore import QTimer
# from PyQt5.QtWidgets import *
# from PyQt5.QtSql import QSqlDatabase, QSqlQuery
# from PyQt5.QtCore import QTime, QDate
# from PyQt5 import uic

# database = QSqlDatabase.addDatabase("QSQLITE")
# database.setDatabaseName("schedule.db")  # 데이터베이스 파일명 지정

# if not database.open():
#     print("Failed to open database.")
#     sys.exit(1)

# # 일정 데이터 테이블 생성
# query = QSqlQuery()
# query.exec_("CREATE TABLE IF NOT EXISTS schedules (date TEXT PRIMARY KEY, text TEXT)")

# # UI 파일 연결 코드
# UI_class = uic.loadUiType("main.ui")[0]
# UI_class2 = uic.loadUiType("edit.ui")[0]  # 다른 UI 파일 연결 코드

# class MyWindow(QMainWindow, UI_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#         self.updateDateTime()

#         self.btn1.clicked.connect(self.openOtherPage)

#         # 1초마다 updateDateTime 함수 호출
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.updateDateTime)
#         self.timer.start(1000)

#         self.showScheduleDataInTextBox(self.textBrowser_3)

#     def showScheduleDataInTextBox(self, text_browser):
#         # 데이터베이스에서 저장된 일정 데이터를 가져와서 text_browser에 표시
#         query = QSqlQuery()
#         query.exec_("SELECT date, text FROM schedules")
#         schedule_text = ""
#         while query.next():
#             date = query.value(0).toString()
#             text = query.value(1).toString()
#             schedule_text += f"{date}: {text}\n"
#         text_browser.setText(schedule_text)

#     def updateDateTime(self):
#         current_time = QTime.currentTime().toString("hh:mm:ss")
#         current_date = QDate.currentDate().toString("yyyy년 MM월 dd일")
#         self.textBrowser.setHtml(f'''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
#         <html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
#         p, li {{ white-space: pre-wrap; }}
#         hr {{ height: 1px; border-width: 0; }}
#         li.unchecked::marker {{ content: "\2610"; }}
#         li.checked::marker {{ content: "\2612"; }}
#         </style></head><body style=" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;">
#         <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:24pt; font-weight:700; color:#7bb36d;">오늘의 주요 일정 :</span></p>
#         <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
#         <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:18pt; font-weight:700; color:#ffffff;">현재 시간: </span><span style=" font-size:18pt; font-weight:700; color:#7bb36d;">{current_time}</span></p>
#         <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:18pt; font-weight:700; color:#ffffff;"> 날짜: </span><span style=" font-size:18pt; font-weight:700; color:#7bb36d;">{current_date}</span></p></body></html>''')

#     def openOtherPage(self):
#         other_page = OtherPage()
#         other_page.loadScheduleData()  # 데이터베이스에서 일정 데이터 불러오기
#         other_page.restoreScheduleData()  # 일정 데이터 출력
#         self.setCentralWidget(other_page)


# class OtherPage(QWidget, UI_class2):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#         self.backhome.clicked.connect(self.openMainPage)
#         self.calendarWidget.selectionChanged.connect(self.showSelectedDate)

#         # 일정을 저장할 변수 초기화
#         self.schedule_data = {}

#         # 저장된 일정 데이터 복원
#         self.restoreScheduleData()

#         # 데이터베이스에서 일정 데이터 불러오기
#         self.loadScheduleData()  # 수정된 부분

#         self.textBrowser_2.setHtml('''
#         <html>
#         <head>
#             <meta charset="utf-8" />
#             <style type="text/css">
#                 body {
#                     font-family: '.AppleSystemUIFont';
#                     font-size: 30pt;
#                     font-weight: 300;
#                     font-style: normal;
#                     color: #FFFFFF;
#                 }
#             </style>
#         </head>
#         <body>
#             <p align="left"> 이번달 일정 : </p>
#         </body>
#         </html>
#         ''')

#     def showSelectedDate(self):
#         selected_date = self.calendarWidget.selectedDate()
#         dialog = CustomInputDialog(self)
#         dialog.setWindowTitle(selected_date.toString("yyyy년 MM월 dd일 일정 추가하기"))

#         if dialog.exec_() == QDialog.Accepted:
#             text = dialog.textEdit.text()
#             self.textBrowser.append(f'{selected_date.toString("yyyy년 MM월 dd일")}: {text}')
#             self.schedule_data[selected_date] = text  # 일정 데이터 저장

#     def loadScheduleData(self):
#         # 데이터베이스에서 저장된 일정 데이터를 불러옴
#         query = QSqlQuery()
#         query.exec_("SELECT date, text FROM schedules")

#         while query.next():
#             date = query.value(0).toString()
#             text = query.value(1).toString()
#             self.schedule_data[date] = text

#     def restoreScheduleData(self):
#         # 선택된 날짜에 해당하는 일정 데이터를 텍스트 창에 표시
#         selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
#         if selected_date in self.schedule_data:
#             self.textBrowser_2.setText(self.schedule_data[selected_date])
#         else:
#             self.textBrowser_2.clear()

#     def openMainPage(self):
#         main_page = MyWindow()
#         self.parent().setCentralWidget(main_page)

#     def closeEvent(self, event):
#         # 프로그램 종료 시 일정 데이터를 저장
#         self.saveScheduleData()
#         event.accept()

#     def saveScheduleData(self):
#         query = QSqlQuery()
#         query.prepare("INSERT OR REPLACE INTO schedules (date, text) VALUES (:date, :text)")
#         for date, text in self.schedule_data.items():
#             query.bindValue(":date", date.toString("yyyy-MM-dd"))
#             query.bindValue(":text", text)
#             if not query.exec_():
#                 print("Failed to save schedule data:", query.lastError().text())


# class CustomInputDialog(QInputDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         # 다이얼로그 속성 설정
#         self.setStyleSheet("background-color: lightblue;")
#         self.resize(400, 150)

#         # 텍스트 입력 위젯 스타일 설정
#         self.setInputMode(QInputDialog.TextInput)
#         self.setTextEchoMode(QLineEdit.Normal)

#         # 레이아웃 생성
#         layout = QVBoxLayout()

#         # 다이얼로그에 추가할 위젯 설정
#         self.textEdit = QLineEdit(self)
#         layout.addWidget(self.textEdit)

#         # 레이아웃 설정
#         self.setLayout(layout)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec_())

# database.close()
