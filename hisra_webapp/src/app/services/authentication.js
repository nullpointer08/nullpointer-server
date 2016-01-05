// TODO move under components; IIFE and other refactoring
(function() {
'use strict';

/* global angular */

angular.module('hisraWebapp')

.factory('Authentication', AuthenticationFactory);

/*@ngInject*/
function AuthenticationFactory($http, $cookies, BASE_URL) {

  var userHolder = {
      currentUser: undefined
  };

  var authentication = {};
  authentication.login = Login;
  authentication.logout = Logout;
  authentication.getCurrentUser = GetCurrentUser;

  function Login(username, password) {
      console.log("CALLING LOGIN");
      return $http.post(BASE_URL + '/api/authentication', { username: username, password: password })
        .then(function (response) {
          if(response.data.success) {
              var authdata = btoa(username + ':' + password);
              $http.defaults.headers.common['Authorization'] = 'Basic ' + authdata;

              var currentUser = {
                  username: username,
                  authdata: authdata
              };

              $cookies.putObject('currentUser', JSON.stringify(currentUser));
              userHolder.currentUser = currentUser;
          }
        });
  };

  function Logout() {
    userHolder.currentUser = undefined;
    $cookies.remove('currentUser');
    delete $http.defaults.headers.common['Authorization'];
  }

  function GetCurrentUser() {
      if(userHolder.currentUser != undefined) {
          return userHolder.currentUser;
      }
      var cookieUser = $cookies.getObject('currentUser');
      if(cookieUser != undefined) {
          $http.defaults.headers.common['Authorization'] = 'Basic ' + cookieUser.authdata;
          return cookieUser;
      }
      return undefined;
  }

  return authentication;
}
})();
