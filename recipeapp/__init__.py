from flask import Flask
from flask_sqlalchemy import SQLAlchemy, declarative_base

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
db = SQLAlchemy(app)

from recipeapp import routes