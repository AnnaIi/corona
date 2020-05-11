from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, PasswordField, StringField
from flask_wtf.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    address = StringField('Адрес пользователя', validators=[DataRequired()])
    chatname = StringField('Имя в чате', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')