from PyQt5 import QtCore, QtGui,QtWidgets
import sys,res
import random
import datetime
import webbrowser
import AppOpener
import pyttsx3
import pywhatkit
import speech_recognition as sr
import wikipedia
import requests
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder
import cv2

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(524, 709)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # =================================================================================================================================================
        engine = pyttsx3.init()

        def say(s):
            engine.say(s)
            engine.runAndWait()
            engine.setProperty('rate', 225)
            engine.setProperty('volume', 1.0)
        def TakeCommand():
            r=sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold=1
                audio=r.listen(source)
            try:
                print("Recognizing...")
                query=r.recognize_google(audio,language='en-in')
                print(f"Your command: {query}\n")
            except:
                return
            return query.lower()
        def TakeCommand_hindi():
            r=sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold=1
                audio=r.listen(source)
            try:
                print("Recognizing...")
                query=r.recognize_google(audio,language='hi')
                print(f"Your command: {query}\n")
            except:
                return
            return query.lower()

        def mylocation():
            ip_add = requests.get('https://api.ipify.org').text
            url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
            geo_q = requests.get(url)
            geo_d = geo_q.json()
            state = geo_d['city']
            country = geo_d['country']
            self.text_area.append(f"You are now in {state}, {country}")
            say(f"You are now in {state, country}")
            self.e.setText("")

        def googlemaps(place):
            url_place = "https://www.google.com/maps/place/" + str(place)
            geolocator = Nominatim(user_agent="myGeocoder")
            location = geolocator.geocode(place, addressdetails=True)
            target_latlon = location.latitude, location.longitude
            location = location.raw['address']

            target = {
                'city': location.get('city', ''),
                'state': location.get('state', ''),
                'country': location.get('country', '')
            }
            current_loc = geocoder.ip('me')
            current_latlon = current_loc.latlng

            distance = str(great_circle(current_latlon, target_latlon))
            distance = str(distance.split()[0])
            distance = round(float(distance), 2)

            webbrowser.open(url=url_place)

            for key,values in target.items():
                self.text_area.append(f"{key}: {str(values)} \n")
            self.text_area.append(f"{place} is {distance} Km away from your location")
            self.e.setText("")

        def face_recognition():
            # Load the pre-trained face detector from OpenCV
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            # Open the camera
            cap = cv2.VideoCapture(0)

            while True:
                # Capture frame from camera
                ret, frame = cap.read()

                # Convert frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect faces in the frame
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                      flags=cv2.CASCADE_SCALE_IMAGE)

                # Draw rectangles around the detected faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display the frame with face detection result
                cv2.imshow('Face Detection', frame)

                # Exit the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release the camera and close all OpenCV windows
            cap.release()
            cv2.destroyAllWindows()
            cv2.destroy()

        # =================================================================================================================================================

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, -10, 570, 680))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 500, 720))
        self.label.setStyleSheet("border-image: url(:/images/C:/Users/Hriday panchal/Downloads/background.png);\n"
"border-radius:20px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(0, 10, 500, 720))
        self.label_2.setStyleSheet("background-color:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:0.715909,stop:0 rgbs(0,0,0,9),stop:0.375 rgba(0,0,0,50),stop:0.835227 rgba(0,0,0,75));\n"
"border-image: url(:/images/background.png);\n"
"border-radius:20px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        # Text area
        self.text_area = QtWidgets.QTextEdit(self.widget)
        self.text_area.setGeometry(QtCore.QRect(10, 20, 481, 581))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.text_area.setFont(font)
        self.text_area.setAutoFillBackground(False)
        self.text_area.setStyleSheet("background-color:rgba(0,0,0,100);\n"
                                     "border-radius:15px;")
        self.text_area.setObjectName("text_area")

        #close button
        self.close = QtWidgets.QPushButton(self.widget)
        self.close.setGeometry(QtCore.QRect(460, 30, 21, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)

        #Entry box
        self.e = QtWidgets.QLineEdit(self.widget)
        self.e.setGeometry(QtCore.QRect(20, 610, 331, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.e.setFont(font)
        self.e.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105,118,132,255);\n"
"color:rgba(255,255,255,230);\n"
"padding-bottom:7px;")
        self.e.setObjectName("e")

        # =================================================================================================================================================
        #important
        now=datetime.datetime.now()
        time=str(now.strftime("%H:%M:%S"))
        date=str(now.strftime("%Y-%m-%d"))
        # =================================================================================================================================================
        responses = {
            "hello": ["Hello!", "Hi there!", "Hey!"],
            "hi": ["Hello!", "Hi there!", "Hey!"],
            "hey": ["Hello!", "Hi there!", "Hey!"],
            "how are you": ["I'm doing well, thank you.", "I'm fine, thanks for asking.", "I'm good, how are you?"],
            "goodbye": ["Goodbye!", "See you later!", "Bye!"],
            "your name": ["Aaron","It's Aaron"],
            "what is your name": ["Aaron","It's Aaron"],
            "time": [time],
            "date": [date],
            "help": ["Police   100 \n Fire   101 \n Ambulance   102 \n child help   1098 \n Gas leakage   1906 \n Thane civil hospital   022-25472582 \n Railway enquiry   139"],
            "helpline": ["Police   100 \n Fire   101 \n Ambulance   102 \n child help   1098 \n Gas leakage   1906 \n Thane civil hospital   022-25472582 \n Railway enquiry   139"]
        }
        links={
            "chrome": "http://www.google.com",
            "youtube": "https://www.youtube.com/",
            "maps": "https://www.google.com/maps",
            "facebook": "http://www.facebook.com",
            "instagram": "http://www.instagram.com"
        }
        apps={
            "notepad":"notepad",
            "whatsapp":"whatsapp",
            "calc":"calculator",
            "calculator":"calculator",
            "calendar":"calendar",
            "spotify":"spotify",
            "clock":"clock",
            "paint":"paint",
            "camera":"camera"
        }

        # =================================================================================================================================================
        user_input=""
        def respond():
            global user_input
            user_input = self.e.text().lower()
            self.text_area.append(f"User: " + user_input + "\n")
            if user_input.lower() == "exit":
                MainWindow.destroy()  # Exit the Tkinter app if user types "exit"

            for i in responses:
                if user_input.lower() in i:
                    bot_response = random.choice(responses[i])
                    self.text_area.append(f"Bot: " + bot_response + "\n")
                    say(bot_response)
                    self.e.setText("")
                    return

            for j in links:
                if user_input.lower() in j:
                    webbrowser.open(links[j])
                    self.text_area.append(f"Bot: Opening {j} \n")
                    say(f"Opening {j}")
                    self.e.setText("")
                    return

            for k in apps:
                if user_input.lower() in k:
                    AppOpener.open(apps[k])
                    self.text_area.append(f"Bot: Opening {k} \n")
                    say(f"Opening {k}")
                    self.e.setText("")
                    return

            if "google search" in user_input.lower():
                user_input = user_input.replace("google search", "")
                user_input = user_input.replace("google", "")
                pywhatkit.search(user_input)
                self.text_area.append(f"Bot: Searching {user_input}...")
                say(f"searching {user_input}")
                self.e.setText("")
            elif "on youtube" in user_input.lower():
                user_input = user_input.replace("on youtube", "")
                user_input = user_input.replace("youtube", "")
                pywhatkit.playonyt(user_input)
                self.text_area.append(f"Bot: Searching {user_input} on youtube...")
                say(f"playing {user_input} on youtube")
                self.e.setText("")
            elif "my location" in user_input.lower():
                mylocation()
            elif ("distance to") in user_input.lower():
                user_input=user_input.replace("distance to","")
                query=user_input
                googlemaps(query)
            elif "face recognition" in user_input.lower():
                face_recognition()

            else:
                self.text_area.append(f"Bot: I'm sorry, I don't understand what you're saying." + "\n")
                say(f"Bot: I'm sorry, I don't understand what you're saying.")
                self.e.setText("")
                return

        #Send button
        self.send_b = QtWidgets.QPushButton(self.widget)
        self.send_b.clicked.connect(lambda: respond())
        self.send_b.setGeometry(QtCore.QRect(360, 620, 61, 31))
        self.send_b.setStyleSheet("QPushButton#send_b{\n"
"    background-color: qlineargradient(spread:pad,x1:0,y1:0.505682,x2:1,y2:0.477,stop:0 rgba(20,47,78,219), stop:1 rgba(85,98,112,226));\n"
"    color: rgba(225,225,225,210);\n"
"    border-radius:5px;\n"
"}\n"
"\n"
"QPushButton#send_b:hover{\n"
"    background-color: qlineargradient(spread:pad,x1:0,y1:0.505682,x2:1,y2:0.477,stop:0 rgba(20,67,98,219), stop:1 rgba(105,118,132,226));\n"
"    color: rgba(225,225,225,210);\n"
"    border-radius:5px;\n"
"}\n"
"\n"
"QPushButton#send_b:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(105,118,132,200);\n"
"}")
        self.send_b.setObjectName("send_b")

        self.text_area.append(f"Welcome sir \nIts aaron at you service \nHow can I help you?? \n")

        #clear button
        self.clear_b = QtWidgets.QPushButton(self.widget)
        self.clear_b.setGeometry(QtCore.QRect(430, 620, 61, 31))
        self.clear_b.clicked.connect(lambda:delete_text())

        def delete_text():
            self.text_area.clear()

        self.clear_b.setStyleSheet("QPushButton#clear_b{\n"
"    background-color: qlineargradient(spread:pad,x1:0,y1:0.505682,x2:1,y2:0.477,stop:0 rgba(20,47,78,219), stop:1 rgba(85,98,112,226));\n"
"    color: rgba(225,225,225,210);\n"
"    border-radius:5px;\n"
"}\n"
"\n"
"QPushButton#clear_b:hover{\n"
"    background-color: qlineargradient(spread:pad,x1:0,y1:0.505682,x2:1,y2:0.477,stop:0 rgba(20,67,98,219), stop:1 rgba(105,118,132,226));\n"
"    color: rgba(225,225,225,210);\n"
"    border-radius:5px;\n"
"}\n"
"\n"
"QPushButton#clear_b:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(105,118,132,200);\n"
"}")
        self.clear_b.setObjectName("clear_b")

        #exit button
        self.close.setFont(font)
        self.close.clicked.connect(lambda: exit_window())
        def exit_window():
            MainWindow.close()
        self.close.setStyleSheet("QPushButton#exit{\n"
"    background-color: qlineargradient(spread:pad,x1:0,y1:0.505682,x2:1,y2:0.477,stop:0 rgba(0,0,0,50), stop:1 rgba(0,0,0,50));\n"
"    color: rgba(0,0,0,50);\n"
"    border-radius:99px;\n"
"}\n"
"\n"
"QPushButton#exit:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(0,0,0,50);\n"
"}")
        self.close.setObjectName("exit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.e.setPlaceholderText(_translate("MainWindow", "Type here"))
        self.send_b.setText(_translate("MainWindow", "Send"))
        self.send_b.setShortcut(_translate("MainWindow", "Return"))
        self.clear_b.setText(_translate("MainWindow", "Clear"))
        self.close.setText(_translate("MainWindow", "x"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
