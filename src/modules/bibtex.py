"""
BibTeX-dataan ja tiedostoihin liittyvät funktiot tänne?

Esimerkki dataa:
@article{einstein1935can,
  author  = {Einstein, A. and Podolsky, B. and Rosen, N.},
  title   = {Can Quantum-Mechanical Description of Physical Reality Be Considered Complete?},
  journal = {Physical Review},
  year    = {1935},
  doi     = {10.1103/PhysRev.47.777}
}
"""
# Alun artikkeli vielä vaiheessa, voi miettiä parempaa toteutusta myöhemmin
# Muokataan loppuun valmiiksi, kun tiedetään miten ja mitä dataa saadaan


from modules.io_handler import IOHandler
from typing import final


@final
class BibTeXHandler:
    """
    Luokka BibTeX-datan hallintaan
    """

    def __init__(self, io: IOHandler):
        self.io = io

    def create_bibtex_data(self, entries: list[dict]):
        """
        Create BibTeX data from database entries (rows)
        """

        # self.validate(data) # TODO: DOESNT WORK

        output = ""

        # DB keys
        keys = ["id", "author", "title", "journal", "year", "doi"]

        for entry in entries:
            type = "book"
            id = entry['id']

            content = ""
            for key, value in entry.items():
                if key not in ["id"]:
                    content += f"    {key} = {{{value}}},\n"

            output += f"""@{type}{{{id}\n{content}}}\n"""

        return output

    def validate(self, data: dict):
        """
        TODO TODO TODO
        Validoidaan data,
        esim. key:ssa ei saa olla välilyöntejä tms.
        """
        if " " in data["key"]:
            # TODO
            raise ValueError("Key sisältää välilyöntejä")

    def save_to_file(self, bibtex_data: str, filepath: str):
        """
        Saves the data to a file.
        """
        self.io.write_file(bibtex_data, filepath)


# Testi kehitysympäristössä
if __name__ == "__main__":
    data = [{'id': 1, 'author': 'Bell, J. S.', 'title': 'On the Einstein Podolsky Rosen Paradox', 'journal': 'Physics Physique Fizika', 'year': 1964, 'doi': '10.1103/PhysicsPhysiqueFizika.1.195'},
            {'id': 2, 'author': 'Shannon, C. E.', 'title': 'A Mathematical Theory of Communication', 'journal': 'The Bell System Technical Journal', 'year': 1948, 'doi': '10.1002/j.1538-7305.1948.tb01338.x'}]

    from modules.database import OhtuDatabase
    db = OhtuDatabase()
    io = IOHandler()
    handler = BibTeXHandler(io)

    viittaukset = db.get_references()
    print(viittaukset)
    print()

    bibtex = handler.create_bibtex_data(viittaukset)
    io.console_print(bibtex)
