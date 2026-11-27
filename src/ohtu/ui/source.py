from PyQt6.QtWidgets import (QTreeWidgetItem)
from ohtu.ui.reference import Reference
from typing import final

@final
class Source(QTreeWidgetItem):
    """
    Source data model. Entry tulee hakemalla databasesta.
    Kentät löytyy self.referencesta.
    """

    def __init__(self, entry: dict[str, str | int | None]) -> None:
        self.reference = Reference(entry)
        super().__init__([
            self.reference.title,
            self.reference.author,
            self.reference.journal or "",
            "" if self.reference.year is None else str(self.reference.year),
        ])

        self.search_text = " ".join(
            str(value) for value in (self.reference.title, self.reference.author, self.reference.journal, self.reference.year, self.reference.doi)
            if value not in (None, "")
        ).casefold()


    def __getattr__ (self, name):
        return self.reference.__getattribute__(name)

