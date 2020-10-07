from flask import Flask, json, request as req
import config
import db_manager as dbm
import rules_checker as rc
import logging
import os
import time
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

api = Flask(__name__)


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    filename=os.path.basename(__file__) + time.strftime("-%Y-%m-%d.log"))


def get_data(parameters):
    d = MultiDict()
    for k, v in parameters.items():
        d.add(k, v)
    return ImmutableMultiDict(d)


@api.route('/users', methods=['GET'])
def get_users():
    logging.debug('[GET]Received following arguments: {}'.format(str(req.args)))
    users, _ = dbm.get_users(req.args)
    return users


@api.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    logging.debug('[GET]Received following ID: {}'.format(user_id))
    data = get_data({config.DB_PRIMARY_KEY: user_id})
    users, keys_to_ignore = dbm.get_users(data)
    return users


@api.route('/users', methods=['POST'])
def create_user():
    if not req.json:
        return ("Missing JSON format input parameters"), 400
    logging.debug('[POST]Received following data: {}'.format(json.dumps(req.json)))

    visitor_country = rc.get_country_from_ip(req.remote_addr)
    if not rc.is_country_allowed(req.remote_addr):
        return ("{} visitor's country is not allowed to perform this operation".format(visitor_country)), 400
    new_item_id = dbm.insert_user(req.json)

    if isinstance(new_item_id, str):
        return (new_item_id), 400
    return ({config.DB_PRIMARY_KEY: new_item_id}), 201


@api.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    logging.debug('[UPDATE]User ID {} to be updated with following arguments: {}'.format(user_id, str(req.args)))
    updated_user_id = dbm.update_user(user_id, req.args)
    if isinstance(updated_user_id, str):
        return (updated_user_id), 400
    return ({config.DB_PRIMARY_KEY: updated_user_id}), 200


@api.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    logging.debug('[DELETE]User ID {} to be deleted'.format(user_id))
    deleted_user_id = dbm.delete_user(user_id)
    if isinstance(deleted_user_id, str):
        return (deleted_user_id), 400
    return ({config.DB_PRIMARY_KEY: deleted_user_id}), 200


if __name__ == '__main__':
    api.run(host=config.SERVER_IP_ADDRESS, port=config.SERVER_PORT_NUMBER)
