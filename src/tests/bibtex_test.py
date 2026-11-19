import unittest
from modules.bibtex import *

class TestBibTeX(unittest.TestCase):
    def setUp(self):
        pass

    def test_luodaan_bibtex_data(self):
        data = {
            "tyyppi": "book",
            "tunnus": "science_book_123",
            "author": ["Einstein, A"],
            "title": "Can Quantum-Mechanical Description of Physical Reality Be Considered Complete?",
            "year": 1935,
        }
        bibtex = luo_bibtex_data(data)
        self.assertIn(data["title"], bibtex)