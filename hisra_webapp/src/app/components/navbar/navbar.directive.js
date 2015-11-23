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
    function NavbarController(moment/*, User*/) {
      var vm = this;

      // "vm.creation" is avaible by directive option "bindToController: true"
      vm.relativeDate = moment(vm.creationDate).fromNow();

      vm.title = 'HISRA Management';

      vm.username = 'P. Lace Holder';


      // function getUserName(User)
      // {
      //   return User.resource;
      // }
    }
  }

})();
