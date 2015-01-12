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
    }]);
