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
      console.log("CALLING LOGIN");
      $http.post(BASE_URL + '/api/authentication/', { username: username, password: password })
      .success(function (data, status, headers, config) {
        $window.sessionStorage.token = data.token;
        callback(true);
      })
      .error(function (data, status, headers, config) {
        // Erase the token if the user fails to log in
        delete $window.sessionStorage.token;
        callback(false);
      });
  };

  function Logout() {
    userHolder.currentUser = undefined;
    delete $window.sessionStorage.token;
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
