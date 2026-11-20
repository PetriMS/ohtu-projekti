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


class BibTeXHandler:
    """
    Luokka BibTeX-datan hallintaan
    """

    def __init__(self, io):
        self.io = io

    def create_bibtex_data(self, data: dict):
        """
        Muodostetaan BibTeX-sisältö datan perusteella.
        Datassa pitää olla vähintäänkin type ja key.
        """
        self.validate(data)

        type = data["type"]
        key = data["key"]

        content = ""
        for key in data:
            # Käsitellään kaikki kentät paitsi key ja lähteen type
            if key not in ["type", "key"]:
                content += f"    {key} = {{{data[key]}}},\n"

        return f"""@{type}{{{key}\n{content}}}"""

    def validate(self, data: dict):
        """
        Validoidaan data,
        esim. key:ssa ei saa olla välilyöntejä tms.
        """
        if " " in data["key"]:
            # TODO
            raise ValueError("Key sisältää välilyöntejä")

    def save_to_file(self, filepath: str, bibtex_data: str):
        """
        Tallennetaan BibTeX-muotoinen data tiedostoon.
        """
        self.io.write_file(bibtex_data, filepath)


# Testi kehitysympäristössä
if __name__ == "__main__":
    data = {
        "type": "book",
        "key": "kirja123",
        "author": "Einstein, A.",
        "title": "Kirja",
        "journal": "tiedelehti",
        "year": 2027,
    }

    io = IOHandler()
    handler = BibTeXHandler(io)
    bibtex = handler.create_bibtex_data(data)
    print(bibtex)
