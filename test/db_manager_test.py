import json
import random
import string
import unittest
import db_manager as dbm
import logging_messages as lm
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

def get_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


class TestDbManager(unittest.TestCase):
    def test_invalid_search_parameters(self):
        # Input data
        data = MultiDict()
        data.add('addresses', '8 avenue Bellevue - New York')
        data.add('names', 'John')
        data.add('surname', 'Mayer')
        data = ImmutableMultiDict(data)

        # Call the function to test
        keys_to_ignore, sql_search_params, sql_search_values = dbm.get_search_parameters(data)

        # Verify the output against the expected output
        self.assertTrue('addresses' in keys_to_ignore)
        self.assertTrue('surname' in keys_to_ignore)
        self.assertTrue('names' in keys_to_ignore)
        self.assertFalse(sql_search_params)
        self.assertFalse(sql_search_values)

    def test_all_valid_search_parameters(self):
        # Input data
        data = MultiDict()
        data.add('address', '8 avenue Bellevue - New York')
        data.add('name', 'John')
        data.add('email', 'john@yahoo.com')
        data = ImmutableMultiDict(data)

        # Call the function to test
        keys_to_ignore, sql_search_params, sql_search_values = dbm.get_search_parameters(data)

        # Verify the output against the expected output
        self.assertFalse(keys_to_ignore)
        self.assertEqual(3, len(sql_search_params))
        self.assertTrue('address = ?' in sql_search_params)
        self.assertTrue('name = ?' in sql_search_params)
        self.assertTrue('password = ?' not in sql_search_params)
        self.assertTrue('email = ?' in sql_search_params)
        self.assertTrue("8 avenue Bellevue - New York" in sql_search_values)
        self.assertTrue("John" in sql_search_values)
        self.assertTrue("john@yahoo.com" in sql_search_values)


    def test_valid_invalid_search_parameters(self):
        # Input data
        data = MultiDict()
        data.add('address', '8 avenue Bellevue - New York')
        data.add('name', 'John')
        data.add('surname', 'Mayer')
        data = ImmutableMultiDict(data)

        # Call the function to test
        keys_to_ignore, sql_search_params, sql_search_values = dbm.get_search_parameters(data)

        # Verify the output against the expected output
        self.assertEqual(['surname'], keys_to_ignore)
        self.assertTrue('address = ?' in sql_search_params)
        self.assertTrue('name = ?' in sql_search_params)
        self.assertTrue("8 avenue Bellevue - New York" in sql_search_values)
        self.assertTrue("John" in sql_search_values)


    def test_insert_valid_parameters(self):
        # Generate random string for the email (as it has to be 'unique')
        random_email = get_random_string(16)
        # Input data
        user = {'name': 'John', 'email': random_email, 'address': '14 av Bellevue - New York', 'password': 'easypass' }

        # Verify the generated ID is positive
        self.assertGreater(dbm.insert_user(user), 0)

    def test_insert_existing_email(self):
        # Generate random string for the email (as it has to be 'unique')
        random_email = get_random_string(16)
        # Input data
        user = {'name': 'John', 'email': random_email, 'address': '14 av Bellevue - New York', 'password': 'easypass' }
        # Insert the user the first time
        dbm.insert_user(user)
        # Change the user parameters, except the email
        user = {'name': 'Johnny', 'email': random_email, 'address': '12 av Bellevue - New York', 'password': 'easypass2' }

        # Verify that the second attempt of inserting the user will fail, because of the existing email
        self.assertEqual(dbm.insert_user(user), 'UNIQUE constraint failed: users.email')


    def test_insert_partial_parameters(self):
        # Generate random string for the email (as it has to be 'unique')
        random_email = get_random_string(16)
        # Input data
        user = {'name': 'Sean', 'email': random_email, 'password': 'easypass' }

        # Verify that an error is thrown. All fields are mandatory for the insertion.
        self.assertEqual(dbm.insert_user(user), 'NOT NULL constraint failed: users.address')


    def test_get_all_elements(self):
        # Insert 2 elements in the table
        random_email = get_random_string(16)
        random_email2 = get_random_string(16)
        # Input data
        user1 = {'name': 'John', 'email': random_email, 'address': '14 av Bellevue - New York', 'password': 'easypass' }
        user2 = {'name': 'Johnno', 'email': random_email2, 'address': '13 av Bellevue - New York', 'password': 'easypass' }
        # Insert the users
        dbm.insert_user(user1)
        dbm.insert_user(user2)

        # get all users
        users, key_to_ignore = dbm.get_users()

        # Verify we have at least 2 users
        self.assertGreater(len(json.loads(users)), 1)

    def test_get_element_by_email(self):
        # Insert 2 elements in the table
        random_email = get_random_string(16)
        random_email2 = get_random_string(16)
        # Input data
        user1 = {'name': 'John', 'email': random_email, 'address': '14 av Bellevue - New York', 'password': 'easypass' }
        user2 = {'name': 'Johnno', 'email': random_email2, 'address': '13 av Bellevue - New York', 'password': 'easypass5' }
        # Insert the users
        dbm.insert_user(user1)
        dbm.insert_user(user2)

        # instantiate the filter
        data = MultiDict()
        data.add('email', random_email)
        data = ImmutableMultiDict(data)

        # get all users
        users, key_to_ignore = dbm.get_users(data)

        # Being the email unique, there will be only one element returned
        self.assertEqual(len(json.loads(users)), 1)

        # Retrieve the user and verify its content correspond to user1
        user = list(json.loads(users).values())[0]
        self.assertEqual(user.get('name'), 'John')
        self.assertEqual(user.get('email'), random_email)
        self.assertEqual(user.get('password'), 'easypass')
        self.assertEqual(user.get('address'), '14 av Bellevue - New York')


    def test_get_element_by_all_invalid_parameters(self):
        # Insert 1 element in the table
        random_email = get_random_string(16)
        # Input data
        user = {'name': 'John', 'email': random_email, 'address': '14 av Bellevue - New York', 'password': 'easypass' }
        # Insert the users
        dbm.insert_user(user)

        # instantiate the filter with only invalid parameters
        data = MultiDict()
        data.add('email2', random_email)
        data.add('surname', 'Ronny')
        data.add('telephone', '0123456')
        data = ImmutableMultiDict(data)

        # get all users
        users, key_to_ignore = dbm.get_users(data)

        # verify that all the 3 parameters will be ignored
        self.assertEqual(len(key_to_ignore), 3)
        self.assertTrue('email2' in key_to_ignore)
        self.assertTrue('surname' in key_to_ignore)
        self.assertTrue('telephone' in key_to_ignore)

    def test_update_user_no_id(self):
        # Input data
        user_id = None
        data = MultiDict()
        # Update the user without specifying the ID
        out_message = dbm.update_user(user_id, data)

        # Verify that the proper error message is thrown
        self.assertEqual(out_message, lm.NO_USER_ID)

    def test_update_user(self):
        # Insert 1 element in the table
        random_email = get_random_string(16)
        # Input data
        user = {'name': 'John', 'email': random_email, 'address': '14 av Bellevue - New York', 'password': 'easypass' }
        # Insert the users
        id_to_update = dbm.insert_user(user)

        # instantiate the filter
        data = MultiDict()
        new_email = get_random_string(16)
        new_address = '14 av Belorizonte - Toronto'
        data.add('email', new_email)
        data.add('address', new_address)
        data = ImmutableMultiDict(data)

        dbm.update_user(id_to_update, data)

        # Search the updated user, by ID
        data2 = MultiDict()
        data2.add('id', id_to_update)
        data2 = ImmutableMultiDict(data)

        users, key_to_ignore = dbm.get_users(data2)

        # Retrieve the user and verify its content correspond to the updated values
        updated_user = list(json.loads(users).values())[0]
        self.assertEqual(updated_user.get('name'), 'John')
        self.assertEqual(updated_user.get('email'), new_email)
        self.assertEqual(updated_user.get('password'), 'easypass')
        self.assertEqual(updated_user.get('address'), new_address)

    def test_delete_user_after_insertion(self):
        # Input data
        user = {'name': 'Mike', 'email': 'mike@yahoo.com', 'address': '6th avenue - New York', 'password': '123456' }

        # Insert user in the table
        user_id_to_remove = dbm.insert_user(user)

        # Instantiate get filter by ID
        data = MultiDict()
        data.add('id', user_id_to_remove)
        data = ImmutableMultiDict(data)

        # get all users
        users, key_to_ignore = dbm.get_users(data)

        # Verify that the user has been properly inserted
        self.assertEqual(len(json.loads(users)), 1)

        # Remove the user with the same ID
        dbm.delete_user(user_id_to_remove)

        # Re-retrieve the user with above user ID
        users, key_to_ignore = dbm.get_users(data)

        # Verify that the user has been properly removed
        self.assertEqual(len(json.loads(users)), 0)


if __name__ == '__main__':
    unittest.main()
