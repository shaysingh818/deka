from cryptography.fernet import Fernet
from cli_tool.models import AccountKey, QuestionKey
import sqlite3
import json
import requests
import sys 
import os

class DekaClient:

    def __init__(self, db_path, host):
        self.db_path = db_path
        self.host = host
        self.devices = []
        self.accounts = []
        self.questions = []

    def create_connection():
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)   
        except Exception as e: 
            print(e) 
        return conn

    def create_account_key(self, service, key):
        data = (service, key)
        sql = '''  INSERT INTO account_keys(service,key) VALUES (?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, data) 
        self.conn.commit()
        print("inserted private key: {} ".format(key)) 
        self.conn.close()

    def get_account_key(self, account_service):
        data = (account_service,)
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM account_keys WHERE service=?', data)
        result = cur.fetchone() 
        self.conn.close() 
        return result

    def all_account_keys(self):
        accountKeys = []
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM account_keys')   
        rows = cur.fetchall()
        for r in rows:
            a = AccountKey(r[0], r[1], r[2])
            self.accounts.append(a)

    def delete_all_account_keys(self):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM account_keys')
        self.conn.commit()
        self.conn.close()
        return True

    def create_question_key(self, question, key, account_id):
        data = (question,key, account_id)
        sql = '''  INSERT INTO question_keys(question,key,question_account) VALUES (?, ?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, data) 
        self.conn.commit()
        print("inserted private key: {} ".format(key))
        self.conn.close() 

    def all_question_keys(self):
        questionKeys = []
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM question_keys')   
        rows = cur.fetchall()
        for r in rows:
            a = QuestionKey(r[0], r[1], r[2], r[3])
            self.questions.append(a)

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


