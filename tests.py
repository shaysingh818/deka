import unittest
import cli_tool as cli
from cli_tool.database import AccountKeys, QuestionKeys
import requests

class TestClientMethods(unittest.TestCase):

    def test_cli(self): 
        self.assertTrue(cli.create_account("chase", "username", "password")) 
        self.assertTrue(cli.view_keys())
        self.assertTrue(cli.decrypt_all())
        self.assertTrue(cli.decrypt_one("chase"))
        self.assertTrue(cli.delete_accounts()) 
        accounts = AccountKeys()
        self.assertTrue(accounts.delete_all())
    
""" 
class TestServerMethods(unittest.TestCase):

    def test_accounts(self):
        server_request = requests.get('http://deka:5000/accounts') 
        self.assertEqual(200, server_request.status_code)
 
    def test_create_accounts(self):

        params = {
            "service": "test_service",
            "username": "test_username",
            "password": "test_password" 
        }

        server_request = requests.post('http://deka:5000/accounts', data=params) 
        self.assertEqual(200, server_request.status_code) 
    
    def test__delete_accounts(self):
        server_request = requests.delete('http://deka:5000/accounts') 
        self.assertEqual(200, server_request.status_code) 
""" 
if __name__ == '__main__':
    unittest.main() 
