from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLineEdit)
from PyQt6.QtCore import (Qt)
from PyQt6.QtGui import QAction

from typing import final

from modules.database import OhtuDatabase
from modules.bibtex import BibTeXHandler 

fields = [
    "author",
    "title",
    "journal",
    "year",
    "doi",
]

@final
class MainWindow(QMainWindow):
    def __init__(self, database: OhtuDatabase, halder: BibTeXHandler):
        super().__init__()
        self.setWindowTitle("Ohtu")

        self.handler = halder
        self.database = database

        self.bar = Bar()
        _ = self.bar.export_button.clicked.connect(self.on_export)
        _ = self.bar.add_button.clicked.connect(self.on_add)

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
        self.create_menu()
        self.show()
        
    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        help_menu = menu_bar.addMenu("Help")

        export_action = QAction("Export", self)
        import_action = QAction("Import", self)
        about_action = QAction("About", self)

        file_menu.addAction(import_action)
        file_menu.addAction(export_action)

        help_menu.addAction(about_action)

    def on_export(self):
        biptext: str = self.handler.create_bibtex_data(self.database.get_references())
        self.handler.save_to_file(biptext, "./test_biptext.bip")

    def on_add(self):
        print ("add on painettu")
        values = {name: line.text().strip() for name, line in self.editor.inputs.items()}

        if not values["author"] or not values["title"]:
            print("author ja title ovat pakollisia")
            return

        year = int(values["year"]) if values["year"].isdigit() else None

        self.database.add_reference(
            values["author"],
            values["title"],
            values["journal"] or None,
            year,
            values["doi"] or None,
        )

        for line in self.editor.inputs.values():
            line.clear()

        self.viewer.refresh()

        

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
        self.database = database
        self.refresh()

    def refresh(self):
        self.clear()
        # // Display database references as Source list items.
        for reference in self.database.get_references():
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