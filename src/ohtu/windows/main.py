from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTreeWidgetItem)
from PyQt6.QtGui import QAction

from typing import final

from modules.database import OhtuDatabase
from modules.bibtex import BibTeXHandler 

from ohtu.ui.source import Source
from ohtu.ui.editbar import EditBar 
from ohtu.ui.viewbar import ViewBar 
from ohtu.ui.sourceeditor import SourceEditor 
from ohtu.ui.sourceviewer import SourceViewer 

@final
class MainWindow(QMainWindow):
    def __init__(self, database: OhtuDatabase, halder: BibTeXHandler) -> None:
        super().__init__()
        self.setWindowTitle("Ohtu")

        self.handler = halder
        self.database = database

        self.editbar = EditBar()

        _ = self.editbar.add_button.clicked.connect(self.on_add)
        _ = self.editbar.delete_button.clicked.connect(self.on_delete)
        _ = self.editbar.save_button.clicked.connect(self.on_save)
        _ = self.editbar.uncheck_button.clicked.connect(self.on_uncheck)
        self.viewbar = ViewBar()

        top_split = QHBoxLayout()
        top_split.addWidget(self.editbar)
        top_split.addWidget(self.viewbar)

        self.editor = SourceEditor()
        self.viewer = SourceViewer(self.database.get_references())
        _ = self.viewer.currentItemChanged.connect(self.on_selection_changed)
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
        
    def create_menu(self) -> None:
        menu_bar = self.menuBar()
        assert menu_bar is not None

        file_menu = menu_bar.addMenu("File")
        help_menu = menu_bar.addMenu("Help")
        assert file_menu is not None
        assert help_menu is not None

        export_action = QAction("Export", self)
        _ = export_action.triggered.connect(self.on_export)
        import_action = QAction("Import", self)
        about_action = QAction("About", self)

        file_menu.addAction(import_action)
        file_menu.addAction(export_action)

        help_menu.addAction(about_action)

    def refresh(self) -> None:
        self.viewer.refresh(self.database.get_references())

    def on_export(self) -> None:
        bibtext: str = self.handler.create_bibtex_data(self.database.get_references())
        self.handler.save_to_file(bibtext, "./test_bibtext.bib")

    def on_add(self) -> None:
        reftype = "book"
        tag = self.editor.tag_input.text().strip()
        author = self.editor.author_input.text().strip()
        title = self.editor.title_input.text().strip()
        journal = self.editor.journal_input.text().strip()
        doi = self.editor.doi_input.text().strip()
        year = self.editor.year_input.date().year()

        if not author:
            _ = QMessageBox.warning(self, "Virheilmoitus", "author is missing.")
            return
        if not title:
            _ = QMessageBox.warning(self, "Virheilmoitus", "title is missing.")
            return
        if not tag:
            _ = QMessageBox.warning(self, "Virheilmoitus", "tag is missing.")
            return

        self.database.add_reference(
            reftype=reftype,
            tag=tag,
            author=author,
            title=title,
            journal=journal or None,
            year=year,
            doi=doi or None,
        )

        self.editor.clear()
        self.refresh()

    def on_save(self) -> None:
        # reftype = self.editor.reftype_input.text().strip()
        reftype = "book"
        tag = self.editor.tag_input.text().strip()
        author = self.editor.author_input.text().strip()
        title = self.editor.title_input.text().strip()
        journal = self.editor.journal_input.text().strip()
        doi = self.editor.doi_input.text().strip()
        year = self.editor.year_input.date().year()

        if not author:
            _ = QMessageBox.warning(self, "Virheilmoitus", "author is missing.")
            return
        if not title:
            _ = QMessageBox.warning(self, "Virheilmoitus", "title is missing.")
            return
        if not tag:
            _ = QMessageBox.warning(self, "Virheilmoitus", "tag is missing.")
            return


        if (self.editor.id == None):
            # add a panic UI has bug!
            raise Exception("The id wasn't set we have a bug!");

        self.database.update_reference(
            source_id=self.editor.id,
            reftype=reftype,
            tag=tag,
            author=author,
            title=title,
            journal=journal or None,
            year=year,
            doi=doi or None,
        )

        self.editor.clear()
        self.refresh()

    def on_delete(self) -> None:
        source = self.viewer.currentItem()
        if not isinstance(source, Source):
            return

        answer = QMessageBox.question(
            self,
            "Confirm deletion",
            f"Delete '{source.title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        self.database.delete_reference(source.id)
        self.refresh()
        self.viewer.filter_items(self.viewbar.search_input.text())

    def on_uncheck(self) -> None:
        self.viewer.setCurrentItem(None) 

    def on_selection_changed(self, current: QTreeWidgetItem | None, _previous: QTreeWidgetItem | None) -> None:
        if isinstance(current, Source):
            self.editor.load_source(current)
            self.editbar.selection()
        else:
            self.editor.clear()
            self.editbar.no_selection()


