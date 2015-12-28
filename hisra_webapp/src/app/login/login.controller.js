(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('LoginController', LoginController);

/* @ngInject */
function LoginController(User) {
  var vm = this;

  vm.devices = [];

  // TODO: Get username from auth service
  User.getDevices({username: 'testy'}).$promise
    .then(function (devices) {
      vm.devices = devices;
    });
}

})();
