from src.db import DBManager
from src.api import get_companies
from src.api import get_vacancies_for_company


def setup_database():
    """Получает компании и вакансии для них и вставляет их в БД"""
    db_manager = DBManager()
    db_manager.create_tables()

    companies = get_companies()
    db_manager.insert_companies(companies)

    for comp in companies:
        vacancies = get_vacancies_for_company(comp['id'])
        db_manager.insert_vacancies(vacancies)


if __name__ == "__main__":
    setup_database()
