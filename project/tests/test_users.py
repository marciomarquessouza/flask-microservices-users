#project/tests/test_users.py

import json

from project.tests.base     import BaseTestCase
from project.api.models     import User
from project                import db

def add_user(username,email):
    user = User(username=username,email=email)
    db.session.add(user)
    db.session.commit()
    return user

class TestUserService(BaseTestCase):
    """ Tests for the Users Service"""

    def test_users(self):
        """Ensure the ping route behaves correctly """
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code,200)
        self.assertIn('pong!',data['message'])
        self.assertIn('success',data['status'])

    def test_add_user(self):
        """Ensure if a new user can be added"""
        with self.client:
            response=self.client.post(
            '/users',
            data=json.dumps(dict(
                username='michael',
                email='michael@realpython.com'
            )),
            content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,201)
            self.assertIn('michael@realpython.com was added!',data['message'])
            self.assertIn('success',data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,400)
            self.assertIn('Invalid payload.',data['message'])
            self.assertIn('fail',data['status'])

    def test_add_user_without_user(self):
        """Ensure error is thrown if the JSON hasn't a user"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(email='marcio.souza@mms.com')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,400)
            self.assertIn('Invalid payload.',data['message'])
            self.assertIn('fail',data['status'])

    def test_add_user_duplicated_user(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
            '/users',
            data=json.dumps(dict(
                username='michael',
                email='michael@realpython.com'
            )),
            content_type='application/json',
        )
        response = self.client.post(
            '/users',
            data=json.dumps(dict(
                username='michael',
                email='michael@realpython.com'
            )),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Sorry. That email already exists.', data['message'])
        self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly"""
        user = add_user('michael','michael@realpython.com')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('michael',data['data']['username'])
            self.assertIn('michael@realpython.com',data['data']['email'])
            self.assertIn('success', data['status'])

    def test_id_not_provided(self):
        """Ensure error is throw if a valid id is not provided"""
        with self.client:
            response= self.client.get('/users/it_is_not_an_id')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,404)
            self.assertIn('User format is not valid',data['message'])
            self.assertIn('fail',data['status'])

    def test_id_not_exit(self):
        """Ensure error is throw if a invalid id is sent"""
        with self.client:
            response= self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,404)
            self.assertIn('User does not exist',data['message'])
            self.assertIn('fail',data['status'])

    def test_add_more_than_one_users(self):
        """Ensure that the system accept more than one register"""
        add_user(username='marcio souza',email='marciomultimedia@gmail.com')
        add_user(username='flavia monteiro',email='flavia.monteiro@gmail.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,200)
            self.assertEqual(len(data['data']['users']),2)
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][1])
            self.assertIn('marcio souza',data['data']['users'][0]['username'] )
            self.assertIn('marciomultimedia@gmail.com',data['data']['users'][0]['email'] )
            self.assertIn('flavia monteiro',data['data']['users'][1]['username'] )
            self.assertIn('flavia.monteiro@gmail.com',data['data']['users'][1]['email'] )
            self.assertIn('success',data['status'])

    def test_main_no_user(self):
        """Ensure the main route behaves correctly when no users have been added to the database"""
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'<h1>All Users</h1>',response.data)
        self.assertIn(b'<p>No users!</p>',response.data)

    def test_main_with_users(self):
        """ Ensure the main route behaves correctly when users have been added to database"""
        add_user('michael','michael@realpython.com')
        add_user('fletcher','fletcher@realpython.com')
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'<h1>All Users</h1>',response.data)
        self.assertNotIn(b'<p>No users!</p>',response.data)
        self.assertIn(b'<strong>michael</strong>',response.data)
        self.assertIn(b'<strong>fletcher</strong>',response.data)

    def test_main_add_user(self):
        """Ensure a new user can be added to the database"""
        with self.client:
            response = self.client.post (
                '/',
                data = dict(username='michael', email='michael@realpython.com'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code,200)
            self.assertIn(b'<h1>All Users</h1>',response.data)
            self.assertNotIn(b'<p>No users!</p>',response.data)
            self.assertIn(b'<strong>michael</strong>',response.data)
