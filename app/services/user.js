'use strict';

/* global angular */

var User = angular.module('User', ['ngResource', 'Media']);

User.factory('User', ['$resource', 'Media', 'Playlist', 'Device',
function ($resource, Media, Playlist, Device) {
  return $resource('/api/user/:username', {
    username: '@username'
  }, {
    getMedia: {
      method: 'GET',
      url: '/api/user/:username/media',
      isArray: true,
      transformResponse: function (data) {
        var media = angular.fromJson(data);
        return media.map(function (mediaObject) {
          return new Media(mediaObject);
        });
      }
    },
    getPlaylists: {
      method: 'GET',
      url: '/api/user/:username/playlist',
      isArray: true,
      transformResponse: function (data) {
        var playlist = angular.fromJson(data);
        return playlist.map(function (playlistObject) {
          return new Playlist(playlistObject);
        });
      }
    },
    getDevices: {
      method: 'GET',
      url: '/api/user/:username/device',
      isArray: true,
      transformResponse: function (data) {
        var device = angular.fromJson(data);
        return device.map(function (deviceObject) {
          return new Device(deviceObject);
        });
      }
    }
  });
}]);
