from app import app
from app import db
from app.models import User, Post, Comment
from flask import render_template, url_for, redirect, request, flash, abort
from app.forms import LoginForm, CommentForm, RegisterForm, PostForm
from flask_login import (
            LoginManager, login_user, 
            login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash




@app.route('/')
def index():

    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)

    return render_template('general/index.html', posts=posts)



@app.route('/post/<int:id>', methods=['POST', 'GET'])
def post(id):

    post = Post.query.get(id)

    post_comments = post.comments

    form = CommentForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        new_comment = Comment(name=name, email=email, comment=message, post=post)
        db.session.add(new_comment)
        db.session.commit() 

        return redirect(url_for('post', id=post.id))

    return render_template('general/post.html', post=post, form=form, post_comments=post_comments)



@app.route('/dashboard')
@login_required
def dashboard():

    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).all()

    return render_template('authentication/dashboard.html', posts=posts)



@app.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():

    form = PostForm()

    if form.validate_on_submit():

        new_post = Post(title=form.title.data, 
                    description=form.description.data, 
                    body=form.body.data,
                    user=current_user)

        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully')
        return redirect(url_for('dashboard'))

    return render_template('authentication/add_post.html', form=form)



@app.route('/profile')
@login_required
def profile():

    user = User.query.get_or_404(current_user.id)

    if user is None:
        abort(404)

    return render_template('authentication/profile.html', user=user)



@app.route('/edit_post/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_post(id):

    post = Post.query.get_or_404(id)

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('Post updated successfully')
        return redirect(url_for('dashboard'))

    form.title.data = post.title
    form.description.data = post.description
    form.body.data = post.body

    return render_template('authentication/edit_post.html', form=form)



@app.route('/confirm/<int:id>')
@login_required
def confirm(id):

    post  = Post.query.get_or_404(id)

    return render_template('authentication/confirm_delete.html', post=post)




@app.route('/confirm/delete/<int:id>')
@login_required
def delete(id):

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully')
    return redirect(url_for('dashboard'))



@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('dashboard')
        flash('Invalid email or password')
    return render_template('general/login.html', form=form)



@app.route('/register', methods=['POST', 'GET'])
def register():
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password1 = form.password1.data

        new_user = User(username=username, 
                email=email, 
                password=generate_password_hash(password1))

        db.session.add(new_user)
        db.session.commit()
        flash(f'Welcome {new_user} your account has been created successfully')
        return redirect('/login')


    return render_template('general/register.html', form=form)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))





@app.route('/post_view/<int:id>')
@login_required
def post_view(id):

    post = Post.query.get_or_404(id)

    return render_template('authentication/post_view.html', post=post)




@app.route('/about')
def about():
    return render_template('general/about.html')