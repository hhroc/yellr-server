'use strict';

angular
    .module('Yellr')
    .controller('newAssignmentContentCtrl', ['$scope', '$location',
    function ($scope, $location) {
        $('#due-date-datepicker').fdatepicker({
            format: 'mm-dd-yyyy'
        });

        $scope.save = function (assignment) {
            angular.extend($scope.$parent.assignment, assignment);
            $scope.$parent.notify('Saved Assignment Information.');
            $scope.$parent.validate();
            $location.path('/new-assignment/questions');
        };
    }]);
