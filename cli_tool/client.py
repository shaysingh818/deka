from cryptography.fernet import Fernet
from cli_tool.models import AccountKey, QuestionKey
import sqlite3
import json
import requests
import os

class Client:

    def __init__(self, db_file, host_address, alias):
        self.db_file = db_file
        self.host = host_address
        self.accounts = []
        self.questions = [] 
        self.alias = alias

