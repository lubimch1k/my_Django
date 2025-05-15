from flask import Flask
from users import users_bp
from questions import questions_bp
app = Flask(__name__)
# произвожу привязку компонента к проекту
app.register_blueprint(users_bp)
app.register_blueprint(questions_bp)
app.config["CSRF_ENABLED"] = True
app.config["SECRET_KEY"] = "ULTRA_SECRET_KEY"
@app.route("/")
def home():
    return "Домашняя страница"
app.run(debug=True)
