from cryptography.fernet import Fernet
from cli_tool.models import AccountKey, QuestionKey
import cli_tool.database as db
from cli_tool.database import AccountKeys, QuestionKeys
import sqlite3
import json
import requests
import sys
import os

HOST =  "http://deka:5000"

def view_keys():
    keys = AccountKeys()
    myKeys = keys.all() 
    try:
        for m in myKeys:
            obj = m.dump() 
            print("Service: {} || Key: {}".format(obj["service"], obj["key"].decode('utf-8'))) 
    except sqlite3.OperationalError as  e:
        print(e)
        return False
    return True

def decrypt_one(account_service):
    response = requests.get(HOST + "/account/{}".format(account_service))
    json_data = json.loads(response.text)
    account = json_data["service"]
    username = json_data["username"]
    password = json_data["password"] 
    print("Account: {} || Username: {} || Hash: {}".format(account, username, password))
    return True 

def decrypt_all():
    try:
        keys = AccountKeys() 
        myKeys = keys.all()
        response = requests.get(HOST + "/accounts")
        json_data = json.loads(response.text)
        key_count = 0
        for key, password in zip(myKeys, json_data):
            client_key = key.get_key()
            server_pass = password["password"] 
            k = Fernet(client_key)
            myP = bytes(server_pass, 'utf-8')  
            password = k.decrypt(myP)
            password = password.decode('utf-8')
            print("Service:  {} || Password: {}".format(key.get_service(),  password))

    except sqlite3.OperationalError as e:
        print(e)
        return False

    return True


def create_account(service, username, password):
    params = {}
    params["service"] = service
    params["username"] = username
    params["password"] = password
    server = requests.post(HOST + "/accounts", data=params)
    data = json.loads(server.text) 
    service = data["service"] 
    key = bytes(data["key"], "utf-8")
    try:
        keys = AccountKeys()
        keys.create(service, key) 
    except sqlite3.OperationalError as  e:
        print(e)
    return True


def create_question(question, answer, service):
    params = {}
    params["question"] = question
    params["answer"] = answer
    server = requests.post(HOST + "/accounts/" + service, data=params)
    
    data = json.loads(server.text) 
    service = data["service"] 
    key = bytes(data["key"], "utf-8")
    try:
        keys = QuestionKeys()
        keys.create(service, question, answer) 
    except sqlite3.OperationalError as  e:
        print(e)
    return True 

def delete_accounts():  
    server = requests.delete(HOST + "/accounts")
    return True 
