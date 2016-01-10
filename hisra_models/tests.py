import base64
import json
import logging
import shutil
from hashlib import md5

from django.conf import settings
from django.contrib.auth import hashers
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

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


def authenticate(client, username, password):
    response = client.post('/api/authentication', {'username': username, 'password': password})
    if response.status_code == 200:
        client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])


class UserTests(APITestCase):
    """
    Tests posting users and fetching users
    """

    def setUp(self):
        """
        Creates some test users
        """
        self.start_user_count = 10
        for i in range(0, self.start_user_count):
            username = 'user' + str(i)
            password = 'password' + str(i)

            User.objects.create_user(username=username, password=password)
        self.assertEqual(User.objects.count(), self.start_user_count)

    def test_find_user(self):
        """
        Test we can find a user
        """
        authenticate(self.client, 'user0', 'password0')
        url = '/api/user/user0'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['username'], 'user0')
        self.assertFalse('password' in response.data)

    def test_find_missing_user(self):
        """
        Tests that finding a missing user returns 403
        """
        authenticate(self.client, 'user0', 'password0')
        url = '/api/user/user_that_does_not_exist'
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class DeviceTest(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.owner = User.objects.create_user(username=self.username,
                                              password=self.password)
        authenticate(self.client, self.username, self.password)
        self.playlist = Playlist.objects.create(owner=self.owner,
                                                name='test_playlist',
                                                description='test_description',
                                                media_schedule_json='{}')
        self.assertEquals(User.objects.count(), 1)
        self.assertEquals(Playlist.objects.count(), 1)

    def contains_data(self, response_data, data):
        for key in data:
            if key not in response_data or not response_data[key] == data[key]:
                return False
        return True

    def test_get_device(self):
        db_device = Device.objects.create(unique_device_id='device_1',
                                          name='Device 1',
                                          playlist=self.playlist,
                                          owner=self.owner)
        url = '/api/user/' + self.username + '/device/' + \
              str(db_device.id)
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        expected_data = DeviceSerializer(db_device).data
        self.assertTrue(resp_equals(expected_data, response.data))

    def test_get_missing_device(self):
        url = '/api/user/' + self.username + '/device/155'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_devices_for_user(self):
        for i in range(0, 10):
            Device.objects.create(owner=self.owner,
                                  unique_device_id='device_ {0}'.format(i),
                                  playlist=self.playlist,
                                  name='device')
        url = '/api/user/' + self.username + '/device'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 10)


