'use strict';

angular.module('myApp.media', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/media', {
    templateUrl: 'media/media.html',
    controller: 'MediaCtrl'
  });
}])

.controller('MediaCtrl', ['$scope', function($scope) {
	$scope.openFileBrowser = function() {
		document.getElementById('media-add__file').click();
	}
}]);