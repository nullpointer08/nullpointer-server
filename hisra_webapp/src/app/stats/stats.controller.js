(function() {
'use strict';

angular.module('hisraWebapp')
  .controller('StatsController', StatsController);

/*@ngInject*/
function StatsController(Authentication, $location, User, Device, Statistics, $scope) {
  var user = Authentication.getCurrentUser();
  if(user === undefined) {
    $location.path('/login');
  }

  User.getDevices({username: user.username}).$promise.then(function(devices) {
    console.dir(devices);
    $scope.devices = devices;
  });

  var statMap = {};
  Statistics.query(
    {username: user.username, id: 1},
    function() {
      console.log("SUCCESS");
    },
    function() {
      console.log("FAILURE TO FETCH STATS");
    }
  ).$promise.then(function(statistics) {
    statistics.forEach(function(stats) {
      if(statMap[stats.device_id] === undefined) {
        statMap[stats.device_id] = [];
      }
      statMap[stats.device_id].push(stats);
    });
  });

  $scope.getSelectedStats = function() {
    if(!$scope.selectedDevice) {
      return [];
    }
    return statMap[$scope.selectedDevice.id];
  };

  $scope.getStatTypeString = function(stat) {
    if(stat.type === 0) {
      return 'Error';
    }
    if(stat.type === 1) {
      return 'Success';
    }
  };
}

})();
