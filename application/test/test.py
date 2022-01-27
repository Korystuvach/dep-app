from .. import routes
from .. import app
import unittest


class FlaskTestCase(unittest.TestCase):
    # Add path
    url = 'http://127.0.0.1:5000'

    # GET request to Home page, return code 200 and html
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get(self.url + '/index')
        self.assertEqual(response.status_code, 200)

    # GET request to login page, return code 200 and html
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get(self.url + '/login')
        self.assertEqual(response.status_code, 200)

    # Logout request, redirect to homepage
    def test_logout_redirect(self):
        tester = app.test_client(self)
        response = tester.get(self.url + '/logout')
        self.assertEqual(response.status_code, 302)

    def test_departments(self):
        tester = app.test_client(self)
        resource = tester.get(self.url + '/departments')
        self.assertEqual(resource.status_code, 200)


if __name__ == '__main__':
    # Run tests
    unittest.main()
