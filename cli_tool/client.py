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

"""
#create database client
myClient = Client(
    "http://127.0.0.1:5000",
    "client1"
)

myClient.init_db()
""" 
        

