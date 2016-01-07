(function(){
'use strict';

/* global angular */

angular.module('hisraWebapp')

.factory('Notification', NotificationFactory);

/*@ngInject*/
function NotificationFactory($timeout, BASE_URL) {

  return {
    createNotifier: function() {
      return {
        fadeTime: 6000,
        visibility: {
          failure: false,
          success: false
        },
        message: {
          failure: 'Default success',
          success: 'Default fail'
        },
        showMessage: function(type, message) {
          this.visibility[type] = true;
          this.message[type] = message;
          var struct = this;
          $timeout(function() {
            struct.hideMessage(type);
            console.log("Timeout called");
          }, struct.fadeTime);
        },
        hideMessage: function(type) {
          this.visibility[type] = false;
        },
        showSuccess: function(message) {
          this.showMessage('success', message);
        },
        showFailure: function(message) {
          this.showMessage('failure', message);
        },
        isVisible: function(type) {
            return this.visibility[type];
        },
        isSuccessVisible: function() {
          return this.isVisible('success');
        },
        isFailureVisible: function() {
          return this.isVisible('failure');
        },
        hideSuccess: function() {
          this.hideMessage('success');
        },
        hideFailure: function() {
          this.hideMessage('failure');
        },
        getMessage: function(type) {
          return this.message[type];
        },
        getSuccessMessage: function() {
          return this.getMessage('success');
        },
        getFailureMessage: function() {
          return this.getMessage('failure');
        }
      };
    }
  };

}
})();
