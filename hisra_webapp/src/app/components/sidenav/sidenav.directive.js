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
    function SideNavController(Authentication, User, webDevTec, $mdSidenav) {
      var sidenav = this;
      sidenav.title = 'Hisra Management';
      sidenav.modules = [];
      sidenav.getLogin = getLogin;
      sidenav.getModules = getWebDevTec;
      sidenav.close = closeNav;
      
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
      }
      
      function closeNav() {
        $mdSidenav('left')
          .close()
          .then(function(){
            $log.debug('closed');
          });
      }
    }
  }
})();
