(function() {
  'use strict';

  angular
    .module('hisraWebapp')
    .controller('MainController', MainController);

  /* @ngInject */
  function MainController(Authentication, $location, $timeout, webDevTec, toastr) {
    var user = Authentication.getCurrentUser();
    console.dir(user);
    if(user === undefined) {
        return $location.path('/login');
    }

    var vm = this;

    vm.modules = [];
    vm.classAnimation = '';
    vm.creationDate = 1447844996577;
    vm.showToastr = showToastr;

    activate();

    function activate() {
      getWebDevTec();
      $timeout(function() {
        vm.classAnimation = 'rubberBand';
      }, 4000);
    }

    function showToastr() {
      toastr.info('Hello!');
      vm.classAnimation = '';
    }

    function getWebDevTec() {
      vm.modules = webDevTec.getTec();

      // angular.forEach(vm.modules, function(mod) {
      //   mod.rank = Math.random();
      // });
    }
  }
})();
