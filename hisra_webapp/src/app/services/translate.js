(function() {
'use strict';

/* global angular */

angular.module('hisraWebapp')
.config(
  /* @ngInject */
  function($translateProvider) {
    $translateProvider.translations('en', {
      /* Account */
      'FIRSTNAME': 'First name',
      'LASTNAME': 'Last name',
      'EMAIL': 'Email',
      'LOGOUT': 'Logout',

      /* Devices */
      'YOURDEV': 'Your devices',
      'DEVICE': 'Device',
      'PLAYLIST': 'Playlist',
      'CLEARSELECT': 'Clear Selections',
      'SETDEVPLAYLIST': 'Set Device Playlist',
      'PLAYLISTDETAIL': 'Playlist details',
      'NAME': 'Name',
      'DESCRIPTION': 'Description',
      'CONFIRMINUSE': 'Confirmed in use by device',
      'SCHEDULE': 'Schedule',
      'URL': 'URL',
      'TYPE': 'Type',
      'DISPTIME': 'Display time',

      /* Login */
      'LOGIN': 'Login',
      'USERNAME': 'Username',
      'PASSWORD': 'Password',

      /* Media */
      'UPLOADHINT': 'Add media by dragging and dropping it here',
      'UPLOADHINT2': 'or press the "add" button',
      'ADDMEDIA': 'Add Media',
      'ADDEDMEDIA': 'Added media',
      'SHOWVIDEOS': 'Show videos',
      'SHOWIMAGES': 'Show images',
      'SHOWWEB': 'Show web pages',
      'FILTERMEDIA': 'Filter media',
      'ACTIONS': 'Actions',
      'REMOVE': 'Remove',
      'ADDEXTERNAL': 'Add external media',
      'SELECTTYPE': 'Select Type',

      /* Playlist details */
      'SCHEDULEHINT': 'Schedule: (drag and drop to change order)',
      'AVAILABLEMEDIA': 'Available media',
      'ADDTOPLAYLIST': 'Add to playlist',
      'SAVECHANGES': 'Save changes',
      'DELETEPLAYLIST': 'Delete playlist',

      /* Playlists */
      'PLAYLISTS': 'Playlists',
      'ITEMS': 'Items',
      'DETAILS': 'Details',
      'NEWPLAYLIST': 'New playlist',

      /* Stats */
      'CATEGORY': 'Category',
      'TIMESTAMP': 'Timestamp'
    });

    $translateProvider.preferredLanguage('en');
  }
)

})();
