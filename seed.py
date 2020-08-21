"""Seed file to create sample data"""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
aleks = User(first_name='Aleksandr', last_name='Solzhenitsyn', image_url='https://www.nobelprize.org/images/solzhenitsyn-13219-portrait-medium.jpg')
hector = User(first_name='Hector', last_name='of Troy', image_url='https://pbs.twimg.com/profile_images/599783028383043584/_w2fA1sS.jpg')
tom = User(first_name='Thomas', last_name='Jefferson', image_url='https://upload.wikimedia.org/wikipedia/commons/b/b1/Official_Presidential_portrait_of_Thomas_Jefferson_%28by_Rembrandt_Peale%2C_1800%29%28cropped%29.jpg')

# Add new objects to session, so they'll persist
db.session.add(aleks)
db.session.add(hector)
db.session.add(tom)

# Commit--otherwise, this never gets saved!
db.session.commit()