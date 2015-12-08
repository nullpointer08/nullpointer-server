(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('PlaylistsController', DevicesController);

/* @ngInject */
function DevicesController(User) {
  var vm = this;

  vm.playlists = [];

  // TODO: Get username from auth service
  User.getPlaylists({username: 'apina'}).$promise
    .then(function (playlists) {
      vm.playlists = playlists.map(function(playlist) {
        playlist.media_schedule = JSON.parse(playlist.media_schedule_json);
        return playlist;
      });
    });
}

})();
