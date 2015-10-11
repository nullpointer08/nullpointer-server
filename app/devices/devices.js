'use strict';

angular.module('myApp.devices', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/devices', {
    templateUrl: 'devices/devices.html',
    controller: 'DevicesCtrl'
  });
}])

.controller('DevicesCtrl', [function() {

}]);