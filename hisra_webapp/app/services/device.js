'use strict';

/* global angular */

var Device = angular.module('Device', ['ngResource']);

Device.factory('Device', ['$resource', function ($resource) {
  return $resource('/api/user/:username/device/:id', {
    id: '@id'
  }, {
    update: {
      method: 'PUT'
    }
  });
}]);
