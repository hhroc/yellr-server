'use strict';

angular
    .module('Yellr')
    .controller('newAssignmentQuestionsCtrl', ['$scope', '$timeout',
    function ($scope, $timeout) {
        if(angular.isDefined($scope.$parent.assignment)) {
            $scope.questions = $scope.$parent.assignment.questions;
        } else {
            $scope.questions = [];
        }

        $scope.addQuestion = function () {
            $scope.questions.push({ text: '', type: 1 });
        };

        $scope.addChoice = function (question) {
            if(!angular.isDefined(question.choices)) {
                question.choices = [];
            }

            question.choices.push('');
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
