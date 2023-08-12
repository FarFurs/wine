from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
import collections
import openpyxl
from pprint import pprint
import argparse


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
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', help='Путь до excel файла', default='wine3.xlsx', type=str)
    parser.add_argument('--winery_age', help='Возраст винодельни', default=100, type=int)
    args = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    rendered_page = template.render(
        winery_age = args.winery_age,
        year = get_corresponding_text(args.winery_age),
        drinks = get_drinks(args.file_path)
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    get_corresponding_text(100)
        
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()