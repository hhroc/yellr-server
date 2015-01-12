'use strict';

angular
    .module('Yellr')
    .controller('newAssignmentQuestionsCtrl', ['$scope', '$timeout',
    function ($scope, $timeout) {
        $scope.questions = $scope.$parent.assignment.questions || [];

        $scope.addQuestion = function () {
            $scope.questions.push({ text: '', type: 1 });
        };

        $scope.save = function (questions) {
            $scope.$parent.assignment.questions = questions;
            $scope.$parent.notificationMessage = 'Saved Questions.';
            $scope.$parent.activeNotification = true;

            $timeout(function () {
                $scope.$parent.activeNotification = false;
            }, 1200);
        };
    }]);
