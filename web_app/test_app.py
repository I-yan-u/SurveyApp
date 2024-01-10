import unittest
from flask import Flask, url_for
from app import app

"""we create a class named TestApp that inherits from unittest.TestCase. Test classes in unittest inherit from TestCase to use various testing methods and assertions."""
class TestApp(unittest.TestCase):

    """define  setUp method that takes 'self' as an argument which is called before each test method is executed. It's used for setting up any necessary resources or configurations for the tests"""
    def setUp(self):
        app.config['TESTING'] = True #configures the Flask application to run in testing mode
        self.app = app.test_client() #creates a test client for the Flask application that allows user to send HTTP requests to the application during tests.

        """user can clean up any resources created during test  when we define tearDown(self) method which is called after each test method is executed."""
    def tearDown(self):
        pass

        """This is a test method for testing the behavior of the user base '/' route.
Similar explanations apply to the other test methods,  where each method tests a specific route and asserts certain conditions about the response."""
    def test_index_route(self):
        response = self.app.get('/') #This sends a GET request to the / route using the test client and captures the response.
        self.assertEqual(response.status_code, 302)  # This assertion checks if the HTTP status code in the response is equal to 302, indicating a redirect meaning we expect a redirect

    def test_login_route(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
    def test_signup_route(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_about_route(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_survey_route(self):
        response = self.app.get('/survey')
        self.assertEqual(response.status_code, 302)  # Expecting redirect without session

    def test_create_survey_route(self):
        response = self.app.get('/create_survey')
        self.assertEqual(response.status_code, 302)  # Expecting redirect without session

    def test_logout_route(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)  # Expecting redirect without session

    def test_response_route(self):
        response = self.app.get('/responses/')
        self.assertEqual(response.status_code, 302)
    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()
                      
