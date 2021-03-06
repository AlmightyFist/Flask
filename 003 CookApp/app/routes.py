from app import app, bcrypt, db
from flask import render_template, url_for, flash, redirect, request
from app.models import User, Receipe, Ingredient, Comment
from app.forms import RegistrationForm, LoginForm, ReceipeForm, CommentForm, IngredientForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home", methods=['POST','GET'])
def home():

    page = request.args.get('page', 1, type=int)
    ingredients = Ingredient.query.order_by(Ingredient.name)

    ing_list = request.form.getlist('ingredients')

    if ing_list:

        q = db.session.query(Receipe)

        for ing in ing_list:
            q = q.filter(Receipe.ingredients.any(Ingredient.id == ing))

        receipess = q.paginate(page=page, per_page=5)

        return render_template('home.html', receipess=receipess, ingredients=ingredients)

    else:

        receipess = Receipe.query.order_by(Receipe.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('home.html', receipess=receipess, ingredients=ingredients)

"""@app.route("/home_filter/<int:ing_id>")
def home_filter(ing_id):

    ingredient = Ingredient.query.filter(Ingredient.id == ing_id)
    receipess = Receipe.query.filter(Receipe.ingredients.like(ingredient))

    return render_template('home.html', receipess=receipess)"""

@app.route("/about")
def about():

    rec = Receipe.query.filter_by(title='aa').first()

    return render_template('about.html', rec=rec)

@app.route("/login", methods=['POST','GET'])
def login():

    # Jeżeli użytkownik jest zalogowany
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home')) #możliwość przekierowania do adresy, do którego próbowano sie dostać przed zalogowaniem
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', form=form)

@app.route("/register", methods=['POST','GET'])
def register():

    #Jeżeli użytkownik jest zalogowany
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()


    #Jeżeli formularz został wypełniony prawidłowo
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html',form=form)

@app.route("/logout")
def logout():

    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route("/account/<int:user_id>")
def account(user_id):
    user = User.query.get(user_id)
    receipes = Receipe.query.with_parent(user).count()
    comments = Comment.query.with_parent(user).count()
    if user == current_user:
        return render_template('my_account.html', user=user,receipes = receipes, comments = comments)
    elif user != current_user:
        return render_template('account.html', user=user, receipes= receipes, comments=comments)

@app.route("/new_receipe",methods=['POST','GET'])
@login_required
def new_receipe():
    form = ReceipeForm()
    ingredients = Ingredient.query.order_by(Ingredient.name)
    if form.validate_on_submit():
        receipe = Receipe(title = form.title.data, content=form.content.data, author=current_user)
        db.session.add(receipe)
        db.session.commit()

        ing_list = request.form.getlist('ingredients')
        for ing in ing_list:
            ingredient = Ingredient.query.filter_by(name = ing).first()
            ingredient.receipess.append(receipe)
            db.session.commit()
            flash('Your receipe has been added!', 'success')

        return redirect(url_for('home'))

    return render_template('new_receipe.html', form=form, ingredients=ingredients)

@app.route("/receipe/<int:receipe_id>")
def receipe(receipe_id):
    receipe = Receipe.query.get(receipe_id)
    return render_template("receipe.html",receipe=receipe)

@app.route("/add_comment/<int:receipe_id>",methods=['POST','GET'])
def add_comment(receipe_id):
    receipe = Receipe.query.get(receipe_id)
    receipe_id = receipe_id
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content = form.content.data, receipe_id=receipe_id, user_id = receipe.author.id)
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('receipe', receipe_id=receipe_id))
    return render_template('add_comment.html', form = form, receipe=receipe)

@app.route("/add_ingredient", methods=['POST', 'GET'])
@login_required
def add_ing():


    form = IngredientForm()
    ingredients = Ingredient.query.order_by(Ingredient.name)

    if form.validate_on_submit():
        ingredient = Ingredient(name = form.name.data, user_id = current_user.id)
        db.session.add(ingredient)
        db.session.commit()

        ingredients = Ingredient.query.all()

        return render_template('add_ing.html', form=form, ingredients=ingredients)

    return render_template('add_ing.html', form=form, ingredients=ingredients)






