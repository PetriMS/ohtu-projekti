import pytest

from modules.database import OhtuDatabase, init_database


@pytest.fixture
def database():
    db = OhtuDatabase(":memory:")
    db.create_table()
    yield db
    db.conn.close()


def add_reference(db, **overrides):
    values = {
        "reftype": "book",
        "tag": "test-key",
        "author": "Test Author",
        "title": "Test Title",
        "journal": "Test Journal",
        "year": 2024,
        "doi": "10.1234/test",
    }
    values.update(overrides)
    db.add_reference(**values)


def test_create_table_is_idempotent(database):
    database.create_table()
    database.create_table()

    assert database.get_references() == []


def test_add_and_get_reference(database):
    add_reference(database)

    [reference] = database.get_references()
    assert reference["reftype"] == "book"
    assert reference["tag"] == "test-key"
    assert reference["author"] == "Test Author"
    assert reference["title"] == "Test Title"
    assert reference["journal"] == "Test Journal"
    assert reference["year"] == 2024
    assert reference["doi"] == "10.1234/test"


def test_add_reference_accepts_optional_fields_as_none(database):
    add_reference(database, journal=None, year=None, doi=None)

    [reference] = database.get_references()
    assert reference["journal"] is None
    assert reference["year"] is None
    assert reference["doi"] is None


def test_add_reference_ignores_duplicate_doi(database):
    add_reference(database)
    add_reference(database, tag="second", title="Second Title")

    references = database.get_references()
    assert len(references) == 1
    assert references[0]["title"] == "Test Title"


def test_add_reference_treats_sql_like_text_as_data(database):
    unsafe_title = "Title'); DROP TABLE reference;--"
    add_reference(database, title=unsafe_title)

    [reference] = database.get_references()
    assert reference["title"] == unsafe_title


def test_update_reference_changes_all_editable_fields(database):
    add_reference(database)
    reference_id = database.get_references()[0]["id"]

    database.update_reference(
        reference_id,
        reftype="article",
        tag="updated-key",
        author="Updated Author",
        title="Updated Title",
        journal=None,
        year=2025,
        doi="10.1234/updated",
    )

    [reference] = database.get_references()
    assert reference == {
        "id": reference_id,
        "reftype": "article",
        "tag": "updated-key",
        "author": "Updated Author",
        "title": "Updated Title",
        "journal": None,
        "year": 2025,
        "doi": "10.1234/updated",
    }


def test_update_nonexistent_reference_changes_nothing(database):
    add_reference(database)
    before = database.get_references()

    database.update_reference(999, "book", "key", "Author", "Title", None, None, None)

    assert database.get_references() == before


def test_update_with_duplicate_doi_is_ignored(database):
    add_reference(database)
    add_reference(database, tag="second", title="Second Title", doi="10.1234/second")
    second_id = database.get_references()[1]["id"]

    database.update_reference(
        second_id, "book", "second", "Author", "Updated", None, None, "10.1234/test"
    )

    second = next(row for row in database.get_references() if row["id"] == second_id)
    assert second["title"] == "Second Title"
    assert second["doi"] == "10.1234/second"


def test_delete_reference_removes_only_matching_record(database):
    add_reference(database)
    add_reference(database, tag="second", doi="10.1234/second")
    references = database.get_references()
    deleted_id = references[0]["id"]
    remaining_id = references[1]["id"]

    database.delete_reference(deleted_id)

    assert [row["id"] for row in database.get_references()] == [remaining_id]


def test_delete_nonexistent_reference_changes_nothing(database):
    add_reference(database)
    before = database.get_references()

    database.delete_reference(999)

    assert database.get_references() == before


def test_init_database_creates_example_references(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    init_database()
    seeded_database = OhtuDatabase()
    try:
        references = seeded_database.get_references()
    finally:
        seeded_database.conn.close()

    assert {reference["tag"] for reference in references} == {"bell", "shannon"}
