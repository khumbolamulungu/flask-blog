from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, ValidationError
from wtforms.validators import Email, DataRequired, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(message='This is an invalid email')])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=12)])
    password2 = PasswordField('Confirm Password', validators=[EqualTo('password1', message='The two password fields did not match'), DataRequired()])

    # custom validation here
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already in use, provide another one')


    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered')


    


class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(message='This is an invalid email')])
    message = TextAreaField('Message', validators=[DataRequired()])




class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='Provide title please')])
    description = StringField('Description', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
