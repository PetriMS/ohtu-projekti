from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QPushButton)
from PyQt6.QtCore import Qt

from typing import final

@final
class EditBar(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QHBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.add_button = QPushButton("add")
        self.edit_button = QPushButton("edit")
        self.delete_button = QPushButton("delete")
        self.uncheck_button = QPushButton("uncheck")
        self.save_button = QPushButton("save")
        self.new_button = QPushButton("new")
        self.clear_button = QPushButton("clear")

        self.setLayout(self._layout)

        self._all_buttons: list[QPushButton] = [
            self.add_button, self.edit_button, self.delete_button,
            self.uncheck_button, self.save_button, self.new_button,
            self.clear_button,
        ]

        self.no_selection()

    def show_only(self, *buttons: QPushButton) -> None:
        for button in self._all_buttons:
            self._layout.removeWidget(button)
            button.hide()

        for button in buttons:
            self._layout.addWidget(button)
            button.show()

    def no_selection(self) -> None:
        self.show_only(self.add_button, self.clear_button)

    def selection(self) -> None:
        self.show_only(self.save_button, self.delete_button, self.new_button, self.uncheck_button)

    def remove_all_buttons(self) -> None:
        self.show_only()

