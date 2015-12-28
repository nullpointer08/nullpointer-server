(function() {
'use strict';

angular.module('hisraWebapp')
  .config(routeConfig);

function routeConfig ($routeProvider) {
  $routeProvider.when('/login', {
    templateUrl: 'app/login/login.html',
    controller: 'LoginController'
  });
}

})();
