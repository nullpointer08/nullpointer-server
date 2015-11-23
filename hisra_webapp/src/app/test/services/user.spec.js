'use strict';

describe('User API Service', function () {
  var User, httpBackend;

  // Mock dependent resource constructors
  var playlistSpy = jasmine.createSpyObj('Playlist', ['query']);
  var mediaSpy = jasmine.createSpyObj('Media', ['query']);
  var deviceSpy = jasmine.createSpyObj('Device', ['query']);

  beforeEach(module('Playlist', function($provide) {
    $provide.value('Playlist', playlistSpy);
  }));
  beforeEach(module('Media', function($provide) {
    $provide.value('Media', mediaSpy);
  }));
  beforeEach(module('Device', function($provide) {
    $provide.value('Device', deviceSpy);
  }));

  beforeEach(module('ngResource'));
  beforeEach(module('User'));

  beforeEach(inject(function (_User_, $httpBackend) {
    User = _User_;
    httpBackend = $httpBackend;
  }));

  var userJson = {
    'id': 1,
    'username': 'test'
  };

  var newUser = {
    'username': 'test',
    'password': 'password'
  };

  describe('User Object', function () {
    it('should query backend on .get', function () {
      httpBackend.expectGET('/api/user/test').respond(userJson);

      User.get({username: 'test'}).$promise.then(function (response) {
        expect(response).toEqual(jasmine.objectContaining(userJson));
      });

      httpBackend.flush();
    });

    /*it('should save changes on .update', function () {
      httpBackend.expectPUT('/api/user/test/device/1', deviceJson).respond(200);

      var device = new Device(deviceJson);
      device.$update({username:'test'});

      httpBackend.flush();
    });*/

    it('should create new user on .save', function () {
      httpBackend.expectPOST('/api/user/test', newUser).respond(201, userJson);

      User.save({username: 'test'}, newUser).$promise.then(function (response) {
        expect(response).toEqual(jasmine.objectContaining(userJson));
      });

      httpBackend.flush();
    });
  });

  describe('User Resources', function () {
    var user;

    beforeEach(function () {
      user = new User(userJson);
    });

    it('should fetch media on .getMedia', function () {
      user.getMedia();
      expect(mediaSpy.query).toHaveBeenCalledWith({username: user.username});
    });

    it('should fetch playlists on .getPlaylists', function () {
      user.getPlaylists();
      expect(playlistSpy.query).toHaveBeenCalledWith({username: user.username});
    });

    it('should fetch devices on .getDevices', function () {
      user.getDevices();
      expect(deviceSpy.query).toHaveBeenCalledWith({username: user.username});
    });
  });
})
