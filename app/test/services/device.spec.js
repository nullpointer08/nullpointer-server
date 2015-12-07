'use strict';

describe('Device API Service', function () {
  var Device, httpBackend;

  beforeEach(module('ngResource'));
  beforeEach(module('Device'));

  beforeEach(inject(function (_Device_, $httpBackend) {
    Device = _Device_;
    httpBackend = $httpBackend;
  }));

  var deviceJson = {
    'id': 1,
    'owner': 4,
    'playlist': 4,
    'unique_device_id': 'device_1'
  };

  var newDevice = {
    'playlist': 4,
    'unique_device_id': 'device_1'
  };

  it('should query backend on .get', function () {
    httpBackend.expectGET('/api/user/test/device/1').respond(deviceJson);

    Device.get({id: 1, username: 'test'}).$promise.then(function (response) {
      expect(response).toEqual(jasmine.objectContaining(deviceJson));
    });

    httpBackend.flush();
  });

  it('should fetch array of objects on .query', function () {
    httpBackend.expectGET('/api/user/test/device').respond([{a:'a'}]);

    Device.query({username: 'test'}).$promise.then(function (response) {
      expect(response).toEqual(jasmine.arrayContaining([ jasmine.objectContaining({a: 'a'}) ]));
    });

    httpBackend.flush();
  });

  it('should save changes on .update', function () {
    httpBackend.expectPUT('/api/user/test/device/1', deviceJson).respond(200);

    var device = new Device(deviceJson);
    device.$update({username:'test'});

    httpBackend.flush();
  });

  it('should create new item on .save', function () {
    httpBackend.expectPOST('/api/user/test/device', newDevice).respond(201, deviceJson);

    Device.save({username: 'test'}, newDevice).$promise.then(function (response) {
      expect(response).toEqual(jasmine.objectContaining(deviceJson));
    });

    httpBackend.flush();
  });
})
