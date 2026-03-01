from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import psutil

app = Flask(__name__)
app.secret_key = "clave_super_secreta"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Usuario de prueba
users = {
    "admin": generate_password_hash("1234")
}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and check_password_hash(users[username], password):
            user = User(username)
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return "Credenciales incorrectas"

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent

    alert = None
    if cpu > 80:
        alert = "⚠ Alto uso de CPU"

    return render_template("dashboard.html", cpu=cpu, memory=memory, alert=alert)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)