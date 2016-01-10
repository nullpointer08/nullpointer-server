(function() {
  'use strict';

angular.module('hisraWebapp')
.controller('AccountController', AccountController);

/* @ngInject */
function AccountController($scope, User, Authentication, $location) {
  var loggedAs = Authentication.getCurrentUser();
  if(loggedAs === undefined) {
        return $location.path('/login');
  }

  var vm = this;
  var user = User.$get(
    {username: loggedAs.username},
    function() {
      console.log("Success: got user");
      vm.user = user;
    },
    function() {
      console.log("Failure: could not get user");
    }
  )
  .then(function(user) {
    console.dir(user);
      vm.user = user;
  });


  $scope.logout = function() {
      Authentication.logout();
      $location.path('/login');
  };

  $scope.updateUser = function(user) {
  };
}

})();
