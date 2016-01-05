(function(){
'use strict';

/* global angular */

angular.module('hisraWebapp')

.factory('Media', MediaFactory)
.factory('MediaTypes', MediaTypesFactory);

/*@ngInject*/
function MediaFactory($resource, BASE_URL) {
  return $resource(BASE_URL + '/api/user/:username/media/:id', {
    id: '@id'
  });
}

function MediaTypesFactory() {
  return {
    types: [
      {
        label: 'Web page',
        fieldName: 'W'
      }, {
        label: 'Video',
        fieldName: 'V',
      }, {
        label: 'Image',
        fieldName: 'I'
      }
    ],
    labelFor: function(fieldName) {
      for(var i=0; i<this.types.length; ++i) {
        if(this.types[i].fieldName == fieldName) {
          return this.types[i].label;
        }
      }
    },
    fieldNameFor: function(label) {
      for(var i=0; i<this.types.length; ++i) {
        if(this.types[i].label == label) {
          return this.types[i].fieldName;
        }
      }
    }
  };
}
})();
