import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')


def create_database():
    """Функция для создания БД"""
    conn = psycopg2.connect(host=HOST, port=PORT, user=USER, password=PASSWORD)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}';")
    if not cur.fetchone():
        cur.execute(f'CREATE DATABASE {DB_NAME};')
        print(f"База данных {DB_NAME} создана.")
    else:
        print(f"База данных {DB_NAME} уже существует.")
    cur.close()
    conn.close()


def get_connection():
    """Функция, которая возвращает соединение с базой данных."""
    return psycopg2.connect(
        host=HOST,
        port=PORT,
        database=DB_NAME,
        user=USER,
        password=PASSWORD
    )


def create_tables():
    """Функция, которая создает таблицы в базе данных."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS organizations (
                    id SERIAL PRIMARY KEY,
                    employer_id INTEGER UNIQUE NOT NULL,
                    name VARCHAR(255),
                    url VARCHAR(255)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    vacancy_id INTEGER UNIQUE NOT NULL,
                    name VARCHAR(255),
                    description TEXT,
                    salary_from NUMERIC,
                    salary_to NUMERIC,
                    currency VARCHAR(10),
                    published_at TIMESTAMP,
                    employer_id INTEGER REFERENCES organizations(employer_id)
                );
            """)
            print("Таблицы созданы.")
