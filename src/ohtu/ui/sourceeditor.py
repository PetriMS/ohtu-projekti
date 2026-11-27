from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QDateEdit)
from PyQt6.QtCore import (Qt, QDate)

from ohtu.ui.source import Source

from datetime import date
from typing import  final

@final
class SourceEditor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # Id of the source being edited. None means the editor is creating a new source.
        self.id: int | None = None

        layout = QVBoxLayout();

        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.reftype_input = QLineEdit()
        self.reftype_input.setPlaceholderText("reftype - mandatory")
        self.reftype_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.reftype_input.setStyleSheet("""
                QLineEdit {
                    placeholder-text-color: red;
                    } 
        """)
        layout.addWidget(self.reftype_input)

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
        
        self.year_input = QDateEdit(QDate(date.today().year, 1, 1))
        self.year_input.setDisplayFormat("yyyy")
        self.year_input.setCalendarPopup(True)
        self.year_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.year_input)
        
        self.doi_input = QLineEdit()
        self.doi_input.setPlaceholderText("doi")
        self.doi_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.doi_input)
        
        self.categories_input = QLineEdit()
        self.categories_input.setPlaceholderText('categories, separate by ","')
        self.categories_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.categories_input)

        self.setLayout(layout)


    def load_source(self, source: Source) -> None:
        """Fill the editor from a source and switch to edit mode."""
        self.id = source.id
        self.reftype_input.setText(source.reftype)
        self.tag_input.setText(source.tag)
        self.author_input.setText(source.author)
        self.title_input.setText(source.title)
        self.journal_input.setText(source.journal or "")
        # QDateEdit can't be empty, so a source without a year falls back to the current year
        self.year_input.setDate(QDate(source.year, 1, 1) if source.year is not None else QDate(date.today().year, 1, 1))
        self.doi_input.setText(source.doi or "")
        self.categories_input.clear()  # categories aren't stored on Source yet

    def clear(self) -> None:
        """Empty the editor and switch back to add mode."""
        self.id = None
        self.reftype_input.clear()
        self.tag_input.clear()
        self.author_input.clear()
        self.title_input.clear()
        self.journal_input.clear()
        self.year_input.setDate(QDate(date.today().year, 1, 1))
        self.doi_input.clear()
        self.categories_input.clear()
