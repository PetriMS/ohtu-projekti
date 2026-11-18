from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QListWidget, QPushButton,
)

sources = [
    {"id": 0, "name": "Source A", "from": "Website", "writers": ["Alice Johnson", "Mark Lee"], "tags": ["technology", "ai", "news"]},
    {"id": 1, "name": "Source B", "from": "Book", "writers": ["Elena Petrova"], "tags": ["history", "europe", "biography"]},
    {"id": 2, "name": "Source C", "from": "Magazine", "writers": ["David Kim", "Alice Johnson"], "tags": ["design", "architecture", "technology"]},
    {"id": 3, "name": "Source D", "from": "Podcast", "writers": ["Tom Becker"], "tags": ["economics", "interview", "news"]},
    {"id": 4, "name": "Source E", "from": "Website", "writers": ["Priya Sharma", "Lucas Martin", "Elena Petrova"], "tags": ["science", "climate", "research"]},
    {"id": 5, "name": "Source F", "from": "Journal", "writers": ["Dr. Oliver Grant"], "tags": ["science", "medicine", "research"]},
    {"id": 6, "name": "Source G", "from": "Book", "writers": ["Maria Lopez", "James O'Connor"], "tags": ["fiction", "mystery", "history"]},
    {"id": 7, "name": "Source H", "from": "Newspaper", "writers": ["Kenji Tanaka", "Mark Lee"], "tags": ["politics", "news", "opinion"]},
    {"id": 8, "name": "Source I", "from": "Video", "writers": ["Emma Wilson"], "tags": ["tutorial", "programming", "ai"]},
    {"id": 9, "name": "Source J", "from": "Website", "writers": [], "tags": ["travel", "food"]},
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
