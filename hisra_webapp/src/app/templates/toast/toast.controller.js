(function() {
'use strict';

angular.module('hisraWebapp')
  .controller('ToastController', ToastController);

/* @ngInject */
function ToastController($mdToast) {
    var vm = this;
    
    vm.closeToast = function() {
    $mdToast.hide();
  };
}
})();