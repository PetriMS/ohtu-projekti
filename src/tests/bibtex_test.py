from unittest.mock import Mock

import pytest

from modules.bibtex import BibTeXHandler
from modules.io_handler import IOHandler


@pytest.fixture
def handler():
    return BibTeXHandler(IOHandler())


def test_create_bibtex_data_formats_one_entry(handler):
    entry = {
        "id": 7,
        "reftype": "book",
        "tag": "sample-key",
        "author": "Example Author",
        "title": "Example Title",
    }

    result = handler.create_bibtex_data([entry])

    assert result == (
        "@book{7\n"
        "    reftype = {book},\n"
        "    tag = {sample-key},\n"
        "    author = {Example Author},\n"
        "    title = {Example Title},\n"
        "}\n"
    )


def test_create_bibtex_data_formats_multiple_entries(handler):
    entries = [
        {"id": 1, "reftype": "book", "title": "First"},
        {"id": 2, "reftype": "article", "title": "Second"},
    ]

    result = handler.create_bibtex_data(entries)

    assert "@book{1" in result
    assert "@article{2" in result
    assert "title = {First}" in result
    assert "title = {Second}" in result


def test_create_bibtex_data_with_no_entries_returns_empty_text(handler):
    assert handler.create_bibtex_data([]) == ""


def test_save_to_file_delegates_to_io_handler():
    io_handler = Mock(spec=IOHandler)
    handler = BibTeXHandler(io_handler)

    handler.save_to_file("@book{1}", "references.bib")

    io_handler.write_file.assert_called_once_with("@book{1}", "references.bib")


def test_validate_accepts_key_without_spaces(handler):
    handler.validate({"key": "valid-key_1"})


def test_validate_rejects_key_with_spaces(handler):
    with pytest.raises(ValueError, match="Key sisältää välilyöntejä"):
        handler.validate({"key": "invalid key"})
