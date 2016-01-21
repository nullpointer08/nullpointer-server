(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('LoginController', LoginController);

/* @ngInject */
function LoginController(Authentication, $location) {
  	var vm = this;
    
    activate(); // Log the user out if she navigates to the login screen?
    
	vm.login = function(user) {
      Authentication.login(user.username, user.password)
      	.then(function() {
          $location.path('/');
      	});
  };
  
  function activate() {
      Authentication.logout();
  }
}

})();
