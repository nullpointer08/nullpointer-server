(function() {
'use strict';

angular.module('hisraWebapp')
  .config(routeConfig);

function routeConfig ($routeProvider) {
  $routeProvider.when('/playlists', {
    templateUrl: 'app/playlists/playlists.html',
    controller: 'PlaylistsController',
    controllerAs: 'playlists'
  });
}

})();
