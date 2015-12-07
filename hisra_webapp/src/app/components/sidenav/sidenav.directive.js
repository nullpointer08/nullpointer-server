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
    function SideNavController() {
      var sidenav = this;
      sidenav.title = 'SideNav';

    }
  }
})();
