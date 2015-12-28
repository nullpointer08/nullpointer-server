// TODO move under components; IIFE and other refactoring
(function() {
'use strict';

/* global angular */

angular.module('hisraWebapp')

.factory('Authentication', AuthenticationFactory);

/*@ngInject*/
function AuthenticationFactory($http, $cookieStore, BASE_URL) {

  var userHolder = {
      currentUser: undefined
  };

  var authentication = {};
  authentication.login = Login;
  authentication.logout = Logout;
  authentication.getCurrentUser = GetCurrentUser;

  function Login(username, password, callback) {
      $http.post(BASE_URL + '/api/authentication', { username: username, password: password })
      .success(function (response) {
        if(response.success) {
            var authdata = btoa(username + ':' + password);
            $http.defaults.headers.common['Authorization'] = 'Basic ' + authdata;

            var currentUser = {
                username: username,
                authdata: authdata
            };
            $cookieStore.put('currentUser', currentUser);
            userHolder.currentUser = currentUser;
        }
        callback(response);
      });
  };

  function Logout() {
    delete userHolder.currentUser
    $cookieStore.remove('currentUser');
    $http.defaults.headers.common.Authorization = 'Basic';
  }

  function GetCurrentUser() {
      if(userHolder.currentUser != undefined) {
          return userHolder.currentUser;
      }
      var cookieUser = $cookieStore.get('currentUser');
      if(cookieUser != undefined) {
          return cookieUser;
      }
      return undefined;
  }

  return authentication;
}
})();
