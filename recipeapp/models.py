from recipeapp import db

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

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'{self.name}'