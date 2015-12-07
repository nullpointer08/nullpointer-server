'use strict';

angular.module('myApp.stats', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/stats', {
    templateUrl: 'stats/stats.html',
    controller: 'StatsCtrl'
  });
}])

.controller('StatsCtrl', [function() {

}]);