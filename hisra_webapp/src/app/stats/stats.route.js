(function() {
'use strict';
angular.module('hisraWebapp')
  .config(routeConfig);

function routeConfig ($routeProvider) {
  $routeProvider.when('/stats', {
    templateUrl: 'app/stats/stats.html',
    controller: 'StatsController',
    controllerAs: 'stats'
  });
}
})();
