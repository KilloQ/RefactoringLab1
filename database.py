import sqlite3

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    url TEXT,
                    company TEXT,
                    area TEXT,
                    salary_from INT,
                    salary_to INT,
                    currency TEXT
                )
            """)
            conn.commit()

    def clear_vacancies(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM vacancies")
            conn.commit()

    def insert_vacancies(self, vacancies):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany("INSERT INTO vacancies VALUES (?,?,?,?,?,?,?,?)", vacancies)
            conn.commit()

    def get_filtered_vacancies(self, city, salary_from):
        query = "SELECT * FROM vacancies"
        params = []

        if city:
            query += " WHERE area LIKE ?"
            params.append('%' + city + '%')
        if salary_from:
            salary_from = float(salary_from)
            if city:
                query += " AND "
            else:
                query += " WHERE "
            query += "(salary_from >= ? OR (salary_to >= ? AND salary_from IS NULL))"
            params.extend([salary_from, salary_from])

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

