import requests
import unittest

class TestServerMethods(unittest.TestCase):
 
    def test_create_accounts(self):

        params = {
            "service": "test_service",
            "username": "test_username",
            "password": "test_password" 
        }

        server_request = requests.post('http://deka:5000/accounts', data=params) 
        self.assertEqual(200, server_request.status_code)

        server_request1 = requests.get('http://deka:5000/account/test_service') 
        self.assertEqual(200, server_request1.status_code)
    
        server_request2 = requests.get('http://deka:5000/accounts') 
        self.assertEqual(200, server_request2.status_code)

        params_2 = {
            "question": "This is a test question",
            "answer": "test_answer"
        }
    
        server_request3 = requests.post('http://deka:5000/account/question/test_service', data=params_2) 
        self.assertEqual(200, server_request3.status_code)
    
        server_request4 = requests.delete('http://deka:5000/accounts') 
        self.assertEqual(200, server_request4.status_code)
    
        server_request5 = requests.get('http://deka:5000/log') 
        self.assertEqual(200, server_request4.status_code)
        
 
if __name__ == '__main__':
    unittest.main() 
