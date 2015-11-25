(function() {
   'use strict'
   angular.module('hisraWebapp')
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
        controllerAs: 'vm',
        bindToController: true
      };

      return directive;

      // @ngInject
      function SideNavController() {
         // var vm = this;

      }
   }
})();
