from unittest import TestCase
from app import app
from models import db, User, Post
from datetime import datetime, timezone

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """Add sample user and posts"""
        User.query.delete()
        user = User(first_name='Test', last_name='User')
        db.session.add(user)
        db.session.commit()
        post_1 = Post(title='Test1', content='Lorem ipsum', created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc), poster_id=1)
        post_2 = Post(title='Test2', content='Lorem ipsum', created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc), poster_id=1)
        db.session.add(post_1)
        db.session.add(post_2)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.session.rollback()

    def test_homepage(self):
        """Testing home route for status code and post content"""
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h5 class="card-title"><a href="/posts/1">Test1</a></h5>', html)
    
    def test_users(self):
        """Testing users display page"""
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)
            test_string = '<a href="/users/1">Test User</a>'
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
    
    def test_z_post_deletes(self):
        """Testing delete post functionality"""
        with app.test_client() as client:
            res = client.post('/posts/1/delete/home', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertNotIn('<a href="/posts/1">Test1</a>', html)
            self.assertIn('<h1 class="card-title" id="page-title">Blogly Home</h1>', html)

            res = client.post('/posts/2/delete/post', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<div class="alert alert-success" role="alert">Test2 deleted!</div>', html)
    
    def test_z_user_delete(self):
        """Testing delete user functionality"""
        with app.test_client() as client:
            res = client.post('/users/1/delete', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertNotIn('<a href="/users/1">Test User</a>', html)