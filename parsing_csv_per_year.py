import pandas as pd


class ParsingCsv():
    """Класс для парсинга большого csv файла на отдельные csv по годам
    Attributes:
        file_name(str): Название большого csv файла
    """
    def __init__(self, file_name):
        """Инициализация названия большого csv файла
        Args:
             file_name(str): Название большого csv файла
        """
        self.file_name = file_name

    def parse_csv(self):
        """Функция парсинга большого csv файла на отдельные csv по годам"""
        df = pd.read_csv(self.file_name, usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name',
                                                  'published_at'])
        if df.empty:
            return 'Пустой файл!'
        # df.dropna(inplace=True)
        years = (date[:4] for date in df['published_at'])
        years = set(years)
        for year in years:
            temp = []
            for col_name, row in df.iterrows():
                if year in row['published_at']:
                    temp.append(row)
            df_new = pd.DataFrame(temp)
            df_new.to_csv(f'csv\\csv_per_year_new\\{year}.csv', index=False)


ParsingCsv(input()).parse_csv()
