from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Country {self.name}>"


class Counterparty(db.Model):
    __tablename__ = 'counterparty'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    license = db.Column(db.String(20), nullable=False)  # Лицензия как строка
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    business_risk_score = db.Column(db.Integer, nullable=False)
    impact_score = db.Column(db.Integer, nullable=False)

    country = db.relationship('Country', backref=db.backref('counterparties', lazy=True))

    def __repr__(self):
        return f"<Counterparty {self.name}>"


class RankCatalogue(db.Model):
    __tablename__ = 'rank_catalogue'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return f"<RankCatalogue {self.rank}>"


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_of_order = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Order {self.name}>"


class DataAboutOrder(db.Model):
    __tablename__ = 'data_about_order'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    date_receiving_planned = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    order = db.relationship('Order', backref=db.backref('data', lazy=True))

    def __repr__(self):
        return f"<DataAboutOrder {self.id}>"


class RevenueInvoice(db.Model):
    __tablename__ = 'revenue_invoice'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<RevenueInvoice {self.name}>"


class ReturnInvoice(db.Model):
    __tablename__ = 'return_invoice'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<ReturnInvoice {self.name}>"


class Supply(db.Model):
    __tablename__ = 'supply'
    id = db.Column(db.Integer, primary_key=True)
    data_about_order_id = db.Column(db.Integer, db.ForeignKey('data_about_order.id'), nullable=False)
    rank_catalogue_id = db.Column(db.Integer, db.ForeignKey('rank_catalogue.id'), nullable=False)
    counterparty_id = db.Column(db.Integer, db.ForeignKey('counterparty.id'), nullable=False)
    revenue_invoice_id = db.Column(db.Integer, db.ForeignKey('revenue_invoice.id'), nullable=False)
    return_invoice_id = db.Column(db.Integer, db.ForeignKey('return_invoice.id'), nullable=False)
    date_receiving_actual = db.Column(db.Date, nullable=False)
    amount_receiving_actual = db.Column(db.Float, nullable=False)
    refund_amount = db.Column(db.Float, nullable=True)

    data_about_order = db.relationship('DataAboutOrder', backref=db.backref('supplies', lazy=True))
    rank_catalogue = db.relationship('RankCatalogue', backref=db.backref('supplies', lazy=True))
    counterparty = db.relationship('Counterparty', backref=db.backref('supplies', lazy=True))
    revenue_invoice = db.relationship('RevenueInvoice', backref=db.backref('supplies', lazy=True))
    return_invoice = db.relationship('ReturnInvoice', backref=db.backref('supplies', lazy=True))

    def __repr__(self):
        return f"<Supply {self.id}>"
