import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class DBManager:
    """Класс для взаимодействия с базами данных"""

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        self.conn.autocommit = True

    def create_tables(self):
        """Метод для создания таблиц"""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id SERIAL PRIMARY KEY,
                    hh_id INTEGER UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    url TEXT NOT NULL,
                    salary_from NUMERIC,
                    salary_to NUMERIC,
                    salary_currency VARCHAR(10),
                    company_id INTEGER REFERENCES companies(id)
                );
            """)

    def insert_companies(self, companies):
        """Метод для внесения в БД данных о компаниях-работодателях"""
        with self.conn.cursor() as cur:
            for comp in companies:
                cur.execute("""
                    INSERT INTO companies (hh_id, name)
                    VALUES (%s, %s)
                    ON CONFLICT (hh_id) DO NOTHING;
                """, (comp['id'], comp['name']))

    def insert_vacancies(self, vacancies):
        """Метод для внесения в БД данных о вакансиях"""
        with self.conn.cursor() as cur:
            for vac in vacancies:
                # Получим id компании по hh_id
                cur.execute("SELECT id FROM companies WHERE hh_id=%s;", (vac['employer_id'],))
                company_row = cur.fetchone()
                if company_row:
                    company_db_id = company_row[0]
                    cur.execute("""
                        INSERT INTO vacancies (name, url, salary_from, salary_to, salary_currency, company_id)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """, (
                        vac['name'],
                        vac['url'],
                        vac['salary_from'],
                        vac['salary_to'],
                        vac['salary_currency'],
                        company_db_id
                    ))

    def get_companies_and_vacancies_count(self):
        """Метод, который получает список всех компаний и количество вакансий у каждой компании."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, COUNT(v.id) AS vacancy_count
                FROM companies c
                LEFT JOIN vacancies v ON c.id=v.company_id
                GROUP BY c.name;
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        """Метод, который получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и
        ссылки на вакансию."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.salary_currency, 
                v.url
                FROM vacancies v JOIN companies c ON v.company_id=c.id;
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        """Метод, который получает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((v.salary_from + v.salary_to)/2) FROM vacancies v 
                WHERE v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL;
            """)
            result = cur.fetchone()
            return result[0] if result else None

    def get_vacancies_with_higher_salary(self):
        """Метод, который получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, 
                v.salary_currency, v.url
                FROM vacancies v JOIN companies c ON v.company_id=c.id
                WHERE ((v.salary_from + v.salary_to)/2) > %s;
            """, (avg_salary,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Метод, который получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        pattern = f"%{keyword}%"
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.salary_currency, 
                v.url
                FROM vacancies v JOIN companies c ON v.company_id=c.id
                WHERE v.name ILIKE %s;
            """, (pattern,))
            return cur.fetchall()

    def close(self):
        """Метод, который закрывает соединение с БД"""
        self.conn.close()
