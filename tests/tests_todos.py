import unittest

from app import app


# test for todos
class TestTodos(unittest.TestCase):
    """
    Test about route
    """
    # setup values to launch test mode
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_todo_page_access_for_logged_in_user(self):
        """Test that a user can access the about page if they are logged in"""
        # in the view:
        with self.app:
            # send info with as post data :
            self.app.post('/todolist/', data={
                # for the user to be connected
                'email': 'keke.jamet@gmail.com',
                # todo's fields
                'content': 'TodoTest',
                'date': 'datetest',
                'degree': 'important',
                'description': 'this is a description',
                'phone_number': 'testphone_number',
                'maps': 'maps link'
            })
            # get the response
            response = self.app.get('/todolist/')
            # assert and check the status code from the about page
            self.assertEqual(response.status_code, 200)
            # get data from the about page (if logged in) and return True if "About" is mentionned in the page
            self.assertIn(b'TodoTest', response.data)


    def test_edit_todo_page_access_for_logged_in_user(self):
        """Test that a user can access the about page if they are logged in"""
        # in the view:
        with self.app:
            # send info with as post data :
            self.app.post('/login/', data={
                # for the user to be connected
                'email': 'keke.jamet@gmail.com',
                # todo's edited fields
                'content': 'edited TodoTest',
                'date': 'edited datetest',
                'degree': 'edited important',
                'description': 'edited this is a description',
                'phone_number': 'edited testphone_number',
                'maps': 'edited maps link'
            })
            # get the response
            response = self.app.get('/todolist/')
            # assert and check the status code from the about page
            self.assertEqual(response.status_code, 200)
            # get data from the about page (if logged in) and return True if "About" is mentionned in the page
            self.assertIn(b'edited TodoTest', response.data)
