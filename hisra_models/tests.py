from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.contrib.auth import hashers
from models import Playlist, Device, Media
from serializers import DeviceSerializer, MediaSerializer, PlaylistSerializer


def resp_equals(expected, got):
    for key in expected:
        if key not in got:
            raise Exception('The key: ' + unicode(key) + ' is not in ' +
                            unicode(got))
        if unicode(got[key]) != unicode(expected[key]):
            raise Exception('Expected: ' + unicode(expected[key]) +
                            ', got: ' + unicode(got[key]))
    return True


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
        response = self.client.get(url, format='json')
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
        expected_data = DeviceSerializer(db_device).data
        self.assertTrue(resp_equals(expected_data, response.data))

    def test_get_missing_device(self):
        url = '/api/user/' + self.username + '/device/' + 'missing_device'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_devices_for_user(self):
        devices = []
        for i in range(0, 10):
            device = {
                'unique_device_id': 'device_' + str(i),
                'playlist': self.playlist.id
            }
            devices.append(device)

        url = '/api/user/' + self.username + '/device'
        for device in devices:
            self.client.post(url, device, format='json')

        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 10)


class PlaylistTest(APITestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.owner = User.objects.create_user(username=self.username,
                                              password=self.password)

    def test_create_playlist(self):
        url = '/api/user/' + self.username + '/playlist'
        playlist = {
            'name': 'Cool playlist',
            'description': 'All the best stuff',
            'media_schedule_json': '{"fake_playlist" : "true"}'
        }
        response = self.client.post(url, playlist, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(resp_equals(playlist, response.data))
        db_playlist = Playlist.objects.get(pk=response.data['id'])
        expected_data = PlaylistSerializer(db_playlist).data
        self.assertTrue(resp_equals(expected_data, response.data))

    def test_create_playlist_bad_data(self):
        url = '/api/user/' + self.username + '/playlist'
        playlist = {
            'this': 'should',
            'not': 'work'
        }
        response = self.client.post(url, playlist, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_playlist_for_missing_user(self):
        url = '/api/user/doesnotexist/playlist'
        playlist = {
            'name': 'Cool playlist',
            'description': 'All the best stuff',
            'media_schedule_json': '{"fake_playlist" : "true"}'
        }
        response = self.client.post(url, playlist, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_playlists(self):
        playlist_count = 10
        playlists = []
        for i in range(0, playlist_count):
            playlist = {
                'name': 'Cool playlist',
                'description': 'All the best stuff',
                'media_schedule_json': '{"fake_playlist_json" : "true"}'
            }
            playlists.append(playlist)

        url = '/api/user/' + self.username + '/playlist'

        for playlist in playlists:
            response = self.client.post(url, playlist, format='json')
            self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Playlist.objects.count(), playlist_count)

        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 10)

        for i in range(0, len(response.data)):
            for key in playlists[i]:
                self.assertTrue(key in response.data[i])

    def test_get_all_playlists_for_missing_user(self):
        url = '/api/user/doesnotexist/playlist'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_playlist(self):
        playlist = Playlist.objects.create(
            owner=self.owner,
            name='Cool playlist',
            description='All the best stuff',
            media_schedule_json='{"fake_playlist_json": "true"}'
        )

        self.assertEquals(Playlist.objects.count(), 1)
        url = '/api/user/' + self.username + '/playlist/' + str(playlist.id)

        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        expected_data = PlaylistSerializer(playlist).data
        self.assertTrue(resp_equals(expected_data, response.data))

    def test_get_missing_playlist(self):
        url = '/api/user/' + self.username + '/playlist/13371337'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_playlist_update(self):
        playlist = Playlist.objects.create(
            owner=self.owner,
            name='Cool playlist',
            description='All the best stuff',
            media_schedule_json='{"fake_playlist_json": "true"}'
        )
        self.assertEquals(Playlist.objects.count(), 1)

        url = '/api/user/' + self.username + '/playlist/' + str(playlist.id)
        new_name = 'New name'
        new_description = 'New description'
        new_json = '{"new_playlist":"true"}'
        data = {
            'name': new_name,
            'description': new_description,
            'media_schedule_json': new_json
        }
        response = self.client.put(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        received = response.data
        self.assertEquals(received['name'], new_name)
        self.assertEquals(received['description'], new_description)
        self.assertEquals(received['media_schedule_json'], new_json)

    def test_put_playlist_update_bad_data(self):
        playlist = Playlist.objects.create(
            owner=self.owner,
            name='Cool playlist',
            description='All the best stuff',
            media_schedule_json='{"fake_playlist_json": "true"}'
        )
        self.assertEquals(Playlist.objects.count(), 1)
        url = '/api/user/' + self.username + '/playlist/' + str(playlist.id)
        data = {
            'this': 'should',
            'not': 'work'
        }
        response = self.client.put(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_playlist_update_for_missing_playlist(self):
        new_name = 'New name'
        new_description = 'New description'
        new_json = '{"new_playlist":"true"}'
        url = '/api/user/' + self.username + '/13371337'
        data = {
            'name': new_name,
            'description': new_description,
            'media_schedule_json': new_json
        }
        response = self.client.put(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


class MediaTest(APITestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.owner = User.objects.create_user(username=self.username,
                                              password=self.password)
        self.assertEquals(User.objects.count(), 1)

    def test_post_new_media(self):
        url = '/api/user/' + self.username + '/media'
        media = {
            'url': 'http://cdn3.volusion.com/sbcpn.tjpek/v/vspfiles/photos/FACE001C-2.jpg',
            'mediatype': 'P',
            'name': 'sad face',
            'description': 'A big blue sad face',
            'md5_checksum': 'ac59c6b42a025514e5de073d697b2afb'  # fake
        }
        response = self.client.post(url, media, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(resp_equals(media, response.data))
        db_media = Media.objects.get(pk=response.data['id'])
        expected_db_data = MediaSerializer(db_media).data
        self.assertTrue(resp_equals(expected_db_data, response.data))

    def test_post_new_media_bad_data(self):
        url = '/api/user/' + self.username + '/media'
        media = {
            'this': 'should',
            'not': 'work'
        }
        response = self.client.post(url, media, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_new_media_for_missing_user(self):
        url = '/api/user/notarealuser/media'
        media = {
            'url': 'http://cdn3.volusion.com/sbcpn.tjpek/v/vspfiles/photos/FACE001C-2.jpg',
            'mediatype': 'P',
            'name': 'sad face',
            'description': 'A big blue sad face',
            'md5_checksum': 'ac59c6b42a025514e5de073d697b2afb'  # fake
        }
        response = self.client.post(url, media, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_media(self):
        url = '/api/user/' + self.username + '/media'
        media = {
            'url': 'http://cdn3.volusion.com/sbcpn.tjpek/v/vspfiles/photos/FACE001C-2.jpg',
            'mediatype': 'P',
            'name': 'sad face',
            'description': 'A big blue sad face',
            'md5_checksum': 'ac59c6b42a025514e5de073d697b2afb'  # fake
        }
        response = self.client.post(url, media, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        id = response.data['id']
        url = '/api/user/' + self.username + '/media/' + str(id)
        response = self.client.delete(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Media.objects.count(), 0)

    def test_delete_missing_media(self):
        url = '/api/user/' + self.username + '/media/1337'
        response = self.client.delete(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_media(self):
        media = []
        for i in range(0, 10):
            media_item = {
                'url': 'http://cdn3.volusion.com/sbcpn.tjpek/v/vspfiles/photos/FACE001C-2.jpg',
                'mediatype': 'P',
                'name': 'sad face',
                'description': 'A big blue sad face',
                'md5_checksum': 'ac59c6b42a025514e5de073d697b2afb'  # fake
            }
            media.append(media_item)

        url = '/api/user/' + self.username + '/media'
        for media_item in media:
            self.client.post(url, media_item, format='json')

        self.assertEquals(Media.objects.count(), 10)

        response = self.client.get(url, format='json')
        for i in range(0, 10):
            self.assertTrue(resp_equals(media[i], response.data[i]))

    def test_get_all_media_for_missing_user(self):
        url = '/api/user/doesnotexist/media'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_media(self):
        media = Media.objects.create(
            owner=self.owner,
            url='http://cdn3.volusion.com/sbcpn.tjpek/v/vspfiles/photos/FACE001C-2.jpg',
            mediatype='P',
            name='sad face',
            description='A big blue sad face',
            md5_checksum='ac59c6b42a025514e5de073d697b2afb')

        self.assertEquals(Media.objects.count(), 1)

        url = '/api/user/' + self.username + '/media/' + str(media.id)
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        expected_data = MediaSerializer(media).data
        self.assertTrue(resp_equals(expected_data, response.data))

    def test_get_missing_media(self):
        url = '/api/user/' + self.username + '/media/13371337'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
