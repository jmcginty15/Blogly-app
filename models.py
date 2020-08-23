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
    posts = db.relationship('Post', order_by='desc(Post.updated_at)', cascade='all, delete-orphan')

    def __repr__(self):
        """Show info about user."""
        return f'<User id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}, image_url: {self.image_url}'

    def get_full_name(self):
        """Return user's full name"""
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    """Post"""

    __tablename__ = 'Posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    poster_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    poster = db.relationship('User')

    def __repr__(self):
        """Show info about post."""
        return f'<Post id: {self.id}, title: {self.title}, content: {self.content}, created_at: {self.created_at}, updated_at: {self.updated_at}, poster_id: {self.poster_id}>'

    def format_date(self, attr):
        """Format date into a convenient human-readable format."""
        months = {1: 'January',
                  2: 'February',
                  3: 'March',
                  4: 'April',
                  5: 'May',
                  6: 'June',
                  7: 'July',
                  8: 'August',
                  9: 'September',
                  10: 'October',
                  11: 'November',
                  12: 'December'}

        if attr == 'created':
            time_obj = self.created_at
        elif attr == 'updated':
            time_obj = self.updated_at
        
        minute = str(time_obj.minute)
        hour = time_obj.hour
        day = time_obj.day
        month = months[time_obj.month]
        year = time_obj.year

        if len(minute) == 1:
            minute = f'0{minute}'

        if hour < 12:
            am_pm = 'AM'
        else:
            am_pm = 'PM'
            hour -= 12

        return f'{month} {day}, {year}, {hour}:{minute} {am_pm}'