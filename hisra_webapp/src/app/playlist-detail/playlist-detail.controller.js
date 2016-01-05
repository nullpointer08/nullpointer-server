(function() {
  'use strict';

angular.module('hisraWebapp')
.controller('PlaylistDetailController', PlaylistDetailController);

/* @ngInject */
function PlaylistDetailController($scope, $location, $timeout, $routeParams, Authentication, User, Playlist, Media, MediaTypes, Notification) {
  var user = Authentication.getCurrentUser();
  if(user === undefined) {
      return $location.path('/login');
  }

  $scope.allMedia = [];
  User.getMedia({username: user.username}).$promise
  .then(function (media) {
    $scope.allMedia = media;
    console.dir(media);
  });

  $scope.mediaTypes = MediaTypes;

  $scope.addToPlaylist = function(media) {
    media.time = 20;
    $scope.playlist.media_schedule.push(media);
  };

  $scope.savePlaylist = function() {
    var updatedPlaylist = angular.copy($scope.playlist);
    updatedPlaylist.media_schedule_json = JSON.stringify(updatedPlaylist.media_schedule).replace(/"/g, "'");
    delete updatedPlaylist.media_schedule;
    Playlist.update({
        username: user.username,
        id: updatedPlaylist.id
      }, 
      updatedPlaylist
    );
  };

  $scope.removeMedia = function(media) {
    var index = $scope.playlist.media_schedule.indexOf(media);
    if(index != -1) {
      $scope.playlist.media_schedule.splice(index, 1);
    }
  };

  Playlist.get({
    id: $routeParams.playlistId,
    username: user.username
  }).$promise.then(function(playlist) {
    var json = playlist.media_schedule_json.replace(/'/g, '"');
    playlist.media_schedule = JSON.parse(json);
    $scope.playlist = playlist;
  });

  $scope.deletePlaylist = function() {
    var answer = confirm("Are you sure you want to delete the playlist?");
    if(!answer) {
      return;
    }
    Playlist.delete(
      {username: user.username, id: $scope.playlist.id},
      null,
      function() {
        console.log("SUCCESS: playlist deleted");
        $location.path('/playlists');
      },
      function() {
        console.log("FAILURE: Could not delete playlist");
      }
    );
  };

  $scope.notifier = Notification;
}

})();
