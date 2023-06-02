from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.config.from_object('config.Config')

db = SQLAlchemy(app)

from . import models, views  # noqa

db.create_all()


from .crud import add_query_to_database, add_product_history_data

add_query_to_database('test', 'test@test.test', 'test', 10)
add_product_history_data(1, 'test', 10,models.Query.query.get(1))