class PlaylistTest(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.owner = User.objects.create_user(username=self.username,
                                              password=self.password)
        authenticate(self.client, self.username, self.password)

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
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

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
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

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

    def test_delete_playlist(self):
        playlist = Playlist.objects.create(
                owner=self.owner,
                name='Cool playlist',
                description='All the best stuff',
                media_schedule_json='{"fake_playlist_json": "true"}'
        )
        url = '/api/user/' + self.username + '/playlist/' + str(playlist.id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_missing_playlist(self):
        url = '/api/user/' + self.username + '/playlist/1234567890'
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


class MediaTestBase(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.owner = User.objects.create_user(username=self.username,
                                              password=self.password)
        self.assertEquals(User.objects.count(), 1)
        authenticate(self.client, self.username, self.password)

    def test_post_new_media(self):
        url = '/api/user/' + self.username + '/media'
        media = {
            'url': 'http://cdn3.volusion.com/sbcpn.tjpek/v/vspfiles/photos/FACE001C-2.jpg',
            'media_type': 'I',
            # 'name': 'sad face',
            # 'description': 'A big blue sad face',
            # 'md5_checksum': 'ac59c6b42a025514e5de073d697b2afb'  # fake
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
            'media_type': 'I',
            # 'name': 'sad face',
            # 'description': 'A big blue sad face',
            # 'md5_checksum': 'ac59c6b42a025514e5de073d697b2afb'  # fake
        }
        response = self.client.post(url, media, format='json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_media(self):
        url = '/api/user/' + self.username + '/media'
        media = {
            'url': 'http://cdn3.volusion.com/sbcpn.tjpek/v/vspfiles/photos/FACE001C-2.jpg',
            'media_type': 'I',
            # 'name': 'sad face',
            # 'description': 'A big blue sad face',
            # 'md5_checksum': 'ac59c6b42a025514e5de073d697b2afb'  # fake
        }
        response = self.client.post(url, media, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        id = response.data['id']
        url = '/api/user/' + self.username + '/media/' + str(id)
        response = self.client.delete(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
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
                'media_type': 'I',
                # 'name': 'sad face',
                # 'description': 'A big blue sad face',
                # 'md5_checksum': 'ac59c6b42a025514e5de073d697b2afb'  # fake
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
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_media(self):
        media = Media.objects.create(
                owner=self.owner,
                url='http://cdn3.volusion.com/sbcpn.tjpek/v/vspfiles/photos/FACE001C-2.jpg',
                media_type='I',
                # name='sad face',
                # description='A big blue sad face',
                # md5_checksum='ac59c6b42a025514e5de073d697b2afb'
        )

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


class DevicePlaylist(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
                username=self.username,
                password=self.password
        )
        self.playlist = Playlist.objects.create(
                owner=self.user,
                name='test name',
                description='test description',
                media_schedule_json='{"fake_json": "true"}'
        )
        self.device = Device.objects.create(
                owner=self.user,
                unique_device_id='testdevice',
                playlist=self.playlist
        )
        authenticate(self.client, self.username, self.password)

    def test_get_device_playlist(self):
        url = '/api/device/playlist'
        self.client.credentials(HTTP_AUTHORIZATION='Device {0}'.format(self.device.unique_device_id))
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        expected = PlaylistSerializer(self.playlist).data
        serializer = PlaylistSerializer(data=response.data)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(resp_equals(expected, response.data))

    def test_get_device_playlist_no_auth(self):
        url = '/api/device/playlist'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_playlist_from_device_without_playlist(self):
        url = '/api/device/playlist'
        Device.objects.create(unique_device_id='device_with_no_playlist', name='asdf', owner=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Device device_with_no_playlist')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


logger = logging.getLogger(__name__)


def get_md5(filePath):
    m = md5()
    with open(filePath, 'rb') as f:
        while True:
            chunk = f.read(128)
            if not chunk:
                break
            m.update(chunk)
    return m.hexdigest()


@override_settings(MEDIA_ROOT='/tmp/hisra_test_media_root')
class MediaUploadTestCase(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.owner = User.objects.create_user(username=self.username,
                                              password=self.password, id=2000000000)
        self.assertEquals(User.objects.count(), 1)
        self.test_file = 'test_media/kuva.jpg'
        original = open(self.test_file, "rb")
        self.upload_file = SimpleUploadedFile(name="kuva.jpg", content=original.read())
        original.close()

    def test_post_file(self):
        logger.debug("MEDIA ROOT IS: %s", settings.MEDIA_ROOT)
        authenticate(self.client, self.username, self.password)
        response = self.client.post('/api/chunked_upload/', {'the_file': self.upload_file})
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        dict_resp = json.loads(response.content)
        upload_id = dict_resp['upload_id']
        logger.debug(upload_id)
        md5_checksum = get_md5(self.test_file)
        logger.debug(md5_checksum)
        data = {
            'upload_id': upload_id,
            'md5': md5_checksum
        }
        response = self.client.post('/api/chunked_upload_complete/', data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_file_no_authorization(self):
        self.test_post_file()
        self.client.credentials()
        media = Media.objects.first()
        logger.debug("Media id: %s", media.id)
        url = '/media/' + str(media.id)
        # NO auth
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # note: does not actually return a file because we use web server to do that
    def test_get_file_basic_auth(self):
        self.test_post_file()
        media = Media.objects.first()
        logger.debug("Media id: %s", media.id)
        url = '/media/' + str(media.id)

        authenticate(self.client, self.username, self.password)

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        if not response.get('Content-Disposition').startswith("attachment; filename=kuva"):
            raise AssertionError("Content disposition was unexpected")
        if not response.get('X-Accel-Redirect').startswith("/protected/" + str(self.owner.id)):
            raise AssertionError("X-Accel-Redirect was unexpected")

    # note: does not actually return a file because we use web server to do that
    def test_get_file_owned_device(self):
        self.test_post_file()
        Device.objects.create(unique_device_id='device_1', owner=self.owner)
        media = Media.objects.first()
        logger.debug("Media id: %s", media.id)
        device_id = 'Device device_1'
        self.client.credentials(HTTP_AUTHORIZATION=device_id)
        url = '/media/' + str(media.id)
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        if not response.get('Content-Disposition').startswith("attachment; filename=kuva"):
            raise AssertionError("Content disposition was unexpected")
        if not response.get('X-Accel-Redirect').startswith("/protected/" + str(self.owner.id)):
            raise AssertionError("X-Accel-Redirect was unexpected")

    # note: does not actually return a file because we use web server to do that
    def test_get_file_with_filename(self):
        self.test_post_file()
        self.client.credentials()
        Device.objects.create(unique_device_id='device_1', owner=self.owner)
        media = Media.objects.first()

        device_auth = 'Device device_1'
        self.client.credentials(HTTP_AUTHORIZATION=device_auth)

        url = '/media/' + str(media.id)
        #  url = '/media/' + str(media.owner.id) + '/' + str(media.name)
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        if not response.get('Content-Disposition').startswith("attachment; filename=kuva"):
            raise AssertionError("Content disposition was unexpected")
        if not response.get('X-Accel-Redirect').startswith("/protected/" + str(self.owner.id)):
            raise AssertionError("X-Accel-Redirect was unexpected")

    def tearDown(self):
        shutil.rmtree('/tmp/hisra_test_media_root')
