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
      console.dir(user);
      console.dir(Authentication);
      console.dir(Authentication.getCurrentUser());
      Authentication.login(user.username, user.password, function(response) {
          if(response.success) {
              $location.path('/');
          }
      });
  };
}

})();
