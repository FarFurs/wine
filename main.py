from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
import collections
import openpyxl
from pprint import pprint
import argparse
from datetime import datetime


def get_corresponding_text(year) -> str:
    if year % 100 in (11, 12, 13, 14) or year % 10 in (0, 5, 6, 7, 8, 9):
        return 'лет'
    elif year % 10 == 1:
        return 'год'
    elif year % 10 in (2, 3, 4):
        return 'года'


def get_drinks(file_path) -> dict:
    excel_data_wines = pandas.read_excel(file_path,
                                         sheet_name='Лист1',
                                         na_values=['N/A', 'NA'],
                                         keep_default_na=False
                                        )

    drinks = collections.defaultdict(list)
    for wine in excel_data_wines.to_dict(orient='records'):
        drinks[wine['Категория']].append(wine)
    return drinks


def main() -> None:
    parser = argparse.ArgumentParser(description='Данные о напитках которые выпускает винодельня')
    parser.add_argument('--file_path',
                        help='Путь до excel файла',
                        default='wine.xlsx',
                        type=str
                        )
    args = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    year_of_foundation = 1927
    rendered_page = template.render(
        winery_age=datetime.now().year-year_of_foundation,
        year=get_corresponding_text(datetime.now().year - year_of_foundation),
        drinks=get_drinks(args.file_path)
                                    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
