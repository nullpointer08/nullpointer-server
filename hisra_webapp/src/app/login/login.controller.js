(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('LoginController', LoginController);

/* @ngInject */
function LoginController($scope, User, Authentication, $location) {
  $scope.login = function(user) {
      Authentication.login(user.username, user.password, function(response) {
          if(response.success) {
              $location.path('/');
          }
      });
  };
}

})();
