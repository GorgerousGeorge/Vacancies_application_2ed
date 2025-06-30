from src.db import DBManager


def main():
    """Точка входа и взаимодействие с пользователем"""
    db_manager = DBManager()

    while True:
        print("\nВыберите действие:")
        print("1 - Получить список компаний и количество вакансий")
        print("2 - Получить все вакансии")
        print("3 - Средняя зарплата по вакансиям")
        print("4 - Вакансии с зарплатой выше средней")
        print("5 - Вакансии по ключевому слову")
        print("6 - Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            results = db_manager.get_companies_and_vacancies_count()
            for name, count in results:
                print(f"Компания: {name}, Вакансий: {count}")

        elif choice == '2':
            results = db_manager.get_all_vacancies()
            for comp_name, vac_name, s_from, s_to, currency, url in results:
                print(
                    f"Компания: {comp_name}\nВакансия: {vac_name}\nЗарплата: {s_from} - {s_to} {currency}\nСсылка: "
                    f"{url}\n---")

        elif choice == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {avg_salary:.2f}" if avg_salary else "Нет данных о зарплатах.")

        elif choice == '4':
            results = db_manager.get_vacancies_with_higher_salary()
            for comp_name, vac_name, s_from, s_to, currency, url in results:
                print(
                    f"Компания: {comp_name}\nВакансия: {vac_name}\nЗарплата: {s_from} - {s_to} {currency}\nСсылка: "
                    f"{url}\n---")

        elif choice == '5':
            keyword = input("Введите ключевое слово для поиска в названии вакансии: ")
            results = db_manager.get_vacancies_with_keyword(keyword)

            for comp_name, vac_name, s_from, s_to, currency, url in results:
                print(
                    f"Компания: {comp_name}\nВакансия: {vac_name}\nЗарплата: {s_from} - {s_to} {currency}\nСсылка: "
                    f"{url}\n---")

        elif choice == '6':
            print("Выход.")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")

    db_manager.close()


if __name__ == "__main__":
    main()
