#project/tests/test_users.py

import json

from project.tests.base     import BaseTestCase
from project.api.models     import User
from project                import db

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

    def test_single_uer(self):
        """Ensure get single user behaves correctly"""
        user = User(username='michael',email='michael@realpython.com')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('michael',data['data']['username'])
            self.assertIn('michael@realpython.com',data['data']['email'])
            self.assertIn('success', data['status'])
