import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QSlider, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

class FontAdjuster(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Task Week 6 - Font and Color Adjuster')
        self.setGeometry(300, 300, 500, 400)
        self.setMinimumSize(450, 300)

        self.setStyleSheet("""
            QWidget {
                background-color: #2D2D2D;
                color: white;
                font-family: Arial;
            }
            QLabel {
                color: white;
            }
        """)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(30, 30, 30, 30)
        mainLayout.setSpacing(20)

        self.textDisplayFrame = QFrame()
        self.textDisplayFrame.setFrameShape(QFrame.Box)
        self.textDisplayFrame.setStyleSheet("""
            background-color: white;
            border: 1px solid #444444;
            border-radius: 0px;
        """)

        textDisplayLayout = QVBoxLayout(self.textDisplayFrame)
        textDisplayLayout.setContentsMargins(0, 0, 0, 0)

        self.textLabel = QLabel('UMAM ALPARIZI\nF1D02310141')
        self.textLabel.setAlignment(Qt.AlignCenter)
        self.textLabel.setWordWrap(True)

        font = QFont('Arial', 20)
        self.textLabel.setFont(font)
        self.textLabel.setStyleSheet("color: black; background-color: white;")

        textDisplayLayout.addWidget(self.textLabel)
        mainLayout.addWidget(self.textDisplayFrame)

        fontSizeLayout = QHBoxLayout()
        fontSizeLayout.setSpacing(15)

        fontSizeLabel = QLabel('Font Size')
        fontSizeLabel.setStyleSheet("color: white; font-size: 16px;")
        fontSizeLabel.setMinimumWidth(120)

        self.fontSizeSlider = QSlider(Qt.Horizontal)
        self.fontSizeSlider.setMinimum(20)
        self.fontSizeSlider.setMaximum(60)
        self.fontSizeSlider.setValue(36)
        self.fontSizeSlider.setTickPosition(QSlider.TicksBelow)
        self.fontSizeSlider.setTickInterval(10)
        self.fontSizeSlider.valueChanged.connect(self.updateFontSize)
        self.fontSizeSlider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #555555;
            }
            QSlider::handle:horizontal {
                background: #858585;
                width: 15px;
                height: 15px;
                margin: -6px 0;
                border-radius: 7px;
            }
            QSlider::sub-page:horizontal {
                background: #555555;
            }
        """)

        fontSizeLayout.addWidget(fontSizeLabel)
        fontSizeLayout.addWidget(self.fontSizeSlider)
        mainLayout.addLayout(fontSizeLayout)

        bgColorLayout = QHBoxLayout()
        bgColorLayout.setSpacing(15)

        bgColorLabel = QLabel('Background Color')
        bgColorLabel.setStyleSheet("color: white; font-size: 16px;")
        bgColorLabel.setMinimumWidth(120)

        self.bgColorSlider = QSlider(Qt.Horizontal)
        self.bgColorSlider.setMinimum(0)
        self.bgColorSlider.setMaximum(255)
        self.bgColorSlider.setValue(255)
        self.bgColorSlider.setTickPosition(QSlider.TicksBelow)
        self.bgColorSlider.setTickInterval(25)
        self.bgColorSlider.valueChanged.connect(self.updateBgColor)
        self.bgColorSlider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #555555;
            }
            QSlider::handle:horizontal {
                background: #858585;
                width: 15px;
                height: 15px;
                margin: -6px 0;
                border-radius: 7px;
            }
            QSlider::sub-page:horizontal {
                background: #555555;
            }
        """)

        bgColorLayout.addWidget(bgColorLabel)
        bgColorLayout.addWidget(self.bgColorSlider)
        mainLayout.addLayout(bgColorLayout)

        fontColorLayout = QHBoxLayout()
        fontColorLayout.setSpacing(15)

        fontColorLabel = QLabel('Font Color')
        fontColorLabel.setStyleSheet("color: white; font-size: 16px;")
        fontColorLabel.setMinimumWidth(120)

        self.fontColorSlider = QSlider(Qt.Horizontal)
        self.fontColorSlider.setMinimum(0)
        self.fontColorSlider.setMaximum(255)
        self.fontColorSlider.setValue(0)
        self.fontColorSlider.setTickPosition(QSlider.TicksBelow)
        self.fontColorSlider.setTickInterval(25)
        self.fontColorSlider.valueChanged.connect(self.updateFontColor)
        self.fontColorSlider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #555555;
            }
            QSlider::handle:horizontal {
                background: #858585;
                width: 15px;
                height: 15px;
                margin: -6px 0;
                border-radius: 7px;
            }
            QSlider::sub-page:horizontal {
                background: #555555;
            }
        """)

        fontColorLayout.addWidget(fontColorLabel)
        fontColorLayout.addWidget(self.fontColorSlider)
        mainLayout.addLayout(fontColorLayout)

        self.setLayout(mainLayout)

    def updateFontSize(self):
        size = self.fontSizeSlider.value()
        font = self.textLabel.font()
        font.setPointSize(size)
        self.textLabel.setFont(font)

    def updateBgColor(self):
        value = self.bgColorSlider.value()
        self.textDisplayFrame.setStyleSheet(f"""
            background-color: rgb({value}, {value}, {value});
            border: 1px solid #444444;
        """)

        self.updateFontColor()

    def updateFontColor(self):
        bg_value = self.bgColorSlider.value()
        font_value = self.fontColorSlider.value()

        self.textLabel.setStyleSheet(f"""
            color: rgb({font_value}, {font_value}, {font_value});
            background-color: transparent;
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FontAdjuster()
    ex.show()
    sys.exit(app.exec_())
