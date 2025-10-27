import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Task Week 3 - (F1D02310141 - Umam Alparizi)')
        self.setGeometry(400, 250, 500, 300)
        self.setMouseTracking(True)

        self.label = QLabel('X: 0, Y: 0', self)
        self.label.setAlignment(Qt.AlignCenter)

        self.label.setStyleSheet("""
            background-color: rgba(200, 200, 200, 150);
            padding: 8px;
            border-radius: 4px;
        """)

        self.label.adjustSize()

        self.label.setMouseTracking(True)

        self.label.installEventFilter(self)

        self.positionLabelInCenter()

    def positionLabelInCenter(self):
        self.label.move(
            (self.width() - self.label.width()) // 2,
            (self.height() - self.label.height()) // 2
        )

    def resizeEvent(self, event):
        self.positionLabelInCenter()

    def eventFilter(self, obj, event):
        if obj is self.label and event.type() == QEvent.Enter:

            new_x = random.randint(10, self.width() - self.label.width() - 10)
            new_y = random.randint(10, self.height() - self.label.height() - 10)
            self.label.move(new_x, new_y)
            return True
        return super().eventFilter(obj, event)

    def mouseMoveEvent(self, event):
        self.label.setText(f'X: {event.x()}, Y: {event.y()}')
        self.label.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
