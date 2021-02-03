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
    
if __name__ == '__main__':
    unittest.main() 
