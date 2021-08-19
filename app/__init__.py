from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'youcantcrack@@16609jfh'

db = SQLAlchemy(app)
moment = Moment(app)
login_manager = LoginManager(app)
# login_manager.init_app(app)
# moment.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'


from app.models import User, Post, Comment



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from app import views

