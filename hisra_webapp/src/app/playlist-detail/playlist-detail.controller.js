(function() {
  'use strict';

angular.module('hisraWebapp')
.controller('PlaylistDetailController', PlaylistDetailController);

/* @ngInject */
function PlaylistDetailController($location, $routeParams, Authentication, User, Playlist) {
  var user = Authentication.getCurrentUser();
  if(user == undefined) {
      return $location.path('/login');
  }

  var vm = this;
  Playlist.get({
      id: $routeParams.playlistId,
      username: user.username
  }).$promise
    .then(function(playlist) {
        var json = playlist.media_schedule_json.replace(/'/g, '"');
        playlist.media_schedule = JSON.parse(json);
        vm.playlist = playlist;
    });
}

})();
