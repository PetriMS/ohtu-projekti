from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLineEdit)
from PyQt6.QtCore import (Qt)

from typing import final

from modules import database
from modules.database import OhtuDatabase
from modules.bibtex import BibTeXHandler 

fields = [
    "author",
    "title",
    "publisher",
    "address",
    "year",
    "tag",
    "id",
]

@final
class MainWindow(QMainWindow):
    def __init__(self, database: OhtuDatabase, halder: BibTeXHandler):
        super().__init__()
        self.setWindowTitle("Hello, World!")

        self.handler = halder
        self.database = database

        self.bar = Bar()
        _ = self.bar.export_button.clicked.connect(self.on_export)

        self.editor = SourceEditor()
        self.viewer = SourceViewer(self.database)

        split = QHBoxLayout()
        split.addWidget(self.editor)
        split.addWidget(self.viewer)

        layout = QVBoxLayout()
        layout.addWidget(self.bar)
        layout.addLayout(split)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.show()

    def on_export(self):
        print("exporting")
        biptext: str = self.handler.create_bibtex_data(database.get_references())
        self.handler.save_to_file("./test_biptext.bip", biptext)
        # for reference in self.database.haeViittaus():
        #     self.addItem(Source(*reference))

@final
class Bar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout();

        self.export_button = QPushButton("export")
        layout.addWidget(self.export_button)

        self.add_button = QPushButton("add")
        layout.addWidget(self.add_button)

        self.edit_button = QPushButton("edit")
        layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("delete")
        layout.addWidget(self.delete_button)

        self.uncheck_button = QPushButton("uncheck")
        layout.addWidget(self.uncheck_button)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("search")
        layout.addWidget(self.search_input)

        self.setLayout(layout)

@final
class SourceEditor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout();

        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.inputs: dict[str, QLineEdit] = {} 
        for field in fields:
            line = QLineEdit()
            line.setPlaceholderText(field)
            line.setAlignment(Qt.AlignmentFlag.AlignTop)
            layout.addWidget(line)
            self.inputs[field] = line

        self.setLayout(layout)

class SourceViewer(QListWidget):
    def __init__(self, database: OhtuDatabase):
        super().__init__()
        # // Display database references as Source list items.
        for reference in database.get_references():
            self.addItem(Source(*reference))

@final
class Source(QListWidgetItem):
    def __init__(
        self,
        source_id: int,
        author: str,
        title: str,
        journal: str | None,
        year: int | None,
        doi: str | None,
    ):
        details = [value for value in (author, journal, str(year) if year is not None else None) if value]
        super().__init__(f"{title} — {', '.join(details)}")
        # // Keep the database ID on each item for future selection and editing actions.
        self.id = source_id
        self.author = author
        self.title = title
        self.journal = journal
        self.year = year
        self.doi = doi
