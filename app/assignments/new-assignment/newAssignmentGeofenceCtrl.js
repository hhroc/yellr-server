'use strict';
var L = L || {},
    mainTileLayer = {};

angular
    .module('Yellr')
    .controller('newAssignmentGeofenceCtrl', ['$scope',
    function ($scope) {

        // initialize map
        var mainTileLayer = new L.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
             attribution: 'Map data © OpenStreetMap contributors',
             minZoom: 4,
             maxZoom: 16
        }),

        map = L.map('set-geofence-map', {
            center: [41, -77.6],
            zoom: 6,
            layers: [
                mainTileLayer
            ]
        });

        map.drawingBox = false;
        map.geoBox = false;

        $('#geo-fence-button').on('click', function (e) {
            map.enableDrawing = true;
        });

        map.on('mousedown', function (e) {
            if (map.enableDrawing) {
                map.removeLayer(map.geoBox);
                map.dragging.disable();
                map.drawingBox = true;
                map.topLeftCord = e.latlng;
            }
        });

        map.on('mousemove', function (e) {
            if (map.enableDrawing && map.drawingBox) {
                map.removeLayer(map.geoBox);
                map.geoBox = L.rectangle([map.topLeftCord, e.latlng], {color:'#ff7800', weight:1});
                map.addLayer(map.geoBox);
            }
        });

        map.on('mouseup', function (e) {
            if (map.enableDrawing && map.drawingBox) {
                map.removeLayer(map.geoBox);
                var bounds = [map.topLeftCord, e.latlng];
                map.geoBox = L.rectangle(bounds, {color:'#00FF78', weight:1});
                map.addLayer(map.geoBox);

                $scope.$parent.assignment.geofence = {
                    topLeft: {
                        lat: map.topLeftCord.lat,
                        lng: map.topLeftCord.lng
                    },
                    bottomRight: {
                        lat: e.latlng.lat,
                        lng: e.latlng.lng
                    }
                };

                // Since this event is out of angular's standard event listener
                // loop we need to manually apply the change.
                $scope.$apply(function () {
                    $scope.$parent.notify('Saved Geofence.');
                    $scope.$parent.validate();
                });

                map.drawingBox = false;
                map.enableDrawing = false;
                map.dragging.enable();
            }
        });

    }]);
