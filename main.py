import os
from dotenv import load_dotenv
from db import create_database, create_tables, get_connection
from api import get_employers, get_vacancies_for_employer

load_dotenv()


def main():
    create_database()

    create_tables()

    employer_ids = [1001, 1027, 1050, 1070, 1100, 1130, 1150, 1180, 1200, 1250]

    employers_info = get_employers(employer_ids)

    with get_connection() as conn:
        with conn.cursor() as cur:
            for emp in employers_info:
                cur.execute("""
                    INSERT INTO organizations (employer_id, name, url)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (employer_id) DO NOTHING;
                """, (emp['employer_id'], emp['name'], emp['url']))

            for employer_id in employer_ids:
                print(f"Получение вакансий для работодателя {employer_id}...")
                vacancies = get_vacancies_for_employer(employer_id)
                for vac in vacancies:
                    try:
                        cur.execute("""
                            INSERT INTO vacancies (
                                vacancy_id, name, description,
                                salary_from, salary_to,
                                currency, published_at,
                                employer_id)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                            ON CONFLICT (vacancy_id) DO NOTHING;
                        """, (
                            vac['vacancy_id'], vac['name'], vac['description'],
                            vac['salary_from'], vac['salary_to'],
                            vac['currency'], vac['published_at'],
                            vac['employer_id']
                        ))
                    except Exception as e:
                        print(f"Ошибка вставки вакансии {vac['vacancy_id']}: {e}")


if __name__ == '__main__':
    main()
