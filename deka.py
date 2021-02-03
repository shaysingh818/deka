#!/usr/bin/env python3
import cli_tool.cli as cli
import argparse
from cryptography.fernet import Fernet
import sqlite3
import json
import requests
import sys
from art import *


art_1 = text2art("DEKA")
print(art_1)

parser = argparse.ArgumentParser(description='Password Manager arguments.')
parser.add_argument('-s', '--service', help='Account service')
parser.add_argument('-u', '--username', help='Account username')
parser.add_argument('-p', '--password', help='Account password')
parser.add_argument('-v', '--view', help='View Accounts')
parser.add_argument('-k', '--keys', help='View Keys')
parser.add_argument('-q', '--question', help='Questions')
parser.add_argument('-a', '--answer', help='Answers')
args = parser.parse_args()

	
if args.service and args.username and args.password:
	cli.create_account(args.service, args.username, args.password)
	print("To decrypt accounts: ./deka.py -v all ")
elif args.question == 'all':
    cli.view_questions() 
elif args.view == 'all':
	cli.decrypt_all()
elif args.view == 'account':
	cli.decrypt_one(args.service) 
elif args.question and args.answer and args.service:
    cli.create_question(args.question, args.answer, args.service) 
elif args.keys == 'all':
	cli.view_keys() 
