// TODO move under components; IIFE and other refactoring
(function() {
'use strict';

/* global angular */

angular.module('hisraWebapp')

.factory('Authentication', AuthenticationFactory);

/*@ngInject*/
function AuthenticationFactory($http, $window, BASE_URL) {

  var userHolder = {
      currentUser: undefined
  };

  var authentication = {};
  authentication.login = Login;
  authentication.logout = Logout;
  authentication.getCurrentUser = GetCurrentUser;

  function Login(username, password) {
      return $http.post(BASE_URL + '/api/authentication', { username: username, password: password })
        .then(function (response) {
          var currentUser = {
            username: username,
            token: response.data.token
          };

          if($window.sessionStorage) {
            $window.sessionStorage.setItem('currentUser', JSON.stringify(currentUser))
          }

          userHolder.currentUser = currentUser;

          $http.defaults.headers.common.Authorization = 'Token ' + currentUser.token;
        });
  }

  function Logout() {
    userHolder.currentUser = undefined;
    if($window.sessionStorage) {
      $window.sessionStorage.setItem('currentUser', undefined);
    }
    delete $http.defaults.headers.common.Authorization;
  }

  function GetCurrentUser() {
      if(userHolder.currentUser !== undefined) {
          return userHolder.currentUser;
      }

      if($window.sessionStorage) {
        var sessionUser = $window.sessionStorage.getItem('currentUser');
        if(sessionUser) {
          sessionUser = JSON.parse(sessionUser);
          $http.defaults.headers.common.Authorization = 'Token ' + sessionUser.token;
          userHolder.currentUser = sessionUser;
          return sessionUser;
        }
      }

      return undefined;
  }

  return authentication;
}
})();
