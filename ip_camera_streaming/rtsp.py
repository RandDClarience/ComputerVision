import sys
import cv2
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap

class RTSPStream(QMainWindow):
    def __init__(self, config):
        super().__init__()

        # Set window size to fit 1280x800 display
        self.setWindowTitle("Multi-Camera Stream (RTSP)")
        self.setGeometry(100, 100, 1280, 800)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showMinimized()

        # Create layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create camera labels using QGridLayout
        camera_layout = QGridLayout()
        self.camera_labels = []

        # Top-left camera
        label1 = QLabel(self)
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label1.setText("NO SIGNAL\nCamera 1")
        label1.setStyleSheet("border: 1px solid black;")
        self.camera_labels.append(label1)
        camera_layout.addWidget(label1, 0, 0)

        # Top-right camera
        label2 = QLabel(self)
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label2.setText("NO SIGNAL\nCamera 2")
        label2.setStyleSheet("border: 1px solid black;")
        self.camera_labels.append(label2)
        camera_layout.addWidget(label2, 0, 1)

        # Bottom camera
        label3 = QLabel(self)
        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label3.setText("NO SIGNAL\nCamera 3")
        label3.setStyleSheet("border: 1px solid black;")
        self.camera_labels.append(label3)
        camera_layout.addWidget(label3, 1, 0, 1, 2)

        main_layout.addLayout(camera_layout)

        # Set QLabel sizes
        self.top_camera_size = (640, 360)  # Size for top cameras maintaining 16:9 aspect ratio
        self.bottom_camera_size = (1280, 720)  # Size for bottom camera with fixed 720p resolution

        # Set top cameras size
        self.camera_labels[0].setFixedSize(*self.top_camera_size)
        self.camera_labels[1].setFixedSize(*self.top_camera_size)

        # Set bottom camera size
        self.camera_labels[2].setFixedSize(*self.bottom_camera_size)

        # Set up RTSP streams from config
        try:
            self.rtsp_urls = config["rtsp_urls"]
            if len(self.rtsp_urls) != len(self.camera_labels):
                raise ValueError("The number of RTSP URLs does not match the number of camera labels.")
        except KeyError:
            print("Error: 'rtsp_urls' key not found in the config file.")
            sys.exit(1)
        except ValueError as ve:
            print(f"Error: {ve}")
            sys.exit(1)

        # Initialize video captures
        self.caps = [cv2.VideoCapture(url, cv2.CAP_FFMPEG) for url in self.rtsp_urls]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(30)

    def update_frames(self):
        for i, cap in enumerate(self.caps):
            ret, frame = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)

                if i < 2:  # Top cameras
                    # Scale the pixmap while maintaining aspect ratio
                    label_size = self.camera_labels[i].size()
                    scaled_pixmap = pixmap.scaled(label_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                else:  # Bottom camera
                    # Stretch the pixmap to fill the QLabel
                    label_size = self.camera_labels[i].size()
                    scaled_pixmap = pixmap.scaled(label_size, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

                self.camera_labels[i].setPixmap(scaled_pixmap)
                self.camera_labels[i].setText("")

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == '__main__':
    # Load config from JSON
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: 'config.json' file not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from 'config.json'.")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = RTSPStream(config)
    window.show()    
    sys.exit(app.exec())
