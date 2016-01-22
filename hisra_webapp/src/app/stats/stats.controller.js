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

  $scope.getSelectedStats = function() {
    if(!$scope.selectedDevice) {
      return [];
    }
    return getAndCacheStats($scope.selectedDevice);
  };

  var statMap = {};

  function getAndCacheStats(device) {
    var stats = statMap[device.id];
    if(stats) {
      return stats;
    }
    stats = Statistics.query(
       {username: user.username, id: device.id},
       function() {
         console.log("SUCCESS fetching stats");
       },
       function() {
         console.log("FAILURE fetching stats");
       }
    );
    statMap[device.id] = stats;
    return stats;
  }

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
