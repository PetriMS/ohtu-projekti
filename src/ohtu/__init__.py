from PyQt6.QtWidgets import QApplication

from ohtu.windows.main import MainWindow

def main() -> None:
    app = QApplication([])
    window = MainWindow()
    app.exec()


if __name__ == "__main__":
    main()
