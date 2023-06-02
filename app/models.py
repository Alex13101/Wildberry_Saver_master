from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    queries = db.relationship("Query")


class Query(db.Model):
    __tablename__ = 'queries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    query_title = db.Column(db.String(255))
    discount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship("User")
    products = db.relationship("Product", secondary="products_queries")
    notifications = db.relationship("Notification")


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)

    queries = db.relationship("Query", secondary="products_queries")
    history = db.relationship("History")


class ProductsQueries(db.Model):
    __tablename__ = 'products_queries'

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    query_id = db.Column(db.Integer, db.ForeignKey('queries.id'), primary_key=True)


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    query_id = db.Column(db.Integer, db.ForeignKey('queries.id'))
    previous_price = db.Column(db.Float)
    current_price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)

    product = db.relationship("Product")


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    price = db.Column(db.Float)

    product = db.relationship("Product")
