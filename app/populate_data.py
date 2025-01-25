from app import db  # Импорт объекта базы данных из app.py
from app.models import Country, Counterparty, Order, DataAboutOrder, RankCatalogue, Supply, RevenueInvoice, ReturnInvoice  # Импорт моделей
from datetime import date

# Добавляем фиктивные данные для таблицы "Country"
countries = [
    Country(id=1, name='Україна'),
    Country(id=2, name='Китай'),
    Country(id=3, name='Німеччина')
]

for country in countries:
    db.session.add(country)

db.session.commit()
print("Данные для таблицы 'Country' добавлены.")

# Добавляем фиктивные данные для таблицы "Counterparty"
counterparties = [
    Counterparty(
        id=1, name='Counterparty 1', country_id=1,
        license=1234, phone='+380123456789', email='counterparty1@example.com',
        br_assessment=2, im_assessment=2
    ),
    Counterparty(
        id=2, name='Counterparty 2', country_id=2,
        license=5678, phone='+14155552671', email='counterparty2@example.com',
        br_assessment=1, im_assessment=2
    )
]

for counterparty in counterparties:
    db.session.add(counterparty)

db.session.commit()
print("Данные для таблицы 'Counterparty' добавлены.")

# Добавляем фиктивные данные для таблицы "Order"
orders = [
    Order(id=1, name='Замовлення 1', date_of_order=date(2025, 1, 12)),
    Order(id=2, name='Замовлення 2', date_of_order=date(2025, 1, 21))
]

for order in orders:
    db.session.add(order)

db.session.commit()
print("Данные для таблицы 'Order' добавлены.")

# Добавляем фиктивные данные для таблицы "DataAboutOrder"
order_data = [
    DataAboutOrder(
        id=1,
        order_id=1,  # Связь с таблицей "Order"
        date_receiving_planned=date(2025, 1, 12),
        amount=5000
    ),
    DataAboutOrder(
        id=2,
        order_id=2,
        date_receiving_planned=date(2025, 1, 20),
        amount=8000
    )
]

for data in order_data:
    db.session.add(data)

db.session.commit()
print("Данные для таблицы 'DataAboutOrder' добавлены.")

# Фиктивные данные для "RankCatalogue"
catalog_data = [
    RankCatalogue(id=1, score=5, rank='A'),
    RankCatalogue(id=2, score=4, rank='B')
]

for data in catalog_data:
    db.session.add(data)

db.session.commit()
print("Данные для таблицы 'RankCatalogue' добавлены.")

# Фиктивные данные для "Revenue_invoice"
incoming_invoices = [
    RevenueInvoice(id=1, name="Накладна 1"),
    RevenueInvoice(id=2, name="Накладна 2")
]

for invoice in incoming_invoices:
    db.session.add(invoice)

db.session.commit()
print("Данные для таблицы 'RevenueInvoice' добавлены.")

# Фиктивные данные для "Return_invoice"
return_invoices = [
    ReturnInvoice(id=1, name="Зворотня накладна 1"),
    ReturnInvoice(id=2, name="Зворотня накладна 2")
]

for invoice in return_invoices:
    db.session.add(invoice)

db.session.commit()
print("Данные для таблицы 'ReturnInvoice' добавлены.")

# Добавляем фиктивные данные для таблицы "Supply"
supplies = [
    Supply(
        id=1,
        data_about_order_id=1,  # Связь с таблицей "DataAboutOrder"
        rank_catalogue_id=1,   # Связь с таблицей "RankCatalogue"
        counterparty_id=1,     # Связь с таблицей "Counterparty"
        revenue_invoice_id=1,  # Связь с таблицей "Revenue_invoice"
        return_invoice_id=1,   # Связь с таблицей "Return_invoice"
        date_receiving_actual=date(2025, 1, 10),
        amount_receiving_actual=5000,
        refund_amount=100
    ),
    Supply(
        id=2,
        data_about_order_id=2,
        rank_catalogue_id=2,
        counterparty_id=2,
        revenue_invoice_id=2,
        return_invoice_id=2,
        date_receiving_actual=date(2025, 1, 15),
        amount_receiving_actual=8000,
        refund_amount=200
    )
]

for supply in supplies:
    db.session.add(supply)

db.session.commit()
print("Данные для таблицы 'Supply' добавлены.")