'use strict';

var L = L || {};

angular
    .module('Yellr')
    .controller('viewAssignmentsCtrl',
    ['$scope', '$rootScope', '$location', 'assignmentApiService',
    function ($scope, $rootScope, $location, assignmentApiService) {

        if (!window.loggedIn) {
            $location.path('/login');
            return;
        }
        // initialize map
        var mainTileLayer = new L.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
             attribution: 'Map data © OpenStreetMap contributors',
             minZoom: 4,
             maxZoom: 16
        }),

        map = L.map('assignment-map', {
            center: [41, -77.6],
            zoom: 6,
            layers: [
                mainTileLayer
            ]
        }),

        polygon = {};

        $scope.user = $rootScope.user;

        $scope.$parent.clear();
        $scope.$parent.assignmentsPage = true;

        $scope.showGeofence = function (assignment) {
            var coords = [
                [assignment.top_left_lat, assignment.top_left_lng],
                [assignment.top_left_lat, assignment.bottom_right_lng],
                [assignment.bottom_right_lat, assignment.bottom_right_lng],
                [assignment.bottom_right_lat, assignment.top_left_lng]
            ];

            map.removeLayer(polygon);
            polygon = L.polygon(coords).addTo(map);
        };

        /**
         * Create view assignments function
         *
         * @return void
         */
        assignmentApiService.getAssignments()
        .success(function (data) {
            console.log(data);
            $scope.assignments = data.assignments;
        });

    }]);
