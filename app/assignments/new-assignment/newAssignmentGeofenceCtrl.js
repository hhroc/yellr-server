'use strict';
var L = L || {};

var map = map || {};
//var featureGroup = featureGroup || {}

//var drawingBox = false;
//var topLeftCord = undefined;
//var bottomRightCord = undefined;

angular
    .module('Yellr')
    .controller('newAssignmentGeofenceCtrl', ['$scope',
    function ($scope) {

        // initialize map

        var main = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
             attribution: 'Map data © OpenStreetMap contributors',
             minZoom: 10,
             maxZoom: 16,
        });

        map = L.map('set-geofence-map', {
            center: [43.2, -77.6],
            zoom: 10,
            layers: [
                main
            ]
        });

        map.drawingBox = false;
        map.geoBox = false;

        var button = $('#geo-fence-button');
        button.on('click', function(e) {
            map.enableDrawing = true;
        });

        map.on('mousedown', function(e) {
            if (map.enableDrawing) {
                map.removeLayer(map.geoBox);
                map.dragging.disable();
                map.drawingBox = true;
                map.topLeftCord = e.latlng;
            }
        });

        map.on('mousemove', function(e) {
           if ( map.enableDrawing && map.drawingBox ) {
               if ( map.geoBox != false ) {
                   map.removeLayer(map.geoBox);
               }
               var bounds = [map.topLeftCord, e.latlng];
               map.geoBox = L.rectangle(bounds, {color:"#ff7800", weight:1});
               map.addLayer(map.geoBox);
           }
        });

        map.on('mouseup', function(e) {
            if ( map.enableDrawing && map.drawingBox ) {
                map.removeLayer(map.geoBox);
                var bounds = [map.topLeftCord, e.latlng];
                map.geoBox = L.rectangle(bounds, {color:"#00FF78", weight:1})
                map.addLayer(map.geoBox);

                $scope.$parent.assignment.geofence = {
                    topLeft: [
                        map.topLeftCord.lat,
                        map.topLeftCord.lng
                    ],
                    bottomRight: [
                        e.latlng.lat,
                        e.latlng.lng
                    ]
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
