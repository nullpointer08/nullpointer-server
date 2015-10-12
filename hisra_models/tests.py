from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.contrib.auth import hashers
from models import Playlist, Device
from serializers import DeviceSerializer


class UserTests(APITestCase):
    '''
    Tests posting users and fetching users
    '''
    def setUp(self):
        '''
        Creates some test users
        '''
        self.start_user_count = 10
        for i in range(0, self.start_user_count):
            username = 'user' + str(i)
            password = 'password' + str(i)

            User.objects.create_user(username=username, password=password)
        self.assertEqual(User.objects.count(), self.start_user_count)

    def test_create_user(self):
        """
        Ensure we can create a new user
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

    def test_create_user_bad_data(self):
        '''
        Tests that we get 400 bad request for bad data
        '''
        url = '/api/user'
        user = {'this': None, 'should': None, 'not': None, 'work': None}
        response = self.client.post(url, user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_find_user(self):
        '''
        Test we can find a user
        '''
        url = '/api/user/user0'
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['username'], 'user0')
        self.assertFalse('password' in response.data)

    def test_find_missing_user(self):
        '''
        Tests that finding a missing user returns 404
        '''
        url = '/api/user/user_that_does_not_exist'
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


class DeviceTest(APITestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.owner = User.objects.create_user(username=self.username,
                                              password=self.password)
        self.playlist = Playlist.objects.create(owner=self.owner,
                                                name='test_playlist',
                                                description='test_description',
                                                media_schedule_json='{}')
        self.assertEquals(User.objects.count(), 1)
        self.assertEquals(Playlist.objects.count(), 1)

    def test_add_device(self):
        url = '/api/user/' + self.username + '/device'
        device = {
            'unique_device_id': 'device_1',
            'playlist': self.playlist.id
        }
        response = self.client.post(url, device, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.contains_data(response.data, device))
        db_device = Device.objects.get(pk=device['unique_device_id'])
        self.assertEquals(db_device.playlist, self.playlist)
        self.assertEquals(db_device.owner, self.owner)

    def test_add_device_bad_data(self):
        url = '/api/user/' + self.username + '/device'
        device = {
            'bad': 'data',
            'should': 'fail'
        }
        response = self.client.post(url, device, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def contains_data(self, response_data, data):
        for key in data:
            if key not in response_data or not response_data[key] == data[key]:
                return False
        return True

    def test_get_device(self):
        db_device = Device.objects.create(unique_device_id='device_1',
                                          playlist=self.playlist,
                                          owner=self.owner)
        url = '/api/user/' + self.username + '/device/' + \
              db_device.unique_device_id
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, DeviceSerializer(db_device).data)

    def test_get_missing_device(self):
        url = '/api/user/' + self.username + '/device/' + 'missing_device'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
