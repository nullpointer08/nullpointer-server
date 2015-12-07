'use strict';

describe('Playlist API Service', function () {
  var Playlist, httpBackend;

  beforeEach(module('ngResource'));
  beforeEach(module('Playlist'));

  beforeEach(inject(function (_Playlist_, $httpBackend) {
    Playlist = _Playlist_;
    httpBackend = $httpBackend;
  }));

  var playlistJson = {
    'owner': 21,
    'description': 'All the best stuff',
    'media_schedule_json': '{"fake_playlist_json": "true"}',
    'id': 1,
    'name': 'Cool playlist'
  };

  var newPlaylist = {
    'name': 'Cool playlist',
    'description': 'All the best stuff',
    'media_schedule_json': '{"fake_playlist" : "true"}'
  };

  it('should query backend on .get', function () {
    httpBackend.expectGET('/api/user/test/playlist/1').respond(playlistJson);

    Playlist.get({id: 1, username: 'test'}).$promise.then(function (response) {
      expect(response).toEqual(jasmine.objectContaining(playlistJson));
    });

    httpBackend.flush();
  });

  it('should fetch array of objects on .query', function () {
    httpBackend.expectGET('/api/user/test/playlist').respond([{a:'a'}]);

    Playlist.query({username: 'test'}).$promise.then(function (response) {
      expect(response).toEqual(jasmine.arrayContaining([ jasmine.objectContaining({a: 'a'}) ]));
    });

    httpBackend.flush();
  });

  it('should save changes on .update', function () {
    httpBackend.expectPUT('/api/user/test/playlist/1', playlistJson).respond(200, playlistJson);

    var playlist = new Playlist(playlistJson);
    playlist.$update({username:'test'});

    httpBackend.flush();
  });

  it('should create new item on .save', function () {
    httpBackend.expectPOST('/api/user/test/playlist', newPlaylist).respond(201, playlistJson);

    Playlist.save({username: 'test'}, newPlaylist).$promise.then(function (response) {
      expect(response).toEqual(jasmine.objectContaining(playlistJson));
    });

    httpBackend.flush();
  });
})
