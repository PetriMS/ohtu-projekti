from PyQt6.QtWidgets import (QTreeWidgetItem)
from typing import final

@final
class Source(QTreeWidgetItem):
    """
    Source data model.
    TODO: tää omaksi tiedostoksi ja sinne kaikki bibtex kentät, alustavasti None. MVC-arkkitehtuuri?
    """
    def __init__(
        self,
        id: int,
        reftype: str,
        tag: str,
        author: str,
        title: str,
        journal: str | None,
        year: int | None,
        doi: str | None,
    ) -> None:
        super().__init__([
            title,
            author,
            journal or "",
            "" if year is None else str(year),
        ])
        # // Keep the database ID on each item for future selection and editing actions.
        self.id = id
        self.reftype = reftype
        self.tag = tag
        self.author = author
        self.title = title
        self.journal = journal
        self.year = year
        self.doi = doi

        self.search_text = " ".join(
            str(value) for value in (title, author, journal, year, doi)
            if value not in (None, "")
        ).casefold()
