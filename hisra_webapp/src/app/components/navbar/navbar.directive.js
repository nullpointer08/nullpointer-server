(function() {
  'use strict';

  angular
    .module('hisraWebapp')
    .directive('acmeNavbar', acmeNavbar);

  /** @ngInject */
  function acmeNavbar() {
    var directive = {
      restrict: 'E',
      templateUrl: 'app/components/navbar/navbar.html',
      scope: {
          creationDate: '='
      },
      controller: NavbarController,
      controllerAs: 'vm',
      bindToController: true
    };

    return directive;

    /** @ngInject */
    function NavbarController(moment, User, Authentication, $mdSidenav) {
      var vm = this;

      vm.getLogin = getLogin;
      vm.toggleSidenav = toggleSidenav;

      vm.getUsername = function () {
          var user = Authentication.getCurrentUser();
          if(user === undefined) {
              return 'Anonymous';
          }
          return user.username;
      };

      // "vm.creation" is avaible by directive option "bindToController: true"
      vm.relativeDate = moment(vm.creationDate).fromNow();
      vm.title = 'HISRA Management';

      function getLogin() {
        var user = Authentication.getCurrentUser();
        if(user === undefined) {
          return false;
        } else {
          return true;
        }
      }

      function toggleSidenav() {
        $mdSidenav('left')
          .toggle()
          .then(function(){
            //$log.debug('toggled');
          });
      }
    }
  }

})();
