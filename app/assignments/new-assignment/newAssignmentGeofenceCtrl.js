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

        /*

        var map = L.mapbox.map('set-geofence-map', window.MAPBOX_MAP_ID, {
            accessToken: window.MAPBOX_API_KEY
        })
          .setView([38.89399, -77.03659], 17);

        var featureGroup = L.featureGroup().addTo(map);

        // Creates the sidebar with our drawing tools
        var drawControl = new L.Control.Draw({
            edit: {
                featureGroup: featureGroup
            }
        }).addTo(map);

        // Listener for a new shape created on map
        map.on('draw:created', function (e) {
            featureGroup.addLayer(e.layer);

            $scope.$parent.assignment.geofence = {
                topLeft: e.layer._latlngs[1],
                bottomRight: e.layer._latlngs[3]
            };

            // Since this event is out of angular's standard event listener
            // loop we need to manually apply the change.
            $scope.$apply(function () {
                $scope.$parent.notify('Saved Geofence.');
                $scope.$parent.validate();
            });
        });

        */
 
        // initialize map
        //console.log('creating map');

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

        //featureGroup = L.featureGroup().addTo(map);

        map.drawingBox = false;
        map.geoBox = false;

        map.on('mousedown', function(e) {
            if (e.originalEvent.ctrlKey) {
                //if ( map.geoBox != false ) {
                    map.removeLayer(map.geoBox);
                //}
                map.dragging.disable();
                map.drawingBox = true;
                map.topLeftCord = e.latlng;
            }
        });

        map.on('mousemove', function(e) {
           if ( map.drawingBox == true ) {
               if ( map.geoBox != false ) {
                   map.removeLayer(map.geoBox);
               }
               var bounds = [map.topLeftCord, e.latlng];
               map.geoBox = L.rectangle(bounds, {color:"#ff7800", weight:1});
               map.addLayer(map.geoBox);
           }
        });

        map.on('mouseup', function(e) {
            if (e.originalEvent.ctrlKey) {
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
                map.dragging.enable();
            }
        });

        

        /*
        console.log('creating areaSelect()');
        var areaSelect = L.areaSelect({width:200, height:250});

        console.log('setting on change for areaSelect');
        areaSelect.on('change', function() {
            var bounds = this.getBounds();
            //$('#result .sw').val(bounds.getSouthWest().lat + ', ' + bounds.getSouthWest().lng);
            //$('#result .ne').val(bounds.getNorthEast().lat + ', ' + bounds.getNorthEast().lng);
            console.log(bounds);
        });

        console.log('adding areaSelect to map');
        areaSelect.addTo(map);
        console.log('areaSelect added to map');
        */
        

    }]);
