from recipeapp import db


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable = False)
    source = db.Column(db.String())
    preptime = db.Column(db.Interval())
    cooktime = db.Column(db.Interval())
    totaltime = db.Column(db.Interval())
    serves = db.Column(db.String(30))
    directions = db.relationship('Directions', backref = 'recipe', cascade="all, delete-orphan")
    ingredients = db.relationship('Ingredient', backref = 'recipe', cascade="all, delete-orphan")
    

    def __repr__(self):
        return f'Recipe({self.title})'

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.String())
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

    def __repr__(self):
        return f'{self.line}'

class Directions(db.Model):
    __tablename__ = 'directions'
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.String())
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

    def __repr__(self):
        return f'{self.line}'

