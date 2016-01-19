(function() {
'use strict';

angular.module('hisraWebapp')
  .controller('StatsController', StatsController);

function StatsController(Authentication, $location, Device, Statistics, $scope) {
  var user = Authentication.getCurrentUser();
  if(user === undefined) {
    $location.path('/login');
  }

  $scope.statistics = Statistics.query(
    {username: user.username, id: 1},
    function() {
      console.dir($scope.statistics);
    },
    function() {

    }
  );
}

})();
