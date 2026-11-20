from PyQt6.QtWidgets import QApplication

from ohtu.windows.main import MainWindow

from modules.database import OhtuDatabase
from modules.bibtex import BibTeXHandler 
from modules.io_handler import IOHandler 

def main() -> None:
    app = QApplication([])

    database = OhtuDatabase()
    database.create_table()

    handler = BibTeXHandler(IOHandler())
    _ = MainWindow(database, handler)

    _ = app.exec()


if __name__ == "__main__":
    main()
