import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QLabel, QInputDialog, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QScreen, QIcon
from datetime import datetime, timedelta

class TimeProgressApp(QWidget):
    def __init__(self):
        super().__init__()
        self.user_age = self.get_user_info("user_age.txt", "Enter your age:", QInputDialog.IntInput)
        self.deadline_days = self.get_user_info("deadline.txt", "Days to next d3adl1n3:", QInputDialog.IntInput)
        self.deadline_date = datetime.now() + timedelta(days=self.deadline_days)
        self.initUI()
        self.initTray()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress_bars)
        self.timer.start(1000)

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen: QScreen = QApplication.primaryScreen()
        screen_rect: QRect = screen.availableGeometry()
        self.setGeometry(screen_rect.width() - 210, 30, 200, 300)

        self.setWindowTitle('Time Progress')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setStyleSheet("background-color: black;")

        self.progress_bars = {}
        self.days_left_labels = {}

        for period in ['day', 'week', 'month', 'year', 'life', 'd3adl1n3']:
            bar = QProgressBar(self)
            bar.setTextVisible(True) if period != 'd3adl1n3' else bar.setTextVisible(False)
            bar.setStyleSheet("""
                QProgressBar {
                    border: 2px solid white;
                    background-color: black;
                    text-align: center;
                    color: white;
                }
                QProgressBar::chunk {
                    background-color: white;
                }
            """)

            label = QLabel(period.capitalize())
            label.setStyleSheet("color: white;")

            days_left_label = QLabel()
            days_left_label.setStyleSheet("color: white;")
            

            self.layout.addWidget(label)
            self.layout.addWidget(bar)
            self.layout.addWidget(days_left_label)

            self.progress_bars[period] = bar
            self.days_left_labels[period] = days_left_label

    def initTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("in_time.ico"))  
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)

        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(app.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def get_user_info(self, file_name, label_text, input_mode):
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                return int(file.read().strip())
        else:
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
            dialog.setLabelText(label_text)
            dialog.setInputMode(input_mode)

            ok = dialog.exec_()
            value = dialog.intValue()

            if ok:
                with open(file_name, "w") as file:
                    file.write(str(value))
                return value
            else:
                sys.exit()

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
            end = start + timedelta(days=78*365)
        elif period == 'd3adl1n3':
            start = now
            end = self.deadline_date

        progress = (now - start).total_seconds() / (end - start).total_seconds()
        return progress

    def update_progress_bars(self):
        for period, bar in self.progress_bars.items():
            progress = self.calculate_progress(period)
            bar.setValue(int(progress * 100))

            if period != 'd3adl1n3':
                bar.setFormat(f"{int(progress * 100)}%")

            if period == 'd3adl1n3':
                days_left = max((self.deadline_date - datetime.now()).days, 0)
                self.days_left_labels[period].setText(f"{days_left} days left")

                if days_left == 0:
                    new_deadline = self.get_user_info("deadline.txt", "Days to next d3adl1n3:", QInputDialog.IntInput)
                    self.deadline_date = datetime.now() + timedelta(days=new_deadline)

    def run(self):
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TimeProgressApp()
    ex.run()
    sys.exit(app.exec_())
