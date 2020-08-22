from unittest import TestCase
from app import app
from models import db, User

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """Add sample user"""
        User.query.delete()
        user = User(first_name='Test', last_name='User')
        db.session.add(user)
        db.session.commit()
    
    @classmethod
    def tearDownClass(cls):
        db.session.rollback()

    def test_homepage(self):
        """Testing home route for status code and redirect to users page"""
        with app.test_client() as client:
            res = client.get('/')
            self.assertEqual(res.status_code, 302)
    
    def test_users(self):
        """Testing users display page"""
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)
            test_string = '<li class="list-group-item"><a href="/users/1">Test User</a></li>'

            self.assertEqual(res.status_code, 200)
            self.assertIn(test_string, html)
    
    def test_user_details(self):
        """Testing details page for user"""
        with app.test_client() as client:
            res = client.get('/users/1')
            html = res.get_data(as_text=True)
            test_string = '<h5 class="card-title">Test User</h5>'

            self.assertEqual(res.status_code, 200)
            self.assertIn(test_string, html)
    
    def test_form_new(self):
        """Testing new user form"""
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3 class="card-title">Add a new User:</h3>', html)
    
    def test_form_edit(self):
        """Testing edit user form"""
        with app.test_client() as client:
            res = client.get('/users/1/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3 class="card-title">Edit Test User:</h3>', html)