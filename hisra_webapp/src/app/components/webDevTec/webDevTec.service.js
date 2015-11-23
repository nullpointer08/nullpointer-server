(function() {
  'use strict';

  angular
      .module('hisraWebapp')
      .service('webDevTec', webDevTec);

  /** @ngInject */
  function webDevTec() {
    var data = [
      {
        'title': 'Devices',
        'url': '/#/devices',
        'description': 'Manage devices',
        'icon': 'devices'
      },
      {
        'title': 'Playlists',
        'url': '/#/playlists',
        'description': 'Manage playlists',
        'icon': 'list'
      },
      {
        'title': 'Media',
        'url': '/#/media',
        'description': 'Manage media',
        'icon': 'video_library'
      },
      {
        'title': 'Statistics',
        'url': '/#/stats',
        'description': 'Examine system statistics',
        'icon': 'assessment'
      },

    ];

    this.getTec = getTec;

    function getTec() {
      return data;
    }
  }

})();
