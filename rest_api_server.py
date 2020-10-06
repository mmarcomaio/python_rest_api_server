from flask import Flask, json, request as req
import config
import db_manager as dbm
import logging

api = Flask(__name__)

@api.route('/users', methods=['GET'])
def get_users():
    print('GET request received')
    users = dbm.get_users(req.args)

    return users


if __name__ == '__main__':
    api.run(host=config.SERVER_IP_ADDRESS, port=config.SERVER_PORT_NUMBER)
