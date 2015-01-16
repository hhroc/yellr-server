'use strict';

angular
    .module('Yellr')
    .controller('newAssignmentCtrl', ['$scope', '$rootScope', '$location',
                '$timeout',
    function ($scope, $rootScope, $location, $timeout) {

        if($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;
        $scope.$parent.clear();

        $scope.activeNotification = false;
        $scope.createAssignment = false;
        $scope.addQuestions = false;
        $scope.geofence = false;

        $scope.assignment = {};
        $scope.assignment.questions = [ { text: '', type: 0 } ];

        $scope.notify = function (message) {
            console.log('notify');
            $scope.notificationMessage = message;
            $scope.activeNotification = true;
            console.log($scope.activeNotification);

            $timeout(function () {
                $scope.activeNotification = false;
                console.log($scope.activeNotification);
            }, 1200);
        };

        $scope.validate = function () {
            // Validate create assignment page
            if (angular.isDefined($scope.assignment.name) &&
                $scope.assignment.name !== '' &&

                angular.isDefined($scope.assignment.language) &&
                $scope.assignment.language !== '' &&

                angular.isDefined($scope.assignment.expireDate)) {

                $scope.createAssignment = true;
            } else {
                $scope.createAssignment = false;
            }

            // Validate Questions page
            if (angular.isDefined($scope.assignment.questions) &&
               $scope.assignment.questions.length > 0 &&
               $scope.assignment.questions[0].text !== '' &&
               $scope.assignment.questions[0].type !== 0) {

                $scope.addQuestions = true;
            } else {
                $scope.addQuestions = false;
            }

            // Validate geofence page
            if (angular.isDefined($scope.assignment.geofence)) {
                $scope.geofence = true;
            } else {
                $scope.geofence = false;
            }
        };
    }]);
