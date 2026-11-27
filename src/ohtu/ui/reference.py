from typing import cast, final


@final
class Reference():
    """
    Reference (citation) data model.
    """

    id: int
    reftype: str
    tag: str
    author: str
    title: str
    journal: str | None
    year: int | str | None
    doi: str | None


    def __init__(self, entry: dict[str, str | int | None]):
        self.id = cast(int, entry["id"])
        self.reftype = cast(str, entry["reftype"])
        self.tag = cast(str, entry["tag"])
        self.author = cast(str, entry["author"])
        self.title = cast(str, entry["title"])
        self.journal = cast(str | None, entry.get("journal"))
        self.year = entry.get("year")
        self.doi = cast(str | None, entry.get("doi"))


if __name__ == "__main__":
    r = Reference({'id': 1, 'reftype': 'book', 'tag': 'bell', 'author': 'Bell, J. S.', 'title': 'On the Einstein Podolsky Rosen Paradox', 'journal': 'Physics Physique Fizika', 'year': 1964, 'doi': '10.1103/PhysicsPhysiqueFizika.1.195'})
    print(r.title)
