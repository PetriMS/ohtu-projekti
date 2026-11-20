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
from typing import final

# Jos references ei ole olemassa, luo sen automaattisesti
# Muokataan tehdessä paremmaksi
@final
class OhtuDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("references.db")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        # tietokannan luominen tms..
        
    def create_table(self):
        _ = self.cursor.execute("""
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
    # IGNORE tarkoittaa, että ei lisätä olemassa olevaa
    
    def add_reference(self, author: str, title: str, journal: str | None, year: int | None, doi: str | None):
        _ = self.cursor.execute("""
        INSERT OR IGNORE INTO reference (author, title, journal, year, doi)
        VALUES (?, ?, ?, ?, ?)""",
        (author, title, journal, year, doi))
        self.conn.commit()

    def get_references(self) -> list[dict[str, str | int | None]]:
        _ = self.cursor.execute("SELECT * FROM reference")
        data: list[sqlite3.Row] = self.cursor.fetchall()
        # Convert to a list of dicts
        return [dict(row) for row in data]


def init_database() -> None:
    # // Create the database table and add example references.
    db = OhtuDatabase()
    db.create_table()
    db.add_reference(
        "Bell, J. S.",
        "On the Einstein Podolsky Rosen Paradox",
        "Physics Physique Fizika",
        1964,
        "10.1103/PhysicsPhysiqueFizika.1.195",
    )
    db.add_reference(
        "Shannon, C. E.",
        "A Mathematical Theory of Communication",
        "The Bell System Technical Journal",
        1948,
        "10.1002/j.1538-7305.1948.tb01338.x",
    )
    print("Database initialized with example references.")

# Kommentoikaa pois, näin testausta varten
# """
if __name__ == "__main__":
    db = OhtuDatabase()
    db.create_table()
    db.add_reference(
    "Bell, J. S.",
    "On the Einstein Podolsky Rosen Paradox",
    "Physics Physique Fizika",
    1964,
    "10.1103/PhysicsPhysiqueFizika.1.195"
    )

    db.add_reference(
    "Shannon, C. E.",
    "A Mathematical Theory of Communication",
    "The Bell System Technical Journal",
    1948,
    "10.1002/j.1538-7305.1948.tb01338.x"
    )
    references = db.get_references()
    for reference in references:
        print(reference)

#"""
