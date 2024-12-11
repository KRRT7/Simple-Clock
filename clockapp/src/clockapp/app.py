"""
a simple clock app for your basic needs
"""

import importlib.metadata
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PySide6.QtGui import QFontDatabase, QFont, QPixmap
from PySide6.QtCore import Qt, QPoint, QTimer, QTime
from pathlib import Path
import pkgutil


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resources_path = Path(__file__).parent / "resources"
        self.settings_file = self.resources_path / "settings.txt"
        self.WIDTH = 600
        self.HEIGHT = 125
        self.setWindowTitle("Simple Clock")
        self.setGeometry(
            self.get_position("x"), self.get_position("y"), self.WIDTH, self.HEIGHT
        )
        self.setWindowIcon(QPixmap(self.resources_path / "Simple_Clock.ico"))

        self.is_dragging = False
        self.drag_start_pos = QPoint()
        self.__init__UI()

    def __init__UI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create Gui | Main
        self.time_label = QLabel(self)
        self.timer = QTimer(self)
        self.close_button = QPushButton("X", self)
        self.clock_type_button = QPushButton("↔", self)

        # Set Geometry | Main
        self.time_label.setGeometry(0, 0, self.WIDTH, self.HEIGHT)
        self.close_button.setGeometry(self.WIDTH - 25, 5, 20, 20)
        self.clock_type_button.setGeometry(self.WIDTH - 25, self.HEIGHT - 25, 20, 20)

        # Set Font | Main
        font_id = QFontDatabase.addApplicationFont(
            str(self.resources_path / "digital-7.ttf")
        )
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        my_font = QFont(font_family, 95)
        self.time_label.setFont(my_font)

        # Set Settings | Main
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.close_button.clicked.connect(self.close_window)
        self.clock_type_button.clicked.connect(self.change_clock_type)

        self.update_time()

        # Set stylesheet | Main
        self.time_label.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            QLabel{
                border: 2px solid #ffffff;
                border-radius: 5px;
                color: #ffffff;
                background-color: #000000;
            }
            QPushButton{
                font: bold;
                border: 2px solid #ffffff;
                border-radius: 10px;
                color: #ffffff;
                background-color: #000000;
            }
            QPushButton::hover{
                border: 2px solid #0099ff;
                color: #0099ff;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_start_pos = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            self.move(event.globalPosition().toPoint() - self.drag_start_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            event.accept()

    def update_time(self):
        with self.settings_file.open("r") as file:
            clock_type = file.readlines()[0]

            if clock_type == "24":
                current_time = QTime.currentTime().toString("hh:mm:ss")
                self.time_label.setText(current_time)
            elif clock_type == "12":
                current_time = QTime.currentTime().toString("hh:mm:ss AP")
                self.time_label.setText(current_time)
            else:
                current_time = QTime.currentTime().toString("hh:mm:ss AP")
                self.time_label.setText(current_time)

    def close_window(self):
        x_pos = self.pos().x()
        y_pos = self.pos().y()

        data = self.settings_file.read_text().splitlines()
        data[1] = str(x_pos)
        data[2] = str(y_pos)

        self.settings_file.write_text("\n".join(data))

        self.close()

    def change_clock_type(self):
        data = self.settings_file.read_text().splitlines()

        if data[0] == "12":
            data[0] = "24"
        else:
            data[0] = "12"

        self.settings_file.write_text("\n".join(data))

        self.update_time()

    def get_position(self, position: str):
        data = self.settings_file.read_text().splitlines()

        x_pos = int(data[1])
        y_pos = int(data[2])

        if position == "x":
            return x_pos
        elif position == "y":
            return y_pos
        else:
            return 0


def main():
    app_module = sys.modules["__main__"].__package__
    metadata = importlib.metadata.metadata(app_module)
    app = QApplication(sys.argv)
    app.setApplicationName(metadata["Formal-Name"])
    main = MainApp()
    main.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
