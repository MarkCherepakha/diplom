from app import db  # Импорт объекта базы данных из app.py
from app.models import Country, Counterparty, Order, DataAboutOrder, RankCatalogue  # Импорт моделей
from datetime import date

# Добавляем фиктивные данные для таблицы "Country"
countries = [
    Country(PK_ID_country=1, Name='Україна'),
    Country(PK_ID_country=2, Name='Китай'),
    Country(PK_ID_country=3, Name='Німеччина')
]

for country in countries:
    db.session.add(country)

db.session.commit()
print("Данные для таблицы 'Country' добавлены.")

# Добавляем фиктивные данные для таблицы "Counterparty"
counterparty = [
    Counterparty(
        PK_ID_counterparty = 1, name ='Counterparty 1', FK1_ID_country = 1,
        license = 1234, Phone = '+380123456789', E_mail = 'counterparty1@example.com',
        br_assessment = 2, im_assessment = 2
    ),
    Counterparty(
        PK_ID_counterparty=2, name ='Counterparty 2', FK1_ID_country=2,
        license = 5678, Phone = '+14155552671', E_mail = 'counterparty2@example.com',
        br_assessment = 1, im_assessment = 2
    )
]

for contractor in counterparty:
    db.session.add(contractor)

db.session.commit()
print("Данные для таблицы 'Counterparty' добавлены.")

# Добавляем фиктивные данные для таблицы "Замовлення"
orders = [
    Order(PK_ID_order=1, Name='Замовлення 1', date_of_order=date(2025, 1, 12)),
    Order(PK_ID_order=2, Name='Замовлення 2', date_of_order=date(2025, 1, 21))
]

for order in orders:
    db.session.add(order)

db.session.commit()
print("Данные для таблицы 'Order' добавлены.")


order_data = [
    DataAboutOrder(
        PK_ID_data_about_order = 1,
        FK1_ID_order = 1,  # Связь с таблицей "Замовлення"
        date_receiving_planned = date(2025, 1, 12),
        Сума = 5000
    ),
    DataAboutOrder(
        PK_ID_data_about_order = 2,
        FK1_ID_order = 2,
        date_receiving_planned = date(2025, 1, 20),
        Сума = 8000
    )
]

for data in order_data:
    db.session.add(data)

db.session.commit()
print("Данные для таблицы 'Дані про замовлення' добавлены.")


# Фиктивные данные для "Каталог даних"
catalog_data = [
    RankCatalogue(PK_ID_rank_catalogue = 1, score = 5, Rank='A'),
    RankCatalogue(PK_ID_rank_catalogue = 2, score = 4, Rank='B')
]

for data in catalog_data:
    db.session.add(data)

db.session.commit()
print("Данные для таблицы 'Каталог даних' добавлены.")