#!/usr/bin/env python3
import os

DB = {
    'name': 'users.db',
    'path': os.path.join(os.getcwd(), 'data'),
}

DB_PRIMARY_KEY = 'id'

DB_COLUMNS = [
    (DB_PRIMARY_KEY, 'INTEGER'),
    ('name', 'TEXT NOT NULL'),
    ('email', 'TEXT NOT NULL UNIQUE'),
    ('password', 'TEXT NOT NULL'),
    ('address', 'TEXT NOT NULL')
]

DB_ATTRIBUTES = [x[0] for x in DB_COLUMNS]

TABLE_NAME = 'users'

SERVER_IP_ADDRESS = '192.168.0.49'
SERVER_PORT_NUMBER = 4322
