# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('email', validators=[DataRequired()])
    password = PasswordField('haslo', validators=[DataRequired()])
    submit = SubmitField('Zaloguj sie')

class UserRegisterForm(FlaskForm):
    name = StringField('imie', validators=[DataRequired()])
    surname = StringField('nazwisko', validators=[DataRequired()])
    username = StringField('email', validators=[DataRequired()])
    password = PasswordField('haslo', validators=[DataRequired()])
    submit = SubmitField('Zarejestruj sie')

class RefereeRegisterForm(UserRegisterForm):
    phone = StringField('numer telefonu', validators=[DataRequired])

class PlayerRegisterForm(UserRegisterForm):
    pass
