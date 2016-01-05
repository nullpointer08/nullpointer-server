(function() {
  'use strict';

angular.module('hisraWebapp')
.controller('PlaylistDetailController', PlaylistDetailController);

/* @ngInject */
function PlaylistDetailController($scope, $location, $routeParams, Authentication, User, Playlist) {
  var user = Authentication.getCurrentUser();
  if(user === undefined) {
      return $location.path('/login');
  }

  $scope.types = ['web_page', 'video', 'image'];
  $scope.selected = undefined;

  $scope.getTemplate = function (media) {
    if ($scope.selected && media.uri === $scope.selected.uri) return 'edit';
    return 'display';
  };

  $scope.editMedia = function (media) {
    console.dir(media);
    $scope.selected = angular.copy(media);
  };

  $scope.saveMedia = function (index) {
    console.log("Saving contact");
    $scope.playlist.media_schedule[index] = angular.copy($scope.selected);
    $scope.reset();
  };

  $scope.reset = function () {
    $scope.selected = undefined;
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

  Playlist.get({
      id: $routeParams.playlistId,
      username: user.username
  }).$promise
    .then(function(playlist) {
        var json = playlist.media_schedule_json.replace(/'/g, '"');
        playlist.media_schedule = JSON.parse(json);
        $scope.playlist = playlist;
    });
}
})();
