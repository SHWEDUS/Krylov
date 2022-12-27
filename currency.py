import pandas as pd
import requests
import xmltodict
import json
import warnings
warnings.filterwarnings("ignore")

file = 'C:\\Users\\Shwed\\PycharmProjects\\Krylov\\csv\\vacancies_dif_currencies.csv'

df = pd.read_csv(file, usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name',
                                'published_at'])

df.dropna(subset=['salary_currency'], inplace=True)


def get_count_currencies(df):
    """
    Функция подсчёта числа количества валют и отбор
    Atributes:
        param df(DataFrame): Датафрейм который нужно обработать
    Returns:
         correct_df(DataFrame): Датафрейм с нужными валютами
    """
    currencies = [cell for cell in df['salary_currency']]
    non_duplicates_currencies = set(currencies)

    current_currency = {}

    for currency in non_duplicates_currencies:
        if currency != '' and currency and currencies.count(currency) > 5000:
            current_currency[currency] = currencies.count(currency)
    correct_df = df[df.salary_currency.isin(current_currency.keys()) == True]
    return correct_df


def get_vacancy_date(df):
    """Функция обработки даты в датафрейме и получения ранней даты и поздней даты
    Atributes:
        df(DataFrame): Датафрейм который нужно обработать
    Returns:
        date_min(str): Ранняя дата датафрейма
        date_max(str): Поздняя дата датафрейма
    """
    df.dropna(subset=['published_at'], inplace=True)
    min_year = '2003'
    max_year = '2022'
    min_month = '12'
    date_min = ''
    max_month = '01'
    date_max = ''
    for date in df['published_at']:
        if date[5:7] < min_month:
            min_month = date[5:7]
            date_min = date[:7]
        elif date[5:7] == '01':
            date_min = date[:7]
        elif date[:4] > min_year:
            break
    for date in df['published_at']:
        if date[5:7] > max_month and date[:4] == max_year:
            max_month = date[5:7]
            date_max = date[:7]
        elif date[5:7] == '12':
            date_max = date[:7]
    return date_min, date_max


def get_correct_salary_from_api(df):
    """Получаем датафрейм с коффициантами валют для перевода в рубли
    Atributes:
        df(DataFrame): Датафрейм, который нужно обработать
    """
    df_currencies = get_count_currencies(df)
    date_min, date_max = get_vacancy_date(df_currencies)
    currencies_for_date = []
    for year in range(int(date_min[:4]), int(date_max[:4]) + 1):
        for month in range(int(date_min[5:7]), int(date_max[5:7]) + 1):
            date_currencies = {}
            date_currencies['date'] = f'{year}-{month:02}'
            url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{month:02}/{year}'
            response = requests.get(url).text
            json_text = json.dumps(xmltodict.parse(response))
            currencies = eval(json_text)['ValCurs']['Valute']
            #print(currencies)
            for currency in currencies:
                for cell in df_currencies['salary_currency']:
                    # print(currency['CharCode'])
                    if currency['CharCode'] in cell:
                        date_currencies[currency['CharCode']] = round(float(currency['Value'].replace(',', '.')) /
                                                                      float(currency['Nominal'].replace(',', '.')), 7)
            currencies_for_date.append((date_currencies))
            if year == int(date_max[:4] and month == int(date_max[5:7])):
                break
    df_correct_salary = pd.DataFrame(currencies_for_date)
    df_correct_salary.to_csv('\\csv\\correct_currencies_from_CBRF.csv', index=False)


get_correct_salary_from_api(df)

