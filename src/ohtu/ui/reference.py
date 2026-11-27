from typing import final

# Dynamic attrs
# pylint: disable=no-member

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
        for key, value in entry.items():
            setattr(self, key, value)

    
            
        

if __name__ == "__main__":
    r = Reference({'id': 1, 'reftype': 'book', 'tag': 'bell', 'author': 'Bell, J. S.', 'title': 'On the Einstein Podolsky Rosen Paradox', 'journal': 'Physics Physique Fizika', 'year': 1964, 'doi': '10.1103/PhysicsPhysiqueFizika.1.195'})
    print(r.data)