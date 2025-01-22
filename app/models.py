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
    id = db.Column('id_country', db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Country {self.name}>"


class Counterparty(db.Model):
    __tablename__ = 'counterparty'
    id = db.Column('id_counterparty', db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    license = db.Column('lisensis', db.Integer, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id_country'), nullable=False)
    phone = db.Column(db.String(14), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    br_assessment = db.Column(db.Integer, nullable=False)  # Оцінка ДР
    im_assessment = db.Column(db.Integer, nullable=False)  # Оцінка ІМ

    country = db.relationship('Country', backref=db.backref('counterparties', lazy=True))

    def __repr__(self):
        return f"<Counterparty {self.name}>"


class RankCatalogue(db.Model):
    __tablename__ = 'rank_catalogue'
    id = db.Column('id_rank_catalogue', db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return f"<RankCatalogue {self.rank}>"


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column('id_order', db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    date_of_order = db.Column('date_of_order', db.Date, nullable=False)

    def __repr__(self):
        return f"<Order {self.name}>"


class DataAboutOrder(db.Model):
    __tablename__ = 'data_about_order'
    id = db.Column('id_data_about_order', db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id_order'), nullable=False)
    date_receiving_planned = db.Column('date_receiving_planned', db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', backref=db.backref('data', lazy=True))

    def __repr__(self):
        return f"<DataAboutOrder {self.id}>"


class Supply(db.Model):
    __tablename__ = 'supply'
    id = db.Column('id_supply', db.Integer, primary_key=True)
    data_about_order_id = db.Column(db.Integer, db.ForeignKey('data_about_order.id_data_about_order'), nullable=False)
    rank_catalogue_id = db.Column(db.Integer, db.ForeignKey('rank_catalogue.id_rank_catalogue'), nullable=False)
    counterparty_id = db.Column(db.Integer, db.ForeignKey('counterparty.id_counterparty'), nullable=False)
    date_receiving_actual = db.Column('date_receiving_actual', db.Date, nullable=False)
    amount_receiving_actual = db.Column('amount_receiving_actual', db.Integer, nullable=False)
    refund_amount = db.Column('refund_amount', db.Integer, nullable=True)

    data_about_order = db.relationship('DataAboutOrder', backref=db.backref('supplies', lazy=True))
    rank_catalogue = db.relationship('RankCatalogue', backref=db.backref('supplies', lazy=True))
    counterparty = db.relationship('Counterparty', backref=db.backref('supplies', lazy=True))

    def __repr__(self):
        return f"<Supply {self.id}>"
