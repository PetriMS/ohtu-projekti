import pytest

from modules.io_handler import IOHandler


def test_write_and_read_file_round_trip(tmp_path):
    handler = IOHandler()
    path = tmp_path / "nested" / "reference.bib"
    path.parent.mkdir()

    handler.write_file("A title with ääkköset", str(path))

    assert handler.read_file(str(path)) == "A title with ääkköset"


def test_write_file_replaces_existing_content(tmp_path):
    handler = IOHandler()
    path = tmp_path / "reference.bib"
    path.write_text("old content")

    handler.write_file("new content", str(path))

    assert path.read_text() == "new content"


def test_read_missing_file_raises_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        IOHandler().read_file(str(tmp_path / "missing.bib"))


def test_console_read_input_returns_user_text(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: f"reply to {prompt}")

    result = IOHandler().console_read_input("Name: ")

    assert result == "reply to Name: "


def test_console_print_writes_text(capsys):
    IOHandler().console_print("Hello")

    assert capsys.readouterr().out == "Hello\n"
