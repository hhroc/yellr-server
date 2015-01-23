'use strict';

angular
    .module('Yellr')
    .controller('newAssignmentContentCtrl', ['$scope', '$location',
    function ($scope, $location) {
        $scope.format = 'dd-MM-yyyy';
        $scope.dateOptions = {
            formatYear: 'yy',
            startingDay: 1
        };

        $scope.save = function (assignment) {
            angular.extend($scope.$parent.assignment, assignment);
            $scope.$parent.notify('Saved Assignment Information.');
            $scope.$parent.validate();
            $location.path('/new-assignment/questions');
        };
    }]);
