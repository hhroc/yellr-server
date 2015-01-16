'use strict';

angular
    .module('Yellr')
    .controller('newAssignmentContentCtrl', ['$scope',
    function ($scope) {
        $scope.format = 'dd-MMMM-yyyy';
        $scope.dateOptions = {
            formatYear: 'yy',
            startingDay: 1
        };

        $scope.save = function (assignment) {
            angular.extend($scope.$parent.assignment, assignment);
            $scope.$parent.notify('Saved Assignment Information.');
            $scope.$parent.validate();
        };
    }]);
