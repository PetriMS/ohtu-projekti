from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QLineEdit)
from PyQt6.QtCore import (Qt)

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

fields = [
    "author",
    "title",
    "publisher",
    "address",
    "year",
    "tag",
    "id",
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello, World!")

        bar = Bar()
        editor = SourceEditor()
        viewer = SourceViewer()

        split = QHBoxLayout()
        split.addWidget(editor)
        split.addWidget(viewer)

        layout = QVBoxLayout()
        layout.addWidget(bar)
        layout.addLayout(split)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.show()

class Bar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout();

        layout.addWidget(QPushButton("add"))
        layout.addWidget(QPushButton("edit"))
        layout.addWidget(QPushButton("delete"))
        layout.addWidget(QPushButton("uncheck"))

        search = QLineEdit()
        search.setPlaceholderText("search")
        layout.addWidget(search)

        self.setLayout(layout)

class SourceEditor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout();

        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        for field in fields:
            line = QLineEdit()
            line.setPlaceholderText(field)
            line.setAlignment(Qt.AlignmentFlag.AlignTop)
            layout.addWidget(line)

        self.setLayout(layout)

class SourceViewer(QListWidget):
    def __init__(self):
        super().__init__()
        for source in sources:
            self.addItem(f"{source['name']} — {source['from']}")

class Source(QWidget):
    def __init__(self):
        super().__init__()
