from cryptography.fernet import Fernet

class Account:
    def __init__(self, account_id, service, username, password):
        self.account_id = account_id
        self.service = service
        self.username = username
        self.password = password

    def get_service(self):
        return self.service

    def get_user(self):
        return self.username

    def get_pass(self): 
        return self.password
    
    def set_pass(self, setPass):
        self.password = setPass

    def get_id(self):
        return self.account_id

    def dump(self):
        return {
            'account_id': self.account_id,
            'password': str(self.password),
            'username' : self.username, 
            'service': self.service 
        }

class Question:

    def __init__(self,question_id, question, answer, account_id):
        self.question_id = question_id
        self.question = question
        self.answer = answer
        self.account_id = account_id

    def get_question_id(self):
        return self.question_id

    def get_question(self):
        return self.question
    
    def get_answer(self):
        return self.answer    

    def get_account_id(self):
        return self.account_id

    def set_question(self, setquestion):
        self.question = setquestion
    
    def set_answer(self, setanswer):
        self.answer = setanswer
    
    def set_account_id(self, setaccountid):
        self.accounti_id = setaccountid
    
    def dump(self):
        return {
            'question_id': self.question_id, 
            'question': self.question,
            'answer' : self.answer,
            'account_id': self.account_id
        }

class Contact:

    def __init__(self, contact_id, name, phone, email):
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def set_name(self, setname):
        self.name = setname
     
    def set_phone(self, setphone):
        self.phone = setphone
 
    def get_email(self, setemail):
        self.email = setemail

    def get_name(self):
        return self.name
     
    def get_phone(self):
        return self.phone
 
    def get_email(self):
        return self.email
 
    def dump(self):
        return {
            'contact_id': self.contact_id,
            'password': str(self.password),
            'username' : self.username, 
            'service': self.service 
        }

class Log:

    def __init__(self, log_id, ip_address, user_agent, mac_addr):
        self.log_id = log_id
        self.ip_address = ip_address
        self.agent = user_agent
        self.mac_addr = mac_addr

    def dump(self):
        return {
            'log_id' : self.log_id,
            'ip_address': self.ip_address,
            'user_agent': self.agent,
            'mac_addr': self.mac_addr
        }

