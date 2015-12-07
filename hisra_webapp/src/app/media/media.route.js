(function() {
'use strict';

angular.module('hisraWebapp')
  .config(routeConfig);

function routeConfig ($routeProvider) {
  $routeProvider.when('/media', {
    templateUrl: 'app/media/media.html',
    controller: 'MediaController',
    controllerAs: 'media'
  });
}

})();
