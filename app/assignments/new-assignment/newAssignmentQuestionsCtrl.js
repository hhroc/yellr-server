'use strict';

angular
    .module('Yellr')
    .controller('newAssignmentQuestionsCtrl', ['$scope','$rootScope',
                'userApiService',
    function ($scope, $rootScope, userApiService) {

        if(angular.isDefined($scope.$parent.assignment)) {
            $scope.questions = $scope.$parent.assignment.questions;
        } else {
            $scope.questions = [];
        }

        /**
         * Adds a new blank question to the form.
         *
         * @return void
         */
        $scope.addQuestion = function () {
            $scope.questions.push({ question_text: '', question_type: 1 });
        };

        /**
         * Adds a new choice to a given question
         *
         * @param question : the question to add the choice to.
         *
         * @return void
         */
        $scope.addChoice = function (question) {
            if(!angular.isDefined(question.choices)) {
                question.answers = [];
            }

            question.answers.push('');
        };

        /**
         * Saves the current questions
         *
         * @return void
         */
        $scope.save = function (questions) {
            $scope.$parent.assignment.questions = questions;
            $scope.$parent.notify('Saved Questions.');
            $scope.$parent.validate();
        };

        /**
         * Gets all available languages and populates options with them
         *
         * @return void
         */
        $scope.getLanguages = function () {
            userApiService.getLanguages($rootScope.user.token)
            .success(function (data) {
                $scope.languages = data.languages;
            });
        };

        $scope.getLanguages();
    }]);
