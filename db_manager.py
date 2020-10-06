#!/usr/bin/env python3
import os
from pathlib import Path
import config
import sqlite3
import logging
from collections import OrderedDict
import json


sql_create_table_query = 'CREATE TABLE IF NOT EXISTS {} ('.format(config.TABLE_NAME) +\
                         ', '.join(x[0] + ' ' + x[1] for x in config.DB_COLUMNS) + \
                          ', PRIMARY KEY({}))'.format(config.DB_PRIMARY_KEY)
# Check if db folder exists, else create it
Path(config.DB.get('path')).mkdir(parents=True, exist_ok=True)

# Connect to local db
conn = sqlite3.connect(os.path.join(config.DB.get('path'), config.DB.get('name')), check_same_thread=False)

# Create table if not exists
try:
    c = conn.cursor()
    c.execute(sql_create_table_query)
except sqlite3.Error as e:
    logging.error(e)


def get_search_parameters(search_filters, update=False):
    ignore_keys = []
    keep_keys = []
    keep_values = []

    if search_filters:
        for key in search_filters.keys():
            if key not in config.DB_ATTRIBUTES:
                ignore_keys.append(key)
            else:
                keep_keys.append(key + ' = ?')
                keep_values.append(search_filters[key])

    return ignore_keys, keep_keys, keep_values


def get_users(search_filters=None):
    all_columns = config.DB_ATTRIBUTES
    sql_select_query = 'SELECT * FROM {}'.format(config.TABLE_NAME)
	
    keys_to_ignore, sql_search_params, sql_search_values = get_search_parameters(search_filters)
    if len(sql_search_params):
        sql_select_query += ' WHERE ' + ' AND '.join(sql_search_params)

    users = {}
    try:
        rows = c.execute(sql_select_query, tuple(sql_search_values))
        for row in rows:
            user = OrderedDict(zip(all_columns, list(row)))
            users[user.get(config.DB_PRIMARY_KEY)] = user
    except sqlite3.Error as e:
        logging.error(e)
        return(str(e))

    return json.dumps(users), keys_to_ignore


def insert_user(json_user):
    sql_insert_query = "INSERT INTO {} ({}) VALUES({})".format(config.TABLE_NAME, \
                                                  ', '.join("'{0}'".format(k) for k in list(json_user.keys())), \
                                                  ', '.join("'{0}'".format(v) for v in list(json_user.values())))
    try:
        c.execute(sql_insert_query)
        last_id = c.lastrowid
        conn.commit()
    except sqlite3.Error as e:
        logging.error(e)
        return(str(e))
    return last_id


def update_user(user_id, update_filter):
    sql_update_query = "UPDATE {} SET ".format(config.TABLE_NAME)

    keys_to_ignore, sql_update_params, sql_update_values = get_search_parameters(update_filter, update=True)

    if not sql_update_params:
        return "{}: invalid parameters. Please re-try with valid parameters".format(','.join(keys_to_ignore))

    sql_update_query += ', '.join(sql_update_params) + ' WHERE {} = ?'.format(config.DB_PRIMARY_KEY)
    sql_update_values.append(user_id)

    try:
        c.execute(sql_update_query, tuple(sql_update_values))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(e)
        return(str(e))
    return 'User ID {} updated correctly. Ignored parameters: {}'.format(user_id, ','.join(keys_to_ignore))
