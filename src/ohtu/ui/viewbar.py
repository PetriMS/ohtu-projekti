from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QLineEdit)
from typing import final

@final
class ViewBar(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout();

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("search")
        layout.addWidget(self.search_input)

        self.setLayout(layout)

