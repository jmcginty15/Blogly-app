"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yeet'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

@app.route('/')
def home():
    """Displays the home page"""
    # Just redirects to users for now
    return redirect('/users')

@app.route('/users')
def users():
    """Displays all users currently in the database"""
    users = User.query.order_by('last_name', 'first_name')
    user_count = users.count()
    return render_template('users.html', users=users, user_count=user_count)

@app.route('/users/new')
def add_user():
    """Displays form to add new user"""
    return render_template('user-form.html', new=True, user=None)

@app.route('/users/new', methods=['POST'])
def process_form():
    """Processes input from add user form"""
    form_input = request.form
    if form_input['img-url'] == '':
        new_user = User(first_name=form_input['first-name'], last_name=form_input['last-name'])
    else:
        new_user = User(first_name=form_input['first-name'], last_name=form_input['last-name'], image_url=form_input['img-url'])
    db.session.add(new_user)
    db.session.commit()
    flash(f'{new_user.get_full_name()} added!')
    return redirect('/users')

@app.route('/users/<int:user_id>')
def display_user(user_id):
    """Displays details for a single user"""
    user = User.query.get(user_id)
    return render_template('single-user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Displays a form to edit a user"""
    user = User.query.get(user_id)
    return render_template('user-form.html', new=False, user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def process_edit(user_id):
    """Processes input for editing a user"""
    form_input = request.form
    user = User.query.get(user_id)
    user.first_name = form_input['first-name']
    user.last_name = form_input['last-name']
    if form_input['img-url'] == '':
        user.image_url = 'https://icon-library.com/images/default-user-icon/default-user-icon-4.jpg'
    else:
        user.image_url = form_input['img-url']
    db.session.commit()
    flash(f'{user.get_full_name()} updated!')
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Deletes a user by id"""
    user = User.query.get(user_id)
    username = user.get_full_name()
    db.session.delete(user)
    db.session.commit()
    flash(f'{username} deleted!')
    return redirect('/users')