// TODO move under components; IIFE and other refactoring
(function() {
'use strict';

/* global angular */

angular.module('hisraWebapp')

.factory('Device', DeviceFactory);

/*@ngInject*/
function DeviceFactory($resource, BASE_URL) {
  return $resource(BASE_URL + '/api/user/:username/device/:id', {
    id: '@id'
  }, {
    update: {
      method: 'PUT'
    }
  });
}
})();
