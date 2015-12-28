(function() {
'use strict';

angular.module('hisraWebapp')
  .config(routeConfig);

function routeConfig ($routeProvider) {
  $routeProvider.when('/playlist/:playlistId', {
    templateUrl: 'app/playlist-detail/playlist-detail.html',
    controller: 'PlaylistDetailController',
    controllerAs: 'playlist'
  });
}

})();
