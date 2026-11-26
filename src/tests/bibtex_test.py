import unittest
from modules.bibtex import BibTeXHandler
from modules.io_handler import IOHandler


class TestBibTeX(unittest.TestCase):
    def setUp(self):
        pass

    def test_bibtex_data_creation(self):
        data = [{'id': 1, 'reftype': 'book', 'tag': 'bell', 'author': 'Bell, J. S.', 'title': 'On the Einstein Podolsky Rosen Paradox', 'journal': 'Physics Physique Fizika', 'year': 1964, 'doi': '10.1103/PhysicsPhysiqueFizika.1.195'},
                {'id': 2, 'reftype': 'book', 'tag': 'shannon', 'author': 'Shannon, C. E.', 'title': 'A Mathematical Theory of Communication', 'journal': 'The Bell System Technical Journal', 'year': 1948, 'doi': '10.1002/j.1538-7305.1948.tb01338.x'}]

        io = IOHandler()
        handler = BibTeXHandler(io)
        bibtex = handler.create_bibtex_data(data)
        self.assertIn(data[0]['title'], bibtex)
        self.assertIn(data[1]['title'], bibtex)
