from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QListWidget, QPushButton,
)

sources = [
    {"name": "Source A", "from": "Website", "writers": [], "categories": [], "tags": []},
    {"name": "Source B", "from": "Book", "writers": [], "categories": [], "tags": []},
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello, World!")

        source_list = QListWidget()
        for source in sources:
            source_list.addItem(f"{source['name']} — {source['from']}")

        button = QPushButton("Exit")
        button.pressed.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(source_list)
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.show()


def main() -> None:
    app = QApplication([])
    window = MainWindow()
    app.exec()


if __name__ == "__main__":
    main()
