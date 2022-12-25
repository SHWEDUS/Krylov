import multiprocessing
from get_statistic_per_years import DataSet, Information
import os
import glob
import time
start = time.time()
profession = 'Аналитик'


class PrintData():
    """Клас иницализации файлов и получения данных аналитики
    Atributes:
        file_name(str): Название файла
    """
    def __init__(self, file_name):
        """Инициализация названия файла
        Args:
             file_name(str): Название файла
        """
        self.file_name = file_name

    def print_data_analytic(self):
        """Получение данных по годам
        Returns:
            salary_year(dict{int: int}): Словарь со средними зарплатами по годам
            count_year(dict{int: int}): Словарь с количеством вакансий по годам
            salary_year_prof(dict{int: int}): Словарь со средними зарплатами выбранной профессии по годам
            count_year_prof(dict{int: int}): Словарь с количеством вакансий по выбранной профессии по годам
        """
        vacancies = DataSet(self.file_name).vacancies
        years = Information().get_city_and_year(vacancies)
        salary_year = {}
        count_year = {}
        salary_year_prof = {}
        count_year_prof = {}
        for year in years.keys():
            count_vacancies, length_salary_arr, count_vacancies_prof, length_salary_arr_prof = \
                Information.parser_vacancies_by_year(vacancies, year, profession)
            salary_year[year], count_year[year], salary_year_prof[year], count_year_prof[year] = \
                count_vacancies, length_salary_arr, count_vacancies_prof, length_salary_arr_prof
        return salary_year, count_year, salary_year_prof, count_year_prof


def go(file_name):
    """Старт работы программы
    Atributes:
        file_name(str): Название файла
    Returns:
        PrintData(): Данные по годам
    """
    return PrintData(file_name).print_data_analytic()


def get_multy():
    """Печатаем данные с помощью мультипроцессинга"""
    path = r'C:\Users\Shwed\PycharmProjects\Krylov\csv'
    os.chdir(path)
    files = glob.glob('*.{}'.format('csv'))
    with multiprocessing.Pool(processes=16) as p:
        result = p.map(go, files)
    years_salary_dictionary = {}
    years_count_dictionary = {}
    years_salary_vacancy_dict = {}
    years_count_vacancy_dict = {}
    list_dict = [years_salary_dictionary, years_count_dictionary, years_salary_vacancy_dict, years_count_vacancy_dict]
    for year in result:
        for i in range(len(year)):
            year_items = year[i].items()
            for dic in year_items:
                list_dict[i][dic[0]] = dic[1]
    print(f'Динамика уровня зарплат по годам: {years_salary_dictionary}')
    print(f'Динамика количества вакансий по годам: {years_count_dictionary}')
    print(f'Динамика уровня зарплат по годам для выбранной профессии: {years_salary_vacancy_dict}')
    print(f'Динамика количества вакансий по годам для выбранной профессии: {years_count_vacancy_dict}')


if __name__ == '__main__':
    get_multy()
    print(f'{time.time() - start} seconds')
