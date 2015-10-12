from rest_framework import status
from rest_framework.test import APITestCase
from models import User
from django.contrib.auth import hashers


class AccountTests(APITestCase):

    def setUp(self):

        # Create some users
        self.start_user_count = 10
        for i in range(0, self.start_user_count):
            username = 'user' + str(i)
            password = 'password' + str(i)

            User.objects.create_user(username=username, password=password)
        self.assertEqual(User.objects.count(), self.start_user_count)

    def test_create_user(self):
        """
        Ensure we can create a new account object.
        """
        url = '/api/user'
        user = {'username': 'test_user', 'password': 'password123'}
        response = self.client.post(url, user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data['username'], user['username'])
        self.assertFalse('password' in response.data)

        self.assertEqual(User.objects.count(), self.start_user_count + 1)
        users = User.objects.all().filter(username=user['username'])
        self.assertEquals(len(users), 1)
        self.assertEqual(users[0].username, user['username'])
        pass_ok = hashers.check_password(user['password'], users[0].password)
        self.assertTrue(pass_ok)

        # Test bad data
        user = {'this': None, 'should': None, 'not': None, 'work': None}
        response = self.client.post(url, user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_find_user(self):
        url = '/api/user/user0'
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['username'], 'user0')
        self.assertFalse('password' in response.data)
