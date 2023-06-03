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
    lst = [el for el in lst if el.status_code == 200]
    all_products = [product for f in lst for product in f.json()['data']['products']]
    result = []
    for product in all_products:
        dct = {'product_id': product.get('id'), 'salePriceU': product.get('salePriceU') / 100,
               'name': product.get('name')}
        result.append(dct)
    return result





def run_task():
    queries = db.session.query().filter_by(query_title=()).all()  # Получаем все запросы из базы

    for query in queries:

        all_products = search_right_product(query)

        for i in range(0, len(all_products)): # Идем по списку всех товаров
            product_name = all_products[i].setdefault("name")
            priced = all_products[i].setdefault('salePriceU')
            current_price = float(priced/100)
            product_id = all_products[i].setdefault('id')
            add_product_history_data(product_id, product_name, current_price, query)

# Запуск задачи по расписанию
  # Можно изменить интервал выполнения задачи

def main():
    schedule.every(6).hours.do(run_task)
    while True:
        try:
            schedule.run_pending()
        except Exception as E:
            time.sleep(1)

# Бесконечный цикл для выполнения задачи

if __name__ == '__main__':
    main()




# ToDo: Добавить функцию получения из БД списка запросов

# ToDo: Добавить функцию записи данных в БД


# rs = (grequests.get(url=response_93_http, json=j, headers=headers) for j in jsons)
#     for r in grequests.map(rs, size=16, exception_handler=lambda d, y: print(d, y)):
#         try:
#             if r.status_code == 200:
#                 print(r.json())
#                 print(r.status_code, r.url)
#         except Exception as e:
#             print(e)


# notifications = []
# for product in products_all:
#     product_id = product['id']
#     product_name = product['name']
#     current_price = product['price']
#     notification = add_product_history_data(product_id, product_name, current_price, query_obj)
#     if notification:
#         notifications.append(notification)
#
# send_email(notifications)