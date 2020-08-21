"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.String, default='https://icon-library.com/images/default-user-icon/default-user-icon-4.jpg')

    def __repr__(self):
        """Show info about user."""
        return f'<User id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}, image_url: {self.image_url}'

    def get_full_name(self):
        """Return user's full name"""
        return f'{self.first_name} {self.last_name}'
