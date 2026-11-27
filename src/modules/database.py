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
from typing import cast, final

RefRow = dict[str, str | int | None]

# Jos references ei ole olemassa, luo sen automaattisesti
# Muokataan tehdessä paremmaksi


@final
class OhtuDatabase:
    def __init__(self, database_path: str = "references.db"):
        self.conn = sqlite3.connect(database_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        # tietokannan luominen tms..

    def create_table(self):
        _ = self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS reference (
            id INTEGER PRIMARY KEY,
            reftype TEXT NOT NULL,
            tag TEXT UNIQUE NOT NULL,
            author TEXT NOT NULL,
            title TEXT NOT NULL,
            journal TEXT,
            year INTEGER,
            doi TEXT UNIQUE
        );
        """)

        _ = self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            category TEXT NOT NULL UNIQUE
        );
        """)

        _ = self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS reference_category (
            reference_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            PRIMARY KEY (reference_id, category_id),
            FOREIGN KEY (reference_id) REFERENCES reference(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
        );
        """)

        _ = self.cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_refcat_ref
            ON reference_category(reference_id);
            """)

        _ = self.cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_refcat_cat
            ON reference_category(category_id);
            """)

        self.conn.commit()

    # ?-merkit ovat sql-injektioita vastaan
    # IGNORE tarkoittaa, että ei lisätä olemassa olevaa

    def add_reference(self, reftype: str, tag: str, author: str, title: str, journal: str | None, year: int | None, doi: str | None):
        _ = self.cursor.execute("""
        INSERT OR IGNORE INTO reference (reftype, tag, author, title, journal, year, doi)
        VALUES (?, ?, ?, ?, ?, ?, ?);""",
                                (reftype, tag, author, title, journal, year, doi))
        self.conn.commit()


    def update_reference(self, source_id: int, reftype: str, tag: str, author: str, title: str, journal: str | None, year: int | None, doi: str | None):
        _ = self.cursor.execute("""
        UPDATE OR IGNORE reference
        SET reftype = ?, tag = ?, author = ?, title = ?, journal = ?, year = ?, doi = ?
        WHERE id = ?;""",
                                (reftype, tag, author, title, journal, year, doi, source_id))
        self.conn.commit()

    def get_references(self) -> list[RefRow]:
        _ = self.cursor.execute("SELECT * FROM reference")
        data: list[sqlite3.Row] = self.cursor.fetchall()
        # Convert to a list of dicts
        return [dict(row) for row in data]

    def delete_reference(self, reference_id: int) -> None:
        _ = self.cursor.execute("DELETE FROM reference WHERE id = ?", (reference_id,))
        self.conn.commit()

    def add_category(self, category: str):
        _ = self.cursor.execute(
            """
            INSERT OR IGNORE INTO categories (category)
            VALUES (?);
            """,
            (category,)
        )
        self.conn.commit()

    def add_category_to_reference(self, reference_id: int, category_id: int):
        _ = self.cursor.execute(
            """
            INSERT OR IGNORE INTO reference_category (reference_id, category_id)
            VALUES (?, ?);
            """,
            (reference_id, category_id)
        )
        self.conn.commit()

    def get_categories(self) -> list[RefRow]:
        _ = self.cursor.execute("SELECT * FROM categories")
        data: list[sqlite3.Row] = self.cursor.fetchall()
        return [dict(row) for row in data]

    def get_references_by_category(self, category_id: int) -> list[RefRow]:
        _ = self.cursor.execute(
            """
            SELECT r.*
            FROM reference r
            JOIN reference_category rc
                ON r.id = rc.reference_id
            WHERE rc.category_id = ?;
            """,
            (category_id,)
        )
        data: list[sqlite3.Row] = self.cursor.fetchall()
        return [dict(row) for row in data]

    def get_references_by_category_name(self, category: str) -> list[RefRow]:
        _ = self.cursor.execute(
            """
            SELECT r.*
            FROM reference r
            JOIN reference_category rc
                ON r.id = rc.reference_id
            JOIN categories c
                ON c.id = rc.category_id
            WHERE c.category = ?;
            """,
            (category,)
        )
        data: list[sqlite3.Row] = self.cursor.fetchall()
        return [dict(row) for row in data]

    def get_categories_for_reference(self, reference_id: int) -> list[RefRow]:
        _ = self.cursor.execute(
            """
            SELECT c.*
            FROM categories c
            JOIN reference_category rc
                ON c.id = rc.category_id
            WHERE rc.reference_id = ?;
            """,
            (reference_id,)
        )
        data: list[sqlite3.Row] = self.cursor.fetchall()
        return [dict(row) for row in data]


def init_database() -> None:
    # // Create the database table and add example references.
    db = OhtuDatabase()
    db.create_table()
    db.add_reference(
        reftype="book",
        tag="bell",
        author="Bell, J. S.",
        title="On the Einstein Podolsky Rosen Paradox",
        journal="Physics Physique Fizika",
        year=1964,
        doi="10.1103/PhysicsPhysiqueFizika.1.195",
    )

    db.add_reference(
        reftype="book",
        tag="shannon",
        author="Shannon, C. E.",
        title="A Mathematical Theory of Communication",
        journal="The Bell System Technical Journal",
        year=1948,
        doi="10.1002/j.1538-7305.1948.tb01338.x",
    )
    print("Database initialized with example references.")

# Kommentoikaa pois, näin testausta varten
# """
if __name__ == "__main__":
    db = OhtuDatabase()
    db.create_table()
    db.add_reference(
        reftype="book",
        tag="bell",
        author="Bell, J. S.",
        title="On the Einstein Podolsky Rosen Paradox",
        journal="Physics Physique Fizika",
        year=1964,
        doi="10.1103/PhysicsPhysiqueFizika.1.195"
    )

    db.add_reference(
        reftype="book",
        tag="shannon",
        author="Shannon, C. E.",
        title="A Mathematical Theory of Communication",
        journal="The Bell System Technical Journal",
        year=1948,
        doi="10.1002/j.1538-7305.1948.tb01338.x"
    )

    db.add_category("AI")
    db.add_category("Quantum Mechanics")
    db.add_category_to_reference(1, 1)
    db.add_category_to_reference(2, 1)
    db.add_category_to_reference(1, 2)

    references = db.get_references()
    for reference in references:
        print(reference)

    print("Categories:")
    categories = db.get_categories()
    for category in categories:
        print(category)

    for category in db.get_categories():
        print(f"\nArticles linked to category {category['category']}:")

        references = db.get_references_by_category(cast(int, category["id"]))

        for reference in references:
            print(reference)

    for reference in db.get_references():

        print(f"\nCategories linked to reference {reference['title']}:")

        for category in db.get_categories_for_reference(cast(int, reference["id"])):
            print(category["category"])
# """
