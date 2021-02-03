from cryptography.fernet import Fernet
from cli_tool.models import AccountKey, QuestionKey
import sqlite3
import json
import requests
import os

db_dir = os.path.dirname(os.path.abspath(__file__))
client_db = db_dir + "/db/client.db" 

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(client_db)   
    except Exception as e: 
        print(e) 
    return conn


class AccountKeys:

    def __init__(self):
        self.conn = create_connection()
 
    def create(self, service, key):
        data = (service, key)
        sql = '''  INSERT INTO account_keys(service,key) VALUES (?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, data) 
        self.conn.commit()
        print("inserted private key: {} ".format(key)) 
        self.conn.close()
    
    def get(self, account_service):
        data = (account_service,)
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM account_keys WHERE service=?', data)
        result = cur.fetchone() 
        self.conn.close() 
        return result

    def all(self):
        accountKeys = []
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM account_keys')   
        rows = cur.fetchall()
        for r in rows:
            a = AccountKey(r[0], r[1], r[2])
            accountKeys.append(a)
        return accountKeys

    def detail(self, account_service):
        cur = self.conn.cursor()
        data = (account_service,)
        cur.execute('SELECT * FROM account_keys WHERE service=? ', data)
        result = cur.fetchone()
        account = AccountKey(result[1], result[2])
        return account

    def by_id(self, account_service): 
        cur = self.conn.cursor()
        data = (account_service,)
        cur.execute('SELECT * FROM account_keys WHERE service=? ', data)
        result = cur.fetchone()
        account = AccountKey(result[1], result[2])
        self.conn.close()
        #return account
        

    def delete_all(self):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM account_keys')
        self.conn.commit()
        self.conn.close()
        return True


class QuestionKeys:

    def __init__(self):
        self.conn = create_connection()

    def create(self, question, key, account_id):
        data = (question,key, account_id)
        sql = '''  INSERT INTO question_keys(question,key,question_account) VALUES (?, ?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, data) 
        self.conn.commit()
        print("inserted private key: {} ".format(key))
        self.conn.close() 

    def all(self):
        questionKeys = []
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM question_keys')   
        rows = cur.fetchall()
        for r in rows:
            a = QuestionKey(r[0], r[1], r[2], r[3])
            questionKeys.append(a)
        return questionKeys

    def detail(self, question_id):
        cur = self.conn.cursor()
        data = (question_id,)
        cur.execute('SELECT * FROM question_keys WHERE question_id=? ', data)
        result = cur.fetchone()
        account = AccountKey(result[1], result[2])
        return account
 
    def delete_all(self):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM question_keys')
        self.conn.commit()
        self.conn.close()
        return True

