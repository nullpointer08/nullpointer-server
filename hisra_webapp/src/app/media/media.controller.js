(function() {
  'use strict';
  angular.module('hisraWebapp')

  .controller('MediaController', MediaController);

  /* @ngInject */
  function MediaController(/*User*/) {
    var vm = this;

    vm.media = [];

    // TODO: Get username from auth service
    /*User.getMedia({username: 'test'}).$promise
      .then(function (media) {
        vm.media = media;
      });

    vm.openFileBrowser = function () {
      document.getElementById('media-add__file').click();
      alert('click');
    };*/
  }

})();
