from cryptography.fernet import Fernet
from models import Account, Question, Log
import sqlite3
import json
import netifaces as nif

DB_FILE = 'db/server.db' 

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE) 
    except error as e: 
        print(e) 
    return conn


def mac_for_ip(ip):
    for i in nif.interfaces():
        addrs = nif.ifaddresses(i)
        try:
            if_mac = addrs[nif.AF_LINK][0]['addr']
            if_ip = addrs[nif.AF_INET][0]['addr']
        except (IndexError, KeyError): #ignore ifaces that dont have MAC or IP
            if_mac = if_ip = None
        if if_ip == ip:
            return if_mac
    return None

class Accounts:

    def __init__(self):
        self.conn = create_connection()
    
    def encrypt_and_create(self, service, user, password):
        key = Fernet.generate_key()
        f = Fernet(key)
        token = f.encrypt(bytes(password, 'utf-8'))
        password_test = token.decode('utf-8')
        try:
            data = (service, user, password_test)
            sql = '''  INSERT INTO accounts(service,username, password) VALUES (?, ?, ?) '''
            cur = self.conn.cursor()
            cur.execute(sql, data) 
            self.conn.commit()
            print("inserted account ")
            self.conn.close() 
        except sqlite3.Error as e:
            self.conn.close()
            print(e) 
            return False
        return (service, key)

    def all(self):
        accounts = []
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM accounts')   
        rows = cur.fetchall()
        for r in rows:
            a = Account(r[0],r[1], r[2], r[3])
            accounts.append(a)
        self.conn.close() 
        return accounts

    def get(self, account_service):
        data = (account_service,)
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM accounts WHERE service=?', data)
        result = cur.fetchone() 
        self.conn.close() 
        return result[0]

    def detail(self, account_service):
        cur = self.conn.cursor()
        data = (account_service,)
        cur.execute('SELECT * FROM accounts WHERE service=? ', data)
        result = cur.fetchone() 
        account = Account(result[0],result[1], result[2], result[3])  
        self.conn.close() 
        return account

    def delete_all(self):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM accounts') 
        self.conn.commit()  
        self.conn.close()

class Questions:

    def __init__(self):
        self.conn = create_connection()

    def encrypt_and_create(self, question, answer, service):
        key = Fernet.generate_key()
        f = Fernet(key)
        token = f.encrypt(bytes(answer, 'utf-8'))
        try:
            acc = Accounts()
            account_id = acc.get(service)
            data = (question, token, account_id)
            sql = '''  INSERT INTO account_security_questions(question, answer, question_account) VALUES (?, ?, ?) '''
            cur = self.conn.cursor()
            cur.execute(sql, data) 
            self.conn.commit()
            print("inserted account ")
            self.conn.close() 
        except sqlite3.Error as e:
            self.conn.close()
            print(e) 
            return False
        return (service, key)
    
    def by_service(self, account_id):
        questions = []
        cur = self.conn.cursor()
        data = (account_id,)
        cur.execute('SELECT * FROM account_security_questions WHERE question_account=?', data)  
        rows = cur.fetchall()
        for r in rows:
            q = Question(r[0], r[1], r[2], r[3])
            print(r[0])
            questions.append(q) 
        self.conn.close()
        return questions
 
    def all(self):
        questions = []
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM account_security_questions')     
        rows = cur.fetchall()
        for r in rows:
            q = Question(r[0], r[1],r[2], r[3])
            questions.append(a) 
        self.conn.close()
        return questions

    def delete_all(self):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM account_security_questions') 
        self.conn.commit()
        self.conn.close() 

class Logs:

    def __init__(self):
        self.conn = create_connection()
    
    def create(self, ip, agent, mac_addr):
        data = (ip, agent, mac_addr)
        sql = '''  INSERT INTO decrypt_logs(ip_address, user_agent, mac_address) VALUES (?, ?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, data) 
        self.conn.commit()
        print("Generated log:  ")
        self.conn.close()
        return cur.lastrowid

    def all(self):
        logs = []
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM decrypt_logs')   
        rows = cur.fetchall()
        for r in rows:
            l = Log(r[0],r[1], r[2], r[3])
            logs.append(l) 
        self.conn.close()
        return logs

    
    def delete_all(self):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM account_security_questions') 
        self.conn.commit()
        self.conn.close()
