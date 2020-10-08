from collections import OrderedDict
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import logging
import rules_checker as rc


def on_send_success(record_metadata):
    logging.debug('Topic updated: {}'.format(record_metadata.topic))
    logging.debug('Partition: {}'.format(record_metadata.partition))
    logging.debug('Offset: {}'.format(record_metadata.offset))


def on_send_error(excp):
    logging.error('Error while sending the event', exc_info=excp)


class KProducer:
    def __init__(self, ip, port, topic_name):

        self.producer = KafkaProducer(bootstrap_servers='{}:{}'.format(ip, port),
                                      value_serializer=lambda m: json.dumps(m).encode('ascii'))
        self.topic = topic_name

    def send_event(self, json_event):
        self.producer.send(self.topic, json_event).add_callback(on_send_success).add_errback(on_send_error)
        self.producer.flush()


class KEvent:
    def __init__(self, mutation, mutation_content, flask_request):
        self.visitor_ip = str(flask_request.remote_addr)
        self.visitor_country = rc.get_country_from_ip(self.visitor_ip)
        self.host = str(flask_request.host)
        self.user_agent = str(flask_request.user_agent)
        self.mutation_type = mutation
        self.mutation_content = mutation_content

