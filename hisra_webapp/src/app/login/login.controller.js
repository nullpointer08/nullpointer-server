(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('LoginController', LoginController);

/* @ngInject */
function LoginController($scope, User, Authentication, $location) {
  var vm = this;
  vm.loggedAs = Authentication.getCurrentUser();

  $scope.login = function(user) {
      Authentication.login(user.username, user.password, function(response) {
          if(response.success) {
              $location.path('/');
          }
      });
  };

  $scope.logout = function() {
      Authentication.logout();
  }
}

})();
