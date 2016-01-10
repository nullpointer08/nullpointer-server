(function() {
  'use strict'
  angular
    .module('hisraWebapp')
    .directive('sideNav', sideNav);

    // @ngInject
    function sideNav() {
      var directive = {
      restrict: 'E',
      templateUrl: 'app/components/sidenav/sidenav.html',
      //   scope: {
      //       creationDate: '='
      //   },
      controller: SideNavController,
      controllerAs: 'sidenav',
      bindToController: true
    };

    return directive;

      // @ngInject
    function SideNavController(Authentication, User, webDevTec) {
      var sidenav = this;
      sidenav.title = 'SideNav';
      sidenav.modules = [];
      sidenav.getLogin = getLogin;
      sidenav.getModules = getWebDevTec;
      
      activate();
      
      function activate() {
        getWebDevTec();
      }
      
      function getLogin() {
        var user = Authentication.getCurrentUser();
        if(user == undefined) {
          return false;
        } else {
          return true;
        }
      }
      
      function getWebDevTec() {
        sidenav.modules = webDevTec.getTec();
  
        // angular.forEach(vm.modules, function(mod) {
        //   mod.rank = Math.random();
        // });
      }
    }
  }
})();
