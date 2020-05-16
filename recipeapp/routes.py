from flask import render_template, url_for, redirect, request, session, jsonify
from recipeapp import app, db
from recipeapp.forms import EntryForm, SearchIngredientsForm
from recipeapp.models import Recipe, Ingredient, RecipeSchema


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['GET','POST'])
def search():
    
    form = SearchIngredientsForm()
    search_ingredients = str(form.search_string.data)
    recipes = Recipe.query.all()
    results_list = []
    if recipes:
        if search_ingredients:
            search_list = search_ingredients.split(',')
        else:
            search_list = []
        for ingredient in search_list:
            ingredient_obj = Ingredient.query.filter_by(name=ingredient).first()
            print('obj =', ingredient_obj, type(ingredient_obj))
            for recipe in recipes:
                ingredients_list = list(recipe.ingredients)
                if ingredient_obj in ingredients_list:
                    results_list.append(recipe.id)
                    print('results =', results_list)
        session['results_list'] = results_list
    if form.validate_on_submit():
        return redirect(url_for('results'))
    return render_template('search.html', form=form, recipes=recipes)


@app.route('/results')
def results():
    results_list = session.get('results_list')
    # result = session.query(Recipe).filter(Recipe.id = recipe_id)
    recipe_objects = []
    if results_list:
        for recipe_id in results_list:
            recipe_objects.append(Recipe.query.get(recipe_id)) 
            print('recipe_objects is now: ', recipe_objects)         
    return render_template('results.html', recipe_objects=recipe_objects)


@app.route('/enter', methods=('GET', 'POST'))
def enter():
    form = EntryForm()
    if form.validate_on_submit():        
        recipe = Recipe(title=form.title.data, directions=form.directions.data)
        if form.preptime:
            recipe.preptime = form.preptime.data
        if form.cooktime:
            recipe.cooktime = form.cooktime.data
        if form. serves:
            recipe.serves = form.serves.data
        if form.notes:
            recipe.notes = form.notes.data
        if form.ingredients_string:            
            for ingredient in form.ingredients_string.data.split(','):
                seen = Ingredient.query.filter_by(name=ingredient).first()
                if seen:
                    recipe.ingredients.append(seen)
                else:
                    ingredient_obj = Ingredient(name=ingredient)
                    recipe.ingredients.append(ingredient_obj)            
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('entered'))
    return render_template('enter.html', form=form)

@app.route('/entered')
def entered():
    return render_template('entered.html')