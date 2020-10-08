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

WHITE_LIST_COUNTRIES = ['CH']

######### DATA TO BE UPDATED BY THE USER ############
WHITE_LIST_OVERRIDE = False              # To be set to True during the system tests
SERVER_IP_ADDRESS = '127.0.0.1'          # YOUR_SERVER_IP_ADDRESS
SERVER_PORT_NUMBER = 4322                # YOUR_SERVER_PORT_NUMBER
KAFKA_SERVER_IP = '192.168.0.21'         # YOUR_KAFKA_SERVER_IP_ADDRESS
KAFKA_SERVER_PORT = 9092                 # YOUR_KAFKA_SERVER_PORT_NUMBER
KAFKA_TOPIC = 'my-topic-events-1'        # YOUR_KAFKA_TOPIC_NAME
KAFKA_ACTIVE_SERVER = False              # True if you have a Kafka Server up and running. False otherwise.
