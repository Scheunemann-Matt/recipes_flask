from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
@app.route('/')
def rootRoute():
    if "flash" not in session:
        session['flash'] = ""

    return render_template('index.html')

@app.route("/dashboard")
def one_user():
    if 'user_id' not in session:
        return redirect('/')

    recipes = Recipe.get_all()

    user = {
        'id': session['user_id'],
        'name': session['user_name']
    }
    return render_template("user.html", user=user, recipes=recipes)

@app.route('/create_user', methods=['POST'])
def create_user():

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": request.form['password'],
        "confirm_password": request.form['confirm_password']
    }
    
    if (not User.validate_user(data)):
        session['flash'] = "registration"
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data['password'] = pw_hash

    user_id = User.create(data)
    session['user_id'] = user_id
    session['user_name'] = data['first_name']
    return redirect('/dashboard')

@app.route('/users/login', methods=['POST'])
def login():
    data = {
        "email": request.form['email'],
        "password": request.form['password']
    }
    is_valid = True
    user_in_db = User.get_one_from_email(data)
    print(user_in_db)
    if (not user_in_db):
        is_valid = False
    elif (not bcrypt.check_password_hash(user_in_db['password'], data['password'])):
        is_valid = False

    if (is_valid):
        session['user_id'] = user_in_db['id']
        session['user_name'] = user_in_db['first_name']
    if (not is_valid):
        flash("Ivalid email/password")
        session['flash'] = 'login'
        return redirect('/')
    return redirect('/dashboard')

@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')