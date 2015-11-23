'use strict';

/* global angular */

var Playlist = angular.module('Playlist', ['ngResource']);

Playlist.factory('Playlist', ['$resource', function ($resource) {
  return $resource('/api/user/:username/playlist/:id', {
    id: '@id'
  }, {
    update: {
      method: 'PUT'
    }
  });
}]);
