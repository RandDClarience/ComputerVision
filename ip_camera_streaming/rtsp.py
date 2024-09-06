import sys
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap

class RTSPStream(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Camera Stream")
        self.setGeometry(100, 100, 800, 600)
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

        # Set up RTSP streams (replace with your actual URLs or test methods)
        self.rtsp_urls = [
            "path/to/video1.mp4",  # Example: using sample video files
            "path/to/video2.mp4",
            "path/to/video3.mp4"
        ]
        self.caps = [cv2.VideoCapture(url) for url in self.rtsp_urls]

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
                self.camera_labels[i].setPixmap(pixmap.scaled(self.camera_labels[i].size(), Qt.AspectRatioMode.KeepAspectRatio))
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
    app = QApplication(sys.argv)
    window = RTSPStream()
    window.showMinimized()    
    sys.exit(app.exec())