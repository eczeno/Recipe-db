from flask import render_template, url_for, redirect, request, session, flash
from recipeapp import app, db
from recipeapp.forms import SearchIngredientsForm, EnterLinkForm, DeleteForm, EntryForm
from recipeapp.models import Recipe, Ingredient, Directions
from collections import OrderedDict
import scrape_schema_recipe
import datetime


@app.route('/')
def home():
    recipes = Recipe.query.all()
    return render_template('home.html', recipes=recipes)


@app.route('/delete/', methods=['GET', 'POST'])
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        delete_id = form.delete_id.data
        delete_recipe = Recipe.query.filter_by(id=delete_id).first()
        if delete_recipe:
            db.session.delete(delete_recipe)
            db.session.commit()
            return redirect(url_for('deleted', delete_id=delete_id))
        flash('No recipe with that id.')
    return render_template('delete.html', form=form)


@app.route('/deleted/<delete_id>')
def deleted(delete_id):
    return render_template('deleted.html', delete_id=delete_id)


@app.route('/search', methods=['GET','POST'])
def search():
    form = SearchIngredientsForm()
    if form.validate_on_submit():
        search_ingredients_string = ''.join(form.ingredients_string.data.split(' '))
        search_ingredients_list = search_ingredients_string.split(',')
        recipe_ids = {} 
        if search_ingredients_list:
            for ingredient_name in search_ingredients_list:
                ingredient_objects = Ingredient.query.filter(Ingredient.line.like(f'%{ingredient_name}%')).all()
                if ingredient_objects:
                    for ingredient in ingredient_objects:
                        if ingredient.recipe_id not in recipe_ids.keys():
                            recipe_ids[ingredient.recipe_id] = [ingredient_name]
                        elif ingredient_name not in recipe_ids[ingredient.recipe_id]:
                            recipe_ids[ingredient.recipe_id].append(ingredient_name)
        session['recipe_ids'] = recipe_ids
        return redirect(url_for('results'))
    return render_template('search.html', form=form)


@app.route('/results')
def results():
    recipe_ids = session.get('recipe_ids')
    recipe_objects = {}
    if recipe_ids.keys():
        for recipe_id, ingredients in recipe_ids.items():
            ingredients = list(set(ingredients))
            ingredients = ', '.join(ingredients)
            recipe_objects[recipe_id] = [Recipe.query.get(recipe_id), ingredients]
    recipe_objects = OrderedDict(sorted(recipe_objects.items(), key=lambda x: len(x[1][1]), reverse=True))
    return render_template('results.html', recipe_objects=recipe_objects)


@app.route('/showrecipe/<id>', methods=['POST', 'GET'])
def showrecipe(id):
    recipe_id = id
    recipe = Recipe.query.get(recipe_id)
    return render_template('showrecipe.html', recipe=recipe)


@app.route('/manualentry/', methods=['GET', 'POST'])
def manualentry():
    form = EntryForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data)
        try:
            recipe.preptime = datetime.timedelta(minutes = form.preptime.data)
        except :
            recipe.preptime = datetime.timedelta(minutes=0)
        try:
            recipe.cooktime = datetime.timedelta(minutes = form.cooktime.data)
        except :
            recipe.cooktime = datetime.timedelta(minutes=0)            
        try:
            recipe.totaltime = datetime.timedelta(minutes = form.cooktime.data+form.preptime.data)
        except :
            recipe.totaltime = datetime.timedelta(minutes=0)
        try:
            recipe.serves = form.serves.data
        except :
            recipe.serves = 'N/A'
        ingredients_list = [x.lstrip(' ') for x in form.ingredients.data.split(',')]
        for line in ingredients_list:
            recipe.ingredients.append(Ingredient(line=line))
        directions_list = [x.strip() + '.' for x in form.directions.data.strip().split('.')][:-1]
        for line in directions_list:
            recipe.directions.append(Directions(line=line))
        db.session.add(recipe)
        db.session.commit()
        print('recipeid = ', recipe.id)
        return redirect(url_for('recipeentered', title=recipe.title, id=recipe.id))

    return render_template('manualentry.html', form=form)    


@app.route('/enterlink', methods=['GET', 'POST'])
def enterlink():
    form = EnterLinkForm()
    if form.validate_on_submit():
        url = str(form.url.data)
        if Recipe.query.filter_by(source=url).all():
            flash('That link has already been entered')
            return redirect(url_for('enterlink'))
        try:
            recipe_list = scrape_schema_recipe.scrape_url(url, python_objects=True)
        except:
            return redirect(url_for('linkfailed'))
        if recipe_list:
            link_recipe = recipe_list[0]
            try:
                recipe = Recipe(title=link_recipe['name'])
            except :
                flash('Something went wrong, try a different link')
                return redirect(url_for('enterlink'))
            recipe.source = url
            try:
                recipe.preptime = link_recipe['prepTime']
            except :
                recipe.preptime = datetime.timedelta(minutes=0)
            try:
                recipe.cooktime = link_recipe['cookTime']
            except :
                recipe.cooktime = datetime.timedelta(minutes=0)            
            try:
                recipe.totaltime = link_recipe['totalTime']
            except :
                recipe.totaltime = datetime.timedelta(minutes=0)
            try:
                recipe.serves = link_recipe['recipeYield']
            except :
                recipe.serves = 'N/A'
            try:
                for line in link_recipe['recipeIngredient']:
                    recipe.ingredients.append(Ingredient(line=line)) 
                if type(link_recipe['recipeInstructions']) is str:
                    recipe.directions.append(Directions(line=link_recipe['recipeInstructions']))
                else:   
                    for line in link_recipe['recipeInstructions']:
                        
                        try:
                            recipe.directions.append(Directions(line=line['text']))
                        except:
                            if type(line) is str:
                                recipe.directions.append(Directions(line=line))
                            else:
                                recipe.directions.append(Directions(line='Could not parse directions.'))
            except :
                flash('Something went wrong, try a different link')
                return redirect(url_for('enterlink'))
            db.session.add(recipe)
            db.session.commit()
            return redirect(url_for('recipeentered', title=recipe.title, id=recipe.id))
    return render_template('enterlink.html', form=form)


@app.route('/recipeentered/<id>-<title>')
def recipeentered(title, id):
    return render_template('recipeentered.html', title=title, id=id)


@app.route('/linkfailed')
def linkfailed():
    return render_template('linkfailed.html')