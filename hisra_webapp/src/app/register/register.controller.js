(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('RegisterController', RegisterController);

/* @ngInject */
function RegisterController($scope, User, Authentication, $location) {
  $scope.register = function(user) {
      Authentication.login(user.username, user.password, function(response) {
          if(response.success) {
              $location.path('/');
          }
      });
  };
}

})();
