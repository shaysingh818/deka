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

    def encrypt(self, account):
        key = Fernet.generate_key()
        f = Fernet(key) 
        token = f.encrypt(bytes(account.get_pass(), 'utf-8'))
        account.set_pass(token)
        return (account.get_service(), key)
    
    def create(self, service, user, passw):
        data = (service, user, passw)
        sql = '''  INSERT INTO accounts(service,username, password) VALUES (?, ?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, data) 
        self.conn.commit()
        print("inserted account ")
        self.conn.close() 
    
    def prepare(self, a):
        current_key = self.encrypt(a)
        password_test = a.get_pass().decode('utf-8')
        self.create(a.get_service(), a.get_user(), password_test)
        return(current_key[0], current_key[1])

    def all(self):
        accounts = []
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM accounts')   
        rows = cur.fetchall()
        for r in rows:
            a = Account(r[1], r[2], r[3])
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
        account = Account( result[1], result[2], result[3])  
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

    def encrypt(self, question):
        key = Fernet.generate_key()
        f = Fernet(key) 
        token = f.encrypt(bytes(question.get_answer(), 'utf-8'))
        question.set_answer(token)
        return (question.get_question(), key)
    
    def by_service(self, account_id):
        questions = []
        cur = self.conn.cursor()
        data = (account_id,)
        cur.execute('SELECT * FROM account_security_questions WHERE question_account=?', data)  
        rows = cur.fetchall()
        for r in rows:
            q = Question(r[1], r[2], r[3])
            questions.append(q) 
        self.conn.close()
        return questions

    def create(self, conn, question, answer, account_id):
        data = (question, answer, account_id)
        sql = '''  INSERT INTO account_security_questions(question, answer, question_account) VALUES (?, ?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, data) 
        self.conn.commit()
        print("inserted question ")
        self.conn.close() 
        return cur.lastrowid
 
    def all(self):
        questions = []
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM account_security_questions')     
        rows = cur.fetchall()
        for r in rows:
            q = Question(r[1], r[2], r[3])
            questions.append(a) 
        self.conn.close()
        return questions

    def prepare(self, q):
        current_key = self.encrypt(q)
        answer_test = q.get_answer().decode('utf-8')
        self.create(self.conn,q.get_question(), q.get_answer(), q.get_account_id())
        return(current_key[0], current_key[1])

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
            l = Log(r[1], r[2], r[3])
            logs.append(l) 
        self.conn.close()
        return logs

    
    def delete_all(self):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM account_security_questions') 
        self.conn.commit()
        self.conn.close()
