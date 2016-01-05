(function() {
  'use strict';
  angular.module('hisraWebapp')

  .controller('MediaController', MediaController);

  /* @ngInject */
  function MediaController($http, Authentication, $location, User, Media, BASE_URL) {

    var user = Authentication.getCurrentUser();
    if(user == undefined) {
      return $location.path('/');
    }

    var vm = this;
    vm.media = [];
    vm.BASE_URL = BASE_URL;

    User.getMedia({username: user.username}).$promise
      .then(function (media) {
        vm.media = media;
      });

    vm.removeMedia = function(id) {
      Media.delete({username: user.username, id: id})
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
      //maxChunkSize: 100,
      url: BASE_URL + '/api/chunked_upload/',
      autoUpload: true,
      maxNumberOfFiles: 1,
      beforeSend: function(xhr) {
        xhr.setRequestHeader('Authorization', 'Basic ' + user.authdata);
      },
      done: function(e, data) {
        console.log(e, data);
        $http.post(BASE_URL + '/api/chunked_upload_complete', $.param({
          "upload_id": data.result.upload_id
        }), {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
      }
    })
  }

})();
