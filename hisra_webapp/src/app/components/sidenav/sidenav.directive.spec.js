(function() {
  'use strict';
  describe('directive sidenav', function (){
    var vm;
    var el;

    beforeEach(module('hisraWebapp'));
    beforeEach(inject(function($compile, $rootScope) {
      el = angular.element('<sidenav></sidenav>');

      $compile(el)($rootScope.$new());
      $rootScope.$digest();
      vm = el.isolateScope().vm;
    }));

    it('should be compiled', function() {
      expect(el.html().not.toEqual(null));
    });

    it('should have isolated scope with instanciate members', function() {
      expect(vm).toEqual(jasmine.any(Object));
    });
  });
}();
