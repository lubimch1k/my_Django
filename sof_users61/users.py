from flask import Blueprint, render_template, request
from forms import *
users_bp = Blueprint("users", __name__,
                     url_prefix="/user")
@users_bp.route("/")
def users_hp():
    return "страница юзеров"
@users_bp.route("/registration", method=["GET", "POST"])
def register():
    if request.method == "GET":
        form = RegisterForm()
        return render_template("register.html", form=form)
    elif request.method == "POST":
        # ДЗ принять информацию и сохранить
         info = request.form
         print(dict(info))
         return ("Вы успешно зарегистрированы<br>"
                "<a href='/user/login'> Войти в аккаунт </a>")
        

# ДЗ обрабатывать гет и пост и отловить всю информацию
@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "GET":
        if 'username' in session:
            return ("Вы уже вошли в аккаунт<br>"
                    "<a href='/user/logout'> Выйти из аккаунта </a>")
        return render_template("login.html", form=form)
    elif request.method == "POST":
        session["username"] = form.name.data
        info = request.form
        print(dict(info))
        return ("Вы успешно вошли в аккаунт<br>"
                "<a href='/user/logout'> Выйти из аккаунта </a>")

@users_bp.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)
