from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMessageBox

from modules.bibtex import BibTeXHandler
from modules.database import OhtuDatabase
from modules.io_handler import IOHandler
from ohtu.windows.main import MainWindow


class robot_library:
    ROBOT_LIBRARY_SCOPE = "SUITE"

    def __init__(self):
        self.app = QApplication.instance() or QApplication([])
        self.database = OhtuDatabase(":memory:")
        self.database.create_table()
        self.window = MainWindow(self.database, BibTeXHandler(IOHandler()))
        self.app.processEvents()

    def stop_application(self):
        self.window.close()
        self.database.conn.close()

    def clear_references(self):
        _ = self.database.cursor.execute("DELETE FROM reference")
        self.database.conn.commit()
        self.window.refresh()

    def add_book(self, tag, author, title):
        self.window.editor.tag_input.setText(tag)
        self.window.editor.author_input.setText(author)
        self.window.editor.title_input.setText(title)
        self.window.editor.year_input.setDate(QDate(2024, 1, 1))
        self.window.editor.doi_input.setText(f"{tag}.example")
        self.window.editbar.add_button.click()
        self.app.processEvents()

    def book_should_be_stored_and_visible(self, tag, title):
        stored = any(book["tag"] == tag for book in self.database.get_references())
        visible = any(
            self.window.viewer.topLevelItem(index).title == title
            for index in range(self.window.viewer.topLevelItemCount())
        )
        if not stored or not visible:
            raise AssertionError(f"Book '{title}' was not saved and shown in the list.")

    def select_book(self, tag):
        for index in range(self.window.viewer.topLevelItemCount()):
            source = self.window.viewer.topLevelItem(index)
            if source.tag == tag:
                self.window.viewer.setCurrentItem(source)
                self.app.processEvents()
                return
        raise AssertionError(f"Book with tag '{tag}' is not in the list.")

    def delete_selected_book(self):
        QTimer.singleShot(0, self._confirm_deletion)
        self.window.editbar.delete_button.click()
        self.app.processEvents()

    def book_should_be_deleted(self, tag):
        stored = any(book["tag"] == tag for book in self.database.get_references())
        visible = any(
            self.window.viewer.topLevelItem(index).tag == tag
            for index in range(self.window.viewer.topLevelItemCount())
        )
        if stored or visible:
            raise AssertionError(f"Book with tag '{tag}' was not deleted.")

    def _confirm_deletion(self):
        dialog = QApplication.activeModalWidget()
        if isinstance(dialog, QMessageBox):
            dialog.button(QMessageBox.StandardButton.Yes).click()
