(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('PlaylistsController', PlaylistController);

/* @ngInject */
function PlaylistController(User) {
  var vm = this;

  vm.playlists = [];

  // TODO: Get username from auth service
  User.getPlaylists({username: 'testy'}).$promise
    .then(function (playlists) {
      console.dir(playlists)
      vm.playlists = playlists.map(function(playlist) {
        // JSON parsing doesn't seem to accept single parentheses
        var json = playlist.media_schedule_json.replace(/'/g, '"');
        playlist.media_schedule = JSON.parse(json);
        return playlist;
      });
    });
}

})();
