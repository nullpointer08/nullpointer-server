// TODO move under components; IIFE and other refactoring
(function() {
'use strict';

/* global angular */

angular.module('hisraWebapp')

.factory('Device', DeviceFactory)
.factory('Statistics', StatisticsFactory);

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

function StatisticsFactory($resource, BASE_URL) {
  return $resource(BASE_URL + '/api/user/:username/device/:id/statistics', {
    id: '@id'
  });
}

})();
