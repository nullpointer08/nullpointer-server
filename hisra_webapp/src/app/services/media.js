(function(){
'use strict';

/* global angular */

angular.module('hisraWebapp')

.factory('Media', MediaFactory);

/*@ngInject*/
function MediaFactory($resource, BASE_URL) {
  return $resource(BASE_URL + '/api/user/:username/media/:id', {
    id: '@id'
  });
}

})();
