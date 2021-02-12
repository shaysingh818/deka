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
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        fetch = cursor.fetchall() 
        if len(fetch) == 0:
            command = "cat {}/db/client.sql | sqlite3 {}/db/{}".format(db_dir, db_dir, self.db_file)
            os.system(command) 
            print("creating database: ")
        else:
            print("Schema already generated: ")  
    
    def generate_account_key(self, service, key): 
        data = (service, key)
        sql = '''  INSERT INTO account_keys(service,key) VALUES (?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, data) 
        self.conn.commit()
        print("inserted account private key: {} ".format(key)) 
        self.conn.close()

    def generate_security_question_key(self, question, key, account_id):
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
          
"""          
myClient = Client(
    "http://deka:5000",
    "schoolStuff"
)

myClient.init_db()
myClient.check_status()
myClient.create_account("Spotify3", "Shay", "Password") 
"""
