from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange, URL

class EnterLinkForm(FlaskForm):
    url = StringField('url', validators=[InputRequired(), URL()], render_kw={'autofocus': True})
    submit = SubmitField('Submit')

class SearchIngredientsForm(FlaskForm):
    ingredients_string = StringField('ingredients_string', validators=[InputRequired(), Length(min=1)], render_kw={'autofocus': True})
    submit = SubmitField('Search')

class DeleteForm(FlaskForm):
    delete_id = IntegerField('delete_id', validators=[InputRequired(), NumberRange()], render_kw={'autofocus': True})
    submit = SubmitField('Delete')