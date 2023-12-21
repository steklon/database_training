import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
import os
import json


def record_data():
    with open('data_json.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)

        for record in data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
            }[record.get('model')]

            session.add(model(id=record.get('pk'), **record.get('fields')))


def menu(publisher):
    if is_number(publisher):
        column_name = Publisher.id
        get_data(column_name, publisher)
    else:
        column_name = Publisher.name
        get_data(column_name, publisher)


def is_number(str_):
    try:
        float(str_)
        return True
    except ValueError:
        return False


def get_data(column_name, accept):
    sales = (session
             .query(Book.title, Publisher.name, Shop.name, Sale.price, Sale.date_sale)
             .join(Book.publisher)
             .join(Book.stock)
             .join(Stock.shop)
             .join(Stock.sale)
             .filter(column_name == accept)
             .all())

    for sale in sales:
        print(f'{sale[0]} | {sale[2]} | {sale[3]} | {sale[4].strftime("%Y-%m-%d")} {sale[4].strftime("%H:%M:%S")}')


if __name__ == '__main__':
    DB_DRIVER = os.getenv('DB_DRIVER')
    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_ADDRESS = os.getenv('DB_ADDRESS')
    DB_PORT = os.getenv('DB_PORT')

    DSN = f'{DB_DRIVER}://{LOGIN}:{PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}'
    engine = sqlalchemy.create_engine(DSN)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    record_data()

    search_sales = input('Введите имя или идентификатор издателя: ')
    menu(search_sales)

    session.commit()
    session.close()



