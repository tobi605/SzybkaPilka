# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField(u'Email', validators=[DataRequired()])
    password = PasswordField(u'Hasło', validators=[DataRequired()])
    submit = SubmitField(u'Zaloguj się')

class UserRegisterForm(FlaskForm):
    name = StringField(u'Imię', validators=[DataRequired()])
    surname = StringField('Nazwisko', validators=[DataRequired()])
    username = StringField('Email', validators=[DataRequired()])
    password = PasswordField(u'Hasło', validators=[DataRequired()])
    submit = SubmitField(u'Zarejestruj się')

class RefereeRegisterForm(UserRegisterForm):
    phone = StringField('Numer telefonu', validators=[DataRequired])

class PlayerRegisterForm(UserRegisterForm):
    pass
