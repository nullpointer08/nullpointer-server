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

  var vm = this;
  $scope.items = ["one", "two", "thre", "four", "five", "six"];
  $scope.types = ['web_page', 'video', 'image'];
  $scope.selected = undefined;
  $scope.getTemplate = function (media) {
        if($scope.selected === undefined) return 'display';
       if (media.uri === $scope.selected.uri) return 'edit';
       else return 'display';
   };

   $scope.editMedia = function (media) {
     console.dir(media);
        $scope.selected = angular.copy(media);
    };

    $scope.saveMedia = function (index) {
        console.log("Saving contact");
        vm.playlist.media_schedule[index] = angular.copy($scope.selected);
        $scope.reset();
    };

    $scope.reset = function () {
        $scope.selected = undefined;
    };

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
