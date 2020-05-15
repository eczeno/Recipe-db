from flask import render_template, url_for, redirect, request, session
from recipeapp import app, db
from recipeapp.forms import EntryForm, SearchIngredientsForm
from recipeapp.models import Recipe


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
            for recipe in recipes:
                print(recipe.ingredients, recipe.title)
                if ingredient in recipe.title:
                    results_list.append(recipe.to_json())
                    print('appended to results')
        # print('resultslist =', results_list[0], type(results_list[0]))
        session['results_list'] = results_list   
    print('session =', session['results_list'], type(session['results_list']))              
    if form.validate_on_submit():
        return redirect(url_for('results'))
    return render_template('search.html', form=form, recipes=recipes)


@app.route('/results')
def results():
    print(session.get('results_list'))
    results_list = session.get('results_list')
    
    # print(results_list, type(results_list))
    return render_template('results.html', results_list=results_list)


@app.route('/enter', methods=('GET', 'POST'))
def enter():
    form = EntryForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data, ingredients=form.ingredients.data, directions=form.directions.data)
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('entered'))
    return render_template('enter.html', form=form)

@app.route('/entered')
def entered():
    return render_template('entered.html')