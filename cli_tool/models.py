from cryptography.fernet import Fernet

class AccountKey:
    
    def __init__(self, account_id, service, key): 
        self.account_id = account_id
        self.service = service
        self.key = key
    
    def get_service(self):
        return self.service

    def get_key(self):
        return self.key
    
    def get_id(self):
        return self.account_id

    def decrypt(self, password):
        f = Fernet(self.key)
        word = f.decrypt(password)
        print(word)
 
    def dump(self):
        return {
            'id': self.account_id, 
            'service': self.service,
            'key': self.key 
        } 

        
class QuestionKey:
    
    def __init__(self, question_id, question, key, account_id):
        self.question_id = question_id
        self.question = question
        self.key = key
        self.account = account_id
    
    def get_question(self):
        return self.question

    def get_key(self):
        return self.key
 
    def get_account(self):
        return self.account

    def get_id(self):
        return self.question_id
 
    def dump(self):
        return {
            'id': self.question_id,
            'question': self.service,
            'key': self.key, 
            'account': self.account
        }     
