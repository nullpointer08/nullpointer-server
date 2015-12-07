(function(){
  'use strict';
  /* global angular */

  angular.module('hisraWebapp')
  .factory('User', UserFactory);

  /*@ngInject*/
  function UserFactory($resource, Media, Playlist, Device, BASE_URL) {
    var resource = $resource(BASE_URL + '/api/user/:username', {
      username: '@username'
    });


    angular.extend(resource.prototype, {
      getMedia: function() {
        return Media.query({username: this.username});
      },
      getPlaylists: function() {
        return Playlist.query({username: this.username});
      },
      getDevices: function() {
        return Device.query({username: this.username});
      }
    });

    return resource;
  }

})();
