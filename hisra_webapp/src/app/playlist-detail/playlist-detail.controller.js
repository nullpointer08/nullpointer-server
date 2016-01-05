(function() {
  'use strict';

angular.module('hisraWebapp')
.controller('PlaylistDetailController', PlaylistDetailController);

/* @ngInject */
function PlaylistDetailController($scope, $location, $routeParams, Authentication, User, Playlist, Media) {
  var user = Authentication.getCurrentUser();
  if(user === undefined) {
      return $location.path('/login');
  }

  var typeMap = {
    'I': 'image',
    'V': 'video',
    'W': 'web_page'
  };
  var reverseTypeMap = {
    'image': 'I',
    'video': 'V',
    'web_page': 'W'
  };

  $scope.types = ['web_page', 'video', 'image'];

  $scope.allMedia = [];
  User.getMedia({username: user.username}).$promise
  .then(function (media) {
    media.forEach(function(m) {
      m.uri = m.url;
      m.type = typeMap[m.media_type];
      m.time = 0;
    });
    $scope.allMedia = media;
    console.dir(media);
  });

  $scope.webPageToAdd = {
    name: '',
    description: '',
    uri: '',
    type: 'web_page',
    time: 20
  };

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
}

})();
