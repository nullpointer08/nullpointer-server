(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('DevicesController', DevicesController);

/* @ngInject */
function DevicesController($scope, $location, Authentication, User, Device, MediaTypes, Notification) {
  var vm = this;

  vm.deviceMap = {};
  vm.playlistMap = {};
  vm.errorMessage = '';

  var user = Authentication.getCurrentUser();
  if(user === undefined) {
      return $location.path('/login');
  }

  $scope.notifier = Notification.createNotifier();

  User.getDevices({username: user.username}).$promise
    .then(function (devices) {
      devices.map(function(device) {
        vm.deviceMap[device.id] = device;
      });
    });

  User.getPlaylists({username: user.username}).$promise
    .then(function(playlists) {
      playlists.map(function(playlist) {
          vm.playlistMap[playlist.id] = playlist;
          vm.playlistMap[playlist.id].media_schedule_json = JSON.parse(vm.playlistMap[playlist.id].media_schedule_json);
        });
    });



  $scope.mediaTypes = MediaTypes;

  $scope.$watch('selectedDevice', function(newValue, oldValue) {
    if(newValue !== undefined) {
      console.log(newValue);
      $scope.selectedPlaylist = vm.playlistMap[newValue.playlist];
    }
  });

  $scope.setDevicePlaylist = function(device, playlist) {
    if(device === undefined || playlist === undefined) {
      vm.errorMessage = 'You must select a device and a playlist';
      return;
    }
    vm.errorMessage = '';
    var reqParams = {
      username: user.username,
      id: device.id
    };
    Device.get(
      reqParams,
      function(device) {
        updateDevice(device, playlist.id, reqParams);
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
        $scope.notifier.showSuccess("Device playlist set");
      },
      function() {
        $scope.notifier.showFailure("Could not set device playlist");
      }
    );
  }
}

})();
