from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


class User(db.Model):
    """User"""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key = True)

    password = db.Column(
        db.String(100),
        nullabe = False)

    email = db.Column(
        db.String(50),
        nullable = False,
        unique = True)

    first_name = db.Column(
        db.String(30),
        nullable = False)

    last_name = db.Column(
        db.String(30),
        nullable = False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a user with hash password"""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')
        user = cls(
            username = username,
            password = hashed,
            email = email,
            first_name,
            last_name
        )

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

