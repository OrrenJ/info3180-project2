from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(max=80), Email()])
    name = StringField('Name', validators=[InputRequired(), Length(max=80)])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    age = IntegerField('Age', validators=[InputRequired()])
    gender = StringField('Gender', validators=[InputRequired()])

class LoginForm(FlaskForm):
	email = EmailField('Email', validators=[InputRequired(), Email()])
	password = PasswordField('Password', validators=[InputRequired()])