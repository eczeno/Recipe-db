from flask import jsonify
from recipeapp import db, ma
import json
import jsons 

ref_table = db.Table('ref_table',
                     db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id')),
                     db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id')))

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable = False)
    # source = link
    preptime = db.Column(db.String(20))
    cooktime = db.Column(db.String(20))
    serves = db.Column(db.Integer)
    directions = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    ingredients = db.relationship('Ingredient', secondary=ref_table, backref=db.backref('recipes', lazy='dynamic'))
    

    # def __init__(self, ):
    #     self.id = id
    #     self.title = title
    #     self.preptime = preptime
    #     self.ingredients = ingredients


    def __repr__(self):
        return f'{self.title}'


    def to_json(self):
        recipe_schema = RecipeSchema()
        recipe_json = recipe_schema.dump(self).data
        print('recipejson =', recipe_json)
        return jsonify({'recipe':recipe_json})

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'{self.name}'


class RecipeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Recipe


class IngredientSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Ingredient