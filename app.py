import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
load_dotenv()
from models import connect_db, db, User
from forms import RegisterForm, CSRFProtectForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_notes")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ['APP_SECRET_KEY']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.get("/")
def homepage():
    """"Homepage; redirect to register """

    form = CSRFProtectForm()

    return redirect("/register")


@app.route("/register", methods = ["GET", "POST"])
def register_user():
    """Handle form submission of registering a user or produce register-form"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email,first_name,last_name)

        db.session.commit()

        session["username"] = user.username

        return redirect(f"/users/{user.username}")
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods = ["GET", "POST"])
def login_user():
    """Handle login user submission or renders login page"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Invalid username/password"]

    return render_template("login.html", form=form)

@app.get("/users/<username>")
def show_userpage(username):
    """Direct to userpage"""

    user = User.query.get_or_404(username)

    return render_template("user.html", user=user)


@app.post("/logout")
def logout_user():
    """Logout user and redirect to homepage"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect("/")
















