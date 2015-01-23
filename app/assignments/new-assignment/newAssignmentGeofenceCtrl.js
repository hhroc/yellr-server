'use strict';
var L = L || {};

angular
    .module('Yellr')
    .controller('newAssignmentGeofenceCtrl', ['$scope',
    function ($scope) {

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
    }]);
