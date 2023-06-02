import grequests
import time
import schedule
from app import db

from app.crud import add_product_history_data


def search_right_product(query):
    urls = [
        f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1281648&page={i}&query={query}&regions=80,64,38,4,115,83,33,68,70,69,30,86,75,40,1,66,48,110,31,22,71,114&resultset=catalog&sort=popular&spp=22&suppressSpellcheck=false'
        for i in range(1, 61)]

    rs = (grequests.get(u) for u in urls)
    lst = grequests.map(rs)
    all_products = [product for f in lst for product in f.json()['data']['products']]
    result = []
    for product in all_products:
        dct = {'product_id': product.get('id'), 'salePriceU': product.get('salePriceU') / 100,
               'name': product.get('name')}
        result.append(dct)
    return result

queries = db.session.query().filter_by(query_title=()).all()  # Получаем все запросы из базы

print(queries)

def run_task(queries):
    long_lst = len(search_right_product(queries))  # Длина списка товаров
    for query in queries:
        search_right_product(query)
        all_products = []
        for i in range(0, long_lst): # Идем по списку всех товаров
            product_name = all_products[i].setdefault("name")
            priced = all_products[i].setdefault('salePriceU')
            current_price = float(priced/100)
            product_id = all_products[i].setdefault('id')
            add_product_history_data(product_id, product_name, current_price, query)

# Запуск задачи по расписанию
schedule.every(6).hours.do(run_task(queries))  # Можно изменить интервал выполнения задачи

# Бесконечный цикл для выполнения задачи


while True:
    try:
        schedule.run_pending()
    except Exception as E:
        time.sleep(1)



# ToDo: Добавить функцию получения из БД списка запросов

# ToDo: Добавить функцию записи данных в БД
