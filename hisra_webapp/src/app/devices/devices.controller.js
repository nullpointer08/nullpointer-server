(function() {
  'use strict';
// var controllerID = 'DevicesController';
angular.module('hisraWebapp')

.controller('DevicesController', DevicesController);

/* @ngInject */
function DevicesController(/*User*/) {
  var vm = this;

  vm.devices = [];

  // TODO: Get username from auth service
  User.getDevices({username: 'apina'}).$promise
    .then(function (devices) {
      vm.devices = devices;
    });
}

})();
