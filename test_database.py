import pytest
import sqlite3
from database import Database

@pytest.fixture
def db():
    db = Database("hh_bd.db")
    db.create_table()
    return db

def test_create_table(db):
    db.create_table()
    with sqlite3.connect(db.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vacancies'")
        table_exists = cursor.fetchone()
    assert table_exists is not None

def test_insert_vacancies(db):
    vacancies = [
        ("1", "Python Developer", "http://example.com", "Company", "Moscow", 100000, 150000, "RUB"),
        ("2", "Java Developer", "http://example.com", "Company", "Moscow", 120000, 180000, "RUB"),
    ]
    db.insert_vacancies(vacancies)
    result = db.get_filtered_vacancies("", None)
    assert len(result) == 2

def test_clear_vacancies(db):
    vacancies = [("1", "Test", "url", "company", "city", 100, 200, "USD")]
    db.insert_vacancies(vacancies)
    db.clear_vacancies()
    result = db.get_filtered_vacancies("", None)
    assert len(result) == 0

def test_get_filtered_vacancies(db):
    vacancies = [
        ("1", "Python Dev", "url", "Company", "Moscow", 100000, 150000, "RUB"),
        ("2", "Java Dev", "url", "Company", "Saint Petersburg", 90000, 120000, "RUB"),
    ]
    db.insert_vacancies(vacancies)
    result = db.get_filtered_vacancies("Moscow", 100000)
    assert len(result) == 1
