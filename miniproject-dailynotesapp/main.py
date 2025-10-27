from PyQt5.QtWidgets import QApplication
from ui_main import NotesMainWindow

def main():
    app = QApplication([])

    window = NotesMainWindow()
    window.show()

    app.exec_()

if __name__ == "__main__":
    main()
