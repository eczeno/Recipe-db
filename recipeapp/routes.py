from flask import render_template, url_for, redirect, request, session
from recipeapp import app, db
from recipeapp.forms import EntryForm, SearchIngredientsForm, EnterLinkForm
from recipeapp.models import Recipe, Ingredient, Directions
import scrape_schema_recipe
import datetime


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/search', methods=['GET','POST'])
def search():
    form = SearchIngredientsForm()
    if form.validate_on_submit():
        search_ingredients = str(form.search_string.data)
        search_ingredients_list = search_ingredients.split(',')
        recipe_objs = []
        results_list = []
        if search_ingredients_list:
            for ingredient in search_ingredients_list:
                ingredient_obj = Ingredient.query.filter_by(name=ingredient).first()
                if not ingredient_obj:
                    ingredient_obj = Ingredient(name=ingredient)
                recipe_objs.extend(ingredient_obj.recipes)            
            if recipe_objs:                
                for ingredient in search_ingredients_list:
                    ingredient_obj = Ingredient.query.filter_by(name=ingredient).first()
                    for recipe in recipe_objs:
                        recipe_ingredients = list(recipe.ingredients)
                        if ingredient_obj in recipe_ingredients:
                            results_list.append(recipe.id)
        session['results_list'] = results_list    
        return redirect(url_for('results'))
    return render_template('search.html', form=form)


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


@app.route('/enterlink', methods=['GET', 'POST'])
def enterlink():
    form = EnterLinkForm()
    if form.validate_on_submit():
        url = form.url.data
        recipe_list = scrape_schema_recipe.scrape_url(url, python_objects=True)
        if recipe_list:
            link_recipe = recipe_list[0]
            title = link_recipe['name']
            recipe = Recipe(title=link_recipe['name'])
            recipe.source = url
            recipe.preptime = link_recipe['prepTime']
            recipe.cooktime = link_recipe['cookTime']
            recipe.totaltime = link_recipe['totalTime']
            recipe.serves = link_recipe['recipeYield']
            for line in link_recipe['recipeIngredient']:
                recipe.ingredients.append(Ingredient(line=line))    
            for line in link_recipe['recipeInstructions']:
                recipe.directions.append(Directions(line=line['text']))
            db.session.add(recipe)
            db.session.commit()
            return redirect(url_for('linkentered', title=title))
    return render_template('enterlink.html', form=form)


@app.route('/linkentered/<title>')
def linkentered(title):
    return render_template('linkentered.html', title=title)


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
            new_string = ''.join(form.ingredients_string.data.split())
            new_list = new_string.split(',')
            for ingredient in new_list:
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