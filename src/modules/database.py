"""
Tänne tietokantaan liittyvät asiat?

Esimerkki dataa:
@article{einstein1935can,
  author  = {Einstein, A. and Podolsky, B. and Rosen, N.},
  title   = {Can Quantum-Mechanical Description of Physical Reality Be Considered Complete?},
  journal = {Physical Review},
  year    = {1935},
  doi     = {10.1103/PhysRev.47.777}
}
"""

import sqlite3

# Suoraan tekoälyltä kysyttynä, jos references ei ole olemassa, luo sen 
# automaattisesti
# Muokataan tehdessä paremmaksi
class OhtuDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("references.db")
        self.cursor = self.conn.cursor()
        # tietokannan luominen tms..
        
    def luo_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS reference (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            title TEXT NOT NULL,
            journal TEXT,
            year INTEGER,
            doi TEXT UNIQUE
        )
        """)
        self.conn.commit()
    
    # ?-merkit ovat sql-injektioita vastaan
    
    def lisaaViittaus(self, author, title, journal, year, doi):
        self.cursor.execute("""
        INSERT INTO reference (author, title, journal, year, doi) 
        VALUES (?, ?, ?, ?, ?)""",
        (author, title, journal, year, doi))
        self.conn.commit()
        

    def haeViittaus(self):
        self.cursor.execute("SELECT * FROM reference")
        return self.cursor.fetchall()
        