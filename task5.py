import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale, Base

DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_NAME = os.getenv('DB_NAME', 'test_db')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DSN)
Session = sessionmaker(bind=engine)

def load_test_data():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()
    with open('fixtures/tests_data.json', 'r', encoding='utf-8') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()
    session.close()
    print("Тестовые данные успешно загружены.")

def find_purchases_by_publisher(publisher_input):
    """
    Выводит покупки книг заданного издателя.
    :param publisher_input: Имя издателя (строка) или его идентификатор (число)
    """
    with Session() as session:
        # Преобразуем ввод в число или строку
        if publisher_input.isdigit():
            publisher_input = int(publisher_input)
            publisher_filter = Publisher.id == publisher_input
        else:
            publisher_filter = Publisher.name == publisher_input

        # Поиск издателя
        publisher = session.query(Publisher).filter(publisher_filter).one_or_none()

        if not publisher:
            print(f"Издатель '{publisher_input}' не найден.")
            return

        # Запрос данных о покупках
        purchases_query = (
            session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
            .join(Stock, Stock.id_book == Book.id)
            .join(Sale, Sale.id_stock == Stock.id)
            .join(Shop, Stock.id_shop == Shop.id)
            .filter(Book.id_publisher == publisher.id)
            .order_by(Sale.date_sale)
        )

        print(f"Покупки книг издателя '{publisher.name}':")
        for title, shop_name, price, date_sale in purchases_query:
            print(f"{title} | {shop_name:15} | {price} | {date_sale.strftime('%d-%m-%Y')}")

if __name__ == "__main__":
    print("1. Загрузить тестовые данные")
    print("2. Найти покупки по издателю")
    choice = input("Выберите действие (1 или 2): ").strip()

    if choice == "1":
        load_test_data()
    elif choice == "2":
        publisher_input = input("Введите имя или идентификатор издателя: ").strip()
        find_purchases_by_publisher(publisher_input)
    else:
        print("Неверный выбор. Завершение программы.")