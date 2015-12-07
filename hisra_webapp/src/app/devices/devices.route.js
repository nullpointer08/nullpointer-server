(function() {
'use strict';

angular.module('hisraWebapp')
  .config(routeConfig);

function routeConfig ($routeProvider) {
  $routeProvider.when('/devices', {
    templateUrl: 'app/devices/devices.html',
    controller: 'DevicesController',
    controllerAs: 'devices'
  });
}

})();
