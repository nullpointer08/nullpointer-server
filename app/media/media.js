'use strict';

/* global angular */

angular.module('myApp.media', ['ngRoute', 'User'])

.config(['$routeProvider', function ($routeProvider) {
  $routeProvider.when('/media', {
    templateUrl: 'media/media.html',
    controller: 'MediaCtrl'
  });
}])

.controller('MediaCtrl', ['$scope', 'User', function ($scope, User) {
  $scope.media = [];

  // TODO: Get username from auth service
  User.getMedia({username: 'test'}).$promise
    .then(function (media) {
      $scope.media = media;
    });

  $scope.openFileBrowser = function () {
    document.getElementById('media-add__file').click();
  };
}]);
