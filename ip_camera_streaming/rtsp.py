

rtsp_url = "rtsp://169.254.48.32:554/picstream"

import sys
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap

class RTSPStream(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RTSP Stream")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Make the window borderless

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.label)

        self.rtsp_url = rtsp_url 
        self.cap = cv2.VideoCapture(self.rtsp_url)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30 ms (roughly 33 fps)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.label.setPixmap(pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio))

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
    window.show()
    sys.exit(app.exec())