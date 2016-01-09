(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('PlaylistsController', PlaylistController);

/* @ngInject */
function PlaylistController($location, $scope, Authentication, User, Playlist) {
  var vm = this;

  var user = Authentication.getCurrentUser();
  if(user === undefined) {
      return $location.path('/login');
  }
  vm.playlists = [];

  User.getPlaylists({username: user.username}).$promise
    .then(function (playlists) {
      vm.playlists = playlists.map(function(playlist) {
        // JSON parsing doesn't seem to accept single parentheses
        var jsonSchedule = playlist.media_schedule_json;
        playlist.media_schedule = JSON.parse(jsonSchedule);
        return playlist;
      });
    });

  $scope.createNewPlaylist = function() {
    var newPl = Playlist.save(
      {username: user.username},
      {
        name: 'New playlist',
        description: '',
        media_schedule_json: '[]'
      },
      function() {
        $location.path('/playlist/' + newPl.id);
      },
      function() {
        console.log("Failed to create new playlist");
      }
    );
  };

  $scope.removePlaylist = function(playlist) {
    Playlist.remove(
      {username: user.username, id: playlist.id},
      null,
      function() {
        console.log("SUCCESS Removed playlist");
        vm.playlists = vm.playlists.filter(function(pl) {
          return pl.id !== playlist.id;
        });
      },
      function() {
        console.log("FAILURE Could not remove playlist");
      }
    );
  };
}

})();
