from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from datetime import date


@app.route('/recipes/<int:id>')
def show_recipe(id):
    if ('user_id' not in session):
        return redirect('/')
    id = { 'id':id }
    recipe = Recipe.get_one(id)
    if (not recipe):
        return redirect('/dashboard')
    user = {
        'id': session['user_id'],
        'name': session['user_name']
    }
    return render_template('recipe.html', user = user, recipe = recipe)

@app.route('/recipes/new')
def new_recipe():
    if ('user_id' not in session):
        return redirect('/')

    today = date.today()
    user = {
        'id': session['user_id'],
        'name': session['user_name']
    }
    return render_template('new_recipe.html', today = today, user = user)

@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    if ('user_id' not in session):
        return redirect('/')
    if (not Recipe.validate_recipe(request.form)):
        return redirect('/recipes/new')

    print(request.form)
    
    data = {
        'title' : request.form['title'],
        'under30' : request.form['under30'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'user_id' : session['user_id']
    }
    id = Recipe.create(data)
    print(id)

    return redirect(f'/recipes/{id}')

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if ('user_id' not in session):
        return redirect('/')

    id = { 'id':id }
    recipe = Recipe.get_one(id)
    if (not recipe or session['user_id'] != recipe.user_id):
        return redirect('/dashboard')

    user = {
        'id': session['user_id'],
        'name': session['user_name']
    }
    today = date.today()
    return render_template('edit_recipe.html', today = today, user = user, recipe = recipe)

@app.route('/edit_recipe', methods=['POST'])
def update_recipe():
    if ('user_id' not in session):
        return redirect('/')
    if (not Recipe.validate_recipe(request.form)):
        return redirect(f'/recipes/edit/{request.form["id"]}')
    
    print(request.form)
    
    data = {
        'id' : request.form['id'],
        'title' : request.form['title'],
        'under30' : request.form['under30'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'user_id' : session['user_id']
    }
    Recipe.update(data)

    return redirect(f'/recipes/{request.form["id"]}')

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    if ('user_id' not in session):
        return redirect('/')

    id = {'id':id}
    Recipe.delete(id)

    return redirect('/dashboard')