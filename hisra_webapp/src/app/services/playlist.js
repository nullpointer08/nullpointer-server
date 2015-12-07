(function(){
'use strict';

/* global angular */

angular.module('hisraWebapp')

.factory('Playlist', PlaylistFactory);

/*@ngInject*/
function PlaylistFactory($resource, BASE_URL) {
  return $resource(BASE_URL + '/api/user/:username/playlist/:id', {
    id: '@id'
  }, {
    update: {
      method: 'PUT'
    }
  });
}
})();
