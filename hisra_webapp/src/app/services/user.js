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

    return angular.extend(resource.prototype, {
      getMedia: function(config) {
        config = config || {};
        config.username = config.username || this.username;
        return Media.query(config);
      },
      getPlaylists: function(config) {
        config = config || {};
        config.username = config.username || this.username;
        return Playlist.query(config);
      },
      getDevices: function(config) {
        config = config || {};
        config.username = config.username || this.username;
        return Device.query(config);
      }
    });

  }

})();
