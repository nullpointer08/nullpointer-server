(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('DevicesController', DevicesController);

/* @ngInject */
function DevicesController($scope, $location, Authentication, User, Device) {
  var vm = this;

  vm.devices = [];
  vm.errorMessage = '';

  var user = Authentication.getCurrentUser();
  if(user === undefined) {
      return $location.path('/login');
  }

  User.getDevices({username: user.username}).$promise
    .then(function (devices) {
      vm.devices = devices;
    });

  var playlistMap = {};
  User.getPlaylists({username: user.username}).$promise
    .then(function(playlists) {
      vm.playlists = playlists.map(function(playlist) {
        // JSON parsing doesn't seem to accept single parentheses
        var json = playlist.media_schedule_json.replace(/'/g, '"');
        playlist.media_schedule = JSON.parse(json);
        playlists.forEach(function(playlist) {
          playlistMap[playlist.id] = playlist;
        });
        return playlist;
      });
    });

  $scope.setDevicePlaylist = function(deviceId, playlistId) {
    if(deviceId === undefined || playlistId === undefined) {
      vm.errorMessage = 'You must select a device and a playlist';
      return;
    }
    vm.errorMessage = '';
    var reqParams = {
      username: user.username,
      id: deviceId
    };
    Device.get(
      reqParams,
      function(device) {
        updateDevice(device, playlistId, reqParams);
      },
      // Failure
      function() {
        console.log("Device playlist update failed");
        vm.errorMessage = 'Could not update device playlist';
      }
    );
  };

  function updateDevice(device, playlistId, reqParams) {
    device.playlist = playlistId;
    device.$update(
      reqParams,
      function() {
        console.log("Updated device playlist");
      },
      function() {
        console.log("Device playlist update failed");
        vm.errorMessage = 'Could not update device playlist';
      }
    );
  }

  vm.getPlaylistDetail = function(playlistId, key) {
    if(playlistId in playlistMap) {
      if(key in playlistMap[playlistId]) {
          return playlistMap[playlistId][key];
      }
    }
    return '';
  };
}

})();
