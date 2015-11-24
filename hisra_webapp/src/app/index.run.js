(function() {
  'use strict';

  angular
    .module('hisraWebapp')
    .run(runBlock);

  /** @ngInject */
  function runBlock($log) {

    $log.debug('runBlock end');
  }

})();
