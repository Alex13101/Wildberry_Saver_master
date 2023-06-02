from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///WB.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# таблица пользователь
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# таблица запросы
class Query(Base):
    __tablename__ = 'queries'
    query_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    query = Column(String)
    discount = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    user = relationship("User", backref="queries")

    def __str__(self):
        return f'{self.query = }'

# таблица товары
class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    query_id = Column(Integer, ForeignKey('queries.query_id'))
    name = Column(String)
    price = Column(Float)
    previous_price = Column(Float)
    updated_at = Column(DateTime)
    query = relationship("Query", backref="products")

# таблица уведомления
class Notification(Base):
    __tablename__ = 'notifications'
    notifications_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    query_id = Column(Integer, ForeignKey('queries.id'))
    previous_price = Column(Float)
    current_price = Column(Float)
    created_at = Column(DateTime)
    product = relationship("Product", backref="notifications")
    query = relationship("Query", backref="notifications")

# Создание таблиц
Base.metadata.create_all(engine)

# Закрытие соединения с базой данных
session.close()
