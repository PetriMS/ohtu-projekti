import unittest
from modules.bibtex import BibTeXHandler
from modules.io_handler import IOHandler

class TestBibTeX(unittest.TestCase):
    def setUp(self):
        pass

    def test_luodaan_bibtex_data(self):
        data = {
            "type": "book",
            "key": "science_book_123",
            "author": ["Einstein, A"],
            "title": "Can Quantum-Mechanical Description of Physical Reality Be Considered Complete?",
            "year": 1935,
        }

        io = IOHandler()
        handler = BibTeXHandler(io)
        bibtex = handler.create_bibtex_data(data)
        self.assertIn(data["title"], bibtex)