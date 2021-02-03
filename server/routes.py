from flask import Flask, request, jsonify, session
from flask_restful import Resource, Api
from cryptography.fernet import Fernet
import controllers
from models import Account, Question, Log
from controllers import Accounts, Questions, Logs
import sqlite3
import json
import netifaces as nif
from flask_api import status
#import controllers

secure_shared_service = Flask(__name__)
api = Api(secure_shared_service)

class accounts(Resource):

    def get(self):
        account = Accounts()
        acc = account.all()      
        results = []
        for a in acc:
            results.append(a.dump()) 
        return jsonify(results)
    
    def post(self):
        service = request.form['service']
        username = request.form['username']
        password = request.form['password'] 
        acc = Accounts() 
        result = acc.encrypt_and_create(service, username, password)
        if result == False:
            print(result) 
            return jsonify("Error") 
        obj = {}
        obj["service"] = result[0]
        obj["key"] = result[1]
        return jsonify(obj)

    def delete(self):
        accounts = Accounts()
        accounts.delete_all()
        return jsonify("Deleted Accounts: ") 

class accountDetail(Resource):

    def get(self, account_service):
        accounts = Accounts()
        obj = accounts.detail(account_service)
        return jsonify(obj.dump())
    
            
class accountQuestion(Resource):

    def get(self, account_service):
        acc = Accounts()
        q = Questions()
        a_id = acc.get(account_service) 
        questions = q.by_service(a_id) 
        results = []
        for q in questions:
            results.append(q.dump()) 
        return jsonify(results)

    def post(self, account_service):
        question = request.form['question']
        answer = request.form['answer'] 
        questions = Questions() 
        result = questions.encrypt_and_create(question, answer, account_service)
        if result == False:
            print(result) 
            return jsonify("Error") 
        obj = {}
        obj["service"] = result[0]
        obj["key"] = result[1]
        return jsonify(obj)

        
class accountQuestionDetail(Resource):
    def get(self, account_service):
        acc = Accounts()
        a_id = acc.get(account_service) 
        obj = {}
        obj["service_id"] = a_id
        return jsonify(obj)

class serverLog(Resource):

    def get(self):
        ip_addr = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        mac_addr = controllers.mac_for_ip(ip_addr)
        logs = Logs()
        logs.create(ip_addr, user_agent, mac_addr) 
        log = {}
        log["ip_address"] = ip_addr
        log["user_agent"] = user_agent
        log["mac_address"] = mac_addr       
        return jsonify("test")

    def delete(self):   
        logs = Logs()
        logs.delete_all()
        return jsonify("Deleted decrypt logs: ") 
        

api.add_resource(accounts, '/accounts', endpoint="accounts")
api.add_resource(accountDetail, '/account/<account_service>')
api.add_resource(accountQuestion, '/account/question/<account_service>')
api.add_resource(serverLog, '/log')

def main():
    secure_shared_service.run(host='deka', debug=True)

if __name__ == '__main__':
    main()
