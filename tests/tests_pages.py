import unittest

from app import app


# test to access html pages
class TestPages(unittest.TestCase):
    """
    Test about route
    """
    # setup values to launch test mode
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    # test to access the register page
    def test_register_page(self):
        """Test that a user can access the about page if they are logged in"""
        # in the view:
        with self.app:
            # get the response
            response = self.app.get('/register/')
            # assert and check the status code from the about page
            self.assertEqual(response.status_code, 200)
            # get data from the about page (if logged in) and return True if "About" is mentionned in the page
            self.assertIn(b'ToDoApp', response.data)


    # test to access the login page
    def test_login_page(self):
        """Test that a user can access the about page if they are logged in"""
        # in the view:
        with self.app:
            # get the response
            response = self.app.get('/login/')
            # assert and check the status code from the about page
            self.assertEqual(response.status_code, 200)
            # get data from the about page (if logged in) and return True if "About" is mentionned in the page
            self.assertIn(b'ToDoApp', response.data)

    # test to access the logged_in page
    def test_loggedin_page(self):
        """Test that a user can access the about page if they are logged in"""
        # in the view:
        with self.app:
            # send user info as post data
            self.app.post('/login/', data={
                'email': 'keke.jamet@gmail.com',
                'password': 'kevin18'
            })
            # get the response
            response = self.app.get('/logged_in/')
            # assert and check the status code from the about page
            self.assertEqual(response.status_code, 200)
            # get data from the about page (if logged in) and return True if "About" is mentionned in the page
            self.assertIn(b'ToDoApp', response.data)

    # test to access the main page
    def test_main_page(self):
        """Test that a user can access the about page if they are logged in"""
        # in the view:
        with self.app:
            # send user info as post data
            self.app.post('/login/', data={
                'email': 'test.username@mail.com',
                'password': 'testpw2023'
            })
            # get the response
            response = self.app.get('/')
            # assert and check the status code from the about page
            self.assertEqual(response.status_code, 200)
            # get data from the about page (if logged in) and return True if "About" is mentionned in the page
            self.assertIn(b'ToDoApp', response.data)