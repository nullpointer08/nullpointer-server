(function() {
  'use strict';

angular.module('hisraWebapp')
.controller('AccountController', AccountController);

/* @ngInject */
function AccountController($scope, User, Authentication, $location) {
  var loggedAs = Authentication.getCurrentUser();
  if(loggedAs == undefined) {
      return $location.path('/login');
  }

  var vm = this;
  User.$get({username: loggedAs.username})
  .then(function(user) {
      vm.user = user;
  });

  $scope.logout = function() {
      Authentication.logout();
      $location.path('/login');
  };

  $scope.updateUser = function(user) {
  }
}

})();
