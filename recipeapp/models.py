from recipeapp import db
import json

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
    ingredients = db.relationship('Ingredient', secondary=ref_table, backref='recipes')
    
    def __repr__(self):
        return f'{self.title}'

    def make_ingredients_string(self):
        ingredients_list = [i for i in self.ingredients]
        ingredients_string = ','.join(ingredients_list)
        print('ingredients_string =', ingredients_string)
        return ingredients_string

    def to_json(self):
        recipe_json = {}
        ingredients_string = self.make_ingredients_string()
        recipe_json['id'] = self.id
        recipe_json['title'] = self.title
        if self.preptime:
            recipe_json['preptime'] = self.preptime
        if self.cooktime:
            recipe_json['cooktime'] = self.cooktime
        if self.serves:
            recipe_json['serves'] = self.serves
        recipe_json['directions'] = self.directions
        if self.notes:
            recipe_json['notes'] = self.notes
        recipe_json['ingredients'] = ingredients_string
        return recipe_json

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    # recipes = db.relationship('Recipes', secondary=ref_table, backref='ingredients')
    
    def __repr__(self):
        return f'{self.name}'