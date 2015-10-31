'use strict';

var moment = moment || {},
    async = async || {};

angular
    .module('Yellr')
    .controller('newAssignmentCtrl', ['$scope', '$rootScope', '$location',
                '$timeout', 'assignmentApiService',
    function ($scope, $rootScope, $location, $timeout, assignmentApiService) {

        if (!window.loggedIn) {
            //$location.path('/login');
            window.location = '/login';
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
        $scope.assignment.questions = [{ questionText: '' }];

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
            console.log('$scope.validate()');
            // Validate create assignment page
            if (angular.isDefined($scope.assignment.name) &&
                $scope.assignment.name !== '' &&
                $scope.assignment.questionType !== '' &&
                angular.isDefined($scope.assignment.expireDate)) {

                $scope.createAssignment = true;
                console.log('$scope.createAssignment = true');
            } else {
                $scope.createAssignment = false;
                console.log('$scope.createAssignment = false'); 
            }

            console.log('$scope.assignment:');
            console.log($scope.assignment);
            console.log('$scope.assingment.questions:');
            console.log($scope.assignment.questions)

            // Validate Questions page
            if (angular.isDefined($scope.assignment.questions) &&
               $scope.assignment.questions.length > 0 &&
               $scope.assignment.questions[0].questionText !== '' &&
               //$scope.assignment.questions[0].question_type !== 0 &&
               $scope.assignment.questions[0].languageCode !== '' &&
               $scope.assignment.questions[0].languageCode !== undefined) {
                
                console.log($scope.assignment.questions[0].languageCode);

                $scope.addQuestions = true;
                console.log('$scope.addQuestions = true');
            } else {
                $scope.addQuestions = false;
                console.log('$scope.addQuestions = false');
            }

            // Validate geofence page
            if (angular.isDefined($scope.assignment.geofence)) {
                $scope.geofence = true;
                console.log('$scope.geofence = true');
            } else {
                $scope.geofence = false;
                console.log('$scope.geofence = false');
            }

            if ($scope.createAssignment && $scope.addQuestions &&
                $scope.geofence) {

                $scope.canPublish = true;
                console.log('$scope.canPublish = true');
            }
        };

        /**
         * Publishes the assignment
         *
         * @return void
         */
        $scope.publish = function () {
            
            var exp = moment($scope.assignment.expireDate),
                timeDiff = moment.duration(exp.diff(moment())).asHours();

            $scope.assignment.lifeTime = timeDiff;
            //$scope.assignment.questions = $scope.questions;

            /*
            async.map($scope.assignment.questions,
            function (question, callback) {
                console.log('calling: ', question);
                assignmentApiService.createQuestion(question.language_code,
                    question.question_text, question.description,
                    question.question_type, question.answers)
                .success(function (data) {
                    callback(null, data.question_id);
                });
            },
            function (error, questionIds) {
                assignmentApiService.publishAssignment($scope.assignment.name,
                    timeDiff, questionIds,
                    $scope.assignment.geofence.topLeft.lat,
                    $scope.assignment.geofence.topLeft.lng,
                    $scope.assignment.geofence.bottomRight.lat,
                    $scope.assignment.geofence.bottomRight.lng);
            });
            */

            assignmentApiService.publishAssignment($scope.assignment);

            $location.path('/');
            $scope.notify('Assignment Published');
        };
    }]);
