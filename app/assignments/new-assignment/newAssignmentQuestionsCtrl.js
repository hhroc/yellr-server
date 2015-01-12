'use strict';

angular
    .module('Yellr')
    .controller('newAssignmentQuestionsCtrl', ['$scope',
    function ($scope) {
        $scope.questions = [
            {
                question: '',
                type: 'Full Text'
            }
        ];

        $scope.addQuestion = function () {
            $scope.questions.push({ question: '', type: 'Full Text' });
        };
    }]);
