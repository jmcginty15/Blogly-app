"""Seed file to create sample data"""

from models import User, Post, db
from app import app
from datetime import datetime, timezone

# Create all tables
db.drop_all()
db.create_all()

# If tables aren't empty, empty them
User.query.delete()
Post.query.delete()

# Add users
aleks = User(first_name='Aleksandr', last_name='Solzhenitsyn', image_url='https://www.nobelprize.org/images/solzhenitsyn-13219-portrait-medium.jpg')
hector = User(first_name='Hector', last_name='of Troy', image_url='https://pbs.twimg.com/profile_images/599783028383043584/_w2fA1sS.jpg')
tom = User(first_name='Thomas', last_name='Jefferson', image_url='https://upload.wikimedia.org/wikipedia/commons/b/b1/Official_Presidential_portrait_of_Thomas_Jefferson_%28by_Rembrandt_Peale%2C_1800%29%28cropped%29.jpg')

# Add user objects to session
db.session.add(aleks)
db.session.add(hector)
db.session.add(tom)

# Commit users
db.session.commit()

# Add posts
gulag = Post(title='The Gulag Archipelago', content='The Bluecaps', created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc), poster_id=1)
cancer_ward = Post(title='Cancer Ward', content='Education doesn\'t make you smarter.', created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc), poster_id=1)
stoic = Post(title='Stoicism', content='No man will hurl me down to Death, against my fate.\nAnd fate? No one has ever escaped it,\nneither brave man nor coward, I tell you--\nit\'s born with us the day that we are born.', created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc), poster_id=2)
prettyboy_paris = Post(title='Paris Is a Prettyboy', content='Look\nyour people dying around the city, the steep walls,\ndying in arms--and all for you, the battle cries\nand the fighting flaring up around the citadel.', created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc), poster_id=2)
declaration = Post(title='The Declaration of Independence', content='When in the Course of human events, it becomes necessary for one people to dissolve the political bands which have connected them with another, and to assume among the powers of the earth, the separate and equal station to which the Laws of Nature and of Nature\'s God entitle them, a decent respect to the opinions of mankind requires that they should declare the causes which impel them to the separation.', created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc), poster_id=3)
liberty = Post(title='Liberty', content='When government fears the people, there is liberty. When the people fear the government, there is tyranny.', created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc), poster_id=3)

# Add post objects to session
db.session.add(gulag)
db.session.add(cancer_ward)
db.session.add(stoic)
db.session.add(prettyboy_paris)
db.session.add(declaration)
db.session.add(liberty)

# Commit posts
db.session.commit()