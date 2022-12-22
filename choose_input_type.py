from get_full_statistic_and_table import DataSet, Information, Report
import pdfkit


def choose_type():
    file_name = 'vacancies.csv'
    profession = 'Программист'
    choosing_type = input('Введите данные для печати: ')
    data = DataSet(file_name)
    salary_year, count_year, salary_year_prof, count_year_prof, salary_dict_by_city, count_vacancies_dict_by_city = \
        Information.work(data.vacancies, profession)
    sum_count = sum(list(count_vacancies_dict_by_city.values()))
    count_vacancies_dict_by_city.update(
        (x, f'{round(y * 100, 2)}%') for x, y in count_vacancies_dict_by_city.items())

    new_count_vacancies_dict_by_city = {'Другие': f'{100 - (sum_count * 100)}%'}
    new_count_vacancies_dict_by_city.update(count_vacancies_dict_by_city)
    report = Report(salary_year, count_year, salary_year_prof, count_year_prof, salary_dict_by_city,
                    count_vacancies_dict_by_city, new_count_vacancies_dict_by_city, profession, choosing_type)
    report.generate_excel.save('report.xlsx')
    report.generate_image.savefig('graph.png')
    pdf_template = report.generate_pdf
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdfkit.from_string(pdf_template, 'report.pdf', configuration=config, options={'enable-local-file-access': True})


choose_type()
