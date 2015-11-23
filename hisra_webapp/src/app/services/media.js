'use strict';

/* global angular */

var Media = angular.module('Media', ['ngResource']);

Media.factory('Media', ['$resource', function ($resource) {
  return $resource('/api/user/:username/media/:id', {
    id: '@id'
  });
}]);
