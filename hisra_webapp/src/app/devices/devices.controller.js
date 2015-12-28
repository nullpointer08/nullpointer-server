(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('DevicesController', DevicesController);

/* @ngInject */
function DevicesController($location, Authentication, User) {
  var vm = this;

  vm.devices = [];
  var user = Authentication.getCurrentUser();
  if(user == undefined) {
      return $location.path('/login');
  }

  User.getDevices({username: user.username}).$promise
    .then(function (devices) {
      vm.devices = devices;
    });
}

})();
