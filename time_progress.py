import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QLabel, QInputDialog
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QScreen
from datetime import datetime, timedelta

class TimeProgressApp(QWidget):
    def __init__(self):
        super().__init__()
        self.user_age = self.get_user_age()
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress_bars)
        self.timer.start(1000)

    def initUI(self):
        # Set window attributes for borderless display
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set the window position to the top right corner of the screen
        screen: QScreen = QApplication.primaryScreen()
        screen_rect: QRect = screen.availableGeometry()
        self.setGeometry(screen_rect.width() - 210, 30, 200, 200)

        self.setWindowTitle('Time Progress')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Set main window background to black
        self.setStyleSheet("background-color: black;")
        
        self.progress_bars = {
            'day': QProgressBar(self),
            'week': QProgressBar(self),
            'month': QProgressBar(self),
            'year': QProgressBar(self),
            'life': QProgressBar(self)
        }

        for period, bar in self.progress_bars.items():
            bar.setTextVisible(True)
            
            # Set the QLabel text color to white
            label = QLabel(period.capitalize())
            label.setStyleSheet("color: white;")
            
            # Set the QProgressBar colors
            bar.setStyleSheet("""
                QProgressBar {
                    border: 2px solid white;
                    text-align: center;
                    color: white;
                    background-color: black;
                }
                QProgressBar::chunk {
                    background-color: white;
                }
            """)
            
            self.layout.addWidget(label)
            self.layout.addWidget(bar)

    def get_user_age(self):
        # Check if age file exists
        if os.path.exists("user_age.txt"):
            with open("user_age.txt", "r") as file:
                return int(file.read().strip())
        else:
            # If file doesn't exist, ask for age
            dialog = QInputDialog(self)
            dialog.setStyleSheet("""
                QWidget {
                    background-color: black;
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    color: white;
                    background-color: black;
                    border: 1px solid white;
                }
                QLineEdit {
                    color: white;
                    background-color: black;
                    border: 1px solid white;
                }
            """)
            dialog.setWindowTitle("Input Dialog")
            dialog.setLabelText("Enter your age:")
            dialog.setInputMode(QInputDialog.IntInput)

            ok = dialog.exec_()
            age = dialog.intValue()

            if ok:
                with open("user_age.txt", "w") as file:
                    file.write(str(age))
                return age
            else:
                sys.exit()  # exit if the user cancels the dialog

    def calculate_progress(self, period):
        now = datetime.now()
        if period == 'day':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
        elif period == 'week':
            start = now - timedelta(days=now.weekday())
            end = start + timedelta(weeks=1)
        elif period == 'month':
            start = now.replace(day=1)
            end = (start + timedelta(days=32)).replace(day=1)
        elif period == 'year':
            start = now.replace(month=1, day=1)
            end = start + timedelta(days=365)
        elif period == 'life':
            start = datetime(now.year - self.user_age, 1, 1)
            end = start + timedelta(days=78*365)  # assuming the average lifespan is 78 years
        progress = (now - start) / (end - start)
        return progress

    def update_progress_bars(self):
        for period, bar in self.progress_bars.items():
            progress = self.calculate_progress(period)
            bar.setValue(int(progress * 100))

    def run(self):
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TimeProgressApp()
    ex.run()
    sys.exit(app.exec_())
