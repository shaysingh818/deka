from cryptography.fernet import Fernet
from models import AccountKey, QuestionKey
import sqlite3
import json
import requests
import os

#this is to store the correct db file in the db child dir
db_dir = os.path.dirname(os.path.abspath(__file__))

class Client:

    def __init__(self, host_address, alias):
        self.conn = None
        self.host = host_address
        self.accounts = []
        self.questions = [] 
        self.alias = alias
        self.db_file = "{}.db".format(alias) 
        self.db_path = db_dir + "/db/{}".format(self.db_file)

    # database helper method
    def init_db(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_path) 
        except Exception as e:
            print(e)
 
    def check_status(self):
        self.init_db()
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        fetch = cursor.fetchall() 
        if len(fetch) == 0:
            command = "cat {}/db/client.sql | sqlite3 {}/db/{}".format(db_dir, db_dir, self.db_file)
            os.system(command) 
            print("creating database: ")
        else:
            print("Schema already generated: ") 
        self.conn.close()  
         
    def generate_account_key(self, service, key): 
        self.init_db()
        data = (service, key)
        sql = '''  INSERT INTO account_keys(service,key) VALUES (?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, data) 
        self.conn.commit()
        print("inserted account private key: {} ".format(key)) 
        self.conn.close()
    
    def generate_security_question_key(self, question, key, account_id): 
        self.init_db()
        data = (question,key, account_id)
        sql = '''  INSERT INTO question_keys(question,key,question_account) VALUES (?, ?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, data) 
        self.conn.commit()
        print("inserted security question key: {} ".format(key))
        self.conn.close()

    def create_account(self, service, username, password):
        params = {}
        params["service"] = service
        params["username"] = username
        params["password"] = password
        server = requests.post(self.host + "/accounts", data=params)
        data = json.loads(server.text)
        if data == "Error":
            print("Error occured: Could not create account")
        else: 
            service = data["service"] 
            key = bytes(data["key"], "utf-8")
            try:
                self.generate_account_key(service, key) 
            except sqlite3.OperationalError as  e:
                print(e)

        return True
 
    def create_question(self,question, answer, service):
        account_id_response = requests.get(self.host + "/account/{}".format(service))
        account_data = json.loads(account_id_response.text) 
        account_id = account_data["account_id"]
        params = {}
        params["question"] = question
        params["answer"] = answer   
        server = requests.post(self.host + "/account/question/" + service, data=params)
        data = json.loads(server.text) 
        if data == "Error":
            print("Error occured: Could not create question")
        else:
            service = data["service"] 
            key = bytes(data["key"], "utf-8")
            try:
                self.generate_security_question_key(question, key, account_id)
            except sqlite3.OperationalError as  e:
                print(e)

        return True 
    
    def account_key_id(self, account_service): 
        self.init_db()
        cur = self.conn.cursor()
        data = (account_service,)
        cur.execute('SELECT * FROM account_keys WHERE service=? ', data)
        result = cur.fetchone()
        account = AccountKey(result[0], result[1], result[2])
        self.conn.close()
        return account

    def delete_all_account_keys(self): 
        self.init_db() 
        cur = self.conn.cursor()
        cur.execute('DELETE FROM account_keys')
        self.conn.commit()
        self.conn.close()
        return True
 
    def delete_all_question_keys(self): 
        self.init_db() 
        cur = self.conn.cursor()
        cur.execute('DELETE FROM question_keys')
        self.conn.commit()
        self.conn.close()
        return True

"""
myClient = Client(
    "http://deka:5000",
    "schoolStuff"
)

myClient.check_status()
myClient.create_account("Spotify5", "Shay", "Password") 
#myClient.init_db()
myClient.create_question("Mothers maiden name", "mom", "Spotify5")
"""
