'use strict';

/* global angular*/

angular.module('webappApp.devices', ['ngRoute', 'User'])

.config(['$routeProvider', function ($routeProvider) {
  $routeProvider.when('/devices', {
    templateUrl: 'devices/devices.html',
    controller: 'DevicesCtrl'
  });
}])

.controller('DevicesCtrl', ['$scope', 'User', function ($scope, User) {
  $scope.devices = [];

  // TODO: Get username from auth service
  User.getDevices({username: 'test'}).$promise
    .then(function (devices) {
      $scope.devices = devices;
    });
}]);
