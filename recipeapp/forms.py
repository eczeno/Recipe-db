from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FieldList, FormField, TextAreaField
from wtforms.validators import InputRequired, Length, NumberRange, URL
from recipeapp.models import Ingredient, Directions
class EnterLinkForm(FlaskForm):
    url = StringField('url', validators=[InputRequired(), URL()], render_kw={'autofocus': True})
    submit = SubmitField('Submit')

class SearchIngredientsForm(FlaskForm):
    ingredients_string = StringField('ingredients_string', validators=[InputRequired()], render_kw={'autofocus': True})
    search_ingredients = SubmitField('Search Ingredients')


class SearchTitleForm(FlaskForm):
    title_string = StringField('title_string', validators=[InputRequired()])
    search_title = SubmitField('Search Title')


class DeleteForm(FlaskForm):
    delete_id = IntegerField('delete_id', validators=[InputRequired(), NumberRange()], render_kw={'autofocus': True})
    submit = SubmitField('Delete')

class IngredientForm(FlaskForm):
    ingredient = StringField('Ingredient')


class DirectionForm(FlaskForm):
    direction = StringField('Direction')

class EntryForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()], render_kw={'autofocus': True})
    preptime = IntegerField('Prep Time')
    cooktime = IntegerField('Cook Time')
    totaltime = IntegerField('Total Time')
    serves = StringField('Serves')
    ingredients = TextAreaField('Ingredients', validators=[InputRequired()])
    directions = TextAreaField('Directions', validators=[InputRequired()])
    submit = SubmitField('Submit')




