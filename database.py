import sqlite3

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def _execute_query(self, query, params=()):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            raise

    def create_table(self):
        query = """
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
        """
        self._execute_query(query)

    def clear_vacancies(self):
        self._execute_query("DELETE FROM vacancies")

    def insert_vacancies(self, vacancies):
        query = """
            INSERT OR REPLACE INTO vacancies 
            (id, title, url, company, area, salary_from, salary_to, currency)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany(query, vacancies)
            conn.commit()

    def get_filtered_vacancies(self, city, salary_from):
        query = "SELECT * FROM vacancies WHERE 1=1"
        params = []
        if city:
            query += " AND area LIKE ?"
            params.append(f"%{city}%")
        if salary_from:
            salary_from = float(salary_from)
            query += " AND (salary_from >= ? OR (salary_from IS NULL AND salary_to >= ?))"
            params.extend([salary_from, salary_from])
        cursor = self._execute_query(query, params)
        return cursor.fetchall()