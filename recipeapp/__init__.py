from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../config.py')
db = SQLAlchemy(app)
# app.config['SECRET_KEY'] = '\xc1D\xfd\xdf\xff\xe8\x08\x19\xab*X]\xa6\xcb\xd9\xdd\xc4\xd6m\xd3'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'


from recipeapp import routes