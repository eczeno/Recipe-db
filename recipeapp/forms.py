from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange, URL

class EntryForm(FlaskForm):
    title = StringField('Title', [InputRequired()])
    preptime = StringField('Prep time')
    cooktime = StringField('Cook time')
    serves = IntegerField('Serves', [NumberRange(message='Please enter an integer')])
    ingredients_string = StringField('Ingredients', [InputRequired()])
    directions = TextField('Directions', [InputRequired(), Length(min=100, message='Please enter more directions')])
    notes = TextField('Notes')    
    submit = SubmitField('Submit')

class EnterLinkForm(FlaskForm):
    url = StringField('url', validators=[InputRequired(), URL()])
    submit = SubmitField('Submit')

class SearchIngredientsForm(FlaskForm):
    search_string = StringField('Search string', [InputRequired()])
    submit = SubmitField('Search')