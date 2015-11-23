'use strict';

describe('Media API Service', function () {
  var Media, httpBackend;

  beforeEach(module('ngResource'));
  beforeEach(module('Media'));

  beforeEach(inject(function (_Media_, $httpBackend) {
    Media = _Media_;
    httpBackend = $httpBackend;
  }));

  var mediaJson = {
    'description': 'A big blue sad face',
    'url': 'http://cdn3.volusion.com/sbcpn.tjpek/v/vspfiles/photos/FACE001C-2.jpg',
    'mediatype': 'P',
    'md5_checksum': 'ac59c6b42a025514e5de073d697b2afb',
    'owner': 12,
    'id': 1,
    'name': 'sad face'
  };

  var newMedia = {
    'url': 'http://cdn3.volusion.com/sbcpn.tjpek/v/vspfiles/photos/FACE001C-2.jpg',
    'mediatype': 'P',
    'name': 'sad face',
    'description': 'A big blue sad face',
    'md5_checksum': 'ac59c6b42a025514e5de073d697b2afb'
  };

  it('should query backend on .get', function () {
    httpBackend.expectGET('/api/user/test/media/1').respond(mediaJson);

    Media.get({id: 1, username: 'test'}).$promise.then(function (response) {
      expect(response).toEqual(jasmine.objectContaining(mediaJson));
    });

    httpBackend.flush();
  });

  it('should fetch array of objects on .query', function () {
    httpBackend.expectGET('/api/user/test/media').respond([{a:'a'}]);

    Media.query({username: 'test'}).$promise.then(function (response) {
      expect(response).toEqual(jasmine.arrayContaining([ jasmine.objectContaining({a: 'a'}) ]));
    });

    httpBackend.flush();
  });

  it('should create new item on .save', function () {
    httpBackend.expectPOST('/api/user/test/media', newMedia).respond(201, mediaJson);

    Media.save({username: 'test'}, newMedia).$promise.then(function (response) {
      expect(response).toEqual(jasmine.objectContaining(mediaJson));
    });

    httpBackend.flush();
  });

  it('should delete media on .delete', function () {
    httpBackend.expectDELETE('/api/user/test/media/1').respond(200);

    var media = new Media({id: 1});
    media.$delete({username: 'test'});

    httpBackend.flush();
  });
})
