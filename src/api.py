import requests
import time

BASE_URL = "https://api.hh.ru"


def get_companies():
    """Возвращает список из компаний, вакансии которых мы ищем"""
    companies_names = [
        "Yandex",
        "Т-Банк",
        "Т1",
        "Ростелеком",
        "Yadro",
        "VK",
        "билайн",
        "ГАЗИНФОРМСЕРВИС",
        "КРОК",
        "Газпром автоматизация"
    ]
    companies = []
    for name in companies_names:
        params = {'text': name}
        response = requests.get(f"{BASE_URL}/employers", params=params)
        if response.status_code == 200:
            items = response.json().get('items', [])
            if items:
                employer = items[0]
                companies.append({
                    'id': employer['id'],
                    'name': employer['name']
                })
        time.sleep(0.3)  # чтобы не перегружать API ставим небольшой спящий режим
    return companies


def get_vacancies_for_company(employer_id):
    """Получает вакансии для компании по employer_id."""
    vacancies = []
    page = 0
    while True:
        params = {
            'employer_id': employer_id,
            'page': page,
            'per_page': 50
        }
        response = requests.get(f"{BASE_URL}/vacancies", params=params)
        if response.status_code != 200:
            break
        data = response.json()
        items = data.get('items', [])
        for item in items:
            salary_from = item['salary']['from'] if item['salary'] and item['salary']['from'] else None
            salary_to = item['salary']['to'] if item['salary'] and item['salary']['to'] else None
            salary_currency = item['salary']['currency'] if item['salary'] and 'currency' in item['salary'] else None
            vacancies.append({
                'name': item['name'],
                'url': item['alternate_url'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'salary_currency': salary_currency,
                'employer_id': employer_id
            })
        if not data.get('more'):
            break
        page += 1
        time.sleep(0.3)
    return vacancies
