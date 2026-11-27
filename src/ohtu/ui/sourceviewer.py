from PyQt6.QtWidgets import (QTreeWidget)
from typing import final

from ohtu.ui.source import Source

@final
class SourceViewer(QTreeWidget):
    def __init__(self, references: list[dict[str, str | int | None]]) -> None:
        super().__init__()
        self.setColumnCount(4)
        self.setHeaderLabels(["Title", "Author", "Journal", "Year"])
        self.setRootIsDecorated(False)
        self.refresh(references)

    def refresh(self, references: list[dict[str, str | int | None]]) -> None:
        self.clear()
        for reference in references:
            self.addTopLevelItem(Source(reference))

    def filter_items(self, search_text: str) -> None:
        search_text = search_text.casefold()
        for index in range(self.topLevelItemCount()):
            item = self.topLevelItem(index)
            if isinstance(item, Source):
                item.setHidden(search_text not in item.search_text)
