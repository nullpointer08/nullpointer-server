'use strict';

/* global angular*/

angular.module('myApp.main', ['ngRoute'])

.config(['$routeProvider', function ($routeProvider) {
  $routeProvider.when('/', {
    templateUrl: 'main/main.html',
    controller: 'MainViewCtrl'
  });
}])

.controller('MainViewCtrl', ['$scope', function () {

}]);
