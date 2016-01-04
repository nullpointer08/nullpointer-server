(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('LoginController', LoginController);

/* @ngInject */
function LoginController($scope, User, Authentication, $location, $window) {
  $scope.login = function(user) {
      Authentication.login(user.username, user.password, function(success) {
          if(success) {
              $location.path('/');
          }
      });
  };
}

})();
