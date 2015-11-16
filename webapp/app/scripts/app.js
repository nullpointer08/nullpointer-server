'use strict';

/**
 * @ngdoc overview
 * @name webappApp
 * @description
 * # webappApp
 *
 * Main module of the application.
 */
angular
  .module('webappApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ngMaterial',
    'webappApp.devices',
    'webappApp.media',
    'webappApp.stats',
    'webappApp.main'
  ])
  .config(function ($routeProvider, $mdThemingProvider) {
    $routeProvider.otherwise({redirectTo: '/'});

      $mdThemingProvider.theme('default')
         .primaryPalette('blue')
         .accentPalette('light-green');
  });
