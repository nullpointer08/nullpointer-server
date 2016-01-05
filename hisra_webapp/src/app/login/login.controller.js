(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('LoginController', LoginController);

/* @ngInject */
function LoginController(Authentication, $location) {
  	var vm = this;
	vm.login = function(user) {
      Authentication.login(user.username, user.password)
      	.then(function() {
          $location.path('/');
      	});
  };
}

})();
