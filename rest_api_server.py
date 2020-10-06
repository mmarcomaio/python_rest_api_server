from flask import Flask, json, request as req
import config
import db_manager as dbm
import logging
import os
import sys
import time

api = Flask(__name__)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    filename=os.path.basename(__file__) + time.strftime("-%Y-%m-%d.log"))


@api.route('/users', methods=['GET'])
def get_users():
    logging.debug('Received following arguments: {}'.format(str(req.args)))
    users, keys_to_ignore = dbm.get_users(req.args)

    return users + '<br><hr>Ignored keys: ' + ','.join(keys_to_ignore)


if __name__ == '__main__':
    api.run(host=config.SERVER_IP_ADDRESS, port=config.SERVER_PORT_NUMBER)
