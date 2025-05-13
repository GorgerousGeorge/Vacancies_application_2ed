import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()


class DBManager:
    """Класс, который подключается к БД и взаимодействует с ней"""
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """метод, который получает список всех компаний и количество вакансий у каждой компании."""
        query = """
        SELECT company_name, COUNT(*) AS vacancies_count
        FROM vacancies
        GROUP BY company_name;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """метод, который получает список всех вакансий"""
        query = "SELECT * FROM vacancies;"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """метод, который получает среднюю зарплату по вакансиям"""
        query = "SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL;"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_vacancies_with_higher_salary(self):
        """метод, который получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        query = "SELECT * FROM vacancies WHERE salary > %s;"
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """метод, который получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        query = "SELECT * FROM vacancies WHERE description ILIKE %s;"
        like_pattern = f"%{keyword}%"
        self.cursor.execute(query, (like_pattern,))
        return self.cursor.fetchall()

    def close(self):
        """метод, который закрывает соединение с БД"""
        self.cursor.close()
        self.conn.close()
