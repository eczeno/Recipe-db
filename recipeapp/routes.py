from flask import render_template, url_for, redirect
from recipeapp import app, db
from recipeapp.forms import EntryForm
from recipeapp.models import Recipe

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search')
def search():
    return render_template('search.html')


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