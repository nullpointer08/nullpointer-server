(function() {
'use strict';

angular.module('hisraWebapp')
  .config(routeConfig);

function routeConfig ($routeProvider) {
  $routeProvider.when('/account', {
    templateUrl: 'app/account/account.html',
    controller: 'AccountController',
    controllerAs: 'vm'
  });
}

})();
