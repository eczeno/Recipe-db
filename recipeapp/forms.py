from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, IntegerField, FieldList
from wtforms.validators import DataRequired, Length, NumberRange

class EntryForm(FlaskForm):
    title = StringField('Title', [DataRequired()])
    preptime = StringField('Prep time')
    cooktime = StringField('Cook time')
    serves = IntegerField('Serves', [NumberRange(message='Please enter an integer')])
    ingredients_string = StringField('Ingredients', [DataRequired()])
    directions = TextField('Directions', [DataRequired(), Length(min=100, message='Please enter more directions')])
    notes = TextField('Notes')    
    submit = SubmitField('Submit')


class SearchIngredientsForm(FlaskForm):
    search_string = StringField('Search string', [DataRequired()])
    submit = SubmitField('Search')