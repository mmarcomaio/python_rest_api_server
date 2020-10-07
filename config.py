#!/usr/bin/env python3
import os

DB = {
    'name': 'users.db',
    'path': os.path.join(os.getcwd(), 'data'),
}

TABLE_NAME = 'users'
DB_PRIMARY_KEY = 'id'
MULTIPLE_VALUE_DELIMETER = ','

DB_COLUMNS = [
    (DB_PRIMARY_KEY, 'INTEGER'),
    ('name', 'TEXT NOT NULL'),
    ('email', 'TEXT NOT NULL UNIQUE'),
    ('password', 'TEXT NOT NULL'),
    ('address', 'TEXT NOT NULL')
]

DB_ATTRIBUTES = [x[0] for x in DB_COLUMNS]

######### DATA TO BE UPDATED BY THE USER ############
SERVER_IP_ADDRESS = '127.0.0.1' # YOUR_SERVER_IP_ADDRESS
SERVER_PORT_NUMBER = 4322       # YOUR_SERVER_PORT_NUMBER
