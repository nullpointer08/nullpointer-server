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
    function SideNavController(Authentication, User) {
      var sidenav = this;
      sidenav.title = 'SideNav';
      sidenav.getLogin = getLogin;
      
      function getLogin() {
        var user = Authentication.getCurrentUser();
        if(user == undefined) {
          return false;
        } else {
          return true;
        }
      }
    }
  }
})();
