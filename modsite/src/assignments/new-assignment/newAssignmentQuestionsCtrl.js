'use strict';

angular
    .module('Yellr')
    .controller('newAssignmentQuestionsCtrl', ['$scope','$rootScope',
                '$location', 'userApiService',
    function ($scope, $rootScope, $location, userApiService) {

        if (angular.isDefined($scope.$parent.assignment)) {
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
            $scope.questions.push({ questionText: '', questionType: 1 });
        };

        /**
         * Adds a new answer to a given question
         *
         * @param question : the question to add the answer to.
         *
         * @return void
         */
        $scope.addAnswer= function (question) {
            console.log('addaAnswer');
            console.log(question.answers);

            if (!angular.isDefined(question.answers)) {
                question.answers = [];
            }

            question.answers.push('');
            console.log(question.answers);
        };

        /**
         * Saves the current questions
         *
         * @return void
         */
        $scope.save = function (questions) {
            console.log('$scope.save()');
            $scope.$parent.assignment.questions = questions;
            $scope.$parent.notify('Saved Questions.');
            $scope.$parent.validate();
            $location.path('/new-assignment/geofence');
        };

        $scope.deleteQuestion = function (index) {
            console.log(index);
            $scope.questions.splice(index, 1);
            console.log($scope.questions);
        };

        /**
         * Gets all available languages and populates options with them
         *
         * @return void
         */
        //$scope.getLanguages = function () {
        //    userApiService.getLanguages()
        //    .success(function (data) {
        //        $scope.languages = data.languages;
        //    });
        //};

        //$scope.getLanguages();
    }]);
