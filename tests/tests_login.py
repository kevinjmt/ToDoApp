import unittest

from app import app


# test to log in and access pages as a logged in/out user
class TestLogin(unittest.TestCase):
    """
    Test about route
    """
    # setup values to launch test mode
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    # test to access the login page
    def test_about_page_access_for_logged_in_user(self):
        """Test that a user can access the about page if they are logged in"""
        # in the view:
        with self.app:
            # send info with as post data :
            self.app.post('/login/', data={
                'email': 'test.username@mail.com',
                'password': 'testpw2023'
            })
            # get the response
            response = self.app.get('/about/')
            # assert and check the status code from the about page
            self.assertEqual(response.status_code, 200)
            # get data from the about page (if logged in) and return True if "About" is mentionned in the page
            self.assertIn(b'About', response.data)

    # test to register user
    def test_register_user(self):
        """Test that a user can access the about page if they are logged in"""
        # in the view:
        with self.app:
            # send info with as post data :
            self.app.post('/register/', data={
                'fullname': 'testUser',
                'email': 'test.username@mail.com',
                'password1': 'testpw2023',
                'password2': 'testpw2023'
            })
            # get the response
            response = self.app.get('/logged_in/')
            # assert and check the status code from the about page
            self.assertEqual(response.status_code, 200)
            # get data from the logged_in page (if logged in) and return True if "Hello You are Logged in" is mentionned in the page
            self.assertIn(b'Hello You are Logged in', response.data)

    # test to log out user
    def test_about_page_access_for_logged_out_user(self):
        """Test that a user is redirected to the login page if they are not logged in"""
        # in the view:
        with self.app:
            # get the response
            response = self.app.get('/about/')
            # assert and check the status code from the about page
            self.assertEqual(response.status_code, 302)
            # get data from the logged_in page (if logged in) and return True if "Hello You are Logged in" is mentionned in the page
            self.assertIn(b'/login/', response.data)