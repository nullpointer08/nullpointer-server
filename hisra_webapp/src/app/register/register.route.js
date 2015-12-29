(function() {
'use strict';

angular.module('hisraWebapp')
  .config(routeConfig);

function routeConfig ($routeProvider) {
  $routeProvider.when('/register', {
    templateUrl: 'app/register/register.html',
    controller: 'RegisterController'
  });
}

})();
