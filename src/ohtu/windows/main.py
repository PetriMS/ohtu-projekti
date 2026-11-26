from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLineEdit, QMessageBox, QDateEdit)
from PyQt6.QtCore import (Qt, QDate)
from PyQt6.QtGui import QAction

from typing import final

from modules.database import OhtuDatabase
from modules.bibtex import BibTeXHandler 

@final
class MainWindow(QMainWindow):
    def __init__(self, database: OhtuDatabase, halder: BibTeXHandler):
        super().__init__()
        self.setWindowTitle("Ohtu")

        self.handler = halder
        self.database = database

        self.editbar = EditBar()
        _ = self.editbar.add_button.clicked.connect(self.on_add)
        self.viewbar = ViewBar()

        top_split = QHBoxLayout()
        top_split.addWidget(self.editbar)
        top_split.addWidget(self.viewbar)

        self.editor = SourceEditor()
        self.viewer = SourceViewer(self.database.get_references())
        _ = self.viewbar.search_input.textChanged.connect(self.viewer.filter_items)

        bottom_split = QHBoxLayout()
        bottom_split.addWidget(self.editor)
        bottom_split.addWidget(self.viewer)

        layout = QVBoxLayout()
        layout.addLayout(top_split)
        layout.addLayout(bottom_split)

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
        _ = export_action.triggered.connect(self.on_export)
        import_action = QAction("Import", self)
        about_action = QAction("About", self)

        file_menu.addAction(import_action)
        file_menu.addAction(export_action)

        help_menu.addAction(about_action)

    def refresh(self):
        self.viewer.refresh(self.database.get_references())

    def on_export(self):
        biptext: str = self.handler.create_bibtex_data(self.database.get_references())
        self.handler.save_to_file(biptext, "./test_biptext.bip")

    def on_add(self):
        print("add on painettu")
        tag = self.editor.tag_input.text().strip()
        author = self.editor.author_input.text().strip()
        title = self.editor.title_input.text().strip()
        journal = self.editor.journal_input.text().strip()
        doi = self.editor.doi_input.text().strip()

        if not author:
            QMessageBox.warning(self, "Virheilmoitus", "author is missing.")
            return
        if not title:
            QMessageBox.warning(self, "Virheilmoitus", "title is missing.")
            return
        if not tag:
            QMessageBox.warning(self, "Virheilmoitus", "tag is missing.")
            return

        year = self.editor.year_input.date().year()

        self.database.add_reference(
            tag,
            author,
            title,
            journal or None,
            year,
            doi or None,
        )

        self.editor.tag_input.clear()
        self.editor.author_input.clear()
        self.editor.title_input.clear()
        self.editor.journal_input.clear()
        self.editor.year_input.setDate(QDate.currentDate())
        self.editor.doi_input.clear()

        self.refresh()

@final
class EditBar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout();

        self.add_button = QPushButton("add")
        layout.addWidget(self.add_button)

        self.edit_button = QPushButton("edit")
        layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("delete")
        layout.addWidget(self.delete_button)

        self.uncheck_button = QPushButton("uncheck")
        layout.addWidget(self.uncheck_button)

        self.setLayout(layout)

@final
class ViewBar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout();

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

        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("tag - mandatory")
        self.tag_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tag_input.setStyleSheet("""
                QLineEdit {
                    placeholder-text-color: red;
                    } 
        """)
        layout.addWidget(self.tag_input)

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("author - mandatory")
        self.author_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.author_input.setStyleSheet("""
                QLineEdit {
                    placeholder-text-color: red;
                    } 
        """)
        layout.addWidget(self.author_input)
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("title - mandatory")
        self.title_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.title_input.setStyleSheet("""
                QLineEdit {
                    placeholder-text-color: red;
                    } 
        """)
        layout.addWidget(self.title_input)
        
        self.journal_input = QLineEdit()
        self.journal_input.setPlaceholderText("journal")
        self.journal_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.journal_input)
        
        self.year_input = QDateEdit(QDate.currentDate())
        self.year_input.setDisplayFormat("yyyy")
        self.year_input.setCalendarPopup(True)
        self.year_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.year_input)
        
        self.doi_input = QLineEdit()
        self.doi_input.setPlaceholderText("doi")
        self.doi_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.doi_input)

        self.setLayout(layout)

class SourceViewer(QListWidget):
    def __init__(self, references: list[dict[str, str | int | None]]):
        super().__init__()
        self.refresh(references)

    def refresh(self, references: list[dict[str, str | int | None]]):
        self.clear()
        for reference in references:
            self.addItem(Source(**reference))

    def filter_items(self, search_text: str):
        search_text = search_text.casefold()
        for index in range(self.count()):
            item = self.item(index)
            item.setHidden(search_text not in item.text().casefold())

@final
class Source(QListWidgetItem):
    """
    Source data model.
    TODO: tää omaksi tiedostoksi ja sinne kaikki bibtex kentät, alustavasti None. MVC-arkkitehtuuri?
    """
    def __init__(
        self,
        id: int,
        tag: str,
        author: str,
        title: str,
        journal: str | None,
        year: int | None,
        doi: str | None,
    ):
        details = [value for value in (author, journal, str(year) if year is not None else None) if value]
        super().__init__(f"{title} — {', '.join(details)}")
        # // Keep the database ID on each item for future selection and editing actions.
        self.id = id
        self.tag = tag
        self.author = author
        self.title = title
        self.journal = journal
        self.year = year
        self.doi = doi
