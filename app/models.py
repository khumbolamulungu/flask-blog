from app import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20))
    fullname = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(255), unique=True)
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    password = db.Column(db.String())
    posts = db.relationship('Post', backref='user', lazy='dynamic')


    def __repr__(self):
        return f'{self.username}'



class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String(255))
    body = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return f'{self.title}'



class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(255))
    comment = db.Column(db.Text)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return f'{self.name} said {self.comment}'