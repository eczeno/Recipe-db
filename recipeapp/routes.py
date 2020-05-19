from flask import render_template, url_for, redirect, request, session, flash
from recipeapp import app, db
from recipeapp.forms import EntryForm, SearchIngredientsForm, EnterLinkForm, DeleteForm
from recipeapp.models import Recipe, Ingredient, Directions
from collections import OrderedDict
import scrape_schema_recipe
import datetime


@app.route('/')
def home():
    return render_template('home.html')


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

        search_ingredients_string = form.ingredients_string.data
        search_ingredients_string = ''.join(search_ingredients_string.split(' '))
        search_ingredients_list = search_ingredients_string.split(',')
        recipe_ids = {}
        

        if search_ingredients_list:
            print('searchlist =', search_ingredients_list)
            for ingredient_name in search_ingredients_list:
                print('ingname =', ingredient_name)
                ingredient_objects = Ingredient.query.filter(Ingredient.line.like(f'%{ingredient_name}%')).all()
                print('ingobjlst =', ingredient_objects)
                print('type =', type(ingredient_objects[0]), 'len =', len(ingredient_objects))
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
    print('recipeid =', recipe_id)
    recipe = Recipe.query.get(recipe_id)
    return render_template('showrecipe.html', recipe=recipe)


@app.route('/enterlink', methods=['GET', 'POST'])
def enterlink():
    form = EnterLinkForm()
    if form.validate_on_submit():
        url = str(form.url.data)
        try:
            recipe_list = scrape_schema_recipe.scrape_url(url, python_objects=True)
        except:
            return redirect(url_for('linkfailed'))
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
            print('len instructions =', len(link_recipe['recipeInstructions']), type(link_recipe['recipeInstructions']))
            if type(link_recipe['recipeInstructions']) is str:
                recipe.directions.append(Directions(line=link_recipe['recipeInstructions']))
            else:   
                for line in link_recipe['recipeInstructions']:
                    
                    try:
                        recipe.directions.append(Directions(line=line['text']))
                    except:
                        recipe.directions.append(Directions(line=line))
            db.session.add(recipe)
            db.session.commit()
            return redirect(url_for('linkentered', title=title))
    return render_template('enterlink.html', form=form)


@app.route('/linkentered/<title>')
def linkentered(title):
    return render_template('linkentered.html', title=title)


@app.route('/linkfailed')
def linkfailed():
    return render_template('linkfailed.html')


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