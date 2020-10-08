#!/usr/bin/env python3
import os
from pathlib import Path
import config
import sqlite3
import logging
import logging_messages as lm
from collections import OrderedDict
import json
import time


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    filename=os.path.basename(__file__) + time.strftime("-%Y-%m-%d.log"))


sql_create_table_query = 'CREATE TABLE IF NOT EXISTS {} ('.format(config.TABLE_NAME) +\
                         ', '.join(x[0] + ' ' + x[1] for x in config.DB_COLUMNS) + \
                          ', PRIMARY KEY({}))'.format(config.DB_PRIMARY_KEY)


def get_search_values(input_value):
    return input_value.split(config.MULTIPLE_VALUE_DELIMETER)


def get_search_parameters(search_filters):
    """ Take the input search filter and
    extract the valid (according to the DB schema) search parameters
    while identifying the invalid ones (and ignoring them, not blocking the query).

    :param search_filters: the user's URL search parameters, e.g.: '{email:USER_EMAIL1,EMAIL2, name:USER_NAME}'
    :type search_filters: dict

    :return:
            ignore_keys: the user's inserted search parameters which are invalid, as not found in the DB schema
            keep_keys: the valid search keys specified by the user, pre-formatted for a SQL query
            keep_values: the valid search values specified by the user, pre-formatted for a SQL query
    :rtype: list
    """
    ignore_keys = []
    keep_keys = []
    keep_values = []

    if search_filters:
        for key in search_filters.keys():
            if key not in config.DB_ATTRIBUTES:
                ignore_keys.append(key)
            else:
                search_values = get_search_values(str(search_filters[key]))
                search_values_length = len(search_values)
                keep_values.extend(search_values)
                key_to_append = key + ' = ?'
                if search_values_length > 1:
                    key_to_append = '({})'.format(' OR '.join(search_values_length*[key_to_append]))
                keep_keys.append(key_to_append)
    return ignore_keys, keep_keys, keep_values


class DbManager:
    def __init__(self):
        # Check if db folder exists, else create it
        Path(config.DB.get('path')).mkdir(parents=True, exist_ok=True)
        # Connect to local db
        self.conn = sqlite3.connect(os.path.join(config.DB.get('path'), config.DB.get('name')), check_same_thread=False)

        # Create table if not exists
        try:
            self.c = self.conn.cursor()
            self.c.execute(sql_create_table_query)
        except sqlite3.Error as e:
            logging.error(e)

    def __del__(self):
        self.conn.close()

    def get_users(self, search_filters=None):
        logging.info(lm.ACTION_REQUESTED.format('GET'))

        all_columns = config.DB_ATTRIBUTES
        sql_select_query = 'SELECT * FROM {}'.format(config.TABLE_NAME)

        keys_to_ignore, sql_search_params, sql_search_values = get_search_parameters(search_filters)
        logging.debug(lm.DATA_STRUCTURES.format(keys_to_ignore, sql_search_params, sql_search_values))

        if len(sql_search_params):
            sql_select_query += ' WHERE ' + ' AND '.join(sql_search_params)

        users = {}
        try:
            logging.debug([sql_select_query, tuple(sql_search_values)])
            rows = self.c.execute(sql_select_query, tuple(sql_search_values))
            for row in rows:
                user = OrderedDict(zip(all_columns, list(row)))
                users[user.get(config.DB_PRIMARY_KEY)] = user
        except sqlite3.Error as e:
            logging.error(e)
            return(str(e))

        return json.dumps(users), keys_to_ignore

    def insert_user(self, json_user):
        logging.info(lm.ACTION_REQUESTED.format('INSERT'))

        sql_insert_query = "INSERT INTO {} ({}) VALUES({})".format(config.TABLE_NAME,
                                                      ', '.join("'{0}'".format(k) for k in list(json_user.keys())),
                                                      ', '.join("'{0}'".format(v) for v in list(json_user.values())))
        try:
            logging.debug(sql_insert_query)
            self.c.execute(sql_insert_query)
            last_id = self.c.lastrowid
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(e)
            return(str(e))
        return last_id

    def update_user(self, user_id, update_filter):
        if not user_id:
            logging.debug(lm.NO_USER_ID)
            return lm.NO_USER_ID

        logging.info(lm.ACTION_REQUESTED_FOR_ID.format('UPDATE', str(user_id)))
        sql_update_query = "UPDATE {} SET ".format(config.TABLE_NAME)

        keys_to_ignore, sql_update_params, sql_update_values = get_search_parameters(update_filter)
        logging.debug(lm.DATA_STRUCTURES.format(keys_to_ignore, sql_update_params, sql_update_values))

        if not sql_update_params:
            return lm.INVALID_PARAM.format(','.join(keys_to_ignore))

        sql_update_query += ', '.join(sql_update_params) + ' WHERE {} = ?'.format(config.DB_PRIMARY_KEY)
        sql_update_values.append(user_id)

        try:
            logging.debug([sql_update_query, tuple(sql_update_values)])
            self.c.execute(sql_update_query, tuple(sql_update_values))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(e)
            return(str(e))
        return int(user_id)

    def delete_user(self, user_id):
        if not user_id:
            logging.debug(lm.NO_USER_ID)
            return lm.NO_USER_ID

        logging.info(lm.ACTION_REQUESTED_FOR_ID.format('DELETE', user_id))
        sql_delete_query = "DELETE from {} WHERE {} = ?".format(config.TABLE_NAME, config.DB_PRIMARY_KEY)
        try:
            logging.debug([sql_delete_query, tuple([user_id])])
            self.c.execute(sql_delete_query, tuple([user_id]))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(e)
            return(str(e))
        return int(user_id)
