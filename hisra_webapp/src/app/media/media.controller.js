(function() {
  'use strict';
  angular.module('hisraWebapp')

  .controller('MediaController', MediaController);

  /* @ngInject */
  function MediaController(User, Media, BASE_URL) {
    var vm = this;

    vm.media = [];

    vm.BASE_URL = BASE_URL;

    // TODO: Get username from auth service
    User.getMedia({username: 'testy'}).$promise
      .then(function (media) {
        vm.media = media;
      });

    vm.removeMedia = function(id) {
      Media.delete({username: 'testy', id: id})
        .$promise.then(function() {
          vm.media.filter(function(file) {
            return file.id != id;
          })
        })
    }

    vm.openFileBrowser = function () {
      document.getElementById('media-add__file').click();
    };

    $('#media-add__file').fileupload({
      url: BASE_URL + '/api/chunked_upload/',
      autoUpload: true,
      maxNumberOfFiles: 1,
      beforeSend: function(xhr) {
        xhr.setRequestHeader('Authorization', 'Basic dGVzdHk6cGFzcw==');
      },
      done: function(e, data) {
        console.log(data);
      }
    })
  }

})();
