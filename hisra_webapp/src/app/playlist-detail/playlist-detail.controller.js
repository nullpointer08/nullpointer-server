(function() {
  'use strict';

angular.module('hisraWebapp')
.controller('PlaylistDetailController', PlaylistDetailController);

/* @ngInject */
function PlaylistDetailController($routeParams, User, Playlist) {
  var vm = this;
  Playlist.get({id: $routeParams.playlistId, username: 'testy'}).$promise
    .then(function(playlist) {
        var json = playlist.media_schedule_json.replace(/'/g, '"');
        playlist.media_schedule = JSON.parse(json);
        vm.playlist = playlist;
        console.dir(vm.playlist);
    });
  /*var vm = this;

  vm.playlists = [];

  // TODO: Get username from auth service
  //Playlist.get({username='testy', id='1'})
  User.getPlaylists({username: 'testy'}).$promise
    .then(function (playlists) {
      console.dir(playlists)
      vm.playlists = playlists.map(function(playlist) {
        // JSON parsing doesn't seem to accept single parentheses
        var json = playlist.media_schedule_json.replace(/'/g, '"');
        playlist.media_schedule = JSON.parse(json);
        return playlist;
      });
  });*/
}

})();
