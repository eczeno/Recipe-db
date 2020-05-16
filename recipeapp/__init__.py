from flask import Flask
from flask_sqlalchemy import SQLAlchemy, declarative_base
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

from recipeapp import routes