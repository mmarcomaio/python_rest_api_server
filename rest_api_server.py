from flask import Flask, json, request as req
import config
import db_manager
import kafka_manager as km
import rules_checker as rc
import logging
import os
import time
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

api = Flask(__name__)
dbm = db_manager.DbManager()
if config.KAFKA_ACTIVE_SERVER:
    kafka_producer = km.KProducer(config.KAFKA_SERVER_IP, config.KAFKA_SERVER_PORT, config.KAFKA_TOPIC)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    filename=os.path.basename(__file__) + time.strftime("-%Y-%m-%d.log"))


def get_data(parameters):
    """ Transform a dictionary containing search parameters into an ImmutableMultiDict.

    :param parameters: search parameters
    :type parameters: dict

    :return: same input values, in another format
    :rtype: ImmutableMultiDict
    """
    d = MultiDict()
    for k, v in parameters.items():
        d.add(k, v)
    return ImmutableMultiDict(d)


def handle_kafka_notification(mutation_type, mutation_content, request):
    """ Send a notification to a Kafka topic, if the Kafka server is active

    :param mutation_type: Create/Update/Delete
    :type mutation_type: str

    :param mutation_content: The output of the request which brought to a db status change
    :type mutation_content: int, list

    :param request: flask request containing relevant data to send to the topic
    """

    if not config.KAFKA_ACTIVE_SERVER:
        return 'Kafka Server not activated'
    mutation_event = km.KEvent(mutation_type, mutation_content, request)
    kafka_producer.send_event(mutation_event.__dict__)


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

    handle_kafka_notification('CREATE_USER', new_item_id, req)

    return ({config.DB_PRIMARY_KEY: new_item_id}), 201


@api.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    logging.debug('[UPDATE]User ID {} to be updated with following arguments: {}'.format(user_id, str(req.args)))
    updated_user_id = dbm.update_user(user_id, req.args)
    if isinstance(updated_user_id, str):
        return (updated_user_id), 400

    handle_kafka_notification('UPDATE_USER', updated_user_id, req)

    return ({config.DB_PRIMARY_KEY: updated_user_id}), 200


@api.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    logging.debug('[DELETE]User ID {} to be deleted'.format(user_id))
    deleted_user_id = dbm.delete_user(user_id)
    if isinstance(deleted_user_id, str):
        return (deleted_user_id), 400

    handle_kafka_notification('DELETE_USER', deleted_user_id, req)

    return ({config.DB_PRIMARY_KEY: deleted_user_id}), 200


if __name__ == '__main__':
    api.run(host=config.SERVER_IP_ADDRESS, port=config.SERVER_PORT_NUMBER)
