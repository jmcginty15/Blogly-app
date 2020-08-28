"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, Markup
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from datetime import datetime, timezone

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
    """Displays the home page with the 5 most recently updated posts"""
    posts = Post.query.order_by(Post.updated_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)

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
    posts = Post.query.filter_by(poster_id=user_id)
    post_count = posts.count()
    return render_template('single-user.html', user=user, posts=posts, post_count=post_count)

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

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Shows a single post by id"""
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Displays a form to edit a post"""
    post = Post.query.get(post_id)
    user = post.poster
    tags = Tag.query.all()
    return render_template('post-form.html', new=False, post=post, user=user, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def process_post_edit(post_id):
    """Processes input for editing a post"""
    form_input = request.form
    post = Post.query.get(post_id)
    post.title = form_input['title']
    post.content = form_input['content']
    post.updated_at = datetime.now(timezone.utc)
    tags = Tag.query.all()
    for tag in tags:
        try:
            post.tags.remove(tag)
        except:
            pass
        if form_input.get(tag.name):
            post.tags.append(tag)
    db.session.commit()
    flash(f'{post.title} updated!')
    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete/<page>', methods=['POST'])
def delete_post(post_id, page):
    """Deletes a post by id"""
    post = Post.query.get(post_id)
    user = post.poster
    title = post.title
    db.session.delete(post)
    db.session.commit()
    flash(f'{title} deleted!')
    if page == 'home':
        return redirect('/')
    elif page == 'post':
        return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """Displays form for adding a new post"""
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template('post-form.html', new=True, post=None, user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def process_new_post(user_id):
    """Processes form input for new post"""
    form_input = request.form
    user = User.query.get(user_id)
    new_post = Post(title=form_input['title'], content=form_input['content'], created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc), poster_id=user_id)
    tags = Tag.query.all()
    for tag in tags:
        if form_input.get(tag.name):
            new_post.tags.append(tag)
    db.session.add(new_post)
    db.session.commit()
    flash(f'{new_post.title} added!')
    return redirect(f'/users/{user_id}')

@app.route('/tags')
def tags():
    """Shows a list of all existing tags"""
    tags = Tag.query.order_by('name').all()
    tag_count = len(tags)
    return render_template('tags.html', tags=tags, tag_count=tag_count)

@app.route('/tags/<int:tag_id>')
def tag(tag_id):
    """Shows details for a single tag"""
    tag = Tag.query.get(tag_id)
    post_count = len(tag.posts)
    return render_template('single-tag.html', tag=tag, post_count=post_count)

@app.route('/tags/new')
def add_tag():
    """Displays form to add a new tag"""
    posts = Post.query.all()
    return render_template('tag-form.html', new=True, tag=None, posts=posts)

@app.route('/tags/new', methods=['POST'])
def process_new_tag():
    """Processes form input for new tag"""
    form_input = request.form
    tag_name = form_input['name']
    new_tag = Tag(name=tag_name)
    posts = Post.query.all()
    for post in posts:
        if form_input.get(post.title):
            new_tag.posts.append(post)
    db.session.add(new_tag)
    db.session.commit()
    flash_msg = Markup(f'<span class="badge badge-primary">{tag_name}</span> added!')
    flash(flash_msg)
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Deletes a tag by id"""
    tag = Tag.query.get(tag_id)
    tag_name = tag.name
    db.session.delete(tag)
    db.session.commit()
    flash_msg = Markup(f'<span class="badge badge-primary">{tag_name}</span> deleted!')
    flash(flash_msg)
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Displays a form for editing a tag name"""
    tag = Tag.query.get(tag_id)
    posts = Post.query.all()
    return render_template('tag-form.html', new=False, tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def process_tag_edit(tag_id):
    """Process form input for editing a tag name"""
    form_input = request.form
    tag_name = form_input['name']
    tag = Tag.query.get(tag_id)
    tag.name = tag_name
    posts = Post.query.all()
    for post in posts:
        try:
            tag.posts.remove(post)
        except:
            pass
        if form_input.get(post.title):
            tag.posts.append(post)
    db.session.commit()
    flash_msg = Markup(f'<span class="badge badge-primary">{tag_name}</span> updated!')
    flash(flash_msg)
    return redirect('/tags')