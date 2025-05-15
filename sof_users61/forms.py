from flask_wtf import FlaskForm
from wtforms import (StringField, EmailField,
                     PasswordField, SubmitField)
from wtforms.validators import DataRequired, Length, EqualTo
class RegisterForm(FlaskForm):
    name = StringField(label="Имя", validators=[DataRequired("Напишите свое имя"),
                                                Length(min=2, max=16)])
    email = EmailField(label="Почта", validators=[DataRequired("Напишите email")])
    password1 = PasswordField(label="Придумайте пароль",
                              validators=[DataRequired("Напишите пароль")])

    password2 = PasswordField(label="Повторите пароль",
                              validators=[DataRequired("Повторите пароль"),
                                          EqualTo("password1", message="Пароли не совпадают")])
    button = SubmitField(label="Зарегистрироваться")
class LoginForm(FlaskForm):
    email = EmailField(label="Почта", validators=[DataRequired("Напишите email")])
    password = PasswordField(label="Введите пароль",
                              validators=[DataRequired("Напишите пароль")])
    button = SubmitField(label="Войти")