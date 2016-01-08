(function() {
  'use strict';

  angular
    .module('hisraWebapp')
    .config(config);

  /** @ngInject */
  function config($logProvider, $mdThemingProvider, toastrConfig) {
    // Enable log
    $logProvider.debugEnabled(true);

    $mdThemingProvider.theme('default')
      .primaryPalette('blue')
      .accentPalette('light-green');

    // Set options third-party lib
    toastrConfig.allowHtml = true;
    toastrConfig.timeOut = 3000;
    toastrConfig.positionClass = 'toast-top-right';
    toastrConfig.preventDuplicates = true;
    toastrConfig.progressBar = true;

  }

})();
