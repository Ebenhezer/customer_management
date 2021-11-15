import unittest
import urllib.request
from flask_testing import TestCase
from flask import Flask
import requests
import json

from utils import utilities
# from utilities.dbUtils import dbUtilities

# dbUtils = dbUtilities()
utils = utilities()
server = "http://127.0.0.1:8000/"
test_results = utils.test_results_file
class sensorTests(TestCase):
    render_templates = False

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 8000
        # Default timeout is 5 seconds
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def test_server_is_up_and_running(self):
        response = urllib.request.urlopen(server)
        self.assertEqual(response.code, 200)
    
    def test_a_login_page(self):
        utils.logMessage(" # Testing test_login_page")
        response = requests.get(server+'login')
        assert b"Create new user account" in response.content
        utils.logger("Pass");
        return True

    def test_b_login_failed(self):
        utils.logMessage(" # Testing test_login_failed")
        # Use wrong username and password
        data = ({'username': "ebby@ebby.co.za",
                 'password': 2222})

        response = requests.post(server+'login', data=data)
        assert b"Incorrect username/password" in response.content
        utils.logger("Pass");
        return True

    def test_c_login_pass(self):
        utils.logMessage(" # Testing test_login_pass")
        # Use correct username and password
        data = ({'username': "ebby@ebby.co.za",
                 'password': 12345})
        response = requests.post(server+'login', data=data)
        assert b"Hello," in response.content
        utils.logger("Pass");
        return True

    def test_d_logout(self):
        utils.logMessage(" # Testing test_logout")
        response = requests.post(server+'logout')
        assert b"Logged out" in response.content
        utils.logger("Pass");
        return True
          
    def test_z_signUpFailedUserExists(self):
        # Testing the sign up functionality
        
        test_status = True
    
   


if __name__ == "__main__":
    tests_class = sensorTests()
    utils.logMessage(" ************************ Starting the test ************************")

    
    # Run the tests
    unittest.main(verbosity=2) 