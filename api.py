import requests
import time

HEADERS = {
    'User-Agent': 'MyVacancyBot/1.0'
}


def get_employers(employer_ids: list):
    """Функция, которая получает информацию о работодателях по их ID."""
    employers = []
    for emp_id in employer_ids:
        url = f'https://api.hh.ru/employers/{emp_id}'
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            employers.append({
                'employer_id': data['id'],
                'name': data['name'],
                'url': data['alternate_url']
            })
        else:
            print(f"Ошибка при получении работодателя {emp_id}: {response.status_code}")
        time.sleep(0.3)  # чтобы не перегружать API ставим небольшой спящий режим
    return employers


def get_vacancies_for_employer(employer_id, per_page=10):
    """Функция, которая получает вакансии для работодателя."""
    url = 'https://api.hh.ru/vacancies'
    params = {
        'employer_id': employer_id,
        'per_page': per_page,
        'page': 0
    }
    vacancies = []

    while True:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Ошибка при получении вакансий для работодателя {employer_id}: {response.status_code}")
            break

        data = response.json()
        for item in data['items']:
            salary_from = item['salary']['from'] if item['salary'] and item['salary']['from'] else None
            salary_to = item['salary']['to'] if item['salary'] and item['salary']['to'] else None
            currency = item['salary']['currency'] if item['salary'] and item['salary']['currency'] else None

            vacancies.append({
                'vacancy_id': item['id'],
                'name': item['name'],
                'description': item.get('description', ''),
                'salary_from': salary_from,
                'salary_to': salary_to,
                'currency': currency,
                'published_at': item['published_at'],
                'employer_id': employer_id
            })

        if not data['pages'] or data['page'] >= data['pages'] - 1:
            break

        params['page'] += 1

    return vacancies
