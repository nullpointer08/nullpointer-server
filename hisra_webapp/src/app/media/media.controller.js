(function() {
  'use strict';
  angular.module('hisraWebapp')

  .controller('MediaController', MediaController);

  /* @ngInject */
  function MediaController(Authentication, $cookieStore, $location, User, Media, BASE_URL) {

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

    var md5 = "";
    var form_data = [];
    function calculate_md5(file, chunk_size) {
      var slice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice,
          chunks = Math.ceil(file.size / chunk_size),
          current_chunk = 0,
          spark = new SparkMD5.ArrayBuffer();
      function onload(e) {
        spark.append(e.target.result);  // append chunk
        current_chunk++;
        if (current_chunk < chunks) {
          read_next_chunk();
        } else {
          md5 = spark.end();
        }
      }
      function read_next_chunk() {
        var reader = new FileReader();
        reader.onload = onload;
        var start = current_chunk * chunk_size,
            end = Math.min(start + chunk_size, file.size);
        reader.readAsArrayBuffer(slice.call(file, start, end));
      }
      read_next_chunk();
    }
    $("#media-add__file").fileupload({
      url: BASE_URL + '/api/chunked_upload/',
      dataType: "json",
      autoUpload: true,
      maxChunkSize: 100000, // Chunks of 100 kB
      formData: form_data,
      xhrFields: {
        withCredentials: true
      },
      beforeSend: function(xhr) {
        xhr.setRequestHeader('Authorization', 'Basic ' + user.authdata);
      },
      add: function(e, data) { // Called before starting upload
        // If this is the second file you're uploading we need to remove the
        // old upload_id and just keep the csrftoken (which is always first).
        form_data.splice(1);
        calculate_md5(data.files[0], 100000);  // Again, chunks of 100 kB
        data.submit();
      },
      chunkdone: function (e, data) { // Called after uploading each chunk
        if (form_data.length < 2) {
          form_data.push(
            {"name": "upload_id", "value": data.result.upload_id}
          );
        }
      },
      done: function (e, data) { // Called when the file has completely uploaded
        $.ajax({
          beforeSend: function(xhr){
            xhr.setRequestHeader('Authorization', 'Basic ' + user.authdata);
          },
          xhrFields: {
            withCredentials: true
          },
          type: "POST",
            url: BASE_URL + '/api/chunked_upload_complete/',
          data: {
            upload_id: data.result.upload_id,
            md5: md5,
          },
          dataType: "json",
          success: function(data) {
            console.log("SUCCESS");
          }
        });
      },
    });
  }

})();
