'use strict';
/* global angular */

// Declare app level module which depends on views, and components
angular.module('myApp', [
  'ngRoute',
  'myApp.devices',
  'myApp.media',
  'myApp.stats',
  'myApp.main'
])
.config(['$routeProvider', function ($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/'});
}]);
