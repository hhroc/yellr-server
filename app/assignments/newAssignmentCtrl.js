'use strict';

var moment = moment || {};

angular
    .module('Yellr')
    .controller('newAssignmentCtrl', ['$scope', '$rootScope', '$location',
                '$timeout', 'assignmentApiService',
    function ($scope, $rootScope, $location, $timeout, assignmentApiService) {

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
        $scope.canPublish = false;

        $scope.assignment = {};
        $scope.assignment.questions = [ { question_text: '' } ];

        /**
         * Utility function which toggles the notification bar.
         *
         * @param message : message which you would like to appear in the
         * notification bar.
         *
         * @return void
         */
        $scope.notify = function (message) {
            $scope.notificationMessage = message;
            $scope.activeNotification = true;

            $timeout(function () {
                $scope.activeNotification = false;
            }, 1200);
        };

        /**
         * Validates each of our sub pages and sets their check value
         * accordingly.
         *
         * @return void
         */
        $scope.validate = function () {
            // Validate create assignment page
            if (angular.isDefined($scope.assignment.name) &&
                $scope.assignment.name !== '' &&

                angular.isDefined($scope.assignment.expireDate)) {

                $scope.createAssignment = true;
            } else {
                $scope.createAssignment = false;
            }

            // Validate Questions page
            if (angular.isDefined($scope.assignment.questions) &&
               $scope.assignment.questions.length > 0 &&
               $scope.assignment.questions[0].question_text !== '' &&
               $scope.assignment.questions[0].question_type !== 0 &&
               $scope.assignment.questions[0].language_code !== '' &&
               $scope.assignment.questions[0].language_code !== undefined) {
                console.log($scope.assignment.questions[0].language_code);

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

            if ($scope.createAssignment && $scope.addQuestions &&
                $scope.geofence) {

                $scope.canPublish = true;
            }
        };

        /**
         * Publishes the assignment
         *
         * @return void
         */
        $scope.publish = function () {
            var exp = moment($scope.assignment.expireDate);
            var timeDiff = moment.duration(exp.diff(moment())).asHours();

            assignmentApiService.publishAssignment($rootScope.user.token,
                timeDiff, $scope.assignment.questions,
                $scope.assignment.geofence.topLeft.lat,
                $scope.assignment.geofence.topLeft.lng,
                $scope.assignment.geofence.bottomRight.lat,
                $scope.assignment.geofence.bottomRight.lng)
            .success(function (data) {
                console.log(data);
            });
        };
    }]);
