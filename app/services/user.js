'use strict';

/* global angular */

var User = angular.module('User', ['ngResource', 'Media', 'Playlist', 'Device']);

User.factory('User', ['$resource', 'Media', 'Playlist', 'Device',
function ($resource, Media, Playlist, Device) {
  var resource = $resource('/api/user/:username', {
    username: '@username'
  });


  angular.extend(resource.prototype, {
    getMedia: function() {
      return Media.query({username: this.username});
    },
    getPlaylists: function() {
      return Playlist.query({username: this.username});
    },
    getDevices: function() {
      return Device.query({username: this.username});
    }
  });

  return resource;
}]);
