(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('PlaylistsController', PlaylistController);

/* @ngInject */
function PlaylistController($location, Authentication, User) {
  var vm = this;

  var user = Authentication.getCurrentUser();
  if(user == undefined) {
      return $location.path('/login');
  }
  vm.playlists = [];

  // TODO: Get username from auth service
  User.getPlaylists({username: user.username}).$promise
    .then(function (playlists) {
      vm.playlists = playlists.map(function(playlist) {
        // JSON parsing doesn't seem to accept single parentheses
        var json = playlist.media_schedule_json.replace(/'/g, '"');
        playlist.media_schedule = JSON.parse(json);
        return playlist;
      });
    });
}

})();
