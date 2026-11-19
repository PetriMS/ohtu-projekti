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


def luo_bibtex_data(data):
    """
    Muodostetaan BibTeX-sisältö datan perusteella.
    Datassa pitää olla vähintäänkin tyyppi ja tunnus.
    """
    validoi(data)

    tyyppi = data["tyyppi"]
    tunnus = data["tunnus"]

    content = ""
    for key in data:
        # Käsitellään kaikki kentät paitsi tunnus ja lähteen tyyppi
        if key not in ["tyyppi", "tunnus"]:
            content += f"    {key} = {{{data[key]}}},\n"

    return f"""@{tyyppi}{{{tunnus}\n{content}}}"""


def validoi(data):
    """
    Validoidaan data,
    esim. tunnuksessa ei saa olla välilyöntejä tms.
    """
    if " " in data["tunnus"]:
        # TODO
        raise ValueError("Tunnus sisältää välilyöntejä")

    pass


def tallenna_tiedostoon(bibtex_data):
    pass


# Testi kehitysympäristössä
if __name__ == "__main__":
    data = {
        "tyyppi": "book",
        "tunnus": "kirja123",
        "author": "Einstein, A.",
        "title": "Kirja",
        "journal": "tiedelehti",
        "year": 2027,
    }

    bibtex = luo_bibtex_data(data)
    print(bibtex)
