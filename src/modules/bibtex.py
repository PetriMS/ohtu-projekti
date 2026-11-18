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
    
    return f"@article{{{tunnus}, {author}, {title}, {journal}, {year}, {doi}}}"

def tallenna_tiedostoon(bibtex_data):
    pass